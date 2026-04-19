from sqlalchemy import (
    Column, BigInteger, String, Boolean, DateTime, ForeignKey, Text, func
)
from sqlalchemy.orm import relationship
from app.core.database import Base

# 1. Tabla: persons (Datos del Mundo Real)
class Person(Base):
    __tablename__ = "persons"

    id = Column(BigInteger, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    second_name = Column(String(100), nullable=True)
    other_name = Column(String(100), nullable=True)
    paternal_surname = Column(String(100), nullable=False)
    maternal_surname = Column(String(100), nullable=True)
    married_surname = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    #Relaciones 1:1
    user = relationship("User", back_populates="person", uselist=False)
    documents = relationship("PersonDocument", back_populates="person", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Person(id={self.id}, name={self.first_name} {self.paternal_surname})>"
    
# 2. Tabla: users (Datos del Sistema)
class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    # FK unica a persons (nullable=True para permitir registro sin perfil inicial)
    person_id = Column(BigInteger, ForeignKey("persons.id"), unique=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    #Relaciones
    person = relationship("Person", back_populates="user", uselist=False)
    user_pins = relationship("UserPin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    password_history = relationship("PasswordHistory", back_populates="user", cascade="all, delete-orphan")
    pin_history = relationship("PinHistory", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    assigned_roles = relationship("UserRole", foreign_keys="UserRole.assigned_by", back_populates="assigner")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
    
# 3. Tabla: person_documents (Reemplaza user_documents)
class PersonDocument(Base):
    __tablename__ = "person_documents"

    id = Column(BigInteger, primary_key=True, index=True)
    person_id = Column(BigInteger, ForeignKey("persons.id"), unique=True, nullable=False)
    # Documentos legales (String para preservar ceros y formatos)
    dpi = Column(String(13), unique=True, nullable=True)
    nit = Column(String(12), unique=True, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    verified_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    #Relaciones
    person = relationship("Person", back_populates="documents", uselist=False)
    verifier = relationship("User", foreign_keys=[verified_by])

    def __repr__(self):
        return f"<PersonDocument(person_id={self.person_id})>"
    
# 4. Tabla: roles
class Role(Base):
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # Relaciones
    users = relationship("UserRole", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"
    
# 5. Tabla: user_roles (Pivote Many-to-Many con atributos)
class UserRole(Base):
    __tablename__ = "user_roles"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    role_id = Column(BigInteger, ForeignKey("roles.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    assigned_by = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    # Relaciones explicitas para evitar ambiguedad con multiples FKs a users
    user = relationship("User", foreign_keys=[user_id], back_populates="roles")
    role = relationship("Role", back_populates="users")
    assigner = relationship("User", foreign_keys=[assigned_by], back_populates="assigned_roles")

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"
    
# 6. Tabla: user_pins (Actualizada)
class UserPin(Base):
    __tablename__ = "user_pins"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), unique=True, nullable=False)
    pin_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    must_change = Column(Boolean, default=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    # Relaciones
    user = relationship("User", back_populates="user_pins", uselist=False)

    def __repr__(self):
        return f"<UserPin(user_id={self.user_id})>"
    
# 7. Tabla: password_history (Actualizada)
class PasswordHistory(Base):
    __tablename__ = "password_history"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    # Relaciones
    user = relationship("User", back_populates="password_history")

    def __repr__(self):
        return f"<PasswordHistory(user_id={self.user_id})>"
    
# 8. Tabla: pin_history (Actualizada)
class PinHistory(Base):
    __tablename__ = "pin_history"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    pin_hash = Column(String(255), nullable=False)
    changed_by = Column(BigInteger, ForeignKey("users.id"), nullable=True)
    change_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # Relaciones
    user = relationship("User", foreign_keys=[user_id], back_populates="pin_history")
    changer = relationship("User", foreign_keys=[changed_by])

    def __repr__(self):
        return f"<PinHistory(user_id={self.user_id})>"