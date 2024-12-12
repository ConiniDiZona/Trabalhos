import React, { useState } from 'react';
import './styles.css';

function Borrow() {
  const [userId, setUserId] = useState('');
  const [bookId, setBookId] = useState('');

  const handleBorrow = () => {
    fetch('/borrow', { // Update this URL to your API endpoint
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, book_id: bookId })
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Erro ao realizar empréstimo:', error));
  };

  return (
    <div>
      <h2>Realizar Empréstimo</h2>
      <input
        type="text"
        placeholder="ID do Usuário"
        value={userId}
        onChange={e => setUserId(e.target.value)}
      />
      <input
        type="text"
        placeholder="ID do Livro"
        value={bookId}
        onChange={e => setBookId(e.target.value)}
      />
      <button onClick={handleBorrow}>Empréstimo</button>
    </div>
  );
}

export default Borrow;
