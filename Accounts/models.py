# accounts/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from Items.models import Item, ItemUnit  # Assuming Items app
from django.core.validators import MinValueValidator
from User.models import User
# --------------------------
# Creditors and Vendors
# --------------------------

class Creditor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    account_balance = models.FloatField(default=0)  # Track balance
    contact_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    account_balance = models.FloatField(default=0)  # Track balance
    contact_no = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

# --------------------------
# Cash Account (singleton)
# --------------------------

class CashAccount(models.Model):
    balance = models.FloatField(default=0)

    def __str__(self):
        return f"Cash: {self.balance}"

    class Meta:
        verbose_name = "Cash Account"
        verbose_name_plural = "Cash Account"

# --------------------------
# Sales & Purchases
# --------------------------

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('credit', 'Credit'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    unit = models.ForeignKey(ItemUnit, on_delete=models.CASCADE)
    price = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sales_created', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sales_updated', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    creditor = models.ForeignKey(Creditor, on_delete=models.SET_NULL, blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.unit.price  # Fetch price from ItemUnit

        super().save(*args, **kwargs)

        # Update accounts
        cash_account, _ = CashAccount.objects.get_or_create(id=1)
        if self.payment_type == 'cash':
            cash_account.balance += self.price
            cash_account.save()
        elif self.payment_type == 'credit' and self.creditor:
            self.creditor.account_balance += self.price
            self.creditor.save()

    def __str__(self):
        return f"{self.item.name} - {self.unit.unit_name} ({self.payment_type})"


class Purchase(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('credit', 'Credit'),
    ]
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    unit = models.ForeignKey(ItemUnit, on_delete=models.CASCADE)
    price = models.FloatField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='purchases_created', null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='purchases_updated', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.unit.price  # Fetch price from ItemUnit

        super().save(*args, **kwargs)

        # Update accounts
        cash_account, _ = CashAccount.objects.get_or_create(id=1)
        if self.payment_type == 'cash':
            cash_account.balance -= self.price
            cash_account.save()
        elif self.payment_type == 'credit' and self.vendor:
            self.vendor.account_balance += self.price
            self.vendor.save()

    def __str__(self):
        return f"{self.item.name} - {self.unit.unit_name} ({self.payment_type})"

# --------------------------
# Income & Expense
# --------------------------

class Income(models.Model):
    amount = models.FloatField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, blank=True, null=True)
    creditor_payment = models.ForeignKey(Creditor, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        cash_account, _ = CashAccount.objects.get_or_create(id=1)

        # Update accounts based on origin
        if self.sale:
            # Cash already added in Sale model
            pass
        elif self.creditor_payment:
            # Payment from creditor
            cash_account.balance += self.amount
            cash_account.save()
            self.creditor_payment.account_balance -= self.amount
            self.creditor_payment.save()
        else:
            # Other source, just add to cash
            cash_account.balance += self.amount
            cash_account.save()

    def __str__(self):
        return f"Income: {self.amount}"


class Expense(models.Model):
    amount = models.FloatField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL, blank=True, null=True)
    vendor_payment = models.ForeignKey(Vendor, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        cash_account, _ = CashAccount.objects.get_or_create(id=1)

        if self.purchase:
            # Purchase expense already deducted in Purchase model
            pass
        elif self.vendor_payment:
            cash_account.balance -= self.amount
            cash_account.save()
            self.vendor_payment.account_balance -= self.amount
            self.vendor_payment.save()
        else:
            cash_account.balance -= self.amount
            cash_account.save()

    def __str__(self):
        return f"Expense: {self.amount}"