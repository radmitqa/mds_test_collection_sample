import pytest
from api_client import APIClient

BASE_URL = "http://127.0.0.1:8000/api/v1/"
BEARER_TOKEN = "b27912f4-78fd-4d15-977c-1325d4b64732"


@pytest.fixture
def api_client():
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    return APIClient(BASE_URL, headers=headers)
