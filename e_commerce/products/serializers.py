# from rest_framework import serializers
# from products.models import ProductCategory, ProductItem, Promotion

# class ProductCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductCategory
#         fields = ['name', 'slug', 'category_items']
        
# class ProductItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductItem
#         fields = '__all__'
        
# class PromotionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Promotion
#         fields = ['start_date', 'slug', 'discount_rate', 'end_date', 'promotion_items']
from rest_framework import serializers
from products.models import ProductCategory, ProductItem, Promotion

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name', 'slug', 'category_items']
        
class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = '__all__'
        
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['start_date', 'slug', 'discount_rate', 'end_date', 'promotion_items']