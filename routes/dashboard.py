import os

from dotenv import load_dotenv
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter(prefix="", tags=["dashboard"])


templates = Jinja2Templates(directory="templates")
load_dotenv()
BASE_FOLDER = os.getenv("BASE_FOLDER")

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    computers = []
    try:
        # Only list directories in the root
        for name in os.listdir(f'{BASE_FOLDER}'):
            full_path = os.path.join(f'{BASE_FOLDER}', name)
            if os.path.isdir(full_path):
                computers.append({
                    "name": name,
                    "path": full_path
                })
    except Exception as e:
        return HTMLResponse(content=f"Error accessing Network Root: {e}",
                            status_code=500)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "computers": computers
    })
