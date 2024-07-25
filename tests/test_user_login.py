import allure
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('User Login')
class TestUserLogin:

    @allure.story('Login with valid credentials')
    def test_login_valid_credentials(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        password = "password123"

        # Create user first
        api.create_user(email, password, "Test User")

        # Try to login
        response = api.login_user(email, password)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()
        assert 'user' in response.json()

    @allure.story('Login with invalid credentials')
    def test_login_invalid_credentials(self):
        api = StellarBurgersApi()
        email = generate_random_email()

        response = api.login_user(email, "wrongpassword")

        assert response.status_code == 401
        assert response.json()['success'] == False
        assert "email or password are incorrect" in response.json()['message']