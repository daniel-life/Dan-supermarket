from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField()
    description = models.TextField()
    price = models.FloatField()
