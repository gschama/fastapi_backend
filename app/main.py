from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from sqlalchemy import text

app = FastAPI(
    title=f"Mi Proyecto API - {settings.ENVIRONMENT}",
    description="API para aprender FastAPI y Screaming Architecture"
)

@app.get("/")
def leer_root():
    return {
        "mensaje": "Hola Mundo, estoy aprendiendo FastAPI",
        "entorno": settings.ENVIRONMENT,
        "base_datos": settings.DB_NAME
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Verifica que la API y la base de datos esten funcionando.
    """
    try:
        #Ejecutar una consulta simple para verificar conexion
        db.execute(text("SELECT 1"))
        return{
            "status": "ok",
            "environment": settings.ENVIRONMENT,
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Validacion de entorno al iniciar
if settings.ENVIRONMENT == "prod":
    print("CORRIENDO EN PRODUCCION - SEGURIDAD MAXIMA")
elif settings.ENVIRONMENT == "dev":
    print("CORRIENDO EN DESARROLLO - MODO DEBUG")
else:
    print("ENTORNO DESCONOCIDO")