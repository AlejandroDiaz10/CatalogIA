from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from users_crud_server import crud, schemas
from users_crud_server.database import get_db

app = FastAPI(
    title="CatalogIA Users API",
    description="API para gestión de usuarios - CatalogIA E-commerce Platform",
    version="1.0.0",
)


# Health Check
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "catalogia-users-api", "version": "1.0.0"}


# CREATE - Crear usuario
@app.post(
    "/users/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo usuario.

    - **email**: Email único del usuario
    - **password**: Contraseña (será hasheada automáticamente)
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)


# READ - Obtener todos los usuarios
@app.get("/users/", response_model=List[schemas.UserResponse], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de usuarios con paginación.

    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Número máximo de registros a devolver (default: 100)
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# READ - Obtener usuario por ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener un usuario específico por su ID.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


# UPDATE - Actualizar usuario
@app.patch("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def update_user(
    user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)
):
    """
    Actualizar información de un usuario.

    Puedes actualizar uno o varios campos:
    - **email**: Nuevo email
    - **password**: Nueva contraseña
    - **is_active**: Estado de la cuenta
    - **is_verified**: Estado de verificación
    """
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


# DELETE - Soft delete de usuario
@app.delete("/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Desactivar un usuario (soft delete).

    El usuario no se elimina de la base de datos, solo se marca como inactivo.
    """
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user
