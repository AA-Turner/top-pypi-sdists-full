"""Shared MCP lookup wire types."""

from __future__ import annotations

from typing import TypedDict


class MCPServer(TypedDict, total=False):
    name: str
    url: str
    command: str
    source: str
