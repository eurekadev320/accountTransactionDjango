from rest_framework import serializers
from account.models.transaction import Transaction
from account.models.account import Account


class TransactionRequestSerializer(serializers.Serializer):
    receiver = serializers.EmailField(required=True)
    amount = serializers.FloatField(default=0.0)


class TransactionTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("uuid", "email")


class TransactionSerializer(serializers.ModelSerializer):
    target = TransactionTargetSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ("uuid", "target", "type", "amount", "created_at", "updated_at")
