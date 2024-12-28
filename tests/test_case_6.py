import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/"
HEADERS = {"Authorization": "Bearer b27912f4-78fd-4d15-977c-1325d4b64732"}


@pytest.fixture
def api_client():
    """
    A simple fixture to provide a session for API requests.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def test_get_users(api_client):
    """
    Test fetching the list of users.
    """
    # Define the endpoint
    endpoint = f"{BASE_URL}users/"

    # Send a GET request to the endpoint
    response = api_client.get(endpoint)

    # Print the response for debugging
    print(f"Response Code: {response.status_code}")
    print(f"Response Body: {response.text}")

    # Assert the status code is 200
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Parse the response as JSON
    users = response.json()

    # Assert the response is a list
    assert isinstance(users, list), "Expected the response to be a list of users."

    # Assert that the list is not empty
    assert len(users) > 0, "The list of users is empty."
