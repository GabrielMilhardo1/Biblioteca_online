# 📚 Sistema de Gerenciamento de Livros

Sistema completo para gerenciar biblioteca digital com operações CRUD.

## 🚀 Tecnologias

- **Backend**: FastAPI + SQLAlchemy + MySQL
- **Frontend**: React + TypeScript + Vite
- **Banco**: MySQL 8.0+ (criação automática de tabelas)
- **ORM**: SQLAlchemy 2.0

## 🗄️ Configuração do Banco MySQL

### Pré-requisitos
- MySQL Server 8.0+ instalado
- Acesso administrativo ao MySQL

### Setup do Banco
```sql
-- Conectar ao MySQL
mysql -u root -p

-- Criar banco de dados
CREATE DATABASE biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criar usuário (opcional)
CREATE USER 'biblioteca_user'@'localhost' IDENTIFIED BY 'sua_senha_segura';
GRANT ALL PRIVILEGES ON biblioteca.* TO 'biblioteca_user'@'localhost';
FLUSH PRIVILEGES;
```

## ⚡ Como Executar

### 1. Configurar Variáveis de Ambiente
```bash
cd backend
cp .env.example .env
# Editar .env com suas credenciais MySQL
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
▶️ **Roda em**: http://localhost:8000

### 3. Frontend
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

## 🗄️ Banco de Dados - MySQL

- MySQL 8.0+ com SQLAlchemy ORM
- Tabelas criadas automaticamente na inicialização
- Schema: Tabela `books` com constraints e relacionamentos
- Suporte a transações e rollback automático

## 📊 API Documentation

Acesse: http://localhost:8000/docs (Swagger automático)

## 🛠️ Estrutura do Projeto

```
├── backend/
│   ├── main.py              # API FastAPI + SQLAlchemy
│   ├── requirements.txt     # Dependências Python + MySQL
│   ├── .env.example         # Exemplo de configuração
│   └── .env                # Configurações MySQL (criar)
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