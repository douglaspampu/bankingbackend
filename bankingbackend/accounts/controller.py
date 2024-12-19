from accounts.models import Accounts
from enum import Enum
from django.db import transaction

class AccountTypes(Enum):
    STANDARD = 'standard'
    GOLD = 'gold'
    PLATINIUM = 'platinium'

class Transaction:
    destinAccount:int
    value:float

class AccountInput:
    type:AccountTypes
    balance:float = 0
    limit:float = 0

    def AccountFactory(self):
        if self.type == AccountTypes.STANDARD:
            return StandardAccount()
        elif self.type == AccountTypes.GOLD:
            return GoldAccount()
        elif self.type == AccountTypes.PLATINIUM:
            return PlatinumAccount()
        
    def getAccount(self, accountId:int):
        acc = Accounts.objects.get(pk=accountId)

        if acc.type == AccountTypes.STANDARD.value:
            return StandardAccount(acc)
        elif acc.type == AccountTypes.GOLD.value:
            return GoldAccount(acc)
        elif acc.type == AccountTypes.PLATINIUM.value:
            return PlatinumAccount(acc) 


class Account:
    limit = 0

    def __init__(self, accountData:Accounts|None = None):
        if accountData:
            self.accountData = accountData


    def CreateAccount(self, account_input:AccountInput, client):
        account = Accounts()

        account.client = client
        account.type = account_input.type
        account.limit = self.limit

        account.save()

        return account

    def ValidateTransaction(self, account:Accounts, value:float):
        if account.balance + account.limit >= value:
            return True
        return False

    @transaction.atomic
    def MakeTransaction(self, transaction_data:Transaction):
        if not self.accountData:
            raise ValueError('Origin account is not defined')
        destin_account = Accounts.objects.get(pk=transaction_data.destinAccount)

        if self.ValidateTransaction(self.accountData, transaction_data.value):
            self.accountData.balance -= transaction_data.value
            destin_account.balance += transaction_data.value

            self.accountData.save()
            destin_account.save()

        return self.accountData


class StandardAccount(Account):
    limit = 0


class GoldAccount(Account):
    limit = 100

class PlatinumAccount(Account):
    limit = 1000

    @transaction.atomic
    def MakeTransaction(self, transaction_data:Transaction):
        origin_account = Accounts.objects.get(pk=self.accountData.pk)
        destin_account = Accounts.objects.get(pk=transaction_data.destinAccount)

        if self.ValidateTransaction(origin_account, transaction_data.value):
            origin_account.balance -= transaction_data.value * 0.95
            destin_account.balance += transaction_data.value

            origin_account.save()
            destin_account.save()

        return origin_account
