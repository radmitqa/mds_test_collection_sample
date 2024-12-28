import pytest
from api_client import APIClient
import random

BASE_URL = "http://127.0.0.1:8000/api/v1/"
BEARER_TOKEN = "b27912f4-78fd-4d15-977c-1325d4b64732"


@pytest.fixture
def api_client():
    """
    Fixture to initialize APIClient with Authorization header.
    """
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    return APIClient(BASE_URL, headers=headers)


def test_prevent_editing_with_taken_data(api_client):
    """
    Test to ensure editing user data fails if the email or nickname is already taken.
    """
    # Step 1: Send GET request to /users endpoint to show list of users
    users_response = api_client.get("users")
    assert users_response.status_code == 200, f"Expected status 200, got {users_response.status_code}"
    users_list = users_response.json()
    assert isinstance(users_list, list), "Expected a list of users"
    assert len(users_list) > 1, "At least two users are required to test this scenario"

    # Step 2: Pick user for data editing
    target_user = random.choice(users_list)
    conflicting_user = random.choice([user for user in users_list if user != target_user])

    # Save email and nickname for conflicting data
    conflicting_email = conflicting_user["email"]
    conflicting_nick = conflicting_user["nick"]

    # Step 3: Fill in payload with conflicting email or nickname
    payload_email = {"email": conflicting_email}
    payload_nick = {"nickname": conflicting_nick}

    # Step 4: Pick random UUID as parameter for the target user
    target_uuid = target_user["uuid"]

    # Step 5: Send PATCH request with prepared payload (email)
    email_patch_response = api_client.patch(f"users/{target_uuid}", data=payload_email)
    assert email_patch_response.status_code == 409, f"Expected status 409, got {email_patch_response.status_code}"
    email_response_data = email_patch_response.json()

    # Step 6: Assert response contains the expected error message
    assert email_response_data["code"] == 409, "Expected response code 409"
    assert "already taken" in email_response_data["message"].lower(), "Error message does not mention 'already taken'"
    assert conflicting_email in email_response_data["message"], "Error message does not include conflicting email"

    # Step 7: Send PATCH request with prepared payload (nickname)
    nick_patch_response = api_client.patch(f"users/{target_uuid}", data=payload_nick)
    assert nick_patch_response.status_code == 409, f"Expected status 409, got {nick_patch_response.status_code}"
    nick_response_data = nick_patch_response.json()

    # Assert response contains the expected error message
    assert nick_response_data["code"] == 409, "Expected response code 409"
    assert "already taken" in nick_response_data["message"].lower(), "Error message does not mention 'already taken'"
    assert conflicting_nick in nick_response_data["message"], "Error message does not include conflicting nickname"
