"""S6 typed tool outcomes — the additive tool-result payloads the model sees.

Every tool name, argument, and existing response key is unchanged; everything
here is ADDITIVE (S6 §2). Producers build these; a caller that knows nothing
about profiles keeps working.

The three statuses are exhaustive: ``ok`` | ``human_required`` |
``reopened_for_handoff`` (S6 §5.6). Errors travel on ``ToolError`` with the
error-type catalogue of S6 §5.4.
"""

from __future__ import annotations

from typing import Literal

from matrx_ai.browser_handoff.models import HandoffReason, PageFacts, PageInventory
from matrx_ai.tools.models import ToolError
from matrx_ai.tools.output_caps import cap_list, cap_text

Status = Literal["ok", "human_required", "reopened_for_handoff"]

# S6 §5.4 — the complete new error_type literal set (existing types unchanged).
NEW_ERROR_TYPES: frozenset[str] = frozenset(
    {
        "browser_controlled_by_human",
        "profile_access_denied",
        "profile_not_found",
        "stale_run",
        "profile_busy",
    }
)

# Retryability is asserted by test, not left to chance — a "retryable" conflict
# is how a tool loop burns a paid turn every second while a human types a
# password (S6 §5.3).
_NON_RETRYABLE_NEW = NEW_ERROR_TYPES  # all new error types are non-retryable

_SUGGESTED_ACTIONS: dict[str, str] = {
    "browser_controlled_by_human": (
        "Wait for the person to return control. Do not retry this action in a loop."
    ),
    "profile_access_denied": (
        "Ask the profile owner to share this Cloud Browser with you, or call this "
        "tool without profile_id to use your own."
    ),
    "profile_not_found": "Call this tool without profile_id to use your own Cloud Browser.",
    "stale_run": (
        "This browser moved on. Call cloud_browser action='navigate' with the same profile_id to reattach."
    ),
    "profile_busy": (
        "This Cloud Browser is already running somewhere else. Wait for it to finish, "
        "or open a different profile."
    ),
}


def new_error(error_type: str, *, message: str) -> ToolError:
    """Build one of the S6 §5.4 new browser error types with its pinned
    retryability + suggested action. Rejects any type not in the catalogue —
    a new error_type requires a DECISIONS.md entry (S6 §5.4)."""
    if error_type not in NEW_ERROR_TYPES:
        raise ValueError(
            f"{error_type!r} is not a catalogued browser error type "
            f"(add it to S6 §5.4 with a DECISIONS.md entry first)."
        )
    return ToolError(
        error_type=error_type,
        message=message,
        is_retryable=False,
        suggested_action=_SUGGESTED_ACTIONS[error_type],
    )


def ok_identity(*, run_id: str | None, profile_id: str | None) -> dict:
    """The additive success keys (S6 §5.1). ``status:"ok"`` always; ``run_id`` /
    ``profile_id`` only on a persistent-profile run (transient legacy calls omit
    them entirely — the backwards-compatibility anchor)."""
    out: dict = {"status": "ok"}
    if run_id is not None:
        out["run_id"] = run_id
    if profile_id is not None:
        out["profile_id"] = profile_id
    return out


def human_required_output(
    *,
    reason: HandoffReason | str,
    handoff_id: str,
    run_id: str,
    profile_id: str,
    url: str | None = None,
    title: str | None = None,
    message: str,
) -> dict:
    """S6 §5.2. A SUCCESSFUL tool result whose output carries ``success: true`` —
    returning the park as a failure would make the executor mark it retryable and
    tell the agent to retry the exact thing that needs a human. ``reason`` is
    passed through untouched (never validated against a local enum)."""
    reason_str = reason.value if isinstance(reason, HandoffReason) else reason
    out: dict = {
        "status": "human_required",
        "reason": reason_str,
        "handoff_id": handoff_id,
        "continuation_required": True,
        "success": True,
        "session_id": run_id,
        "run_id": run_id,
        "profile_id": profile_id,
        "message": cap_text(message, limit=512)[0],
    }
    if url is not None:
        out["url"] = url
    if title is not None:
        out["title"] = title
    return out


_PRESERVED = ["cookies", "local_storage", "indexed_db", "history"]
_NOT_PRESERVED = [
    "in_page_javascript_state",
    "in_flight_requests",
    "open_dialogs",
    "unsubmitted_form_input",
]


def reopened_for_handoff_output(
    *,
    reason: HandoffReason | str,
    handoff_id: str,
    new_run_id: str,
    previous_run_id: str,
    profile_id: str,
    url: str | None = None,
    title: str | None = None,
    message: str,
) -> dict:
    """S6 §5.5. ``volatile_state_preserved`` is ALWAYS literally False — a
    constant, not a computed field. The session_id changes; the old handle is
    dead. ``previous_run_id`` connects the two runs."""
    reason_str = reason.value if isinstance(reason, HandoffReason) else reason
    out: dict = {
        "status": "reopened_for_handoff",
        "success": True,
        "reason": reason_str,
        "handoff_id": handoff_id,
        "continuation_required": True,
        "session_id": new_run_id,
        "run_id": new_run_id,
        "previous_run_id": previous_run_id,
        "profile_id": profile_id,
        "volatile_state_preserved": False,
        "preserved": list(_PRESERVED),
        "not_preserved": list(_NOT_PRESERVED),
        "message": cap_text(message, limit=512)[0],
    }
    if url is not None:
        out["url"] = url
    if title is not None:
        out["title"] = title
    return out


def page_inventory_payload(inventory: PageInventory) -> tuple[dict, bool]:
    """S6 §7.2 — the self-capped resume page inventory. Returns the payload and
    ``output_self_capped=True`` (the whole result is provably bounded). Rows are
    projected to exactly ``page_id`` / ``url`` / ``title`` / ``active`` — never
    DOM, never page text — the active page is ALWAYS included even under
    truncation, and ``url`` / ``title`` are each ``cap_text``-bounded."""
    pages = list(inventory.pages)
    active_id = inventory.active_page_id
    active = next((p for p in pages if p.page_id == active_id), None)

    shown, info = cap_list(pages, limit=25)
    # The active page is always included, even if truncation dropped it.
    if active is not None and all(p.page_id != active.page_id for p in shown):
        shown = [active, *shown[:-1]] if shown else [active]

    def _row(p: PageFacts) -> dict:
        return {
            "page_id": p.page_id,
            "url": cap_text(p.url, limit=512)[0] if p.url is not None else None,
            "title": cap_text(p.title, limit=512)[0] if p.title is not None else None,
            "active": p.page_id == active_id,
        }

    dialogs_shown, dinfo = cap_list([], limit=10)  # placeholder projection point
    payload = {
        "pages": [_row(p) for p in shown],
        "pages_total": info.total,
        "pages_shown": len(shown),
        "pages_truncated": info.truncated,
        "dialogs": [],
        "dialogs_total": inventory.open_dialogs,
        "downloads": [],
        "downloads_total": inventory.pending_downloads,
    }
    return payload, True
