import pytest
import requests
import random

BASE_URL = "http://127.0.0.1:8000/api/v1/"
HEADERS = {"Authorization": "Bearer b27912f4-78fd-4d15-977c-1325d4b64732"}


@pytest.fixture(scope="module")
def api_client():
    """
    Provides a session object configured with default headers for API requests.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def test_delete_random_user(api_client):
    """
    Test deleting a random user and validating the deletion.
    """
    # Step 1: Send GET request to fetch the list of users
    users_endpoint = f"{BASE_URL}users/"
    response = api_client.get(users_endpoint)
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    users = response.json()
    assert isinstance(users, list), "Expected a list of users."
    assert len(users) > 0, "The users list should not be empty."

    # Step 2: Pick a random user and save their UUID
    random_user = random.choice(users)
    var_1 = random_user["uuid"]
    print(f"Selected user UUID for deletion: {var_1}")

    # Step 3: Send DELETE request to /users/{var_1} endpoint
    delete_endpoint = f"{BASE_URL}users/{var_1}/"
    delete_response = api_client.delete(delete_endpoint)
    assert delete_response.status_code == 204, f"Expected 204, but got {delete_response.status_code}"
    print(f"User with UUID {var_1} deleted successfully.")

    # Step 4: Validate the user is deleted by fetching the list of users
    response_after_deletion = api_client.get(users_endpoint)
    assert response_after_deletion.status_code == 200, f"Expected 200, but got {response_after_deletion.status_code}"
    updated_users = response_after_deletion.json()
    user_ids_after_deletion = [user["uuid"] for user in updated_users]
    assert var_1 not in user_ids_after_deletion, f"User with UUID {var_1} should not be in the updated users list."

    # Step 5: Verify user is not returned by sending GET request to /users/{var_1} endpoint
    user_detail_endpoint = f"{BASE_URL}users/{var_1}/"
    user_detail_response = api_client.get(user_detail_endpoint)
    assert user_detail_response.status_code == 404, f"Expected 404, but got {user_detail_response.status_code}"
    print(f"User with UUID {var_1} is confirmed as deleted.")
