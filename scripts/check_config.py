#scripts/chech_config.py
import sys
from pathlib import Path

#Agregar la raiz del proyecto al path para poder importar
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.config import settings

print("Verificacion de Configuracion")
print("=" * 50)
print(f"Entorno: {settings.ENVIRONMENT or 'NO CONFIGURADO'}")
print(f"Es prduccion?? {settings.is_production}")
print(f"Es desarrollo?? {settings.is_development}")
print(f"DB Host: {settings.DB_HOST or 'NO CONFIGURADO'}")
print(f"DB Name: {settings.DB_NAME or 'NO CONFIGURADO'}")
print(f"SECRET_KEY: {'CONFIGURADA' if settings.SECRET_KEY else 'NO CONFIGURADA'}")
print(F"DEBUG: {settings.DEBUG}")
print("=" * 50)

#Validaciones basicas
errores = []

if not settings.ENVIRONMENT:
    errores.append("ENVIRONMENT no configurado")

if not settings.DB_HOST:
    errores.append("DB_HOST no Configurado")

if not settings.DB_PASSWORD:
    errores.append("DB_PASSWORD no configurado")

if not settings.SECRET_KEY:
    errores.append("SECRET_KEY no configurado")

if settings.is_production and settings.DEBUG:
    errores.append("DEBUG no puede estar activo en produccion")

if errores:
    print("ERRORES ENCONTRADOS:")
    for error in errores:
        print(f"{error}")
    sys.exit(1)
else: 
    print("Configuracion valida")