from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from config.config import settings

# Configuración de conexión
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    query={
        "charset": "utf8mb4"
    }
)

# Crear engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Crear sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependencia para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":

    try:
        with engine.connect() as connection:
            print("Conexión a MySQL exitosa")

    except Exception as error:
        print("Error al conectar con MySQL:")
        print(error)