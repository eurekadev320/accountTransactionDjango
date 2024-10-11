from django.test import TestCase
from rest_framework.test import APIClient
from account.tests.factories import AccountFactory


class TestAccountView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_account_creation(self):
        response = self.client.post("/accounts/", data={
            'email': 'test@test.com'
        })

        assert response.status_code == 201
        data = response.json()

        assert data['email'] == 'test@test.com'
        assert data['balance'] == 0

        # should show an error when using an existing email
        response = self.client.post("/accounts/", data={
            'email': 'test@test.com'
        })

        assert response.status_code == 400
        data = response.json()
        assert data['email'][0] == 'account with this email already exists.'

    def test_account_detail(self):
        account = AccountFactory(balance=20.5, email="test@test.com")
        response = self.client.get(f"/accounts/{account.uuid}/")

        assert response.status_code == 200
        data = response.json()
        assert data['uuid'] == str(account.uuid)
        assert data['email'] == "test@test.com"
        assert data['balance'] == 20.5
