# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.org`` — the generated resource classes.

``OrgResource`` (sync) and ``AsyncOrgResource`` (async),
holding the sub-resources below.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from ..._base import AsyncAPIResource, SyncAPIResource
from .consumer.consumer import AsyncConsumerResource, ConsumerResource

if TYPE_CHECKING:
    from ...._base_client import AsyncAPIClient, SyncAPIClient


class OrgResource(SyncAPIResource):
    consumer: ConsumerResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.consumer = ConsumerResource(client)

    @cached_property
    def with_raw_response(self) -> OrgResourceWithRawResponse:
        return OrgResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrgResourceWithStreamingResponse:
        return OrgResourceWithStreamingResponse(self)


class AsyncOrgResource(AsyncAPIResource):
    consumer: AsyncConsumerResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.consumer = AsyncConsumerResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncOrgResourceWithRawResponse:
        return AsyncOrgResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrgResourceWithStreamingResponse:
        return AsyncOrgResourceWithStreamingResponse(self)


class OrgResourceWithRawResponse:
    def __init__(self, resource: OrgResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncOrgResourceWithRawResponse:
    def __init__(self, resource: AsyncOrgResource) -> None:
        self._resource = resource
        self._client = resource._client


class OrgResourceWithStreamingResponse:
    def __init__(self, resource: OrgResource) -> None:
        self._resource = resource
        self._client = resource._client


class AsyncOrgResourceWithStreamingResponse:
    def __init__(self, resource: AsyncOrgResource) -> None:
        self._resource = resource
        self._client = resource._client
