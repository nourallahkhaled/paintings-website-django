from django.urls import path

from .views import WishListListView, AddToWishListView, RemoveFromWishListView
# from .views import AddToWishListAPIView , GetWishListAPIView


urlpatterns = [
    path('wishlist/', WishListListView.as_view(), name='wishlist-list'),
    path('wishlist/add/', AddToWishListView.as_view(), name='wishlist-create'),
    path('wishlist/remove/<int:pk>/', RemoveFromWishListView.as_view(), name='wishlist-remove'),
    # path('wishlist/<int:user_id>/add/', AddToWishListAPIView.as_view(), name='add-to-wishlist'),
    # path('wishlist/my/', GetWishListAPIView.as_view(), name='get-wishlist')
    # path('wishlist/<int:user_id>/', GetWishListAPIView.as_view(), name='get-wishlist'),
]