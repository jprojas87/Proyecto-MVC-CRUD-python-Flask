from pydantic_settings import BaseSettings
from pathlib import Path

# Obtener la ruta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    database_url: str
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = BASE_DIR / ".env"  # Busca .env en la raíz del proyecto

settings = Settings()