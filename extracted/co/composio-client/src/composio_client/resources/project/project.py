# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.project`` — the generated resource classes.

``ProjectResource`` (sync) and ``AsyncProjectResource`` (async),
holding the sub-resources below.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from .._base import AsyncAPIResource, SyncAPIResource
from .usage import AsyncUsageResource, UsageResource

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient


class ProjectResource(SyncAPIResource):
    usage: UsageResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.usage = UsageResource(client)

    @cached_property
    def with_raw_response(self) -> ProjectResourceWithRawResponse:
        return ProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectResourceWithStreamingResponse:
        return ProjectResourceWithStreamingResponse(self)


class AsyncProjectResource(AsyncAPIResource):
    usage: AsyncUsageResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.usage = AsyncUsageResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncProjectResourceWithRawResponse:
        return AsyncProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectResourceWithStreamingResponse:
        return AsyncProjectResourceWithStreamingResponse(self)


class ProjectResourceWithRawResponse:
    def __init__(self, resource: ProjectResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncProjectResourceWithRawResponse:
    def __init__(self, resource: AsyncProjectResource) -> None:
        self._resource = resource
        self._client = resource._client


class ProjectResourceWithStreamingResponse:
    def __init__(self, resource: ProjectResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncProjectResourceWithStreamingResponse:
    def __init__(self, resource: AsyncProjectResource) -> None:
        self._resource = resource
        self._client = resource._client
