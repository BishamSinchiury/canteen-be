from django.db import models
from User.models import User

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    veg = models.BooleanField(default=True)
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    ingredients = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class ItemUnit(models.Model):
    item = models.ForeignKey(Item, related_name='units', on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=50)  # e.g. Small, Medium, Large
    price = models.FloatField()

    def __str__(self):
        return f"{self.item.name} - {self.unit_name} ({self.price})"

class NonFood(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='nonfood_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
