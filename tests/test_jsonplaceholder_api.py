import pytest
import logging
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
    assert "username" in user, "Expected user object to contain 'username' field"