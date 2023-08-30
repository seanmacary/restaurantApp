from rest_framework import generics
from django.db.models import F, Func
from .models import Restaurants
from .serializers import RestaurantSerializer


class RestaurantList(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    print(serializer_class.data)

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
