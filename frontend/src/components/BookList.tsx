import React from 'react';
import { Book } from '../types/book';

interface BookListProps {
  books: Book[];
  onEdit: (book: Book) => void;
  onDelete: (id: number) => void;
  loading: boolean;
}

const BookList: React.FC<BookListProps> = ({ books, onEdit, onDelete, loading }) => {
  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem' }}>
        <p>Carregando livros...</p>
      </div>
    );
  }

  if (books.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '2rem' }}>
        <p>Nenhum livro encontrado.</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Lista de Livros ({books.length})</h2>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5' }}>
              <th style={{ padding: '12px', textAlign: 'left', border: '1px solid #ddd' }}>ID</th>
              <th style={{ padding: '12px', textAlign: 'left', border: '1px solid #ddd' }}>Título</th>
              <th style={{ padding: '12px', textAlign: 'left', border: '1px solid #ddd' }}>Autor</th>
              <th style={{ padding: '12px', textAlign: 'left', border: '1px solid #ddd' }}>ISBN</th>
              <th style={{ padding: '12px', textAlign: 'left', border: '1px solid #ddd' }}>Data</th>
              <th style={{ padding: '12px', textAlign: 'left', border: '1px solid #ddd' }}>Ações</th>
            </tr>
          </thead>
          <tbody>
            {books.map((book) => (
              <tr key={book.id} style={{ borderBottom: '1px solid #ddd' }}>
                <td style={{ padding: '12px', border: '1px solid #ddd' }}>{book.id}</td>
                <td style={{ padding: '12px', border: '1px solid #ddd', fontWeight: 'bold' }}>
                  {book.title}
                </td>
                <td style={{ padding: '12px', border: '1px solid #ddd' }}>{book.author}</td>
                <td style={{ padding: '12px', border: '1px solid #ddd' }}>{book.isbn}</td>
                <td style={{ padding: '12px', border: '1px solid #ddd' }}>
                  {new Date(book.publication_date).toLocaleDateString('pt-BR')}
                </td>
                <td style={{ padding: '12px', border: '1px solid #ddd' }}>
                  <button
                    onClick={() => onEdit(book)}
                    style={{
                      marginRight: '8px',
                      padding: '6px 12px',
                      backgroundColor: '#007bff',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                    }}
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => {
                      if (window.confirm(`Tem certeza que deseja excluir "${book.title}"?`)) {
                        onDelete(book.id);
                      }
                    }}
                    style={{
                      padding: '6px 12px',
                      backgroundColor: '#dc3545',
                      color: 'white',
                      border: 'none',
                      borderRadius: '4px',
                      cursor: 'pointer',
                    }}
                  >
                    Excluir
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default BookList;