// DataPage.js

import React, { useState } from "react";
import { Link } from 'react-router-dom';
import SemicircularGraph from '../components/SemicircularGraph';
import fetchApi from "../components/Fetch";

function DataPage() {
  const [data, setData] = useState({
    labels: [],
    datasets: [
      {
        label: "Radar Detecting Object Ranges nearby",
        data: [],
        backgroundColor: "#57F807",
        borderColor: "rgba(0, 0, 0, 1)",
        borderWidth: 1,
      },
    ],
  });

  const [lastUpdateTimestamp, setLastUpdateTimestamp] = useState("");

  async function initializeArrayWithRandomNumbers  () {
    const backendUrl = 'http://localhost:5000';
    const fetchedActualArray = await fetchApi(backendUrl,"N");
    const randomArray = [];
    for (let i = 0; i < 360; i++) {
        randomArray.push(String(0));
    }
    for (let i = 270; i < 360; i++) {
        randomArray[i] = await fetchedActualArray[i-270];
        // randomArray[i] = Math.random();
    }
    for (let i = 0; i < 90; i++) {
        randomArray[i] = await fetchedActualArray[i+90];
        // randomArray[i] = Math.random();
    }
    console.log(randomArray);
    return randomArray;
  }
  function initializeArrayWithStrings(length) {
    const stringArray = [];
    for (let i = 0; i < 360; i++) {
        stringArray.push(String(0));
    }
    for (let i = 270; i < 360; i++) {
        stringArray[i] = String(i-270);
    }
    for (let i = 0; i < 90; i++) {
        stringArray[i]=String(i+90);
    }
    return stringArray;
  }

  const updateData = () => {
    const currentDateTime = new Date();
    const formattedDateTime = currentDateTime.toLocaleString();
    initializeArrayWithRandomNumbers().then((Final)=>{
    setData({
      labels: initializeArrayWithStrings(360),
      datasets: [
        {
          label: "Radar Detecting Object Ranges nearby",
          data: Final,

          backgroundColor: "rgb(87, 248, 7,0.8)",
          borderColor: "#3A9F08",
          pointBackgroundColor: "rgb(0, 255, 255)",
          pointBorderColor: "#fff",
        },
      ],
    });});

    setLastUpdateTimestamp(formattedDateTime);
  };
  
    const backendUrl = 'http://localhost:5000';

    const [isButtonDisabled, setButtonDisabled] = useState(false);
  
    const sendRequest = (command) => {
      // Disable all buttons
      setButtonDisabled(true);
  
      // Send the request to the backend
      fetchApi(backendUrl, command);
  
      // Enable the buttons after 5 seconds
      setTimeout(() => {
        setButtonDisabled(false);
      }, 2000);
    };

  return (
    <div >
      <div className="dataUpdate">
        <button onClick={updateData}>Update Data</button>
        <p className="timeUpdate">
          <strong>Last Updated:</strong> {lastUpdateTimestamp}
        </p>
      </div>
      <div style={containerStyle}>
        <SemicircularGraph data={data} />
      </div>
      <section style={controllerSectionStyle}>
        <h2>Controller</h2>
        <div style={buttonContainerStyle}>
        <button style={topButtonStyle} onClick={() => sendRequest('F')} disabled={isButtonDisabled}>Forward</button>
        <div style={inlineLeftRight}>
          <button style={leftButtonStyle}  onClick={() => sendRequest('L')} disabled={isButtonDisabled}>Left</button>
          <button style={centerButtonStyle} onClick={() => sendRequest('S')} disabled={isButtonDisabled}>Stop</button>
          <button style={rightButtonStyle} onClick={() => sendRequest('R')} disabled={isButtonDisabled}>Right</button>
          </div>
          <button style={ReverseButtonStyle} onClick={() => sendRequest('B')} disabled={isButtonDisabled}>Reverse</button>
        </div>
      </section>
      <div className="dataUpdate">
      <Link to="/">
        <a href="#plot">
            <button id="Go Back Home">Go Back Home</button>
        </a>
        </Link>
      </div>
    </div>
  );
}
const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '200vh',
    width: '95vw', 
    margin: 'auto',
  };
  
  const controllerSectionStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '50vh',
    width: '95vw',
    margin: 'auto',
  };
  
  const buttonContainerStyle = {
    display: 'flex',
    alignItems: 'center',
    flexDirection : 'column',
    justifyContent: 'center',
    margin: '2px',
  };
  
  const topButtonStyle = {
    marginTop : '15px',
    height: '50px',
    width : '100px'
  };
   
  const inlineLeftRight = {
    margin : '30px',
    display : 'flex',
    flexDirection : 'row',
    justifyContent :'center'
  }
  const leftButtonStyle = {
    justifyContent: 'flex-start',
    height: '50px',
    width : '100px'
  };
  
  const centerButtonStyle = {
    margin :'0px 50px',
    height: '50px',
    width : '100px'
  };
  
  const rightButtonStyle = {
    justifyContent: 'flex-end',
    height: '50px',
    width : '100px'
  };
  
  const ReverseButtonStyle = {
    marginBottom : '20px',
    height: '50px',
    width : '100px'
      
  }
export default DataPage;
