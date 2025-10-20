from fastapi import APIRouter, HTTPException, status, Path
from app.models.user import (
    UserCreate, 
    UserUpdate, 
    UserResponse, 
    UserProfileResponse,
    DeleteAccountResponse
)
from app.controllers.user_controller import UserController

router = APIRouter(prefix="/api/users", tags=["User Profile Management"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Registra un nuevo usuario en la plataforma
    """
    try:
        # Verificar si el email ya existe
        existing_user = UserController.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {user.email} ya está registrado"
            )
        
        result = UserController.create_user(user)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )

@router.get("/{user_id}/profile", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: int = Path(..., description="ID del usuario", gt=0)
):
    """
    Obtiene el perfil completo del usuario
    
    Permite a un usuario acceder a toda su información personal almacenada
    """
    user = UserController.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado o cuenta inactiva"
        )
    return user

@router.put("/{user_id}/profile", response_model=UserResponse)
async def update_user_profile(
    user_id: int = Path(..., description="ID del usuario", gt=0),
    user_data: UserUpdate = None
):
    """
    Actualiza la información personal del usuario
    
    Permite al usuario modificar sus datos personales:
    - Nombre completo
    - Teléfono
    - Biografía
    - Ubicación
    
    Solo se actualizan los campos proporcionados (actualización parcial)
    """
    result = UserController.update_user_profile(user_id, user_data)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado o cuenta inactiva"
        )
    return result

@router.delete("/{user_id}/account", response_model=DeleteAccountResponse)
async def delete_user_account(
    user_id: int = Path(..., description="ID del usuario", gt=0)
):
    """
    Elimina la cuenta del usuario de forma PERMANENTE
    
    ⚠️ ADVERTENCIA: Esta acción es irreversible
    
    Elimina completamente:
    - Toda la información personal del usuario
    - El perfil del usuario
    - Todos los datos asociados
    
    Esta operación NO puede deshacerse.
    """
    deleted_user = UserController.delete_user_account(user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado o ya fue eliminado"
        )
    
    return DeleteAccountResponse(
        message="Cuenta eliminada exitosamente. Todos tus datos han sido borrados de forma permanente.",
        deleted_user_id=deleted_user["id"],
        deleted_email=deleted_user["email"]
    )

@router.post("/{user_id}/deactivate")
async def deactivate_account(
    user_id: int = Path(..., description="ID del usuario", gt=0)
):
    """
    Desactiva la cuenta del usuario (alternativa a eliminación permanente)
    
    Esta es una opción más segura que permite:
    - Ocultar el perfil del usuario
    - Mantener los datos en el sistema
    - Posibilidad de reactivación futura
    """
    result = UserController.deactivate_user_account(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado o ya está inactivo"
        )
    
    return {
        "message": "Cuenta desactivada exitosamente",
        "user_id": result["id"],
        "email": result["email"],
        "is_active": result["is_active"]
    }