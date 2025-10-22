from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pathlib import Path
from app.database import db
# from app.views.user_view import router as user_api_router
from app.views.user_web_view import router as user_web_router  # ← NUEVO
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Inicializar base de datos
    db.init_db()
    print("✅ Base de datos inicializada")
    print(f"🚀 API ejecutándose en http://{settings.host}:{settings.port}")
    print(f"🌐 Frontend disponible en http://{settings.host}:{settings.port}/web")  # ← NUEVO
    yield
    # Shutdown
    print("👋 Cerrando aplicación")

app = FastAPI(
    title="API de Gestión de Perfiles de Usuario",
    description="API REST con interfaz web para gestión de perfiles",
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

# Montar archivos estáticos
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Incluir rutas
# app.include_router(user_router)
app.include_router(user_web_router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "API de Gestión de Perfiles de Usuario",
        "version": "1.0.0",
        "api_documentation": "/docs",
        "web_interface": "/web",  # ← NUEVO
        "endpoints": {
            "api_create_user": "POST /api/users/",
            "api_get_profile": "GET /api/users/{user_id}/profile",
            "api_update_profile": "PUT /api/users/{user_id}/profile",
            "api_delete_account": "DELETE /api/users/{user_id}/account",
            "web_interface": "GET /web",  # ← NUEVO
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