"""When the person's machine is DOWN, a tool says so — it does not substitute.

THE FAILURE THIS CLOSES. With no sandbox bound, ``shell_execute`` and the
``fs_*`` tools fall through to the durable-VFS emulator over the person's code
files. For an ordinary conversation that is exactly right: nobody attached a
box, so there is no box to be down, and the emulator is the honest local
answer.

For somebody whose product is *"the box and the browser always there"* it is a
lie. They HAVE a machine. It is supposed to be up. And a turn that quietly runs
coreutils in an emulator while the person believes their own files are being
read is the silent-degrade class the sandbox hard-gate exists to prevent —
arriving through the one door that gate cannot close, because a conversation
with no binding at all raises no refusal and never should.

THE HOST DECIDES, THE PACKAGE OBEYS. This module reads ONE key,
``workspace_outage``, off the same ``AppContext.metadata`` that already carries
``active_sandbox``. The host (aidream's ``sandbox_autobind._stamp_workspace_
outage``) is the only thing that can know a person's box is down rather than
absent — it holds the enrollment, the knob and the rows. A bare ``matrx-ai``
install, and every conversation the host does not stamp, behaves exactly as it
does today.

THE SENTENCE COMES FROM THE HOST TOO, VERBATIM. It is written for a person to
read on a lock screen, and it names BOTH halves — what the staff cannot do now,
and what it still can — because somebody told only "it is down" has no idea
whether to wait or to ask for something else. Nothing here rewrites it.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

#: The key the host stamps on the run. One string, one meaning.
WORKSPACE_OUTAGE_KEY = "workspace_outage"


@dataclass(frozen=True)
class WorkspaceOutage:
    """The host's verdict about the person's machine, for this run."""

    status: str
    sentence: str
    since: str | None = None


def active_workspace_outage() -> WorkspaceOutage | None:
    """The outage this run is carrying, or ``None``.

    ``None`` is the overwhelmingly common answer and means "no host has told us
    this person's machine is down" — never "their machine is fine". A tool that
    reads ``None`` behaves exactly as it always has.
    """

    try:
        from matrx_connect import try_get_app_context
    except Exception:  # noqa: BLE001 — a bare install has no host context
        return None

    ctx = try_get_app_context()
    if ctx is None:
        return None
    raw: Any = ctx.metadata.get(WORKSPACE_OUTAGE_KEY) if ctx.metadata else None
    if not raw or not isinstance(raw, dict):
        return None
    sentence = str(raw.get("sentence") or "").strip()
    if not sentence:
        # A stamp with no sentence cannot be put in front of a person, and this
        # module will not invent one: the host owns those words. Refusing on a
        # sentence we composed here is how a tool starts telling somebody
        # something nobody decided to say.
        return None
    since = raw.get("since")
    return WorkspaceOutage(
        status=str(raw.get("status") or "down"),
        sentence=sentence,
        since=str(since) if since else None,
    )


def outage_result(tool_name: str, ctx: ToolContext, outage: WorkspaceOutage) -> ToolResult:
    """The refusal a tool returns instead of quietly using the emulator.

    ``error_type='unavailable'`` and ``is_retryable=True``: the workspace is
    coming back, and a turn later in the same conversation may well find it up.
    The message is the host's sentence unchanged, plus the one instruction the
    model needs — SAY THIS, do not work around it. Without that instruction an
    agent handed a failure reaches for the next tool, and the person receives a
    silent non-answer instead of the sentence somebody wrote for them.
    """

    now = time.time()
    return ToolResult(
        success=False,
        error=ToolError(
            error_type="unavailable",
            message=(
                f"{outage.sentence}\n\n"
                f"(Operator detail: this person's workspace is {outage.status}"
                + (f" since {outage.since}" if outage.since else "")
                + f"; `{tool_name}` needs it and there is no honest substitute. The "
                "durable file emulator is NOT their machine and must not be presented "
                "as it.)"
            ),
            suggested_action=(
                "Tell them the sentence above, in your own voice, and carry on with "
                "whatever you CAN do for them. Do not retry this tool in this turn, do "
                "not reach for a different tool to work around it, and never imply the "
                "command ran."
            ),
            is_retryable=True,
        ),
        started_at=now,
        completed_at=now,
        tool_name=tool_name,
        call_id=ctx.call_id,
    )


def refuse_if_workspace_is_down(tool_name: str, ctx: ToolContext) -> ToolResult | None:
    """One line at the top of a fallback branch. ``None`` means carry on.

    Call it ONLY where a tool is about to serve a substitute for the person's
    machine — never before the sandbox branch, which is the real thing and can
    never be refused by a stale stamp.
    """

    outage = active_workspace_outage()
    if outage is None:
        return None
    return outage_result(tool_name, ctx, outage)


__all__ = [
    "WORKSPACE_OUTAGE_KEY",
    "WorkspaceOutage",
    "active_workspace_outage",
    "outage_result",
    "refuse_if_workspace_is_down",
]
