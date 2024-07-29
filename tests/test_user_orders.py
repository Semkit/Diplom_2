import allure
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('Заказы пользователя')
class TestUserOrders:

    @allure.title('Получение списка заказов авторизированного пользователя')
    def test_get_orders_authorized(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        password = "password123"

        # Cоздание пользователя и авторизация
        api.create_user(email, password, "Test User")
        login_response = api.login_user(email, password)
        token = login_response.json()['accessToken']

        # Получение списка заказов
        response = api.get_user_orders(token)

        assert (response.status_code == 200 and
                response.json()['success'] == True and
                'orders' in response.json() and
                'total' in response.json() and
                'totalToday' in response.json())


    @allure.story('Получение списка заказов неавторизированного пользователя')
    def test_get_orders_unauthorized(self):
        api = StellarBurgersApi()

        # Try to get orders without token
        response = api.get_user_orders(None)

        assert response.status_code == 401
        assert response.json()['success'] == False
        assert "You should be authorised" in response.json()['message']