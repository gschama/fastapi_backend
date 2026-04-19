import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal
from app.usuarios.models import Person, User, Role, UserRole

def test_e2e_models():
    print(" Iniciando validación End-to-End de modelos y relaciones...")
    db = SessionLocal()
    
    try:
        # 1. Crear una Persona de prueba
        print("\n Creando Persona de prueba...")
        persona_prueba = Person(
            first_name="Juan",
            second_name="Carlos",
            paternal_surname="Pérez",
            maternal_surname="García",
            phone="5555-1234"
        )
        db.add(persona_prueba)
        db.flush()  # Genera el ID sin hacer commit definitivo aún
        print(f" Persona creada con ID: {persona_prueba.id}")

        # 2. Crear Usuario vinculado a la Persona
        print("\n Creando Usuario vinculado a la Persona...")
        usuario_prueba = User(
            email="juan.prueba@ejemplo.com",
            username="juan_prueba",
            password_hash="$argon2id$v=19$m=65536,t=2,p=1$...hash_falso_test...",
            person_id=persona_prueba.id,  # Relación 1:1
            is_active=True
        )
        db.add(usuario_prueba)
        db.flush()
        print(f" Usuario creado con ID: {usuario_prueba.id} | person_id: {usuario_prueba.person_id}")

        # 3. Asignar Rol (Many-to-Many vía pivote)
        print("\n Asignando rol 'admin' al usuario...")
        rol_admin = db.query(Role).filter(Role.name == "admin").first()
        if not rol_admin:
            raise Exception(" No se encontró el rol 'admin'. Ejecuta seed_initial_data.py primero.")
        
        asignacion = UserRole(
            user_id=usuario_prueba.id,
            role_id=rol_admin.id
        )
        db.add(asignacion)
        db.commit()  # Confirmar todos los cambios
        print(" Transacción completada. Datos guardados en BD.")

        # 4. Verificación de lectura (Relaciones inversas)
        print("\n Verificando relaciones inversas (lectura)...")
        usuario_leido = db.query(User).filter(User.id == usuario_prueba.id).first()
        print(f"* Usuario.email: {usuario_leido.email}")
        print(f"* Usuario.person.first_name: {usuario_leido.person.first_name}")
        print(f"* Usuario.roles[0].role.name: {usuario_leido.roles[0].role.name}")
        
        rol_leido = db.query(Role).filter(Role.id == rol_admin.id).first()
        print(f"* Rol.users[0].user.username: {rol_leido.users[0].user.username}")

        # 5. Limpieza automática (dejar la BD limpia para el siguiente paso del curso)
        print("\n Limpiando datos de prueba...")
        db.delete(asignacion)
        db.delete(usuario_leido)
        db.delete(persona_prueba)
        db.commit()
        print(" Datos de prueba eliminados. BD queda en estado limpio.")
        print("\n" + "=" * 60)
        print(" VALIDACIÓN E2E EXITOSA. La arquitectura refactorizada es 100% funcional.")

    except Exception as e:
        db.rollback()
        print(f"\n Error durante la validación: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_e2e_models()