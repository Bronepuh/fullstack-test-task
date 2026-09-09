from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_session
from src.repositories.alert import AlertRepository
from src.repositories.file import FileRepository
from src.services.alert import AlertService
from src.services.file import FileService


def get_file_repository(session: AsyncSession = Depends(get_db_session)) -> FileRepository:
    return FileRepository(session)


def get_alert_repository(session: AsyncSession = Depends(get_db_session)) -> AlertRepository:
    return AlertRepository(session)


def get_file_service(repo: FileRepository = Depends(get_file_repository)) -> FileService:
    return FileService(repo)


def get_alert_service(repo: AlertRepository = Depends(get_alert_repository)) -> AlertService:
    return AlertService(repo)