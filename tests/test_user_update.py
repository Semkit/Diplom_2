import allure
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('Обновление информации о пользователе')
class TestUserUpdate:

    @allure.title('Обновление данных авторизированного пользователя')
    def test_update_user_with_auth(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        password = "password123"

        # Создание пользователя
        create_response = api.create_user(email, password, "Test User")
        token = create_response.json()['accessToken']

        # Обновление данных
        new_name = "Updated User"
        update_response = api.update_user(token, name=new_name)

        assert (update_response.status_code == 200 and
                update_response.json()['success'] == True and
                update_response.json()['user']['name'] == new_name)

    @allure.title('Обновление данных неавторизированного пользователя')
    def test_update_user_without_auth(self):
        api = StellarBurgersApi()

        # Попытка обновление данных без токена
        update_response = api.update_user(None, name="Updated User")

        assert (update_response.status_code == 401 and
                update_response.json()['success'] == False and
                "You should be authorised" in update_response.json()['message'])
    @allure.title('Смена электронной почты на уже используемую')
    def test_update_user_existing_email(self):
        api = StellarBurgersApi()
        email1 = generate_random_email()
        email2 = generate_random_email()
        password = "password123"

        # Создание пользователей
        create_response1 = api.create_user(email1, password, "Test User 1")
        api.create_user(email2, password, "Test User 2")

        token = create_response1.json()['accessToken']

        # Обновление электронной почты
        update_response = api.update_user(token, email=email2)

        assert (update_response.status_code == 403 and
                update_response.json()['success'] == False and
                "User with such email already exists" in update_response.json()['message'])
