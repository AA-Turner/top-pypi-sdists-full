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

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
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


# --------------------------------------------------------------------------- #
# THE PER-CALL SPEND CAP (2026-10-27)                                          #
# --------------------------------------------------------------------------- #
#
# A caller that must keep EACH call cheap (a workflow AI step's ``max_call_cost_usd``) opens
# :func:`call_spend_cap_scope`; every paid call made inside it is priced BEFORE it is sent — the
# exact outgoing request's estimated input tokens plus its output ceiling (``max_output_tokens``)
# at the model's catalog price — and refused over the cap. A call that cannot be priced (no
# output ceiling, no catalog price) is refused too: a cap that cannot be checked is not a cap.
# Nothing is spent on a refused call. No scope: one ContextVar read.

CALL_SPEND_CAP = "call_spend_cap"
FIX_ACTION_RAISE_CALL_CAP = "raise_call_spend_cap"


@dataclass(frozen=True)
class CallSpendCap:
    max_usd: float
    subject: str


_CALL_SPEND_CAP: ContextVar[CallSpendCap | None] = ContextVar("matrx_call_spend_cap", default=None)


@contextmanager
def call_spend_cap_scope(max_usd: float | None, *, subject: str) -> Iterator[CallSpendCap | None]:
    """Cap every paid call inside the block at ``max_usd`` (``None`` / ``<= 0``: no cap)."""
    if max_usd is None or max_usd <= 0:
        yield None
        return
    cap = CallSpendCap(max_usd=float(max_usd), subject=subject)
    token = _CALL_SPEND_CAP.set(cap)
    try:
        yield cap
    finally:
        _CALL_SPEND_CAP.reset(token)


def current_call_spend_cap() -> CallSpendCap | None:
    """The per-call cap open around this call, if any (the send boundary bounds its document
    ceiling by it — ``send_boundary._bound_ceiling_by_spend_cap``)."""
    return _CALL_SPEND_CAP.get()


def _call_cap_stop(cap: CallSpendCap, message: str, observed: float | None) -> GuardrailStopError:
    stop = GuardrailStopError(
        kind=CALL_SPEND_CAP,
        subject_kind="workflow_step",
        subject_id=cap.subject,
        limit=cap.max_usd,
        observed=observed,
        message=message,
    )
    stop.error_info.details["fix_action"] = FIX_ACTION_RAISE_CALL_CAP
    return stop


def estimate_call_usd(profile: Any, config: Any) -> tuple[float | None, str, int, int]:
    """``(usd | None, model, input_tokens, output_tokens)`` for the call about to be sent: the
    ONE prompt estimator over the exact config, plus its output ceiling, at the catalog price."""
    from matrx_ai.config.context_preflight import estimate_prompt_tokens
    from matrx_ai.config.usage_config import TokenUsage, _get_db_pricing_lookup

    model = str(
        getattr(profile, "model_name", None)
        or getattr(config, "matrx_model_name", None)
        or getattr(config, "model", None)
        or ""
    )
    input_tokens = max(1, int(estimate_prompt_tokens(config)))
    output_tokens = int(getattr(config, "max_output_tokens", None) or 0)
    if not model or output_tokens <= 0:
        return None, model, input_tokens, output_tokens
    usage = TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        matrx_model_name=model,
        offering_id=str(getattr(profile, "offering_id", None) or ""),
    )
    cost = usage.calculate_catalog_cost(_get_db_pricing_lookup())
    return (None if cost is None else float(cost)), model, input_tokens, output_tokens


def admit_call_spend_cap(profile: Any = None, config: Any = None) -> None:
    """Refuse the call about to be sent when it is estimated over the open per-call cap."""
    cap = _CALL_SPEND_CAP.get()
    if cap is None:
        return
    if config is None:
        raise _call_cap_stop(
            cap,
            f"{cap.subject} has a ${cap.max_usd:.2f} cap per AI call, but this call carries no "
            "request to price. Nothing was sent or charged.",
            None,
        )
    try:
        usd, model, input_tokens, output_tokens = estimate_call_usd(profile, config)
    except Exception as exc:  # noqa: BLE001 — an unpriceable call is refused, never waved through
        usd, model, input_tokens, output_tokens = None, "", 0, 0
        vcprint(f"[GuardrailGate] call spend cap could not price the call: {exc!r}", color="red")
    if output_tokens <= 0:
        raise _call_cap_stop(
            cap,
            f"{cap.subject} has a ${cap.max_usd:.2f} cap per AI call, but the call has no longest-"
            "answer limit, so its price cannot be checked. Set the step's max output tokens. "
            "Nothing was sent or charged.",
            None,
        )
    if usd is None:
        raise _call_cap_stop(
            cap,
            f"{cap.subject} has a ${cap.max_usd:.2f} cap per AI call, but {model or 'its model'} has "
            "no catalog price, so the call cannot be checked. Nothing was sent or charged.",
            None,
        )
    if usd > cap.max_usd:
        raise _call_cap_stop(
            cap,
            f"{cap.subject} would cost about ${usd:.3f} on {model} ({input_tokens:,} tokens in, up "
            f"to {output_tokens:,} out), over its ${cap.max_usd:.2f} cap per AI call. Nothing was "
            "sent or charged.",
            round(usd, 6),
        )


def admit_guardrails(profile: Any = None, config: Any = None) -> None:
    """Admit or stop the paid call about to be made. Asked on EVERY paid call."""
    global _unwired_announced
    from matrx_ai.context.app_context import try_get_app_context

    admit_call_spend_cap(profile, config)
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


def _usage_named_by_profile(usage: Any, profile: Any) -> Any:
    """``usage`` as a catalog-priceable ``TokenUsage`` named by the dispatched route.

    A provider whose wire usage carries only counters (TypeSafe's ``{input_tokens, output_tokens}``
    on a decision call) has no model name, so pricing it read "unknown model" and raised a false
    ``model_call_unpriced`` alarm on every decision call (2026-10-16, Jev decisions) while the
    same call was priced correctly a step later. The dispatcher already knows the route: name it."""
    if usage is None or profile is None or getattr(usage, "matrx_model_name", None):
        return usage
    model_name = getattr(profile, "model_name", None)
    if not model_name:
        return usage
    from matrx_ai.config.usage_config import TokenUsage

    input_tokens = int(getattr(usage, "input_tokens", 0) or 0)
    output_tokens = int(getattr(usage, "output_tokens", 0) or 0)
    return TokenUsage(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        matrx_model_name=str(model_name),
        provider_model_name=str(getattr(profile, "provider_model_id", None) or model_name),
        api=str(getattr(profile, "vendor", "") or ""),
        offering_id=str(getattr(profile, "offering_id", None) or ""),
        offering_route=str(getattr(profile, "resolution_route", None) or ""),
        raw_usage={"input_tokens": input_tokens, "output_tokens": output_tokens},
    )


async def note_paid_result(result: Any, *, profile: Any = None) -> None:
    """After a paid call: add its catalog cost to the guarded run. Never raises.

    An UNPRICED call (no resolvable catalog price) is never accrued as $0: it accrues a
    conservative estimate (``conservative_unpriced_cost``) and is reported to the host's
    ``every_call_unpriced`` hook, which alarms. ``profile`` (the dispatched route) names a usage
    whose provider reported only counters, so it prices against the right offering."""
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
        if usage is not None:
            from matrx_ai.providers.unified_client import billable_usage

            try:
                usage = billable_usage(usage)  # STT carries seconds: price it in its basis's units
            except Exception:  # noqa: BLE001 — an unconvertible usage stays unpriced and alarms
                pass
            usage = _usage_named_by_profile(usage, profile)
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
    "CALL_SPEND_CAP",
    "CallSpendCap",
    "admit_call_spend_cap",
    "call_spend_cap_scope",
    "current_call_spend_cap",
    "estimate_call_usd",
    "FIX_ACTION_RAISE_LIMIT",
    "GuardrailStopError",
    "admit_guardrails",
    "guardrail_stop_in",
    "note_paid_result",
    "set_guardrail_host",
]
