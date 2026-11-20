from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

import jwt
from jwt.exceptions import InvalidTokenError


from db.database import get_db

from controllers import user as usuario

from models.user import User

from enums.user_role import UserRole

from config.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la autenticación",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )
    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = usuario.get_user(
            db,
            int(user_id)
        )
        if not user or not user.is_active:
            raise credentials_exception
        return user
    except (
        InvalidTokenError,
        ValueError,
        TypeError
    ):
        raise credentials_exception

def require_roles(*allowed_roles: UserRole):
    def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta operación"
            )
        return current_user
    return role_checker