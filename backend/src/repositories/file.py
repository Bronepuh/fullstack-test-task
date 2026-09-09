from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import StoredFile

class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[StoredFile]:
        # Оптимизация N+1: сразу подгружаем связанные алерты
        result = await self.session.execute(
            select(StoredFile)
            .options(selectinload(StoredFile.alerts))
            .order_by(StoredFile.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, file_id: str) -> StoredFile | None:
        return await self.session.get(StoredFile, file_id)

    async def create(self, file_item: StoredFile) -> StoredFile:
        self.session.add(file_item)
        await self.session.commit()
        await self.session.refresh(file_item)
        return file_item

    async def update(self, file_item: StoredFile) -> StoredFile:
        await self.session.commit()
        await self.session.refresh(file_item)
        return file_item

    async def delete(self, file_item: StoredFile) -> None:
        await self.session.delete(file_item)
        await self.session.commit()