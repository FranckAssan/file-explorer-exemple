import os
from shlex import join

from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from core.config import AppConfig, get_settings

router = APIRouter(
    prefix="/download",
    tags=["download"]
)


@router.get("/")
async def download_file(
        path: str, new_name: str | None = None,
        config: AppConfig = Depends(get_settings)
):
    file_src_path = join(path.split('/')[1:4])
    is_path_valide = False

    for f in config.folders:
        base_path = join( str(f.path.resolve()).split('/')[1:4] )
        if base_path.__eq__(file_src_path):
            is_path_valide = True

    # Security check: Ensure the file exists
    if os.path.exists(path) and os.path.isfile(path):
        print(f'File exit: {path}')
        if not is_path_valide:
            return f"Acces to {path} not Allowed"
        filename = os.path.basename(path)
        if new_name is not None:
            filename=os.path.basename(new_name)
        return FileResponse(path=path, filename=filename)

    return {"error": "File not found"}