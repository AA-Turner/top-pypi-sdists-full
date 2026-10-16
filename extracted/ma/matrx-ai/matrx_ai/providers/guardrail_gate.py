"""The automation guardrail gate — every automatic run stops at its limits (Arman, 2026-10-09:
"Any AI task that runs automatically ALWAYS has max cost and max turns set, even if very high.
Without them it cannot run automatically").

Same seam as the usage, run-approval and readiness gates: ``UnifiedAIClient._dispatch_with_billing_net``,
the one place every paid provider call passes. Unlike the run-approval gate it is asked on EVERY
paid call, because the limits it enforces are reached MID-run:

* max turns per run — the next paid call of a conversation that already used its turns;
* max cost per run — the next paid call of a run that already spent its budget;
* daily / weekly / monthly caps — the next paid call that would run past the automation's cap
  (the host pauses the automation);
* missing limits — an automation that uses AI but carries no max turns / max cost is refused.

A stop is a CALLER refusal (``is_caller_refusal``): never retried, rerouted or filed as a provider
failure. Every turn already taken keeps its output — the gate only refuses the NEXT call.

THE DECISION IS THE HOST'S. matrx-ai never imports aidream: the host registers, with
:func:`set_guardrail_host`, a synchronous ``(ctx) -> bool`` "is this run guarded" read, a
synchronous ``(ctx, profile) -> GuardrailStopError | None`` resolver (memory only — it also counts
the admitted call as a turn), and a synchronous ``(ctx, cost_usd) -> None`` accrual. With none
registered nothing is gated (announced once).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

AUTOMATION_GUARDRAIL = "automation_guardrail"
FIX_ACTION_RAISE_LIMIT = "raise_automation_limit"


class GuardrailStopError(Exception):
    """An automatic run reached (or lacks) one of its guardrail limits. The next call was not made."""

    is_caller_refusal = True
    http_status = 429

    def __init__(
        self,
        *,
        kind: str,
        subject_kind: str,
        subject_id: str,
        limit: float | int | None,
        observed: float | int | None,
        message: str,
        run_key: str = "",
        pauses: bool = False,
    ) -> None:
        self.kind = kind
        self.subject_kind = subject_kind
        self.subject_id = subject_id
        self.limit = limit
        self.observed = observed
        self.run_key = run_key
        self.pauses = pauses
        self.message = message
        self.code = AUTOMATION_GUARDRAIL
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
            "fix_action": FIX_ACTION_RAISE_LIMIT,
            "guardrail": self.kind,
            "limit": self.limit,
            "observed": self.observed,
            "subject_kind": self.subject_kind,
            "subject_id": self.subject_id,
            "pauses": self.pauses,
        }


Guarded = Callable[[Any], bool]
Resolver = Callable[[Any, Any], "GuardrailStopError | None"]
Accrue = Callable[[Any, float], None]
#: ``(ctx, profile, config) -> GuardrailStopError | None`` — asked on EVERY paid call, automation or
#: not: the platform kill switch, per-account daily ceilings, the per-call input-size cap.
EveryCall = Callable[[Any, Any, Any], "GuardrailStopError | None"]

_guarded: Guarded | None = None
_resolver: Resolver | None = None
_accrue: Accrue | None = None
_every_call: EveryCall | None = None
_every_call_tracked: Guarded | None = None
_every_call_accrue: Accrue | None = None
#: ``(ctx, usage) -> None`` — the provider's own token figures after a call (calibrates estimates).
_every_call_usage: Callable[[Any, Any], None] | None = None
#: ``(ctx, usage, estimate_usd) -> None`` — a paid call whose price is UNKNOWN (no resolvable
#: catalog price). The host alarms; caps and run limits accrue ``estimate_usd`` (conservative).
_every_call_unpriced: Callable[[Any, Any, float], None] | None = None
_unwired_announced = False


def set_guardrail_host(
    *,
    guarded: Guarded | None,
    resolver: Resolver | None,
    accrue: Accrue | None,
    every_call: EveryCall | None = None,
    every_call_tracked: Guarded | None = None,
    every_call_accrue: Accrue | None = None,
    every_call_usage: Callable[[Any, Any], None] | None = None,
    every_call_unpriced: Callable[[Any, Any, float], None] | None = None,
) -> None:
    """Host wiring: SYNCHRONOUS memory reads/writes. ``None`` everywhere unwires.

    ``guarded`` / ``resolver`` / ``accrue`` — the automation subject's own limits.
    ``every_call`` / ``every_call_tracked`` / ``every_call_accrue`` — platform-wide limits asked on
    every paid call (kill switch, account ceilings, input size)."""
    global _guarded, _resolver, _accrue, _every_call, _every_call_tracked, _every_call_accrue, _every_call_usage
    global _every_call_unpriced
    _every_call_usage = every_call_usage
    _every_call_unpriced = every_call_unpriced
    _guarded = guarded
    _resolver = resolver
    _accrue = accrue
    _every_call = every_call
    _every_call_tracked = every_call_tracked
    _every_call_accrue = every_call_accrue


def _is_guarded(ctx: Any) -> bool:
    if ctx is None or _guarded is None:
        return False
    try:
        return bool(_guarded(ctx))
    except Exception as exc:  # noqa: BLE001 — a broken read never blocks a run, loudly
        vcprint(
            f"[GuardrailGate] guarded() raised ({type(exc).__name__}: {exc}) — call admitted.",
            color="red",
            log_level="ERROR",
        )
        return False


def _tracked(ctx: Any) -> bool:
    if ctx is None or _every_call_tracked is None:
        return False
    try:
        return bool(_every_call_tracked(ctx))
    except Exception:  # noqa: BLE001
        return False


def admit_guardrails(profile: Any = None, config: Any = None) -> None:
    """Admit or stop the paid call about to be made. Asked on EVERY paid call."""
    global _unwired_announced
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None:
        return
    if _every_call is not None:
        try:
            stop = _every_call(ctx, profile, config)
        except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run
            vcprint(
                f"[GuardrailGate] every-call resolver raised ({type(exc).__name__}: {exc}) — call admitted.",
                color="red",
                log_level="ERROR",
            )
            stop = None
        if stop is not None:
            vcprint(f"[GuardrailGate] refused {stop.kind}: {stop.message}", color="yellow", log_level="WARNING")
            raise stop
    if _resolver is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[GuardrailGate] no host wired — automation turn / cost limits are NOT "
                "enforced in this process.",
                color="red",
                log_level="WARNING",
            )
        return
    if not _is_guarded(ctx):
        return
    try:
        stop = _resolver(ctx, profile)
    except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a run
        vcprint(
            f"[GuardrailGate] resolver raised ({type(exc).__name__}: {exc}) — call admitted.",
            color="red",
            log_level="ERROR",
        )
        return
    if stop is not None:
        vcprint(
            f"[GuardrailGate] stopped {stop.subject_kind}={stop.subject_id} "
            f"{stop.kind} limit={stop.limit} observed={stop.observed}",
            color="yellow",
            log_level="WARNING",
        )
        raise stop


async def note_paid_result(result: Any) -> None:
    """After a paid call: add its catalog cost to the guarded run. Never raises.

    An UNPRICED call (no resolvable catalog price) is never accrued as $0: it accrues a
    conservative estimate (``conservative_unpriced_cost``) and is reported to the host's
    ``every_call_unpriced`` hook, which alarms."""
    if (
        _accrue is None
        and _every_call_accrue is None
        and _every_call_usage is None
        and _every_call_unpriced is None
    ):
        return
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if _every_call_usage is not None and ctx is not None:
        try:
            _every_call_usage(ctx, getattr(result, "usage", None))
        except Exception:  # noqa: BLE001
            pass
    guarded = _accrue is not None and _is_guarded(ctx)
    tracked = _every_call_accrue is not None and _tracked(ctx)
    if not (guarded or tracked or _every_call_unpriced is not None):
        return
    try:
        from matrx_ai.providers.unified_client import catalog_cost_or_none

        usage = getattr(result, "usage", None)
        priced = await catalog_cost_or_none(usage)
        if priced is None and usage is not None:
            from matrx_ai.config.usage_config import conservative_unpriced_cost

            cost = conservative_unpriced_cost(usage)
            if _every_call_unpriced is not None:
                try:
                    _every_call_unpriced(ctx, usage, cost)
                except Exception as exc:  # noqa: BLE001 — the alarm never breaks a finished call
                    vcprint(
                        f"[GuardrailGate] unpriced-call hook raised ({type(exc).__name__}: {exc}).",
                        color="red",
                        log_level="ERROR",
                    )
        else:
            cost = float(priced or 0.0)
        if not (guarded or tracked):
            return
        if guarded:
            _accrue(ctx, cost)
        if tracked:
            _every_call_accrue(ctx, cost)
    except Exception as exc:  # noqa: BLE001
        vcprint(
            f"[GuardrailGate] could not accrue run cost ({type(exc).__name__}: {exc}).",
            color="red",
            log_level="ERROR",
        )


def guardrail_stop_in(source: Any, *, _max_depth: int = 16) -> GuardrailStopError | None:
    """The guardrail stop inside ``source`` (exception chain or ``.exception``), or None."""
    seen: set[int] = set()
    stack: list[Any] = [source]
    while stack and len(seen) < _max_depth:
        node = stack.pop()
        if node is None or id(node) in seen:
            continue
        seen.add(id(node))
        if isinstance(node, GuardrailStopError):
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
    "AUTOMATION_GUARDRAIL",
    "FIX_ACTION_RAISE_LIMIT",
    "GuardrailStopError",
    "admit_guardrails",
    "guardrail_stop_in",
    "note_paid_result",
    "set_guardrail_host",
]
