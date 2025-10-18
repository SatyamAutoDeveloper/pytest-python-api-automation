import base64
import requests
from .get_base_url import extract_base_url
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

class APIRequestFailed(Exception):
    """Custom exception for retry purposes."""
    pass

class BearerToken:
    def __init__(self, token):
        self.token = token

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self.token}"}
    
    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
    
    def refresh_token(self, new_token):
        self.token = new_token

    def get_token(self):
        return self.token
    
class GoRestClient:
    def __init__(self, token):
        self.base_url = extract_base_url("GORESTAPI").strip('"').strip("'")
        self.users_endpoint = f"{self.base_url}/users"
        self.token_manager = BearerToken(token)

    @retry(
    # Stop after 5 attempts
    stop=stop_after_attempt(2),
    # Wait 2^x * 1 second between retries, up to 10 seconds max
    wait=wait_exponential(multiplier=1, min=2, max=10),
    # Only retry if an APIRequestFailed exception is raised
    retry=retry_if_exception_type(APIRequestFailed),
    # reraise the last exception if all retries fail
    reraise=True,
    )
    def get_users(self):
        """Sends a GET request to retrieve all users."""
        try:
            headers = self.token_manager.get_headers()
            response = requests.get(self.users_endpoint, headers=headers)
            if response.status_code >= 500:
                raise APIRequestFailed(f"Server error: {response.status_code}")
            return response
        except requests.RequestException as e:
            raise APIRequestFailed(f"Request failed: {e}")
        except requests.Timeout as e:
            raise APIRequestFailed(f"Request timed out: {e}")
        except requests.ConnectionError as e:
            raise APIRequestFailed(f"Connection error: {e}")
    
    def get_user_by_id(self, user_id):
        """Sends a GET request to retrieve a specific user by ID."""
        url = f"{self.users_endpoint}/{user_id}"
        headers = self.token_manager.get_headers()
        response = requests.get(url, headers=headers)
        return response
    
    def create_user(self, payload):
        """Sends a POST request to create a new user."""
        headers = self.token_manager.get_headers()
        response = requests.post(self.users_endpoint, json=payload, headers=headers)
        return response
    
    def update_user(self, user_id, payload):
        """Sends a PUT request to update an existing user."""
        url = f"{self.users_endpoint}/{user_id}"
        headers = self.token_manager.get_headers()
        response = requests.put(url, json=payload, headers=headers)
        return response
    
    def delete_user(self, user_id):
        """Sends a DELETE request to remove a user."""
        url = f"{self.users_endpoint}/{user_id}"
        headers = self.token_manager.get_headers()
        response = requests.delete(url, headers=headers)
        return response
    
    def create_dynamic_email(self, base_email):
        """Generates a unique email address by appending a timestamp."""
        import time
        timestamp = int(time.time())
        local_part, domain = base_email.split("@")
        dynamic_email = f"{local_part}+{timestamp}@{domain}"
        return dynamic_email