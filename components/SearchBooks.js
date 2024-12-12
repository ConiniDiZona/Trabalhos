import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function SearchBooks() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const navigate = useNavigate();

  const handleSearch = async () => {
    if (!query.trim()) {
      alert('Por favor, insira um termo de pesquisa!');
      return;
    }

    try {
      const response = await fetch(`http://localhost:5000/buscar_livros?q=${query}`);
      const data = await response.json();
      if (data.items) {
        setResults(data.items);
      } else {
        setResults([]);
        alert('Nenhum livro encontrado.');
      }
    } catch (error) {
      console.error('Erro ao buscar livros:', error);
      alert('Ocorreu um erro ao buscar livros. Tente novamente.');
    }
  };

  const handleViewDetails = (book) => {
    navigate(`/book-details`, { state: { book } });
  };

  return (
    <div className="search-container">
      <h2>Buscar Livros na Google Books API</h2>
      <input
        type="text"
        placeholder="Digite o nome do livro"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Buscar</button>
      <div className="results">
        {results.length > 0 ? (
          results.map((book) => (
            <div
              key={book.id}
              className="book-item"
              onClick={() => handleViewDetails(book)}
              style={{ cursor: 'pointer', margin: '20px', textAlign: 'center' }}
            >
              {book.volumeInfo.imageLinks?.thumbnail && (
                <img
                  src={book.volumeInfo.imageLinks.thumbnail}
                  alt={book.volumeInfo.title}
                  style={{ width: '100px', height: '150px' }}
                />
              )}
              <h3>{book.volumeInfo.title}</h3>
            </div>
          ))
        ) : (
          <p>Nenhum resultado para exibir.</p>
        )}
      </div>
    </div>
  );
}

export default SearchBooks;
