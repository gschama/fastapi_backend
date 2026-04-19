from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pathlib import Path
import os

#Obtener la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    #Configuracion de Pydantic
    model_config = SettingsConfigDict(
        #Intentar cargar archivos en este orden de prioridad
        env_file=[
            BASE_DIR / f".env.{os.getenv('ENVIRONMENT', 'dev')}",
            BASE_DIR / ".env.dev",
            BASE_DIR / ".env"
        ],
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore" #Ignora variables no definidas en la clase
    )
    #===========================
    #VARIABLES DE CONFIGURACION |
    #===========================

    #Entorno
    ENVIRONMENT: str = ""

    #Base de Datos
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_NAME: str = ""

    #Seguridad JWT
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0

    #Debug (solo para desarrollo)
    DEBUG: bool = False

    #========================
    #PROPIEDADES DERIVADAS
    #========================

    @property
    def DATABASE_URL(self) -> str:
        """
        Construye la URL de conexion para SQLAlchemy.
        Formato: mysql+pymysql://usuario:password@host:puerto/base_datos
        """
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def is_production(self) -> bool:
        """Helper para verificar si estamos en produccion"""
        return self.ENVIRONMENT.lower() == "prod"
    
    @property
    def is_development(self) -> bool:
        """Helper para verificar si estamos en desarrollo"""
        return self.ENVIRONMENT.lower() == "dev"
    
    #==========================
    # Validaciones de Seguridad
    #==========================

    def validate_for_production(self) -> None:
        """
        Valida que las configuraciones criticas esten presentes en produccion.
        Lanza error si falta algo importante
        """
        if self.is_production:
            if not self.SECRET_KEY:
                raise ValueError("SECRET_KEY es requerida en produccion")
            if not self.DB_PASSWORD:
                raise ValueError("DB_PASSWORD es requerida en produccion")
            if self.DEBUG:
                raise ValueError("DEBUG debe ser False en produccion")
            
@lru_cache()
def get_settings() -> Settings:
    """
    Singleton: Carga la configuracion una sola vez y la cachea.
    Esto mejora el rendimiento y asegura consistencia.
    """
    return Settings()

#Instancia global para importar en toda la aplicacion
settings = get_settings()

#Validar configuracion al cargar (opcional, para detectar errores temprano)
# settings.validate_for_production()