import pytest  # Импортируем pytest
from _pytest.fixtures import SubRequest  # Импортируем класс SubRequest для аннотации
from playwright.sync_api import Playwright, Page  # Импортируем класс страницы, будем использовать его для аннотации типов

from pages.authentication.registration_page import RegistrationPage
from tools.playwright.pages import initialize_playwright_page

from config import settings
from tools.routes import AppRoute


@pytest.fixture(params=settings.browsers)  # Объявляем фикстуру, по умолчанию скоуп function, то что нам нужно
def chromium_page(request: SubRequest, playwright: Playwright) -> Page:  # Аннотируем возвращаемое фикстурой значение
    yield from initialize_playwright_page(
        playwright,
        test_name=request.node.name,
        browser_type=request.param
    )

@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):
    browser = playwright.chromium.launch(headless=settings.headless)
    context = browser.new_context(base_url=settings.get_base_url())
    page = context.new_page()

    # Работаем с регистрационной страницей через Page Object
    registration_page = RegistrationPage(page=page)
    registration_page.visit(AppRoute.REGISTRATION)
    registration_page.registration_form.fill(
        email=settings.test_user.email,
        username=settings.test_user.username,
        password=settings.test_user.password
    )
    registration_page.click_registration_button()

    context.storage_state(path=settings.browser_state_file)
    browser.close()

@pytest.fixture(params=settings.browsers)
def chromium_page_with_state(initialize_browser_state, request: SubRequest, playwright: Playwright) -> Page:
    yield from initialize_playwright_page(
        playwright,
        test_name=request.node.name,
        browser_type=request.param,
        storage_state=settings.browser_state_file
    )