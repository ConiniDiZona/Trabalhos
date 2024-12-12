import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import SearchBooks from './components/SearchBooks';
import BookDetails from './components/BookDetails';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/search" element={<SearchBooks />} />
        <Route path="/book-details" element={<BookDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
