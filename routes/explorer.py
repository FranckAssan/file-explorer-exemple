import os

from dotenv import load_dotenv
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter(prefix="/explore", tags=["explore"])

templates = Jinja2Templates(directory="templates")
load_dotenv()
BASE_FOLDER = os.getenv("BASE_FOLDER")

@router.get("/", response_class=HTMLResponse)
async def explore(request: Request, path: str):
    """Detailed file navigation for a selected computer."""
    try:
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

        # Stop 'Back' button from going above the Network Root for security
        if path.rstrip(os.sep) == f'{BASE_FOLDER}'.rstrip(os.sep):
            parent_dir = None

        return templates.TemplateResponse("explorer.html", {
            "request": request,
            "items": items,
            "current_path": path,
            "parent_dir": parent_dir
        })
    except Exception as e:
        return HTMLResponse(content=f"Error: {e}", status_code=400)