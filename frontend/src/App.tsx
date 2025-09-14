import React, { useState, useEffect } from 'react';
import { Book, BookFormData } from './types/book';
import BookList from './components/BookList';
import BookForm from './components/BookForm';

const API_BASE_URL = 'http://localhost:8000/api';

function App() {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [showForm, setShowForm] = useState(false);
  const [editingBook, setEditingBook] = useState<Book | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchBooks = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/books`);
      if (!response.ok) throw new Error('Erro ao carregar livros');
      const data = await response.json();
      setBooks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const searchBooks = async (query: string) => {
    if (!query.trim()) {
      fetchBooks();
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/books/search/${encodeURIComponent(query)}`);
      if (!response.ok) throw new Error('Erro ao buscar livros');
      const data = await response.json();
      setBooks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBook = async (bookData: BookFormData) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/books`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao criar livro');
      }

      await fetchBooks();
      setShowForm(false);
      setEditingBook(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateBook = async (bookData: BookFormData) => {
    if (!editingBook) return;

    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/books/${editingBook.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookData),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao atualizar livro');
      }

      await fetchBooks();
      setShowForm(false);
      setEditingBook(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteBook = async (id: number) => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/books/${id}`, {
        method: 'DELETE',
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erro ao excluir livro');
      }

      await fetchBooks();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (book: Book) => {
    setEditingBook(book);
    setShowForm(true);
  };

  const handleCancelForm = () => {
    setShowForm(false);
    setEditingBook(null);
  };

  const handleSubmitForm = (bookData: BookFormData) => {
    if (editingBook) {
      handleUpdateBook(bookData);
    } else {
      handleCreateBook(bookData);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    searchBooks(searchQuery);
  };

  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px' }}>
      <header style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h1 style={{ color: '#333', marginBottom: '0.5rem' }}>
          📚 Sistema de Gerenciamento de Livros
        </h1>
        <p style={{ color: '#666', fontSize: '1.1rem' }}>
          Gerencie sua biblioteca digital de forma simples e eficiente
        </p>
      </header>

      {error && (
        <div
          style={{
            background: '#f8d7da',
            color: '#721c24',
            padding: '12px',
            borderRadius: '4px',
            marginBottom: '1rem',
            border: '1px solid #f5c6cb',
          }}
        >
          <strong>Erro:</strong> {error}
          <button
            onClick={() => setError('')}
            style={{
              float: 'right',
              background: 'none',
              border: 'none',
              fontSize: '18px',
              cursor: 'pointer',
              color: '#721c24',
            }}
          >
            ×
          </button>
        </div>
      )}

      {!showForm && (
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
            <button
              onClick={() => setShowForm(true)}
              style={{
                padding: '12px 24px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '16px',
              }}
            >
              ➕ Novo Livro
            </button>
            <button
              onClick={fetchBooks}
              disabled={loading}
              style={{
                padding: '12px 24px',
                backgroundColor: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '16px',
              }}
            >
              🔄 Atualizar Lista
            </button>
          </div>

          <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '12px', marginBottom: '1rem' }}>
            <input
              type="text"
              placeholder="Buscar por título, autor ou descrição..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{
                flex: 1,
                padding: '12px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '16px',
              }}
            />
            <button
              type="submit"
              style={{
                padding: '12px 24px',
                backgroundColor: '#17a2b8',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '16px',
              }}
            >
              🔍 Buscar
            </button>
            {searchQuery && (
              <button
                type="button"
                onClick={() => {
                  setSearchQuery('');
                  fetchBooks();
                }}
                style={{
                  padding: '12px 24px',
                  backgroundColor: '#6c757d',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '16px',
                }}
              >
                Limpar
              </button>
            )}
          </form>
        </div>
      )}

      {showForm ? (
        <BookForm
          book={editingBook}
          onSubmit={handleSubmitForm}
          onCancel={handleCancelForm}
          loading={loading}
        />
      ) : (
        <BookList
          books={books}
          onEdit={handleEdit}
          onDelete={handleDeleteBook}
          loading={loading}
        />
      )}
    </div>
  );
}

export default App;