import factory
from account.models.account import Account
from account.models.transaction import Transaction


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
