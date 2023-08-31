import requests
from restaurants.models import Restaurants

# Initialize counters for API requests and total inserted rows
total_api_requests = 0
total_inserted_rows = 0

# Define the latitude and longitude boundaries for Manhattan
min_latitude = 40.7
max_latitude = 40.88
min_longitude = -74.02
max_longitude = -73.92

# Specify the step size for the latitude and longitude grid
latitude_step = 0.02
longitude_step = 0.02

url = "https://api.yelp.com/v3/businesses/search"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer RkmpdJs9bQPiHydwmeXhPsyCiSdGLJbV96PmCHABstSCUj5vq4BRNEZRBU2c" \
                     "6djAEnLh9puYZWUGmLqhOzUSYfLj_Fggh6oUOYuGuvXWWsN4-uxjt-tx0beBM0DpZHYx"
}

# Loop through the latitude and longitude grid
for lat in range(int(min_latitude * 100), int(max_latitude * 100), int(latitude_step * 100)):
    for lon in range(int(min_longitude * 100), int(max_longitude * 100), int(longitude_step * 100)):
        latitude = lat / 100.0
        longitude = lon / 100.0
        total_api_requests += 1

        # Define parameters for the API request
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "limit": 50,  # Number of results per request
            "sort_by": "best_match"
        }

        # Make the API request
        response = requests.get(url, params=params, headers=headers)

        if response.ok:

            data = response.json()
            for restaurant in data['businesses']:
                print(restaurant)
                name = restaurant.get('name')
                total_review_count = restaurant.get('review_count')
                categories = restaurant.get('categories', [])
                cuisine_type = ', '.join(category['title'] for category in categories)
                latitude = restaurant.get('coordinates').get('latitude')
                longitude = restaurant.get('coordinates').get('longitude')
                address = ', '.join(restaurant.get('location', {}).get('display_address', []))

                restaurant_instance, created = Restaurants.objects.get_or_create(
                    name=name,
                    defaults={
                        'TotalReview': total_review_count,
                        'Cuisinetype': cuisine_type,
                        'Latitude': latitude,
                        'Longitude': longitude,
                        'Address': address
                    }
                )

                if not created:
                    # Update the instance if it already exists
                    restaurant_instance.TotalReview = total_review_count
                    restaurant_instance.Cuisinetype = cuisine_type
                    restaurant_instance.Latitude = latitude
                    restaurant_instance.Longitude = longitude
                    restaurant_instance.Address = address
                    restaurant_instance.save()

        else:
            print(f"Failed to fetch data for lat={latitude}, lon={longitude}. Status code: {response.status_code}")

print(f"Total API requests made: {total_api_requests}")