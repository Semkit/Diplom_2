import pytest
import allure
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('Создание пользователя')
class TestUserCreation:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        response = api.create_user(email, "password123", "Test User")

        assert (response.status_code == 200 and response.json()['success'] == True and
                'user' in response.json() and
                'accessToken' in response.json() and
                'refreshToken' in response.json())

    @allure.title('Создание уже существующего пользователя')
    def test_create_existing_user(self):
        api = StellarBurgersApi()
        email = generate_random_email()

        # создание первого
        api.create_user(email, "password123", "Test User")

        # попытка повторного создания
        response = api.create_user(email, "password123", "Test User")

        assert (response.status_code == 403 and
                response.json()['success'] == False and
                "User already exists" in response.json()['message'])

    @allure.title('Создание пользователя с одним из пропущенных полей')
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        api = StellarBurgersApi()
        data = {
            "email": generate_random_email(),
            "password": "password123",
            "name": "Test User"
        }

        data[missing_field] = None

        response = api.create_user(**data)

        assert (response.status_code == 403 and
                '"success":false' in response.text and
                response.json()['message'] == 'Email, password and name are required fields')