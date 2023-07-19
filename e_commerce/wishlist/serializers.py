from rest_framework import serializers
from .models import WishList
from base.api.serializers import UserSerializer
from products.serializers import ProductItemSerializer

class WishListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductItemSerializer(read_only=True)
    class Meta:
        model = WishList
        fields = ("id", "user", "product")
        
# class WishlistSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ('id', 'user', 'product')
#         model = Wishlist