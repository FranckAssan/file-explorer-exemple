import os
from pathlib import Path

from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from core.config import AppConfig, get_settings

router = APIRouter(prefix="/explore", tags=["explore"])

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def explore(request: Request, path: str, config: AppConfig = Depends(
    get_settings)):
    """Detailed file navigation for a selected computer."""

    path = Path(path).resolve()
    rootFolder = config.folders[0].path.resolve()
    try:
        path.relative_to(rootFolder)
        items = []
        for item in os.listdir(path):
            full_item_path = os.path.join(path, item)
            items.append({
                "name": item,
                "path": full_item_path,
                "is_dir": os.path.isdir(full_item_path)
            })

        items.sort(key=lambda x: not x["is_dir"])
        parent_dir = os.path.dirname(path)


        return templates.TemplateResponse("explorer.html", {
            "request": request,
            "items": items,
            "current_path": path,
            "parent_dir": parent_dir
        })
    except ValueError:
        print(f"Impossible to navigate beyond Root Folder! PathRequested: {path}")
        return RedirectResponse("/")