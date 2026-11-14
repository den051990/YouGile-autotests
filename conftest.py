import time
from typing import Dict, Generator
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import Config
from pages.login_page import LoginPage


@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    options = Options()
    options.add_argument("--window-size=1920,1080")
    browser: WebDriver = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver: WebDriver) -> WebDriver:
    login_page = LoginPage(driver)
    login_page.open_login_page()
    login_page.login(Config.USER_EMAIL, Config.USER_PASSWORD)
    return driver


@pytest.fixture(scope="session")
def api_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {Config.API_TOKEN}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="function")
def created_project_id(api_headers: Dict[str, str]) -> Generator[str, None, None]:
    response = requests.post(
        f"{Config.BASE_API_URL}/projects",
        json={"title": f"API Автотест {int(time.time())}"},
        headers=api_headers
    )
    project_id: str = response.json()["id"]
    yield project_id
    requests.put(
        f"{Config.BASE_API_URL}/projects/{project_id}",
        json={"deleted": True},
        headers=api_headers
    )


@pytest.fixture(scope="function")
def temp_ui_project(api_headers: Dict[str, str]) -> Generator[str, None, None]:
    project_title: str = f"Диплом {int(time.time())}"
    project_payload = {
        "title": project_title,
        "users": {
            Config.USER_ID: "admin"
        }
    }
    proj_resp = requests.post(
        f"{Config.BASE_API_URL}/projects",
        json=project_payload,
        headers=api_headers
    )
    project_id: str = proj_resp.json()["id"]

    board_resp = requests.post(
        f"{Config.BASE_API_URL}/boards",
        json={"title": "Основная доска", "projectId": project_id},
        headers=api_headers
    )
    board_id: str = board_resp.json()["id"]

    requests.post(
        f"{Config.BASE_API_URL}/columns",
        json={"title": "Новая колонка", "boardId": board_id},
        headers=api_headers
    )

    yield project_title

    requests.put(
        f"{Config.BASE_API_URL}/projects/{project_id}",
        json={"deleted": True},
        headers=api_headers
    )

