from django.urls import path
from cart import views 

urlpatterns = [
    path("cart/", views.get_cart, name="cart"),
    path("add_to_cart/", views.add_to_cart, name= "add"),
    path('item/<int:item_id>/', views.update_cart_item , name='update-cart-item'),
]