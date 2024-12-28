import pytest
import requests

# Base configuration for API
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


def test_get_users(api_client):
    """
    Test fetching the list of users from the API.
    """
    endpoint = f"{BASE_URL}users/"  # Define the users endpoint
    response = api_client.get(endpoint)  # Send the GET request

    # Logging response details for debugging
    print("Response Details:")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    # Assertions to validate the response
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

    # Parse the response JSON
    try:
        users = response.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON")

    # Validate the structure and content of the response
    assert isinstance(users, list), "Expected the response to be a list of users."
    assert len(users) > 0, "The list of users should not be empty."

    # Optional: Log user details
    print("User List:")
    for user in users:
        print(user)
