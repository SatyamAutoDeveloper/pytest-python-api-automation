import pytest
import logging
from api_clients import helpers

logger = logging.getLogger(__name__)
payload = helpers.load_test_data("../testdata/petstore/petstore_data.json")

@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.parametrize("status", payload['FIND_PETS_BY_STATUS']["status"])
def test_get_pets_by_status(pet_store_client, status):
    """Test to get pets by status."""
    response = pet_store_client.get_pets_by_status(status)
    assert response.status_code == 200
    pets = response.json()
    assert isinstance(pets, list)
    for pet in pets:
        assert pet['status'] == status
    logger.info("test_get_pets_by_status passed.")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.dependency()
def test_create_pet(pet_store_client):
    """Test to create a new pet."""
    new_pet = payload['CREATE_PET']
    response = pet_store_client.create_pet(new_pet)
    assert response.status_code == 200
    created_pet = response.json()
    assert created_pet['name'] == new_pet['name']
    assert created_pet['status'] == new_pet['status']
    logger.info("test_create_pet passed.")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_create_pet"])
def test_upload_pet_image(pet_store_client):
    """Test to upload an image for a specific pet."""
    pet_id = payload['ADD_PET_IMAGE']['petId']
    image_path = payload['ADD_PET_IMAGE']['file']
    response = pet_store_client.upload_pet_image(pet_id, image_path)
    assert response.status_code == 200
    upload_response = response.json()
    assert 'message' in upload_response
    logger.info("test_upload_pet_image passed.")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_create_pet"])
def test_update_pet(pet_store_client):
    """Test to update an existing pet."""
    updated_pet = payload['UPDATE_PET']
    response = pet_store_client.update_pet(updated_pet)
    assert response.status_code == 200
    pet = response.json()
    assert pet['name'] == updated_pet['name']
    assert pet['status'] == updated_pet['status']
    logger.info("test_update_pet passed.")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_create_pet"])
def test_get_pet_by_id(pet_store_client):
    """Test to get a specific pet by ID."""
    pet_id = payload['GET_PET_BY_ID']['petId']
    response = pet_store_client.get_pet_by_id(pet_id)
    assert response.status_code == 200
    pet = response.json()
    assert pet['id'] == pet_id
    logger.info("test_get_pet_by_id passed.")


@pytest.mark.api
@pytest.mark.regression
def test_inventory_store(pet_store_client):
    """Test to get pet inventory by status."""
    response = pet_store_client.get_pet_inventory_by_status()
    assert response.status_code == 200
    inventory = response.json()
    assert isinstance(inventory, dict)
    logger.info("test_inventory_by_status passed.")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_create_pet"])
def test_order_new_pet(pet_store_client):
    """Test to place a new pet order."""
    new_order = payload['ORDER_PET']
    response = pet_store_client.create_order(new_order)
    assert response.status_code == 200
    order = response.json()
    assert order['petId'] == new_order['petId']
    assert order['quantity'] == new_order['quantity']
    logger.info("test_place_order passed.")



@pytest.mark.api
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_order_new_pet"])
def test_get_order_by_id(pet_store_client):
    """Test to get a specific order by ID."""
    order_id = payload['GET_ORDER_BY_ID']['orderId']
    response = pet_store_client.get_order_by_id(order_id)
    assert response.status_code == 200
    order = response.json()
    assert order['id'] == order_id
    logger.info("test_get_order_by_id passed.")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_order_new_pet"])
def test_delete_order(pet_store_client):
    """Test to delete a specific order by ID."""
    order_id = payload['DELETE_ORDER']['orderId']
    response = pet_store_client.delete_order(order_id)
    assert response.status_code == 200
    delete_response = response.json()
    assert delete_response['message'] == str(order_id)
    logger.info("test_delete_order passed.")


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.dependency(depends=["test_create_pet"])
def test_delete_pet(pet_store_client):
    """Test to delete a specific pet by ID."""
    pet_id = payload['DELETE_PET']['petId']
    response = pet_store_client.delete_pet(pet_id)
    assert response.status_code == 200
    delete_response = response.json()
    assert delete_response['message'] == str(pet_id)
    logger.info("test_delete_pet passed.")