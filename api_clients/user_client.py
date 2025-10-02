import requests
from .get_base_url import extract_base_url

class UserClient:
    def __init__(self):
        self.base_url = extract_base_url('JSONPlaceholderAPI').strip('"').strip("'")
        self.users_endpoint = f"{self.base_url}/users"

    def get_all_users(self):
        """Sends a GET request to retrieve all users."""
        response = requests.get(self.users_endpoint)
        return response

    def get_user_by_id(self, user_id):
        """Sends a GET request to retrieve a specific user by ID."""
        url = f"{self.users_endpoint}/{user_id}"
        response = requests.get(url)
        return response

    def create_user(self, payload):
        """Sends a POST request to create a new user."""
        response = requests.post(self.users_endpoint, json=payload)
        return response