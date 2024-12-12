import React, { useState } from 'react';
import '../styles.css';

function Return() {
  const [userId, setUserId] = useState('');
  const [bookId, setBookId] = useState('');
  const [loading, setLoading] = useState(false);

  const handleReturn = () => {
    if (!userId || !bookId) {
      alert("Por favor, preencha todos os campos.");
      return;
    }
    
    setLoading(true);
    fetch('http://localhost:5000/return', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, book_id: bookId })
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      setLoading(false);
    })
    .catch(error => {
      console.error('Erro ao devolver livro:', error);
      alert('Ocorreu um erro ao devolver o livro.');
      setLoading(false);
    });
  };

  return (
    <div className="container">
      <h2>Devolver Livro</h2>
      <input
        className="form-control"
        type="text"
        placeholder="ID do Usuário"
        value={userId}
        onChange={e => setUserId(e.target.value)}
      />
      <input
        className="form-control"
        type="text"
        placeholder="ID do Livro"
        value={bookId}
        onChange={e => setBookId(e.target.value)}
      />
      <button className="btn btn-success" onClick={handleReturn} disabled={loading}>
        {loading ? 'Processando...' : 'Devolver'}
      </button>
    </div>
  );
}

export default Return;

