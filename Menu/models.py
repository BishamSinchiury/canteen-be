from django.db import models
from User.models import User

# Create your models here.

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    veg = models.BooleanField(default=True)
    unit = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    veg = models.BooleanField(default=True)
    unit = models.CharField(max_length=50)
    price = models.FloatField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp of creation
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,   
        null=True,
        blank=True,
        related_name='transactions_created'
    )

    def save(self, *args, **kwargs):
        # automatically calculate total price before saving
        self.total_price = self.item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} × {self.item.name} @ {self.created_at.strftime('%Y-%m-%d %H:%M')}"