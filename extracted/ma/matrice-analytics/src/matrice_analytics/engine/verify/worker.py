"""The VLM verification worker -- the engine's one sanctioned background thread.

Normative source: ``VLM-VERIFY-INTERFACES.md`` §2 (the interface, frozen) and
``alert-verification-api.md`` §4-§5 (what each status code means and how to retry it).

**Why a thread at all.**  ``POST /vss/verify`` waits for "after" frames to be recorded and
makes one VLM call per frame: seconds to minutes.  The ``verification`` primitive runs on the
frame loop and must never wait on it, so it hands a :class:`VerifyJob` to this worker and
polls a mailbox with :meth:`VerificationWorker.take` on later frames.  The operator approved
this as the single exception to the engine's "no threads, no I/O" rule (PY-15); the
exception is narrow on purpose:

* **one** daemon thread per live worker, **one** request in flight (the Thor VSS serialises
  VLM calls anyway);
* every structure the thread and the frame loop share sits behind **one**
  :class:`threading.Lock`, held only for dict/deque edits -- never across I/O -- so
  :meth:`~VerificationWorker.submit` and :meth:`~VerificationWorker.take` never block;
* the thread sees only :class:`VerifyJob` (immutable) and writes only :class:`Verdict`
  (immutable) into mailboxes -- it never touches engine state;
* nothing starts at import: :func:`worker_for` builds lazily, and ``stub`` / ``off`` modes
  start no thread and do no I/O at all, so the app validator (which runs every app twice
  and compares bytes) stays deterministic.

**Retry table** (§2, restating API §5 for this client):

========================================  ===============================================
reply                                     outcome
========================================  ===============================================
200, ``status`` confirmed/rejected/       that :class:`Verdict` (final)
unverifiable
400 / 422 (and any other 4xx but 408/429) ``bad_request`` -- never retried, logged ERROR
500, or a 200 that is not a verify reply  retried **once**, then ``unavailable``
503 / other 5xx / 408 / 429 /             retried with backoff 2, 4, 8, 16, 30 s (+ up to
transport error / timeout                 50 % jitter) until ``MAX_AGE``, then
                                          ``unavailable``
========================================  ===============================================

``MAX_AGE`` is measured from the job's **first attempt**, not from submit: a job that waited
in the queue behind a slow one still gets at least one try.  It bounds when a *new* attempt
may start; an attempt already running is allowed to finish (up to ``TIMEOUT_S``).
"""

from __future__ import annotations

import atexit
import logging
import math
import os
import random
import threading
import time
from collections import OrderedDict, deque
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable
from urllib.parse import urlsplit

from matrice_analytics.engine.verify.http import HttpReply, post_json

__all__ = [
    "BAD_REQUEST",
    "CONFIRMED",
    "DROPPED",
    "REJECTED",
    "STATUSES",
    "UNAVAILABLE",
    "UNVERIFIABLE",
    "LiveVerificationWorker",
    "ScheduledVerificationWorker",
    "Verdict",
    "VerificationWorker",
    "VerifyJob",
    "WorkerSettings",
    "close_all_workers",
    "worker_for",
]

logger = logging.getLogger(__name__)

# -- verdict statuses (§2) ----------------------------------------------------
CONFIRMED = "confirmed"  # 200, final
REJECTED = "rejected"  # 200, final
UNVERIFIABLE = "unverifiable"  # 200, final
UNAVAILABLE = "unavailable"  # retry budget exhausted on 503 / 5xx / transport / timeout
BAD_REQUEST = "bad_request"  # 400 / 422 -- never retried
DROPPED = "dropped"  # evicted from a full queue before it was sent
STATUSES: frozenset[str] = frozenset(
    {CONFIRMED, REJECTED, UNVERIFIABLE, UNAVAILABLE, BAD_REQUEST, DROPPED}
)
_FINAL_200: frozenset[str] = frozenset({CONFIRMED, REJECTED, UNVERIFIABLE})

# -- retry policy (§2) --------------------------------------------------------
_BACKOFF_S: tuple[float, ...] = (2.0, 4.0, 8.0, 16.0, 30.0)
_JITTER = 0.5  # up to +50 % of the step
_SERVER_BUG_RETRIES = 1  # a 500 is retried once, then unavailable
_RETRYABLE_4XX: frozenset[int] = frozenset({408, 429})
_MAX_REASON_CHARS = 300  # a server message is a log line, not a document
_MAILBOX_DEPTH = 16  # verdicts held per mailbox before the oldest is discarded

# -- environment (§2) ---------------------------------------------------------
_MODES: frozenset[str] = frozenset({"live", "stub", "off"})
_DEFAULTS: dict[str, str] = {
    "MATRICE_VERIFY_MODE": "live",
    "MATRICE_VSS_VERIFY_URL": "http://127.0.0.1:8080/vss/verify",
    "MATRICE_VSS_VERIFY_TIMEOUT_S": "300",
    "MATRICE_VSS_VERIFY_MAX_AGE_S": "120",
    "MATRICE_VSS_VERIFY_MAX_QUEUE": "32",
    "MATRICE_VERIFY_STUB_STATUS": CONFIRMED,
    "MATRICE_VERIFY_STUB_DELAY_S": "2.0",
}


@dataclass(frozen=True, slots=True)
class VerifyJob:
    """One verification request, as the primitive builds it (§2)."""

    camera_id: str  # 24-hex ObjectID (primitive validates before submit)
    rtp_timestamp: int  # uint32, 0 = locate by time
    timestamp_ms: int  # epoch ms, >= 2020-01-01 (primitive guards)
    query: str
    frames: Mapping[str, Any]  # {"window_seconds", "spacing_seconds", "position"}
    vote: Mapping[str, Any]  # {"rule", "at_least", "min_decided"}
    frame_ts: float  # stream-clock seconds of the candidate frame (stub mode uses it)


@dataclass(frozen=True, slots=True)
class Verdict:
    """The outcome delivered to a mailbox; ``status`` is one of :data:`STATUSES`."""

    status: str
    evidence: str | None = None
    reason: str | None = None
    votes_confirmed: int = 0
    votes_total: int = 0


@runtime_checkable
class VerificationWorker(Protocol):
    """What the ``verification`` primitive codes against (§2)."""

    def submit(self, mailbox: str, job: VerifyJob) -> bool:
        """Queue ``job`` for ``mailbox``; never blocks.  ``False`` only once closed."""
        ...

    def take(self, mailbox: str, frame_ts: float) -> Verdict | None:
        """Pop the next verdict for ``mailbox`` if one has arrived; never blocks."""
        ...

    def close(self, timeout_s: float = 5.0) -> None:
        """Stop accepting jobs; a live worker also stops and joins its thread."""
        ...


# -- settings -----------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class WorkerSettings:
    """The seven §2 environment variables, parsed and bounded.

    Read once, when a worker is built -- never from the manifest: the endpoint is
    deployment-specific and app folders are immutable.
    """

    mode: str = "live"
    url: str = _DEFAULTS["MATRICE_VSS_VERIFY_URL"]
    timeout_s: float = 300.0
    max_age_s: float = 120.0
    max_queue: int = 32
    stub_status: str = CONFIRMED
    stub_delay_s: float = 2.0

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> WorkerSettings:
        """Parse the environment; a bad value is logged at ERROR and its default used.

        Falling back rather than raising is deliberate: :func:`worker_for` is called lazily
        from the frame loop on the first candidate, so a typo in a deployment variable
        would otherwise crash the pipeline at the moment an alert is being raised.
        """
        env = os.environ if environ is None else environ
        mode = _env_choice(env, "MATRICE_VERIFY_MODE", _MODES)
        return cls(
            mode=mode,
            url=_env_url(env, "MATRICE_VSS_VERIFY_URL"),
            timeout_s=_env_number(env, "MATRICE_VSS_VERIFY_TIMEOUT_S", float, minimum=0.001),
            max_age_s=_env_number(env, "MATRICE_VSS_VERIFY_MAX_AGE_S", float, minimum=0.0),
            max_queue=int(_env_number(env, "MATRICE_VSS_VERIFY_MAX_QUEUE", int, minimum=1)),
            stub_status=_env_choice(env, "MATRICE_VERIFY_STUB_STATUS", STATUSES),
            stub_delay_s=_env_number(env, "MATRICE_VERIFY_STUB_DELAY_S", float, minimum=0.0),
        )


def _env_raw(env: Mapping[str, str], name: str) -> str:
    value = env.get(name, "").strip()
    return value or _DEFAULTS[name]


def _env_fallback(name: str, value: str, why: str) -> str:
    logger.error("%s=%r is invalid (%s); using the default %r", name, value, why, _DEFAULTS[name])
    return _DEFAULTS[name]


def _env_choice(env: Mapping[str, str], name: str, allowed: frozenset[str]) -> str:
    value = _env_raw(env, name).lower()
    if value in allowed:
        return value
    return _env_fallback(name, value, f"expected one of {sorted(allowed)}")


def _env_url(env: Mapping[str, str], name: str) -> str:
    value = _env_raw(env, name)
    parts = urlsplit(value)
    # http(s) only: urllib would otherwise happily open file:// or ftp:// URLs.
    if parts.scheme in ("http", "https") and parts.netloc:
        return value
    return _env_fallback(name, value, "expected an http:// or https:// URL")


def _env_number(
    env: Mapping[str, str], name: str, kind: Callable[[str], float], *, minimum: float
) -> float:
    value = _env_raw(env, name)
    try:
        number = kind(value)
    except ValueError:
        return kind(_env_fallback(name, value, "not a number"))
    if not math.isfinite(number) or number < minimum:
        return kind(_env_fallback(name, value, f"must be finite and >= {minimum}"))
    return number


# -- stub / off ---------------------------------------------------------------


class ScheduledVerificationWorker:
    """``stub`` and ``off`` modes: no thread, no I/O, fully deterministic.

    Each submit schedules ``verdict`` for its mailbox, visible once the caller's stream clock
    reaches ``job.frame_ts + delay_s``.  ``delay_s=None`` (``off``) makes it visible on the
    very next :meth:`take`, whatever the clock.  A mailbox re-submitting a job equal on
    ``(camera_id, timestamp_ms, query)`` to one it is still waiting on gets one verdict, as
    in live mode.
    """

    __slots__ = ("_closed", "_delay_s", "_lock", "_pending", "_verdict")

    def __init__(self, verdict: Verdict, delay_s: float | None) -> None:
        self._verdict = verdict
        self._delay_s = delay_s
        self._lock = threading.Lock()
        self._closed = False
        # mailbox -> FIFO of (visible_at, dedup key)
        self._pending: dict[str, deque[tuple[float, tuple[str, int, str]]]] = {}

    @property
    def closed(self) -> bool:
        return self._closed

    def submit(self, mailbox: str, job: VerifyJob) -> bool:
        key = _dedup_key(job)
        visible_at = -math.inf if self._delay_s is None else job.frame_ts + self._delay_s
        with self._lock:
            if self._closed:
                return False
            queue = self._pending.setdefault(mailbox, deque())
            if all(k != key for _, k in queue):
                queue.append((visible_at, key))
            return True

    def take(self, mailbox: str, frame_ts: float) -> Verdict | None:
        with self._lock:
            queue = self._pending.get(mailbox)
            if not queue or frame_ts < queue[0][0]:
                return None
            queue.popleft()
            if not queue:
                del self._pending[mailbox]
            return self._verdict

    def close(self, timeout_s: float = 5.0) -> None:
        with self._lock:
            self._closed = True


# -- live ---------------------------------------------------------------------


@dataclass(slots=True)
class _Pending:
    """A job queued or in flight, and every mailbox waiting on its verdict."""

    job: VerifyJob
    mailboxes: list[str] = field(default_factory=list)


class LiveVerificationWorker:
    """``live`` mode: one daemon thread POSTing jobs to the VSS verify endpoint in order.

    Args:
        settings: Parsed §2 environment.
        backoff_s: Retry steps; the last one repeats.  Overridable so tests can run the real
            retry loop in milliseconds -- production always uses the §2 table.
    """

    def __init__(
        self,
        settings: WorkerSettings,
        *,
        backoff_s: Sequence[float] = _BACKOFF_S,
    ) -> None:
        self._settings = settings
        self._backoff_s = tuple(backoff_s) or _BACKOFF_S
        # The one lock (§2).  The Condition shares it: it is how the thread sleeps until a
        # job arrives and how close() interrupts a backoff wait.
        self._lock = threading.Lock()
        self._wake = threading.Condition(self._lock)
        self._queue: OrderedDict[tuple[str, int, str], _Pending] = OrderedDict()
        self._inflight: tuple[tuple[str, int, str], _Pending] | None = None
        self._verdicts: dict[str, deque[Verdict]] = {}
        self._closed = False
        self._thread = threading.Thread(target=self._run, name="matrice-verify-worker", daemon=True)
        self._thread.start()

    @property
    def closed(self) -> bool:
        return self._closed

    def submit(self, mailbox: str, job: VerifyJob) -> bool:
        key = _dedup_key(job)
        with self._lock:
            if self._closed:
                return False
            if self._inflight is not None and self._inflight[0] == key:
                _subscribe(self._inflight[1], mailbox)
                return True
            pending = self._queue.get(key)
            if pending is not None:
                _subscribe(pending, mailbox)
                return True
            if len(self._queue) >= self._settings.max_queue:
                _, evicted = self._queue.popitem(last=False)
                logger.warning(
                    "verify queue full (%d): dropping the oldest job camera=%s ts_ms=%d",
                    self._settings.max_queue,
                    evicted.job.camera_id,
                    evicted.job.timestamp_ms,
                )
                self._deliver(evicted, Verdict(DROPPED, reason="verification queue full"))
            self._queue[key] = _Pending(job, [mailbox])
            self._wake.notify()
            return True

    def take(self, mailbox: str, frame_ts: float) -> Verdict | None:
        with self._lock:
            verdicts = self._verdicts.get(mailbox)
            if not verdicts:
                return None
            verdict = verdicts.popleft()
            if not verdicts:
                del self._verdicts[mailbox]
            return verdict

    def close(self, timeout_s: float = 5.0) -> None:
        """Stop the thread and join it for up to ``timeout_s``.

        Queued jobs get ``unavailable``.  A request already on the wire cannot be
        interrupted (``urllib`` has no cancel); if it outlasts ``timeout_s`` the daemon
        thread is abandoned, logged, and dies with the process.
        """
        with self._lock:
            self._closed = True
            closing = Verdict(UNAVAILABLE, reason="verification worker closed")
            while self._queue:
                self._deliver(self._queue.popitem(last=False)[1], closing)
            self._wake.notify_all()
        if self._thread is not threading.current_thread():
            self._thread.join(timeout_s)
        if self._thread.is_alive():
            logger.warning("verify worker thread still busy after %.1fs; abandoning it", timeout_s)

    # -- thread side ------------------------------------------------------------

    def _deliver(self, pending: _Pending, verdict: Verdict) -> None:
        """Post ``verdict`` to every subscriber.  Caller holds the lock."""
        for mailbox in pending.mailboxes:
            self._verdicts.setdefault(mailbox, deque(maxlen=_MAILBOX_DEPTH)).append(verdict)

    def _run(self) -> None:
        while True:
            with self._lock:
                while not self._closed and not self._queue:
                    self._wake.wait()
                if self._closed:
                    return
                key, pending = self._queue.popitem(last=False)
                self._inflight = (key, pending)
            try:
                verdict = self._verify(pending.job)
            except Exception as exc:  # noqa: BLE001 - a bug must not kill the only verify thread
                logger.exception("verify worker failed on camera=%s", pending.job.camera_id)
                verdict = Verdict(UNAVAILABLE, reason=f"worker error: {type(exc).__name__}")
            with self._lock:
                self._inflight = None
                self._deliver(pending, verdict)

    def _sleep(self, seconds: float) -> bool:
        """Wait ``seconds`` unless closed first; ``True`` when the wait ran its course."""
        deadline = time.monotonic() + seconds
        with self._lock:
            while not self._closed:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    return True
                self._wake.wait(remaining)
            return False

    def _backoff(self, attempt: int) -> float:
        step = self._backoff_s[min(attempt, len(self._backoff_s) - 1)]
        return step * (1.0 + random.random() * _JITTER)  # noqa: S311 - jitter, not crypto

    def _verify(self, job: VerifyJob) -> Verdict:
        """Run one job to a final :class:`Verdict` under the retry table above."""
        deadline = time.monotonic() + self._settings.max_age_s  # from the first attempt
        try:
            body = request_body(job)
            reply = post_json(self._settings.url, body, self._settings.timeout_s)
        except (TypeError, ValueError) as exc:
            logger.error("verify request for camera=%s is not JSON: %s", job.camera_id, exc)
            return Verdict(BAD_REQUEST, reason=_clip(f"request not serialisable: {exc}"))
        attempt = 0
        server_bugs = 0
        while True:
            verdict, retry_kind = _classify(reply)
            if verdict is not None:
                if verdict.status == BAD_REQUEST:
                    logger.error(
                        "verify rejected the request (HTTP %s) camera=%s ts_ms=%d: %s",
                        reply.code,
                        job.camera_id,
                        job.timestamp_ms,
                        reply.message,
                    )
                return verdict
            if retry_kind == "server_bug":
                server_bugs += 1
                if server_bugs > _SERVER_BUG_RETRIES:
                    return _give_up(job, reply, "server error persisted")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return _give_up(job, reply, f"retry budget {self._settings.max_age_s:g}s spent")
            logger.info(
                "verify camera=%s attempt %d failed (%s); retrying",
                job.camera_id,
                attempt + 1,
                _describe(reply),
            )
            if not self._sleep(min(self._backoff(attempt), remaining)):
                return Verdict(UNAVAILABLE, reason="verification worker closed")
            attempt += 1
            reply = post_json(self._settings.url, body, self._settings.timeout_s)


# -- reply classification -------------------------------------------------------


def request_body(job: VerifyJob) -> dict[str, Any]:
    """The exact §2 wire body: ``{camera_id, rtp_timestamp, timestamp_ms, query, frames, vote}``."""
    return {
        "camera_id": job.camera_id,
        "rtp_timestamp": int(job.rtp_timestamp),
        "timestamp_ms": int(job.timestamp_ms),
        "query": job.query,
        "frames": dict(job.frames),
        "vote": dict(job.vote),
    }


def _classify(reply: HttpReply) -> tuple[Verdict | None, str]:
    """``(final verdict, "")`` or ``(None, "server_bug" | "transient")``."""
    code = reply.code
    if code == 200:
        verdict = _verdict_from_200(reply.payload)
        return (verdict, "") if verdict is not None else (None, "server_bug")
    if code is not None and 400 <= code < 500 and code not in _RETRYABLE_4XX:
        return Verdict(BAD_REQUEST, reason=_clip(f"HTTP {code}: {reply.message}")), ""
    if code == 500:
        return None, "server_bug"
    # 503, any other 5xx or 2xx/3xx surprise, 408/429, transport error, timeout.
    return None, "transient"


def _verdict_from_200(payload: Any) -> Verdict | None:
    """A final verdict from a 200 body, or ``None`` when it is not a verify reply."""
    if not isinstance(payload, dict) or payload.get("status") not in _FINAL_200:
        return None
    votes = payload.get("votes")
    votes = votes if isinstance(votes, dict) else {}
    return Verdict(
        status=payload["status"],
        evidence=_opt_str(payload.get("evidence")),
        reason=_opt_str(payload.get("reason")),
        votes_confirmed=_as_count(votes.get("confirmed")),
        votes_total=_as_count(votes.get("total")),
    )


def _give_up(job: VerifyJob, reply: HttpReply, why: str) -> Verdict:
    logger.warning(
        "verify camera=%s ts_ms=%d unavailable: %s; last %s",
        job.camera_id,
        job.timestamp_ms,
        why,
        _describe(reply),
    )
    return Verdict(UNAVAILABLE, reason=_clip(f"{why}; last {_describe(reply)}"))


def _describe(reply: HttpReply) -> str:
    if reply.code is None:
        return f"transport error {reply.message}"
    return f"HTTP {reply.code} {reply.message}".rstrip()


def _dedup_key(job: VerifyJob) -> tuple[str, int, str]:
    return (job.camera_id, int(job.timestamp_ms), job.query)


def _subscribe(pending: _Pending, mailbox: str) -> None:
    if mailbox not in pending.mailboxes:
        pending.mailboxes.append(mailbox)


def _opt_str(value: Any) -> str | None:
    return _clip(value) if isinstance(value, str) and value else None


def _as_count(value: Any) -> int:
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0


def _clip(text: str) -> str:
    return text if len(text) <= _MAX_REASON_CHARS else text[: _MAX_REASON_CHARS - 3] + "..."


# -- process-wide registry -------------------------------------------------------

_registry_lock = threading.Lock()
_workers: dict[tuple[str, str], LiveVerificationWorker | ScheduledVerificationWorker] = {}
_atexit_registered = False


def build_worker(settings: WorkerSettings) -> LiveVerificationWorker | ScheduledVerificationWorker:
    """A new, unshared worker for ``settings``.  Prefer :func:`worker_for`."""
    if settings.mode == "off":
        return ScheduledVerificationWorker(Verdict(CONFIRMED, reason="verification off"), None)
    if settings.mode == "stub":
        verdict = Verdict(settings.stub_status, reason="verification stub")
        return ScheduledVerificationWorker(verdict, settings.stub_delay_s)
    return LiveVerificationWorker(settings)


def worker_for() -> VerificationWorker:
    """The process-wide worker for the current ``(mode, endpoint)``; built on first call.

    The environment is read here, not at import, so importing the engine starts nothing.
    A worker that was closed is replaced on the next call.
    """
    global _atexit_registered
    settings = WorkerSettings.from_env()
    key = (settings.mode, settings.url)
    with _registry_lock:
        worker = _workers.get(key)
        if worker is None or worker.closed:
            worker = build_worker(settings)
            _workers[key] = worker
            if not _atexit_registered:
                atexit.register(close_all_workers)
                _atexit_registered = True
        return worker


def close_all_workers(timeout_s: float = 5.0) -> None:
    """Close and forget every worker :func:`worker_for` built.  Safe to call repeatedly."""
    with _registry_lock:
        workers = list(_workers.values())
        _workers.clear()
    for worker in workers:
        worker.close(timeout_s)
