from django.contrib import admin
from account.models.account import Account
from account.models.transaction import Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "id", "email", "balance"
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "account", "target", "type", "amount"
    )
