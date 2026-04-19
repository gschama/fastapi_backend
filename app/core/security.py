from argon2 import PasswordHasher, exceptions
from argon2.exceptions import VerifyMismatchError
from typing import Optional

#Configuracion de Argon 2
#PaswordHasher ya viene con configuraciones seguras por defecto
#Pero podemos personalizarlas si es necesario.
ph = PasswordHasher(
    time_cost=2,             #Numero de iteraciones
    memory_cost=65536,     # Memoria usada en KB (64 MB)
    parallelism=1,         #Hilos paralelos
    hash_len=32,           #Longitud del hash resultante
    salt_len=16            #Longitud del salt aleatorio
)

#Funciones de Hashing

def hash_password(password: str) -> str:
    """
    Genera un hash seguro de una contrasenia usando Argon2.

    Args:
        password: La contrasenia en texto plano del usuario

    Returns:
        str: El hash encriptado (incluye el salt automaticamente)

    Ejemplo:
        >>> hash_password("mi contrasenia123")
        '$argon2d$v=19$m=6553, t=3, p=4$...salt...$...hash...'
    """
    return p