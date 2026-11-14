import time
import allure
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import Config
from pages.login_page import LoginPage
from pages.workspace_page import WorkspacePage


@allure.epic("YouGile UI")
@allure.feature("Позитивные функциональные тесты (по кейсам Test IT)")
class TestYouGileUI:

    @allure.title("UI-1: Авторизация на портале YouGile")
    def test_user_authorization(self, driver: WebDriver) -> None:
        login_page = LoginPage(driver)
        login_page.open_login_page()
        login_page.login(Config.USER_EMAIL, Config.USER_PASSWORD)

        workspace = WorkspacePage(driver)
        assert workspace.is_loaded(), "После авторизации не открылось рабочее пространство"

    @allure.title("UI-2: Создание нового 'Проекта с задачами'")
    def test_create_project_with_tasks(self, logged_in_driver: WebDriver) -> None:
        workspace = WorkspacePage(logged_in_driver)
        project_name: str = f"Диплом {int(time.time())}"

        workspace.create_project(project_name)
        assert workspace.is_text_visible("Новая колонка"), "Автоматическая колонка 'Новая колонка' не создалась"

    @allure.title("UI-3: Создание новой задачи в колонке проекта")
    def test_create_task_in_column(self, logged_in_driver: WebDriver, temp_ui_project: str) -> None:
        workspace = WorkspacePage(logged_in_driver)
        workspace.open_project(temp_ui_project)

        task_name: str = "Написать тест-план"
        workspace.create_task(task_name)
        assert workspace.is_text_visible(task_name), f"Задача '{task_name}' не отобразилась в колонке"

    @allure.title("UI-4: Создание новой колонки в проекте")
    def test_create_new_column(self, logged_in_driver: WebDriver, temp_ui_project: str) -> None:
        workspace = WorkspacePage(logged_in_driver)
        workspace.open_project(temp_ui_project)

        column_name: str = "Тест-план"
        workspace.create_column(column_name)
        assert workspace.is_text_visible(column_name), f"Колонка '{column_name}' не создалась"

    @allure.title("UI-5: Переименование проекта через раздел 'Моя компания'")
    def test_rename_project(self, logged_in_driver: WebDriver, temp_ui_project: str) -> None:
        workspace = WorkspacePage(logged_in_driver)
        new_project_name: str = f"{temp_ui_project} YouGile"

        workspace.rename_project(temp_ui_project, new_project_name)
        assert workspace.is_text_visible(new_project_name), "Название проекта не обновилось"
