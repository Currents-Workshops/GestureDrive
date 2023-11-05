const fetchApi = async (backendUrl,command) => {
    console.log(command);
    try {
      const requestData = {
        command: command 
      };
  
      const response = await fetch(backendUrl + '/gestureDrive', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      });
  
      if (!response.ok) {
        throw new Error('Network error');
      }
  
      const data = await response.json();
  
     
      if (data && data.data) {
        console.log('Received data:', data.data);
        
        return data.data;
      }
    } catch (error) {
      
      console.error('Error: ', error);
      
      throw error;
    }
  };
  
  export default fetchApi;