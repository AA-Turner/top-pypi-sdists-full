"""Statistics endpoints for user activity and token usage."""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/stats", tags=["stats"])


# ============================================================================
# Data Models
# ============================================================================

class UserStats(BaseModel):
    """Aggregated user statistics."""
    total_sessions: int
    total_tokens: int
    input_tokens: int
    output_tokens: int
    thinking_tokens: int
    estimated_cost: float = 0.0
    cost_formatted: str = "$0.0000"
    first_seen: Optional[str] = None
    last_active: Optional[str] = None
    model_usage: list[dict] = []


class SessionInfo(BaseModel):
    """Information about a single session."""
    session_id: str
    created_at: Optional[str] = None
    last_active: Optional[str] = None
    token_count: int
    checkpoint_count: int
    model: Optional[str] = None


class SessionList(BaseModel):
    """List of sessions with pagination."""
    sessions: list[SessionInfo]
    total: int


class TokenBreakdown(BaseModel):
    """Token usage breakdown."""
    total: int
    input: int
    output: int
    thinking: int


# ============================================================================
# Helper Functions
# ============================================================================

def _get_checkpoints_dir() -> Path:
    """Get the checkpoints directory."""
    # Check for per-repo checkpoints in .emdash/checkpoints
    checkpoints_dir = Path(".emdash/checkpoints")
    if not checkpoints_dir.exists():
        # Fall back to home directory for legacy/global checkpoints
        checkpoints_dir = Path.home() / ".emdash" / "checkpoints"
    return checkpoints_dir


def _get_sessions_dir() -> Path:
    """Get the sessions directory."""
    sessions_dir = Path(".emdash/sessions")
    if not sessions_dir.exists():
        sessions_dir = Path.home() / ".emdash" / "sessions"
    return sessions_dir


def _parse_timestamp(filepath: Path) -> Optional[datetime]:
    """Extract timestamp from checkpoint filename."""
    try:
        # Checkpoint files are named: checkpoint_<timestamp>.json
        name = filepath.stem
        if name.startswith("checkpoint_"):
            ts_str = name.replace("checkpoint_", "")
            return datetime.fromisoformat(ts_str.replace("_", "-").replace(":", "-"))
    except Exception:
        pass
    return None


def _aggregate_checkpoints() -> dict:
    """Read all checkpoints and aggregate stats."""
    checkpoints_dir = _get_checkpoints_dir()

    if not checkpoints_dir.exists():
        return {
            "total_sessions": 0,
            "total_tokens": 0,
            "input_tokens": 0,
            "output_tokens": 0,
            "thinking_tokens": 0,
            "first_seen": None,
            "last_active": None,
            "model_usage": {},
            "sessions": [],
        }

    stats = {
        "total_sessions": 0,
        "total_tokens": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "thinking_tokens": 0,
        "first_seen": None,
        "last_active": None,
        "model_usage": {},
        "sessions": {},
    }

    checkpoint_files = sorted(checkpoints_dir.glob("checkpoint_*.json"))

    for cp_file in checkpoint_files:
        try:
            import json
            with open(cp_file, 'r') as f:
                data = json.load(f)

            # Extract token usage
            token_usage = data.get("token_usage", {})
            input_tokens = token_usage.get("input", 0)
            output_tokens = token_usage.get("output", 0)
            thinking_tokens = token_usage.get("thinking", 0)
            session_tokens = input_tokens + output_tokens + thinking_tokens

            stats["total_tokens"] += session_tokens
            stats["input_tokens"] += input_tokens
            stats["output_tokens"] += output_tokens
            stats["thinking_tokens"] += thinking_tokens

            # Track sessions (dedup by session_id if present)
            session_id = data.get("session_id", cp_file.stem)
            if session_id not in stats["sessions"]:
                stats["sessions"][session_id] = {
                    "session_id": session_id,
                    "created_at": _parse_timestamp(cp_file) or datetime.now(),
                    "last_active": _parse_timestamp(cp_file) or datetime.now(),
                    "token_count": session_tokens,
                    "checkpoint_count": 0,
                    "model": data.get("model"),
                }
                stats["total_sessions"] += 1
            else:
                # Add tokens from this checkpoint to existing session
                stats["sessions"][session_id]["token_count"] += session_tokens
                stats["sessions"][session_id]["last_active"] = _parse_timestamp(cp_file) or datetime.now()

            stats["sessions"][session_id]["checkpoint_count"] += 1

            # Track model usage with input/output breakdown for cost calculation
            model = data.get("model", "unknown")
            if model not in stats["model_usage"]:
                stats["model_usage"][model] = {
                    "model": model,
                    "sessions": 0,
                    "tokens": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "thinking_tokens": 0,
                }
            stats["model_usage"][model]["tokens"] += session_tokens
            stats["model_usage"][model]["input_tokens"] += input_tokens
            stats["model_usage"][model]["output_tokens"] += output_tokens
            stats["model_usage"][model]["thinking_tokens"] += thinking_tokens

            # Track first/last seen
            cp_time = _parse_timestamp(cp_file)
            if cp_time:
                if stats["first_seen"] is None or cp_time < stats["first_seen"]:
                    stats["first_seen"] = cp_time
                if stats["last_active"] is None or cp_time > stats["last_active"]:
                    stats["last_active"] = cp_time

        except Exception:
            continue

    return stats


# ============================================================================
# API Endpoints
# ============================================================================

@router.get("", response_model=UserStats)
async def get_user_stats() -> UserStats:
    """Get aggregated user statistics."""
    from ..agent.providers.models import calculate_cost

    data = _aggregate_checkpoints()

    # Convert model usage dict to list and calculate cost per model
    model_usage = list(data["model_usage"].values())

    # Calculate total cost from model usage
    total_cost = 0.0
    for usage in model_usage:
        model_cost = calculate_cost(
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            model=usage.get("model", "unknown"),
            thinking_tokens=usage.get("thinking_tokens", 0),
        )
        usage["estimated_cost"] = round(model_cost, 6)
        total_cost += model_cost

    model_usage.sort(key=lambda x: x["tokens"], reverse=True)

    return UserStats(
        total_sessions=data["total_sessions"],
        total_tokens=data["total_tokens"],
        input_tokens=data["input_tokens"],
        output_tokens=data["output_tokens"],
        thinking_tokens=data["thinking_tokens"],
        estimated_cost=round(total_cost, 6),
        cost_formatted=f"${total_cost:.4f}",
        first_seen=data["first_seen"].isoformat() if data["first_seen"] else None,
        last_active=data["last_active"].isoformat() if data["last_active"] else None,
        model_usage=model_usage,
    )


@router.get("/sessions", response_model=SessionList)
async def get_sessions(limit: int = 20, offset: int = 0) -> SessionList:
    """Get list of sessions with optional pagination."""
    data = _aggregate_checkpoints()
    sessions = list(data["sessions"].values())

    # Sort by last_active descending
    sessions.sort(key=lambda x: x.get("last_active") or datetime.min, reverse=True)

    # Paginate
    total = len(sessions)
    paginated = sessions[offset:offset + limit]

    # Convert to SessionInfo
    session_infos = []
    for s in paginated:
        session_infos.append(SessionInfo(
            session_id=s["session_id"],
            created_at=s["created_at"].isoformat() if s.get("created_at") else None,
            last_active=s["last_active"].isoformat() if s.get("last_active") else None,
            token_count=s["token_count"],
            checkpoint_count=s["checkpoint_count"],
            model=s.get("model"),
        ))

    return SessionList(sessions=session_infos, total=total)


@router.get("/tokens", response_model=TokenBreakdown)
async def get_token_breakdown() -> TokenBreakdown:
    """Get detailed token usage breakdown."""
    data = _aggregate_checkpoints()

    return TokenBreakdown(
        total=data["total_tokens"],
        input=data["input_tokens"],
        output=data["output_tokens"],
        thinking=data["thinking_tokens"],
    )


@router.get("/usage")
async def get_usage_log() -> dict:
    """Get usage log if it exists."""
    usage_file = Path(".emdash/usage.jsonl")
    if not usage_file.exists():
        usage_file = Path.home() / ".emdash" / "usage.jsonl"

    if not usage_file.exists():
        return {"entries": [], "message": "No usage log found"}

    entries = []
    try:
        with open(usage_file, 'r') as f:
            for line in f:
                if line.strip():
                    import json
                    entries.append(json.loads(line))
    except Exception:
        pass

    return {"entries": entries[-100:], "total": len(entries)}