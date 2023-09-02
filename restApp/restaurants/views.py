from .models import Restaurants, CustomUser as User
from .serializers import RestaurantSerializer, UserRegistrationSerializer, UserProfileSerializer, \
    ChangePasswordSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate, update_session_auth_hash
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
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("UserName")
        password = request.data.get("Password")

        if not username or not password:
            # print("Missing fields")
            return Response({"error": "Both UserName and Password are required."}, status=400)

        user = authenticate(request, UserName=username, password=password)
        if user:
            # print("User authenticated")
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

        # print("Invalid credentials")
        return Response({"error": "Invalid credentials"}, status=400)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            if not self.request.user.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.request.user.set_password(serializer.validated_data.get('new_password'))
            self.request.user.save()
            update_session_auth_hash(request, self.request.user)  # Important, to update the session with the new password
            return Response({"success": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
