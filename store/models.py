from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=800)
    price = models.FloatField()
    description = models.TextField()
    imglink = models.CharField(max_length=800)

class Order(models.Model):
    first_name = models.CharField(max_length=400)
    last_name = models.CharField(max_length=400)
    address = models.CharField(max_length=600)
    city = models.CharField(max_length=400)
    payment_method = models.CharField(max_length=400)
    payment_data = models.CharField(max_length=400)
    items = models.TextField()
    fulfilled = models.BooleanField()


