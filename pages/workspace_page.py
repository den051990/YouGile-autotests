from typing import Tuple
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class WorkspacePage(BasePage):
    MY_COMPANY_TAB: Tuple[str, str] = (By.XPATH, "//*[contains(text(), 'Моя компания')]")
    ADD_PLUS_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-testid='add-project-button']")
    PROJECT_WITH_TASKS_ITEM: Tuple[str, str] = (By.XPATH, "//*[contains(text(), 'Проект с задачами')]")
    PROJECT_NAME_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "input[placeholder*='Введите название проекта']")
    SUBMIT_PROJECT_BTN: Tuple[str, str] = (By.XPATH, "//div[@role='button'][.//div[text()='Добавить проект с задачами']]")


    ADD_TASK_BTN: Tuple[str, str] = (By.XPATH, "//*[contains(text(), 'Добавить задачу')]")
    TASK_NAME_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "[data-testid='board-task-input-name']")

    CREATE_COLUMN_BTN: Tuple[str, str] = (By.XPATH, "//div[@role='button'][.//span[text()='Создать колонку']]")
    COLUMN_NAME_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "[data-testid='add-column-textarea']")


    RENAME_MENU_ITEM: Tuple[str, str] = (By.CSS_SELECTOR, "[data-testid='menu-item-edit']")
    RENAME_PROJECT_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "input[placeholder='Название проекта']")
    SAVE_RENAME_BTN: Tuple[str, str] = (By.XPATH, "//div[@role='button'][.//span[text()='Сохранить']]")

    @allure.step("Проверить загрузку рабочего пространства после авторизации")
    def is_loaded(self) -> bool:
        return self.find_element(self.MY_COMPANY_TAB).is_displayed()

    @allure.step("Создать 'Проект с задачами' с названием '{project_name}'")
    def create_project(self, project_name: str) -> None:
        self.click(self.ADD_PLUS_BUTTON)
        self.click(self.PROJECT_WITH_TASKS_ITEM)
        self.send_keys(self.PROJECT_NAME_INPUT, project_name)
        self.click(self.SUBMIT_PROJECT_BTN)

    @allure.step("Открыть проект '{project_name}' в левом меню")
    def open_project(self, project_name: str) -> None:
        locator: Tuple[str, str] = (By.XPATH, f"//*[contains(text(), '{project_name}')]")
        self.click(locator)

    @allure.step("Создать задачу '{task_title}' в колонке")
    def create_task(self, task_title: str) -> None:
        self.click(self.ADD_TASK_BTN)
        task_input = self.find_element(self.TASK_NAME_INPUT)
        task_input.send_keys(task_title)
        task_input.send_keys(Keys.ENTER)

    @allure.step("Создать новую колонку '{column_title}'")
    def create_column(self, column_title: str) -> None:
        self.click(self.CREATE_COLUMN_BTN)
        col_input = self.find_element(self.COLUMN_NAME_INPUT)
        col_input.send_keys(column_title)
        col_input.send_keys(Keys.ENTER)

    @allure.step("Переименовать проект '{old_name}' в '{new_name}'")
    def rename_project(self, old_name: str, new_name: str) -> None:
        self.click(self.MY_COMPANY_TAB)
        dots_locator: Tuple[str, str] = (
            By.XPATH,
            f"//div[@data-testid='project-card'][.//div[@data-testid='project-title' and text()='{old_name}']]//div[@data-testid='project-card-menu-button']"
        )
        self.click(dots_locator)
        self.click(self.RENAME_MENU_ITEM)
        self.send_keys(self.RENAME_PROJECT_INPUT, new_name)
        self.click(self.SAVE_RENAME_BTN)

    @allure.step("Проверить, что текст '{text}' отображается на странице")
    def is_text_visible(self, text: str) -> bool:
        locator: Tuple[str, str] = (By.XPATH, f"//*[contains(text(), '{text}')]")
        return self.find_element(locator).is_displayed()
