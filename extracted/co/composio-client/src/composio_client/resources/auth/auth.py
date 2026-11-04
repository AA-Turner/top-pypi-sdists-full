# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.auth`` — the generated resource classes.

``AuthResource`` (sync) and ``AsyncAuthResource`` (async),
holding the sub-resources below.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from .._base import AsyncAPIResource, SyncAPIResource
from .session import AsyncSessionResource, SessionResource

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient


class AuthResource(SyncAPIResource):
    session: SessionResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.session = SessionResource(client)

    @cached_property
    def with_raw_response(self) -> AuthResourceWithRawResponse:
        return AuthResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AuthResourceWithStreamingResponse:
        return AuthResourceWithStreamingResponse(self)


class AsyncAuthResource(AsyncAPIResource):
    session: AsyncSessionResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.session = AsyncSessionResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncAuthResourceWithRawResponse:
        return AsyncAuthResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAuthResourceWithStreamingResponse:
        return AsyncAuthResourceWithStreamingResponse(self)


class AuthResourceWithRawResponse:
    def __init__(self, resource: AuthResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncAuthResourceWithRawResponse:
    def __init__(self, resource: AsyncAuthResource) -> None:
        self._resource = resource
        self._client = resource._client


class AuthResourceWithStreamingResponse:
    def __init__(self, resource: AuthResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncAuthResourceWithStreamingResponse:
    def __init__(self, resource: AsyncAuthResource) -> None:
        self._resource = resource
        self._client = resource._client
