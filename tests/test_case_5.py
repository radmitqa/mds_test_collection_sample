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


def test_update_user_wishlist(api_client):
    """
    Test to update the wishlist of a user by adding a song.
    """
    # Step 1: Send GET request to /users endpoint to show the list of users
    users_response = api_client.get("users")
    assert users_response.status_code == 200, f"Expected status 200, got {users_response.status_code}"
    users_list = users_response.json()
    assert isinstance(users_list, list), "Expected a list of users"
    assert len(users_list) > 0, "Users list is empty"

    # Step 2: Pick a random user and collect their UUID
    random_user = random.choice(users_list)
    user_uuid = random_user["uuid"]

    # Step 3: Send GET request to /songs endpoint to show the list of all songs
    songs_response = api_client.get("songs")
    assert songs_response.status_code == 200, f"Expected status 200, got {songs_response.status_code}"
    songs_list = songs_response.json()
    assert isinstance(songs_list, list), "Expected a list of songs"
    assert len(songs_list) > 0, "Songs list is empty"

    # Step 4: Collect a random song and its UUID
    random_song = random.choice(songs_list)
    song_uuid = random_song["uuid"]

    # Step 5: Prepare payload with the song UUID
    payload = {"item_uuid": song_uuid}

    # Step 6: Prepare the endpoint for adding the song to the user's wishlist
    add_to_wishlist_endpoint = f"users/{user_uuid}/wishlist/add"

    # Step 7: Send POST request to the wishlist/add endpoint
    add_response = api_client.post(add_to_wishlist_endpoint, data=payload)
    assert add_response.status_code == 200, f"Expected status 200, got {add_response.status_code}"

    # Step 8: Send GET request to /users/{uuid}/wishlist endpoint
    wishlist_endpoint = f"users/{user_uuid}/wishlist"
    wishlist_response = api_client.get(wishlist_endpoint)
    assert wishlist_response.status_code == 200, f"Expected status 200, got {wishlist_response.status_code}"
    wishlist_data = wishlist_response.json()

    # Step 9: Assert that the song UUID is successfully added to the wishlist
    assert isinstance(wishlist_data, list), "Expected a list of wishlist items"
    added_song = next((item for item in wishlist_data if item["uuid"] == song_uuid), None)
    assert added_song, f"Song with UUID {song_uuid} was not added to the wishlist"
