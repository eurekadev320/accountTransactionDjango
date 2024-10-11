from django.test import TestCase
from rest_framework.test import APIClient
from account.tests.factories import AccountFactory


class TestAccountView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account1 = AccountFactory(email="sender@test.com", balance=20.5)
        self.account2 = AccountFactory(email="receiver@test.com", balance=30.5)

    def test_transaction(self):
        # should show an error when the amount is 0
        response = self.client.post(f"/accounts/{self.account1.uuid}/send/", data={
            'receiver': self.account2.email,
            'amount': 0
        })

        assert response.status_code == 400
        data = response.json()
        assert data[0] == 'Amount should be greater than 0.'

        # should show an error when the receiver is same as sender
        response = self.client.post(f"/accounts/{self.account1.uuid}/send/", data={
            'receiver': self.account1.email,
            'amount': 10
        })

        assert response.status_code == 400
        data = response.json()
        assert data[0] == 'Could not send into same account.'

        # should show an error when the amount is greater than account balance
        response = self.client.post(f"/accounts/{self.account1.uuid}/send/", data={
            'receiver': self.account2.email,
            'amount': self.account1.balance + 1
        })

        assert response.status_code == 400
        data = response.json()
        assert data[0] == 'Your balance on the account should be greater than the amount sent.'

        response = self.client.post(f"/accounts/{self.account1.uuid}/send/", data={
            'receiver': self.account2.email,
            'amount': 10
        })

        assert response.status_code == 200
        data = response.json()

        account1_balance = self.account1.balance - 10
        account2_balance = self.account2.balance + 10

        self.account1.refresh_from_db()
        self.account2.refresh_from_db()

        assert self.account1.balance == account1_balance
        assert self.account2.balance == account2_balance

        assert data['balance'] == self.account1.balance
        assert data['email'] == self.account1.email

    def test_transaction_history(self):
        self.client.post(f"/accounts/{self.account1.uuid}/send/", data={
            'receiver': self.account2.email,
            'amount': 10
        })

        self.client.post(f"/accounts/{self.account1.uuid}/send/", data={
            'receiver': self.account2.email,
            'amount': 5
        })

        response = self.client.get(f"/accounts/{self.account1.uuid}/transactions/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['amount'] == -10
        assert data[0]['target']['email'] == self.account2.email
        assert data[1]['amount'] == -5
        assert data[1]['target']['email'] == self.account2.email
