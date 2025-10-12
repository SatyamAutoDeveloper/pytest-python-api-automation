import base64
import requests
from .get_base_url import extract_base_url

class BasicAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_headers(self):
        credentials = f"{self.username}:{self.password}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
        }
    
    

class PetStoreClient:
    def __init__(self):
        self.base_url = extract_base_url("PETSTOREAPI").strip('"').strip("'")
        self.pet_endpoint = f"{self.base_url}/pet"
        self.store_endpoint = f"{self.base_url}/store"

    def get_pets_by_status(self, status):
        """Sends a GET request to retrieve pets by status."""
        url = f"{self.pet_endpoint}/findByStatus?status={status}"
        response = requests.get(url)
        return response

    def get_pet_by_id(self, pet_id):
        """Sends a GET request to retrieve a specific pet by ID."""
        url = f"{self.pet_endpoint}/{pet_id}"
        response = requests.get(url)
        return response

    def create_pet(self, payload):
        """Sends a POST request to create a new pet."""
        response = requests.post(self.pet_endpoint, json=payload)
        return response

    def update_pet(self, payload):
        """Sends a PUT request to update an existing pet."""
        response = requests.put(self.pet_endpoint, json=payload)
        return response

    def delete_pet(self, pet_id):
        """Sends a DELETE request to remove a pet."""
        url = f"{self.pet_endpoint}/{pet_id}"
        response = requests.delete(url)
        return response
    
    def upload_pet_image(self, pet_id, image_path):
        """Sends a POST request to upload an image for a specific pet."""
        url = f"{self.pet_endpoint}/{pet_id}/uploadImage"
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            response = requests.post(url, files=files)
        return response
    
    def get_pet_inventory_by_status(self):
        """Sends a GET request to retrieve pet inventory by status."""
        url = f"{self.store_endpoint}/inventory"
        response = requests.get(url)
        return response
    
    def create_order(self, payload):
        """Sends a POST request to create a new order."""
        url = f"{self.store_endpoint}/order"
        response = requests.post(url, json=payload)
        return response
    
    def get_order_by_id(self, order_id):
        """Sends a GET request to retrieve a specific order by ID."""
        url = f"{self.store_endpoint}/order/{order_id}"
        response = requests.get(url)
        return response
    
    def delete_order(self, order_id):
        """Sends a DELETE request to remove an order."""
        url = f"{self.store_endpoint}/order/{order_id}"
        response = requests.delete(url)
        return response
    
