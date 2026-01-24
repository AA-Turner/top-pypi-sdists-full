import os
import uuid
import shutil
from typing import Sequence
from pathlib import Path
from fastapi import APIRouter, Request, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from alm.model import settings
from alm.orm import engine, LloFile

# 기본 제공 API
file_router = APIRouter(prefix="/alm/file")


@file_router.get("")
async def retrieve_files(request: Request, offset=0, limit=10) -> Sequence[LloFile]:
    token = request.state.token
    with Session(engine) as session:
        statement = select(LloFile).where(LloFile.user_id == token['user']['id']).offset(offset).limit(limit)
        files = session.exec(statement).all()
        return files


@file_router.post("")
async def save_file(request: Request, file: UploadFile = File(...)) -> LloFile:
    token = request.state.token
    with Session(engine) as session:
        save_dir = os.path.join("_contents", str(token['user']['id']), "file")
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        relative_path = os.path.join(save_dir, str(uuid.uuid4()))
        with open(os.path.join(settings.workspace, relative_path), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        new_file = LloFile(user_id=token['user']['id'], size=file.size, logical_name=file.filename, physical_path=relative_path)
        session.add(new_file)
        session.commit()
        return new_file


@file_router.get("/{file_id}")
async def retrieve_file(request: Request, file_id: int) -> LloFile:
    token = request.state.token
    with Session(engine) as session:
        statement = select(LloFile).where(LloFile.user_id == token['user']['id'], LloFile.id == file_id)
        file = session.exec(statement).first()
        return file


@file_router.delete("/{file_id}")
async def delete_file(request: Request, file_id: int) -> LloFile:
    token = request.state.token
    with Session(engine) as session:
        statement = select(LloFile).where(LloFile.user_id == token['user']['id'], LloFile.id == file_id)
        file = session.exec(statement).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        physical_path = os.path.join(settings.workspace, file.physical_path)
        if os.path.exists(physical_path):
            os.remove(physical_path)

        session.delete(file)
        session.commit()
        return file


@file_router.get("/{file_id}/download")
async def download_file(request: Request, file_id: int) -> FileResponse:
    token = request.state.token
    with Session(engine) as session:
        statement = select(LloFile).where(LloFile.user_id == token['user']['id'], LloFile.id == file_id)
        file = session.exec(statement).first()
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        physical_path = os.path.join(settings.workspace, file.physical_path)
        if not os.path.exists(physical_path):
            raise HTTPException(status_code=404, detail="File not found")
        file.download_count += 1
        session.add(file)
        session.commit()
        return FileResponse(physical_path, media_type="application/octet-stream", filename=file.logical_name)
