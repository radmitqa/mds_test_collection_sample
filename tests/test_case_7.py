import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/api/v1/"
HEADERS = {"Authorization": "Bearer b27912f4-78fd-4d15-977c-1325d4b64732"}


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

