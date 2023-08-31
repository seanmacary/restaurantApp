from rest_framework import serializers
from .models import Restaurants
from django.contrib.auth.models import User


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
