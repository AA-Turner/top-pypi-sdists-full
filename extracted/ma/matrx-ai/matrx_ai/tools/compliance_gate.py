"""The compliance gate every tool call passes before it runs (the runtime backstop of rule H).

The host decides which tools a regulated run may use (aidream: HIPAA mode, TOOL-SOURCES.md rule H)
and removes the rest from the toolset before the model sees it. A tool can still reach the executor
another way — the discovery gateway (``use_tool``), a tool queued mid-run, a nested agent, a
misconfigured agent — so ``ToolExecutor.execute`` asks this gate on EVERY call, delegated client
tools included, exactly like the admin-only backstop.

The package never decides who is regulated: the host injects one async callable with
:func:`configure_tool_compliance_gate`. With no gate configured every tool runs (a bare install).
A gate that RAISES refuses the call (fail closed): a regulated run must never run an unchecked tool
because the check itself broke.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

#: ``gate(canonical_tool_name, app_context_or_None) -> refusal message | None``.
ToolComplianceGate = Callable[[str, Any], Awaitable[str | None]]

#: The error type a refused call carries (the host's own refusal code).
COMPLIANCE_REFUSAL_ERROR_TYPE = "hipaa_not_covered"

_gate: ToolComplianceGate | None = None


def configure_tool_compliance_gate(gate: ToolComplianceGate | None) -> None:
    """Install (or clear, with ``None``) the host's per-call compliance gate."""
    global _gate
    _gate = gate


def tool_compliance_gate_configured() -> bool:
    return _gate is not None


async def tool_compliance_refusal(canonical_name: str, app_ctx: Any) -> str | None:
    """The sentence that refuses this call, or ``None`` when it may run."""
    if _gate is None:
        return None
    try:
        return await _gate(canonical_name, app_ctx)
    except Exception as exc:  # noqa: BLE001 — fail closed, loudly, with the cause carried
        from matrx_connect.streaming.error_capture import capture_error

        from matrx_ai.utils.carried_failure import FailureText

        cause = f"{type(exc).__name__}: {exc}"
        vcprint(
            f"[compliance_gate] the compliance check for tool {canonical_name!r} failed ({cause}) — "
            "refusing the call rather than running it unchecked",
            color="red",
        )
        await capture_error(exc, kind="tool_compliance_gate_failed", tool_name=canonical_name)
        return FailureText(
            f"Tool '{canonical_name}' could not be checked against this organization's compliance "
            f"rules, so it was not run. The check failed: {cause}",
            exc,
        )
