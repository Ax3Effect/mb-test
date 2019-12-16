from rest_framework import serializers
from pizza.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404

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
        fields = ('id', 'name', 'description', 'price', 'available', 'size')

class AnonCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymousCustomer
        fields = '__all__'



class OrderItemSerializer(serializers.ModelSerializer):
    item = MenuLightItemSerializer()
    size = serializers.ReadOnlyField(source='size.name')
    
    class Meta:
        model = OrderItem
        fields = ('item', 'quantity', 'price', 'size', 'total')

class OrderReadSerializer(serializers.ModelSerializer):
    customer = AnonCustomerSerializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'items', 'created_at', 'updated_at')

class OrderPizzaWriteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    size = serializers.SlugField()
    '''
    class Meta:
        model = OrderItem
        fields = '__all__'
    '''
    def create(self, validated_data):
        pizza_id = validated_data.pop('id')
        pizza_size_slug = validated_data.pop('size')
        try:
            pizza = MenuItem.objects.get(id=pizza_id)
            pizza_size = MenuItemSize.objects.get(slug=pizza_size_slug)
        except ObjectDoesNotExist:
            raise Http404('Pizza or pizza size does not exist')
        order = self.context.get("order")

        order_size = OrderItemSize.objects.create(name=pizza_size.name, price=pizza_size.price)
        order.save()
        order_item = OrderItem.objects.create(order=order, item=pizza, quantity=validated_data.pop('quantity'), size=order_size)
        return order_item


class OrderWriteSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField(required=False)
    order_id = serializers.IntegerField(required=False)
    items = OrderPizzaWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = ('customer_id', 'order_id', 'items')

    def validate_items(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("No items in the order")
        return value

    def create(self, validated_data):
        order_items = validated_data.pop('items')
        if validated_data.get("order_id", None):
            order = get_object_or_404(Order, pk=validated_data.pop("order_id"))
            for i in order.items.all():
                i.delete()
        else:
            if validated_data.get("customer_id", None):
                customer = get_object_or_404(AnonymousCustomer, pk=validated_data.pop('customer_id'))
                order = Order(customer=customer)
            else:
                raise serializers.ValidationError("customer_id not included")
        
        for item_data in order_items:
            item_serializer = OrderPizzaWriteSerializer(data=item_data, context={"order": order})
            if item_serializer.is_valid():
                item_serializer.save()
            else:
                raise serializers.ValidationError(item_serializer.errors)

        return order
    
    def update(self, instance, validated_data):
        if instance.available_for_edit() == False:
            raise serializers.ValidationError("Order is already past prep, items can't be edited")


        order_items = validated_data.pop('items')
        for i in instance.items.all():
            i.delete()

        for item_data in order_items:
            item_serializer = OrderPizzaWriteSerializer(data=item_data, context={"order": instance})
            if item_serializer.is_valid():
                item_serializer.save()
            else:
                raise serializers.ValidationError(item_serializer.errors)
    
        return instance
