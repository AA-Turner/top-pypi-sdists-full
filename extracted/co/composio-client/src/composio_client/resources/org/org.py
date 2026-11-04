# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.org`` — the generated resource classes.

``OrgResource`` (sync) and ``AsyncOrgResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

import httpx

from ..._base_client import QueryParam, RequestOptions
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ...types.org_list_response import OrgListResponse
from .._base import AsyncAPIResource, SyncAPIResource, compact, make_request_options, merge_mapping
from .owner.owner import AsyncOwnerResource, OwnerResource
from .project import AsyncProjectResource, ProjectResource
from .usage import AsyncUsageResource, UsageResource

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient

_LIST_OPERATION = OPERATIONS_BY_CHAIN[("org", "list")]


class OrgResource(SyncAPIResource):
    owner: OwnerResource
    project: ProjectResource
    usage: UsageResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.owner = OwnerResource(client)
        self.project = ProjectResource(client)
        self.usage = UsageResource(client)

    @cached_property
    def with_raw_response(self) -> OrgResourceWithRawResponse:
        return OrgResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OrgResourceWithStreamingResponse:
        return OrgResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> OrgListResponse:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/org/list",
            cast_to=OrgListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncOrgResource(AsyncAPIResource):
    owner: AsyncOwnerResource
    project: AsyncProjectResource
    usage: AsyncUsageResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.owner = AsyncOwnerResource(client)
        self.project = AsyncProjectResource(client)
        self.usage = AsyncUsageResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncOrgResourceWithRawResponse:
        return AsyncOrgResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOrgResourceWithStreamingResponse:
        return AsyncOrgResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> OrgListResponse:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/org/list",
            cast_to=OrgListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class OrgResourceWithRawResponse:
    def __init__(self, resource: OrgResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list(
        self,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[OrgListResponse]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/org/list",
            cast_to=OrgListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncOrgResourceWithRawResponse:
    def __init__(self, resource: AsyncOrgResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def list(
        self,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[OrgListResponse]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/org/list",
            cast_to=OrgListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class OrgResourceWithStreamingResponse:
    def __init__(self, resource: OrgResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list(
        self,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[OrgListResponse]]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return ResponseContextManager(
            lambda: self._client._request_raw(
                "get",
                "/api/v3.1/org/list",
                cast_to=OrgListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )


class AsyncOrgResourceWithStreamingResponse:
    def __init__(self, resource: AsyncOrgResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list(
        self,
        *,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[OrgListResponse]]:
        query_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
            }
        )
        query_data = merge_mapping(query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return AsyncResponseContextManager(
            self._client._request_raw(
                "get",
                "/api/v3.1/org/list",
                cast_to=OrgListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )
