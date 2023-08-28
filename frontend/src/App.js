import React from 'react';
import './App.css';
import RestaurantList from './restaurants/RestaurantList';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>My Restaurants App</h1>
      </header>
      <main>
        <RestaurantList />
      </main>
    </div>
  );
}

export default App;

