import pytest
import logging
from api_clients import helpers
from api_clients.go_rest_client import APIRequestFailed

logger = logging.getLogger(__name__)
payload = helpers.load_test_data("../testdata/gorest/gorest_data.json")

@pytest.mark.api
@pytest.mark.smoke
def test_get_users(GoRest):
    """Test to retrieve a list of users from the GoRest API."""
    try:
        response = GoRest.get_users()
        response.raise_for_status()
    except APIRequestFailed as e:
        pytest.fail(f"API request failed after all retries: {e}")
    assert response.status_code == 200
    users = response.json()
    logger.info(f"Retrieved {len(users)} users.")


@pytest.mark.api
@pytest.mark.regression
def test_create_user(GoRest):
    """Test to create a new user in the GoRest API."""
    new_user_payload = payload["CREATE_USER"]
    updated_email = GoRest.create_dynamic_email(new_user_payload["email"])
    new_user_payload["email"] = updated_email
    response = GoRest.create_user(new_user_payload)
    assert response.status_code == 201
    created_user = response.json()
    logger.info(f"Created user with ID: {created_user['id']}")


@pytest.mark.api
@pytest.mark.regression  
def test_update_user(GoRest):
    """Test to update an existing user in the GoRest API."""
    
    new_user_payload = payload["CREATE_USER"]
    updated_email = GoRest.create_dynamic_email(new_user_payload["email"])
    new_user_payload["email"] = updated_email
    response = GoRest.create_user(new_user_payload)
    assert response.status_code == 201
    created_user = response.json()

    user_id = created_user["id"]
    update_payload = payload["UPDATE_USER_STATUS"]
    response = GoRest.update_user(user_id, update_payload)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["status"] == update_payload["status"]
    logger.info(f"Updated User: {updated_user}")  


@pytest.mark.api
@pytest.mark.regression
def test_delete_user(GoRest):
    """Test to delete a user from the GoRest API."""

    new_user_payload = payload["CREATE_USER"]
    updated_email = GoRest.create_dynamic_email(new_user_payload["email"])
    new_user_payload["email"] = updated_email
    response = GoRest.create_user(new_user_payload)
    assert response.status_code == 201
    created_user = response.json()

    user_id = created_user["id"]
    response = GoRest.delete_user(user_id)
    assert response.status_code == 204
    logger.info(f"Deleted user with ID: {user_id}")