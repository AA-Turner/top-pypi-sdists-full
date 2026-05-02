"""Durable experience helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from packages.contracts.runtime import ExperienceRecord


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_summary(summary: str) -> str:
    return " ".join(summary.split())


def _title_from_summary(summary: str, *, limit: int = 96) -> str:
    text = summary.strip()
    if not text:
        return "Untitled experience"
    for separator in (". ", "\n", "; "):
        if separator in text:
            text = text.split(separator, 1)[0].strip()
            break
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def capture_turn_experience(
    *,
    session_id: str,
    profile_id: str,
    workspace_id: str | None,
    summary: str,
    source_event_id: str | None = None,
    run_id: str | None = None,
    goal_id: str | None = None,
    tool_call_count: int = 0,
    model_turn_count: int = 0,
    related_skill_ids: tuple[str, ...] = (),
    produced_artifact_ids: tuple[str, ...] = (),
    tags: tuple[str, ...] = (),
    now: datetime | None = None,
) -> ExperienceRecord | None:
    normalized_summary = _normalize_summary(summary)
    if not normalized_summary:
        return None
    timestamp = now or _utc_now()
    resolved_tags = ["experience", "turn-outcome"]
    if tool_call_count >= 2:
        resolved_tags.append("tool-heavy")
    if model_turn_count >= 2:
        resolved_tags.append("multi-turn")
    if related_skill_ids:
        resolved_tags.append("skill-attached")
    for tag in tags:
        tag_text = tag.strip()
        if tag_text and tag_text not in resolved_tags:
            resolved_tags.append(tag_text)
    return ExperienceRecord(
        experience_id=f"experience:{session_id}:{uuid4().hex[:10]}",
        session_id=session_id,
        profile_id=profile_id,
        workspace_id=workspace_id,
        kind="turn-outcome",
        title=_title_from_summary(normalized_summary),
        summary=normalized_summary,
        status="captured",
        run_id=run_id,
        source_event_id=source_event_id,
        goal_id=goal_id,
        tool_call_count=tool_call_count,
        model_turn_count=model_turn_count,
        related_skill_ids=related_skill_ids,
        produced_artifact_ids=produced_artifact_ids,
        tags=tuple(resolved_tags),
        created_at=timestamp,
        updated_at=timestamp,
    )
