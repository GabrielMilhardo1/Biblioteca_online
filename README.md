# 📚 Sistema de Gerenciamento de Livros

Sistema completo para gerenciar biblioteca digital com operações CRUD.

## 🚀 Tecnologias

- **Backend**: FastAPI + SQLite
- **Frontend**: React + TypeScript + Vite
- **Banco**: SQLite (criação automática)

## ⚡ Como Executar

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
▶️ **Roda em**: http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm run dev
```
▶️ **Roda em**: http://localhost:3000

## 📋 Funcionalidades

- ➕ **Criar livros** (título, autor, ISBN, data, descrição)
- 📋 **Listar todos** os livros
- ✏️ **Editar livros** existentes  
- 🗑️ **Excluir** com confirmação
- 🔍 **Buscar** por título, autor ou descrição

## 🗄️ Banco de Dados

- SQLite local auto-configurável
- Arquivo: `backend/books.db` (criado automaticamente)
- Schema: Tabela `books` com validações e índices

## 📊 API Documentation

Acesse: http://localhost:8000/docs (Swagger automático)

## 🛠️ Estrutura do Projeto

```
├── backend/
│   ├── main.py              # API FastAPI completa
│   ├── requirements.txt     # Dependências Python
│   └── books.db            # Banco SQLite (auto-gerado)
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── types/         # Tipos TypeScript
│   │   └── App.tsx        # App principal
│   └── package.json       # Dependências Node.js
└── README.md
```

## 🎯 Exemplos de Uso

### Via Interface Web
1. Acesse http://localhost:3000
2. Use os botões para criar/editar/excluir livros
3. Use a busca para filtrar

### Via API REST
```bash
# Criar livro
curl -X POST "http://localhost:8000/api/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "1984",
    "author": "George Orwell", 
    "isbn": "9780451524935",
    "publication_date": "1949-06-08",
    "description": "Distopia clássica"
  }'

# Listar livros
curl "http://localhost:8000/api/books"

# Buscar livros
curl "http://localhost:8000/api/books/search/orwell"
```