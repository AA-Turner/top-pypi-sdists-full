from fastapi import FastAPI
from app.routes import (
    config_api,
    agent_api,
    credential_api,
    memory_api,
    research_api,
    shell_api,
    tool_api,
    upload_api,
    log_api,
    queue_api,
    auth_api,
)
from fastapi.staticfiles import StaticFiles
from app.db.init_db import init_db

app = FastAPI(
    title="Cneura API",
    description="",
    version="1.0.0",
    contact={
        "name": "Savindu Shehan",
        "email": "shehandezen@gmail.com",
        "url": "https://cneura.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.mount("/media", StaticFiles(directory="media"), name="media")

@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(config_api.router)
app.include_router(agent_api.router)
app.include_router(credential_api.router)
app.include_router(memory_api.router)
app.include_router(research_api.router)
app.include_router(shell_api.router)
app.include_router(tool_api.router)
app.include_router(upload_api.router)
app.include_router(log_api.router)
app.include_router(queue_api.router)
app.include_router(auth_api.router)

