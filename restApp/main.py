import requests
import sqlite3

conn = sqlite3.connect('./databases/data.sqlite3django ')
cursor = conn.cursor()

# Define the table structure
cursor.execute('''
CREATE TABLE IF NOT EXISTS Restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT,
    latitude REAL,
    longitude REAL
)
''')

url = "https://api.yelp.com/v3/businesses/search?location=New%20York%2C%20New%20York&sort_by=best_match&limit=50"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer RkmpdJs9bQPiHydwmeXhPsyCiSdGLJbV96PmCHABstSCUj5vq4BRNEZRBU2c" \
                     "6djAEnLh9puYZWUGmLqhOzUSYfLj_Fggh6oUOYuGuvXWWsN4-uxjt-tx0beBM0DpZHYx"
}

response = requests.get(url, headers=headers)

if response.ok:
    data = response.json()

    for restaurant in data['businesses']:
        name = restaurant.get('name')
        latitude = restaurant.get('coordinates').get('latitude')
        longitude = restaurant.get('coordinates').get('longitude')

        cursor.execute('''
                    INSERT INTO restaurants (name, latitude, longitude) VALUES (?, ?, ?)
                ''', (name, latitude, longitude))

        # Commit after inserting each restaurant (or commit once after the loop ends to do it in one transaction)
        conn.commit()
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

conn.close()
