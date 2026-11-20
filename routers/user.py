from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Response
)

from sqlalchemy.orm import Session

from db.database import get_db

from schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from services import user as user_service

from fastapi import Depends

from config.dependencies import require_roles
from enums.user_role import UserRole

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
    dependencies=[
        Depends(
            require_roles(UserRole.Administrador)
        )
    ]
)

# CREATE
@router.post(
    "/",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return user_service.create_user(db, user)
    except user_service.UserAlreadyExistsError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

# READ - Todos los usuarios
@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

# READ - Usuario por ID
@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        return user_service.get_user(db, user_id)
    except user_service.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

# UPDATE
@router.patch(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    try:
        return user_service.update_user(
            db,
            user_id,
            user
        )
    except user_service.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except user_service.UserAlreadyExistsError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )

# DELETE
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        user_service.delete_user(db, user_id)
        return {
            "message": "Usuario eliminado correctamente"
        }
    except user_service.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

# SUBIR FOTOGRAFÍA
@router.post("/{user_id}/photo")
async def upload_photo(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        photo = await file.read()
        user_service.upload_photo(
            db,
            user_id,
            photo,
            file.content_type or ""
        )
        return {
            "message": "Fotografía guardada correctamente"
        }
    except user_service.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except user_service.InvalidPhotoError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
        
# CONSULTAR FOTOGRAFÍA
@router.get("/{user_id}/photo")
def get_photo(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        photo, content_type = user_service.get_photo(
            db,
            user_id
        )
        return Response(
            content=photo,
            media_type=content_type
        )
    except user_service.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except user_service.InvalidPhotoError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

# ELIMINAR FOTOGRAFÍA
@router.delete("/{user_id}/photo")
def delete_photo(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        user_service.delete_photo(db, user_id)
        return {
            "message": "Fotografía eliminada correctamente"
        }
    except user_service.UserNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
    except user_service.InvalidPhotoError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )