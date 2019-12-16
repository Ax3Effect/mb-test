from django.db import models
from decimal import Decimal
from django.core.validators import MinValueValidator
from pizza import OrderStatus

# Create your models here.

class AnonymousCustomer(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    address = models.CharField(max_length=300)
    email = models.EmailField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MenuItemSize(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        default = Decimal(0.00)
    )
    slug = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return "MenuItemSize {} - ${}".format(self.name, self.price)


class MenuItem(models.Model):
    name = models.CharField(max_length = 80)
    description = models.CharField(max_length = 200, null=True, blank=True)
    size = models.ManyToManyField(MenuItemSize)
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        default=Decimal(0.00)
    )
    available = models.BooleanField(default=True)

    def __str__(self):
        return "{} MenuItem {} {} ${}".format(self.id, self.name, self.description, self.price)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(AnonymousCustomer, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.CharField(max_length=30, choices=OrderStatus.CHOICES, default=OrderStatus.DRAFT)

    def all_statuses(self):
        available = []
        for i in OrderStatus.CHOICES:
            available.append(i[0])
        return available

    def set_status(self, new_status):
        if new_status in self.all_statuses():
            self.status = new_status
            self.save()
            return True
        else:
            return False

    def available_for_edit(self):
        if self.status in [OrderStatus.DRAFT, OrderStatus.CONFIRMED]:
            return True
        else:
            return False

    def __str__(self):
        return "Order #{} - {} {}".format(self.pk, self.status, self.created_at)

class OrderItemSize(models.Model):
    #item = models.ForeignKey(OrderItem, related_name='size', editable=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        default = Decimal(0.00)
    )

    def __str__(self):
        return "{} ${}".format(self.name, self.price)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=6, decimal_places=2,
        default=Decimal(0.00)
    )
    size = models.ForeignKey(OrderItemSize, on_delete=models.CASCADE)

    @property
    def total(self):
        total = Decimal(0.00)
        total += (self.price + self.size.price) * self.quantity
        return total

    def __str__(self):
        return "{} qty, ${}".format(self.quantity, self.total)