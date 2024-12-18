from accounts.controller import Transaction, AccountInput

# Create your views here.
def MakeTransaction(originAccountId:int, transaction:Transaction):
    accController = AccountInput()

    acc = accController.getAccount(originAccountId)

    updatedAcc = acc.MakeTransaction(transaction)

    return updatedAcc