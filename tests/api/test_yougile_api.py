from typing import Any, Dict
import allure
import requests
from config.config import Config


@allure.epic("YouGile API")
@allure.feature("Тестирование API по кейсам из Test IT")
class TestYouGileAPI:

    @allure.title("API-1: Создание проекта с валидным названием")
    def test_create_project_positive(self, api_headers: Dict[str, str]) -> None:
        payload: Dict[str, str] = {"title": "Диплом"}
        with allure.step("Отправить POST-запрос на /api-v2/projects"):
            response = requests.post(
                f"{Config.BASE_API_URL}/projects",
                json=payload,
                headers=api_headers
            )
        assert response.status_code == 201
        data: Dict[str, Any] = response.json()
        assert "id" in data and len(data["id"]) > 0

        requests.put(
            f"{Config.BASE_API_URL}/projects/{data['id']}",
            json={"deleted": True},
            headers=api_headers
        )


    @allure.title("API-2: Создание доски в проекте")
    def test_create_board_positive(self, api_headers: Dict[str, str], created_project_id: str) -> None:
        payload: Dict[str, Any] = {
            "title": "YouGile",
            "projectId": created_project_id,
            "stickers": {
                "timer": False,
                "deadline": True,
                "stopwatch": True,
                "timeTracking": True,
                "assignee": True,
                "repeat": True
            }
        }
        with allure.step("Отправить POST-запрос на /api-v2/boards"):
            response = requests.post(
                f"{Config.BASE_API_URL}/boards",
                json=payload,
                headers=api_headers
            )
        assert response.status_code == 201
        assert "id" in response.json()

    @allure.title("API-3: Негативный тест — создание проекта с пустым title")
    def test_create_project_empty_title(self, api_headers: Dict[str, str]) -> None:
        with allure.step("Отправить POST-запрос с пустым полем title"):
            response = requests.post(
                f"{Config.BASE_API_URL}/projects",
                json={"title": ""},
                headers=api_headers
            )
        assert response.status_code == 400
        body: Dict[str, Any] = response.json()
        assert "title should not be empty" in body.get("message", [])

    @allure.title("API-4: Негативный тест — запрос с невалидным токеном авторизации")
    def test_create_project_invalid_token(self) -> None:
        bad_headers: Dict[str, str] = {
            "Authorization": "Bearer invalid_token_12345",
            "Content-Type": "application/json"
        }
        with allure.step("Отправить POST-запрос с некорректным токеном"):
            response = requests.post(
                f"{Config.BASE_API_URL}/projects",
                json={"title": "Диплом"},
                headers=bad_headers
            )
        assert response.status_code == 401
        assert response.json().get("error") == "Unauthorized"

    @allure.title("API-5: Негативный тест — создание задачи с несуществующим columnId")
    def test_create_task_nonexistent_column(self, api_headers: Dict[str, str]) -> None:
        payload: Dict[str, Any] = {
            "title": "test task",
            "columnId": "8a28ee0d-843c-407b-9de3-3f25f6ef8585",
            "description": "string",
            "archived": False,
            "completed": False
        }
        with allure.step("Отправить POST-запрос на /api-v2/tasks с несуществующим UUID колонки"):
            response = requests.post(
                f"{Config.BASE_API_URL}/tasks",
                json=payload,
                headers=api_headers
            )
        assert response.status_code == 404
        assert response.json().get("message") == "Колонка не найдена"
