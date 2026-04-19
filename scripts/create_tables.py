import sys
from pathlib import Path

# Agregar la raiz del proyecto al path para poder importar
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import engine, Base
from app.usuarios.models import User, UserProfile, UserDocument, UserPin, PasswordHistory, PinHistory # Importar todos los modelos aqui

def crear_tablas():
    """
    Crear todas las tablas en la base de datos que aun no existen.
    """
    print("Conectando a la base de datos...")
    print(f"URL: {engine.url}")

    try:
        print("Creando tablas...")
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas exitosamente!!!")

        #Verificar que tablas se crearon
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tablas = inspector.get_table_names()
        print(f"Tablas en la base de datos: {tablas}")

    except Exception as e:
        print(f"Error al crear tablas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    crear_tablas()