from pathlib import Path

from pydantic import BaseModel


class SkillFile(BaseModel):
    title: str
    path: Path
    content: str


class DiscoveredSkill(BaseModel):
    path: str
    name: str
    description: str | None = None
    files: list[SkillFile] = []
