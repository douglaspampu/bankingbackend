from accounts.controller import AccountInput
from clients.models import Client

class ClientInput:
    name:str


class ClientOutput:
    name:str
    clientId:int
    accountType:str|None = None
    accountBalance:float|None = None
    accountId:int|None = None

    def setClientData(self, client:Client):
        self.name = client.name
        self.clientId = client.pk

    def setAccountData(self, account):
        self.accountType = account.type
        self.accountBalance = account.balance
        self.accountId = account.pk

    def Serialize(self):
        return {
            "name": self.name,
            "clientId":self.clientId,
            "accountType":self.accountType,
            "accountBalance": self.accountBalance,
            "accountId": self.accountId
        }

class Clients:
    def RegisterClient(self, clientInput: ClientInput, accountInput:AccountInput|None=None) -> ClientOutput:

        client = Client()

        client.name = clientInput.name

        client.save()

        clientOutput = ClientOutput()

        clientOutput.setClientData(client)

        if accountInput:
            account = accountInput.AccountFactory()
            newAcc = account.CreateAccount(accountInput, client)

            clientOutput.setAccountData(newAcc)

        return clientOutput.Serialize()
