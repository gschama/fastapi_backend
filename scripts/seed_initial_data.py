import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.usuarios.models import Role

def seed_initial_data():
    """
    Crea roles base si no existen.
    Es idempotente: seguro ejecutar múltiples veces.
    """
    print(" Iniciando poblado de datos base...")
    db = SessionLocal()
    
    try:
        # Roles que siempre deben existir al inicio
        roles_base = [
            {"name": "admin", "description": "Acceso total al sistema"},
            {"name": "user", "description": "Usuario estándar del sistema"}
        ]
        
        created_count = 0
        for role_data in roles_base:
            # Verificar si ya existe (por nombre único)
            existing = db.query(Role).filter(Role.name == role_data["name"]).first()
            
            if not existing:
                new_role = Role(
                    name=role_data["name"],
                    description=role_data["description"]
                )
                db.add(new_role)
                created_count += 1
                print(f" Rol '{role_data['name']}' creado.")
            else:
                print(f"ℹ  Rol '{role_data['name']}' ya existe.")
        
        db.commit()
        print(f"\n Resumen: {created_count} rol(es) nuevo(s) insertado(s).")
        
        # Verificación final
        total_roles = db.query(Role).count()
        print(f" Total de roles en base de datos: {total_roles}")
        print(" Poblado base completado exitosamente.")
        
    except Exception as e:
        db.rollback()
        print(f" Error durante el poblado: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_initial_data()