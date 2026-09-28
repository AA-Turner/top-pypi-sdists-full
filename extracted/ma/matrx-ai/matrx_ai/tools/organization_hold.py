"""The organization hold, as a tool answers it.

A tool that writes a row owned by an organization needs the organization the
request CARRIES (``ToolContext.organization_id`` — the conversation's verified
AppContext). When the run carries none, the write must not happen and nothing may
be picked on the person's behalf (no personal organization, no "default"). The
tool answers with the platform's ONE hold shape
(:func:`matrx_connect.org_hold.organization_hold_detail`) so the model can tell
the person to choose the organization they are working in and try again.

Law: ``common-docs/policies/context-is-carried-never-rebuilt.md`` and aidream
CLAUDE.md "A default organization decides NOTHING".
"""

from __future__ import annotations

import time
from typing import Any

from matrx_ai.tools.models import ToolContext, ToolError, ToolResult


def carried_organization_id(ctx: ToolContext) -> str | None:
    """The organization this call carries, or ``None``. Never looked up, never defaulted."""
    try:
        raw = ctx.organization_id
    except Exception:  # noqa: BLE001 — no AppContext on this path means no organization.
        return None
    value = str(raw).strip() if raw else ""
    return value or None


def organization_required_result(
    *,
    what: str,
    tool_name: str,
    ctx: ToolContext,
    started_at: float | None = None,
) -> ToolResult:
    """A refused write: the canonical ``organization_required`` hold, as a ToolResult.

    ``what`` names the write in plain words ("create a dataset"). The output
    carries the full hold envelope so a client can render the organization picker.
    """
    from matrx_connect.org_hold import organization_hold_detail

    detail: dict[str, Any] = organization_hold_detail(
        what=f"{tool_name}: this call carries no organization, so it cannot {what}.",
        set_on="request",
    )
    now = time.time()
    return ToolResult(
        success=False,
        output={"hold": detail},
        error=ToolError(
            error_type=detail["code"],
            message=(
                f"Nothing was saved: this conversation is not working in an organization, "
                f"so I cannot {what}. {detail['user_message']}"
            ),
            suggested_action=(
                "Tell the person, in one sentence, to choose the organization they are "
                "working in (the workspace picker) and ask again. Do not retry this call "
                "until they have."
            ),
            is_retryable=False,
        ),
        started_at=started_at or now,
        completed_at=now,
        tool_name=tool_name,
        call_id=ctx.call_id,
    )
