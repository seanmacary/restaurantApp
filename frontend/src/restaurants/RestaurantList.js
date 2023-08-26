import React, { useState, useEffect } from 'react';

function RestaurantList() {
  // Setting initial state
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // API call
    fetch("http://127.0.0.1:8000/api/?latitude=40.76678&longitude=-73.96757") // Adjust the URL and params as needed
      .then(response => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then(data => {
        setRestaurants(data.results);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, []);  // The empty dependency array means this useEffect runs once when the component mounts, similar to componentDidMount.

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h2>List of Restaurants</h2>
      <ul>
        {restaurants.map(restaurant => (
    <div key={restaurant.id}>
        <h2>{restaurant.name}</h2>
        <p>Latitude: {restaurant.latitude}</p>
        <p>Longitude: {restaurant.longitude}</p>
    </div>
        ))}

      </ul>
    </div>
  );
}

export default RestaurantList;
