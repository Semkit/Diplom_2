import allure
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('Авторизация пользователя')
class TestUserLogin:

    @allure.title('Попытка авторизация с верными данными')
    def test_login_valid_credentials(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        password = "password123"

        # Создание пользователя
        api.create_user(email, password, "Test User")

        # Авторизация
        response = api.login_user(email, password)

        assert (response.status_code == 200 and response.json()['success'] == True and
                'accessToken' in response.json() and
                'refreshToken' in response.json() and
                'user' in response.json())

    @allure.title('Попытка авторизации с неверными данными')
    def test_login_invalid_credentials(self):
        api = StellarBurgersApi()
        email = generate_random_email()

        response = api.login_user(email, "wrongpassword")

        assert (response.status_code == 401 and
                response.json()['success'] == False and
                "email or password are incorrect" in response.json()['message'])
