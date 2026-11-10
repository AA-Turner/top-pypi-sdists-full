"""RelayTransport (an httpx transport): a training process's HTTP goes through the Probe service
(`api.call`, plan D10). Everything the SDK builds here (headers, auth, the body) is packaged and sent
there; the answer comes back as an httpx.Response, so retries and error mapping stay `Transport`'s.
`pick_http_transport` decides once per process: the relay for the SDK, httpx's own under a service."""

from __future__ import annotations

import base64
import contextlib
import os
import select
import socket
import tempfile
import threading
import time
from collections.abc import Iterator

import httpx

#: On a request whose body is a file range: `(fd, offset, length)`. The relay passes the open file
#: (the service reads it with `pread`) instead of reading it here (`blobs.py`).
FILE_BODY_EXTENSION = "probe.file_body"
#: On a download (`blobs.get_url`, `download_to`): its byte budget (0: none). It rides the bulk
#: lane, and the relay stops a body past the budget (H3).
DOWNLOAD_EXTENSION = "probe.download"
#: On a download to a file (`download_to`): the destination's folder. A body past the inline size
#: is written into a temp file there (M-3), named on the response (`SINK_PATH_EXTENSION`), so the
#: caller renames it into place instead of copying it.
SINK_DIR_EXTENSION = "probe.sink_dir"
SINK_PATH_EXTENSION = "probe.sink_path"
#: A body up to this size rides in the request; a bigger one in an unlinked temp file's fd.
INLINE_BYTES = 512 * 1024
#: How long the answer may stay silent past the request's own timeouts (the service sends
#: `api.progress` while a body streams, so a long download is never cut by this).
MARGIN_S = 5.0
#: A file body's slowest upload this allows before giving up on the answer (bytes a second).
SLOWEST_UPLOAD_BPS = 256 * 1024
#: On a GET read as it comes (the live events' SSE, `Transport.open_stream`): the service holds the response
#: and writes its body into a socket this process reads (`api.call` with `stream: true`).
STREAM_EXTENSION = "probe.stream"
#: On a held stream's response: ends it from any thread (`SocketBody.cut`, `streams.cut_stream`).
CUT_EXTENSION = "probe.cut"
#: Test-only: "off" sends every request from this process (the suite's fakes stand in for HTTP).
RELAY_ENV = "PROBE_API_RELAY"
#: The network settings a relayed request carries (the service sends through them, not its own).
NETWORK_NAMES = ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "NO_PROXY", "SSL_CERT_FILE", "SSL_CERT_DIR",
                 "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE")


class RelayTransport(httpx.BaseTransport):
    """httpx's transport interface over `api.call`. No service, or a request it never sent:
    `httpx.ConnectError` (replayable); an answer that broke off or made no sense: `httpx.ReadError`
    / `httpx.RemoteProtocolError`."""

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        from probe.foundation.service_api import handoff
        from probe.foundation.service_api.service_api import ServiceError
        from probe.foundation.service_api.wire import Method

        handoff.hold_open()  # the service stays up while this process sends through it
        if request.extensions.get(STREAM_EXTENSION):
            return _open_stream(request)
        sink = _open_sink(request)  # the answer's body past INLINE_BYTES: this process's own file
        try:
            parameters, fds, closer, body_length = _pack_request(request, sink)
            try:
                answer = handoff.request(Method.API_CALL, parameters, timeout=_answer_timeout(request, body_length),
                                         fds=fds)
            except (handoff.ServiceUnavailable, ServiceError) as exc:
                raise httpx.ConnectError(f"the Probe service did not send it: {exc}", request=request) from exc
            except (OSError, ValueError) as exc:
                raise httpx.ReadError(f"the Probe service's answer broke off: {exc!r}", request=request) from exc
            finally:
                closer()
            response = _to_response(answer, request, sink)
        except BaseException:
            _discard_sink(sink)
            raise
        return response


def _open_stream(request: httpx.Request) -> httpx.Response:
    """A held GET through the service: it answers at the response's headers, then writes the body into the
    socket passed with the call; the response reads it (`SocketBody`)."""
    from probe.foundation.service_api import handoff
    from probe.foundation.service_api.service_api import ServiceError
    from probe.foundation.service_api.wire import Method

    ours, theirs = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        parameters = {
            "method": request.method, "url": str(request.url), "stream": True, "body_sink": {"index": 0},
            "headers": [[name, value] for name, value in request.headers.multi_items()],
            "timeout": {k: v for k, v in (request.extensions.get("timeout") or {}).items() if v is not None},
        }
        env = get_network_env()
        if env:
            parameters["env"] = env
        try:
            answer = handoff.request(Method.API_CALL, parameters, timeout=_answer_timeout(request, 0),
                                     fds=[theirs.fileno()])
        except (handoff.ServiceUnavailable, ServiceError) as exc:
            raise httpx.ConnectError(f"the Probe service did not open the stream: {exc}", request=request) from exc
        except (OSError, ValueError) as exc:
            raise httpx.ReadError(f"the Probe service's answer broke off: {exc!r}", request=request) from exc
    except BaseException:
        ours.close()
        raise
    finally:
        theirs.close()  # the service holds its own copy
    if not (isinstance(answer, dict) and answer.get("streaming") is True):
        ours.close()
        return _to_response(answer, request, None)
    try:
        status = int(answer["status"])
        headers = [(str(name), str(value)) for name, value in answer.get("headers") or []]
    except (KeyError, TypeError, ValueError) as exc:
        ours.close()
        raise httpx.RemoteProtocolError(f"the Probe service's answer made no sense: {exc!r}", request=request) from exc
    body = SocketBody(ours, (request.extensions.get("timeout") or {}).get("read"))
    return httpx.Response(status, headers=headers, request=request, stream=body, extensions={CUT_EXTENSION: body.cut})


class SocketBody(httpx.SyncByteStream):
    """A held stream's body: what the service writes into this end of the socket pair, as it comes. Silence past
    the read timeout is `httpx.ReadTimeout`. `cut()` (any thread) and `close()` shut the socket itself down, so
    the reader wakes and the service's next write fails, even while a forked child (a DataLoader worker) still
    holds a copy; a child's own close shuts nothing. `poll`, never `select`: the fd may be past 1023."""

    def __init__(self, sock: socket.socket, read_timeout: float | None) -> None:
        self.sock = sock
        self.read_timeout = read_timeout
        self._pid = os.getpid()
        self._is_closed = False
        self._lock = threading.Lock()

    def __iter__(self) -> Iterator[bytes]:
        poller = select.poll()
        poller.register(self.sock.fileno(), select.POLLIN)
        wait_ms = None if self.read_timeout is None else self.read_timeout * 1000
        while not self._is_closed:
            if not poller.poll(wait_ms):
                raise httpx.ReadTimeout("the Probe service sent nothing for the read timeout")
            try:
                chunk = self.sock.recv(64 * 1024)
            except OSError:
                return
            if not chunk:
                return
            yield chunk

    def cut(self) -> None:
        """End the stream from any thread: the reader wakes, the service stops."""
        with self._lock:
            if not self._is_closed and os.getpid() == self._pid:
                with contextlib.suppress(OSError):
                    self.sock.shutdown(socket.SHUT_RDWR)

    def close(self) -> None:
        with self._lock:
            if self._is_closed:
                return
            self._is_closed = True
            if os.getpid() == self._pid:
                with contextlib.suppress(OSError):
                    self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()


def _open_sink(request: httpx.Request):
    """Where a big answer's body goes: a temp file in the destination's folder for a download to a
    file (renamed into place after), else an unlinked one."""
    folder = request.extensions.get(SINK_DIR_EXTENSION)
    if folder:
        return tempfile.NamedTemporaryFile(dir=folder, prefix=".probe-download-", delete=False)
    return tempfile.TemporaryFile()


def _discard_sink(sink) -> None:
    with contextlib.suppress(OSError):
        sink.close()
    name = getattr(sink, "name", None)
    if isinstance(name, str):
        with contextlib.suppress(OSError):
            os.unlink(name)


def _pack_request(request: httpx.Request, sink):
    """`api.call`'s parameters, its fds (a file body, then the sink), what closes what this
    opened, and the body's length."""
    parameters: dict = {
        "method": request.method,
        "url": str(request.url),
        "headers": [[name, value] for name, value in request.headers.multi_items()],
        "timeout": {k: v for k, v in (request.extensions.get("timeout") or {}).items() if v is not None},
    }
    deadline = _get_deadline_s()
    if deadline is not None:
        parameters["deadline"] = deadline
    env = get_network_env()
    if env:
        parameters["env"] = env
    download = request.extensions.get(DOWNLOAD_EXTENSION)
    if download is not None:
        parameters["lane"] = "bulk"
        if download:
            parameters["max_bytes"] = int(download)
    fds: list[int] = []
    closer = lambda: None  # noqa: E731
    file_body = request.extensions.get(FILE_BODY_EXTENSION)
    if file_body is not None:
        fd, offset, length = file_body
        parameters["body_fd"] = {"index": 0, "offset": int(offset), "length": int(length)}
        fds.append(fd)
        body_length = int(length)
    else:
        body = request.read()
        body_length = len(body)
        if len(body) <= INLINE_BYTES:
            if body:
                parameters["body"] = base64.b64encode(body).decode("ascii")
        else:
            spill = tempfile.TemporaryFile()  # unlinked: only the fd crosses
            spill.write(body)
            spill.flush()
            parameters["body_fd"] = {"index": 0, "offset": 0, "length": len(body)}
            parameters["lane"] = "bulk"
            fds.append(spill.fileno())
            closer = spill.close
    parameters["body_sink"] = {"index": len(fds)}
    fds.append(sink.fileno())
    return parameters, fds, closer, body_length


def _get_deadline_s() -> float | None:
    """Seconds left of the caller's deadline scope (`deadlines.deadline_scope`), if one is open: a
    call still queued in the service past it never goes out (M3)."""
    from .deadlines import _request_deadline

    deadline = _request_deadline.get()
    return None if deadline is None else max(0.0, deadline - time.monotonic())


def _answer_timeout(request: httpx.Request, body_length: int) -> float:
    """How long the answer may be silent: the request's own timeouts, a margin, and the upload."""
    parts = request.extensions.get("timeout") or {}
    total = sum(float(v) if v is not None else 300.0 for v in (parts.get(k) for k in ("connect", "read", "write", "pool")))
    return total + MARGIN_S + body_length / SLOWEST_UPLOAD_BPS


def _to_response(answer: object, request: httpx.Request, sink) -> httpx.Response:
    """The answer as httpx's Response: its body inline, or the sink the service wrote it into (L3:
    an answer that makes no sense is the httpx error of a broken response)."""
    if not isinstance(answer, dict):
        raise httpx.RemoteProtocolError("the Probe service answered no response", request=request)
    failed = answer.get("failed")
    if failed is not None:
        raise _to_httpx_error(str(failed), str(answer.get("message") or ""), request)
    if sink is None and answer.get("body_in_sink") is not None:
        raise httpx.RemoteProtocolError("the Probe service wrote a body nowhere it was asked to", request=request)
    try:
        status = int(answer["status"])
        headers = [(str(name), str(value)) for name, value in answer.get("headers") or []]
        extensions = {"http_version": str(answer.get("http_version") or "HTTP/1.1").encode("ascii", "replace")}
        if answer.get("body_in_sink") is not None:
            size = int(answer["body_in_sink"])
            sink.seek(0)
            headers.append(("content-length", str(size)))
            name = getattr(sink, "name", None)
            if isinstance(name, str):
                extensions[SINK_PATH_EXTENSION] = name
            return httpx.Response(status, headers=headers, stream=_SinkBody(sink, size), request=request,
                                  extensions=extensions)
        if sink is not None:
            _discard_sink(sink)
        raw = base64.b64decode(answer.get("body") or "", validate=True)
        return httpx.Response(status, headers=headers, stream=httpx.ByteStream(raw), request=request,
                              extensions=extensions)
    except (KeyError, TypeError, ValueError) as exc:
        raise httpx.RemoteProtocolError(f"the Probe service's answer made no sense: {exc!r}", request=request) from exc


def _to_httpx_error(kind: str, message: str, request: httpx.Request) -> httpx.HTTPError:
    """The httpx error a direct request would have raised; a body over its budget is `download_to`'s
    own ValueError."""
    from probe.foundation.service_api.vocabularies import RelayFailure

    if kind in (RelayFailure.CONNECT, RelayFailure.REFUSED):
        return httpx.ConnectError(message, request=request)
    if kind == RelayFailure.EXPIRED:
        return httpx.PoolTimeout(message, request=request)  # never sent: replayable
    if kind == RelayFailure.TIMEOUT:
        return httpx.ReadTimeout(message, request=request)
    if kind == RelayFailure.PROTOCOL:
        return httpx.RemoteProtocolError(message, request=request)
    if kind == RelayFailure.TOO_LARGE:
        raise ValueError("artifact download exceeds its byte budget")  # as `download_to` says it
    return httpx.ReadError(message, request=request)


class _SinkBody(httpx.SyncByteStream):
    """A response body the service wrote into this process's unlinked temp file."""

    def __init__(self, sink, size: int) -> None:
        self.sink = sink
        self.size = size

    def __iter__(self) -> Iterator[bytes]:
        left = self.size
        while left > 0:
            chunk = self.sink.read(min(1 << 20, left))
            if not chunk:
                break
            left -= len(chunk)
            yield chunk

    def close(self) -> None:
        _discard_sink(self.sink)  # a temp file in the destination's folder not renamed into place goes


def get_network_env() -> dict:
    """This process's proxy and CA settings, either case (`NETWORK_NAMES`)."""
    import os

    wanted = {name.upper() for name in NETWORK_NAMES}
    return {name: value for name, value in os.environ.items() if value and name.upper() in wanted}


def pick_http_transport(surface: str) -> httpx.BaseTransport | None:
    """The httpx transport a default `Transport` sends with: the relay for the SDK outside a
    service (plan D10); None (httpx's own) under a service, for the CLI and MCP surfaces (the
    CLI's commands move under the service, plan A2), and where `PROBE_API_RELAY=off` (tests)."""
    import os

    from probe.foundation.request_identity.surface import Surface
    from probe.foundation.service_api.handoff import is_under_service

    if surface != Surface.SDK.value or is_under_service() or os.environ.get(RELAY_ENV, "").lower() == "off":
        return None
    return RelayTransport()
