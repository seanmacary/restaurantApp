from .models import Restaurants
from .serializers import RestaurantSerializer, UserRegistrationSerializer, UserProfileSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import F, Func





class RestaurantList(generics.ListAPIView):
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        # Get user location from request
        user_latitude = float(self.request.query_params.get('latitude', None))
        user_longitude = float(self.request.query_params.get('longitude', None))

        # Fetch and sort restaurants by distance
        restaurants = Restaurants.objects.annotate(
            distance=Func(
                (F('latitude') - user_latitude) * (F('latitude') - user_latitude) +
                (F('longitude') - user_longitude) * (F('longitude') - user_longitude),
                function='SQRT'
            )
        ).order_by('distance')

        return restaurants

class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            # Here, you can return a token or any other response
            return Response({"message": "Login successful!"})
        return Response({"error": "Invalid credentials"}, status=400)

class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'username'

    def get_object(self):
        return self.request.user