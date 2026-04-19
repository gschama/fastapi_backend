import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.usuarios.models import User, Person, Role, UserRole
from app.core.database import Base

print(" Verificando estructura de modelos y relaciones...")
print("=" * 60)
# 1. Verificar que las tablas están registradas en el metadata
tablas = list(Base.metadata.tables.keys())
tablas_esperadas = ["persons", "users", "person_documents", "roles", "user_roles", "user_pins", "password_history", "pin_history"]
print(f" Tablas registradas en ORM: {sorted(tablas)}")
faltantes = [t for t in tablas_esperadas if t not in tablas]
if faltantes:
    print(f" Faltan tablas en el metadata: {faltantes}")
else:
    print(" Todas las tablas esperadas están registradas.")
# 2. Verificar relaciones clave sin consultar la BD
print("\n Verificando relaciones definidas...")
# User -> Person (1:1)
rel_person = User.person.property
print(f"* User.person -> {rel_person.mapper.class_.__tablename__} (uselist=False: {rel_person.uselist})")
# User -> Roles (1:N vía pivote)
rel_roles = User.roles.property
print(f"* User.roles -> {rel_roles.mapper.class_.__tablename__}")
# Role -> Users
rel_users = Role.users.property
print(f"* Role.users -> {rel_users.mapper.class_.__tablename__}")
# Person -> Documents (1:1)
rel_docs = Person.documents.property
print(f"* Person.documents -> {rel_docs.mapper.class_.__tablename__} (uselist=False: {rel_docs.uselist})")
print("\n" + "=" * 60)
print(" Verificación de modelos completada. El ORM está listo para operaciones.")