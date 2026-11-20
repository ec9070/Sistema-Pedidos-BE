from sqlalchemy import String, LargeBinary, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from enums.user_role import UserRole

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
            String(100),
            nullable=False
        )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    photo: Mapped[bytes | None] = mapped_column(
        LargeBinary(length=4294967295),
        nullable=True
    )

    photo_content_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )