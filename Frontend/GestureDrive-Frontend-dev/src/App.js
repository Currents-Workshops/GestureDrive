import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from "./pages/HomePage";
import DataPage from "./pages/DataPage.js";

const App = () => {
  return (
    <Router>
    <div className="App">
      <Routes>
        <Route path="/" element={<HomePage/>} />
        <Route path="/data" element={<DataPage/>} />
      </Routes>
    </div>
  </Router>
  );
};

export default App;
