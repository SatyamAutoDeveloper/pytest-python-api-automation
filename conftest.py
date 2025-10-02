import sys
import pytest
from api_clients.user_client import UserClient

sys.dont_write_bytecode = True

@pytest.fixture(scope="session")
def user_client():
    """Fixture to provide an instance of the UserClient."""
    return UserClient()