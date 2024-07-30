import pytest
from utils.helpers import generate_random_email
from utils.api import StellarBurgersApi


@pytest.fixture
def authorized_user():
    api = StellarBurgersApi()
    email = generate_random_email()
    password = "password123"
    response = api.create_user(email, password, "Test User")
    return response.json()['accessToken']