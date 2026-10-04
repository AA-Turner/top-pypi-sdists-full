"""The usage gate — the ONE check before money is spent, answered from memory.

THE LAW (Arman, 2026-10-03; common-docs/systems/platform/entitlements-knobs/
USAGE-GATE.md). Every person has a usage state ``ok`` / ``near`` / ``over``,
computed by ONE database function. The server keeps it in memory; at the paid
call it reads ONLY that memory:

* cached ``over`` (and the host says enforcement is on) → refuse BEFORE any
  provider is called, with a refusal that names the limit, ``required_tier``
  and ``fix_action: "upgrade_plan"``;
* cached ``near`` → run, and tell the client (an ``info`` event,
  ``code="usage_state"``, on the request's own stream);
* nothing cached → run, fully honored. A miss never refuses, waits or fetches;
* a running request is NEVER stopped: the decision is made once, at the
  request's first paid call, and every later paid call carrying the same
  ``AppContext.request_id`` (sub-agents, workflow steps, tool-loop iterations,
  retries) is admitted without asking again — even if the person crosses the
  line mid-request.

ADMISSION SURVIVES PROCESSES. The memo above is per process. A request that
pauses (client tool results, an answer to a question) and resumes keeps its
request id but may land on another ECS task or after a release restart, where
the memo is empty. So admission also rides ON THE CONTEXT:
``AppContext.usage_admitted``. The server code that resumes an existing request
(``prepare_resume_conversation``, which has already proved the request exists
and had answered delegated calls) sets it, and every fork inherits it; a
context carrying it is never refused. No database read is added for gating —
the resume path already loads the request it resumes. One user operation that
mints an internal request id for a later step (e.g. Knowledge Ask's answer
step) carries its parent's admission with :func:`admission_of` so the step is
never refused after earlier steps were paid for.

WHERE IT RUNS. ``UnifiedAIClient._dispatch_with_billing_net`` — the seam every
paid request/response provider call already passes (chat, media, TTS, STT,
extraction, embeddings, decisions, rerank) — calls :func:`admit_paid_call`
before its admission slot. :func:`precheck_usage` is the same memory read at
the request boundary (``conversation_gate.ensure_user_request_exists``), so an
``over`` person's new message is refused before the turn is stored.

THE MEMORY IS THE HOST'S. matrx-ai never imports aidream: the host registers a
SYNCHRONOUS resolver with :func:`set_usage_verdict_resolver`. It is synchronous
on purpose — a coroutine could await a database read, a plain function cannot,
so "no database read on the request path" is enforced by the type, not by a
comment. A host that registers none is announced once and nothing is gated.

WHO IS GATED. A person's request: any context carrying a ``user_id`` whose
``origin_class`` is not machine work (``system`` / ``scheduled``). Guests are
ordinary people here — their state comes from the ``guest`` plan's windows.
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_utils import vcprint

from matrx_ai.providers.errors import RetryableError

UsageState = Literal["ok", "near", "over"]

#: The refusal codes. A guest keeps the code the web client's ONE sign-up
#: reminder already listens for; a signed-in person gets the plan refusal.
USAGE_LIMIT_REACHED = "usage_limit_reached"
GUEST_AI_ALLOWANCE_USED = "guest_ai_allowance_used"
GUEST_PLAN_KEY = "guest"
FIX_ACTION_UPGRADE_PLAN = "upgrade_plan"
USAGE_INFO_CODE = "usage_state"

USAGE_LIMIT_MESSAGE = "You've reached your AI usage limit for now. Upgrade your plan to keep going."
GUEST_LIMIT_MESSAGE = "You've used your free AI tries. Create a free account to keep going."
USAGE_NEAR_MESSAGE = "You're close to your AI usage limit."

#: Machine work never pays out of a person's allowance at this seam.
UNGATED_ORIGIN_CLASSES: frozenset[str] = frozenset({"system", "scheduled"})

#: Request ids already decided (admitted). Bounded; an evicted id is asked
#: again, which can only matter for a request still running after 50k newer
#: ones were admitted in this process.
_ADMITTED_MEMO_MAX = 50_000


@dataclass(frozen=True)
class UsageVerdict:
    """What the host's memory says about one person, right now.

    ``refuse`` is the host's whole decision (cached ``over`` AND enforcement
    on); ``usage`` is the ``billing.user_usage_state`` jsonb verbatim, carried
    into the refusal and the ``near`` notice so the client never recomputes.
    """

    state: UsageState
    refuse: bool
    enforced: bool
    usage: dict[str, Any] = field(default_factory=dict)


VerdictResolver = Callable[[str], "UsageVerdict | None"]


def _binding_window(usage: dict[str, Any]) -> dict[str, Any]:
    period = usage.get("binding_period")
    for window in usage.get("windows") or []:
        if isinstance(window, dict) and window.get("period") == period:
            return window
    return {}


class UsageLimitReachedError(Exception):
    """A person whose cached usage state is ``over``. Raised BEFORE any provider call.

    A caller refusal, not a provider failure: ``is_caller_refusal`` tells the
    executor and the stream crash handler not to retry, reroute or file it as
    an incident. ``error_info`` carries the stable code and the numbers so every
    stream path emits the same thing; ``envelope()`` is the HTTP 402 body.
    """

    is_caller_refusal = True
    http_status = 402

    def __init__(self, usage: dict[str, Any]) -> None:
        self.usage = dict(usage or {})
        self.is_guest = self.usage.get("plan_key") == GUEST_PLAN_KEY
        self.code = GUEST_AI_ALLOWANCE_USED if self.is_guest else USAGE_LIMIT_REACHED
        self.message = GUEST_LIMIT_MESSAGE if self.is_guest else USAGE_LIMIT_MESSAGE
        details = self.envelope()
        details.pop("error", None)
        details.pop("message", None)
        self.error_info = RetryableError(
            error_type=self.code,
            message=self.message,
            status_code=self.http_status,
            is_retryable=False,
            user_message=self.message,
            details=details,
        )
        super().__init__(self.message)

    def envelope(self) -> dict[str, Any]:
        window = _binding_window(self.usage)
        return {
            "error": self.code,
            "message": self.message,
            "fix_action": FIX_ACTION_UPGRADE_PLAN,
            "required_tier": self.usage.get("required_tier"),
            "plan_key": self.usage.get("plan_key"),
            "state": self.usage.get("state", "over"),
            "binding_period": self.usage.get("binding_period"),
            "limit": window.get("limit"),
            "used": window.get("used"),
            "resets_at": self.usage.get("resets_at"),
            "usage": self.usage,
        }


_resolver: VerdictResolver | None = None
_unwired_announced = False
_admitted: OrderedDict[str, None] = OrderedDict()


def set_usage_verdict_resolver(resolver: VerdictResolver | None) -> None:
    """Host wiring: a SYNCHRONOUS ``user_id -> UsageVerdict | None`` memory read."""
    global _resolver
    _resolver = resolver


def reset_usage_gate_state() -> None:
    """Tests: forget which requests were already admitted."""
    _admitted.clear()


def _remember(request_id: str) -> None:
    _admitted[request_id] = None
    _admitted.move_to_end(request_id)
    while len(_admitted) > _ADMITTED_MEMO_MAX:
        _admitted.popitem(last=False)


def _already_admitted(ctx: Any) -> bool:
    if bool(getattr(ctx, "usage_admitted", False)):
        return True
    request_id = str(getattr(ctx, "request_id", "") or "")
    return bool(request_id) and request_id in _admitted


def admission_of(ctx: Any = None) -> bool:
    """Whether ``ctx`` (default: the ambient context) belongs to an operation
    already admitted — in this process (memo) or carried (``usage_admitted``).

    For server code that mints a NEW request id for a later step of the SAME
    user operation: pass the result as ``usage_admitted=`` on the step's context
    so the step inherits the parent's admission instead of being judged anew.
    """
    if ctx is None:
        from matrx_ai.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    return ctx is not None and _already_admitted(ctx)


def _gated_person(ctx: Any) -> str | None:
    if ctx is None:
        return None
    if str(getattr(ctx, "origin_class", "") or "") in UNGATED_ORIGIN_CLASSES:
        return None
    user_id = str(getattr(ctx, "user_id", "") or "").strip()
    return user_id or None


def _verdict_for(user_id: str) -> UsageVerdict | None:
    global _unwired_announced
    if _resolver is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[UsageGate] no usage verdict resolver wired by the host — AI usage is "
                "NOT gated in this process.",
                color="red",
                log_level="WARNING",
            )
        return None
    try:
        return _resolver(user_id)
    except Exception as exc:  # noqa: BLE001 — a broken memory read never blocks a person
        vcprint(
            f"[UsageGate] verdict resolver raised ({type(exc).__name__}: {exc}) — "
            "honoring the request as uncached.",
            color="red",
            log_level="ERROR",
        )
        return None


async def _tell_near(ctx: Any, verdict: UsageVerdict) -> None:
    """The ``near`` notice on the request's own stream (best-effort, never raises)."""
    emitter = getattr(ctx, "emitter", None)
    if emitter is None:
        return
    try:
        from matrx_connect.context.events import InfoPayload

        await emitter.send_info(
            InfoPayload(
                code=USAGE_INFO_CODE,
                system_message=(
                    f"usage state {verdict.state} (plan={verdict.usage.get('plan_key')}, "
                    f"binding_period={verdict.usage.get('binding_period')})"
                ),
                user_message=USAGE_NEAR_MESSAGE,
                metadata={"usage": verdict.usage, "enforced": verdict.enforced},
            )
        )
    except Exception as exc:  # noqa: BLE001 — a notice never breaks the run
        vcprint(f"[UsageGate] near notice not emitted: {exc!r}", color="yellow")


async def admit_paid_call() -> None:
    """Admit or refuse the paid call about to be made — from memory only.

    Raises :class:`UsageLimitReachedError` only when this is the request's
    FIRST paid call and the host's memory says ``over`` with enforcement on.
    """
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    user_id = _gated_person(ctx)
    if user_id is None:
        return
    request_id = str(getattr(ctx, "request_id", "") or "")
    if _already_admitted(ctx):
        return  # a running request is never stopped
    verdict = _verdict_for(user_id)
    if verdict is not None and verdict.refuse:
        vcprint(
            f"[UsageGate] refused user={user_id[:8]}… request={request_id[:8]}… — cached "
            f"state over (plan={verdict.usage.get('plan_key')}, "
            f"period={verdict.usage.get('binding_period')})",
            color="yellow",
            log_level="WARNING",
        )
        raise UsageLimitReachedError(verdict.usage)
    if request_id:
        _remember(request_id)
    if verdict is not None and verdict.state in ("near", "over"):
        await _tell_near(ctx, verdict)


def precheck_usage() -> None:
    """The same memory read at the request boundary, before the turn is stored.

    Never records the request as admitted (the paid-call seam does that); a
    request already admitted is never refused here either.
    """
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    user_id = _gated_person(ctx)
    if user_id is None:
        return
    if _already_admitted(ctx):
        return
    verdict = _verdict_for(user_id)
    if verdict is not None and verdict.refuse:
        raise UsageLimitReachedError(verdict.usage)


__all__ = [
    "FIX_ACTION_UPGRADE_PLAN",
    "GUEST_AI_ALLOWANCE_USED",
    "GUEST_LIMIT_MESSAGE",
    "UNGATED_ORIGIN_CLASSES",
    "USAGE_INFO_CODE",
    "USAGE_LIMIT_MESSAGE",
    "USAGE_LIMIT_REACHED",
    "UsageLimitReachedError",
    "UsageVerdict",
    "admission_of",
    "admit_paid_call",
    "precheck_usage",
    "reset_usage_gate_state",
    "set_usage_verdict_resolver",
]
