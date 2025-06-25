from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    current_stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_photo/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.unit_price})"


from django.db import models
from django.contrib.auth.models import User
from accounts.models import Department

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    current_stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_photo/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.unit_price})"