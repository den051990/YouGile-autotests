from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, Config.DEFAULT_TIMEOUT)

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: Tuple[str, str]) -> None:
        element: WebElement = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator: Tuple[str, str], text: str) -> None:
        element: WebElement = self.find_element(locator)
        element.clear()
        element.send_keys(text)
