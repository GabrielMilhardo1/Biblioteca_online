from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import date, datetime
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, text, Column, Integer, String, Text, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/biblioteca")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BookModel(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    publication_date = Column(Date, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(
    title="Sistema de Gerenciamento de Livros",
    description="API simples para CRUD de livros usando MySQL",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/", summary="Root endpoint")
async def read_root():
    return {"message": "Sistema de Gerenciamento de Livros API", "version": "2.0.0", "database": "MySQL"}

@app.post("/api/books", response_model=Book, status_code=201, summary="Criar novo livro")
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        db_book = BookModel(
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            publication_date=book.publication_date,
            description=book.description
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError as e:
        db.rollback()
        if "isbn" in str(e).lower() or "duplicate" in str(e).lower():
            raise HTTPException(status_code=400, detail="ISBN já existe")
        raise HTTPException(status_code=400, detail="Erro de integridade dos dados")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

@app.get("/api/books", response_model=List[Book], summary="Listar todos os livros")
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        books = db.query(BookModel).order_by(BookModel.created_at.desc()).offset(skip).limit(limit).all()
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livros: {str(e)}")

@app.get("/api/books/{book_id}", response_model=Book, summary="Obter livro por ID")
async def get_book(book_id: int, db: Session = Depends(get_db)):
    try:
        book = db.query(BookModel).filter(BookModel.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livro: {str(e)}")

@app.put("/api/books/{book_id}", response_model=Book, summary="Atualizar livro")
async def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    try:
        db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
        if db_book is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        
        update_data = book.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
        
        for field, value in update_data.items():
            setattr(db_book, field, value)
        
        db_book.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_book)
        return db_book
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        if "isbn" in str(e).lower() or "duplicate" in str(e).lower():
            raise HTTPException(status_code=400, detail="ISBN já existe")
        raise HTTPException(status_code=400, detail="Erro de integridade dos dados")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar livro: {str(e)}")

@app.delete("/api/books/{book_id}", status_code=204, summary="Excluir livro")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
        if db_book is None:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        
        db.delete(db_book)
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao excluir livro: {str(e)}")

@app.get("/api/books/search/{query}", response_model=List[Book], summary="Buscar livros")
async def search_books(query: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    try:
        search_query = f"%{query}%"
        books = db.query(BookModel).filter(
            (BookModel.title.like(search_query)) |
            (BookModel.author.like(search_query)) |
            (BookModel.description.like(search_query))
        ).order_by(BookModel.created_at.desc()).offset(skip).limit(limit).all()
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livros: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)