// HomePage.js

import React from 'react';
import { Link } from 'react-router-dom';

const HomePage=() =>{
  return (
    <div className="homePage">
      <div className="main-area">
        <h1 style={{ backgroundColor: 'rgba(0, 0, 0, 0)' }}>Gesture Drive</h1>
        <p className="info">
            This is bot that works on the gesture provided by hand based on
            which the bot takes turn and it also detects the obstacle and change
            their route and this thing is performed using machine learning and
            the points are plotted on the website showing how the bot is moving.
        </p>
        <Link to="/data">
        <a href="#plot">
          <button id="goTo">Go!</button>
        </a>
        </Link>
      </div>
    </div>
  );
}

export default HomePage;
