from sqlalchemy import(
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, UniqueConstraint, Index, Table
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
from app.core.database import Base

class User(Base):
    """
    Tabla de Autenticacion.
    Datos minimos para login y seguridad.
    """
    __tablename__="users" # Nombre de la tabla en la base de datos
    id = Column(Integer, primary_key=True, index=True) #Clave primario (ID unico para cada usuario)
    email = Column(String(255), unique=True, index=True, nullable=False) # email (unico, no puede repetirse)
    username = Column(String(100), unique=True, index=True, nullable=False) #nombre de usuario (unico)
    password_hash = Column(String(255), nullable=False) #Contrasena (hash encriptado, NUNCA texto plano)
    is_active = Column(Boolean, default=True, nullable=False) # El usuario esta activo?
    is_admin = Column(Boolean, default=False, nullable=False) #El usuario es administrador?
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) #Fecha de creacion (automatica)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True) #Fecha de actualizacion (automatica)
    #RELACIONES
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    documents = relationship("UserDocument", back_populates="user", uselist=False, cascade="all, delete-orphan")
    pin = relationship("UserPin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    password_history = relationship("PasswordHistory", back_populates="user", cascade="all, delete-orphan")
    pin_history = relationship("PinHistory", back_populates="user", cascade="all, delete-orphan")

    #REPRESENTACION DEL OBJETO
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
    
class UserProfile(Base):
    """
    Tabla de Perfil Personal.
    Informacion personal del usuario con flesibilidad para diferentes culturas.
    """
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    second_name = Column(String(100), nullable=True)
    other_name = Column(String(100), nullable=True)
    paternal_surname = Column(String(100), nullable=False)
    maternal_surname = Column(String(100), nullable=True)
    married_surname = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=False)
    addres = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    #RELACION INVERSA
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id})>"
    
class UserDocument(Base):
    """
    Tabla de Documentos Legales.
    Datos sensibles que requieren verificacion adicional.
    """
    __tablename__ = "user_documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    dpi = Column(String(13), unique=True, nullable=True)
    nit = Column(String(12), unique=True, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    #RELACION INVERSA
    user = relationship("User", back_populates="documents")
    def __repr__(self):
        return f"<UserDocumento(user_id={self.user_id})>"
    
class UserPin(Base):
    """
    Tabla de PIN Actual del Usuario.
    Para autenticacion de segundo factor o transacciones.
    """
    __tablename__ = "user_pins"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    pin_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    must_change = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    #RELACION INVERSA
    user = relationship("User", back_populates="pin")

    def __repr__(self):
        return f"<UserPin(user_id={self.user_id})>"
    
class PasswordHistory(Base):
    """
    Historial de contrasenas.
    Para evitar reutilizacion de contrasenas antiguas.
    """
    __tablename__ = "password_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    user = relationship("User", back_populates="password_history")
    
    def __repr__(self):
        return f"<PasswordHistory(user_id={self.user_id})>"
    
class PinHistory(Base):
    __tablename__ = "pin_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pin_hash = Column(String(255), nullable=False)
    change_by = Column(Integer, ForeignKey("users.id"), nullable = True)
    change_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user = relationship("User", back_populates="pin_history")
    def __repr__(self):
        return f"<PinHistory(user_id={self.user_id})>"