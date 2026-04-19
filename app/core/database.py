from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

#CREAR EL MOTOR DE BASE DE DATOS
#echo=True: Muestra las consultas SQL en la consola (uitl para aprender)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,    #Solo muestra SQL si DEBUG=true
    pool_pre_ping=True      #Verifica que la conexion este viva antes de usarla
)

#CREAR LA SESION
#La sesion es como un ventana temporal para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#BASE PARA LOS MODELOS
#Todos los modelos heredaran de esta clase
Base = declarative_base()

#DEPENDENCIA PARA OBTENER SESION
#Esto se usara en las rutas de FastAPI para obtener una sesion de BD
def get_db():
    """
    Genera una nueva sesion de base de datos.
    Se cierra automaticamente despues de usar
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()