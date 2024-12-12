import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function BookDetails() {
  const location = useLocation();
  const navigate = useNavigate();
  const { book } = location.state || {};

  console.log('Dados do livro:', book);

  if (!location.state || !book) {
    alert('Nenhum livro foi selecionado.');
    navigate('/');
    return null;
  }

  return (
    <div>
      <h2>Detalhes do Livro</h2>
      <h3>{book.volumeInfo?.title || 'Título não disponível'}</h3>
      <p><strong>Autores:</strong> {book.volumeInfo?.authors?.join(', ') || 'Desconhecido'}</p>
      <p><strong>Descrição:</strong> {book.volumeInfo?.description || 'Não disponível'}</p>
      {book.volumeInfo?.imageLinks?.thumbnail ? (
        <img
          src={book.volumeInfo.imageLinks.thumbnail}
          alt={book.volumeInfo.title}
          style={{ width: '200px' }}
        />
      ) : (
        <p>Imagem não disponível</p>
      )}
      <button
        style={{
          padding: '10px 20px',
          backgroundColor: '#28a745',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '20px',
        }}
        onClick={async () => {
          const token = localStorage.getItem('token'); // Recupera o token armazenado no localStorage
          
          if (!token) {
            alert('Usuário não autenticado. Faça login para continuar.');
            return;
          }
      
          try {
            const response = await fetch('http://localhost:5000/emprestimos', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`, // Passa o token no cabeçalho Authorization
              },
              body: JSON.stringify({
                book_id: book.id, // Passa o ID do livro selecionado
              }),
            });
      
            if (response.ok) {
              alert('Empréstimo realizado com sucesso!');
            } else {
              const data = await response.json();
              alert(`Erro ao realizar empréstimo: ${data.error}`);
            }
          } catch (error) {
            console.error('Erro ao realizar empréstimo:', error);
            alert('Ocorreu um erro ao realizar o empréstimo. Tente novamente.');
          }
        }}
      >
        Fazer Empréstimo
      </button>
      <button
        style={{
          padding: '10px 20px',
          backgroundColor: '#6c757d',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer',
          marginTop: '20px',
          marginLeft: '10px',
        }}
        onClick={() => navigate('/')}
      >
        Voltar
      </button>
    </div>
  );
}

export default BookDetails;
