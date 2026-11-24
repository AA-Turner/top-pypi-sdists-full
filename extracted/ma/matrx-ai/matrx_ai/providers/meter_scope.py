"""THE RUNTIME METER BACKSTOP — every paid send asks, at send time, whether a meter is open (P8-RUNS, 2026-11-17).

The static guard (``aidream/services/ai_catalog/tests/test_direct_send_callers_are_metered.py``) reads code; an
adversary can always write a shape it does not read. This module is the second, independent layer: the provider
layer ITSELF checks, at the moment it sends, that the call will settle on a ledger. A meter is open when ANY of:

* an explicit direct-spend scope is open (:func:`direct_spend_scope`): the caller declares it records the cost itself
  (``record_direct_spend`` / ``note_direct_spend`` in aidream) once the call returns;
* the ambient AppContext carries a runtime execution (``metadata.runtime_execution_id`` /
  ``runtime_root_execution_id``) AND a recorder will bank this call on it: with a host run probe configured
  (:func:`configure_run_meter_probe`; aidream: ``loop_control.live_meter_target``) the probe must name the execution
  the call is metered onto — a run id in the context alone is NOT a meter (P8-RUNS, 2026-11-17: an agent-as-tool
  child carried the root's id while nothing recorded its tools' calls, so the backstop read "open" and filed
  nothing). With no run probe (the package alone) the run keys are trusted;
* the host's probe says so (:func:`configure_meter_probe`; aidream: an open spend scope, ``runtime/utility.py``).

With none open the call STILL SENDS — nothing may block. It is FILED as unmetered through the host's sink
(:func:`configure_unmetered_call_sink`; aidream: ``billing.absorbed.file_unbanked_spend`` with reason
``unmetered_provider_call``) with the entry point, provider, model, the first caller frame outside the provider layer,
and the cost once the response priced it, and a WARNING is logged every time. No sink configured: the WARNING alone.

Entry points that ask (``providers/FEATURE.md`` § The runtime meter backstop): ``UnifiedAIClient._dispatch_with_billing_net``
(chat, media — image / video / TTS — STT, decisions, rerank, extraction, embeddings), ``batch_live.send_live`` (the batch
lane's live send), ``realtime_wire.open_realtime_wire`` and ``realtime_wire.synthesize_speech_pcm``. A nested dispatch
on a pool the outer call already holds is not asked again (the outer call owns it).

Never raises: a probe or sink failure is logged and the send goes on.
"""

from __future__ import annotations

import asyncio
import logging
import sys
import time
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, replace
from typing import Any

logger = logging.getLogger("matrx_ai.providers.meter_scope")

#: The reason word the host files an unmetered call under (``execution_spend_unbanked`` error_type).
UNMETERED_REASON = "unmetered_provider_call"
#: AppContext metadata keys that name the runtime execution a send settles on.
RUN_KEYS: tuple[str, ...] = ("runtime_execution_id", "runtime_root_execution_id")
#: The same (entry, provider, model, caller) opens at most one finding per this many seconds per process; the WARNING
#: is logged every time. A loop of unmetered calls is one finding, not a flood — but NEVER a smaller one: every repeat
#: inside the window reaches the sink carrying the finding's running count and total (P8-RUNS, 2026-11-17: the old
#: dedupe dropped every later call, so five calls costing $62.75 filed one row of $0.50).
FILE_EVERY_SECONDS = 3600.0  # protocol-constant: internal cadence of one accounting-flush line per meter scope, a latency/log-volume trade-off with no admin-facing meaning

_DIRECT_SPEND: ContextVar[str | None] = ContextVar("matrx_ai_direct_spend_scope", default=None)
_probe: Callable[[], Any] | None = None
_run_probe: Callable[[dict[str, Any]], Any] | None = None
_sink: Callable[[UnmeteredProviderCall], Any] | None = None
_last_filed: dict[tuple[str, str, str, str], _Tally] = {}
_pending: set[asyncio.Task[Any]] = set()


@dataclass(frozen=True)
class UnmeteredProviderCall:
    """One paid provider call that ran with no meter open, with the running tally of its finding.

    ``cost_usd`` is THIS call's catalog cost (None: unpriced). ``repeats`` is how many calls the finding holds so far
    (this one included), ``total_cost_usd`` their summed known cost and ``unpriced_repeats`` how many of them carried
    no price. ``finding`` names the finding (stable across its repeats): ``repeats == 1`` opens it (the host files a
    row), a later record UPDATES that row with the new tally — the host never drops one."""

    entry: str
    provider: str
    model: str
    caller: str
    cost_usd: float | None
    repeats: int = 1
    total_cost_usd: float | None = None
    unpriced_repeats: int = 0
    finding: str = ""


@dataclass
class _Tally:
    started: float
    finding: str
    repeats: int = 0
    total_cost_usd: float = 0.0
    unpriced_repeats: int = 0


def configure_meter_probe(probe: Callable[[], Any] | None) -> None:
    """The host's answer to "is a meter open here?" (truthy = yes). Read on every paid send; must be cheap and sync."""
    global _probe
    _probe = probe


def configure_run_meter_probe(probe: Callable[[dict[str, Any]], Any] | None) -> None:
    """The host's answer to "will a recorder bank a call made under this run context?" Given the AppContext metadata
    (which carries a run key), returns the execution the call is metered onto (truthy) or None. Sync and cheap."""
    global _run_probe
    _run_probe = probe


def configure_unmetered_call_sink(sink: Callable[[UnmeteredProviderCall], Any] | None) -> None:
    """Where an unmetered call is filed. May be sync or async (an awaitable is run detached); never on the send path."""
    global _sink
    _sink = sink


@contextmanager
def direct_spend_scope(feature: str) -> Iterator[None]:
    """Declare that the calls inside record their own cost (``record_direct_spend`` / ``note_direct_spend``)."""
    token = _DIRECT_SPEND.set(feature or "direct_spend")
    try:
        yield
    finally:
        _DIRECT_SPEND.reset(token)


def open_meter() -> str | None:
    """The name of the meter this send settles on, or None when nothing will record it."""
    scope = _DIRECT_SPEND.get()
    if scope:
        return f"direct_spend:{scope}"
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
        metadata = getattr(ctx, "metadata", None) if ctx is not None else None
        if isinstance(metadata, dict) and any(metadata.get(key) for key in RUN_KEYS):
            run_probe = _run_probe
            if run_probe is None:
                return f"run:{next(metadata[key] for key in RUN_KEYS if metadata.get(key))}"
            try:
                banker = run_probe(metadata)
            except Exception:  # noqa: BLE001 — a broken probe never blocks a send; it is loud
                logger.exception("meter backstop: the host's run probe raised; asking the meter probe")
                banker = None
            if banker:
                return f"run:{banker}"
    except Exception:  # noqa: BLE001 — cannot read the context: ask the host
        logger.debug("meter backstop: could not read the AppContext", exc_info=True)
    if _probe is not None:
        try:
            found = _probe()
        except Exception:  # noqa: BLE001 — a broken probe never blocks a send; it is loud
            logger.exception("meter backstop: the host's meter probe raised; treating the call as unmetered")
            return None
        if found:
            return f"host:{found}"
    return None


_LAYER_MARKERS = (
    "/matrx_ai/providers/",
    "/matrx_ai/orchestrator/",
    "/matrx_ai/processing/",  # execute_stt / execute_tts are pass-throughs: the finding must name THEIR caller
    "/asyncio/",
    "/contextlib.py",
    "/concurrent/",
    "/threading.py",
)


def caller_module() -> str:
    """The first frame outside the provider layer and the event loop: ``module:function:line``."""
    frame = sys._getframe(1)
    while frame is not None:
        filename = frame.f_code.co_filename.replace("\\", "/")
        if not any(m in filename for m in _LAYER_MARKERS):
            module = frame.f_globals.get("__name__", "?")
            return f"{module}:{frame.f_code.co_name}:{frame.f_lineno}"
        frame = frame.f_back
    return "?"


class SendCheck:
    """The verdict for one send, taken BEFORE it goes; :meth:`settle` files it (with the cost) once it returns."""

    __slots__ = ("caller", "entry", "meter", "model", "provider", "_settled")

    def __init__(self, entry: str, provider: str, model: str, meter: str | None, caller: str) -> None:
        self.entry = entry
        self.provider = provider
        self.model = model
        self.meter = meter
        self.caller = caller
        self._settled = False

    @property
    def metered(self) -> bool:
        return self.meter is not None

    def settle(self, cost_usd: float | None = None) -> UnmeteredProviderCall | None:
        """File the call when it was unmetered (once). Returns the filed record, else None."""
        if self._settled or self.meter is not None:
            self._settled = True
            return None
        self._settled = True
        return _file(UnmeteredProviderCall(self.entry, self.provider, self.model, self.caller, cost_usd))


def check_send(entry: str, *, provider: Any, model: Any) -> SendCheck:
    """Ask at send time whether a meter is open. Logs the WARNING now; the filing waits for :meth:`SendCheck.settle`."""
    meter = open_meter()
    caller = caller_module() if meter is None else ""
    check = SendCheck(entry, str(provider or "unknown"), str(model or "unknown"), meter, caller)
    if meter is None:
        logger.warning(
            "UNMETERED provider call: %s %s/%s from %s ran with no meter open (no runtime execution, spend scope or "
            "direct_spend_scope). It is sent anyway and filed as %s.",
            entry,
            check.provider,
            check.model,
            caller,
            UNMETERED_REASON,
        )
    return check


def note_send(entry: str, *, provider: Any, model: Any, cost_usd: float | None = None) -> UnmeteredProviderCall | None:
    """:func:`check_send` + settle at once, for an entry point whose cost is never known here (a socket, a batch body)."""
    return check_send(entry, provider=provider, model=model).settle(cost_usd)


def _file(record: UnmeteredProviderCall) -> UnmeteredProviderCall:
    """Count the call on its finding (opening a new one per window) and hand the sink the record with the tally."""
    key = (record.entry, record.provider, record.model, record.caller)
    now = time.monotonic()
    tally = _last_filed.get(key)
    if tally is None or now - tally.started >= FILE_EVERY_SECONDS:
        tally = _Tally(started=now, finding=f"{'|'.join(key)}|{time.time():.6f}")
        _last_filed[key] = tally
    tally.repeats += 1
    if record.cost_usd is None:
        tally.unpriced_repeats += 1
    else:
        tally.total_cost_usd += float(record.cost_usd)
    record = replace(
        record,
        repeats=tally.repeats,
        total_cost_usd=round(tally.total_cost_usd, 10) if tally.repeats > tally.unpriced_repeats else None,
        unpriced_repeats=tally.unpriced_repeats,
        finding=tally.finding,
    )
    sink = _sink
    if sink is None:
        return record
    try:
        result = sink(record)
        if asyncio.iscoroutine(result):
            try:
                task = asyncio.get_running_loop().create_task(result)
            except RuntimeError:  # no running loop (a sync bench call): run it here, it never raises out
                asyncio.run(result)
            else:
                _pending.add(task)
                task.add_done_callback(_pending.discard)
    except Exception:  # noqa: BLE001 — the filing never fails the call that already happened
        logger.exception("meter backstop: could not file the unmetered call %s", record)
    return record


def reset_for_tests() -> None:
    """Forget the dedupe memory (tests only)."""
    _last_filed.clear()
