from sqlalchemy.orm import Session

from models.user import User

# CREATE
def create_user(db: Session, user_data: dict):
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# READ - Todos los usuarios
def get_users(db: Session):
    return db.query(User).order_by(User.id).all()

# READ - Usuario por ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(
        User.id == user_id
    ).first()

# READ - Usuario por correo
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(
        User.email == email
    ).first()

# UPDATE
def update_user(
    db: Session,
    db_user: User,
    update_data: dict
):
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE
def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
    return True

# ACTUALIZAR FOTOGRAFÍA
def update_user_photo(
    db: Session,
    db_user: User,
    photo: bytes | None,
    content_type: str | None
):
    db_user.photo = photo
    db_user.photo_content_type = content_type
    db.commit()
    db.refresh(db_user)
    return db_user