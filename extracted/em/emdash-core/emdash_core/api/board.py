"""API endpoints for board persistence via webhooks.

This module provides REST endpoints for saving and loading kanban boards.
Board changes are dispatched via webhooks to all registered consumers.
"""

from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..multiuser.webhooks import get_webhook_registry
from ..utils.logger import log

router = APIRouter(prefix="/board", tags=["board"])


# ─────────────────────────────────────────────────────────────
# Request/Response Models
# ─────────────────────────────────────────────────────────────


class TaskData(BaseModel):
    """Task data in a kanban board."""

    id: str
    title: str
    description: str = ""
    column: str  # 'todo', 'design-review', 'in-progress', 'in-pr'
    created_at: str
    updated_at: str
    labels: list[str] = []
    assignee: str = ""
    priority: str = "medium"  # 'low', 'medium', 'high'
    spec_path: str = ""
    plan: str = ""
    ai_status: str = "idle"  # 'idle', 'generating_spec', etc.


class SaveBoardRequest(BaseModel):
    """Request to save a kanban board."""

    board_id: str = Field(..., description="Unique board identifier (derived from project root)")
    project_root: str = Field(..., description="Project root path")
    tasks: list[TaskData] = Field(default_factory=list, description="List of tasks")
    timestamp: Optional[str] = Field(None, description="Save timestamp")
    user_id: Optional[str] = Field(None, description="User saving the board")


class SaveBoardResponse(BaseModel):
    """Response after saving a board."""

    success: bool
    board_id: str
    task_count: int
    timestamp: str


class BoardResponse(BaseModel):
    """Response with board data."""

    board_id: str
    project_root: Optional[str]
    tasks: list[dict[str, Any]]
    last_updated: Optional[str]


# In-memory board state (for development/testing)
# In production, boards are persisted by webhook consumers
_board_cache: dict[str, dict[str, Any]] = {}


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────


@router.post("/save", response_model=SaveBoardResponse)
async def save_board(request: SaveBoardRequest):
    """Save board data and dispatch webhook to all consumers.

    This endpoint:
    1. Accepts board data from the desktop app
    2. Caches it in memory for quick retrieval
    3. Dispatches a 'board.saved' webhook to all registered consumers
    4. Consumers persist the data to their preferred storage (local files, database, etc.)
    """
    timestamp = request.timestamp or datetime.utcnow().isoformat()

    # Cache board data in memory
    _board_cache[request.board_id] = {
        "board_id": request.board_id,
        "project_root": request.project_root,
        "tasks": [t.model_dump() for t in request.tasks],
        "last_updated": timestamp,
        "user_id": request.user_id,
    }

    # Dispatch webhook to all registered consumers
    registry = get_webhook_registry()
    await registry.dispatch(
        "board.saved",
        {
            "board_id": request.board_id,
            "project_root": request.project_root,
            "tasks": [t.model_dump() for t in request.tasks],
            "timestamp": timestamp,
        },
        origin_user_id=request.user_id,
    )

    log.info(f"Board saved: {request.board_id} with {len(request.tasks)} tasks")

    return SaveBoardResponse(
        success=True,
        board_id=request.board_id,
        task_count=len(request.tasks),
        timestamp=timestamp,
    )


@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(board_id: str):
    """Get board data from cache.

    Note: This returns cached data from memory. The authoritative
    source is the consumer's persistence layer (e.g., local JSON files).
    """
    board = _board_cache.get(board_id)

    if not board:
        # Return empty board if not found (consumer handles persistence)
        return BoardResponse(
            board_id=board_id,
            project_root=None,
            tasks=[],
            last_updated=None,
        )

    return BoardResponse(
        board_id=board["board_id"],
        project_root=board.get("project_root"),
        tasks=board.get("tasks", []),
        last_updated=board.get("last_updated"),
    )


@router.delete("/{board_id}")
async def delete_board(board_id: str, user_id: Optional[str] = None):
    """Delete a board from cache and notify consumers.

    This dispatches a 'board.deleted' webhook so consumers can
    clean up their persistence layer.
    """
    if board_id in _board_cache:
        del _board_cache[board_id]

    # Dispatch webhook
    registry = get_webhook_registry()
    await registry.dispatch(
        "board.deleted",
        {
            "board_id": board_id,
            "timestamp": datetime.utcnow().isoformat(),
        },
        origin_user_id=user_id,
    )

    log.info(f"Board deleted: {board_id}")

    return {"success": True, "board_id": board_id}


@router.get("/")
async def list_boards():
    """List all boards in cache.

    Returns a summary of all cached boards. Useful for debugging
    and admin purposes.
    """
    return {
        "boards": [
            {
                "board_id": board_id,
                "task_count": len(board.get("tasks", [])),
                "last_updated": board.get("last_updated"),
            }
            for board_id, board in _board_cache.items()
        ],
        "total": len(_board_cache),
    }
