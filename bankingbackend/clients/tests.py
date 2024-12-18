from django.test import TestCase
from clients.controller import Clients, ClientInput
from accounts.controller import AccountTypes, AccountInput

# Create your tests here.
class ClientsTest(TestCase):
    def test_RegisterClientAccount(self):
        input = ClientInput()
        account = AccountInput()

        account.type = AccountTypes.STANDARD

        input.name = "testUser"

        newClient = Clients()

        output = newClient.RegisterClient(input, account)

        self.assertEqual(output.get("accountBalance"), 0)
        self.assertEqual(output.get("name"), 'testUser')

    def test_RegisterClientNoAccount(self):
        input = ClientInput()

        input.name = "testUser"

        newClient = Clients()

        output = newClient.RegisterClient(input)

        self.assertEqual(output.get("name"), 'testUser')
        self.assertFalse(output.get('accountId'))