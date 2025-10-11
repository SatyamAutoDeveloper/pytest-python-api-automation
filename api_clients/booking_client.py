import base64
import requests
from .get_base_url import extract_base_url

"""credentials = f"{USERNAME}:{PASSWORD}"
credentials_bytes = credentials.encode("utf-8")
encoded_bytes = base64.b64encode(credentials_bytes)
encoded_credentials = encoded_bytes.decode("utf-8")
auth_header_value = f"Basic {encoded_credentials}"""


class BearerToken:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={self.token}",
        }

    def refresh_token(self, new_token):
        self.token = new_token

    def get_token(self):
        return self.token


class BookingClient:
    def __init__(self):
        self.base_url = extract_base_url("BOOKINGAPI").strip('"').strip("'")
        self.booking_endpoint = f"{self.base_url}/booking"

    def get_all_bookings(self):
        """Sends a GET request to retrieve all bookings."""
        response = requests.get(self.booking_endpoint)
        return response

    def get_booking_by_id(self, booking_id):
        """Sends a GET request to retrieve a specific booking by ID."""
        url = f"{self.booking_endpoint}/{booking_id}"
        response = requests.get(url)
        return response

    def create_booking(self, payload):
        """Sends a POST request to create a new booking."""
        response = requests.post(self.booking_endpoint, json=payload)
        return response

    def update_booking(self, booking_id, payload, token):
        """Sends a PUT request to update an existing booking."""
        url = f"{self.booking_endpoint}/{booking_id}"
        headers = BearerToken(token).get_headers()
        response = requests.put(url, json=payload, headers=headers)
        return response

    def delete_booking(self, booking_id, token):
        """Sends a DELETE request to remove a booking."""
        url = f"{self.booking_endpoint}/{booking_id}"
        headers = BearerToken(token).get_headers()
        response = requests.delete(url, headers=headers)
        return response

    def partial_update_booking(self, booking_id, payload, token):
        """Sends a PATCH request to partially update an existing booking."""
        url = f"{self.booking_endpoint}/{booking_id}"
        headers = BearerToken(token).get_headers()
        response = requests.patch(url, json=payload, headers=headers)
        return response

    def authenticate(self, username, password):
        """Sends a POST request to authenticate and retrieve a token."""
        auth_endpoint = f"{self.base_url}/auth"
        payload = {"username": username, "password": password}
        response = requests.post(auth_endpoint, json=payload)
        return response

    def get_booking_ids_by_firstname(self, firstname):
        """Sends a GET request to retrieve booking IDs filtered by first name."""
        url = f"{self.booking_endpoint}?firstname={firstname}"
        response = requests.get(url)
        return response

    def get_booking_ids_by_checkin(self, checkin):
        """Sends a GET request to retrieve booking IDs filtered by check-in date."""
        url = f"{self.booking_endpoint}?checkin={checkin}"
        response = requests.get(url)
        return response

    def get_booking_api_health(self):
        """Sends a GET request to check the health of the booking service."""
        health_endpoint = f"{self.base_url}/ping"
        response = requests.get(health_endpoint)
        return response
