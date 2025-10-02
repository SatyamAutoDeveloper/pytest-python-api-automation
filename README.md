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
- **configs.ini**: For environment-specific configurations like base URLs.
- **testdata/**: To store test data, including JSON schemas for response validation.
- **reports/**: Where test execution reports will be saved.
- **tests/**: Contains all your test files.
- **conftest.py**: A special pytest file for sharing fixtures across multiple test files.
- **pytest.ini**: For custom markers, logging and html report configuration.
- **requirements.txt**: To list all project dependencies.
