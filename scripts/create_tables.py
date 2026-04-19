import sys
from pathlib import Path

# Agregar la raiz del proyecto al path para poder importar
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import engine, Base
from app.usuarios.models import (
    Person,
    User,
    PersonDocument,
    Role,
    UserRole,
    UserPin,
    PasswordHistory,
    PinHistory
)

def crear_tablas():
    """
    Crear todas las tablas en la base de datos que aun no existen.
    """
    print("Conectando a la base de datos...")
    print(f"URL: {engine.url}")

    try:
        print("Verificando y creando tablas faltantes...")

        #Listar tablas que estan definidas en nuestros modelos
        tablas_registradas = list(Base.metadata.tables.keys())
        print(f"Tablas definidas en codigo: {tablas_registradas}")
        # SQLAlchemy solo crea talbas que NO existen en la BD
        #No borra tablas viejas automaticamente.
        Base.metadata.create_all(bind=engine)
        print("Proceso completado. Se crearon las tablas nuevas.")
        #Verificacion final contra la BD real
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tablas_reales = inspector.get_table_names()
        print(f"Tablas existentes en la base de datos: {tablas_reales}")
        #Verificacion de seguridad para tablas viejas
        tablas_obsoletas = ['user_profiles', 'user_documents']
        for tabla_vieja in tablas_obsoletas:
            if tabla_vieja in tablas_reales:
                print(f"ADVERTENCIA: La tabla antigua '{tabla_vieja}' sigue existiendo. "
                      f"Debes eliminarla manualmente desde DBeaver si ya no la necesitas.")

    except Exception as e:
        print(f"Error al gestionar tablas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    crear_tablas()