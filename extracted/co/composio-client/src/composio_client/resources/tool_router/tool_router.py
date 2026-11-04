# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.tool_router`` — the generated resource classes.

``ToolRouterResource`` (sync) and ``AsyncToolRouterResource`` (async),
holding the sub-resources below.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from .._base import AsyncAPIResource, SyncAPIResource
from .session.session import AsyncSessionResource, SessionResource

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient


class ToolRouterResource(SyncAPIResource):
    session: SessionResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.session = SessionResource(client)

    @cached_property
    def with_raw_response(self) -> ToolRouterResourceWithRawResponse:
        return ToolRouterResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ToolRouterResourceWithStreamingResponse:
        return ToolRouterResourceWithStreamingResponse(self)


class AsyncToolRouterResource(AsyncAPIResource):
    session: AsyncSessionResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.session = AsyncSessionResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncToolRouterResourceWithRawResponse:
        return AsyncToolRouterResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncToolRouterResourceWithStreamingResponse:
        return AsyncToolRouterResourceWithStreamingResponse(self)


class ToolRouterResourceWithRawResponse:
    def __init__(self, resource: ToolRouterResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncToolRouterResourceWithRawResponse:
    def __init__(self, resource: AsyncToolRouterResource) -> None:
        self._resource = resource
        self._client = resource._client


class ToolRouterResourceWithStreamingResponse:
    def __init__(self, resource: ToolRouterResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncToolRouterResourceWithStreamingResponse:
    def __init__(self, resource: AsyncToolRouterResource) -> None:
        self._resource = resource
        self._client = resource._client
