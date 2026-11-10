"""StreamsMixin: a held GET (the live channel's SSE stream), sent the way this transport sends everything (an SDK
process's through the Probe service), and the headers and typed errors an async caller (the MCP `events` tool)
reuses for a request it sends itself."""

from __future__ import annotations

import contextlib
import socket
from collections.abc import Iterator, Mapping
from typing import Any

import httpx

from ....foundation.request_identity.request_identity import current_client_headers
from .relay import CUT_EXTENSION, STREAM_EXTENSION

#: A held stream's connect budget; reads wait `read_timeout` (the live server sends a keepalive every 15 s).
STREAM_CONNECT_SECONDS = 5.0


class StreamsMixin:
    """Part of Transport: its methods run with `self` the Transport; fold_parts() copies them into Transport."""

    def make_headers(self, method: str, path: str) -> dict[str, str]:
        """The headers `request()` sends for a bodyless call: identity, auth, workspace limit, surface, tool."""
        from .transport import need_api_path  # defined below the parts transport.py folds in

        need_api_path(path)
        override = current_client_headers()
        identity = self._client_headers if override is None else override
        return self._build_headers(
            method, path, b"", has_json=False, content=None, content_headers=None, extra_headers=None,
            override=override, client_identity=identity,
        )

    def check_answer(self, response: httpx.Response) -> None:
        """Raise the typed error `request()` raises for a refused answer (the body must be read)."""
        if response.status_code >= 400:
            raise self._to_error(response)

    @contextlib.contextmanager
    def open_stream(
        self,
        path: str,
        *,
        read_timeout: float,
        parameters: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Iterator[httpx.Response]:
        """A held GET, sent as this transport sends every request: an SDK process's goes through the Probe
        service, which holds the response and passes its body on as it comes (`relay.STREAM_EXTENSION`; the
        CLI's and the MCP's go from their own process, as all their requests do). Yields the open response; a
        refused one raises its typed error."""
        sent = {**self.make_headers("GET", path), **(headers or {})}
        timeout = httpx.Timeout(read_timeout, connect=STREAM_CONNECT_SECONDS)
        with self._client.stream("GET", path, params=dict(parameters or {}), headers=sent, timeout=timeout,
                                 extensions={STREAM_EXTENSION: True}) as response:
            if response.status_code >= 400:
                response.read()
                raise self._to_error(response)
            yield response


def cut_stream(response: httpx.Response) -> None:
    """Wake a thread blocked reading `response` (another thread's `close()`): a relayed stream ends through its
    own hook (`SocketBody.cut`), any other has its socket shut down; the reader sees the end and closes it
    itself. Closing the socket alone does not wake a blocked read."""
    cut = response.extensions.get(CUT_EXTENSION)
    if callable(cut):
        cut()
        return
    stream = response.extensions.get("network_stream")
    sock = stream.get_extra_info("socket") if stream is not None else None
    if sock is None:
        with contextlib.suppress(Exception):
            response.close()
        return
    with contextlib.suppress(OSError):
        sock.shutdown(socket.SHUT_RDWR)

