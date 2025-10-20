from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import db
from app.views.user_view import router as user_router
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Inicializar base de datos
    db.init_db()
    print("✅ Base de datos inicializada")
    print(f"🚀 API ejecutándose en http://{settings.host}:{settings.port}")
    yield
    # Shutdown
    print("👋 Cerrando aplicación")

app = FastAPI(
    title="API de Gestión de Perfiles de Usuario",
    description="""
    API REST para gestión completa de perfiles de usuario en plataforma de reseñas.
    
    ## Funcionalidades principales:
    
    * **Crear usuario**: Registro de nuevos usuarios en la plataforma
    * **Ver perfil**: Acceso a información personal completa
    * **Actualizar perfil**: Modificación de datos personales
    * **Eliminar cuenta**: Eliminación permanente de la cuenta
    * **Desactivar cuenta**: Alternativa reversible a la eliminación
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(user_router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "API de Gestión de Perfiles de Usuario",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "create_user": "POST /api/users/",
            "get_profile": "GET /api/users/{user_id}/profile",
            "update_profile": "PUT /api/users/{user_id}/profile",
            "delete_account": "DELETE /api/users/{user_id}/account",
            "deactivate_account": "POST /api/users/{user_id}/deactivate"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )