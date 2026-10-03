"""Guest AI allowance — the ONE gate on a signed-out visitor's paid AI use.

THE PRODUCT RULE (owner, 2026-10-02): every feature is free forever for
guests. The ONLY limit is AI usage, because AI costs money. A guest gets a
small number of free AI actions; the next one is refused with a friendly
"create a free account to keep going". Non-AI use is never limited, and a
signed-in person never reaches this code's counting branch at all.

WHERE IT RUNS. ``UnifiedAIClient._dispatch_with_billing_net`` calls
:func:`admit_guest_ai_action` before its admission slot — the seam every paid
request/response provider call already passes through (chat, media, TTS, STT,
extraction, embeddings, decisions, rerank). Gating there, rather than at any
of the dozen route boundaries, means a new AI route written tomorrow is gated
the moment it spends money, and a run with ``store=False`` (no
``cx_user_request`` row) is gated exactly like one that persists.

ONE USER ACTION = ONE COUNT. The unit is the carried ``AppContext.request_id``
— the id the auth boundary minted for this HTTP request. Every sub-agent,
workflow step, tool-loop iteration, retry and background helper spawned
inside the action inherits it (``fork_for_child_agent`` /
``fork_for_workflow_step`` keep it), so only the FIRST paid call of a request
is counted. A per-request_id lock serialises concurrent first calls within a
process; the durable ledger row keyed by the request id makes the count
idempotent across processes too.

THE LEDGER. One ``users.guest_execution_log`` row per admitted action
(``resource_type='ai_action'``, ``resource_id=request_id``), keyed to the
guest's ``users.guest_executions`` row. Durable, per guest identity — opening
a new conversation, a new tab or a new feature cannot reset it.

THE NUMBER is the host's: :func:`set_guest_ai_allowance_resolver` (aidream
wires the platform knob ``auth.guest_ai / free_ai_actions``). A host that
wires none is announced once and nothing is gated — a stand-in that says so.

WHAT COUNTS (coordinator ruling, 2026-10-02): an AI action a PERSON triggers —
a chat message, an agent run, a tutor answer, generated flashcards. Embeddings
a guest's FILE INGEST produces (``/files/{id}/ingest``, ``/ingest/stream``,
``/refresh``, automatic processing on upload) do NOT count: they are matrx-rag
embedding calls that never reach this seam, deliberately left outside it, so
uploading a document never spends a free try. RAG embeddings inside an agent's
knowledge tool ride the chat action that was already counted.

THE BOUNDARY PRE-CHECK. :func:`precheck_guest_ai_action` is the read-only twin,
called where a NEW user request is first recorded
(``conversation_gate.ensure_user_request_exists``, during route prep), so a
used-up guest's message is refused as HTTP 403 before the turn is stored. The
seam stays the authority that counts.

FAIL BEHAVIOUR. If the allowance or the ledger cannot be read, the action is
ALLOWED and the failure is recorded loudly (``system_error`` kind
``guest_ai_allowance_unreadable``): a guest trying the product beats a broken
page, and the record makes the gap visible instead of silent.
"""

from __future__ import annotations

import asyncio
from collections import OrderedDict
from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import detached_task, vcprint

from matrx_ai.providers.errors import RetryableError

GUEST_AI_ALLOWANCE_USED = "guest_ai_allowance_used"
GUEST_AI_ALLOWANCE_MESSAGE = "You've used your free AI tries. Create a free account to keep going."
LEDGER_RESOURCE_TYPE = "ai_action"

#: Process memo of request ids already admitted (or already decided as
#: fail-open). Bounded; an evicted id falls back to the durable ledger check.
_ADMITTED_MEMO_MAX = 50_000


class GuestAIAllowanceUsedError(Exception):
    """A guest's free AI actions are used up. Raised BEFORE any provider call.

    A caller refusal, not a provider failure: ``is_caller_refusal`` tells the
    executor and the stream crash handler not to retry, reroute, or file it as
    an incident. ``error_info`` carries the stable ``error_type`` and the
    numbers so every stream path emits the same code; ``envelope()`` is the
    HTTP 403 body for request/response routes.
    """

    is_caller_refusal = True
    http_status = 403

    def __init__(self, *, allowance: int, used: int) -> None:
        self.allowance = allowance
        self.used = used
        self.error_info = RetryableError(
            error_type=GUEST_AI_ALLOWANCE_USED,
            message=GUEST_AI_ALLOWANCE_MESSAGE,
            status_code=403,
            is_retryable=False,
            user_message=GUEST_AI_ALLOWANCE_MESSAGE,
            details={"allowance": allowance, "used": used},
        )
        super().__init__(GUEST_AI_ALLOWANCE_MESSAGE)

    def envelope(self) -> dict[str, Any]:
        return {
            "error": GUEST_AI_ALLOWANCE_USED,
            "message": GUEST_AI_ALLOWANCE_MESSAGE,
            "allowance": self.allowance,
            "used": self.used,
        }


_allowance_resolver: Callable[[], Awaitable[int]] | None = None
_unwired_announced = False
_admitted: OrderedDict[str, None] = OrderedDict()
_locks: dict[str, asyncio.Lock] = {}
_locks_guard = asyncio.Lock()


def set_guest_ai_allowance_resolver(resolver: Callable[[], Awaitable[int]] | None) -> None:
    """Host wiring: an async callable returning how many AI actions a guest gets."""
    global _allowance_resolver
    _allowance_resolver = resolver


def reset_guest_ai_allowance_state() -> None:
    """Tests: forget the process memo (the durable ledger is untouched)."""
    _admitted.clear()
    _locks.clear()


def _is_guest(ctx: Any) -> bool:
    return (
        ctx is not None
        and getattr(ctx, "auth_type", None) == "fingerprint"
        and not getattr(ctx, "is_authenticated", False)
    )


def _remember(request_id: str) -> None:
    _admitted[request_id] = None
    _admitted.move_to_end(request_id)
    while len(_admitted) > _ADMITTED_MEMO_MAX:
        _admitted.popitem(last=False)


async def _lock_for(request_id: str) -> asyncio.Lock:
    async with _locks_guard:
        lock = _locks.get(request_id)
        if lock is None:
            lock = asyncio.Lock()
            _locks[request_id] = lock
        return lock


async def _record_unreadable(exc: BaseException, ctx: Any, stage: str) -> None:
    vcprint(
        f"[GuestAIAllowance] {stage} failed — ALLOWING this guest action and recording "
        f"the gap: {type(exc).__name__}: {exc}",
        color="red",
        log_level="ERROR",
    )
    try:
        from matrx_orm import record_error

        await record_error(
            exc,
            kind="guest_ai_allowance_unreadable",
            request_id=getattr(ctx, "request_id", None) or None,
            user_id=getattr(ctx, "user_id", None) or None,
            source_app="matrx-ai",
            source_feature="guest_ai_allowance",
            route="providers.guest_ai_allowance",
            error_type=type(exc).__name__,
            context={"stage": stage},
        )
    except Exception as capture_exc:  # noqa: BLE001 — the vcprint above already screamed
        vcprint(
            f"[GuestAIAllowance] could not record the gap either: {capture_exc}",
            color="red",
        )


async def _decide(fingerprint: str, request_id: str, allowance: int) -> tuple[bool, int]:
    """Read the ledger and, when admitted, write this action's row.

    Returns ``(admitted, used_before)``. Runs in a detached task so its reads
    and its write take their own pool connection — never the caller's open
    transaction (the ContextVar connection-leak class).
    """
    from matrx_ai.db._registry import get_instance

    guests = get_instance("guest_executions_manager")
    ledger = get_instance("guest_execution_log_manager")
    rows = await guests.filter_all_guest_executions(fingerprint=fingerprint)
    if not rows:
        raise LookupError(f"no guest_executions row for fingerprint {fingerprint[:12]}…")
    guest_id = str(rows[0].id)
    if await ledger.exists(
        guest_id=guest_id, resource_type=LEDGER_RESOURCE_TYPE, resource_id=request_id
    ):
        return True, -1
    used = await ledger.count(guest_id=guest_id, resource_type=LEDGER_RESOURCE_TYPE)
    if used >= allowance:
        return False, used
    await ledger.create_guest_execution_log(
        guest_id=guest_id,
        fingerprint=fingerprint,
        resource_type=LEDGER_RESOURCE_TYPE,
        resource_id=request_id,
    )
    return True, used


async def admit_guest_ai_action() -> None:
    """Admit or refuse the paid AI call about to be made, for a guest only.

    Signed-in callers, system work and any context that is not a fingerprint
    guest return immediately with no read. Raises
    :class:`GuestAIAllowanceUsedError` when this guest has used every free
    action and this call belongs to a NEW action.
    """
    global _unwired_announced
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if not _is_guest(ctx):
        return
    request_id = str(getattr(ctx, "request_id", "") or "")
    fingerprint = str(getattr(ctx, "fingerprint_id", "") or "")
    if request_id in _admitted:
        return
    if _allowance_resolver is None:
        if not _unwired_announced:
            _unwired_announced = True
            vcprint(
                "[GuestAIAllowance] no allowance resolver wired by the host — guest AI "
                "use is NOT limited in this process.",
                color="red",
                log_level="WARNING",
            )
        return
    if not request_id or not fingerprint:
        await _record_unreadable(
            ValueError("guest context carries no request_id or fingerprint"),
            ctx,
            "identify the action",
        )
        return

    lock = await _lock_for(request_id)
    try:
        async with lock:
            await _admit_locked(ctx, request_id, fingerprint)
    finally:
        _locks.pop(request_id, None)


async def _admit_locked(ctx: Any, request_id: str, fingerprint: str) -> None:
    if request_id in _admitted or _allowance_resolver is None:
        return
    try:
        allowance = int(await _allowance_resolver())
    except Exception as exc:  # noqa: BLE001 — fail open, loudly
        await _record_unreadable(exc, ctx, "read the allowance")
        _remember(request_id)
        return
    try:
        admitted, used = await detached_task(
            _decide(fingerprint, request_id, allowance),
            name="guest_ai_allowance_decide",
        )
    except Exception as exc:  # noqa: BLE001 — fail open, loudly
        await _record_unreadable(exc, ctx, "read or write the guest ledger")
        _remember(request_id)
        return
    if not admitted:
        vcprint(
            f"[GuestAIAllowance] refused request {request_id[:8]}… — "
            f"{used}/{allowance} free AI actions used",
            color="yellow",
            log_level="WARNING",
        )
        raise GuestAIAllowanceUsedError(allowance=allowance, used=used)
    _remember(request_id)


async def _peek(fingerprint: str, request_id: str) -> int | None:
    """Read-only twin of :func:`_decide`: ``used`` for a NEW action, None if already admitted."""
    from matrx_ai.db._registry import get_instance

    guests = get_instance("guest_executions_manager")
    ledger = get_instance("guest_execution_log_manager")
    rows = await guests.filter_all_guest_executions(fingerprint=fingerprint)
    if not rows:
        raise LookupError(f"no guest_executions row for fingerprint {fingerprint[:12]}…")
    guest_id = str(rows[0].id)
    if await ledger.exists(
        guest_id=guest_id, resource_type=LEDGER_RESOURCE_TYPE, resource_id=request_id
    ):
        return None
    return await ledger.count(guest_id=guest_id, resource_type=LEDGER_RESOURCE_TYPE)


async def precheck_guest_ai_action() -> None:
    """Refuse a used-up guest at the REQUEST BOUNDARY, before anything is stored.

    NOT the authority — :func:`admit_guest_ai_action` at the paid-call seam is,
    and it still runs and records. This read-only twin exists so an exhausted
    guest's new message is refused before the turn is persisted (otherwise the
    seam refuses mid-run and the transcript keeps a failed turn). Called from
    ``conversation_gate.ensure_user_request_exists`` on the branch that is about
    to create a NEW request row — the boundary every persisted AI route crosses
    during prep. Writes nothing; an unreadable allowance or ledger passes
    (the seam then records the gap).
    """
    from matrx_ai.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if not _is_guest(ctx) or _allowance_resolver is None:
        return
    request_id = str(getattr(ctx, "request_id", "") or "")
    fingerprint = str(getattr(ctx, "fingerprint_id", "") or "")
    if not request_id or not fingerprint or request_id in _admitted:
        return
    try:
        allowance = int(await _allowance_resolver())
        used = await detached_task(
            _peek(fingerprint, request_id), name="guest_ai_allowance_precheck"
        )
    except Exception as exc:  # noqa: BLE001 — the seam is the authority and records
        vcprint(
            f"[GuestAIAllowance] boundary pre-check could not read ({type(exc).__name__}: "
            f"{exc}) — passing to the paid-call seam",
            color="yellow",
            log_level="WARNING",
        )
        return
    if used is not None and used >= allowance:
        raise GuestAIAllowanceUsedError(allowance=allowance, used=used)
