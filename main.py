from fastapi import FastAPI

from routes import dashboard, explorer, download_file

app = FastAPI()

app.include_router(dashboard.router)
app.include_router(explorer.router)
app.include_router(download_file.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
