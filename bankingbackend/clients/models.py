from django.db import models
from datetime import datetime

# Create your models here.

class Client (models.Model):
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(default=datetime.now())