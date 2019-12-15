from rest_framework import serializers
from pizza.models import *

class MenuItemSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemSize
        fields = ('id', 'name', 'price')

class MenuLightItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'description', 'price', 'available')

class MenuItemSerializer(MenuLightItemSerializer):
    size = MenuItemSizeSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = ('size',)

class AnonCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousCustomer
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    item = MenuLightItemSerializer()
    
    class Meta:
        model = OrderItem
        fields = ('item', 'name', 'quantity', 'price', 'size', 'total')

class OrderSerializer(serializers.ModelSerializer):
    customer = AnonCustomerSerializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('customer', 'status', 'items', 'created_at', 'updated_at')