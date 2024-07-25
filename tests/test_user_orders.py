import allure
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('User Orders')
class TestUserOrders:

    @allure.story('Get orders for authorized user')
    def test_get_orders_authorized(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        password = "password123"

        # Create user and login
        api.create_user(email, password, "Test User")
        login_response = api.login_user(email, password)
        token = login_response.json()['accessToken']

        # Get orders
        response = api.get_user_orders(token)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'orders' in response.json()
        assert 'total' in response.json()
        assert 'totalToday' in response.json()

    @allure.story('Get orders for unauthorized user')
    def test_get_orders_unauthorized(self):
        api = StellarBurgersApi()

        # Try to get orders without token
        response = api.get_user_orders(None)

        assert response.status_code == 401
        assert response.json()['success'] == False
        assert "You should be authorised" in response.json()['message']