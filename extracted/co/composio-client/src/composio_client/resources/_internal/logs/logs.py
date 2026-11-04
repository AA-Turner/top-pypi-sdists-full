# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.logs`` — the generated resource classes.

``LogsResource`` (sync) and ``AsyncLogsResource`` (async),
holding the sub-resources below.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ..._base import AsyncAPIResource, SyncAPIResource
from .tools import AsyncToolsResource, ToolsResource
from .triggers import AsyncTriggersResource, TriggersResource

if TYPE_CHECKING:
    from ...._base_client import AsyncAPIClient, SyncAPIClient


class LogsResource(SyncAPIResource):
    triggers: TriggersResource
    tools: ToolsResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.triggers = TriggersResource(client)
        self.tools = ToolsResource(client)

    @cached_property
    def with_raw_response(self) -> LogsResourceWithRawResponse:
        return LogsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LogsResourceWithStreamingResponse:
        return LogsResourceWithStreamingResponse(self)


class AsyncLogsResource(AsyncAPIResource):
    triggers: AsyncTriggersResource
    tools: AsyncToolsResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.triggers = AsyncTriggersResource(client)
        self.tools = AsyncToolsResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncLogsResourceWithRawResponse:
        return AsyncLogsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLogsResourceWithStreamingResponse:
        return AsyncLogsResourceWithStreamingResponse(self)


class LogsResourceWithRawResponse:
    def __init__(self, resource: LogsResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncLogsResourceWithRawResponse:
    def __init__(self, resource: AsyncLogsResource) -> None:
        self._resource = resource
        self._client = resource._client


class LogsResourceWithStreamingResponse:
    def __init__(self, resource: LogsResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncLogsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncLogsResource) -> None:
        self._resource = resource
        self._client = resource._client
