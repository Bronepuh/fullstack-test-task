from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import FileResponse

from src.api.dependencies import get_file_service
from src.schemas import FileItem, FileUpdate
from src.services.file import FileService

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("", response_model=list[FileItem])
async def list_files_view(file_service: FileService = Depends(get_file_service)):
    return await file_service.list_files()


@router.post("", response_model=FileItem, status_code=status.HTTP_201_CREATED)
async def create_file_view(
    title: str = Form(...),
    file: UploadFile = File(...),
    file_service: FileService = Depends(get_file_service)
):
    return await file_service.create_file(title=title, upload_file=file)


@router.get("/{file_id}", response_model=FileItem)
async def get_file_view(
    file_id: str, 
    file_service: FileService = Depends(get_file_service)
):
    return await file_service.get_file(file_id)


@router.patch("/{file_id}", response_model=FileItem)
async def update_file_view(
    file_id: str,
    payload: FileUpdate,
    file_service: FileService = Depends(get_file_service)
):
    return await file_service.update_file(file_id=file_id, title=payload.title)


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file_view(
    file_id: str, 
    file_service: FileService = Depends(get_file_service)
):
    await file_service.delete_file(file_id)


@router.get("/{file_id}/download")
async def download_file(
    file_id: str, 
    file_service: FileService = Depends(get_file_service)
):
    file_item, stored_path = await file_service.get_file_path_for_download(file_id)
    return FileResponse(
        path=stored_path,
        media_type=file_item.mime_type,
        filename=file_item.original_name,
    )