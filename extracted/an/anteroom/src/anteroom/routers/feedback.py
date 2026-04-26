"""Feedback submission API endpoint."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

router = APIRouter(tags=["feedback"])


class FeedbackRequest(BaseModel):
    description: str = Field(..., min_length=1, max_length=4096)
    include_history: bool = False
    conversation_id: str | None = None
    space_id: str | None = None

    @field_validator("description", mode="before")
    @classmethod
    def strip_description(cls, v: Any) -> Any:
        if isinstance(v, str):
            v = v.strip()
        return v


def _public_feedback_result(result: dict[str, Any]) -> dict[str, Any]:
    """Return an API-safe feedback result without filesystem or exception details."""
    status = str(result.get("status", "failed"))
    reporter = str(result.get("reporter", ""))
    if status == "sent":
        return {"status": "sent", "reporter": reporter}
    if status == "saved_locally":
        return {
            "status": "saved_locally",
            "reporter": reporter or "local",
            "message": "Feedback bundle saved locally on the server.",
        }
    return {
        "status": "failed",
        "reporter": reporter,
        "error": "Feedback submission failed. Check server logs for details.",
    }


@router.post("/feedback")
async def submit_feedback_endpoint(body: FeedbackRequest, request: Request) -> dict[str, Any]:
    ct = request.headers.get("content-type", "")
    if not ct.startswith("application/json"):
        raise HTTPException(status_code=415, detail="Content-Type must be application/json")

    config = request.app.state.config
    db = request.app.state.db
    tool_registry = getattr(request.app.state, "tool_registry", None)
    mcp_manager = getattr(request.app.state, "mcp_manager", None)

    from ..services import storage as _storage

    conversation: dict[str, Any] | None = None
    if body.conversation_id:
        try:
            conversation = _storage.get_conversation(db, body.conversation_id)
        except Exception:
            logger.exception("feedback: could not verify conversation")
            raise HTTPException(status_code=500, detail="Could not verify conversation") from None

    active_space: dict[str, Any] | None = None
    space_id = body.space_id
    if not space_id and conversation:
        space_id = conversation.get("space_id")
    if space_id:
        try:
            from ..services.space_storage import get_space

            active_space = get_space(db, space_id)
        except Exception:
            pass

    # Optionally fetch conversation history
    conversation_messages: list[dict[str, Any]] | None = None
    if body.include_history:
        if not body.conversation_id:
            raise HTTPException(status_code=400, detail="conversation_id required when include_history is true")
        if conversation is None:
            raise HTTPException(status_code=404, detail="conversation not found")
        try:
            msgs = _storage.list_messages(db, body.conversation_id)
            conversation_messages = [dict(m) for m in (msgs or [])]
        except Exception:
            logger.exception("feedback: could not fetch conversation messages")
            raise HTTPException(status_code=500, detail="Could not fetch conversation history") from None

    from ..services.feedback import submit_feedback

    result = await submit_feedback(
        body.description,
        config,
        db,
        conversation_id=body.conversation_id,
        conversation_messages=conversation_messages,
        active_space=active_space,
        tool_registry=tool_registry,
        mcp_manager=mcp_manager,
    )
    return _public_feedback_result(result)
