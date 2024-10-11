import uuid
from django.db import models
from account.models.timestamped import Timestamped


class Account(Timestamped):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    balance = models.FloatField(default=0.0)
