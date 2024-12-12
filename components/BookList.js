import React, { useEffect, useState } from 'react';

function BookList() {
  const [books, setBooks] = useState([]);

  useEffect(() => {
    // Fetch the books from the backend API
    fetch('http://localhost:5000/books')
      .then((response) => response.json())
      .then((data) => setBooks(data))
      .catch((error) => console.error('Erro ao buscar livros:', error));
  }, []);

  return (
    <div className="container">
      <h2>Catálogo de Livros</h2>
      <ul className="book-list">
        {books.map((book) => (
          <li key={book.id}>
            <strong>{book.title}</strong> por {book.author}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BookList;
