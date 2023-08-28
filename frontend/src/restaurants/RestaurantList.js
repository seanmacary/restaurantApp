import React, { useState, useEffect } from 'react';
import './RestaurantList.css';


const DEFAULT_LATITUDE = "40.76678";
const DEFAULT_LONGITUDE = "-73.96757";

const RestaurantList = () => {
  // Setting initial state
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [latitude, setLatitude] = useState(DEFAULT_LATITUDE);
  const [longitude, setLongitude] = useState(DEFAULT_LONGITUDE);

  useEffect(() => {
        // Fetch restaurants for default values
        fetchRestaurants();
    // eslint-disable-next-line
    }, []);


  const fetchRestaurants = () => {
    if (latitude && longitude) {
    // API call
    fetch(`http://127.0.0.1:8000/api/?latitude=${latitude}&longitude=${longitude}`) // Adjust the URL and params as needed
      .then(response => {if (!response.ok) {throw new Error("Network response was not ok");}return response.json();})
      .then(data => {setRestaurants(data.results);setLoading(false);})
      .catch(err => {setError(err);setLoading(false);});
    } else {
        alert("Please provide both latitude and longitude.")
    }
}

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="container">
            {/* Input for Latitude */}
            <input
                type="text"
                placeholder="Enter Latitude"
                value={latitude}
                onChange={e => setLatitude(e.target.value)}
            />

            {/* Input for Longitude */}
            <input
                type="text"
                placeholder="Enter Longitude"
                value={longitude}
                onChange={e => setLongitude(e.target.value)}
            />

            {/* Button to initiate the API call */}
            <button onClick={fetchRestaurants} className="SearchButton">Search</button>

            {/* Display the list of restaurants */}
            <ul>
                {restaurants.map(restaurant => (
                    <li key={restaurant.id}>
                      <h2>{restaurant.name}</h2>
                        <p>Latitude: {restaurant.latitude}</p>
                        <p>Longitude: {restaurant.longitude}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default RestaurantList;
