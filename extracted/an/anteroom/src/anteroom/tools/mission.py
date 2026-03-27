"""Mission tools — conversational steering for mission sessions.

Ten tools for listing, inspecting, mutating, and patching mission plans.
Registered opt-in via ``register_mission_tools()`` in ``tools/__init__.py``.
"""

from __future__ import annotations

import logging
from dataclasses import asdict
from typing import Any

from ..services import mission_storage
from ..services.mission_compiler import apply_patch, compile_patch

logger = logging.getLogger(__name__)


def _validate_item_in_session(
    db: Any, session_id: str, item_id: str
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None]:
    """Validate session exists and item belongs to it. Returns (session, item, error_dict)."""
    session = mission_storage.get_session(db, session_id)
    if session is None:
        return None, None, {"error": f"Session not found: {session_id}"}
    item = mission_storage.get_item(db, item_id)
    if item is None:
        return session, None, {"error": f"Item not found: {item_id}"}
    if item["session_id"] != session_id:
        return session, item, {"error": f"Item {item_id} does not belong to session {session_id}"}
    return session, item, None


# ---------------------------------------------------------------------------
# Definitions (OpenAI function-call format)
# ---------------------------------------------------------------------------

MISSION_LIST_DEFINITION: dict[str, Any] = {
    "name": "mission_list",
    "description": "List mission sessions, optionally filtered by status.",
    "parameters": {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Filter by session status (pending, active, paused, completed, failed, cancelled).",
            },
        },
        "required": [],
    },
}

MISSION_STATUS_DEFINITION: dict[str, Any] = {
    "name": "mission_status",
    "description": (
        "Show detailed status for a mission session including all items"
        " with their status, priority, lane, and adapter type."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "The mission session ID.",
            },
        },
        "required": ["session_id"],
    },
}

MISSION_EXPLAIN_BLOCKERS_DEFINITION: dict[str, Any] = {
    "name": "mission_explain_blockers",
    "description": (
        "Explain why mission items are blocked or pending. If item_id is omitted, explains all blocked/pending items."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {
                "type": "string",
                "description": "The mission session ID.",
            },
            "item_id": {
                "type": "string",
                "description": "Optional specific item ID to explain. If omitted, explains all blocked/pending items.",
            },
        },
        "required": ["session_id"],
    },
}

MISSION_ADD_ITEM_DEFINITION: dict[str, Any] = {
    "name": "mission_add_item",
    "description": "Add a new item to a mission session.",
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string", "description": "The mission session ID."},
            "summary": {"type": "string", "description": "Short summary of the item."},
            "description": {"type": "string", "description": "Longer description."},
            "priority": {"type": "integer", "description": "Priority 1-100 (lower = higher priority). Default 50."},
            "adapter_type": {"type": "string", "description": "Adapter type (e.g. noop, agent)."},
            "adapter_config": {"type": "object", "description": "Adapter configuration."},
            "depends_on": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of item IDs this item depends on.",
            },
            "lane": {"type": "string", "description": "Lane name for concurrency limiting."},
            "concurrency_group": {"type": "string", "description": "Concurrency group name."},
        },
        "required": ["session_id", "summary"],
    },
}

MISSION_HOLD_DEFINITION: dict[str, Any] = {
    "name": "mission_hold",
    "description": "Place a mission item on hold, preventing it from being scheduled.",
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string", "description": "The mission session ID."},
            "item_id": {"type": "string", "description": "The item ID to hold."},
        },
        "required": ["session_id", "item_id"],
    },
}

MISSION_RESUME_DEFINITION: dict[str, Any] = {
    "name": "mission_resume",
    "description": "Resume a held mission item so it can be scheduled again.",
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string", "description": "The mission session ID."},
            "item_id": {"type": "string", "description": "The item ID to resume."},
        },
        "required": ["session_id", "item_id"],
    },
}

MISSION_REPRIORITIZE_DEFINITION: dict[str, Any] = {
    "name": "mission_reprioritize",
    "description": "Change the priority of a mission item.",
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string", "description": "The mission session ID."},
            "item_id": {"type": "string", "description": "The item ID to reprioritize."},
            "priority": {"type": "integer", "description": "New priority 1-100 (lower = higher priority)."},
        },
        "required": ["session_id", "item_id", "priority"],
    },
}

MISSION_DROP_ITEM_DEFINITION: dict[str, Any] = {
    "name": "mission_drop_item",
    "description": "Drop a mission item, marking it as no longer needed.",
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string", "description": "The mission session ID."},
            "item_id": {"type": "string", "description": "The item ID to drop."},
            "reason": {"type": "string", "description": "Optional reason for dropping the item."},
        },
        "required": ["session_id", "item_id"],
    },
}

MISSION_COMPLETE_DEFINITION: dict[str, Any] = {
    "name": "mission_complete",
    "description": "Manually mark a mission session as completed.",
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string", "description": "The mission session ID."},
        },
        "required": ["session_id"],
    },
}

MISSION_PATCH_PLAN_DEFINITION: dict[str, Any] = {
    "name": "mission_patch_plan",
    "description": (
        "Apply natural language changes to a mission plan."
        " Describe what you want to change and the AI will compile"
        " and apply the appropriate patch operations."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "session_id": {"type": "string", "description": "The mission session ID."},
            "instruction": {
                "type": "string",
                "description": "Natural language description of the changes to apply to the plan.",
            },
        },
        "required": ["session_id", "instruction"],
    },
}

MISSION_TOOL_DEFINITIONS: list[dict[str, Any]] = [
    MISSION_LIST_DEFINITION,
    MISSION_STATUS_DEFINITION,
    MISSION_EXPLAIN_BLOCKERS_DEFINITION,
    MISSION_ADD_ITEM_DEFINITION,
    MISSION_HOLD_DEFINITION,
    MISSION_RESUME_DEFINITION,
    MISSION_REPRIORITIZE_DEFINITION,
    MISSION_DROP_ITEM_DEFINITION,
    MISSION_COMPLETE_DEFINITION,
    MISSION_PATCH_PLAN_DEFINITION,
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _next_revision_number(db: Any, session_id: str) -> int:
    revisions = mission_storage.list_revisions(db, session_id)
    return len(revisions) + 1


def _snapshot_and_revise(
    db: Any,
    session_id: str,
    operations: list[dict[str, Any]],
    reason: str | None = None,
) -> dict[str, Any]:
    snapshot = mission_storage.build_plan_snapshot(db, session_id)
    rev_num = _next_revision_number(db, session_id)
    return mission_storage.create_revision(
        db,
        session_id=session_id,
        revision_number=rev_num,
        operations=operations,
        plan_snapshot_after=snapshot,
        reason=reason,
    )


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_mission_list(
    status: str | None = None,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    kwargs: dict[str, Any] = {}
    if status:
        kwargs["status"] = status
    sessions = mission_storage.list_sessions(_db, **kwargs)
    return {
        "sessions": [
            {
                "id": s["id"],
                "status": s["status"],
                "title": s["title"],
                "created_at": s["created_at"],
            }
            for s in sessions
        ],
        "count": len(sessions),
    }


async def handle_mission_status(
    session_id: str,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    session = mission_storage.get_session(_db, session_id)
    if session is None:
        return {"error": f"Session not found: {session_id}"}
    items = mission_storage.list_items_by_session(_db, session_id)
    counts: dict[str, int] = {}
    for item in items:
        s = item["status"]
        counts[s] = counts.get(s, 0) + 1
    return {
        "session": {
            "id": session["id"],
            "status": session["status"],
            "title": session["title"],
            "description": session["description"],
            "created_at": session["created_at"],
        },
        "items": [
            {
                "id": item["id"],
                "summary": item["summary"],
                "status": item["status"],
                "priority": item["priority"],
                "lane": item["lane"],
                "adapter_type": item["adapter_type"],
                "hold_requested": item["hold_requested"],
            }
            for item in items
        ],
        "progress": counts,
        "total_items": len(items),
    }


async def handle_mission_explain_blockers(
    session_id: str,
    item_id: str | None = None,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    session = mission_storage.get_session(_db, session_id)
    if session is None:
        return {"error": f"Session not found: {session_id}"}

    items = mission_storage.list_items_by_session(_db, session_id)
    item_map = {i["id"]: i for i in items}

    if item_id:
        if item_id not in item_map:
            return {"error": f"Item not found: {item_id}"}
        targets = [item_map[item_id]]
    else:
        targets = [i for i in items if i["status"] in ("blocked", "pending")]

    explanations: list[dict[str, Any]] = []
    for item in targets:
        reasons: list[str] = []
        deps = mission_storage.get_dependencies(_db, item["id"])
        incomplete_deps: list[dict[str, str]] = []
        for dep_id in deps:
            dep = item_map.get(dep_id)
            if dep and dep["status"] != "completed":
                incomplete_deps.append({"id": dep_id, "summary": dep["summary"], "status": dep["status"]})
        if incomplete_deps:
            reasons.append(f"Waiting on {len(incomplete_deps)} incomplete dependency(ies)")
        if item.get("hold_requested"):
            reasons.append("Item is on hold")
        if not reasons and item["status"] in ("blocked", "pending"):
            reasons.append("No specific blockers found — item may be waiting for scheduling")
        explanations.append(
            {
                "item_id": item["id"],
                "summary": item["summary"],
                "status": item["status"],
                "reasons": reasons,
                "incomplete_dependencies": incomplete_deps,
                "hold_requested": bool(item.get("hold_requested")),
            }
        )

    return {"explanations": explanations, "count": len(explanations)}


async def handle_mission_add_item(
    session_id: str,
    summary: str,
    description: str | None = None,
    priority: int = 50,
    adapter_type: str = "noop",
    adapter_config: dict[str, Any] | None = None,
    depends_on: list[str] | None = None,
    lane: str | None = None,
    concurrency_group: str | None = None,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    session = mission_storage.get_session(_db, session_id)
    if session is None:
        return {"error": f"Session not found: {session_id}"}

    if depends_on:
        existing_items = mission_storage.list_items_by_session(_db, session_id)
        existing_ids = {i["id"] for i in existing_items}
        for dep_id in depends_on:
            if dep_id not in existing_ids:
                return {"error": f"Dependency {dep_id} not found in session {session_id}"}

    item = mission_storage.create_item(
        _db,
        session_id=session_id,
        summary=summary,
        description=description,
        priority=priority,
        adapter_type=adapter_type,
        adapter_config=adapter_config,
        concurrency_group=concurrency_group,
        lane=lane,
    )

    if depends_on:
        for dep_id in depends_on:
            mission_storage.add_dependency(_db, item_id=item["id"], depends_on_id=dep_id)

    _snapshot_and_revise(
        _db,
        session_id,
        [{"op": "add_item", "item_id": item["id"], "summary": summary}],
        reason=f"Added item: {summary}",
    )

    return {"item": item, "message": f"Item '{summary}' added to mission"}


async def handle_mission_hold(
    session_id: str,
    item_id: str,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    _session, item, err = _validate_item_in_session(_db, session_id, item_id)
    if err:
        return err
    assert item is not None

    mission_storage.update_item(_db, item_id, hold_requested=1)
    _snapshot_and_revise(
        _db,
        session_id,
        [{"op": "hold", "item_id": item_id}],
        reason=f"Held item: {item['summary']}",
    )
    return {"item_id": item_id, "hold_requested": True, "message": f"Item '{item['summary']}' placed on hold"}


async def handle_mission_resume(
    session_id: str,
    item_id: str,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    _session, item, err = _validate_item_in_session(_db, session_id, item_id)
    if err:
        return err
    assert item is not None

    mission_storage.update_item(_db, item_id, hold_requested=0)
    _snapshot_and_revise(
        _db,
        session_id,
        [{"op": "resume", "item_id": item_id}],
        reason=f"Resumed item: {item['summary']}",
    )
    return {"item_id": item_id, "hold_requested": False, "message": f"Item '{item['summary']}' resumed"}


async def handle_mission_reprioritize(
    session_id: str,
    item_id: str,
    priority: int,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    _session, item, err = _validate_item_in_session(_db, session_id, item_id)
    if err:
        return err
    assert item is not None

    old_priority = item["priority"]
    mission_storage.update_item(_db, item_id, priority=priority)
    _snapshot_and_revise(
        _db,
        session_id,
        [{"op": "reprioritize", "item_id": item_id, "old_priority": old_priority, "new_priority": priority}],
        reason=f"Reprioritized item: {item['summary']} ({old_priority} -> {priority})",
    )
    return {
        "item_id": item_id,
        "old_priority": old_priority,
        "new_priority": priority,
        "message": f"Item '{item['summary']}' reprioritized from {old_priority} to {priority}",
    }


async def handle_mission_drop_item(
    session_id: str,
    item_id: str,
    reason: str | None = None,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    _session, item, err = _validate_item_in_session(_db, session_id, item_id)
    if err:
        return err
    assert item is not None

    mission_storage.update_item(_db, item_id, status="dropped")
    _snapshot_and_revise(
        _db,
        session_id,
        [{"op": "drop_item", "item_id": item_id, "reason": reason}],
        reason=reason or f"Dropped item: {item['summary']}",
    )
    return {"item_id": item_id, "status": "dropped", "message": f"Item '{item['summary']}' dropped"}


async def handle_mission_complete(
    session_id: str,
    _db: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    session = mission_storage.get_session(_db, session_id)
    if session is None:
        return {"error": f"Session not found: {session_id}"}

    mission_storage.update_session(_db, session_id, status="completed")
    mission_storage.create_event(
        _db,
        session_id=session_id,
        event_type="session_completed",
        detail={"previous_status": session["status"]},
    )
    return {"session_id": session_id, "status": "completed", "message": "Mission marked as completed"}


async def handle_mission_patch_plan(
    session_id: str,
    instruction: str,
    _db: Any = None,
    _ai_service: Any = None,
    **_: Any,
) -> dict[str, Any]:
    if _db is None:
        return {"error": "No database connection available"}
    if _ai_service is None:
        return {"error": "No AI service available"}
    session = mission_storage.get_session(_db, session_id)
    if session is None:
        return {"error": f"Session not found: {session_id}"}

    current_items = mission_storage.list_items_by_session(_db, session_id)
    items_for_compiler = [
        {
            "id": item["id"],
            "summary": item["summary"],
            "status": item["status"],
            "priority": item["priority"],
            "adapter_type": item["adapter_type"],
            "lane": item.get("lane"),
        }
        for item in current_items
    ]

    artifact_context = session.get("referenced_artifacts") or []

    # Enrich instruction with profile context if the session has one.
    # Validate the profile name against the known registry to prevent
    # prompt injection via crafted session metadata.
    enriched_instruction = instruction
    session_meta = session.get("metadata") or {}
    profile_name = session_meta.get("execution_profile")
    if profile_name and isinstance(profile_name, str):
        from ..services.mission_profiles import _BUILTIN_PROFILES

        if profile_name in _BUILTIN_PROFILES:
            enriched_instruction = (
                f"[Profile context: this mission uses the '{profile_name}' execution profile. "
                f"When changing adapter bindings, prefer workflows matching this profile's style.]\n\n"
                f"{instruction}"
            )

    patch = await compile_patch(
        enriched_instruction, items_for_compiler, _ai_service, artifact_context=artifact_context
    )

    if not patch.operations:
        return {"message": "No operations compiled from instruction", "operations": []}

    apply_patch(_db, session_id, patch)

    return {
        "message": f"Applied {len(patch.operations)} operation(s)",
        "operations": [asdict(op) for op in patch.operations],
    }


# ---------------------------------------------------------------------------
# Handler registry
# ---------------------------------------------------------------------------

MISSION_TOOL_HANDLERS: dict[str, Any] = {
    "mission_list": handle_mission_list,
    "mission_status": handle_mission_status,
    "mission_explain_blockers": handle_mission_explain_blockers,
    "mission_add_item": handle_mission_add_item,
    "mission_hold": handle_mission_hold,
    "mission_resume": handle_mission_resume,
    "mission_reprioritize": handle_mission_reprioritize,
    "mission_drop_item": handle_mission_drop_item,
    "mission_complete": handle_mission_complete,
    "mission_patch_plan": handle_mission_patch_plan,
}
