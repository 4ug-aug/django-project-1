from django.db import models
from django.conf import settings
from django.db.models.base import Model
from django_mysql.models import ListCharField
from django.contrib.auth.models import User
import datetime
from django.core.files.storage import FileSystemStorage

from django.core.files import File
import os

# Create your models here.
class Bruger(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    account = models.IntegerField()

class Beverage(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='tommerbob/tømmerbob/polls/static/polls/images')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return self.title

# Class to make an order for a user
class Order(models.Model):
    order = models.ForeignKey(Beverage, null=False, related_name='order', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
    user = models.ForeignKey(Bruger, null=True, on_delete=models.CASCADE)


    def placeOrder(self):
        self.save()

    def get_orders_by_customer(bruger_id):
        return Order.objects.filter(bruger=bruger_id).order_by('-date')