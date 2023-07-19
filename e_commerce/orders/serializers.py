from rest_framework import serializers
from .models import Order, OrderItem, OrderDetail

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    order_detail = OrderDetailSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'