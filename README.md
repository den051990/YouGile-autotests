# Автотесты для веб-приложения YouGile (Дипломный проект)

Проект содержит набор независимых автоматизированных UI- и API-тестов для проверки функционала авторизации, управления проектами, досками, колонками и задачами в сервисе YouGile.

## Стек технологий
- Python 3.11+
- Pytest
- Selenium WebDriver (паттерн Page Object)
- Requests
- Allure Report

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/den051990/YouGile-autotests.git
   cd YouGile-autotests
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   # Для Windows:
   venv\Scripts\activate
   # Для Linux/macOS:
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте файл `.env` в корне проекта и укажите ваши тестовые данные:
   ```env
   YOUGILE_EMAIL=ваш_email
   YOUGILE_PASSWORD=ваш_пароль
   YOUGILE_TOKEN=ваш_api_токен
   ```

5. Запустите тесты (результаты сохранятся в папку `allure-results`):
   ```bash
   pytest
   ```

6. Сгенерируйте и откройте отчет Allure:
   ```bash
   allure serve allure-results
   ```
