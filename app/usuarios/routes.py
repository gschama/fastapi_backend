from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.core.security import hash_password
from app.usuarios import schemas
from app.usuarios.models import Person, User, PersonDocument, Role, UserRole

router = APIRouter(prefix="/auth", tags=["Autenticacion"])

@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(payload: schemas.UserRegisterIn, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario con su perfil y rol por defecto.
    Operacion atomica: si algo falla, nada se guarda.
    """
    try:
        # 1. Verificar duplicados a nivel de BD (evita race conditions)
        existing = db.query(User).filter(
            (User.email == payload.email) | (User.username == payload.username)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email o username ya estan registrados"
            )
        
        # 2. Hashear contrasenia de forma segura
        hashed_password = hash_password(payload.password)

        # 3. Crear registro de Persona
        persona_data = payload.person.model_dump()
        persona = Person(**persona_data)
        db.add(persona)
        db.flush()   # Asigna ID temporal sin hacer commit todavia

        # 4. Crear registro de Usuario vinculado a la persona
        usuario = User(
            email=payload.email,
            username=payload.username,
            password_hash=hashed_password,
            person_id=persona.id,
            is_active=True
        )
        db.add(usuario)
        db.flush()

        # 5. Documentos legales (opcionales)
        if payload.documents:
            doc_data = payload.documents.model_dump()
            documento = PersonDocument(person_id=persona.id, **doc_data)
            db.add(documento)

        # 6. Asignar rol por defecto "user"
        rol_base = db.query(Role).filter(Role.name == "user").first()
        if not rol_base:
            # Esto no deberia pasar si ejecutaste seed_initial_data.py
            raise HTTPException(status_code=500, detail="Error de configuracion: rol 'user' no encuentrado")
        
        db.add(UserRole(user_id=usuario.id, role_id=rol_base.id))

        # 7. Commit atomico: todo o nada
        db.commit()
        db.refresh(usuario) # Carga relaciones recien creadas

        return usuario
    
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Conflicto de datos: email, username o documento ya existente"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al registrar usuario: {str(e)}"
        )