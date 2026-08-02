"""Hand-written SSE streaming clients for the agent run endpoints.

Never produced by openapi-generator (protected by ``.openapi-generator-ignore``).
Owns its own httpx client built from the shared ``Configuration``; parses SSE
frames into the generated per-product stream envelope and auto-reconnects on
transient network errors via ``GET {path}/{run_id}?starting_after=``.

The agent products share one base (``_BaseStream`` / ``_BaseAsyncStream``); each
subclass sets three class attributes:

* ``_PATH``         — the run route (``/v1/agent/retrieval/runs`` etc.)
* ``_ENVELOPE``     — the generated envelope whose ``from_json`` parses each frame
* ``_RESULT_EVENT`` — the terminal ``agent_result`` block type whose ``.data``
  is captured as ``.result``

  | product         | _PATH                    | _ENVELOPE                    | _RESULT_EVENT            |
  | --------------- | ------------------------ | ---------------------------- | ------------------------ |
  | retrieval agent | /v1/agent/retrieval/runs | RetrievalAgentStreamEnvelope | RetrievalAgentResultEvent|
  | answer agent    | /v1/agent/answer/runs    | AnswerAgentStreamEnvelope    | AnswerAgentResultEvent   |

Everything else (dispatch, reconnect, backoff, frame parsing, teardown) is
identical across products and lives in the base.
"""

from __future__ import annotations

import asyncio
import logging
import time
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from types import TracebackType
from typing import (
    Any,
    AsyncIterator,
    ClassVar,
    Iterator,
    Optional,
    Type,
    Union,
)
from typing_extensions import Self

import httpx
from httpx_sse import EventSource
from pydantic import ValidationError

from tako.aio.configuration import Configuration as AsyncConfiguration
from tako.aio.models.answer_agent_result_event import AnswerAgentResultEvent as AsyncAnswerAgentResultEvent
from tako.aio.models.answer_agent_stream_envelope import AnswerAgentStreamEnvelope as AsyncAnswerAgentStreamEnvelope
from tako.aio.models.retrieval_agent_result_event import RetrievalAgentResultEvent as AsyncRetrievalAgentResultEvent
from tako.aio.models.retrieval_agent_stream_envelope import (
    RetrievalAgentStreamEnvelope as AsyncRetrievalAgentStreamEnvelope,
)
from tako.configuration import Configuration
from tako.exceptions import ApiException
from tako.models.answer_agent_result_event import AnswerAgentResultEvent
from tako.models.answer_agent_stream_envelope import AnswerAgentStreamEnvelope
from tako.models.retrieval_agent_result_event import RetrievalAgentResultEvent
from tako.models.retrieval_agent_stream_envelope import RetrievalAgentStreamEnvelope

log = logging.getLogger("tako")

_RETRIABLE = (httpx.NetworkError, httpx.TimeoutException, httpx.RemoteProtocolError)
_TERMINAL_KIND = "stream_done"


def _base_url(config: Union[Configuration, AsyncConfiguration]) -> str:
    return config.host.rstrip("/")


def _headers(config: Union[Configuration, AsyncConfiguration]) -> dict[str, str]:
    headers: dict[str, str] = {"Accept": "text/event-stream", "Cache-Control": "no-store"}
    api_key = config.auth_settings().get("apiKey")
    if api_key is not None:
        value = api_key.get("value")
        if value:
            headers[api_key["key"]] = value
    return headers


def _backoff_seconds(attempt: int) -> float:
    """Exponential backoff (1-based attempt), capped at 10s."""
    return float(min(0.5 * (2 ** (attempt - 1)), 10.0))


class _BaseStream:
    """Auto-reconnecting SSE stream over an agent run. Iterates the per-product envelope.

    Dispatches the run eagerly (POST) on construction; the object holds an open
    connection, so use it as a context manager (or call ``close()``). Subclasses
    set ``_PATH`` / ``_ENVELOPE`` / ``_RESULT_EVENT`` (see the module docstring).
    """

    _PATH: ClassVar[str]
    _ENVELOPE: ClassVar[Type[Any]]
    _RESULT_EVENT: ClassVar[Type[Any]]

    def __init__(
        self,
        client: httpx.Client,
        *,
        config: Configuration,
        request: Any,
        max_retries: int = 5,
        read_timeout: float = 120.0,
    ) -> None:
        self._client = client
        self._config = config
        self._request = request
        self._max_retries = max_retries
        self._read_timeout = read_timeout
        self.run_id: Optional[str] = None
        self.last_seq: int = -1
        self.result: Optional[Any] = None
        self._cm: Optional[AbstractContextManager[httpx.Response]] = None
        self._source: Optional[EventSource] = None
        try:
            self._open("POST", _base_url(config) + self._PATH, body=request.to_json())
        except BaseException:
            self._client.close()
            raise

    def _open(
        self,
        method: str,
        url: str,
        *,
        body: Optional[str] = None,
        params: Optional[dict[str, str]] = None,
    ) -> None:
        headers = _headers(self._config)
        if body is not None:
            headers["Content-Type"] = "application/json"
        cm = self._client.stream(
            method, url, content=body, params=params, headers=headers, timeout=self._read_timeout
        )
        response = cm.__enter__()
        if response.status_code // 100 != 2:
            detail = response.read().decode(errors="replace")
            cm.__exit__(None, None, None)
            raise ApiException(status=response.status_code, reason=response.reason_phrase, body=detail)
        self._cm = cm
        self._source = EventSource(response)

    def _close_connection(self) -> None:
        if self._cm is not None:
            try:
                self._cm.__exit__(None, None, None)
            except Exception:  # best-effort teardown
                pass
            self._cm = None
            self._source = None

    def _reconnect(self) -> None:
        self._close_connection()
        params: Optional[dict[str, str]] = {"starting_after": str(self.last_seq)} if self.last_seq >= 0 else None
        self._open("GET", f"{_base_url(self._config)}{self._PATH}/{self.run_id}", params=params)

    def __iter__(self) -> Iterator[Any]:
        if self._source is None:
            raise RuntimeError("stream not open")
        retries = 0
        while True:
            try:
                for sse in self._source.iter_sse():
                    if not sse.data.strip():
                        continue
                    try:
                        maybe_envelope = self._ENVELOPE.from_json(sse.data)
                    except (ValueError, ValidationError):
                        # Forward-compat: skip frames this SDK version can't parse
                        # (e.g. a block kind added server-side after release).
                        log.debug("skipping unparseable SSE frame", exc_info=True)
                        continue
                    if maybe_envelope is None:
                        continue
                    envelope = maybe_envelope
                    self.run_id = envelope.run_id
                    self.last_seq = envelope.seq
                    retries = 0
                    block = envelope.block.actual_instance
                    if isinstance(block, self._RESULT_EVENT):
                        self.result = block.data
                    yield envelope
                    if block is not None and block.kind == _TERMINAL_KIND:
                        return
                # No terminal frame before the connection closed = an abnormal
                # mid-run close (LB idle-timeout, HTTP/2 GOAWAY as clean EOF).
                # The contract ends a stream with stream_done (or a terminal
                # error frame), so resume against last_seq within the retry
                # budget; end gracefully (caller can poll get()) if we can't.
                if self.run_id is None or retries >= self._max_retries:
                    return
                retries += 1
                delay = _backoff_seconds(retries)
                log.info(
                    "agent stream closed mid-run (run=%s seq=%d); reconnecting in %.1fs (attempt %d/%d)",
                    self.run_id, self.last_seq, delay, retries, self._max_retries,
                )
                time.sleep(delay)
                self._reconnect()
                continue
            except _RETRIABLE:
                if self.run_id is None or retries >= self._max_retries:
                    raise
                retries += 1
                delay = _backoff_seconds(retries)
                log.info(
                    "agent stream lost (run=%s seq=%d); reconnecting in %.1fs (attempt %d/%d)",
                    self.run_id, self.last_seq, delay, retries, self._max_retries,
                )
                time.sleep(delay)
                self._reconnect()

    def close(self) -> None:
        self._close_connection()
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.close()


class RetrievalAgentStream(_BaseStream):
    """SSE stream over a Retrieval Agent run (``/v1/agent/retrieval/runs``).

    ``result`` is a ``RetrievalAgentResult`` carrying ``structured_output*``.
    """

    _PATH = "/v1/agent/retrieval/runs"
    _ENVELOPE = RetrievalAgentStreamEnvelope
    _RESULT_EVENT = RetrievalAgentResultEvent


class AnswerAgentStream(_BaseStream):
    """SSE stream over an Answer Agent run (``/v1/agent/answer/runs``)."""

    _PATH = "/v1/agent/answer/runs"
    _ENVELOPE = AnswerAgentStreamEnvelope
    _RESULT_EVENT = AnswerAgentResultEvent


class _BaseAsyncStream:
    """Async auto-reconnecting SSE stream. Async-iterates the per-product envelope.

    Unlike the sync class it cannot dispatch in ``__init__`` (no await), so the
    initial POST happens in ``open()``, called by ``__aenter__`` (and by the
    resource ``stream`` factory before returning the stream).
    """

    _PATH: ClassVar[str]
    _ENVELOPE: ClassVar[Type[Any]]
    _RESULT_EVENT: ClassVar[Type[Any]]

    def __init__(
        self,
        client: httpx.AsyncClient,
        *,
        config: AsyncConfiguration,
        request: Any,
        max_retries: int = 5,
        read_timeout: float = 120.0,
    ) -> None:
        self._client = client
        self._config = config
        self._request = request
        self._max_retries = max_retries
        self._read_timeout = read_timeout
        self.run_id: Optional[str] = None
        self.last_seq: int = -1
        self.result: Optional[Any] = None
        self._cm: Optional[AbstractAsyncContextManager[httpx.Response]] = None
        self._source: Optional[EventSource] = None

    async def open(self) -> Self:
        try:
            await self._open("POST", _base_url(self._config) + self._PATH, body=self._request.to_json())
        except BaseException:
            await self._client.aclose()
            raise
        return self

    async def _open(self, method: str, url: str, *, body: Optional[str] = None, params: Optional[dict[str, str]] = None) -> None:
        headers = _headers(self._config)
        if body is not None:
            headers["Content-Type"] = "application/json"
        cm = self._client.stream(
            method, url, content=body, params=params, headers=headers, timeout=self._read_timeout
        )
        response = await cm.__aenter__()
        if response.status_code // 100 != 2:
            detail = (await response.aread()).decode(errors="replace")
            await cm.__aexit__(None, None, None)
            raise ApiException(status=response.status_code, reason=response.reason_phrase, body=detail)
        self._cm = cm
        self._source = EventSource(response)

    async def _close_connection(self) -> None:
        if self._cm is not None:
            try:
                await self._cm.__aexit__(None, None, None)
            except Exception:  # best-effort teardown
                pass
            self._cm = None
            self._source = None

    async def _reconnect(self) -> None:
        await self._close_connection()
        params: Optional[dict[str, str]] = {"starting_after": str(self.last_seq)} if self.last_seq >= 0 else None
        await self._open("GET", f"{_base_url(self._config)}{self._PATH}/{self.run_id}", params=params)

    async def __aiter__(self) -> AsyncIterator[Any]:
        if self._source is None:
            raise RuntimeError("stream not open")
        retries = 0
        while True:
            try:
                async for sse in self._source.aiter_sse():
                    if not sse.data.strip():
                        continue
                    try:
                        maybe_envelope = self._ENVELOPE.from_json(sse.data)
                    except (ValueError, ValidationError):
                        # Forward-compat: skip frames this SDK version can't parse
                        # (e.g. a block kind added server-side after release).
                        log.debug("skipping unparseable SSE frame", exc_info=True)
                        continue
                    if maybe_envelope is None:
                        continue
                    envelope = maybe_envelope
                    self.run_id = envelope.run_id
                    self.last_seq = envelope.seq
                    retries = 0
                    block = envelope.block.actual_instance
                    if isinstance(block, self._RESULT_EVENT):
                        self.result = block.data
                    yield envelope
                    if block is not None and block.kind == _TERMINAL_KIND:
                        return
                # No terminal frame before the connection closed = an abnormal
                # mid-run close (LB idle-timeout, HTTP/2 GOAWAY as clean EOF).
                # The contract ends a stream with stream_done (or a terminal
                # error frame), so resume against last_seq within the retry
                # budget; end gracefully (caller can poll get()) if we can't.
                if self.run_id is None or retries >= self._max_retries:
                    return
                retries += 1
                delay = _backoff_seconds(retries)
                log.info(
                    "agent stream closed mid-run (run=%s seq=%d); reconnecting in %.1fs (attempt %d/%d)",
                    self.run_id, self.last_seq, delay, retries, self._max_retries,
                )
                await asyncio.sleep(delay)
                await self._reconnect()
                continue
            except _RETRIABLE:
                if self.run_id is None or retries >= self._max_retries:
                    raise
                retries += 1
                delay = _backoff_seconds(retries)
                log.info(
                    "agent stream lost (run=%s seq=%d); reconnecting in %.1fs (attempt %d/%d)",
                    self.run_id, self.last_seq, delay, retries, self._max_retries,
                )
                await asyncio.sleep(delay)
                await self._reconnect()

    async def close(self) -> None:
        await self._close_connection()
        await self._client.aclose()

    async def __aenter__(self) -> Self:
        if self._source is None:
            await self.open()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.close()


class AsyncRetrievalAgentStream(_BaseAsyncStream):
    """Async SSE stream over a Retrieval Agent run (``/v1/agent/retrieval/runs``).

    ``result`` is a ``RetrievalAgentResult`` carrying ``structured_output*``.
    """

    _PATH = "/v1/agent/retrieval/runs"
    _ENVELOPE = AsyncRetrievalAgentStreamEnvelope
    _RESULT_EVENT = AsyncRetrievalAgentResultEvent


class AsyncAnswerAgentStream(_BaseAsyncStream):
    """Async SSE stream over an Answer Agent run (``/v1/agent/answer/runs``)."""

    _PATH = "/v1/agent/answer/runs"
    _ENVELOPE = AsyncAnswerAgentStreamEnvelope
    _RESULT_EVENT = AsyncAnswerAgentResultEvent
