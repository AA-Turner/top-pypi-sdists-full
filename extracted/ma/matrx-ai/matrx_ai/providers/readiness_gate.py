"""The readiness gate — a mandate whose declared core inputs are missing is refused at its
first paid call, before any money is spent (Arman, 2026-10-08: "Never run automations on
anything without all of the core data being there — not silent, make it clear what is
required"; common-docs/policies/ai-model-and-spend-rules.md §5b).

Same seam as the usage gate and the run-approval gate: ``UnifiedAIClient._dispatch_with_billing_net``,
the one place every paid provider call passes. A gate only at service doors is bypassed by every
path that reaches a mandate another way (a workflow node, a direct agent run, a sub-agent);
this one cannot be.

THE DECISION IS THE HOST'S. matrx-ai never imports aidream: the host registers an ASYNC
``ctx -> ReadinessRefusedError | None`` resolver with :func:`set_readiness_resolver`. The host
knows which mandates declare core inputs, reads them for the run's subject (site / brand /
tracker) and records the visible verdict. Unlike the run-approval gate it is asked on EVERY
paid call — a sub-agent may run a different mandate inside the same request — so the host
memoizes its own "ready" answers per (request, mandate, subject). With none registered nothing
is gated (announced once).

A refusal is a CALLER refusal (``is_caller_refusal``): never retried, rerouted or filed as a
provider failure; its message names what is missing and where it is filled.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

AUTOMATION_NOT_READY = "automation_not_ready"
FIX_ACTION_FILL_INPUTS = "fill_required_inputs"


class ReadinessRefusedError(RuntimeError):
    """A mandate run refused because a declared core input is missing. Nothing was spent."""

    is_caller_refusal = True
    http_status = 409

    def __init__(self, *, mandate_key: str, summary: str, missing: list[dict[str, str]] | None = None) -> None:
        self.mandate_key = mandate_key
        self.summary = summary
        self.missing = list(missing or [])
        fills = "; ".join(f"{m.get('label')} ({m.get('fill_url')})" for m in self.missing if m.get("label"))
        self.message = f"{mandate_key}: {summary}" + (f". Fill in: {fills}" if fills else "")
        self.code = AUTOMATION_NOT_READY
        self.error_info = RetryableError(
            error_type=self.code,
            message=self.message,
            status_code=self.http_status,
            is_retryable=False,
            user_message=self.message,
            details=self.envelope(),
        )
        super().__init__(self.message)

    def envelope(self) -> dict[str, Any]:
        return {
            "error": self.code,
            "message": self.message,
            "fix_action": FIX_ACTION_FILL_INPUTS,
            "mandate_key": self.mandate_key,
            "summary": self.summary,
            "missing": self.missing,
        }


Resolver = Callable[[Any], Awaitable["ReadinessRefusedError | None"]]

_resolver: Resolver | None = None
_unwired_announced = False


def set_readiness_resolver(resolver: Resolver | None) -> None:
    """Host wiring: an ASYNC ``ctx -> ReadinessRefusedError | None``."""
    global _resolver
    _resolver = resolver


async def admit_readiness() -> None:
    """Refuse the paid call about to be made when the run's mandate is not ready."""
    global _unwired_announced
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return
    if _resolver is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[ReadinessGate] no resolver wired by the host — mandates with missing core "
                "inputs are NOT refused in this process.",
                color="red",
                log_level="WARNING",
            )
        return
    refusal = await _resolver(ctx)
    if refusal is not None:
        vcprint(f"[ReadinessGate] refused — {refusal.message}", color="yellow", log_level="WARNING")
        raise refusal


def readiness_refusal_in(source: Any, *, _max_depth: int = 16) -> ReadinessRefusedError | None:
    """The readiness refusal inside ``source`` (exception chain or ``.exception``), or None."""
    seen: set[int] = set()
    stack: list[Any] = [source]
    while stack and len(seen) < _max_depth:
        node = stack.pop()
        if node is None or id(node) in seen:
            continue
        seen.add(id(node))
        if isinstance(node, ReadinessRefusedError):
            return node
        for attr in ("exception", "terminal_exception"):
            carried = getattr(node, attr, None)
            if isinstance(carried, BaseException):
                stack.append(carried)
        if isinstance(node, BaseException):
            stack.append(node.__cause__)
            stack.append(node.__context__)
            members = getattr(node, "exceptions", None)
            if isinstance(members, (list, tuple)):
                stack.extend(m for m in members if isinstance(m, BaseException))
    return None


__all__ = [
    "AUTOMATION_NOT_READY",
    "FIX_ACTION_FILL_INPUTS",
    "ReadinessRefusedError",
    "admit_readiness",
    "readiness_refusal_in",
    "set_readiness_resolver",
]
