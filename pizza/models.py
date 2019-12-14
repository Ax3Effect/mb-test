from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from pizza import OrderStatus

# Create your models here.

class AnonymousCustomer(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=300)

class MenuItemSize(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        default = Decimal(0.00)
    )


class MenuItem(models.Model):
    name = models.CharField(max_length = 80)
    description = models.CharField(max_length = 200, null=True, blank=True)
    size = models.ManyToManyField(MenuItemSize)
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        default=Decimal(0.00)
    )
    available = models.BooleanField(default=True)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(AnonymousCustomer, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.CharField(max_length=30, choices=OrderStatus.CHOICES, default=OrderStatus.DRAFT)



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', editable=False, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        default=Decimal(0.00)
    )

    @property
    def total(self):
        total = Decimal(0.00)
        total += self.price * self.quantity
        for i in self.sizes.all():
            total += i.price * self.quantity
        return total

class OrderItemSize(models.Model):
    item = models.ForeignKey(OrderItem, related_name='sizes', editable=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        default = Decimal(0.00)
    )