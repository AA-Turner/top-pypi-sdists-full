# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.org.owner`` — the generated resource classes.

``OwnerResource`` (sync) and ``AsyncOwnerResource`` (async),
holding the sub-resources below.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ..._base import AsyncAPIResource, SyncAPIResource
from .project import AsyncProjectResource, ProjectResource

if TYPE_CHECKING:
    from ...._base_client import AsyncAPIClient, SyncAPIClient


class OwnerResource(SyncAPIResource):
    project: ProjectResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.project = ProjectResource(client)

    @cached_property
    def with_raw_response(self) -> OwnerResourceWithRawResponse:
        return OwnerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OwnerResourceWithStreamingResponse:
        return OwnerResourceWithStreamingResponse(self)


class AsyncOwnerResource(AsyncAPIResource):
    project: AsyncProjectResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.project = AsyncProjectResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncOwnerResourceWithRawResponse:
        return AsyncOwnerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOwnerResourceWithStreamingResponse:
        return AsyncOwnerResourceWithStreamingResponse(self)


class OwnerResourceWithRawResponse:
    def __init__(self, resource: OwnerResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncOwnerResourceWithRawResponse:
    def __init__(self, resource: AsyncOwnerResource) -> None:
        self._resource = resource
        self._client = resource._client


class OwnerResourceWithStreamingResponse:
    def __init__(self, resource: OwnerResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncOwnerResourceWithStreamingResponse:
    def __init__(self, resource: AsyncOwnerResource) -> None:
        self._resource = resource
        self._client = resource._client
