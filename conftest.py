import os
import sys
import pytest
from api_clients.user_client import UserClient
from api_clients.booking_client import BookingClient
from api_clients.go_rest_client import GoRestClient

# Prevent pytest from generating .pyc files
sys.dont_write_bytecode = True

@pytest.fixture(scope="session")
def user_client():
    """Fixture to provide an instance of the UserClient."""
    return UserClient()

@pytest.fixture(scope="session")
def booking_client():
    """Fixture to provide an instance of the BookingClient."""
    return BookingClient()


@pytest.fixture(scope="session")
def booking_api_credentials():
    """
    Fixture to securely read API username and password from environment 
    variables (like those injected by GitHub Actions).
    """
    # 1. Read environment variables from the OS environment
    username = os.environ.get("API_USERNAME") 
    password = os.environ.get("API_PASSWORD")
    
    # 2. Add a safeguard: If variables are missing, skip the tests gracefully.
    if not username or not password:
        pytest.skip(
            "Skipping tests requiring authentication. "
            "API_USERNAME and API_PASSWORD must be set in the environment (e.g., via GitHub Secrets)."
        )
    
    # 3. Return a properly structured dictionary
    return {
        "username": username,
        "password": password
    }


@pytest.fixture(scope="session")
def gorest_token():
    """Reads GoRest PAT from environment variable."""
    token = os.environ.get("GOREST_TOKEN") 
    if not token:
        pytest.skip('GOREST_TOKEN must be set for GoRest API tests.')
    return token


@pytest.fixture(scope="session")
def GoRest(gorest_token):
    """Fixture to provide an instance of the GoRestClient."""
    return GoRestClient(gorest_token)