import uuid
from django.db import models
from account.models.timestamped import Timestamped
from account.models.account import Account
from account.utils.enum import ModelEnum


class TransactionType(ModelEnum):
    send = "send"
    receive = "receive"


class Transaction(Timestamped):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transaction_account")
    target = models.ForeignKey(Account, null=True, on_delete=models.PROTECT, related_name="transaction_sender")
    type = models.CharField(
        max_length=16,
        choices=TransactionType.choices(),
    )
    amount = models.FloatField(default=0.0)
