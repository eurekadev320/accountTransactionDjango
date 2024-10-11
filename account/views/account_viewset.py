from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction
from account.models.account import Account
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.exceptions import ValidationError
from account.serializers.transaction_serializer import TransactionRequestSerializer, TransactionSerializer
from account.serializers.account_serializer import AccountSerializer
from rest_framework.response import Response
from account.models.transaction import Transaction
from account.services.transaction_service import TransactionService

transaction_service = TransactionService()


class AccountViewSet(viewsets.GenericViewSet, RetrieveModelMixin, CreateModelMixin):
    lookup_field = "uuid"
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @swagger_auto_schema(responses={200: TransactionSerializer(many=True)})
    @action(detail=True, methods=["GET"])
    def transactions(self, request, uuid):
        account = Account.objects.filter(uuid=uuid).first()
        transactions = Transaction.objects.filter(account=account)

        return Response(TransactionSerializer(transactions, many=True).data)

    @swagger_auto_schema(request_body=TransactionRequestSerializer, responses={200: AccountSerializer()})
    @action(detail=True, methods=["POST"])
    @transaction.atomic
    def send(self, request, uuid):
        request_serializer = TransactionRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        validated_data = request_serializer.validated_data

        receiver = validated_data.get("receiver")

        receiver_account = Account.objects.filter(email=receiver).first()

        if not receiver_account:
            raise ValidationError("Invalid receiver account.")

        sender_account = Account.objects.filter(uuid=uuid).first()

        if not sender_account:
            raise ValidationError("Invalid sender account.")

        amount = validated_data.get('amount')

        if amount <= 0:
            raise ValidationError("Amount should be greater than 0.")

        transaction_service.send(sender_account=sender_account, receiver_account=receiver_account, amount=amount)

        sender_account.refresh_from_db()

        return Response(AccountSerializer(sender_account).data)
