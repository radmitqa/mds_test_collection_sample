import requests


class APIClient:
    """
    A simple API client for making HTTP requests.
    """
    def __init__(self, base_url, headers=None):
        """
        Initialize the API client.
        :param base_url: Base URL of the API
        :param headers: Default headers for all requests
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}

    def _handle_response(self, response):
        """
        Handle the HTTP response.
        :param response: Response object from the requests library
        :return: Parsed JSON response or raw response if JSON fails
        """
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e.response.status_code} - {e.response.text}")
            raise
        except ValueError:
            # Return raw text if JSON decoding fails
            return response.text

    def get(self, endpoint, params=None):
        """
        Send a GET request to the specified endpoint.
        :param endpoint: API endpoint (relative to base URL)
        :param params: Query parameters
        :return: Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json_data=True):
        """
        Send a POST request to the specified endpoint.
        :param endpoint: API endpoint (relative to base URL)
        :param data: Request payload (JSON by default)
        :param json_data: Whether the payload is in JSON format
        :return: Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if json_data:
            response = requests.post(url, headers=self.headers, json=data)
        else:
            response = requests.post(url, headers=self.headers, data=data)
        return self._handle_response(response)

    def patch(self, endpoint, data=None, json_data=True):
        """
        Send a PATCH request to the specified endpoint.
        :param endpoint: API endpoint (relative to base URL)
        :param data: Request payload (JSON by default)
        :param json_data: Whether the payload is in JSON format
        :return: Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        if json_data:
            response = requests.patch(url, headers=self.headers, json=data)
        else:
            response = requests.patch(url, headers=self.headers, data=data)
        return self._handle_response(response)

    def delete(self, endpoint):
        """
        Send a DELETE request to the specified endpoint.
        :param endpoint: API endpoint (relative to base URL)
        :return: Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)




# import requests
#
#
# class APIClient:
#     def __init__(self, base_url, headers=None):
#         self.base_url = base_url
#         self.headers = headers or {}
#
#     def get(self, endpoint, params=None, expect_status=True):
#         response = requests.get(f"{self.base_url}/{endpoint}", params=params, headers=self.headers)
#         if expect_status:
#             response.raise_for_status()
#         return response
#
#     def delete(self, endpoint):
#         response = requests.delete(f"{self.base_url}/{endpoint}", headers=self.headers)
#         return response
#
#     def post(self, endpoint, data=None):
#         response = requests.post(f"{self.base_url}/{endpoint}", json=data, headers=self.headers)
#         response.raise_for_status()
#         return response
#
#     def patch(self, endpoint, data=None):
#         response = requests.patch(f"{self.base_url}/{endpoint}", json=data, headers=self.headers)
#         response.raise_for_status()
#         return response
