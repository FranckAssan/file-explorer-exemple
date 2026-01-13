import os

from fastapi import APIRouter
from starlette.responses import FileResponse

router = APIRouter(
    prefix="/download",
    tags=["download"]
)

BASE_FOLDER = os.getenv("BASE_FOLDER")

@router.get("/")
async def download_file(path: str, new_name: str | None = None):
    if not path.startswith(BASE_FOLDER):
        return {"error": "Access Denied"}
    # Security check: Ensure the file exists
    if os.path.exists(path) and os.path.isfile(path):
        filename = os.path.basename(path)
        if new_name is not None:
            filename=os.path.basename(new_name)
        return FileResponse(path=path, filename=filename)
    return {"error": "File not found"}