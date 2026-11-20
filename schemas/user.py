from pydantic import (
    BaseModel,
    EmailStr,
    ConfigDict,
    Field
)

from enums.user_role import UserRole

# Esquema para crear usuarios
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    phone: str | None = Field(
        default=None,
        max_length=20
    )
    role: UserRole

# Esquema para actualizar usuarios
class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    email: EmailStr | None = None
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128
    )
    phone: str | None = Field(
        default=None,
        max_length=20
    )
    role: UserRole | None = None
    is_active: bool | None = None

# Esquema de respuesta
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str | None
    role: UserRole
    is_active: bool
    photo_content_type: str | None
    model_config = ConfigDict(
        from_attributes=True
    )
