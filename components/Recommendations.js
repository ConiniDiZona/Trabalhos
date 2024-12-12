import React, { useEffect, useState } from 'react';
import './styles.css';

function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);

  // Fetch recommendations from the backend
  useEffect(() => {
    fetch('/recommendations') // Update this URL to your API endpoint
      .then(response => response.json())
      .then(data => setRecommendations(data))
      .catch(error => console.error('Erro ao buscar recomendações:', error));
  }, []);

  return (
    <div>
      <h2>Recomendações de Livros</h2>
      <ul>
        {recommendations.map((book, index) => (
          <li key={index}>{book}</li>
        ))}
      </ul>
    </div>
  );
}

export default Recommendations;
