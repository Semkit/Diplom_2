import requests

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

class StellarBurgersApi:
    def __init__(self):
        self.base_url = BASE_URL

    def create_user(self, email, password, name):
        return requests.post(f"{self.base_url}/auth/register", json={
            "email": email,
            "password": password,
            "name": name
        })

    def login_user(self, email, password):
        return requests.post(f"{self.base_url}/auth/login", json={
            "email": email,
            "password": password
        })

    def update_user(self, token, **kwargs):
        headers = {"Authorization": token}
        return requests.patch(f"{self.base_url}/auth/user", json=kwargs, headers=headers)

    def create_order(self, ingredients, token=None):
        headers = {"Authorization": token} if token else {}
        return requests.post(f"{self.base_url}/orders", json={"ingredients": ingredients}, headers=headers)

    def get_user_orders(self, token):
        headers = {"Authorization": token}
        return requests.get(f"{self.base_url}/orders", headers=headers)