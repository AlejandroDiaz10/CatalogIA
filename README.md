# CatalogIA

Sistema de e-commerce potenciado por IA con funcionalidades de búsqueda semántica y recomendaciones personalizadas.

## Estructura del Proyecto
```
CatalogIA/
├── .env                    # Variables de entorno (no subir a git)
├── .gitignore              # Archivos ignorados por git
├── .venv/                  # Entorno virtual de Python
├── README.md               # Este archivo
├── requirements.txt        # Dependencias del proyecto
├── script.py               # Scripts auxiliares
└── users_crud_server/      # API de gestión de usuarios
    ├──__init__.py          # Para importar módulos
    ├── main.py             # Punto de entrada de la aplicación
    ├── models.py           # Modelos SQLAlchemy
    ├── schemas.py          # Esquemas Pydantic
    ├── crud.py             # Operaciones CRUD
    └── database.py         # Configuración de la base de datos
```

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **PostgreSQL**: Base de datos relacional
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

## Requisitos Previos

- Python 3.9+
- PostgreSQL 14+
- Homebrew (para Mac)

---

## Configuración del Proyecto

### 1. Instalar PostgreSQL
```bash
# Instalar PostgreSQL con Homebrew
brew install postgresql@14

# Iniciar el servicio
brew services start postgresql@14

# Verificar instalación
psql postgres
```

### 2. Crear la Base de Datos

Dentro de `psql`, ejecuta los siguientes comandos:
```sql
-- Crear la base de datos
CREATE DATABASE catalogia_db;

-- Conectarse a la base de datos
\c catalogia_db

-- Crear la tabla users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- (Opcional) Insertar datos de prueba
INSERT INTO users (email, password_hash, is_active, is_verified) 
VALUES 
    ('test1@example.com', '$2b$12$dummyhash1', TRUE, TRUE),
    ('test2@example.com', '$2b$12$dummyhash2', TRUE, FALSE);

-- Verificar
SELECT * FROM users;

-- Salir
\q
```

### 3. Configurar el Entorno Virtual
```bash
# Clonar el repositorio
git clone https://github.com/AlejandroDiaz10/CatalogIA

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate  # En Mac/Linux
# .venv\Scripts\activate   # En Windows

# Instalar dependencias
pip install -r requirements.txt

# Generar requirements.txt
pip freeze > requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (`CatalogIA/.env`):
```bash
# Obtener tu usuario de PostgreSQL (generalmente es tu usuario de Mac)
whoami

# Crear archivo .env
touch .env
```

Contenido del archivo `.env`:
```env
# Formato: postgresql://[usuario]:[password]@[host]:[puerto]/[database]
DATABASE_URL=postgresql://tu_usuario@localhost:5432/catalogia_db

# Ejemplo si tu usuario es "juan" y sin contraseña (default en Mac):
# DATABASE_URL=postgresql://juan@localhost:5432/catalogia_db

# Si configuraste una contraseña:
# DATABASE_URL=postgresql://juan:tu_password@localhost:5432/catalogia_db
```

**Nota**: Reemplaza `tu_usuario` con el resultado del comando `whoami`.

### 5. Ejecutar la Aplicación
```bash
# Asegúrate de estar en la raíz del proyecto CatalogIA/
# y con el entorno virtual activado
source .venv/bin/activate

# Ejecutar el servidor
uvicorn users_crud_server.main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: **http://localhost:8000**

---

## Documentación de la API

Una vez que el servidor esté corriendo, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Endpoints Disponibles

### Health Check
- `GET /health` - Verificar estado del servicio

### Users (CRUD)
- `POST /users/` - Crear nuevo usuario
- `GET /users/` - Listar todos los usuarios (con paginación)
- `GET /users/{user_id}` - Obtener usuario por ID
- `PATCH /users/{user_id}` - Actualizar usuario
- `DELETE /users/{user_id}` - Desactivar usuario (soft delete)

---

## Ejemplos de Uso

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Crear Usuario
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nuevo@example.com",
    "password": "mipassword123"
  }'
```

### 3. Listar Usuarios
```bash
curl http://localhost:8000/users/
```

### 4. Obtener Usuario por ID
```bash
curl http://localhost:8000/users/1
```

### 5. Actualizar Usuario
```bash
curl -X PATCH "http://localhost:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{
    "is_verified": true
  }'
```

### 6. Desactivar Usuario (Soft Delete)
```bash
curl -X DELETE "http://localhost:8000/users/1"
```

---

## Comandos Útiles
```bash
# Activar entorno virtual
source .venv/bin/activate

# Desactivar entorno virtual
deactivate

# Ver dependencias instaladas
pip list

# Actualizar requirements.txt
pip freeze > requirements.txt

# Verificar que PostgreSQL está corriendo
brew services list

# Conectarse a la base de datos
psql -d catalogia_db
```

## Licencia

Este proyecto es parte de un proyecto académico para demostración de capacidades de IA en e-commerce.