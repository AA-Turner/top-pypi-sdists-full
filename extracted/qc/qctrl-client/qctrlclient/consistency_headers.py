from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypedDict

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from httpx import Request, Response


CONSISTENCY_TOKEN_HEADER = "x-authorization-consistency-token"  # noqa: S105


class TokenCache(Protocol):
    """Protocol for a cache storing consistency tokens for authorization clients."""

    def get(self) -> str | None:
        """Get the token from the cache."""

    def set(self, value: str) -> None:
        """Set the token in the cache."""


class SimpleTokenCache:
    """
    A simple in-memory token cache.

    This is not thread-safe and should only be used in single-threaded contexts.
    """

    def __init__(self) -> None:
        self._token: str | None = None

    def get(self) -> str | None:
        """Get the token from the cache."""
        return self._token

    def set(self, value: str) -> None:
        """Set the token in the cache."""
        self._token = value


class _HttpxEventHooks(TypedDict):
    request: list[Callable[[Request], None]]
    response: list[Callable[[Response], None]]


class _AsyncHttpxEventHooks(TypedDict):
    request: list[Callable[[Request], Awaitable[None]]]
    response: list[Callable[[Response], Awaitable[None]]]


class HttpxConsistencyHandler:
    """Handles propagation of consistency tokens via HTTP headers using httpx."""

    def __init__(self, token_cache: TokenCache) -> None:
        self._token_cache = token_cache

    def process_inbound(self, inbound: Response) -> None:
        """Process an inbound request/response and cache the consistency token."""
        if header_value := inbound.headers.get(CONSISTENCY_TOKEN_HEADER):
            self._token_cache.set(header_value)

    def prepare_outbound(self, outbound: Request) -> None:
        """Attach the cached consistency token to an outbound request/response."""
        if (token := self._token_cache.get()) is not None:
            outbound.headers[CONSISTENCY_TOKEN_HEADER] = token

    async def async_process_inbound(self, inbound: Response) -> None:
        """Process an inbound request/response and cache the consistency token."""
        return self.process_inbound(inbound)

    async def async_prepare_outbound(self, outbound: Request) -> None:
        """Attach the cached consistency token to an outbound request/response."""
        return self.prepare_outbound(outbound)

    def as_event_hooks(self) -> _HttpxEventHooks:
        """
        Return httpx event hooks for use with `httpx.Client`.

        The returned dict is compatible with the `event_hooks` parameter.
        """
        return {"request": [self.prepare_outbound], "response": [self.process_inbound]}

    def as_async_event_hooks(self) -> _AsyncHttpxEventHooks:
        """
        Return async httpx event hooks for use with `httpx.AsyncClient`.

        The returned dict is compatible with the `event_hooks` parameter.
        """
        return {
            "request": [self.async_prepare_outbound],
            "response": [self.async_process_inbound],
        }
