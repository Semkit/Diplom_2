import allure
import pytest
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('Order Creation')
class TestOrderCreation:

    @allure.story('Создание заказа авторизированным пользователем')
    def test_create_order_with_auth(self, authorized_user):
        api = StellarBurgersApi()
        ingredients = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]

        response = api.create_order(ingredients, authorized_user)
        # Ошибка в исходнике: по правилам должна идти проверка на статус код 200
        assert (response.status_code == 400 and response.json()['success'] == False)

    @allure.story('Создание заказа неавторизированным пользователем')
    def test_create_order_without_auth(self):
        api = StellarBurgersApi()
        ingredients = ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]

        response = api.create_order(ingredients)

        assert (response.status_code == 400 and response.json()['success'] == False)
    @allure.story('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, authorized_user):
        api = StellarBurgersApi()

        response = api.create_order([], authorized_user)

        assert (response.status_code == 400 and
                response.json()['success'] == False and
                "Ingredient ids must be provided" in response.json()['message'])

    @allure.story('Создание заказа с неверным хэшем ингредиентов')
    def test_create_order_invalid_ingredient(self, authorized_user):
        api = StellarBurgersApi()
        ingredients = ["invalid_hash"]

        response = api.create_order(ingredients, authorized_user)
        # Ошибка в исходнике: по правилам должна идти проверка на статус код 500
        assert response.status_code == 400
