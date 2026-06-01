from pathlib import Path

from pydantic import BaseModel

from runlayer_cli.skills.models import DiscoveredSkill


class ServerConnector(BaseModel):
    server_id: str
    entry_name: str


class DiscoveredPlugin(BaseModel):
    root: Path
    path: str
    name: str
    description: str | None = None
    version: str | None = None
    identifier: str | None = None
    manifest_warnings: list[str] = []
    mcp_warnings: list[str] = []
    server_connectors: list[ServerConnector] = []
    skills: list[DiscoveredSkill] = []
