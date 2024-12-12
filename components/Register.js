import React, { useState } from 'react';

function Register() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const handleRegister = async () => {
    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome, email, senha }),
      });

      if (response.ok) {
        alert('Conta criada com sucesso!');
        window.location.href = '/'; // Redireciona para a tela de login
      } else {
        const data = await response.json();
        alert(`Erro ao criar conta: ${data.error}`);
      }
    } catch (error) {
      console.error('Erro ao criar conta:', error);
      alert('Erro inesperado. Tente novamente.');
    }
  };

  return (
    <div className="register-container">
      <h2>Criar Conta</h2>
      <input
        type="text"
        placeholder="Nome"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Senha"
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
      />
      <button onClick={handleRegister}>Registrar</button>
      <button
        style={{ marginTop: '10px' }}
        onClick={() => (window.location.href = '/')}
      >
        Voltar para Login
      </button>
    </div>
  );
}

export default Register;
