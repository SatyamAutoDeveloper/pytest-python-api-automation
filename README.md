# pytest-python-api-automation
API Automation using Python and Pytest Framework.

**Environment Setup:**
Download and Install Python 3.10+ version

**Framework Setup:**

1. Clone Github Repository: https://github.com/SatyamAutoDeveloper/pytest-python-api-automation
2. Create Virtual Environment.
3. Install all dependencies/requirements with below command:
   pip install -r requirements.txt

**Framework Structure:**

- **api_clients/**: To create wrapper classes for your API endpoints (abstracts requests logic).
- **.github/**: Contains github actions workflows for API Test Execution.
- **configs.ini**: For environment-specific configurations like base URLs.
- **testdata/**: To store test data, including JSON schemas for response validation.
- **reports/**: Where test execution reports will be saved.
- **tests/**: Contains all your test files.
- **conftest.py**: A special pytest file for sharing fixtures across multiple test files.
- **pytest.ini**: For custom markers, logging and html report configuration.
- **requirements.txt**: To list all project dependencies.

**Commands for Running Test in Local:**

- **JsonPlaceHolder API**: pytest tests\test_jsonplaceholder_api.py 
- **Booking API**: $env:API_USERNAME="original_username"; $env:API_PASSWORD="original_password"; pytest -v tests\test_booking_api.py
- **GoRest API**: $env:GOREST_TOKEN="original_gorest_pat"; pytest -v tests\test_go_rest_api.py
- **PetStore API**: pytest tests\test_swagger_pet_store_api.py


**Implemented retry logic on API level for gorestAPI**

## Overview
This section describes the implementation of retry logic at the API level within the project.

## Details
- **Feature**: Retry Logic
- **Purpose**: To enhance the reliability of API calls by automatically retrying failed requests.
- **Implementation**: The retry logic is designed to handle transient errors, ensuring that the application can recover from temporary issues without manual intervention.

## Usage
- The retry mechanism is invoked automatically during API calls.
- Configurable parameters may include the number of retries and the delay between attempts.

## Benefits
- Improved resilience of the application.
- Reduced likelihood of failure due to temporary network issues or server unavailability.

## Conclusion
The implemented retry logic significantly contributes to the robustness of the API interactions in the project.
