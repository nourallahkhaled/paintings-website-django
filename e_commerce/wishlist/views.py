from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# ------------------ Django Task ------------------
from .models import WishList
from base.models import User
from products.models import ProductItem
from .serializers import WishListSerializer


class WishListListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_data = WishList.objects.filter(user=request.user)
        serializer = WishListSerializer(wishlist_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# To Insert Item into Cart Write this in the Content box in Add to wishlist page
# {
# "product_id":1
# }  
class AddToWishListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = ProductItem.objects.get(id=product_id)
        except ProductItem.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item, created = WishList.objects.get_or_create(user=request.user, product=product)

        if not created:
            return Response({'error': 'Product already in wishlist.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = WishListSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_200_OK)   

# send id of wishlist in url 
class RemoveFromWishListView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            wishlist_item = WishList.objects.get(pk=pk, user=request.user)
        except WishList.DoesNotExist:
            return Response({'error': 'Wishlist item not found.'}, status=status.HTTP_404_NOT_FOUND)

        wishlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
         
# class AddToWishListAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id):
#         try:
#             user = get_object_or_404(User, id=user_id)
#             product_id = request.data.get('product')
#             if not product_id:
#                 return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
#             product = get_object_or_404(ProductItem, id=product_id)
#             wishlist_item, created = WishList.objects.get_or_create(user=user, product=product)
#             if not created:
#                 return Response({'error': f'{product} is already in your wishlist.'}, status=status.HTTP_400_BAD_REQUEST)
#             wishlist_item.save()
#             data = {'success': f'{product} has been added to your wishlist.'}
#             return Response(data=data, status=status.HTTP_201_CREATED)

#         except User.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
#         except ProductItem.DoesNotExist:
#             return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(f'exception in add_to_wishlist_api => {e}')
#             data = {'error': 'Error occurred while adding item to wishlist.'}
#             return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class GetWishListAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             wishlist_items = WishList.objects.filter(user=request.user)
#             serializer = WishListSerializer(wishlist_items, many=True)
#             data = serializer.data
#             return Response(data=data, status=status.HTTP_200_OK)

#         except Exception as e:
#             print(f'exception in get_wishlist_api => {e}')
#             data = {'error': 'Error occurred while retrieving wishlist items.'}
#             return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class GetWishListAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, user_id):
#         try:
#             user = get_object_or_404(User, id=user_id)
#             wishlist_items = WishList.objects.filter(user=user)
#             serializer = WishListSerializer(wishlist_items, many=True)
#             data = serializer.data
#             return Response(data=data, status=status.HTTP_200_OK)

#         except User.DoesNotExist:
#             return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             print(f'exception in get_wishlist_api => {e}')
#             data = {'error': 'Error occurred while retrieving wishlist items.'}
#             return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        