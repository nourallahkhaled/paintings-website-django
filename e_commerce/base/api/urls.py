from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import TokenObtainPairView
from .views import RegisterView , UserLoginAPIView,send_otp, verify_otp

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('send-otp/', send_otp.as_view(), name='send-otp'),
    path('verify-otp/', verify_otp.as_view(), name='verify-otp'),
]