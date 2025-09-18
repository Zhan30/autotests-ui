from playwright.sync_api import Page, Locator, expect


class BaseElement:
    def __init__(self, page: Page, locator: str, name: str):
        self.page = page
        self.name = name
        self.locator = locator

        # Метод принимает кейворд аргументы (kwargs)

    def get_locator(self, **kwargs) -> Locator:  # объект Locator для взаимодействия с элементом
        # Инициализирует объект локатора, подставляя динамические значения в локатор.
        locator = self.locator.format(**kwargs)
        # Возвращаем объект локатора
        return self.page.get_by_test_id(locator)

    def click(self, **kwargs):
        # "Лениво" инициализируем локатор
        locator = self.get_locator(**kwargs)
        # Выполняем нажатие на элемент
        locator.click()

    def check_visible(self, **kwargs):
        # Инициализируем локатор "лениво"
        locator = self.get_locator(**kwargs)
        # Проверяем, что элемент виден на странице
        expect(locator).to_be_visible()

    def check_have_text(self, text: str, **kwargs):
        locator = self.get_locator(**kwargs)
        expect(locator).to_have_text(text)