from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional
from app.controllers.user_controller import UserController
from app.models.user import UserCreate, UserUpdate

router = APIRouter(prefix="/web", tags=["Web Interface"])

# Configurar templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Página de inicio"""
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/users", response_class=HTMLResponse)
async def list_users(request: Request):
    """Lista todos los usuarios"""
    users = UserController.get_all_users()
    return templates.TemplateResponse(
        "users_list.html",
        {"request": request, "users": users}
    )

@router.get("/users/create", response_class=HTMLResponse)
async def create_user_form(request: Request):
    """Formulario para crear usuario"""
    return templates.TemplateResponse("create_user.html", {"request": request})

@router.post("/users/create")
async def create_user_submit(
    request: Request,
    email: str = Form(...),
    full_name: str = Form(...),
    phone: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    location: Optional[str] = Form(None)
):
    """Procesar creación de usuario"""
    try:
        # Verificar si el email ya existe
        existing_user = UserController.get_user_by_email(email)
        if existing_user:
            return templates.TemplateResponse(
                "create_user.html",
                {
                    "request": request,
                    "error": f"El email {email} ya está registrado",
                    "email": email,
                    "full_name": full_name,
                    "phone": phone,
                    "bio": bio,
                    "location": location
                }
            )
        
        # Crear usuario
        user_data = UserCreate(
            email=email,
            full_name=full_name,
            phone=phone,
            bio=bio,
            location=location
        )
        new_user = UserController.create_user(user_data)
        
        # Redirigir al perfil del usuario creado
        return RedirectResponse(
            url=f"/web/users/{new_user['id']}/profile",
            status_code=303
        )
    except Exception as e:
        return templates.TemplateResponse(
            "create_user.html",
            {
                "request": request,
                "error": f"Error al crear usuario: {str(e)}",
                "email": email,
                "full_name": full_name,
                "phone": phone,
                "bio": bio,
                "location": location
            }
        )

@router.get("/users/{user_id}/profile", response_class=HTMLResponse)
async def view_profile(request: Request, user_id: int):
    """Ver perfil de usuario"""
    user = UserController.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return templates.TemplateResponse(
        "view_profile.html",
        {"request": request, "user": user}
    )

@router.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_profile_form(request: Request, user_id: int):
    """Formulario para editar perfil"""
    user = UserController.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return templates.TemplateResponse(
        "edit_profile.html",
        {"request": request, "user": user}
    )

@router.post("/users/{user_id}/edit")
async def edit_profile_submit(
    request: Request,
    user_id: int,
    full_name: str = Form(...),
    phone: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    location: Optional[str] = Form(None)
):
    """Procesar actualización de perfil"""
    try:
        user_data = UserUpdate(
            full_name=full_name,
            phone=phone if phone else None,
            bio=bio if bio else None,
            location=location if location else None
        )
        
        updated_user = UserController.update_user_profile(user_id, user_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return RedirectResponse(
            url=f"/web/users/{user_id}/profile?updated=true",
            status_code=303
        )
    except Exception as e:
        user = UserController.get_user_by_id(user_id)
        return templates.TemplateResponse(
            "edit_profile.html",
            {
                "request": request,
                "user": user,
                "error": f"Error al actualizar: {str(e)}"
            }
        )

@router.post("/users/{user_id}/delete")
async def delete_user_submit(user_id: int):
    """Eliminar usuario"""
    deleted_user = UserController.delete_user_account(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return RedirectResponse(url="/web/users?deleted=true", status_code=303)