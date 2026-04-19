from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from typing import Union

#Configuracion de Argon 2
#PaswordHasher ya viene con configuraciones seguras por defecto
#Solo se personalizan si hay requisitos especificos de rendimiento/seguridad.
ph = PasswordHasher()

#Funciones de Hashing

def hash_password(password: str) -> str:
    """
    Genera un hash seguro de una contrasenia usando Argon2.

    Args:
        password: La contrasenia en texto plano

    Returns:
        str: El hash encriptado (incluye el salt version y parametro)
    """
    return ph.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica si una contrasenia coincide con un hash almacenado.

    Args:
        password: Contrasenia ingresada por el usuario
        hashed_password: Hash guardado en la base de datos

    Returns:
        bool: True si coinciden, False si no
    """
    try:
        ph.verify(hashed_password, password)
        return True
    except (VerifyMismatchError, InvalidHashError):
        return False
    except Exception:
        #Cualquier otro error de parsing = fallo seguro
        return False
    
def needs_rehash(hashed_password: str) -> bool:
    """
    Verificar si el hash necesita actualizarse con parametros mas modernos.
    Util para mejorar seguridad gradualmente sin forzar cambio de contrasenia.
    """
    return ph.check_needs_rehash(hashed_password)