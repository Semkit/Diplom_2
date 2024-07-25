import allure
from utils.api import StellarBurgersApi
from utils.helpers import generate_random_email


@allure.feature('User Update')
class TestUserUpdate:

    @allure.story('Update user with authorization')
    def test_update_user_with_auth(self):
        api = StellarBurgersApi()
        email = generate_random_email()
        password = "password123"

        # Create user
        create_response = api.create_user(email, password, "Test User")
        token = create_response.json()['accessToken']

        # Update user
        new_name = "Updated User"
        update_response = api.update_user(token, name=new_name)

        assert update_response.status_code == 200
        assert update_response.json()['success'] == True
        assert update_response.json()['user']['name'] == new_name

    @allure.story('Update user without authorization')
    def test_update_user_without_auth(self):
        api = StellarBurgersApi()

        # Try to update without token
        update_response = api.update_user(None, name="Updated User")

        assert update_response.status_code == 401
        assert update_response.json()['success'] == False
        assert "You should be authorised" in update_response.json()['message']

    @allure.story('Update user email to existing email')
    def test_update_user_existing_email(self):
        api = StellarBurgersApi()
        email1 = generate_random_email()
        email2 = generate_random_email()
        password = "password123"

        # Create two users
        create_response1 = api.create_user(email1, password, "Test User 1")
        api.create_user(email2, password, "Test User 2")

        token = create_response1.json()['accessToken']

        # Try to update first user's email to second user's email
        update_response = api.update_user(token, email=email2)

        assert update_response.status_code == 403
        assert update_response.json()['success'] == False
        assert "User with such email already exists" in update_response.json()['message']