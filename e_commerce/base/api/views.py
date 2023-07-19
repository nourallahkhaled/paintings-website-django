# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.decorators import api_view , permission_classes
# from rest_framework.permissions import IsAuthenticated

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView


# from base.models import  User

# from rest_framework.permissions import AllowAny
# from django.contrib.auth.models import User
# from .serializers import *
# from rest_framework import generics
# from rest_framework.views import APIView
# # from .serializers import UserRegisterSerializer
# from rest_framework import permissions, status

# from django.contrib.auth import get_user_model
# from .serializers import UserSerializer, CustomTokenObtainPairSerializer 
# from rest_framework.exceptions import PermissionDenied, AuthenticationFailed

# from rest_framework import generics, permissions, status

# User = get_user_model()

# class UserLoginAPIView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.user
#         # Raise an exception if the user is blocked

#         token = serializer.validated_data
#         return Response(token, status=status.HTTP_200_OK)

# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from base.models import  User

from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
# from .serializers import UserRegisterSerializer
from rest_framework import permissions, status

from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CustomTokenObtainPairSerializer 
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed

from rest_framework import generics, permissions, status

User = get_user_model()

class UserLoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.user

        token = serializer.validated_data
        return Response(token, status=status.HTTP_200_OK)



from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from random import randint
om_el_otp = 0
class send_otp(APIView):
    def post(self, request):
        global om_el_otp
        email = request.data.get('email')
        otp = str(randint(100000, 999999))
        email_subject = "Verification OTP for your account"
        email_body = f'Your verification OTP is: {otp}'
        om_el_otp = otp

        try:
            send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            data = {'message': 'OTP sent successfully.'}
            http_status = status.HTTP_200_OK

            session = SessionStore()
            session['otp'] = otp
            session.save()

        except Exception as e:
            print(f'exception in send_otp => {e}')
            data = {'error': 'An error occurred while sending the OTP.'}
            http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
           

        return Response(data=data, status=http_status)
from django.contrib.sessions.backends.db import SessionStore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class verify_otp(APIView):
    global om_el_otp
    def post(self, request):
        received_otp = request.data.get('otp')
        
        session = SessionStore(request.data.get('session_key'))
      
        session.delete()

        if received_otp == om_el_otp:
            data = {'message': 'OTP verified successfully.'}
            http_status = status.HTTP_200_OK
            
        else:
            data = {'error': 'Invalid OTP.'}
            print('maryam')
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(data=data, status=http_status)
from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]