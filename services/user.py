from sqlalchemy.orm import Session

from controllers import user as usuario
from schemas.user import UserCreate, UserUpdate
from config.security import hash_password
from enums.user_role import UserRole

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class InvalidPhotoError(Exception):
    pass

# CREATE
def create_user(db: Session, user_data: UserCreate):
    # Comprobar si el correo ya existe
    existing_user = usuario.get_user_by_email(
        db,
        user_data.email
    )
    if existing_user:
        raise UserAlreadyExistsError(
            "El correo electrónico ya está registrado"
        )
    # Preparar información
    data = user_data.model_dump()
    # Generar hash de contraseña
    data["password"] = hash_password(data["password"])
    return usuario.create_user(db, data)

# READ - Todos los usuarios
def get_users(db: Session):
    return usuario.get_users(db)

# READ - Usuario por ID
def get_user(db: Session, user_id: int):
    user = usuario.get_user(db, user_id)
    if not user:
        raise UserNotFoundError(
            "Usuario no encontrado"
        )
    return user

# UPDATE
def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate
):
    # Buscar usuario
    db_user = get_user(db, user_id)
    # Obtener campos enviados
    data = user_data.model_dump(
        exclude_unset=True
    )
    # No permitir contraseñas nulas
    if "password" in data:
        if data["password"] is None:
            data.pop("password")
        else:
            data["password"] = hash_password(
                data["password"]
            )
    # Comprobar correo duplicado
    if data.get("email") is not None:
        existing_user = usuario.get_user_by_email(
            db,
            data["email"]
        )
        if existing_user and existing_user.id != user_id:
            raise UserAlreadyExistsError(
                "El correo electrónico ya está registrado"
            )
    return usuario.update_user(
        db,
        db_user,
        data
    )

# DELETE
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    return usuario.delete_user(db, db_user)

# SUBIR FOTOGRAFÍA
def upload_photo(
    db: Session,
    user_id: int,
    photo: bytes,
    content_type: str
):
    db_user = get_user(db, user_id)
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]
    if content_type not in allowed_types:
        raise InvalidPhotoError(
            "Formato de imagen no permitido"
        )
    if not photo:
        raise InvalidPhotoError(
            "La imagen está vacía"
        )

    max_size = 5 * 1024 * 1024
    if len(photo) > max_size:
        raise InvalidPhotoError(
            "La imagen no puede superar los 5 MB"
        )
    return usuario.update_user_photo(
        db,
        db_user,
        photo,
        content_type
    )

# CONSULTAR FOTOGRAFÍA
def get_photo(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user.photo:
        raise InvalidPhotoError(
            "El usuario no tiene fotografía"
        )
    return db_user.photo, db_user.photo_content_type

# ELIMINAR FOTOGRAFÍA
def delete_photo(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user.photo:
        raise InvalidPhotoError(
            "El usuario no tiene fotografía"
        )
    usuario.update_user_photo(
        db,
        db_user,
        None,
        None
    )
    return True