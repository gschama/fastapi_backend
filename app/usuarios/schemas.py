from pydantic import BaseModel, ConfigDict, field_validator
import re
from typing import Optional
from datetime import datetime

#Schemas Base (Reutilizables)
class PersonBase(BaseModel):
    firs_name: str
    second_name: Optional[str] = None
    other_name: Optional[str] = None
    paternal_surname: str
    maternal_surname: Optional[str] = None
    married_surname: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    @field_validator("first_name", "paternal_surname")
    @classmethod
    def validate_names(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError("Debe tener al menos 2 caracteres")
        return v.strip()
    
class DocumentBase(BaseModel):
    dpi: Optional[str] = None
    nit: Optional[str] = None

    @field_validator("dpi")
    @classmethod
    def validate_dpi(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r"^\d{13}$", v):
            raise ValueError("DPI debe tener exactamente 13 digitos numericos")
        return v
    
    @field_validator("nit")
    @classmethod
    def validate_nit(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not re.match(r"^(?:\d{7,12}|\d{6,11}[a-zA-Z])$", v):
            raise ValueError("NIT invalido: debe tener entre 7 y 12 caracteres. Solo numeros, o numeros terminados en una sola letra.")
        return v
    
#Schema de Entrada (Registro de Usuario)
class UserRegisterIn(BaseModel):
    email: str
    username: str
    password: str
    person: PersonBase
    documents: Optional[DocumentBase] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(r"^(?=.{6,254}$)[^@]+@[^@]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Formato de email invalido")
        return v
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.strip().lower()
        if not re.match(r"^[a-z0-9]{3,20}$"):
            raise ValueError("Username: solo minusculas, numeros y guion bajo (3 - 20 caracteres)")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Minimo 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Debe contener al menos una mayuscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("Debe contener al menos una minuscula")
        if not re.search(r"\d", v):
            raise ValueError("Debe contener al menos un numero")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Debe contener al menos un caracter especial")
        return v
    
# Schema de Salida (Respuesta de la API)
class UserOut(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime
    person: Optional[PersonBase] = None
    #Pydantic v2: Permite leer atributos de objetos SQLAlchemy directamente
    model_config = ConfigDict(from_attributes=True)