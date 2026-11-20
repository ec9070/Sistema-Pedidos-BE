from fastapi import FastAPI

from db.base import Base
from db.database import engine

from models.user import User

from routers import user, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Kivox",
    description="API para sistema de pedidos",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {
        "message": "Bienvenido a la API de sistema pedidos"
    }