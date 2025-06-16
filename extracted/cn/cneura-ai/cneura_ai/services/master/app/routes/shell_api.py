import os
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

from cneura_ai.shell import ShellSessionManager
from cneura_ai.logger import logger
from app.dependencies import get_db_hub, DatabaseHub

router = APIRouter(prefix="/shell", tags=["Shell"])


class CommandRequest(BaseModel):
    agent_id: str
    command: List[str]


class SessionRequest(BaseModel):
    agent_id: str


class FileRequest(BaseModel):
    agent_id: str
    path: str

class FolderRequest(BaseModel):
    agent_id: str
    container_path: str


async def get_shell_manager(db_hub: DatabaseHub = Depends(get_db_hub)) -> ShellSessionManager:
    await db_hub.load_config()
    remote_url = db_hub.config.get("REMOTE_URL")
    mongo_uri = db_hub.config.get("MONGO_URI")

    if not remote_url or not mongo_uri:
        raise HTTPException(status_code=500, detail="REMOTE_URL or MONGO_URI missing in DB config")

    return ShellSessionManager(remote_url=remote_url, mongo_uri=mongo_uri)


@router.post("/session/create")
def create_session(
    request: SessionRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        manager.get_session(request.agent_id)
        return {"message": f"Session created or resumed for agent {request.agent_id}"}
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/stop")
def stop_session(
    request: SessionRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        manager.stop_session(request.agent_id)
        return {"message": f"Session stopped for agent {request.agent_id}"}
    except Exception as e:
        logger.error(f"Error stopping session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/command/run")
def run_command(
    request: CommandRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        result = manager.run_command(request.agent_id, request.command)
        return result
    except Exception as e:
        logger.error(f"Error running command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/file/get")
def get_file(
    request: FileRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        session = manager.get_session(request.agent_id)
        file_data = session.get_file(request.path)

        if file_data is None:
            raise HTTPException(status_code=404, detail="File not found in container")

        # Save the archive to media folder
        safe_name = request.path.strip("/").replace("/", "_")
        media_path = f"media/shell/{request.agent_id}_{safe_name}.tar"

        with open(media_path, "wb") as f:
            f.write(file_data)

        download_url = f"/media/shell/{request.agent_id}_{safe_name}.tar"

        return {
            "message": "File saved",
            "download_url": download_url
        }

    except Exception as e:
        logger.error(f"Error getting file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    

@router.post("/folder/get")
def get_folder(
    request: FolderRequest,
    manager: ShellSessionManager = Depends(get_shell_manager),
):
    try:
        session = manager.get_session(request.agent_id)

        # Generate safe local path
        folder_name = request.container_path.strip("/").replace("/", "_")
        local_dir = f"media/shell"
        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, f"{request.agent_id}_{folder_name}.tar")

        # Download archive from container and save
        result = session.get_folder(request.container_path, local_path)

        if not os.path.exists(local_path):
            raise HTTPException(status_code=500, detail="Folder not downloaded correctly")

        download_url = f"/media/shell/{os.path.basename(local_path)}"

        return {
            "message": "Folder saved as archive",
            "download_url": download_url
        }

    except Exception as e:
        logger.error(f"Error getting folder: {e}")
        raise HTTPException(status_code=500, detail=str(e))
