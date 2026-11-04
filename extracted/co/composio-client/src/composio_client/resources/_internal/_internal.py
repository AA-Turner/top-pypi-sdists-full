# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal`` — the generated resource classes.

``InternalResource`` (sync) and ``AsyncInternalResource`` (async),
holding the sub-resources below.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from .._base import AsyncAPIResource, SyncAPIResource
from .cli.cli import AsyncCliResource, CliResource
from .consumer.consumer import AsyncConsumerResource, ConsumerResource
from .logs.logs import AsyncLogsResource, LogsResource
from .org.org import AsyncOrgResource, OrgResource

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient


class InternalResource(SyncAPIResource):
    cli: CliResource
    consumer: ConsumerResource
    logs: LogsResource
    org: OrgResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.cli = CliResource(client)
        self.consumer = ConsumerResource(client)
        self.logs = LogsResource(client)
        self.org = OrgResource(client)

    @cached_property
    def with_raw_response(self) -> InternalResourceWithRawResponse:
        return InternalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InternalResourceWithStreamingResponse:
        return InternalResourceWithStreamingResponse(self)


class AsyncInternalResource(AsyncAPIResource):
    cli: AsyncCliResource
    consumer: AsyncConsumerResource
    logs: AsyncLogsResource
    org: AsyncOrgResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.cli = AsyncCliResource(client)
        self.consumer = AsyncConsumerResource(client)
        self.logs = AsyncLogsResource(client)
        self.org = AsyncOrgResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncInternalResourceWithRawResponse:
        return AsyncInternalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInternalResourceWithStreamingResponse:
        return AsyncInternalResourceWithStreamingResponse(self)


class InternalResourceWithRawResponse:
    def __init__(self, resource: InternalResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncInternalResourceWithRawResponse:
    def __init__(self, resource: AsyncInternalResource) -> None:
        self._resource = resource
        self._client = resource._client


class InternalResourceWithStreamingResponse:
    def __init__(self, resource: InternalResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncInternalResourceWithStreamingResponse:
    def __init__(self, resource: AsyncInternalResource) -> None:
        self._resource = resource
        self._client = resource._client
