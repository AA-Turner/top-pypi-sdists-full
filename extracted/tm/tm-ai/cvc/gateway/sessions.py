"""
Sessions router — /api/sessions/* (vendored SessionDB-backed)
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger("cvc.gateway.sessions")

router = APIRouter()


class CreateSessionBody(BaseModel):
    title: str | None = None
    workspace_path: str | None = None


@router.get("/sessions")
async def list_sessions(limit: int = 50):
    from cvc.gateway.agent import get_session_db
    db = get_session_db()
    if db is None:
        return {"sessions": []}
    try:
        # SessionDB exposes list_sessions; signature varies, handle both
        if hasattr(db, "list_sessions"):
            sessions = db.list_sessions(limit=limit)
        elif hasattr(db, "get_recent_sessions"):
            sessions = db.get_recent_sessions(limit=limit)
        else:
            return {"sessions": []}
        return {"sessions": [_session_to_dict(s) for s in (sessions or [])]}
    except Exception as e:
        logger.exception("list_sessions failed")
        return {"sessions": [], "error": str(e)}


@router.post("/sessions")
async def create_session(body: CreateSessionBody):
    from cvc.gateway.agent import get_session_db
    db = get_session_db()
    session_id = f"cvc_{uuid.uuid4().hex[:16]}"
    title = body.title or "New chat"
    if db is not None:
        try:
            if hasattr(db, "create_session"):
                db.create_session(session_id=session_id, title=title)
        except Exception as e:
            logger.debug("create_session: %s", e)
    return {"session": {"id": session_id, "title": title, "workspace_path": body.workspace_path}}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    from cvc.gateway.agent import get_session_db
    db = get_session_db()
    if db is None:
        raise HTTPException(status_code=404, detail="session store unavailable")
    if hasattr(db, "get_session"):
        s = db.get_session(session_id)
    elif hasattr(db, "get"):
        s = db.get(session_id)
    else:
        raise HTTPException(status_code=404, detail="session lookup not supported")
    if not s:
        raise HTTPException(status_code=404, detail="session not found")
    return {"session": _session_to_dict(s)}


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str, limit: int = 200):
    from cvc.gateway.agent import get_session_db
    db = get_session_db()
    if db is None:
        return {"messages": []}
    if hasattr(db, "get_messages"):
        msgs = db.get_messages(session_id, limit=limit)
    elif hasattr(db, "get_session_messages"):
        msgs = db.get_session_messages(session_id, limit=limit)
    else:
        return {"messages": []}
    return {"messages": list(msgs or [])}


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    from cvc.gateway.agent import get_session_db
    db = get_session_db()
    if db is not None and hasattr(db, "delete_session"):
        try:
            db.delete_session(session_id)
        except Exception as e:
            logger.debug("delete_session: %s", e)
    return {"ok": True}


def _session_to_dict(s: Any) -> dict:
    if isinstance(s, dict):
        return s
    if hasattr(s, "__dict__"):
        return vars(s)
    return {"id": str(s)}
