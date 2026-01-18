from pathlib import Path

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from core.config import AppConfig, get_settings, Folder

router = APIRouter(prefix="", tags=["dashboard"])


templates = Jinja2Templates(directory="templates")


def buildPath(folders: list[Folder]):
    for folder in folders:
        if isinstance(folder.path, list):
            folderPath = Path(*folder.path)
            folder.path.clear()
            folder.path = folderPath


@router.get("/", response_class=HTMLResponse)
async def dashboard(
        request: Request,
        config : AppConfig = Depends(get_settings)
):

    if len(config.folders) == 0:
        return RuntimeError("Impossible to access Shared folders")
    else:
        buildPath(config.folders)
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "folders": config.folders
        })
