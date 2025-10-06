import pytest
import logging
from api_clients import helpers

logger = logging.getLogger(__name__)


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.dependency()
def test_get_booking_api_health(booking_client):
    """
    Test case for checking the health of the Booking API.
    This test verifies that a GET request to the Booking API health endpoint returns a successful response
    """
    response = booking_client.get_booking_api_health()
    assert response.status_code == 201, f"Expected status code 200, but got {response.status_code}"


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.dependency(on=['test_get_booking_api_health'])
def test_get_all_bookings(booking_client):
    """
    Test case for retrieving all bookings from the Booking API.
    This test verifies that a GET request to the Booking API returns a successful response and a list of bookings.
    """
    response = booking_client.get_all_bookings()
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    bookings = response.json()
    assert isinstance(bookings, list), "Expected response to be a list of bookings"
    logger.info(f"Retrieved {len(bookings)} bookings")


@pytest.mark.api
@pytest.mark.regression
def test_create_booking(booking_client):
    """
    Test case for creating a new booking in the Booking API.
    This test verifies that a POST request to the Booking API with valid booking data returns a successful response
    and the created booking details.
    """
    booking_payload = helpers.load_test_data("../testdata/booking/booking_data.json")
    response = booking_client.create_booking(booking_payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    created_booking = response.json()
    logger.info(f"Created booking data: {created_booking}") 
    assert 'bookingid' in created_booking, "Response does not contain 'bookingid'"
    logger.info(f"Created booking with ID: {created_booking['bookingid']}")


@pytest.mark.api
@pytest.mark.regression
def test_get_booking_by_id(booking_client):
    """
    Test case for retrieving a specific booking by ID from the Booking API.
    This test verifies that a GET request to the Booking API with a valid booking ID returns a successful response
    and the correct booking details.
    """
    # First, create a booking to ensure there is a booking to retrieve
    booking_payload = helpers.load_test_data("../testdata/booking/booking_data.json")
    response = booking_client.create_booking(booking_payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    created_booking = response.json()
    
    # Now, retrieve the booking by ID
    response = booking_client.get_booking_by_id(created_booking["bookingid"])
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    booking = response.json()
    logger.info(f"Retrieved booking data: {booking}")
    assert booking["firstname"] == "Savi", f"Expected firstname '{"Savi"}', but got {booking['firstname']}"
    assert booking["lastname"] == "Kumari", f"Expected lastname '{"Kumari"}', but got {booking['lastname']}"


@pytest.mark.api
@pytest.mark.regression
def test_get_booking_by_invalid_id(booking_client):
    """
    Test case for retrieving a booking by an invalid ID from the Booking API.
    This test verifies that a GET request to the Booking API with an invalid booking ID returns a 404 response.
    """
    invalid_booking_id = 999999  # Assuming this ID does not exist
    response = booking_client.get_booking_by_id(invalid_booking_id)
    assert response.status_code == 404, f"Expected status code 404, but got {response.status_code}"


@pytest.mark.api
@pytest.mark.regression
def test_get_booking_by_firstname(booking_client):
    """
    Test case for retrieving booking IDs filtered by first name from the Booking API.
    This test verifies that a GET request to the Booking API with a valid first name returns a successful response
    and a list of booking IDs.
    """
    firstname = "Savi"
    response = booking_client.get_booking_ids_by_firstname(firstname)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    booking_ids = response.json()
    assert booking_ids, f"No booking IDs found for firstname '{firstname}'"
    logger.info(f"Retrieved {len(booking_ids)} booking IDs for firstname '{firstname}'")


@pytest.mark.api
@pytest.mark.regression
def test_get_booking_by_checkin(booking_client):
    """
    Test case for retrieving booking IDs filtered by check-in date from the Booking API.
    This test verifies that a GET request to the Booking API with a valid check-in date returns a successful response
    and a list of booking IDs.
    """
    checkin_date = "2018-01-01"
    response = booking_client.get_booking_ids_by_checkin(checkin_date)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    booking_ids = response.json()
    assert booking_ids, f"No booking IDs found for check-in date '{checkin_date}'"
    logger.info(f"Retrieved {len(booking_ids)} booking IDs for check-in date '{checkin_date}'")

"""
@pytest.mark.api
@pytest.mark.regression
def test_update_booking(booking_client):
    '''
    Test case for updating an existing booking in the Booking API.
    This test verifies that a PUT request to the Booking API with valid booking data and authentication
    returns a successful response and the updated booking details.
    '''
    # First, create a booking to ensure there is a booking to update
    booking_payload = helpers.load_test_data("../testdata/booking/booking_data.json")
    response = booking_client.create_booking(booking_payload)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    created_booking = response.json()
    logger.info(f"Created booking id: {created_booking['bookingid']}")
    
    # Authenticate to get a token
    auth_response = booking_client.authenticate("admin", "password123")
    assert auth_response.status_code == 200, f"Expected status code 200, but got {auth_response.status_code}"
    token = auth_response.json().get("token")
    assert token, "Authentication failed, no token received"
    
    # Update the booking
    updated_payload = helpers.load_test_data("../testdata/booking/updated_booking_data.json")
    response = booking_client.update_booking(created_booking["bookingid"], updated_payload, token)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    updated_booking = response.json()
    logger.info(f"Updated booking data: {updated_booking}")
    assert updated_booking["firstname"] == updated_payload["firstname"], f"Expected firstname '{updated_payload['firstname']}', but got {updated_booking['firstname']}"
    assert updated_booking["lastname"] == updated_payload["lastname"], f"Expected lastname '{updated_payload['lastname']}', but got {updated_booking['lastname']}"
"""
