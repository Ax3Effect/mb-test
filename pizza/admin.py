from django.contrib import admin
from pizza.models import *
# Register your models here.

admin.site.register(MenuItem)
admin.site.register(MenuItemSize)
admin.site.register(AnonymousCustomer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemSize)