"""Layer 1 of the tool-result size gate — source-aware, graceful, at production.

Applied once to every result that carries real tool output, at the executor's
single convergence point. The model NEVER sees more than the soft cap from a tool
that did not self-manage; the full payload is cached for ``fetch_tool_result`` and
the firing is recorded so the gap becomes visible.

Three outcomes, three alarm tiers (see output_caps.py):
  * CANARY  — result in [CANARY, SOFT): passed, but recorded so we can replay and
              tune the cap empirically. Quiet (no console banner).
  * SOFT    — result ≥ SOFT and the tool did NOT declare ``output_self_capped``:
              truncate-with-notice + stash + alarm. For a tool we OWN this is a
              defect ("teach it to manage itself"); for an external/MCP tool it is
              expected (we cannot teach it) — the severity differs by ``tool_kind``.
  * (self-capped) — the tool managed its own size: trusted, untouched.

The ABSOLUTE ceiling (Layer 2) is enforced separately at the provider boundary
(MessageList.sanitize) so even results that bypass this executor are bounded.

The durable recording is an INJECTED sink (aidream wires an ops-triage writer in
package_integration.py) — matrx-ai must not import a host's DB layer. Absent a
sink, only the console sink runs, so the package stays standalone.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal

from matrx_utils import vcprint
from pydantic import BaseModel

from matrx_ai.tools.output_caps import (
    TOOL_RESULT_CANARY_CHARS,
    TOOL_RESULT_SOFT_CAP_CHARS,
    truncate_with_notice,
)
from matrx_ai.tools.output_overflow import stash_overflow

GateTier = Literal["canary", "soft_fired", "ceiling_fired"]
ToolKind = Literal["native", "external", "agent", "unknown"]


class ToolResultGateEvent(BaseModel):
    """A single gate firing — handed to every registered sink, typed end to end."""

    tier: GateTier
    tool_name: str
    tool_kind: ToolKind
    output_chars: int
    limit: int
    conversation_id: str | None = None
    call_id: str | None = None
    user_id: str | None = None


_SINKS: list[Callable[[ToolResultGateEvent], None]] = []


def register_tool_result_gate_sink(sink: Callable[[ToolResultGateEvent], None]) -> None:
    """Register a durable sink for gate firings (e.g. the ops-triage writer).

    Sinks must be best-effort and non-blocking; a sink that raises is isolated
    here so one bad sink never breaks dispatch.
    """
    _SINKS.append(sink)


def _emit(event: ToolResultGateEvent) -> None:
    for sink in _SINKS:
        try:
            sink(event)
        except Exception as exc:  # noqa: BLE001 — a sink must never break dispatch
            vcprint(f"[result_gate] sink raised, ignored: {exc}", color="yellow")


def _console_sink(event: ToolResultGateEvent) -> None:
    # Canary is informational and high-volume-ish — keep it quiet on the console
    # (the durable sink still records it for tuning). Soft/ceiling firings SCREAM.
    if event.tier == "canary":
        return
    owned = event.tool_kind in ("native", "agent")
    headline = (
        "🚨 TOOL-RESULT SIZE GATE FIRED — A TOOL DID NOT MANAGE ITS OWN OUTPUT"
        if owned
        else "⚠️ TOOL-RESULT SIZE GATE FIRED on an EXTERNAL tool (expected — cannot self-manage)"
    )
    fix = (
        "FIX THE TOOL: it must truncate its large fields itself (matrx_ai.tools."
        "output_caps.cap_text), offer the agent a way to fetch more, and set "
        "ToolResult.output_self_capped=True. The generic truncation here is BLUNT "
        "and can destroy a structured result — that is why this is an alarm."
        if owned
        else "No action needed per-firing; the result was truncated and cached for "
        "fetch_tool_result. Recorded for cost visibility."
    )
    vcprint(
        data={
            "tool": event.tool_name,
            "tool_kind": event.tool_kind,
            "output_chars": event.output_chars,
            "soft_cap": event.limit,
            "conversation_id": event.conversation_id,
            "call_id": event.call_id,
        },
        title=f"{headline}\n{fix}",
        color="red" if owned else "yellow",
        verbose=True,
    )


_SINKS.append(_console_sink)


def tool_kind_label(tool_type: Any) -> ToolKind:
    """Map a ToolType (or its string value) to the gate's coarse kind."""
    val = getattr(tool_type, "value", tool_type)
    if val in ("local",):
        return "native"
    if val in ("agent",):
        return "agent"
    if val in ("external", "external_handler"):
        return "external"
    return "unknown"


def apply_size_gate(
    content_dict: dict[str, Any],
    *,
    output_self_capped: bool,
    tool_name: str,
    tool_kind: ToolKind,
    conversation_id: str | None,
    user_id: str | None,
) -> tuple[dict[str, Any], bool]:
    """Gate ONE tool-result content dict (the output of ``to_tool_result_content``).

    Returns ``(content_dict, truncated)`` where ``truncated`` is True only when the
    soft cap fired (so the caller can inject ``fetch_tool_result`` for the next
    turn). Pure except for the best-effort overflow stash + sink emit. Cheap on the
    hot path: a single ``len`` when nothing's wrong. Never raises — a gate failure
    must not break a tool result.
    """
    try:
        content = content_dict.get("content")
        # Media / typed-block results carry references the model needs intact —
        # never touch a non-string content (image/audio/video blocks are a list).
        if not isinstance(content, str):
            return content_dict, False
        chars = len(content)
        call_id = str(content_dict.get("call_id") or "")

        # A self-capped tool owns its size — trusted, no soft cap, no canary noise.
        if output_self_capped:
            return content_dict, False

        if chars < TOOL_RESULT_SOFT_CAP_CHARS:
            # Shadow/canary band — passed, but record for empirical tuning.
            if chars >= TOOL_RESULT_CANARY_CHARS:
                _emit(
                    ToolResultGateEvent(
                        tier="canary",
                        tool_name=tool_name,
                        tool_kind=tool_kind,
                        output_chars=chars,
                        limit=TOOL_RESULT_SOFT_CAP_CHARS,
                        conversation_id=conversation_id,
                        call_id=call_id or None,
                        user_id=user_id,
                    )
                )
            return content_dict, False

        # Over the soft cap and NOT self-managed → gate it.
        stash_overflow(
            call_id=call_id,
            content=content,
            total_chars=chars,
            user_id=user_id,
            conversation_id=conversation_id,
            tool_name=tool_name,
        )
        new_content = truncate_with_notice(
            content,
            limit=TOOL_RESULT_SOFT_CAP_CHARS,
            total_chars=chars,
            call_id=call_id,
            tool_name=tool_name,
        )
        content_dict["content"] = new_content
        # output_chars on the CONTENT dict is "what the model now sees" (it feeds
        # the FE's total_chars_visible_to_model). Lower it to the truncated size so
        # the indicator is accurate; result.output_chars (the DB/true size) is a
        # separate field and stays untouched for persistence + canary replay.
        content_dict["output_chars"] = len(new_content)
        # Mark the preview so the UI / context-trim can tell this was gated, and
        # carry the true pre-truncation size for display.
        preview = content_dict.get("output_preview")
        if isinstance(preview, dict):
            preview["size_gated"] = True
            preview["true_output_chars"] = chars
        _emit(
            ToolResultGateEvent(
                tier="soft_fired",
                tool_name=tool_name,
                tool_kind=tool_kind,
                output_chars=chars,
                limit=TOOL_RESULT_SOFT_CAP_CHARS,
                conversation_id=conversation_id,
                call_id=call_id or None,
                user_id=user_id,
            )
        )
        return content_dict, True
    except Exception as exc:  # noqa: BLE001 — the gate must never break a result
        vcprint(f"[result_gate] apply_size_gate failed, returning ungated: {exc}", color="yellow")
        return content_dict, False
