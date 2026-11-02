"""SSE frame fields for streaming parsing."""

from __future__ import annotations

from typing import TypedDict


class SseFields(TypedDict):
    """Accumulated identifier, event, and data lines of one frame."""

    id: str | None
    event: str
    data: list[str]
