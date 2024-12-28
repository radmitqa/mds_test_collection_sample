import pytest
from api_client import APIClient
import random

BASE_URL = "http://127.0.0.1:8000/api/v1/"
BEARER_TOKEN = "b27912f4-78fd-4d15-977c-1325d4b64732"


@pytest.fixture
def api_client():
    ## initialize APIClient with Authorization header
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    return APIClient(BASE_URL, headers=headers)


def test_delete_user(api_client):
    """
    Test to delete a random user and validate the deletion process.
    """
    # Step 1: Send GET request to /users endpoint to get the list of users
    users = api_client.get("users")
    assert isinstance(users, list), "Expected a list of users"
    assert len(users) > 0, "User list is empty"

    # Step 2: Pick a random user and save their UUID to var_1
    random_user = random.choice(users)
    var_1 = random_user["uuid"]  # Adjust the key if UUID is under a different field

    # Step 3: Send DELETE request to /users/{var_1} endpoint
    delete_response = api_client.delete(f"users/{var_1}")
    assert delete_response.status_code == 204, f"Expected status 204, got {delete_response.status_code}"

    # Step 4: Validate that the user with UUID var_1 is deleted by sending GET to /users
    updated_users = api_client.get("users")
    user_ids = [user["uuid"] for user in updated_users]
    assert var_1 not in user_ids, f"User with UUID {var_1} was not deleted from the list"

    # Step 5: Verify that a GET request to /users/{var_1} returns 404
    get_deleted_user_response = api_client.get(f"users/{var_1}", expect_status=False)
    assert get_deleted_user_response.status_code == 404, f"Expected status 404, got {get_deleted_user_response.status_code}"


# def test_get_users(api_client):
#     response = api_client.get("users")
#     assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
#     users = response.json()
#     assert isinstance(users, list), "Expected a list of users"
#     assert len(users) > 0, "No users found"
