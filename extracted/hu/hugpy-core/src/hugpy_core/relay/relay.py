# LIFTED from legacy hugpy (read-only reference):
#   _WORKER_FINISH_MAP, _event_from_worker_line <- py/inference/hugpy_engine/src/hugpy_engine/resolvers/remote.py:3113-3175
#   _worker_stream (SSE line loop)              <- remote.py:3212-3282
#   worker payload                               <- remote.py:_worker_payload 2999 (contract fields only)
# CHANGED: events are plain dicts (no StreamEvent classes); transport is a plain
#   blocking urllib stream (no breaker / async client); a >=400 head raises
#   WorkerHTTPError with the worker's JSON body.
# DROPPED: _force_local, spill, alloc on the wire, relay load-failure recording.
"""Relay one chat to a worker's POST /infer/stream and yield its events."""
from __future__ import annotations

import contextlib
import http.client
import json
import select
import socket
import threading
import urllib.error
import urllib.request
from typing import Any, Dict, Iterator, Optional

# llama.cpp / OpenAI finish reasons -> DoneEvent's strict Literal.
_WORKER_FINISH_MAP = {
    "length": "max_tokens", "max_tokens": "max_tokens",
    "stop": "stop", "eos": "stop", None: "stop",
    "cancelled": "cancelled", "error": "error",
}

WORKER_PAYLOAD_KEYS = ("model_key", "messages", "request_id", "task",
                       "max_new_tokens", "temperature", "top_p", "knobs", "metadata")


# A call to a worker's front door waits in that worker's queue for as long as the queue needs: there is no read
# deadline (operator 2026-11-16: "a 6 hour per call timeout? what even is this for?"). With a 600 s socket timeout
# here, 205 of a 261-call test fire failed "TimeoutError: timed out" at exactly 600 s while their calls were still
# queued at the Wrapper, which went on serving them for nobody. Reaching the worker is bounded (CONNECT_TIMEOUT_S);
# after that a dead peer is noticed by TCP keepalive, and a caller that hangs up is noticed by watching ITS socket
# (CALLER_CHECK_S): the upstream socket is then shut, so the worker (the Wrapper cancels a parked call whose caller
# hung up) stops working for nobody. A caller that passes a number keeps that socket timeout throughout, as before.
CONNECT_TIMEOUT_S = 30.0
CALLER_CHECK_S = 5.0
_UPSTREAM = threading.local()        # the request thread's upstream socket, recorded at connect for the watcher


class CallerGone(ConnectionError):
    """The caller hung up while its call waited at the worker; the worker was told (its socket shut)."""


def _keepalive(sock) -> None:
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        for name, value in (("TCP_KEEPIDLE", 60), ("TCP_KEEPINTVL", 15), ("TCP_KEEPCNT", 4)):
            if hasattr(socket, name):
                sock.setsockopt(socket.IPPROTO_TCP, getattr(socket, name), value)
    except OSError:
        pass


def _waiting(sock) -> None:
    """A connected upstream socket: keepalive on, no read deadline, recorded for the caller watcher."""
    _keepalive(sock)
    sock.settimeout(None)
    ref = getattr(_UPSTREAM, "ref", None)
    if ref is not None:
        ref["sock"] = sock


class _QueueWaitHTTPConnection(http.client.HTTPConnection):
    def connect(self):
        super().connect()                 # bounded by the connect timeout
        _waiting(self.sock)


class _QueueWaitHTTPSConnection(http.client.HTTPSConnection):
    def connect(self):
        super().connect()                 # TCP + TLS handshake bounded by the connect timeout
        _waiting(self.sock)


class _QueueWaitHTTPHandler(urllib.request.HTTPHandler):
    def http_open(self, req):
        return self.do_open(_QueueWaitHTTPConnection, req)


class _QueueWaitHTTPSHandler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(_QueueWaitHTTPSConnection, req, context=self._context)


_QUEUE_WAIT = urllib.request.build_opener(_QueueWaitHTTPHandler, _QueueWaitHTTPSHandler)


def _open(req, timeout: Optional[float]):
    """timeout None: connect within CONNECT_TIMEOUT_S, then wait for the answer as long as the worker's queue needs;
    a number: that socket timeout throughout (connect and every read), as before. HTTPError as urlopen raises it."""
    if timeout is None:
        return _QUEUE_WAIT.open(req, timeout=CONNECT_TIMEOUT_S)
    return urllib.request.urlopen(req, timeout=timeout)


def _peer_closed(sock) -> bool:
    """Whether the peer on `sock` hung up (FIN or reset). Its request was read whole, so a readable socket that peeks
    EMPTY is its close. Never consumes a byte, never blocks; a socket that cannot be peeked (TLS) reads as live."""
    try:
        readable, _, _ = select.select([sock], [], [], 0)
    except (OSError, ValueError):
        return True
    if not readable:
        return False
    try:
        return sock.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT) == b""
    except (BlockingIOError, InterruptedError, ValueError):
        return False
    except OSError:
        return True


def _caller_socket():
    """The socket of the request being served on this thread (werkzeug's environ), or None outside a request."""
    try:
        from flask import has_request_context, request
        return request.environ.get("werkzeug.socket") if has_request_context() else None
    except Exception:  # noqa: BLE001 — no request, no watcher
        return None


@contextlib.contextmanager
def _follows_caller(active: bool):
    """While the block runs (the upstream connect, the queue wait, the answer), watch the caller's socket every
    CALLER_CHECK_S; when the caller has hung up, shut the upstream socket — which ends the blocked read here and
    tells the worker. Yields a dict: "caller_gone" is set when that happened."""
    ref: dict = {}
    caller = _caller_socket() if active else None
    stop = threading.Event()
    _UPSTREAM.ref = ref
    if caller is not None:
        def watch():
            while not stop.wait(CALLER_CHECK_S):
                if _peer_closed(caller):
                    ref["caller_gone"] = True
                    up = ref.get("sock")
                    if up is not None:
                        try:
                            up.shutdown(socket.SHUT_RDWR)
                        except OSError:
                            pass
                    return
        threading.Thread(target=watch, daemon=True, name="relay-caller-watch").start()
    try:
        yield ref
    finally:
        stop.set()
        _UPSTREAM.ref = None


class WorkerHTTPError(Exception):
    def __init__(self, status: int, body: Any, url: str):
        self.status, self.body, self.url = status, body, url
        msg = body.get("error") if isinstance(body, dict) else None
        super().__init__(f"worker {url} HTTP {status}: {msg or body}")


def worker_payload(kwargs: dict, worker: "dict | None" = None) -> dict:
    """The worker's /infer body. With ``worker`` given, the pair's operator knobs
    (hugpy_core.model_workers.user_settings) ride along as ``knobs``."""
    out = {k: kwargs[k] for k in WORKER_PAYLOAD_KEYS if kwargs.get(k) is not None}
    if worker is not None and out.get("model_key"):
        # the request names the model as this worker serves it (a short or default name is not one)
        from hugpy_core.relay.pick import served_name
        out["model_key"] = served_name(out["model_key"], worker)
    # The former engine request schema merged adjacent plain turns before
    # dispatch. Core's relay takes raw dicts, so restore that behavior here for
    # both /v1 and the console stream, including older /infer workers.
    if out.get("messages"):
        from hugpy_resources.imports.functions import merge_consecutive_messages
        out["messages"] = merge_consecutive_messages(out["messages"])
    if worker is not None and out.get("model_key") and not is_native(worker):
        from hugpy_core.models.modeldb import get_knobs
        knobs = get_knobs(out["model_key"], worker["id"])
        # a call's own knobs (OpenAI `knobs`, e.g. from `model@options`) override
        # single settings; the pair's other knobs still apply
        if isinstance(out.get("knobs"), dict):
            knobs = {**knobs, **{k: v for k, v in out["knobs"].items() if k != "blocked"}}
        if knobs:
            out["knobs"] = knobs
    from hugpy_core.calllog.call_record import dispatch
    return dispatch(out, worker or {})


def event_from_worker_line(d: dict) -> Optional[Dict[str, Any]]:
    """Map one worker SSE dict to a token/done/error event; None for the rest
    (request/status) — the router has no browser to show progress to."""
    t = d.get("type")
    if t == "token":
        return {"type": "token", "text": d.get("text", "")}
    if t == "done":
        # Workers emit raw llama.cpp reasons ('length', 'stop', ...); map first.
        return {"type": "done",
                "finish_reason": _WORKER_FINISH_MAP.get(d.get("finish_reason"), "stop"),
                "execution_request_id": d.get("execution_request_id"),
                "worker_request_id": d.get("worker_request_id"),
                "usage": d.get("usage") if isinstance(d.get("usage"), dict) else None,
                "timings": d.get("timings") if isinstance(d.get("timings"), dict) else None}
    if t == "error":
        return {"type": "error", "message": d.get("message", "worker error"),
                "code": (str(d.get("code")) if d.get("code") else None),
                "execution_request_id": d.get("execution_request_id"),
                "worker_request_id": d.get("worker_request_id")}
    return None


def is_native(worker: dict) -> bool:
    return (worker.get('data_service') or {}).get('implementation') == 'hugpy-wrapper-native'


def is_front_door(worker: dict) -> bool:
    """A box reached through the router: its wrapper speaks OpenAI /v1, not /infer."""
    eng = worker.get("engine")
    return is_native(worker) or isinstance(eng, dict) and eng.get("name") == "fitevict"


def _openai_body(payload: dict) -> dict:
    from hugpy_core.brain.intent import stamp
    body = {"model": payload.get("model_key"), "messages": payload.get("messages") or [], "stream": True,
            "stream_options": {"include_usage": True}}
    for src, dst in (("max_new_tokens", "max_tokens"), ("temperature", "temperature"), ("top_p", "top_p"),
                     ("knobs", "knobs"), ("task", "task")):
        if payload.get(src) is not None:
            body[dst] = payload[src]
    # Every hop carries the call's intent in its body, so whatever records the call
    # next (any wrapper version) records the label core gave it on arrival.
    body["metadata"] = stamp(payload.get("metadata"), payload.get("intent"))
    if payload.get("request_id") and not body["metadata"].get("parent_request_id"):
        body["metadata"]["parent_request_id"] = str(payload["request_id"])
    return body


# "unbounded (auto-continue)" as the live hugpy_server streamed it (streaming.py /
# base_runner.stream_chat_unbounded): each pass may run to DEFAULT_MAX_TOKENS; a pass
# that stops on the cap is followed by a user "continue" turn, up to MAX_ROUNDS passes.
# -1 = llama.cpp n_predict -1: run until the model stops (or the window fills). A positive
# per-pass budget would also become the wrapper's context FLOOR (sizing need_tokens) and
# push a model that fits the card at a smaller window off it (seen 2026-10-08: 32768 ->
# allura 35B ram-only at 11 tok/s instead of gpu-only at 163).
UNBOUNDED_ROUND = int(__import__("os").environ.get("HUGPY_DEFAULT_MAX_TOKENS") or -1)
MAX_ROUNDS = int(__import__("os").environ.get("HUGPY_MAX_CHUNKS") or 256)


def front_door_stream(worker: dict, payload: dict, timeout: Optional[float] = None) -> Iterator[Dict[str, Any]]:
    """Relay one chat to a box's wrapper through the router (POST /v1/chat/completions,
    streamed) as the same token/done/error events the /infer path yields. The call's
    request_id rides as X-Hugpy-Parent-Request-Id, so the box's call_log row points at
    core's; the box answers with its own id (X-Hugpy-Execution-Request-Id).

    A caller with no cap (the console's "unbounded (auto-continue)") gets UNBOUNDED_ROUND
    tokens per round — the wrapper's own default is 128, which a thinking model spends
    entirely on reasoning — and when a round stops on the cap, the reply is continued
    from where it stopped (the answer so far as the assistant's prefill)."""
    unbounded = payload.get("max_new_tokens") is None and not is_native(worker)
    p = dict(payload)
    if unbounded:
        p["max_new_tokens"] = UNBOUNDED_ROUND
    text, total, last = "", {}, None
    for _round in range(MAX_ROUNDS if unbounded else 1):
        if text:
            p["messages"] = list(payload.get("messages") or []) + [{"role": "assistant", "content": text},
                                                                   {"role": "user", "content": "continue"}]
        for ev in _front_door_round(worker, p, timeout):
            if ev["type"] == "token":
                text += ev["text"]
                yield ev
            elif ev["type"] == "error":
                yield ev
                return
            else:
                last = ev
                for k, v in (ev.get("usage") or {}).items():
                    if isinstance(v, int):
                        total[k] = total.get(k, 0) + v
        if not last or last.get("finish_reason") != "max_tokens" or not unbounded or not text:
            break
    if last is not None:
        yield {**last, "usage": total or last.get("usage")}


def _front_door_round(worker: dict, payload: dict, timeout: Optional[float]) -> Iterator[Dict[str, Any]]:
    with _follows_caller(timeout is None) as watch:
        try:
            for ev in _front_door_events(worker, payload, timeout):
                if ev.get("type") == "done" and watch.get("caller_gone"):   # a shut stream reads as a short answer
                    raise CallerGone("the caller hung up while its call waited at the worker; the worker was told")
                yield ev
        except (OSError, http.client.HTTPException) as exc:
            if watch.get("caller_gone") and not isinstance(exc, CallerGone):
                raise CallerGone("the caller hung up while its call waited at the worker; the worker was told") from exc
            raise


def _front_door_events(worker: dict, payload: dict, timeout: Optional[float]) -> Iterator[Dict[str, Any]]:
    from hugpy_core.registry.transport import headers as worker_headers
    url = worker["url"].rstrip("/") + "/v1/chat/completions"
    headers = worker_headers(worker, {"Content-Type": "application/json", "Accept": "text/event-stream"})
    if payload.get("_station_lease"):
        headers["X-Hugpy-Station-Lease"] = str(payload["_station_lease"])
    if payload.get("request_id"):
        headers["X-Hugpy-Parent-Request-Id"] = str(payload["request_id"])
    if is_native(worker) and payload.get("request_id"):
        headers["Idempotency-Key"] = str(payload["request_id"])
    req = urllib.request.Request(url, data=json.dumps(_openai_body(payload)).encode("utf-8"),
                                 headers=headers, method="POST")
    try:
        resp = _open(req, timeout)
    except urllib.error.HTTPError as exc:
        body = None
        try:
            body = json.loads(exc.read().decode("utf-8") or "null")
        except Exception:  # noqa: BLE001
            body = None
        raise WorkerHTTPError(exc.code, body, url) from exc
    from hugpy_core.calllog.call_record import current
    exec_id = resp.headers.get("X-Hugpy-Execution-Request-Id")
    row = current()
    if row is not None and exec_id:
        row.setdefault("response_meta", {})["execution_request_id"] = exec_id
    finish, usage, timings, thinking = None, None, None, False
    with resp:
        for raw_line in resp:
            line = raw_line.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            raw = line[len("data:"):].strip()
            if not raw or raw == "[DONE]":
                continue
            try:
                d = json.loads(raw)
            except ValueError:
                continue
            if not isinstance(d, dict):
                continue
            # the box carries its execution call-log id in-band (hugpy.request_id on
            # the terminal chunk) as well as in the response header: a header-dropping
            # router cannot lose it. In-band wins — it names the row that actually
            # answered (a ctx-retry relaunch's row, not the first attempt's header).
            in_band = d.get("hugpy")
            if isinstance(in_band, dict) and in_band.get("request_id"):
                exec_id = in_band["request_id"]
                if row is not None:
                    row.setdefault("response_meta", {})["execution_request_id"] = exec_id
            if d.get("error"):
                err = d["error"] if isinstance(d["error"], dict) else {"message": str(d["error"])}
                if row is not None:
                    row.update(error=err.get("message"), http_status=502)
                yield {"type": "error", "message": err.get("message", "worker error"),
                       "code": str(err.get("code")) if err.get("code") else None,
                       "execution_request_id": exec_id, "worker_request_id": None}
                return
            if isinstance(d.get("usage"), dict):
                usage = d["usage"]
            if isinstance(d.get("timings"), dict):
                timings = d["timings"]
            for ch in d.get("choices") or []:
                delta = ch.get("delta") or {}
                thought = delta.get("reasoning_content")
                if thought:
                    if not thinking:
                        thinking = True
                        yield {"type": "token", "text": "<think>"}
                    yield {"type": "token", "text": thought}
                text = delta.get("content")
                if text:
                    if thinking:
                        thinking = False
                        yield {"type": "token", "text": "</think>"}
                    yield {"type": "token", "text": text}
                if ch.get("finish_reason"):
                    finish = ch["finish_reason"]
    if thinking:
        yield {"type": "token", "text": "</think>"}
    yield {"type": "done", "finish_reason": _WORKER_FINISH_MAP.get(finish, "stop"),
           "execution_request_id": exec_id, "worker_request_id": None, "usage": usage, "timings": timings}


def worker_stream(worker: dict, payload: dict, timeout: Optional[float] = None) -> Iterator[Dict[str, Any]]:
    """Relay a worker's POST /infer/stream SSE as event dicts (a box behind the
    router: its OpenAI /v1/chat/completions, front_door_stream). timeout None (the
    default): connect within CONNECT_TIMEOUT_S, then wait as long as the worker's queue
    needs; a number: that socket timeout throughout."""
    if is_front_door(worker):
        yield from front_door_stream(worker, payload, timeout)
        return
    url = worker["url"].rstrip("/") + "/infer/stream"
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"},
                                 method="POST")
    try:
        resp = _open(req, timeout)
    except urllib.error.HTTPError as exc:
        body = None
        try:
            body = json.loads(exc.read().decode("utf-8") or "null")
        except Exception:  # noqa: BLE001 — a bodyless 5xx is still a 5xx
            body = None
        raise WorkerHTTPError(exc.code, body, url) from exc
    with resp:
        for raw_line in resp:
            line = raw_line.decode("utf-8", "replace").strip()
            if not line or not line.startswith("data:"):
                continue
            raw = line[len("data:"):].strip()
            if not raw:
                continue
            try:
                d = json.loads(raw)
            except ValueError:
                continue
            ev = event_from_worker_line(d) if isinstance(d, dict) else None
            if ev is None:
                continue
            from hugpy_core.calllog.call_record import current
            row = current()
            if row is not None:
                if ev.get("type") == "error":
                    row.update(error=ev.get("message"), http_status=502)
                if ev.get("execution_request_id"):
                    row.setdefault("response_meta", {})["execution_request_id"] = ev["execution_request_id"]
                if ev.get("worker_request_id"):
                    row.setdefault("response_meta", {})["worker_request_id"] = ev["worker_request_id"]
            yield ev


def worker_cancel(worker: dict, request_id: str) -> "tuple[int, dict]":
    """POST {worker}/infer/cancel/<rid>; returns (status, body)."""
    from urllib.parse import quote
    from hugpy_core.registry.transport import headers as worker_headers
    sql = is_native(worker) or (worker.get('data_service') or {}).get('implementation') == 'hugpy-wrapper-sql'
    path = ('/v1/requests/' + quote(request_id, safe='') + '/cancel' if sql
            else '/infer/cancel/' + quote(request_id, safe=''))
    url = worker["url"].rstrip("/") + path
    req = urllib.request.Request(url, data=b"", method="POST", headers=worker_headers(worker))
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "{}")
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read().decode("utf-8") or "{}")
        except Exception:  # noqa: BLE001
            return exc.code, {"cancelled": False}
