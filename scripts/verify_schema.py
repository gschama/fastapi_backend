import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.database import engine
from sqlalchemy import inspect

def verify_schema():
    print(" Verificando esquema de base de datos...")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f" Tablas encontradas en BD: {tables}")

    # 1. Verificar tablas obsoletas
    old_tables = ['user_profiles', 'user_documents']
    print("\n  Estado de tablas obsoletas:")
    for old in old_tables:
        if old in tables:
            print(
                f"  ADVERTENCIA: '{old}' aún existe. Elimínala manualmente en DBeaver.")
        else:
            print(f" '{old}' ya fue eliminada.")

    # 2. Verificar columnas de 'users'
    print("\n Verificando tabla 'users':")
    if 'users' in tables:
        cols = inspector.get_columns('users')
        col_names = [c['name'] for c in cols]
        expected_cols = ['id', 'email', 'username', 'password_hash', 'person_id',
                         'is_active', 'created_at', 'updated_at', 'email_verified_at', 'last_login_at']
        missing = [c for c in expected_cols if c not in col_names]
        extra = [c for c in col_names if c not in expected_cols and c != 'id']

        if not missing:
            print(" Columnas de 'users' correctas.")
        else:
            print(f" Faltan columnas en 'users': {missing}")

        # Verificar que is_admin YA NO existe
        if 'is_admin' in col_names:
            print(" 'is_admin' aún existe en 'users'. Debe eliminarse.")
        else:
            print(" 'is_admin' eliminado correctamente.")
    else:
        print(" La tabla 'users' no existe.")

    # 3. Verificar tipos BIGINT en IDs
    print("\n Verificando tipos de datos (BIGINT en IDs):")
    tables_to_check = ['persons', 'users', 'roles', 'user_roles', 'user_pins',
                       'password_history', 'pin_history', 'person_documents']
    all_bigint_ok = True
    for t in tables_to_check:
        if t in tables:
            cols = inspector.get_columns(t)
            id_col = next((c for c in cols if c['name'] == 'id'), None)
            if id_col:
                type_str = str(id_col['type']).upper()
                if 'BIGINT' in type_str or 'BIG INT' in type_str:
                    print(f" {t}.id es BIGINT")
                else:
                    print(f" {t}.id es {id_col['type']} (Debe ser BIGINT)")
                    all_bigint_ok = False

    # 4. Verificar FKs críticas
    print("\n Verificando Foreign Keys principales:")
    if 'users' in tables:
        fks_users = inspector.get_foreign_keys('users')
        person_fk = next(
            (fk for fk in fks_users if 'person_id' in fk['constrained_columns']), None)
        if person_fk and person_fk['referred_table'] == 'persons':
            print(" users.person_id -> persons.id")
        else:
            print(" users.person_id FK incorrecta o faltante")

    print("\n" + "=" * 60)
    if all_bigint_ok and 'users' in tables:
        print(" ESQUEMA VERIFICADO CORRECTAMENTE. Base de datos lista.")
    else:
        print("  Revisa las advertencias/errores antes de continuar.")


if __name__ == "__main__":
    verify_schema()
