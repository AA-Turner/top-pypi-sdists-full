"""Lazy response objects used by raw and streaming resource wrappers."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Any, Generic, TypeVar, cast

import httpx

ResponseT = TypeVar("ResponseT")
OtherT = TypeVar("OtherT")


class APIResponse(Generic[ResponseT]):
    """An HTTP response whose typed body is parsed on demand."""

    def __init__(
        self,
        *,
        raw: httpx.Response,
        cast_to: type[ResponseT] | None,
        client: Any,
        stream: bool,
        stream_cls: type[Any] | None,
        options: object,
        retries_taken: int = 0,
    ) -> None:
        self.http_response = raw
        self.http_request = raw.request
        self.status_code = raw.status_code
        self.headers = raw.headers
        self._cast_to = cast_to
        self._client = client
        self._stream = stream
        self._stream_cls = stream_cls
        self._options = options
        self.retries_taken = retries_taken
        self._parsed: object = _UNPARSED

    @property
    def is_closed(self) -> bool:
        return self.http_response.is_closed

    def read(self) -> bytes:
        return self.http_response.read()

    def json(self) -> object:
        self.read()
        return self.http_response.json()

    def parse(self, *, to: type[OtherT] | None = None) -> ResponseT | OtherT:
        target: type[Any] | None = to if to is not None else self._cast_to
        if to is None and self._parsed is not _UNPARSED:
            return cast(ResponseT, self._parsed)
        if not self.http_response.is_stream_consumed:
            self.http_response.read()
        parsed = self._client._parse_response(self.http_response, target)
        if to is None:
            self._parsed = parsed
        return cast(ResponseT | OtherT, parsed)

    def close(self) -> None:
        self.http_response.close()


class AsyncAPIResponse(Generic[ResponseT]):
    """Async HTTP response with awaitable read, parse, and close methods."""

    def __init__(
        self,
        *,
        raw: httpx.Response,
        cast_to: type[ResponseT] | None,
        client: Any,
        stream: bool,
        stream_cls: type[Any] | None,
        options: object,
        retries_taken: int = 0,
    ) -> None:
        self.http_response = raw
        self.http_request = raw.request
        self.status_code = raw.status_code
        self.headers = raw.headers
        self._cast_to = cast_to
        self._client = client
        self._stream = stream
        self._stream_cls = stream_cls
        self._options = options
        self.retries_taken = retries_taken
        self._parsed: object = _UNPARSED

    @property
    def is_closed(self) -> bool:
        return self.http_response.is_closed

    async def read(self) -> bytes:
        return await self.http_response.aread()

    async def json(self) -> object:
        await self.read()
        return self.http_response.json()

    async def parse(self, *, to: type[OtherT] | None = None) -> ResponseT | OtherT:
        target: type[Any] | None = to if to is not None else self._cast_to
        if to is None and self._parsed is not _UNPARSED:
            return cast(ResponseT, self._parsed)
        if not self.http_response.is_stream_consumed:
            await self.http_response.aread()
        parsed = self._client._parse_response(self.http_response, target)
        if to is None:
            self._parsed = parsed
        return cast(ResponseT | OtherT, parsed)

    async def close(self) -> None:
        await self.http_response.aclose()


APIResponseT = TypeVar("APIResponseT", bound=APIResponse[Any])


class ResponseContextManager(Generic[APIResponseT]):
    def __init__(self, request_func: Callable[[], APIResponseT]) -> None:
        self._request_func = request_func
        self._response: APIResponseT | None = None

    def __enter__(self) -> APIResponseT:
        response = self._request_func()
        self._response = response
        return response

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._response is not None:
            self._response.close()


AsyncAPIResponseT = TypeVar("AsyncAPIResponseT", bound=AsyncAPIResponse[Any])


class AsyncResponseContextManager(Generic[AsyncAPIResponseT]):
    def __init__(self, api_request: Awaitable[AsyncAPIResponseT]) -> None:
        self._api_request = api_request
        self._response: AsyncAPIResponseT | None = None

    async def __aenter__(self) -> AsyncAPIResponseT:
        response = await self._api_request
        self._response = response
        return response

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._response is not None:
            await self._response.close()


_UNPARSED = object()
