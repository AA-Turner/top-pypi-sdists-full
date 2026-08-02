"""Local storage helpers for the NX CLI.

This module keeps artifact saving and session/training exports self-contained
inside the installed CLI package. It does not require backend APIs.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import re
import uuid
from pathlib import Path


_HOME = Path.home()
_NX_DIR = _HOME / ".nx"
_ARTIFACT_DIR = _NX_DIR / "artifacts"
_SESSION_LOG_DIR = _NX_DIR / "session-logs"
_TRAINING_DIR = _NX_DIR / "training-candidates"


def _ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def _utc_timezone():
    return getattr(_dt, "UTC", _dt.timezone.utc)


def _timestamp() -> str:
    return _dt.datetime.now(_utc_timezone()).strftime("%Y%m%d-%H%M%S")


def _utc_iso() -> str:
    return _dt.datetime.now(_utc_timezone()).isoformat()


def _safe_slug(value, fallback: str) -> str:
    text = (value or "").strip().lower()
    slug = re.sub(r"[^a-z0-9._-]+", "-", text).strip("-._")
    return slug or fallback


def _user_partition(user_id) -> str:
    """Collision-resistant per-user directory name. A bare slug can collide
    (e.g. 'a/b' and 'a:b' both → 'a-b'), letting one user's artifacts/session
    logs/training data land in another's directory. We append a short, stable
    hash of the RAW user_id so distinct ids never share a partition, while
    keeping a readable slug prefix."""
    import hashlib
    raw = (user_id or "anonymous")
    slug = _safe_slug(user_id, "anonymous")
    digest = hashlib.sha256(str(raw).encode("utf-8")).hexdigest()[:12]
    return f"{slug}-{digest}"


def _safe_extension(extension: str | None, fallback: str = "txt") -> str:
    text = (extension or fallback).strip().lower().lstrip(".")
    text = re.sub(r"[^a-z0-9]+", "", text)
    return text or fallback


def save_artifact(user_id, user_jwt, content, filename=None, extension="txt"):
    """Persist an artifact to ~/.nx/artifacts and return path metadata."""
    del user_jwt
    artifact_dir = _ensure_dir(_ARTIFACT_DIR / _user_partition(user_id))
    stem = _safe_slug(filename, "artifact")
    ext = _safe_extension(extension)
    basename = f"{stem}-{_timestamp()}.{ext}"
    path = artifact_dir / basename
    path.write_text(content or "", encoding="utf-8")
    return {
        "id": str(uuid.uuid4()),
        "path": str(path),
        "url": path.resolve().as_uri(),
        "filename": basename,
        "created_at": _utc_iso(),
    }


def save_session_log(session_id, user_id, messages, metadata=None):
    """Persist the full session log to ~/.nx/session-logs."""
    session_dir = _ensure_dir(_SESSION_LOG_DIR / _user_partition(user_id))
    world = _safe_slug((metadata or {}).get("world"), "cowork")
    basename = f"{world}-{session_id}.json"
    path = session_dir / basename
    payload = {
        "session_id": session_id,
        "user_id": user_id,
        "metadata": metadata or {},
        "messages": messages or [],
        "saved_at": _utc_iso(),
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return {
        "path": str(path),
        "url": path.resolve().as_uri(),
        "message_count": len(messages or []),
    }


def export_training_candidates(messages, session_id, user_id, world):
    """Export adjacent user/assistant trainable pairs as JSONL."""
    pairs = []
    pending_user = None

    for message in messages or []:
        if not isinstance(message, dict):
            continue
        if not message.get("trainable", True):
            if message.get("role") == "user":
                pending_user = None
            continue

        role = message.get("role")
        if role == "user":
            pending_user = message
            continue

        if role == "assistant" and pending_user:
            pairs.append(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": pending_user.get("content", ""),
                        },
                        {
                            "role": "assistant",
                            "content": message.get("content", ""),
                        },
                    ],
                    "metadata": {
                        "session_id": session_id,
                        "user_id": user_id,
                        "world": world,
                        "user_model_used": pending_user.get("model_used"),
                        "assistant_model_used": message.get("model_used"),
                        "exported_at": _utc_iso(),
                    },
                }
            )
            pending_user = None

    if not pairs:
        return {"skipped": True, "pairs_exported": 0}

    training_dir = _ensure_dir(_TRAINING_DIR / _user_partition(user_id))
    basename = f"{_safe_slug(world, 'cowork')}-{session_id}.jsonl"
    path = training_dir / basename
    with path.open("w", encoding="utf-8") as handle:
        for pair in pairs:
            handle.write(json.dumps(pair, ensure_ascii=True))
            handle.write("\n")

    return {
        "skipped": False,
        "pairs_exported": len(pairs),
        "path": str(path),
        "url": path.resolve().as_uri(),
    }
