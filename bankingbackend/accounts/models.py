from django.db import models
from clients.models import Client
from django.utils.translation import gettext_lazy as _

# Create your models here.

class AccountTypes(models.TextChoices):
    STANDARD = 'standard', _('standard')
    GOLD = 'gold', _('gold')
    PLATINIUM = 'platinium', _('platinium')

class AccountLimits(models.IntegerChoices):
    STANDARD = 0
    GOLD = 100
    PLATINIUM = 1000

class Accounts (models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=AccountTypes.choices, default=AccountTypes.STANDARD)
    balance = models.FloatField(default=0)
    limit = models.FloatField()
