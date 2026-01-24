import os
from datetime import datetime
from sqlalchemy import func, Column, DateTime # ForeignKey, String
# from sqlalchemy import create_engine # from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship
from sqlmodel import Field, Relationship, SQLModel, create_engine, Session, select, Field

from alm.model import settings


class LloFile(SQLModel, table=True):
    __tablename__ = "llo_file"
    id: int | None = Field(default=None, primary_key=True)
    size: int
    logical_name: str
    physical_path: str = Field(exclude=True)
    download_count: int = 0
    created_at: datetime = Field(sa_column=Column(DateTime(), server_default=func.now()))

    user_id: int | None = Field(default=None)

    def __repr__(self) -> str:
        return f"LloFile(id={self.id!r}, logical_name={self.logical_name!r})"


# create_async_engine(f"sqlite+aiosqlite:///{os.path.join(settings.workspace, 'llo.db')}", echo=True)
engine = create_engine(f"sqlite:///{os.path.join(settings.workspace, 'llo.db')}", echo=False, connect_args={"check_same_thread": False})
