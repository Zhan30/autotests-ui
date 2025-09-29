import allure
import pytest  # Импортируем pytest
from _pytest.fixtures import SubRequest  # Импортируем класс SubRequest для аннотации
from playwright.sync_api import Playwright, Page  # Имопртируем класс страницы, будем использовать его для аннотации типов

from pages.authentication.registration_page import RegistrationPage


@pytest.fixture  # Объявляем фикстуру, по умолчанию скоуп function, то что нам нужно
def chromium_page(request: SubRequest, playwright: Playwright) -> Page:  # Аннотируем возвращаемое фикстурой значение
    browser = playwright.chromium.launch(headless=False) # Запускаем браузер
    context = browser.new_context()  # Создаем контекст для новой сессии браузера
    context.tracing.start(screenshots=True, snapshots=True, sources=True)  # Включаем трейсинг
    yield browser.new_page()  # Передаем страницу для использования в тесте

    # В данном случае request.node.name содержит название текущего автотеста
    context.tracing.stop(path=f'./tracing/{request.node.name}.zip')  # Сохраняем трейсинг в файл
    browser.close()  # Закрываем браузер после выполнения тестов

    allure.attach.file(f'./tracing/{request.node.name}.zip', name='trace', extension='zip')

@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # Работаем с регистрационной страницей через Page Object
    registration_page = RegistrationPage(page=page)
    registration_page.visit('https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/registration')
    registration_page.registration_form.fill(email='user.name@gmail.com', username='username', password='password')
    registration_page.click_registration_button()

    context.storage_state(path="browser-state.json")
    browser.close()

@pytest.fixture
def chromium_page_with_state(initialize_browser_state, request: SubRequest, playwright: Playwright) -> Page:  # Добавили аргумент request
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="browser-state.json")  # Создаем контекст для новой сессии браузера
    context.tracing.start(screenshots=True, snapshots=True, sources=True)  # Включаем трейсинг

    yield context.new_page()  # Открываем новую страницу в контексте

    context.tracing.stop(path=f'./tracing/{request.node.name}.zip')  # Сохраняем трейсинг в файл
    browser.close()  # Закрываем браузер

    allure.attach.file(f'./tracing/{request.node.name}.zip', name='trace', extension='zip')