from .models import Restaurants, CustomUser as User
from .serializers import RestaurantSerializer, UserRegistrationSerializer, UserProfileSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db.models import F, Func
from django.db.utils import IntegrityError


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
    authentication_classes = ()  # Override the default authentication
    permission_classes = ()
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            return super(UserRegistrationView, self).create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("UserName")
        password = request.data.get("Password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'UserName'

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
