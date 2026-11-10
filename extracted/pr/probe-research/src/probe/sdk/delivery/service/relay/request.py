"""ApiCall: one `api.call` request (plan D10), checked: the HTTP request a training process packaged
(method, absolute URL, headers, a body inline or in a passed file), its timeouts and its network
settings. The wire shape is in DESIGN.md beside this file."""

from __future__ import annotations

import base64
import binascii
import os
import stat
import time
from dataclasses import dataclass, field

from probe.foundation.service_api.env import MAX_HOOK_ENV, MAX_HOOK_ENV_VALUE, runtime_env_name
from probe.foundation.service_api.wire import invalid_params

METHODS = frozenset({"GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"})
#: Headers a hop does not pass on (RFC 9110 7.6.1): the relay's own connection says them.
HOP_HEADERS = frozenset({"connection", "keep-alive", "proxy-connection", "te", "trailer", "transfer-encoding", "upgrade"})
MAX_HEADERS = 128
MAX_URL = 16 * 1024
#: Each timeout part, at most (seconds).
MAX_TIMEOUT_S = 3600.0
#: A call's `deadline` (seconds from its arrival), at most.
MAX_DEADLINE_S = 24 * 3600.0
#: `lane`: small calls (heartbeats, closes, metadata) never wait behind bulk ones (part uploads,
#: downloads), M3.
LANES = frozenset({"small", "bulk"})
#: The network settings a call may name: proxies and CAs, by `runtime_env_name`.
NETWORK_PREFIXES = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "SSL_", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE")


@dataclass
class FileBody:
    """A body read from a passed file: `length` bytes from `offset`, never moving its offset."""

    fd: int
    offset: int
    length: int


@dataclass
class ApiCall:
    method: str
    url: str
    headers: list[tuple[str, str]]
    body: bytes | None = None
    file_body: FileBody | None = None
    timeout: dict = field(default_factory=dict)
    env: dict = field(default_factory=dict)
    #: A passed fd the answer's body is written into past the inline size (H3): the caller's.
    sink_fd: int | None = None
    #: Stop a body past this many bytes (`download_to`'s budget), None: no limit.
    max_bytes: int | None = None
    lane: str = "small"
    #: Monotonic: a call still queued past it never goes out (`expired`).
    expires_at: float | None = None
    #: The caller may be in a sandbox (plan D25): it may reach only the API and its storage.
    is_fenced: bool = False
    #: A held stream (`stream: true`, the live events' SSE): answered at its headers, its body written into
    #: the passed socket (`sink_fd`) as it comes, on the held streams' own threads (`streams.py`).
    is_stream: bool = False
    #: The calling process (its pid, from the connection): a held stream's budget is also per caller.
    caller_pid: int | None = None
    #: The fds this call holds (closed when it is done).
    fds: list[int] = field(default_factory=list)

    def close(self) -> None:
        for fd in self.fds:
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds = []


def need_api_call(parameters: dict, fds: list[int]) -> ApiCall:
    """`api.call`'s parameters, checked; the call owns `fds` from here (closed on a refusal too)."""
    try:
        return _parse(parameters, fds)
    except BaseException:
        for fd in fds:
            try:
                os.close(fd)
            except OSError:
                pass
        raise


def _parse(parameters: dict, fds: list[int]) -> ApiCall:
    method = parameters.get("method")
    if method not in METHODS:
        raise invalid_params(f"method must be one of {sorted(METHODS)}")
    url = parameters.get("url")
    if not isinstance(url, str) or len(url) > MAX_URL or not url.startswith(("https://", "http://")):
        raise invalid_params("url must be an absolute http(s) URL")
    headers = parameters.get("headers", [])
    if not isinstance(headers, list) or len(headers) > MAX_HEADERS or not all(
        isinstance(h, list) and len(h) == 2 and all(isinstance(x, str) and "\n" not in x and "\r" not in x for x in h)
        for h in headers
    ):
        raise invalid_params(f"headers must be a list of at most {MAX_HEADERS} [name, value] strings")
    call = ApiCall(method=method, url=url, headers=[(n, v) for n, v in headers if n.lower() not in HOP_HEADERS])
    call.fds = list(fds)
    stream = parameters.get("stream")
    if stream is not None and stream is not True:
        raise invalid_params("stream must be true or left out")
    call.is_stream = stream is True
    if parameters.get("body") is not None:
        try:
            call.body = base64.b64decode(parameters["body"], validate=True)
        except (binascii.Error, TypeError, ValueError):
            raise invalid_params("body must be base64") from None
    body_fd = parameters.get("body_fd")
    if body_fd is not None:
        call.file_body = _need_file_body(body_fd, call.fds)
    if call.body is not None and call.file_body is not None:
        raise invalid_params("pass body or body_fd, not both")
    sink = parameters.get("body_sink")
    if sink is not None:
        call.sink_fd = _need_sink(sink, call.fds, is_stream=call.is_stream)
    max_bytes = parameters.get("max_bytes")
    if max_bytes is not None:
        if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes < 0:
            raise invalid_params("max_bytes must be a count of bytes")
        call.max_bytes = max_bytes
    lane = parameters.get("lane", "bulk" if call.file_body is not None else "small")
    if lane not in LANES:
        raise invalid_params(f"lane must be one of {sorted(LANES)}")
    call.lane = "bulk" if call.file_body is not None else lane
    if call.is_stream:
        if method != "GET" or call.body is not None or call.file_body is not None or call.sink_fd is None:
            raise invalid_params("a stream is a GET with no body, read from a passed socket (body_sink)")
        if call.max_bytes is not None:
            raise invalid_params("a stream has no max_bytes")
    deadline = parameters.get("deadline")
    if deadline is not None:
        if not isinstance(deadline, (int, float)) or isinstance(deadline, bool) or not 0 <= deadline <= MAX_DEADLINE_S:
            raise invalid_params("deadline must be seconds from now")
        call.expires_at = time.monotonic() + float(deadline)
    call.timeout = _need_timeout(parameters.get("timeout") or {})
    call.env = _need_network_env(parameters.get("env") or {})
    return call


def _need_file_body(value: object, fds: list[int]) -> FileBody:
    if not isinstance(value, dict):
        raise invalid_params("body_fd must be {index, offset, length}")
    index, offset, length = value.get("index"), value.get("offset"), value.get("length")
    numbers = (index, offset, length)
    if not all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in numbers) or index >= len(fds):
        raise invalid_params("body_fd needs an index of a passed fd, an offset and a length")
    try:
        if not stat.S_ISREG(os.fstat(fds[index]).st_mode):
            raise invalid_params("body_fd must be a regular file")
    except OSError:
        raise invalid_params("body_fd is not an open file") from None
    return FileBody(fds[index], offset, length)


def _need_sink(value: object, fds: list[int], *, is_stream: bool) -> int:
    """A passed fd open for writing: a regular file, or for a stream a socket (written by its own thread, never
    a lane's, so a reader that stops blocks only its own stream; the caller's shutdown reaches it even when a
    forked child still holds a copy)."""
    index = value.get("index") if isinstance(value, dict) else None
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(fds):
        raise invalid_params("body_sink needs the index of a passed fd")
    is_right_kind = stat.S_ISSOCK if is_stream else stat.S_ISREG
    try:
        if not is_right_kind(os.fstat(fds[index]).st_mode):
            raise invalid_params("a stream's body_sink must be a socket" if is_stream
                                 else "body_sink must be a regular file")
    except OSError:
        raise invalid_params("body_sink is not an open file") from None
    return fds[index]


def _need_timeout(value: object) -> dict:
    if not isinstance(value, dict):
        raise invalid_params("timeout must be {connect, read, write, pool}")
    out = {}
    for name in ("connect", "read", "write", "pool"):
        part = value.get(name)
        if part is None:
            continue
        if not isinstance(part, (int, float)) or isinstance(part, bool) or not 0 < part <= MAX_TIMEOUT_S:
            raise invalid_params(f"timeout.{name} must be seconds, at most {MAX_TIMEOUT_S:.0f}")
        out[name] = float(part)
    return out


def _need_network_env(value: object) -> dict:
    if not isinstance(value, dict) or len(value) > MAX_HOOK_ENV:
        raise invalid_params(f"env must be an object of at most {MAX_HOOK_ENV} variables")
    env = {}
    for name, item in value.items():
        if not isinstance(name, str) or not runtime_env_name(name) or not name.upper().startswith(NETWORK_PREFIXES):
            raise invalid_params(f"env may name only proxies and CAs, not {name!r}")
        if not isinstance(item, str) or len(item) > MAX_HOOK_ENV_VALUE or "\0" in item:
            raise invalid_params(f"env.{name} must be a string of at most {MAX_HOOK_ENV_VALUE} characters")
        env[name] = item
    return env
