import mimetypes
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status

from src.core.config import settings
from src.models import StoredFile
from src.repositories.file import FileRepository
from src.tasks import scan_file_for_threats


class FileService:
    def __init__(self, file_repo: FileRepository):
        self.file_repo = file_repo

    async def list_files(self) -> list[StoredFile]:
        return await self.file_repo.get_all()

    async def get_file(self, file_id: str) -> StoredFile:
        file_item = await self.file_repo.get_by_id(file_id)
        if not file_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="File not found"
            )
        return file_item

    async def create_file(self, title: str, upload_file: UploadFile) -> StoredFile:
        # TODO: (Спринт 2) Переписать чтение в память на асинхронную потоковую запись (chunking)
        content = await upload_file.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="File is empty"
            )

        file_id = str(uuid4())
        suffix = Path(upload_file.filename or "").suffix
        stored_name = f"{file_id}{suffix}"
        stored_path = settings.STORAGE_DIR / stored_name
        
        # Сохранение на диск
        stored_path.write_bytes(content)

        mime_type = (
            upload_file.content_type 
            or mimetypes.guess_type(stored_name)[0] 
            or "application/octet-stream"
        )

        file_item = StoredFile(
            id=file_id,
            title=title,
            original_name=upload_file.filename or stored_name,
            stored_name=stored_name,
            mime_type=mime_type,
            size=len(content),
            processing_status="uploaded",
        )
        
        # Сохраняем в БД через репозиторий
        created_file = await self.file_repo.create(file_item)
        
        # Запускаем фоновую задачу Celery
        scan_file_for_threats.delay(created_file.id)
        
        return created_file

    async def update_file(self, file_id: str, title: str) -> StoredFile:
        file_item = await self.get_file(file_id)
        file_item.title = title
        return await self.file_repo.update(file_item)

    async def delete_file(self, file_id: str) -> None:
        file_item = await self.get_file(file_id)
        
        stored_path = settings.STORAGE_DIR / file_item.stored_name
        if stored_path.exists():
            stored_path.unlink()
            
        await self.file_repo.delete(file_item)
        
    async def get_file_path_for_download(self, file_id: str) -> tuple[StoredFile, Path]:
        file_item = await self.get_file(file_id)
        stored_path = settings.STORAGE_DIR / file_item.stored_name
        if not stored_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Stored file not found"
            )
        return file_item, stored_path