"""Every piece of text the PLATFORM adds to what a model receives — registered, labeled, visible.

Owner rules (Arman, 2026-10-17): never add text to a person's message; nothing shapes a
prompt outside ``send_boundary.prepare_for_send``; the Builder shows everything the model
receives. A platform part that is not registered here has no purpose anyone can see, so it
does not ship (defects 25 + 27, 2026-10-18).

Two registries and one reader:

* ``PLATFORM_PARTS`` — the parts a FIRST send can carry (system additions, the per-turn
  ``<turn_context>`` block, the tail channel). ``platform_parts_in_request`` finds each in a
  captured wire request (the Builder Model view / dry run) and labels it with its id and source.
* ``MID_LOOP_PARTS`` — host-authored turns the executor adds only AFTER a provider response
  (empty reply, loop guard, change claim, required member, retry, queued injection). A dry
  run stops at the first send, so they are listed in the dry run as "may be added mid-loop"
  with their purpose and source. Every ``host_authored_user_turn(..., reason=...)`` in
  matrx_ai names a reason registered here. Guard:
  ``tests/test_every_platform_part_is_registered.py``.

The host (aidream) shows these in the Model view (``aidream/api/utils/preview.py``).
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class PlatformPart:
    id: str
    label: str
    channel: str  # system | turn_context | tail | host_turn
    source: str  # where the text is written
    purpose: str


PLATFORM_PARTS: dict[str, PlatformPart] = {
    p.id: p
    for p in (
        PlatformPart(
            "current_date",
            "Today's date",
            "system",
            "matrx_ai/instructions/core.py render_date_block",
            "the model knows today's date (off with include_date)",
        ),
        PlatformPart(
            "organization_catalog",
            "Organizations",
            "system",
            "matrx_ai/instructions/core.py inject_context_block (host: context catalog)",
            "the organizations, scope types and scopes the person belongs to",
        ),
        PlatformPart(
            "skills",
            "Skills",
            "system",
            "matrx_ai/skills/preamble.py render_preamble",
            "the skills the agent may load",
        ),
        PlatformPart(
            "kind_directives",
            "Kind Directives guidance",
            "system",
            "matrx_ai/instructions/core.py _actions_guidance (set by the host from the agent's actions)",
            "when and how to emit the Kind Directives the agent declares",
        ),
        PlatformPart(
            "turn_context",
            "Per-turn context",
            "turn_context",
            "matrx_ai/config/message_config.py render_turn_context (slots staged by the host)",
            "this turn's live date, selection, value list, platform notes; its own host turn after the "
            "newest message on every provider (the end of the system message only for a model the "
            "catalog declares strict_role_alternation)",
        ),
        PlatformPart(
            "live_plan",
            "Task list",
            "tail",
            "matrx_ai/config/live_plan.py render_live_plan (with its update reminder after N tool calls)",
            "the agent's own open task list, after a tool result, so it keeps the plan current",
        ),
    )
}


MID_LOOP_PARTS: dict[str, PlatformPart] = {
    p.id: p
    for p in (
        PlatformPart(
            "empty_reply_continuation",
            "Empty reply: ask for the answer",
            "host_turn",
            "matrx_ai/orchestrator/executor.py _drop_blank_turn_for_continuation",
            "a turn ended with no visible reply: once per run, ask for the answer instead of failing",
        ),
        PlatformPart(
            "text_tool_call",
            "Tool call written as text",
            "host_turn",
            "matrx_ai/orchestrator/executor.py (orchestrator/text_tool_calls.py)",
            "a reply typed a tool call as text: once per run, the markup is removed and the model re-asked",
        ),
        PlatformPart(
            "iteration_ceiling_approaching",
            "Step limit approaching",
            "host_turn",
            "matrx_ai/orchestrator/executor.py _ceiling_approaching_notice",
            "a run nears its step limit: tells the model how many steps are left so it can finish",
        ),
        PlatformPart(
            "iteration_ceiling_wrap_up",
            "Step limit reached: write it up",
            "host_turn",
            "matrx_ai/orchestrator/executor.py _ceiling_wrap_up_notice",
            "a run hit its step limit: one tool-less turn writes what was done and what is left",
        ),
        PlatformPart(
            "visual_map_repair",
            "Visual map: repair the diagram",
            "host_turn",
            "matrx_ai/orchestrator/visual_map_repair.py repair_notice",
            "a visual map failed validation: one tool-less repair turn names what to fix",
        ),
        PlatformPart(
            "strict_json_schema_repair",
            "Structured output: fix the JSON",
            "host_turn",
            "matrx_ai/graph_nodes/_strict_json.py llm_messages_to_pydantic_measured",
            "a strict-JSON answer failed schema validation: one repair turn names the error",
        ),
        PlatformPart(
            "required_member_gate",
            "Required member not consulted",
            "host_turn",
            "matrx_ai/orchestrator/executor.py (Orchestra required members)",
            "an Orchestra declares members that must be consulted before the final answer",
        ),
        PlatformPart(
            "change_claim_gate",
            "Claimed changes without a write",
            "host_turn",
            "matrx_ai/orchestrator/change_claims.py",
            "the reply says changes were made but no write tool succeeded",
        ),
        PlatformPart(
            "loop_guard_approaching",
            "Tool failures: caution",
            "host_turn",
            "matrx_ai/orchestrator/executor.py loop guard (knobs orchestration.loop_guard)",
            "most recent tool calls failed: change approach before tools are disabled",
        ),
        PlatformPart(
            "loop_guard_standoff_continue",
            "Tool failures: one more try",
            "host_turn",
            "matrx_ai/orchestrator/executor.py loop guard standoff verdict",
            "a failing tool is given one reasoned second chance",
        ),
        PlatformPart(
            "loop_guard_tool_disabled",
            "Tool disabled after failures",
            "host_turn",
            "matrx_ai/orchestrator/loop_guard.py disabled_tool_notice",
            "a tool that kept failing is withdrawn for this run",
        ),
        PlatformPart(
            "loop_guard_tools_disabled",
            "Tools disabled: answer honestly",
            "host_turn",
            "matrx_ai/orchestrator/executor.py loop guard",
            "too many failures: stop calling tools and tell the person what happened",
        ),
        PlatformPart(
            "retry_after_failed_call",
            "Retry after a failed call",
            "host_turn",
            "matrx_ai/orchestrator/recovery_logic.py",
            "a retryable provider finish: name the tools still available",
        ),
        PlatformPart(
            "injection",
            "Queued message",
            "host_turn",
            "matrx_ai/tools/dynamic_drain.py (reason injection:<kind>)",
            "a message queued for this live conversation (steer, collaborator write-back)",
        ),
    )
}


#: Host-authored turns that START a turn (``HostTurn(reason=...)``): the activation text is
#: not typed by a person, so its reason is registered here and shown in the Model view.
HOST_TURN_PARTS: dict[str, PlatformPart] = {
    p.id: p
    for p in (
        PlatformPart(
            "inbox_driver",
            "Queued message wakes the thread",
            "host_turn",
            "aidream/services/tooling/inbox_driver.py (the queued row's own text)",
            "a message queued for a thread nobody is in becomes that turn's input, never the "
            "person's words",
        ),
        PlatformPart(
            "applets.build fix round",
            "Applet build: fix the last check",
            "host_turn",
            "matrx-frontend features/applets-host/builder/build-session.ts fixHostTurn",
            "the applet builder asks the agent to fix the one check its last answer failed",
        ),
    )
}


def host_turn_reason_registered(reason: str) -> bool:
    """True when a ``HostTurn`` reason is registered (or is a registered mid-loop reason)."""
    return reason in HOST_TURN_PARTS or mid_loop_reason_registered(reason)


def mid_loop_reason_registered(reason: str) -> bool:
    """True when ``reason`` names a registered mid-loop part (``injection:<kind>`` by prefix)."""
    base = reason.split(":", 1)[0] if reason.startswith("injection:") else reason
    return base in MID_LOOP_PARTS


def _patterns() -> list[tuple[str, re.Pattern[str]]]:
    from matrx_ai.instructions.core import DATE_BLOCK_CLOSE, DATE_BLOCK_OPEN

    return [
        ("current_date", re.compile(re.escape(DATE_BLOCK_OPEN) + r".*?" + re.escape(DATE_BLOCK_CLOSE), re.S)),
        ("organization_catalog", re.compile(r"<org_catalog\b.*?</org_catalog>", re.S)),
        ("skills", re.compile(r"<available_skills>.*?</available_skills>", re.S)),
        ("kind_directives", re.compile(r"## Available Kind Directives\n.*?(?=\n## |\Z)", re.S)),
        ("turn_context", re.compile(r'<turn_context source="platform"[^>]*>.*?</turn_context>', re.S)),
        ("live_plan", re.compile(r'<your_plan source="platform">.*?</your_plan>', re.S)),
    ]


def _strings(node: Any, path: str = "") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if isinstance(node, str):
        out.append((path or "$", node))
    elif isinstance(node, dict):
        for key, value in node.items():
            out.extend(_strings(value, f"{path}.{key}" if path else str(key)))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            out.extend(_strings(value, f"{path}[{i}]"))
    return out


def platform_parts_in_request(payload: Any, *, skip_keys: tuple[str, ...] = ("tools",)) -> list[dict[str, Any]]:
    """Every registered platform part found in a captured request, labeled, verbatim.

    Each entry: ``{id, label, channel, source, purpose, where, text}`` (``where`` is the JSON
    path of the string it sits in). Tool declarations are skipped (they are tools, not text).
    """
    found: list[dict[str, Any]] = []
    patterns = _patterns()
    for where, text in _strings(payload):
        if any(where == k or where.startswith(f"{k}[") or where.startswith(f"{k}.") for k in skip_keys):
            continue
        for part_id, pattern in patterns:
            for match in pattern.finditer(text):
                part = PLATFORM_PARTS[part_id]
                found.append({**asdict(part), "where": where, "text": match.group(0)})
    return found


def without_platform_parts(text: str) -> str:
    """``text`` with every registered platform part removed (what is left is authored or typed)."""
    for _part_id, pattern in _patterns():
        text = pattern.sub("", text)
    return text


def mid_loop_parts() -> list[dict[str, Any]]:
    """The host turns a run MAY add after a provider response, for the Model view."""
    return [asdict(p) for p in MID_LOOP_PARTS.values()]


__all__ = [
    "HOST_TURN_PARTS",
    "host_turn_reason_registered",
    "MID_LOOP_PARTS",
    "PLATFORM_PARTS",
    "PlatformPart",
    "mid_loop_parts",
    "mid_loop_reason_registered",
    "platform_parts_in_request",
    "without_platform_parts",
]
