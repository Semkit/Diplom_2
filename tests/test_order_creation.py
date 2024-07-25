import allure
import pytest
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('Order Creation')
class TestOrderCreation:

    @pytest.fixture
    def authorized_user(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        password = "password123"
        response = api.create_user(email, password, "Test User")
        return response.json()['accessToken']

    @allure.story('Create order with authorization')
    def test_create_order_with_auth(self, authorized_user):
        api = StellarBurgersApi()
        ingredients = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]

        response = api.create_order(ingredients, authorized_user)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'name' in response.json()
        assert 'order' in response.json()
        assert 'number' in response.json()['order']

    @allure.story('Create order without authorization')
    def test_create_order_without_auth(self):
        api = StellarBurgersApi()
        ingredients = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]

        response = api.create_order(ingredients)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert 'name' in response.json()
        assert 'order' in response.json()
        assert 'number' in response.json()['order']

    @allure.story('Create order without ingredients')
    def test_create_order_without_ingredients(self, authorized_user):
        api = StellarBurgersApi()

        response = api.create_order([], authorized_user)

        assert response.status_code == 400
        assert response.json()['success'] == False
        assert "Ingredient ids must be provided" in response.json()['message']

    @allure.story('Create order with invalid ingredient hash')
    def test_create_order_invalid_ingredient(self, authorized_user):
        api = StellarBurgersApi()
        ingredients = ["invalid_hash"]

        response = api.create_order(ingredients, authorized_user)

        assert response.status_code == 500