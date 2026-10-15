"""THE LIVE PLAN — the agent's own checklist, restated at the end of every send.

Why this exists
---------------
2026-10-14, a Notion → AI Matrx migration (chat.conversation 3787dd66): the agent
called ``update_plan`` once at iteration 13 (six phases, approved 28s later), then
ran 34 more minutes, 66 model calls and ~170 tool calls without touching the plan
again. In the final request the plan sat once, as an old tool call at message 27
of 135, inside ~170k tokens. Nothing ever showed it to the model again, and the
model pays attention to the END of its context, not message 27.

What it does
------------
On every loop send of a conversation that has OPEN agent tasks
(``chat.agent_task``), the send boundary stages one compact block in the
MessageList TAIL CHANNEL (``MessageList.attach_tail_context``): every step with
its status, the step in progress, and how many tool calls have run since the
model last updated the list. Past a threshold the block says so plainly, the way
Claude Code's todo reminder does.

Placement (the cache contract): translators render the tail AFTER the last
message's blocks and after Anthropic's rolling cache breakpoint, and only when
that last message is a tool result. The block is never a message, never
persisted, never in the system prompt; the next send re-stages it.

Where the rows come from: the host. This package never imports the host, so the
host installs ONE async source at boot (``set_live_plan_source``) that returns a
:class:`LivePlanSnapshot` for a conversation (tasks + the organization's knobs,
``agents.live_plan``). No source → no block (standalone posture).
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

#: The tail slot the plan rides in.
LIVE_PLAN_SLOT = "live_plan"

#: The organization knobs the host resolves (``platform.feature_knob``).
LIVE_PLAN_KNOB_FEATURE = "agents.live_plan"

#: Tool calls that count as the model working its plan. ``tasks list`` is a read
#: and does not reset the counter; every other ``tasks`` action and an
#: ``update_plan`` proposal do.
_PLAN_TOOL = "tasks"
_PROPOSE_TOOL = "update_plan"
_READ_ONLY_TASK_ACTIONS = frozenset({"list"})

OPEN_STATUSES = frozenset({"pending", "in_progress", "blocked"})


@dataclass(frozen=True)
class PlanTask:
    id: str
    title: str
    status: str
    note: str | None = None


@dataclass(frozen=True)
class LivePlanSettings:
    """``agents.live_plan`` knobs; these defaults are the standalone posture."""

    enabled: bool = True
    #: How many steps the block lists before it summarizes the rest.
    max_steps: int = 20
    #: Tool calls without a task update before the block nudges.
    nudge_after_tool_calls: int = 15


@dataclass(frozen=True)
class LivePlanSnapshot:
    tasks: list[PlanTask] = field(default_factory=list)
    settings: LivePlanSettings = field(default_factory=LivePlanSettings)


#: ``async (conversation_id, organization_id) -> LivePlanSnapshot | None``.
LivePlanSource = Callable[[str, str | None], Awaitable["LivePlanSnapshot | None"]]

_SOURCE: LivePlanSource | None = None


def set_live_plan_source(source: LivePlanSource | None) -> None:
    """Install the host's per-conversation plan reader (``None`` = standalone)."""
    global _SOURCE
    _SOURCE = source


def get_live_plan_source() -> LivePlanSource | None:
    return _SOURCE


def _role_of(message: Any) -> str:
    role = getattr(message, "role", None)
    return str(getattr(role, "value", role) or "").lower()


def _counts_as_plan_work(call: Any) -> bool:
    name = str(getattr(call, "name", "") or "")
    if name == _PROPOSE_TOOL:
        return True
    if name != _PLAN_TOOL:
        return False
    args = getattr(call, "arguments", None)
    action = args.get("action") if isinstance(args, dict) else None
    return action not in _READ_ONLY_TASK_ACTIONS


def tool_calls_since_plan_update(messages: Any) -> int:
    """Tool calls the model made after its last plan write (newest first walk).

    Counted from the message list itself, so it is exact mid-loop — this run's
    calls are in memory long before their rows land. A history with no plan
    write in view counts every call in view.
    """
    from matrx_ai.config.tools_config import ToolCallContent

    count = 0
    for message in reversed(list(messages or [])):
        if _role_of(message) != "assistant":
            continue
        for content in reversed(list(getattr(message, "content", None) or [])):
            if not isinstance(content, ToolCallContent):
                continue
            if _counts_as_plan_work(content):
                return count
            count += 1
    return count


_STATUS_MARK = {
    "done": "[x]",
    "in_progress": "[>]",
    "blocked": "[!]",
    "skipped": "[-]",
    "pending": "[ ]",
}


def render_live_plan(
    tasks: list[PlanTask],
    *,
    tool_calls_since_update: int,
    settings: LivePlanSettings,
) -> str | None:
    """The block, or None when there is nothing open to work."""
    if not settings.enabled or not tasks:
        return None
    if not any(t.status in OPEN_STATUSES for t in tasks):
        return None

    done = sum(1 for t in tasks if t.status == "done")
    current = next((t for t in tasks if t.status == "in_progress"), None)
    lines = [
        '<your_plan source="platform">',
        f"Your task list for this conversation ({done} of {len(tasks)} done). "
        "It is your own working plan; the person sees it live as a checklist.",
    ]
    limit = max(1, int(settings.max_steps))
    shown = tasks[:limit]
    for task in shown:
        mark = _STATUS_MARK.get(task.status, "[ ]")
        lines.append(f"{mark} {task.title}  (id {task.id}, {task.status})")
    if len(tasks) > limit:
        hidden = tasks[limit:]
        open_hidden = sum(1 for t in hidden if t.status in OPEN_STATUSES)
        lines.append(
            f"... {len(hidden)} more step(s), {open_hidden} still open "
            "(tasks action='list' shows them all)."
        )
    if current is not None:
        lines.append(f"In progress now: {current.title}")
    else:
        lines.append("No step is marked in progress.")
    lines.append(f"Tool calls since you last updated this list: {tool_calls_since_update}.")
    if tool_calls_since_update >= max(1, int(settings.nudge_after_tool_calls)):
        lines.append(
            f"You have made {tool_calls_since_update} tool calls without updating your "
            "task list. If a step is finished, mark it done; mark the step you are on "
            "in_progress; add or skip steps if the plan changed. Use the tasks tool "
            "(action='set_status', id, status). Do not mention this reminder to the person."
        )
    else:
        lines.append(
            "Keep it current with the tasks tool: mark a step in_progress when you start "
            "it and done when it is finished."
        )
    lines.append("</your_plan>")
    return "\n".join(lines)


async def stage_live_plan(
    config: Any,
    *,
    conversation_id: str | None,
    organization_id: str | None,
    source: LivePlanSource | None = None,
) -> dict[str, Any] | None:
    """Stage (or clear) the plan block on ``config.messages``; return an audit dict.

    Called by the send boundary on every loop send. Raises only what the
    source raises — the boundary announces it and skips the step.
    """
    messages = getattr(config, "messages", None)
    attach = getattr(messages, "attach_tail_context", None)
    if attach is None:
        return None
    reader = source or _SOURCE
    if reader is None or not conversation_id:
        attach("", slot=LIVE_PLAN_SLOT)
        return None
    snapshot = await reader(str(conversation_id), organization_id)
    if snapshot is None:
        attach("", slot=LIVE_PLAN_SLOT)
        return None
    since = tool_calls_since_plan_update(messages)
    block = render_live_plan(
        snapshot.tasks, tool_calls_since_update=since, settings=snapshot.settings
    )
    attach(block or "", slot=LIVE_PLAN_SLOT)
    if not block:
        return None
    return {
        "tasks": len(snapshot.tasks),
        "open": sum(1 for t in snapshot.tasks if t.status in OPEN_STATUSES),
        "tool_calls_since_update": since,
        "nudged": since >= max(1, int(snapshot.settings.nudge_after_tool_calls)),
        "chars": len(block),
    }


__all__ = [
    "LIVE_PLAN_KNOB_FEATURE",
    "LIVE_PLAN_SLOT",
    "LivePlanSettings",
    "LivePlanSnapshot",
    "LivePlanSource",
    "PlanTask",
    "get_live_plan_source",
    "render_live_plan",
    "set_live_plan_source",
    "stage_live_plan",
    "tool_calls_since_plan_update",
]
