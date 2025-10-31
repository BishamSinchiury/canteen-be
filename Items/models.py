from django.db import models
from User.models import User

# Create your models here.

from django.db import models

from django.db import models

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


