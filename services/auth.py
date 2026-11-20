from sqlalchemy.orm import Session

from controllers import user as usuario
from config.security import verify_password

def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    # Buscar usuario por correo
    user = usuario.get_user_by_email(
        db,
        email
    )
    if not user:
        return None
    # Verificar contraseña
    if not verify_password(
        password,
        user.password
    ):
        return None
    # Comprobar si está activo
    if not user.is_active:
        return None
    return user