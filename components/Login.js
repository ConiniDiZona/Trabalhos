import React, { useState } from 'react';

function Login() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  const handleLogin = async () => {
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, senha }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.token); // Salva o token JWT
        localStorage.setItem('nome', data.nome); // Salva o nome do usuário
        alert('Login realizado com sucesso!');
        window.location.href = '/search'; // Redireciona para a página de pesquisa
      } else {
        const data = await response.json();
        alert(`Erro ao fazer login: ${data.error}`);
      }
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      alert('Erro inesperado. Tente novamente.');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
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
      <button onClick={handleLogin}>Entrar</button>
      <button
        style={{ marginTop: '10px' }}
        onClick={() => window.location.href = '/register'}
      >
        Criar Conta
      </button>
    </div>
  );
}

export default Login;
