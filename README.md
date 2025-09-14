# 📚 Sistema de Gerenciamento de Livros

Sistema completo para gerenciar biblioteca digital com operações CRUD.

## 🚀 Tecnologias

- **Backend**: FastAPI + SQLAlchemy
- **Frontend**: React + TypeScript + Vite
- **Banco**: MySQL 8.0+ com fallback automático para SQLite
- **ORM**: SQLAlchemy 2.0

## 🗄️ Configuração do Banco de Dados

### 🔄 Sistema Inteligente de Fallback
O sistema tenta conectar ao **MySQL primeiro**. Se não conseguir, **automaticamente** usa **SQLite** como fallback.

### Opção 1: MySQL (Recomendado para produção)
```sql
-- Instalar MySQL Server 8.0+
-- Conectar ao MySQL
mysql -u root -p

-- Criar banco de dados
CREATE DATABASE biblioteca CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Criar usuário (opcional)
CREATE USER 'biblioteca_user'@'localhost' IDENTIFIED BY 'sua_senha_segura';
GRANT ALL PRIVILEGES ON biblioteca.* TO 'biblioteca_user'@'localhost';
FLUSH PRIVILEGES;
```

### Opção 2: SQLite (Automático se MySQL não disponível)
- ✅ **Zero configuração** - funciona imediatamente
- ✅ **Arquivo local** - `books.db` criado automaticamente
- ✅ **Perfeito para desenvolvimento** e testes

## ⚡ Como Executar

### Método 1: Início Rápido (SQLite)
```bash
# Backend - roda automaticamente com SQLite
cd backend
pip install -r requirements.txt
python main.py
# ✅ Funcionando em segundos!
```

### Método 2: Com MySQL (Configuração adicional)
```bash
# 1. Configurar variáveis de ambiente
cd backend
cp .env.example .env
# Editar .env com suas credenciais MySQL

# 2. Iniciar backend
pip install -r requirements.txt
python main.py
```

### Frontend (Para ambos os métodos)
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

## 🗄️ Sistema de Banco Inteligente

### 🤖 Detecção Automática:
- ✅ **MySQL disponível**: Usa MySQL (produção)
- ✅ **MySQL indisponível**: Fallback automático para SQLite
- ✅ **Logs informativos**: Mostra qual banco está sendo usado

### 📊 Características:
- **SQLAlchemy ORM 2.0** profissional
- **Criação automática** de tabelas
- **Transações seguras** com rollback
- **Schema consistente** entre MySQL e SQLite

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