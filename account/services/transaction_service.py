from account.models.account import Account
from account.models.transaction import Transaction, TransactionType
from rest_framework.exceptions import ValidationError


class TransactionService:
    def send(self, sender_account: Account, receiver_account: Account, amount: float):
        if receiver_account == sender_account:
            raise ValidationError("Could not send into same account.")

        if sender_account.balance <= 0:
            raise ValidationError("Your balance on the account should be greater than 0.")
        elif sender_account.balance < amount:
            raise ValidationError("Your balance on the account should be greater than the amount sent.")

        Transaction.objects.create(account=sender_account, type=TransactionType.send, target=receiver_account,
                                   amount=-amount)
        Transaction.objects.create(account=receiver_account, type=TransactionType.receive, target=sender_account,
                                   amount=amount)

        sender_account.balance = sender_account.balance - amount
        sender_account.save(update_fields=['balance'])

        receiver_account.balance = receiver_account.balance + amount
        receiver_account.save(update_fields=['balance'])
