from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date, datetime
from contextlib import asynccontextmanager
import sqlite3
from typing import List, Optional
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield

app = FastAPI(
    title="Sistema de Gerenciamento de Livros",
    description="API simples para CRUD de livros usando SQLite",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "books.db"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Título do livro")
    author: str = Field(..., min_length=1, max_length=255, description="Autor do livro")
    isbn: str = Field(..., min_length=10, max_length=13, description="ISBN do livro")
    publication_date: date = Field(..., description="Data de publicação")
    description: Optional[str] = Field(None, max_length=1000, description="Descrição do livro")

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(None, min_length=10, max_length=13)
    publication_date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=1000)

class Book(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            publication_date DATE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_books_author ON books(author)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn)")
    
    conn.commit()
    conn.close()


@app.get("/", summary="Root endpoint")
async def read_root():
    return {"message": "Sistema de Gerenciamento de Livros API", "version": "1.0.0"}

@app.post("/api/books", response_model=Book, status_code=201, summary="Criar novo livro")
async def create_book(book: BookCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO books (title, author, isbn, publication_date, description)
            VALUES (?, ?, ?, ?, ?)
        """, (book.title, book.author, book.isbn, book.publication_date, book.description))
        
        book_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        
        return Book(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            isbn=row["isbn"],
            publication_date=row["publication_date"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    except sqlite3.IntegrityError as e:
        if "isbn" in str(e).lower():
            raise HTTPException(status_code=400, detail="ISBN já existe")
        raise HTTPException(status_code=400, detail="Erro de integridade dos dados")
    finally:
        conn.close()

@app.get("/api/books", response_model=List[Book], summary="Listar todos os livros")
async def get_books(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books ORDER BY created_at DESC LIMIT ? OFFSET ?", (limit, skip))
    rows = cursor.fetchall()
    conn.close()
    
    return [
        Book(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            isbn=row["isbn"],
            publication_date=row["publication_date"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
        for row in rows
    ]

@app.get("/api/books/{book_id}", response_model=Book, summary="Obter livro por ID")
async def get_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    return Book(
        id=row["id"],
        title=row["title"],
        author=row["author"],
        isbn=row["isbn"],
        publication_date=row["publication_date"],
        description=row["description"],
        created_at=row["created_at"],
        updated_at=row["updated_at"]
    )

@app.put("/api/books/{book_id}", response_model=Book, summary="Atualizar livro")
async def update_book(book_id: int, book: BookUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    existing_book = cursor.fetchone()
    
    if existing_book is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    update_data = book.dict(exclude_unset=True)
    if not update_data:
        conn.close()
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    
    set_clause = ", ".join([f"{key} = ?" for key in update_data.keys()])
    set_clause += ", updated_at = CURRENT_TIMESTAMP"
    
    try:
        cursor.execute(
            f"UPDATE books SET {set_clause} WHERE id = ?",
            list(update_data.values()) + [book_id]
        )
        conn.commit()
        
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        
        return Book(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            isbn=row["isbn"],
            publication_date=row["publication_date"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
    
    except sqlite3.IntegrityError as e:
        if "isbn" in str(e).lower():
            raise HTTPException(status_code=400, detail="ISBN já existe")
        raise HTTPException(status_code=400, detail="Erro de integridade dos dados")
    finally:
        conn.close()

@app.delete("/api/books/{book_id}", status_code=204, summary="Excluir livro")
async def delete_book(book_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    existing_book = cursor.fetchone()
    
    if existing_book is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

@app.get("/api/books/search/{query}", response_model=List[Book], summary="Buscar livros")
async def search_books(query: str, skip: int = 0, limit: int = 50):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    search_query = f"%{query}%"
    cursor.execute("""
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ? OR description LIKE ?
        ORDER BY 
            CASE 
                WHEN title LIKE ? THEN 1 
                WHEN author LIKE ? THEN 2 
                ELSE 3 
            END, created_at DESC
        LIMIT ? OFFSET ?
    """, (search_query, search_query, search_query, search_query, search_query, limit, skip))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        Book(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            isbn=row["isbn"],
            publication_date=row["publication_date"],
            description=row["description"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
        for row in rows
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)