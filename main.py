import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

BASE_FOLDER = r"/home/franck/Bureau/SharedNetworkFolder"


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Initial landing page showing folders as cards."""
    computers = []
    try:
        # Only list directories in the root
        for name in os.listdir(BASE_FOLDER):
            full_path = os.path.join(BASE_FOLDER, name)
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


@app.get("/explore", response_class=HTMLResponse)
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
        if path.rstrip(os.sep) == BASE_FOLDER.rstrip(os.sep):
            parent_dir = None

        return templates.TemplateResponse("explorer.html", {
            "request": request,
            "items": items,
            "current_path": path,
            "parent_dir": parent_dir
        })
    except Exception as e:
        return HTMLResponse(content=f"Error: {e}", status_code=400)

@app.get("/download")
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


