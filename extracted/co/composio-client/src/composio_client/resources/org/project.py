# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.org.project`` — the generated resource classes.

``ProjectResource`` (sync) and ``AsyncProjectResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx

from ..._base_client import QueryParam, RequestOptions
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ...types.org.project_list_response import ProjectListResponse
from .._base import AsyncAPIResource, SyncAPIResource, compact, make_request_options, merge_mapping

_LIST_OPERATION = OPERATIONS_BY_CHAIN[("org", "project", "list")]


class ProjectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProjectResourceWithRawResponse:
        return ProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectResourceWithStreamingResponse:
        return ProjectResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        list_all_org_projects: bool | None | Omit = omit,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectListResponse:
        query_fields = compact(
            {
                "list_all_org_projects": list_all_org_projects,
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
            "/api/v3.1/org/project/list",
            cast_to=ProjectListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncProjectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProjectResourceWithRawResponse:
        return AsyncProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectResourceWithStreamingResponse:
        return AsyncProjectResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        list_all_org_projects: bool | None | Omit = omit,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectListResponse:
        query_fields = compact(
            {
                "list_all_org_projects": list_all_org_projects,
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
            "/api/v3.1/org/project/list",
            cast_to=ProjectListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class ProjectResourceWithRawResponse:
    def __init__(self, resource: ProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list(
        self,
        *,
        list_all_org_projects: bool | None | Omit = omit,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectListResponse]:
        query_fields = compact(
            {
                "list_all_org_projects": list_all_org_projects,
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
            "/api/v3.1/org/project/list",
            cast_to=ProjectListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncProjectResourceWithRawResponse:
    def __init__(self, resource: AsyncProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def list(
        self,
        *,
        list_all_org_projects: bool | None | Omit = omit,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectListResponse]:
        query_fields = compact(
            {
                "list_all_org_projects": list_all_org_projects,
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
            "/api/v3.1/org/project/list",
            cast_to=ProjectListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class ProjectResourceWithStreamingResponse:
    def __init__(self, resource: ProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list(
        self,
        *,
        list_all_org_projects: bool | None | Omit = omit,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectListResponse]]:
        query_fields = compact(
            {
                "list_all_org_projects": list_all_org_projects,
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
                "/api/v3.1/org/project/list",
                cast_to=ProjectListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )


class AsyncProjectResourceWithStreamingResponse:
    def __init__(self, resource: AsyncProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list(
        self,
        *,
        list_all_org_projects: bool | None | Omit = omit,
        limit: int | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectListResponse]]:
        query_fields = compact(
            {
                "list_all_org_projects": list_all_org_projects,
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
                "/api/v3.1/org/project/list",
                cast_to=ProjectListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )
