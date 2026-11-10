"""HeldStreams: `api.call` with `stream: true` (the live events' SSE, plan D10): the service holds the upstream
response and writes its bytes into the socket the caller passed as they come. Its own threads, connections and
budget (in all, and per caller), so a held stream never takes a heartbeat's thread or connection, and one caller
never takes every slot. DESIGN.md "Held streams"."""

from __future__ import annotations

import base64
import concurrent.futures
import contextlib
import os
import select
import socket
import threading
import time
from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass

from probe.foundation.service_api.vocabularies import RelayFailure

from .request import ApiCall
from .targets import AllowedTargets
from .upstream import DECODED_DROPS, INLINE_BYTES, get_failure_kind, get_timeout_parts, make_client

#: Streams one service holds at once; past it a stream is refused as never sent and its caller reconnects later.
#: Each holds one thread and one connection of its own.
MAX_STREAMS = 64
#: Streams one calling process holds at once (a process's producers and watchers), so neither one caller (a
#: sandboxed one included) nor one job's ranks take every slot.
MAX_STREAMS_PER_CALLER = 16
#: A reader that has not taken a byte for this long (its socket full) is let go: it reconnects from its cursor.
STALLED_READER_S = 120.0


@dataclass(eq=False)
class _Held:
    """One stream from its admission to its end; what `close()` cuts."""

    call: ApiCall
    client: object | None = None
    response: object | None = None
    sink: socket.socket | None = None
    is_streaming: bool = False


class HeldStreams:
    """`open(call)` -> a future of the answer at the response's headers (`{status, headers, http_version,
    streaming: true}`, or an `api.call` answer: a refusal with its body inline, a failure); the body then
    goes into the caller's socket until the server ends it, the caller shuts its end, or `close()`."""

    def __init__(self, *, targets: AllowedTargets, log: Callable[[str], None] = lambda message: None) -> None:
        self.targets = targets
        self.log = log
        self._pool = concurrent.futures.ThreadPoolExecutor(MAX_STREAMS, thread_name_prefix="probe-relay-stream")
        self._lock = threading.Lock()
        self._held: set[_Held] = set()
        self._per_caller: Counter = Counter()
        self._is_closing = False
        self.opened = self.ended = 0
        #: Refusals by why: the service's budget, the caller's, a sandboxed caller's target.
        self.refused_budget = self.refused_caller = self.refused_target = 0

    def open(self, call: ApiCall) -> concurrent.futures.Future:
        answer: concurrent.futures.Future = concurrent.futures.Future()
        held, refusal = self._take_slot(call)
        if held is None:
            call.close()
            answer.set_result(refusal)
            return answer
        try:
            future = self._pool.submit(self._run, held, answer)
        except RuntimeError:  # shut down meanwhile
            self._settle(held)
            answer.set_result(_STOPPING)
            return answer
        future.add_done_callback(lambda done: self._settle_cancelled(done, held, answer))
        return answer

    def get_counts(self) -> dict:
        """`service.status`'s `relay.streams`."""
        with self._lock:
            return {"held": len(self._held), "opened": self.opened, "ended": self.ended,
                    "refused_budget": self.refused_budget, "refused_caller": self.refused_caller,
                    "refused_target": self.refused_target}

    def close(self) -> None:
        """No new stream; every held one is cut, whatever it is doing (connecting, reading the server, waiting on
        its reader): its caller sees the end and reconnects. A stream still queued frees its slot and socket."""
        from probe.sdk.delivery.transport.streams import cut_stream  # noqa: PLC0415 -- only at a stop

        with self._lock:
            self._is_closing = True
            held = list(self._held)
        self._pool.shutdown(wait=False, cancel_futures=True)
        for stream in held:
            if stream.response is not None:
                cut_stream(stream.response)
            elif stream.client is not None:
                with contextlib.suppress(Exception):
                    stream.client.close()
            if stream.sink is not None:
                with contextlib.suppress(OSError):
                    stream.sink.shutdown(socket.SHUT_RDWR)

    # -- one stream ------------------------------------------------------------------------------

    def _take_slot(self, call: ApiCall) -> tuple[_Held | None, dict | None]:
        with self._lock:
            if self._is_closing:
                return None, _STOPPING
            if len(self._held) >= MAX_STREAMS:
                self.refused_budget += 1
                why = f"this Probe service already holds {MAX_STREAMS} streams"
            elif self._per_caller[call.caller_pid] >= MAX_STREAMS_PER_CALLER:
                self.refused_caller += 1
                why = f"this process already holds {MAX_STREAMS_PER_CALLER} streams through the Probe service"
            else:
                held = _Held(call)
                self._held.add(held)
                self._per_caller[call.caller_pid] += 1
                return held, None
        self.log(f"warning: relay: a held stream refused (pid {call.caller_pid}): {why}")
        return None, {"failed": RelayFailure.EXPIRED, "message": why}

    def _run(self, held: _Held, answer: concurrent.futures.Future) -> None:
        try:
            refusal = self._check(held.call)
            if refusal is not None:
                answer.set_result(refusal)
                return
            self._forward_body(held, answer)
        except Exception as exc:  # noqa: BLE001 -- one bad stream never stops the relay
            if not answer.done():
                answer.set_result({"failed": get_failure_kind(exc), "message": f"{type(exc).__name__}: {exc}"[:2000]})
        finally:
            self._settle(held)

    def _check(self, call: ApiCall) -> dict | None:
        if self._is_closing:
            return _STOPPING
        if call.expires_at is not None and time.monotonic() >= call.expires_at:
            return {"failed": RelayFailure.EXPIRED, "message": "the caller's deadline passed while it waited"}
        if not self.targets.is_allowed(call.url, is_fenced=call.is_fenced):
            with self._lock:
                self.refused_target += 1
            self.log(f"warning: relay: a sandboxed caller's stream refused (pid {call.caller_pid}): not the API")
            return {"failed": RelayFailure.REFUSED,
                    "message": "a caller in a sandbox reaches only the Probe API and the storage it hands out"}
        return None

    def _forward_body(self, held: _Held, answer: concurrent.futures.Future) -> None:
        import httpx

        call = held.call
        held.client = client = make_client(call.env, httpx.Limits(max_connections=1, max_keepalive_connections=0))
        try:
            request = client.build_request(call.method, call.url, headers=call.headers,
                                           timeout=httpx.Timeout(**get_timeout_parts(call.timeout)))
            held.response = response = client.send(request, stream=True)
            try:
                if self._is_closing:
                    answer.set_result(_STOPPING)
                    return
                headers = [[name, value] for name, value in response.headers.multi_items()
                           if name.lower() not in DECODED_DROPS]
                head = {"status": response.status_code, "headers": headers, "http_version": response.http_version}
                if not 200 <= response.status_code < 300:
                    # A refusal is an ordinary answer, its body inline (the caller reads its error from it).
                    answer.set_result({**head, "body": base64.b64encode(_read_head(response)).decode("ascii")})
                    return
                held.sink = socket.socket(fileno=os.dup(call.sink_fd))
                held.sink.setblocking(False)
                with self._lock:
                    self.opened += 1
                    held.is_streaming = True
                answer.set_result({**head, "streaming": True})
                for chunk in response.iter_bytes():
                    if not _write_sink(held.sink, chunk):
                        break
            finally:
                response.close()
        finally:
            client.close()

    def _settle(self, held: _Held) -> None:
        """The stream is over: its slot, its caller's count and its sockets go back."""
        with self._lock:
            if held not in self._held:
                return
            self._held.discard(held)
            self._per_caller[held.call.caller_pid] -= 1
            if self._per_caller[held.call.caller_pid] <= 0:
                del self._per_caller[held.call.caller_pid]
            if held.is_streaming:
                self.ended += 1
        if held.sink is not None:
            # Shut, not only closed: the reader sees the end even if a copy of its socket lives elsewhere.
            with contextlib.suppress(OSError):
                held.sink.shutdown(socket.SHUT_RDWR)
            held.sink.close()
        held.call.close()

    def _settle_cancelled(self, done: concurrent.futures.Future, held: _Held,
                          answer: concurrent.futures.Future) -> None:
        """A stream still queued when the pool shut down never ran: its slot and socket go back all the same."""
        if done.cancelled():
            self._settle(held)
            if not answer.done():
                answer.set_result(_STOPPING)


_STOPPING = {"failed": RelayFailure.OTHER, "message": "the Probe service is stopping"}


def _read_head(response) -> bytes:
    """A refusal's body, at most INLINE_BYTES of it, read as it comes (never the whole of an endless one)."""
    body = bytearray()
    for chunk in response.iter_bytes():
        body += chunk
        if len(body) >= INLINE_BYTES:
            break
    return bytes(body[:INLINE_BYTES])


def _write_sink(sink: socket.socket, data: bytes) -> bool:
    """All of `data` into the caller's socket; False once its reader is gone (shut, or every copy closed) or has
    taken nothing for STALLED_READER_S. `poll`, never `select`: a caller's fd may be past 1023."""
    view = memoryview(data)
    poller = select.poll()
    poller.register(sink.fileno(), select.POLLOUT)
    while view:
        try:
            view = view[sink.send(view):]
        except BlockingIOError:
            if not poller.poll(STALLED_READER_S * 1000):
                return False
        except OSError:
            return False
    return True
