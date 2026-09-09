import os
from pathlib import Path

class Config:
    # Путь до корня папки backend
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    STORAGE_DIR = BASE_DIR / "storage" / "files"
    
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "backend-db")
    PGPORT = os.environ.get("PGPORT", "5433")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "test")
    
    DB_URL = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{PGPORT}/{POSTGRES_DB}"
    )
    REDIS_URL = os.environ.get("REDIS_URL", "redis://backend-redis:6379/0")

settings = Config()
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)