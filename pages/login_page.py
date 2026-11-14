from typing import Tuple
import allure
from selenium.webdriver.common.by import By
from config.config import Config
from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "input[type='password']")
    SUBMIT_BUTTON: Tuple[str, str] = (By.XPATH, "//div[@role='button'][.//div[text()='Войти']]")

    @allure.step("Открыть страницу авторизации YouGile")
    def open_login_page(self) -> None:
        self.open(f"{Config.BASE_UI_URL}/team")

    @allure.step("Выполнить авторизацию с email '{email}'")
    def login(self, email: str, password: str) -> None:
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)
