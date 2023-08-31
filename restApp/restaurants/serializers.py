from rest_framework import serializers
from .models import Restaurants, CustomUser


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['UserName', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['UserName', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']

