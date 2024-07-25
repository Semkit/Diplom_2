import pytest
import allure
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('User Creation')
class TestUserCreation:

    @allure.story('Create unique user')
    def test_create_unique_user(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        response = api.create_user(email, "password123", "Test User")

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'user' in response.json()
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()

    @allure.story('Create existing user')
    def test_create_existing_user(self):
        api = StellarBurgersApi()
        email = generate_random_email()

        # Create user first time
        api.create_user(email, "password123", "Test User")

        # Try to create the same user again
        response = api.create_user(email, "password123", "Test User")

        assert response.status_code == 403
        assert response.json()['success'] == False
        assert "User already exists" in response.json()['message']

    @allure.story('Create user with missing field')
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        api = StellarBurgersApi()
        data = {
            "email": generate_random_email(),
            "password": "password123",
            "name": "Test User"
        }
        del data[missing_field]

        response = api.create_user(**data)

        assert response.status_code == 403
        assert response.json()['success'] == False
        assert "Email, password and name are required fields" in response.json()['message']