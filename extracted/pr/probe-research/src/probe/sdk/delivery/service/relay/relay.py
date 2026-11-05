"""Relay: sends the HTTP requests training processes packaged (`api.call`, plan D10) on threads of its
own, two lanes so a heartbeat never waits behind a part upload, one kept-alive httpx client per set of
network settings. An answer's body rides inline when small, else it streams into the file the caller
passed (`body_sink`), with progress events that keep the caller waiting. DESIGN.md beside this file."""

from __future__ import annotations

import base64
import concurrent.futures
import importlib
import os
import threading
import time
from collections.abc import Callable, Iterator

from probe.foundation.service_api.vocabularies import RelayFailure
from .request import ApiCall, FileBody
from .targets import AllowedTargets

#: Requests sent at once per lane, at most (never the hooks' or commands' threads).
SMALL_THREADS = 8
BULK_THREADS = 8
#: A response body up to this size rides in the answer (base64 keeps the line under 1 MiB).
INLINE_BYTES = 512 * 1024
#: A body is read and written this much at a time.
CHUNK_BYTES = 1 << 20
#: While a body streams into the caller's file, a progress event at least this often.
PROGRESS_EVERY_S = 1.0
#: httpx clients kept, one per set of network settings, at most.
MAX_CLIENTS = 8
#: Headers that describe the wire, not the body handed back (it is decoded here).
DECODED_DROPS = frozenset({"content-encoding", "content-length", "transfer-encoding"})


class Relay:
    """`submit(call, progress)` -> a future of `api.call`'s answer (`{status, headers, body |
    body_in_sink}` or `{failed, message}`); never raises into the future. `progress(bytes)` is
    called while a body streams; it answers False once the caller's connection is gone."""

    def __init__(self, *, log: Callable[[str], None] = lambda message: None) -> None:
        self.log = log
        self._lanes = {
            "small": concurrent.futures.ThreadPoolExecutor(SMALL_THREADS, thread_name_prefix="probe-relay"),
            "bulk": concurrent.futures.ThreadPoolExecutor(BULK_THREADS, thread_name_prefix="probe-relay-bulk"),
        }
        self._lock = threading.Lock()
        #: key -> [client, users]; a client in use is never closed by an eviction (L5).
        self._clients: dict[tuple, list] = {}
        self.targets = AllowedTargets()
        self.sent = self.failed = self.expired = self.refused = 0
        #: Calls from a fenced caller (D25): they reach only the API and its storage.
        self.fenced = 0
        self._in_flight = 0
        self._lanes["bulk"].submit(importlib.import_module, "httpx")  # L6: never on the event loop

    def submit(self, call: ApiCall, progress: Callable[[int], bool] = lambda done: True) -> concurrent.futures.Future:
        with self._lock:
            self._in_flight += 1
        try:
            future = self._lanes[call.lane].submit(self._send, call, progress)
        except BaseException:
            call.close()
            self._settle()
            raise
        future.add_done_callback(lambda _: self._settle())
        return future

    def count_in_flight(self) -> int:
        """Calls taken and not yet answered."""
        with self._lock:
            return self._in_flight

    def _settle(self) -> None:
        with self._lock:
            self._in_flight -= 1

    def public(self) -> dict:
        with self._lock:
            return {"sent": self.sent, "failed": self.failed, "expired": self.expired, "refused": self.refused,
                    "fenced": self.fenced, "in_flight": self._in_flight, "clients": len(self._clients)}

    def close(self) -> None:
        for pool in self._lanes.values():
            pool.shutdown(wait=False, cancel_futures=True)
        with self._lock:
            entries, self._clients = list(self._clients.values()), {}
        for client, users in entries:
            if users == 0:
                client.close()

    # -- one request ---------------------------------------------------------

    def _send(self, call: ApiCall, progress: Callable[[int], bool]) -> dict:
        try:
            if call.expires_at is not None and time.monotonic() >= call.expires_at:
                self._count("expired")
                return {"failed": RelayFailure.EXPIRED, "message": "the caller's deadline passed while it waited"}
            if call.is_fenced:
                self._count("fenced")
            if not self.targets.is_allowed(call.url, is_fenced=call.is_fenced):
                self._count("refused")
                return {"failed": RelayFailure.REFUSED,
                        "message": "a caller in a sandbox reaches only the Probe API and the storage it hands out"}
            return self._exchange(call, progress)
        except Exception as exc:  # noqa: BLE001 -- one bad call never stops the relay
            self._count("failed")
            return {"failed": _get_failure(exc), "message": f"{type(exc).__name__}: {exc}"[:2000]}
        finally:
            call.close()

    def _exchange(self, call: ApiCall, progress: Callable[[int], bool]) -> dict:
        import httpx

        key, client = self._take_client(call.env)
        try:
            content = call.body if call.file_body is None else _read_file(call.file_body)
            request = client.build_request(
                call.method, call.url, headers=call.headers, content=content,
                timeout=httpx.Timeout(**_get_timeout_parts(call.timeout)),
            )
            response = client.send(request, stream=True)
            try:
                answer = self._answer(call, response, progress)
            finally:
                response.close()
        finally:
            self._release_client(key)
        if "failed" in answer:
            self._count("failed")
        else:
            self._count("sent")
        return answer

    def _answer(self, call: ApiCall, response, progress: Callable[[int], bool]) -> dict:
        """The response, decoded: inline up to INLINE_BYTES, else streamed into the caller's file."""
        headers = [[name, value] for name, value in response.headers.multi_items() if name.lower() not in DECODED_DROPS]
        held = bytearray()
        written = 0
        said_at = time.monotonic()
        for chunk in response.iter_bytes(CHUNK_BYTES):
            if call.max_bytes is not None and len(held) + written + len(chunk) > call.max_bytes:
                return {"failed": RelayFailure.TOO_LARGE, "message": f"the body is over {call.max_bytes} bytes"}
            if written == 0 and len(held) + len(chunk) <= INLINE_BYTES:
                held += chunk
                continue
            if call.sink_fd is None:
                return {"failed": RelayFailure.TOO_LARGE, "message": "a body over 512 KiB needs a body_sink"}
            if held:
                written += _write_all(call.sink_fd, bytes(held), written)
                held = bytearray()
            written += _write_all(call.sink_fd, chunk, written)
            if time.monotonic() - said_at >= PROGRESS_EVERY_S:
                said_at = time.monotonic()
                if not progress(written):
                    return {"failed": RelayFailure.OTHER, "message": "the caller is gone"}
        answer = {"status": response.status_code, "headers": headers, "http_version": response.http_version}
        if written:
            answer["body_in_sink"] = written
        else:
            body = bytes(held)
            answer["body"] = base64.b64encode(body).decode("ascii")
            self.targets.record_answer(call.url, response.status_code, response.headers.get("content-type", ""), body)
        return answer

    def _count(self, what: str) -> None:
        with self._lock:
            setattr(self, what, getattr(self, what) + 1)

    # -- clients -------------------------------------------------------------

    def _take_client(self, env: dict):
        """The kept-alive client for `env`'s proxies and CAs (the caller's; a fenced caller's are this
        service's own, set by `SdkMethods.call_api`), counted as in use until `_release_client`."""
        import httpx

        from probe.foundation.tls.tls import ssl_context

        key = tuple(sorted(env.items()))
        with self._lock:
            entry = self._clients.get(key)
            if entry is not None:
                entry[1] += 1
                return key, entry[0]
        verify = ssl_context(env)
        mounts = {pattern: (None if proxy is None else httpx.HTTPTransport(proxy=proxy, verify=verify))
                  for pattern, proxy in _get_proxy_mounts(env).items()}
        client = httpx.Client(
            verify=verify, mounts=mounts, trust_env=False, follow_redirects=False,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20, keepalive_expiry=60.0),
        )
        evicted = []
        with self._lock:
            entry = self._clients.get(key)
            if entry is None:
                entry = self._clients[key] = [client, 0]
            else:
                evicted.append(client)  # another thread built one meanwhile: its wins
            entry[1] += 1
            for other_key in list(self._clients):
                if len(self._clients) <= MAX_CLIENTS:
                    break
                other = self._clients[other_key]
                if other_key != key and other[1] == 0:
                    evicted.append(self._clients.pop(other_key)[0])
        for old in evicted:
            old.close()
        return key, entry[0]

    def _release_client(self, key: tuple) -> None:
        with self._lock:
            entry = self._clients.get(key)
            if entry is not None:
                entry[1] = max(0, entry[1] - 1)


def _write_all(fd: int, data: bytes, offset: int) -> int:
    """`data` at `offset` of the caller's file, by `pwrite` until it is all there (L1)."""
    done = 0
    view = memoryview(data)
    while done < len(data):
        done += os.pwrite(fd, view[done:], offset + done)
    return done


def _read_file(body: FileBody) -> Iterator[bytes]:
    """`body`'s bytes, by `pread`: the caller's file offset never moves."""
    done = 0
    while done < body.length:
        chunk = os.pread(body.fd, min(CHUNK_BYTES, body.length - done), body.offset + done)
        if not chunk:
            break  # it shrank: short, and the length the caller declared fails the request
        done += len(chunk)
        yield chunk


def _get_timeout_parts(parts: dict) -> dict:
    """httpx's four timeouts from `api.call`'s (30 s each when the caller named none)."""
    return {name: parts.get(name, 30.0) for name in ("connect", "read", "write", "pool")}


def _get_failure(exc: Exception) -> str:
    import httpx

    if isinstance(exc, (httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout, httpx.UnsupportedProtocol)):
        return RelayFailure.CONNECT
    if isinstance(exc, httpx.TimeoutException):
        return RelayFailure.TIMEOUT
    if isinstance(exc, (httpx.RemoteProtocolError, httpx.ReadError, httpx.WriteError, httpx.LocalProtocolError)):
        return RelayFailure.PROTOCOL
    return RelayFailure.OTHER


def _get_proxy_mounts(env: dict) -> dict:
    """httpx's mounts for `env`'s proxy variables, as httpx reads its own environment
    (`httpx._utils.get_environment_proxies`): lower case first, NO_PROXY hosts go direct."""
    proxies: dict[str, str] = {}
    for name, value in sorted(env.items(), key=lambda item: item[0].islower()):
        if value and name.lower().endswith("_proxy"):
            proxies[name.lower()[: -len("_proxy")]] = value
    mounts: dict[str, str | None] = {}
    for scheme in ("http", "https", "all"):
        url = proxies.get(scheme)
        if url:
            mounts[f"{scheme}://"] = url if "://" in url else f"http://{url}"
    for host in (h.strip() for h in proxies.get("no", "").split(",")):
        if host == "*":
            return {}
        if not host:
            continue
        if "://" in host:
            mounts[host] = None
        elif host.replace(".", "").isdigit() or host.lower() == "localhost":
            mounts[f"all://{host}"] = None
        elif ":" in host:
            mounts[f"all://[{host}]"] = None
        else:
            mounts[f"all://*{host}"] = None
    return mounts
