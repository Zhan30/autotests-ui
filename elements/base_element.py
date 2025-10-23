import allure
from playwright.sync_api import Page, Locator, expect
from ui_coverage_tool import ActionType, SelectorType

# Импортируем трекер покрытия — основной интерфейс для логирования покрытых элементов
from elements.ui_coverage import tracker

from tools.logger import get_logger

logger = get_logger("BASE_ELEMENT")

class BaseElement:
    def __init__(self, page: Page, locator: str, name: str):
        self.page = page
        self.name = name
        self.locator = locator

    @property
    def type_of(self) -> str:  # Добавили свойство type_of
        return "base element"

        # Метод принимает кейворд аргументы (kwargs)

    def get_locator(self, nth: int = 0, **kwargs) -> Locator:  # объект Locator для взаимодействия с элементом
        # Добавляем аргумент nth со значением по умолчанию 0
        # Инициализирует объект локатора, подставляя динамические значения в локатор
        locator = self.locator.format(**kwargs)
        step = f'Getting locator with "data-testid={locator}" at index "{nth}"'

        with allure.step(step):  # Добавили шаг
            logger.info(step) # Добавили логирование
            # Возвращаем объект локатора
            return self.page.get_by_test_id(locator).nth(nth)  # Теперь выбираем элемент по индексу

    def get_raw_locator(self, nth: int = 0, **kwargs) -> str:
        # Возвращает строковое XPath-представление локатора для покрытия.
        # Важно: Playwright сам не даёт доступ к исходному локатору, поэтому мы формируем его вручную.
        # Используем XPath, так как он легко поддерживает индексацию ([n+1]).
        return f"//*[@data-testid='{self.locator.format(**kwargs)}'][{nth + 1}]"

    def track_coverage(self, action_type: ActionType, nth: int = 0, **kwargs):
        # Трекает действие над элементом, отправляя данные в coverage-трекер.
        # Передаётся:
        # - XPath-селектор
        # - Тип действия (click, visible, text и другие)
        # - Тип селектора (XPATH)
        tracker.track_coverage(
            selector=self.get_raw_locator(nth, **kwargs),
            action_type=action_type,
            selector_type=SelectorType.XPATH
        )

    def click(self, nth: int = 0, **kwargs):
        step = f'Clicking {self.type_of} "{self.name}"'

        with allure.step(step):  # Добавили шаг
            # "Лениво" инициализируем локатор
            # Добавили аргумент nth и передаем его в get_locator
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.click()

        # После успешного клика трекаем действие как CLICK
        self.track_coverage(ActionType.CLICK, nth, **kwargs)

    def check_visible(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is visible'

        with allure.step(step):  # Добавили шаг
            # Инициализируем локатор "лениво"
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_be_visible()

        # Трекаем видимость как VISIBLE
        self.track_coverage(ActionType.VISIBLE, nth, **kwargs)

    def check_have_text(self, text: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" has text "{text}"'

        with allure.step(step):  # Добавили шаг
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_text(text)

        # Трекаем видимость как TEXT
        self.track_coverage(ActionType.TEXT, nth, **kwargs)