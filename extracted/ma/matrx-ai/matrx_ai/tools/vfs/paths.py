from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

InodeType = Literal["file", "dir", "symlink"]


class Inode(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    id: str
    workspace_id: str
    parent_id: str | None
    name: str
    type: InodeType
    mode: int = 0o644
    uid: int = 0
    gid: int = 0
    size: int = 0
    symlink_target: str | None = None
    content_id: str | None = None
    ctime: datetime | None = None
    mtime: datetime | None = None
    atime: datetime | None = None


def is_absolute(path: str) -> bool:
    return path.startswith("/")


def normalize(path: str) -> str:
    if not path:
        return "/"
    absolute = path.startswith("/")
    parts = path.split("/")
    stack: list[str] = []
    for part in parts:
        if part == "" or part == ".":
            continue
        if part == "..":
            if stack:
                stack.pop()
            continue
        stack.append(part)
    if absolute:
        return "/" + "/".join(stack) if stack else "/"
    return "/".join(stack) if stack else "."


def split_components(path: str) -> list[str]:
    norm = normalize(path)
    if norm == "/" or norm == ".":
        return []
    if norm.startswith("/"):
        norm = norm[1:]
    return norm.split("/") if norm else []


def dirname(path: str) -> str:
    norm = normalize(path)
    if norm == "/":
        return "/"
    idx = norm.rfind("/")
    if idx <= 0:
        return "/"
    return norm[:idx]


def basename(path: str) -> str:
    norm = normalize(path)
    if norm == "/":
        return ""
    idx = norm.rfind("/")
    return norm[idx + 1 :] if idx >= 0 else norm


def join(*parts: str) -> str:
    if not parts:
        return "/"
    result = ""
    for part in parts:
        if not part:
            continue
        if part.startswith("/"):
            result = part
        elif not result:
            result = part
        else:
            result = result.rstrip("/") + "/" + part
    return normalize(result) if result else "/"
