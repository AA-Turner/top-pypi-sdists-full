"""
Client-side observability: one report per logical `act()`, delivered async / batched / best-effort.

── What direct-connect broke, and what this restores ──────────────────
Before direct-connect every act crossed the gateway, which minted the rid, timed the outer hop, and
wrote a `request_latency` row. After direct-connect the gateway is off the hot path
— so those measurements have nowhere to be taken unless the client takes them. This module is the
client half: `CallMetrics` is the per-act bundle (rid + client timing + worker perf + outcome), and
`Reporter` ships those bundles to the gateway's ingest endpoint off the control loop.

Two hard rules, both falsifiable:
  * **Privacy whitelist.** A report carries only timing + worker perf + rid + outcome, and on a failed
    act what the robot got back (its error's code, message and hint, cut: `error_of`). Never the
    `direct_secret`, never the account API key, never any observation / image bytes. `to_report()`
    is the one place a payload is built, so the whitelist is enforceable by reading one function.
  * **Never touch the control loop.** `record()` only appends to a bounded in-memory buffer and
    returns; a daemon thread does the HTTP. Every delivery failure is swallowed. The buffer is
    bounded and drops the OLDEST report when full, so a long episode against a dead gateway can
    never grow the robot's memory without limit.

3.9-clean, httpx is reached only through the injected `send` callable, never imports sequence_base.
"""
from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional





INGEST_PATH = "/v1/latency"






FLUSH_EVERY_S = 5.0



OUTCOME_SERVED = "served"
OUTCOME_WARMING = "warming"
OUTCOME_ERROR = "error"


_ERROR_CODE_MAX = 64
_ERROR_TEXT_MAX = 500


def _cut(text: Optional[str]) -> Optional[str]:
    if not isinstance(text, str) or not text.strip():
        return None
    text = text.strip()
    return text if len(text) <= _ERROR_TEXT_MAX else text[:_ERROR_TEXT_MAX - 3] + "..."


def error_of(exc: BaseException) -> Dict[str, Optional[str]]:
    """What the robot got when an act failed, as its report carries it - so its owner sees why each act failed, one that
    never reached a worker too: the platform's error code (busy, unavailable, policy_error), else the class of what was
    raised (ConnectTimeout); its message; its hint. A policy's own exception, raised as itself with its traceback
    attached, is a policy_error. Each cut: the code at 64 characters, the message and the hint at 500. Never the request.

    An error the platform answered also carries the request id it was answered under and why (its details.reason:
    stopped, queue_timeout): the refusal's own line in `seq policy logs` is under that id, so the act's line names it
    and `--rid` follows to it.
"""
    policy_own = getattr(exc, "remote_traceback", None) is not None
    code = getattr(exc, "code", None)
    if not isinstance(code, str) or not code:
        code = "policy_error" if policy_own else type(exc).__name__.lstrip("_")
    message = getattr(exc, "message", None)
    if not isinstance(message, str):
        message = f"{type(exc).__name__}: {exc}" if policy_own else str(exc)
    out = {"code": code[:_ERROR_CODE_MAX], "detail": _cut(message), "hint": _cut(getattr(exc, "hint", None))}
    rid = getattr(exc, "request_id", None)
    details = getattr(exc, "details", None)
    reason = details.get("reason") if isinstance(details, dict) else None
    if isinstance(rid, str) and rid:
        out["request_id"] = rid[:_ERROR_CODE_MAX]
    if isinstance(reason, str) and reason:
        out["reason"] = reason[:_ERROR_CODE_MAX]
    return out


@dataclass
class CallMetrics:
    """
    Everything measured about one logical `act()` call, before it becomes a report.

    Phases are `Optional[float]` and default to None on purpose: an unmeasured or invalid phase is
    reported as None, never as 0, because a false 0 drags an aggregate mean down silently while a
    None is excluded from it. `finalize()` is where the None-vs-value decision is made and named.
    """

    rid: str
    outcome: str = OUTCOME_SERVED

    total_ms: Optional[float] = None


    rtt_ms: Optional[float] = None


    network_ms: Optional[float] = None


    warmup_ms: Optional[float] = None


    first_after_connect: bool = False





    connect_ms: Optional[float] = None
    tcp_ms: Optional[float] = None
    tls_ms: Optional[float] = None



    cc: Optional[str] = None


    session: Optional[str] = None


    rid_echo: Optional[str] = None
    rid_mismatch: bool = False

    perf: Dict[str, Any] = field(default_factory=dict)




    frames: Optional[int] = None

    error: Optional[Dict[str, Optional[str]]] = None



    chunk_left_ms: Optional[float] = None

    def finalize(self) -> None:
        """Derive `network_ms` from `rtt_ms` and the worker's `handler_ms`, applying None-not-zero.

        `handler_ms` is the worker's OUTERMOST wall-time span, not a sub-phase (parse / queue /
        inference / ipc): subtracting a sub-phase would count the worker's own queue/ipc as "network"
        and overstate it. Missing handler (warming, error) or a negative difference
        (clock skew) → None, never 0.
        """
        handler = self.perf.get("handler_ms") if isinstance(self.perf, dict) else None
        if self.rtt_ms is not None and isinstance(handler, (int, float)) and not isinstance(handler, bool):
            diff = self.rtt_ms - float(handler)
            self.network_ms = diff if diff >= 0 else None
        else:
            self.network_ms = None

    def to_report(self) -> Dict[str, Any]:
        """Build the wire payload — the ONE place a report is assembled, so the privacy whitelist is
        enforceable by reading this function alone. Only rid + outcome + client timing + worker perf, and on a
        failed act its error's code, message and hint. No secret, no API key, no observation."""
        return {
            **({"error": dict(self.error)} if self.error and self.outcome == OUTCOME_ERROR else {}),
            "rid": self.rid,
            "outcome": self.outcome,
            "client": {
                "total_ms": self.total_ms,
                "rtt_ms": self.rtt_ms,
                "network_ms": self.network_ms,
                "warmup_ms": self.warmup_ms,
                "first_after_connect": self.first_after_connect,
                "connect_ms": self.connect_ms,
                "tcp_ms": self.tcp_ms,
                "tls_ms": self.tls_ms,
                "cc": self.cc,
                "session": self.session,
                "rid_mismatch": self.rid_mismatch,
                "frames": self.frames,
            },
            "perf": dict(self.perf) if isinstance(self.perf, dict) else {},
        }


def latency_record(report: Dict[str, Any], model: str) -> Dict[str, Any]:
    """One report as the gateway's /v1/latency intake files it: under the deployment's name (the gateway checks
    it is the caller's), with the outcome, the client's three timings and the worker's perf block. The full
    client block rides along; the intake stores first_after_connect and the connect split (connect_ms, tcp_ms, tls_ms)
    from it and ignores the rest.
    """
    c = report.get("client") or {}
    return {"rid": report["rid"], "model_id": model, "deployment_id": model, "outcome": report["outcome"],
            "total_ms": c.get("total_ms"), "rtt_ms": c.get("rtt_ms"), "network_ms": c.get("network_ms"),
            "perf": report.get("perf") or {}, "client": c,

            **({"frames": c["frames"]} if c.get("frames") else {}),

            **({"error": report["error"]} if report.get("error") else {})}


def run_record(run: Dict[str, Any], model: str) -> Dict[str, Any]:
    """One stretch of a robot's acts as the gateway's /v1/latency intake files it under `runs` (beside the per-act
    `records`, into run_outcomes): its chunks - the answers held to the one before - how many came after the robot had
    played the one before (underruns) and the time it stood waiting for them (underrun_s), its wall time, why it ended,
    and how long one answer plays (chunk_s). What `seq policy status`, `seq usage --policy` and the console read as its
    on-time share. No observation, no key: the gateway reads the owner and the robot's key from the request. `run_id`
    is the idempotency key."""
    return {"run_id": run.get("run_id"), "model_id": model, "deployment_id": model, "chunks": run.get("chunks"),
            "underruns": run.get("underruns"), "underrun_s": run.get("underrun_s"), "elapsed_s": run.get("elapsed_s"),
            "reason": run.get("reason"), "chunk_s": run.get("chunk_s")}


def connect_record(connect: Dict[str, Any], model: str) -> Dict[str, Any]:
    """One connect as the gateway's /v1/latency intake files it under `connects` (beside `records` and `runs`): how it
    ended, each stage's time and, for one that stopped, the stage and what it was told (connect_trace.ConnectTrace).
    No secret, no key, no worker's address: the gateway reads the owner and the robot's key from the request.
    `connect_id` is the idempotency key."""
    return {"connect_id": connect.get("connect_id"), "model_id": model, "deployment_id": model,
            "outcome": connect.get("outcome"), "reconnect": connect.get("reconnect"),
            "attempts": connect.get("attempts"), "total_ms": connect.get("total_ms"),
            "stages": connect.get("stages") or {}, **({"stage": connect["stage"]} if connect.get("stage") else {}),
            **({"error": connect["error"]} if connect.get("error") else {})}


class Reporter:
    """
    A bounded, async, best-effort shipper of `CallMetrics` reports to the gateway ingest endpoint.

    `record()` is called on the control loop's thread (or a prefetch thread) and must never block or
    raise: it appends to a bounded deque and returns. A single daemon thread batches the buffer and
    POSTs it through the injected `send` callable, swallowing every failure. On `close()` it flushes
    the last partial batch rather than dropping it, so a clean shutdown does not lose telemetry.
    """

    def __init__(self, send: Callable[[List[Dict[str, Any]]], None], *,
                 max_buffer: int = 1024, batch_size: int = 64,
                 flush_interval_s: float = FLUSH_EVERY_S,
                 on_close: Optional[Callable[[], None]] = None) -> None:
        self._send = send


        self._on_close = on_close


        self._buf: "deque[Dict[str, Any]]" = deque(maxlen=max_buffer)
        self._batch_size = batch_size
        self._flush_interval_s = flush_interval_s
        self._lock = threading.Lock()
        self._wake = threading.Event()
        self._closed = False
        self._thread: Optional[threading.Thread] = None

    def record(self, report: Dict[str, Any]) -> None:
        """Queue one report. Non-blocking; drops silently once closed."""
        if self._closed:
            return
        with self._lock:
            self._buf.append(report)
            pending = len(self._buf)
        self._ensure_thread()
        if pending >= self._batch_size:
            self._wake.set()

    def _ensure_thread(self) -> None:

        if self._thread is not None:
            return
        with self._lock:
            if self._thread is not None or self._closed:
                return
            t = threading.Thread(target=self._loop, name="sequence-ai-reporter", daemon=True)
            self._thread = t
        t.start()

    def _drain(self, n: int) -> List[Dict[str, Any]]:
        with self._lock:
            out: List[Dict[str, Any]] = []
            while self._buf and len(out) < n:
                out.append(self._buf.popleft())
            return out

    def _flush_once(self) -> None:
        batch = self._drain(self._batch_size)
        if not batch:
            return
        try:
            self._send(batch)
        except Exception:
            pass

    def _loop(self) -> None:
        while True:
            self._wake.wait(self._flush_interval_s)
            self._wake.clear()

            while True:
                with self._lock:
                    remaining = len(self._buf)
                if remaining == 0:
                    break
                self._flush_once()
            if self._closed:

                self._flush_once()
                return

    def close(self) -> None:
        """Stop the thread and flush the last partial batch. Idempotent; never raises."""
        if self._closed:
            return
        self._closed = True
        self._wake.set()
        t = self._thread
        if t is not None:
            t.join(timeout=2.0)


        while True:
            with self._lock:
                remaining = len(self._buf)
            if remaining == 0:
                break
            self._flush_once()
        if self._on_close is not None:
            try:
                self._on_close()
            except Exception:
                pass
