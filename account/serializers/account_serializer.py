from rest_framework import serializers
from account.models.transaction import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("uuid", "email", "balance", "created_at", "updated_at")
        read_only_fields = ("balance",)
