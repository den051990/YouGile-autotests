import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_UI_URL: str = "https://yougile.com"
    BASE_API_URL: str = "https://yougile.com/api-v2"
    USER_EMAIL: str = os.getenv("YOUGILE_EMAIL", "")
    USER_PASSWORD: str = os.getenv("YOUGILE_PASSWORD", "")
    API_TOKEN: str = os.getenv("YOUGILE_TOKEN", "")
    USER_ID: str = os.getenv("YOUGILE_USER_ID", "")
    DEFAULT_TIMEOUT: int = 10
