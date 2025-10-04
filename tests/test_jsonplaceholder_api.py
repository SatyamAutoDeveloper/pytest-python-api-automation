import pytest
import logging
from api_clients import helpers
from jsonschema import validate

# Remove direct import of user_client fixture

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.smoke
def test_get_users(user_client):
    """
    Test case for retrieving users from the JSONPlaceholder API.

    This test verifies that a GET request to the users endpoint returns a successful response
    and that the response contains the expected user data.
    """
    response = user_client.get_all_users()

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    users = response.json()
    logger.info(f"Retrieved {len(users)} users")
    assert len(users) > 0, "Expected at least one user in the response"
    assert "username" in users[0], "Expected user object to contain 'username' field"

@pytest.mark.api
@pytest.mark.regression
def test_get_specific_user(user_client):
    """
    Test retrieving a specific user from the JSONPlaceholder API.

    This test verifies that the API returns the correct user data when queried
    for a specific user ID. It checks the response status code and validates
    the structure and content of the returned user information.
    """
    user_id = 1
    response = user_client.get_user_by_id(user_id)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    user = response.json()
    logger.info(f"Retrieved user data: {user}")
    assert user["id"] == user_id, f"Expected user ID {user_id}, but got {user['id']}"
    assert user["name"] == "Leanne Graham", f"Expected name 'Leanne Graham', but got {user['name']}"
    assert user["username"] == "Bret", f"Expected username 'Bret', but got {user['username']}"
    assert user["email"] == "Sincere@april.biz", f"Expected email 'Sincere@april.biz', but got {user['email']}"


@pytest.mark.api
@pytest.mark.regression
def test_create_user(user_client):
    """
    Test creating a new user in the JSONPlaceholder API.

    This test verifies that a POST request to create a new user returns a successful response
    and that the response contains the expected user data, including an assigned ID.
    """
    payload = helpers.load_test_data("../testdata/jsonplaceholder/user_data.json")
    response = user_client.create_user(payload)

    assert response.status_code == 201 or response.status_code == 200, f"Expected status code 201 or 200, but got {response.status_code}"
    created_user = response.json()
    logger.info(f"Created user data: {created_user}")
    assert "id" in created_user, "Expected created user to have an 'id' field"
    assert created_user["name"] == payload["name"], f"Expected name '{payload['name']}', but got {created_user['name']}"
    assert created_user["username"] == payload["username"], f"Expected username '{payload['username']}', but got {created_user['username']}"
    assert created_user["email"] == payload["email"], f"Expected email '{payload['email']}', but got {created_user['email']}"


@pytest.mark.api
@pytest.mark.smoke
def test_get_user_schema_is_valid(user_client):
    """Test to validate the response schema for a single user."""
    user_id = 1
    response = user_client.get_user_by_id(user_id)
    response_data = response.json()
    
    user_schema = helpers.load_test_data("../testdata/jsonplaceholder/user_schema.json")
    
    assert response.status_code == 200
    validate(instance=response_data, schema=user_schema)


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize("user_id, expected_name", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
    (3, "Clementine Bauch")
])
def test_get_multiple_users_by_id(user_client, user_id, expected_name):
    """Data-driven test to get multiple users and verify their names."""
    response = user_client.get_user_by_id(user_id)
    
    assert response.status_code == 200
    assert response.json()["name"] == expected_name
    logger.info(f"User ID {user_id} has the expected name '{expected_name}'") 


@pytest.mark.api
@pytest.mark.regression
def test_update_user(user_client):
    """Test to update an existing user's information."""
    user_id = 1
    response = user_client.get_user_by_id(user_id)
    updated_payload = response.json()
    updated_payload["name"] = "Savi IPS"
    update_response = user_client.update_user(user_id, updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Savi IPS"
    logger.info(f"User ID {user_id} name updated to 'Savi IPS'")
    # Note: JSONPlaceholder does not persist updates, so skip verification step.


@pytest.mark.api
@pytest.mark.regression
def test_delete_user(user_client):
    """Test to delete a user."""
    user_id = 1
    delete_response = user_client.delete_user(user_id)
    assert delete_response.status_code == 200 or delete_response.status_code == 204
    logger.info(f"User ID {user_id} deleted successfully")
    # Note: JSONPlaceholder does not actually delete users, so skip verification step.

