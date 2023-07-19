from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductItemSerializer

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'total_price')

    @property
    def total_price(self):
        return self.product.price * self.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'date_added')