import pytest
from api_client import APIClient

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


def test_create_new_user(api_client):
    """
    Test to create a new user and validate all related operations.
    """
    # Step 1: Prepare payload with valid data
    payload = {
        "email": "joe@mmail.com",
        "password": "securepassword123",
        "name": "Joe Doe",
        "nickname": "joedoe"
    }

    # Step 2: Send POST request to /users endpoint
    create_response = api_client.post("users", data=payload)
    assert create_response.status_code == 200, f"Expected status 200, got {create_response.status_code}"
    user_data = create_response.json()

    # Step 3: Assert that the response is in the correct format
    expected_keys = {"email", "name", "nick", "avatar_url", "uuid"}
    assert set(user_data.keys()) == expected_keys, f"Response keys do not match: {user_data.keys()}"

    assert user_data["email"] == payload["email"]
    assert user_data["name"] == payload["name"]
    assert user_data["nick"] == payload["nickname"]
    assert user_data["avatar_url"] == "", "Avatar URL should be empty by default"
    assert "uuid" in user_data and len(user_data["uuid"]) > 0, "UUID is missing or invalid"

    # Save the UUID for later verification
    user_uuid = user_data["uuid"]

    # Step 4: Verify the new user exists in the list of users
    users_response = api_client.get("users")
    assert users_response.status_code == 200, f"Expected status 200, got {users_response.status_code}"
    users_list = users_response.json()
    assert isinstance(users_list, list), "Expected a list of users"

    # Validate the new user is in the list
    new_user_in_list = next((user for user in users_list if user["uuid"] == user_uuid), None)
    assert new_user_in_list, f"Newly created user with UUID {user_uuid} is not in the users list"
    assert new_user_in_list["email"] == payload["email"]
    assert new_user_in_list["name"] == payload["name"]
    assert new_user_in_list["nick"] == payload["nickname"]

    # Step 5: Validate that we can search for the new user by UUID
    user_by_uuid_response = api_client.get(f"users/{user_uuid}")
    assert user_by_uuid_response.status_code == 200, f"Expected status 200, got {user_by_uuid_response.status_code}"
    user_by_uuid_data = user_by_uuid_response.json()

    # Validate that the data matches and is in the correct order
    assert user_by_uuid_data == user_data, "Data retrieved by UUID does not match the original data"
