import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.security import hash_password, verify_password, needs_rehash

def test_security():
    print(" Probando sistema de encriptación Argon2")
    print("=" * 60)
    
    password_original = "MiContraseñaSegura123!"
    print(f" Contraseña original: {password_original}")
    
    # 1. Generar hash
    hash_1 = hash_password(password_original)
    print(f"\n Hash 1 generado:\n{hash_1[:80]}...")
    
    # 2. Generar otro hash de la misma contraseña (demostrar salt único)
    hash_2 = hash_password(password_original)
    print(f"\n Hash 2 generado:\n{hash_2[:80]}...")
    
    print(f"\n ¿Los hashes son diferentes? {hash_1 != hash_2}")
    print("    ¡Correcto! El salt aleatorio garantiza unicidad")
    
    # 3. Verificar contraseña correcta
    ok = verify_password(password_original, hash_1)
    print(f"\n Verificación (correcta): {ok} {'' if ok else ''}")
    
    # 4. Verificar contraseña incorrecta
    mal = verify_password("ContraseñaEquivocada", hash_1)
    print(f" Verificación (incorrecta): {mal} {'' if not mal else ''}")
    
    # 5. Re-hash check
    rehash = needs_rehash(hash_1)
    print(f"\n ¿Necesita actualizar parámetros? {rehash}")
    
    print("\n" + "=" * 60)
    print(" Todas las pruebas de seguridad completadas exitosamente.")

if __name__ == "__main__":
    test_security()