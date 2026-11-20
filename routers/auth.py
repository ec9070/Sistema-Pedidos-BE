from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from db.database import get_db

from services import auth as auth_service

from config.security import create_access_token

from schemas.auth import Token

from config.dependencies import get_current_user
from schemas.user import UserResponse
from models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth_service.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
    # Generar JWT
    access_token = create_access_token(
        subject=str(user.id)
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get(
    "/me",
    response_model=UserResponse
)
def get_authenticated_user(
    current_user: User = Depends(get_current_user)
):
    return current_user
