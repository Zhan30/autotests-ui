from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    # Открываем браузер и создаем новую страницу
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # Переходим на страницу входа
    page.goto(
        "https://nikita-filonov.github.io/qa-automation-engineer-ui-course/#/auth/login",
        wait_until='networkidle'  # Ждем полной загрузки страницы
    )

    # Выполняем JS-код для замены текста заголовка
    page.evaluate(
        # Принимаем аргумент в JS функции
        """
        (text) => { 
        const title = document.getElementById('authentication-ui-course-title-text');
        title.textContent = text;
        }
        """,
    'New Text'  # Передаём аргумент из Python
    )

    # Добавляем паузу для наглядности
    page.wait_for_timeout(5000)