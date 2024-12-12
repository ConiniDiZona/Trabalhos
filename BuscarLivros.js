import React, { useState } from 'react';

function SearchBooks() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`/buscar_livros?q=${query}`);
      const data = await response.json();
      setResults(data.items || []);
    } catch (error) {
      console.error('Erro ao buscar livros:', error);
    }
  };

  const handleAddBook = async (book) => {
    const bookData = {
      title: book.volumeInfo.title,
      authors: book.volumeInfo.authors || [],
      publishedDate: book.volumeInfo.publishedDate || '',
      categories: book.volumeInfo.categories || [],
      google_books_id: book.id,
    };

    try {
      const response = await fetch('/adicionar_livro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookData),
      });
      if (response.ok) {
        alert('Livro adicionado com sucesso!');
      } else {
        alert('Erro ao adicionar livro.');
      }
    } catch (error) {
      console.error('Erro ao adicionar livro:', error);
    }
  };

  return (
    <div>
      <h2>Buscar Livros na Google Books API</h2>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Digite o nome do livro"
      />
      <button onClick={handleSearch}>Buscar</button>
      <div>
        {results.map((book) => (
          <div key={book.id}>
            <h3>{book.volumeInfo.title}</h3>
            <p>Autores: {book.volumeInfo.authors?.join(', ') || 'Não informado'}</p>
            <p>Publicado em: {book.volumeInfo.publishedDate || 'Não informado'}</p>
            <button onClick={() => handleAddBook(book)}>Adicionar à Biblioteca</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SearchBooks;
