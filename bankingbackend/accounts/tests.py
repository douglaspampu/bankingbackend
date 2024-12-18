from django.test import TestCase
from accounts.controller import AccountInput, StandardAccount, AccountTypes, Transaction, PlatinumAccount
from clients.models import Client
from accounts.models import Accounts

from accounts.views import MakeTransaction

# Create your tests here.

class AccountsTests(TestCase):

    def setUp(self):
        self.testClient = Client.objects.create(name="test")

    def test_CreateStdAccount(self):
        accInput = AccountInput()
        accInput.type = AccountTypes.STANDARD

        acc = accInput.AccountFactory()

        newAcc = acc.CreateAccount(accInput, self.testClient)

        self.assertEqual(newAcc.balance, 0)
        self.assertEqual(newAcc.limit, 0)

    def test_CreateGoldAccount(self):
        accInput = AccountInput()
        accInput.type = AccountTypes.GOLD

        acc = accInput.AccountFactory()

        newAcc = acc.CreateAccount(accInput, self.testClient)

        self.assertEqual(newAcc.balance, 0)
        self.assertEqual(newAcc.limit, 100)

    def test_CreatePlatiniumAccount(self):
        accInput = AccountInput()
        accInput.type = AccountTypes.PLATINIUM

        acc = accInput.AccountFactory()

        newAcc = acc.CreateAccount(accInput, self.testClient)

        self.assertEqual(newAcc.balance, 0)
        self.assertEqual(newAcc.limit, 1000)

class TransactionTest(TestCase):
    def setUp(self):
        self.originClient = Client.objects.create(name="origin")
        self.destinClient = Client.objects.create(name="destin")

        destinAccount = AccountInput()
        destinAccount.type = AccountTypes.STANDARD

        destinAcc = destinAccount.AccountFactory()

        self.destinAccount = destinAcc.CreateAccount(destinAccount, self.destinClient)
        

    def test_standardTransfer(self):
        originAccount = Accounts.objects.create(client=self.originClient, type=AccountTypes.STANDARD, balance=1000, limit=0)

        originStdAcc = StandardAccount(originAccount)

        transaction = Transaction()
        transaction.destinAccount = self.destinAccount.pk
        transaction.value = 100

        originalDestinBalance = self.destinAccount.balance

        orAcc = originStdAcc.MakeTransaction(transaction)

        newDestinAcc = Accounts.objects.get(pk=self.destinAccount.pk)

        self.assertEqual(orAcc.balance, 900)
        self.assertEqual(newDestinAcc.balance, originalDestinBalance + transaction.value)

    def test_StandardTransferNoLimit(self):
        originAccount = Accounts.objects.create(client=self.originClient, type=AccountTypes.STANDARD, balance=10, limit=0)

        originStdAcc = StandardAccount(originAccount)

        transaction = Transaction()
        transaction.destinAccount = self.destinAccount.pk
        transaction.value = 100

        originalDestinBalance = self.destinAccount.balance

        orAcc = originStdAcc.MakeTransaction(transaction)

        newDestinAcc = Accounts.objects.get(pk=self.destinAccount.pk)

        self.assertEqual(orAcc.balance, 10)
        self.assertEqual(newDestinAcc.balance, originalDestinBalance)

    def test_StandardTransferUsingLimit(self):
        originAccount = Accounts.objects.create(client=self.originClient, type=AccountTypes.STANDARD, balance=10, limit=100)

        originStdAcc = StandardAccount(originAccount)

        transaction = Transaction()
        transaction.destinAccount = self.destinAccount.pk
        transaction.value = 100

        originalDestinBalance = self.destinAccount.balance

        orAcc = originStdAcc.MakeTransaction(transaction)

        newDestinAcc = Accounts.objects.get(pk=self.destinAccount.pk)

        self.assertEqual(orAcc.balance, -90)
        self.assertEqual(newDestinAcc.balance, originalDestinBalance + transaction.value)

class TransactionPlatinumTest(TestCase):
    def setUp(self):
        self.originClient = Client.objects.create(name="origin")
        self.destinClient = Client.objects.create(name="destin")

        destinAccount = AccountInput()
        destinAccount.type = AccountTypes.STANDARD

        destinAcc = destinAccount.AccountFactory()

        self.destinAccount = destinAcc.CreateAccount(destinAccount, self.destinClient)

    def test_transferWithCashBack(self):
        originAccount = Accounts.objects.create(client=self.originClient, type=AccountTypes.PLATINIUM, balance=1000, limit=100)

        originPlaAcc = PlatinumAccount(originAccount)

        transaction = Transaction()
        transaction.destinAccount = self.destinAccount.pk
        transaction.value = 100

        originalDestinBalance = self.destinAccount.balance

        orAcc = originPlaAcc.MakeTransaction(transaction)

        newDestinAcc = Accounts.objects.get(pk=self.destinAccount.pk)

        self.assertEqual(orAcc.balance, 1000 - (transaction.value * 0.95))

        self.assertEqual(newDestinAcc.balance, originalDestinBalance + transaction.value)

class AccountsViewsTest(TestCase):
    def setUp(self):
        self.originClient = Client.objects.create(name="origin")
        self.destinClient = Client.objects.create(name="destin")

        destinAccount = AccountInput()
        destinAccount.type = AccountTypes.STANDARD

        destinAcc = destinAccount.AccountFactory()

        self.destinAccount = destinAcc.CreateAccount(destinAccount, self.destinClient)

    def test_ViewsMakeTransfer_StdAcc(self):
        originAccount = Accounts.objects.create(client=self.originClient, type=AccountTypes.STANDARD, balance=100, limit=0)

        transaction = Transaction()
        transaction.destinAccount = self.destinAccount.pk
        transaction.value = 100

        updAcc = MakeTransaction(originAccount.pk, transaction)

        self.assertEqual(updAcc.balance, 0)

    def test_ViewsMakeTransfer_GoldAcc(self):
        originAccount = Accounts.objects.create(client=self.originClient, type=AccountTypes.GOLD, balance=100, limit=0)

        transaction = Transaction()
        transaction.destinAccount = self.destinAccount.pk
        transaction.value = 100

        updAcc = MakeTransaction(originAccount.pk, transaction)

        self.assertEqual(updAcc.balance, 0)

    def test_ViewsMakeTransfer_PlaAcc(self):
        originAccount = Accounts.objects.create(client=self.originClient, type=AccountTypes.PLATINIUM, balance=100, limit=0)

        transaction = Transaction()
        transaction.destinAccount = self.destinAccount.pk
        transaction.value = 100

        updAcc = MakeTransaction(originAccount.pk, transaction)

        self.assertEqual(updAcc.balance, 100 - (transaction.value * (0.95)))