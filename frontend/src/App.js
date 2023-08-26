//import logo from './logo.svg';
//import './App.css';
//
//function App() {
//  return (
//    <div className="App">
//      <header className="App-header">
//        <img src={logo} className="App-logo" alt="logo" />
//        <p>
//          Edit <code>src/App.js</code> and save to reload.
//        </p>
//        <a
//          className="App-link"
//          href="https://reactjs.org"
//          target="_blank"
//          rel="noopener noreferrer"
//        >
//          Learn React
//        </a>
//      </header>
//    </div>
//  );
//}
//
//export default App;

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

