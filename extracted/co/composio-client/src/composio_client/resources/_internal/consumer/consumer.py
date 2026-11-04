# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.consumer`` — the generated resource classes.

``ConsumerResource`` (sync) and ``AsyncConsumerResource`` (async),
holding the sub-resources below.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ..._base import AsyncAPIResource, SyncAPIResource
from .permissions import AsyncPermissionsResource, PermissionsResource

if TYPE_CHECKING:
    from ...._base_client import AsyncAPIClient, SyncAPIClient


class ConsumerResource(SyncAPIResource):
    permissions: PermissionsResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.permissions = PermissionsResource(client)

    @cached_property
    def with_raw_response(self) -> ConsumerResourceWithRawResponse:
        return ConsumerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsumerResourceWithStreamingResponse:
        return ConsumerResourceWithStreamingResponse(self)


class AsyncConsumerResource(AsyncAPIResource):
    permissions: AsyncPermissionsResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.permissions = AsyncPermissionsResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncConsumerResourceWithRawResponse:
        return AsyncConsumerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsumerResourceWithStreamingResponse:
        return AsyncConsumerResourceWithStreamingResponse(self)


class ConsumerResourceWithRawResponse:
    def __init__(self, resource: ConsumerResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncConsumerResourceWithRawResponse:
    def __init__(self, resource: AsyncConsumerResource) -> None:
        self._resource = resource
        self._client = resource._client


class ConsumerResourceWithStreamingResponse:
    def __init__(self, resource: ConsumerResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncConsumerResourceWithStreamingResponse:
    def __init__(self, resource: AsyncConsumerResource) -> None:
        self._resource = resource
        self._client = resource._client
