from rest_framework.serializers import ModelSerializer
from base.models import  User
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password' , 'mobile' )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile=validated_data['mobile'],
        )
        user.set_password(validated_data['password']) 
        user.save()

        return user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, User):
        token = super().get_token(User)
        token['email'] = User.email
        print(User)

        return token