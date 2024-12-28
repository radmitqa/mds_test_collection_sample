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


def test_search_song(api_client):
    """
    Test to search for a song using the first three letters of a random song name.
    """
    # Step 1: Send GET request to /songs endpoint to get the list of all songs
    songs_response = api_client.get("songs")
    assert songs_response.status_code == 200, f"Expected status 200, got {songs_response.status_code}"
    songs = songs_response.json()
    assert isinstance(songs, list), "Expected a list of songs"
    assert len(songs) > 0, "Songs list is empty"

    # Step 2: Pick a random song and copy the first 3 letters of its name to var_1
    random_song = random.choice(songs)
    song_name = random_song["name"]  # Adjust the key if the song name is under a different field
    var_1 = song_name[:3]  # First three letters of the song name

    # Step 3: Prepare query parameter for searching the song
    query_params = {"search": var_1}

    # Step 4: Send GET request to /songs endpoint with the prepared query parameter
    search_response = api_client.get("songs", params=query_params)
    assert search_response.status_code == 200, f"Expected status 200, got {search_response.status_code}"
    search_results = search_response.json()
    assert isinstance(search_results, list), "Expected a list of search results"

    # Step 5: Assert that the response data matches songs from the original list containing var_1
    matching_songs = [song for song in songs if var_1.lower() in song["name"].lower()]
    assert len(search_results) == len(matching_songs), "Search results do not match the expected songs"
    assert all(song in matching_songs for song in search_results), "Search results contain unexpected songs"

    # Step 6: Test behavior when search query is empty
    empty_query_response = api_client.get("songs", params={"search": ""})
    assert empty_query_response.status_code == 200, f"Expected status 200, got {empty_query_response.status_code}"
    empty_query_results = empty_query_response.json()
    assert isinstance(empty_query_results, list), "Expected a list of songs for empty search query"

    # Assert that songs are displayed alphabetically for empty search query
    sorted_songs = sorted(songs, key=lambda x: x["name"].lower())
    assert empty_query_results == sorted_songs, "Songs are not displayed alphabetically for empty search query"

    # Step 7: Test behavior when search query contains invalid characters
    invalid_query_response = api_client.get("songs", params={"search": "###"})
    assert invalid_query_response.status_code == 200, f"Expected status 200, got {invalid_query_response.status_code}"
    invalid_query_results = invalid_query_response.json()
    assert isinstance(invalid_query_results, list), "Expected a list of songs for invalid search query"

    # Assert that songs are displayed alphabetically for invalid search query
    assert invalid_query_results == sorted_songs, "Songs are not displayed alphabetically for invalid search query"
