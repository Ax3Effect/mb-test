from django.contrib import admin
from pizza.models import *
# Register your models here.

admin.site.register(MenuItem)
admin.site.register(MenuItemSize)
admin.site.register(AnonymousCustomer)

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemAdmin, )

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderItemSize)