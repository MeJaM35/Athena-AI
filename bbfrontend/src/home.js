import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Home() {
  const [msg, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/')
      .then(response => {
        setMessage(response.data.msg);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div>
      <h1>Hello, World!</h1>
      <p>{msg}</p>
    </div>
  );
}

export default Home;