# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.logs`` — the generated resource classes.

``LogsResource`` (sync) and ``AsyncLogsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import cached_property

import httpx

from .._base_client import BodyParam, RequestOptions
from .._models import LogCreateToolExecutionBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ..types import log_create_tool_execution_params
from ..types.log_create_tool_execution_response import LogCreateToolExecutionResponse
from ..types.log_retrieve_tool_execution_response import LogRetrieveToolExecutionResponse
from ._base import AsyncAPIResource, SyncAPIResource, build_path, compact, make_request_options, merge_body

_CREATE_TOOL_EXECUTION_OPERATION = OPERATIONS_BY_CHAIN[("logs", "create_tool_execution")]
_RETRIEVE_TOOL_EXECUTION_OPERATION = OPERATIONS_BY_CHAIN[("logs", "retrieve_tool_execution")]


class LogsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LogsResourceWithRawResponse:
        return LogsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LogsResourceWithStreamingResponse:
        return LogsResourceWithStreamingResponse(self)

    def create_tool_execution(
        self,
        body: BodyParam | None = None,
        *,
        limit: float | Omit = omit,
        cursor: str | None | Omit = omit,
        filters: Iterable[log_create_tool_execution_params.Filter] | Omit = omit,
        time_range: log_create_tool_execution_params.TimeRange | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LogCreateToolExecutionResponse:
        body_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "filters": filters,
                "time_range": time_range,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "post",
            "/api/v3.1/logs/tool_execution",
            cast_to=LogCreateToolExecutionResponse,
            operation=_CREATE_TOOL_EXECUTION_OPERATION,
            body=body_data,
            body_model=LogCreateToolExecutionBody,
            options=options_data,
        )

    def retrieve_tool_execution(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LogRetrieveToolExecutionResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            build_path(
                "/api/v3.1/logs/tool_execution/{id}",
                {"id": id},
            ),
            cast_to=LogRetrieveToolExecutionResponse,
            operation=_RETRIEVE_TOOL_EXECUTION_OPERATION,
            options=options_data,
        )


class AsyncLogsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLogsResourceWithRawResponse:
        return AsyncLogsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLogsResourceWithStreamingResponse:
        return AsyncLogsResourceWithStreamingResponse(self)

    async def create_tool_execution(
        self,
        body: BodyParam | None = None,
        *,
        limit: float | Omit = omit,
        cursor: str | None | Omit = omit,
        filters: Iterable[log_create_tool_execution_params.Filter] | Omit = omit,
        time_range: log_create_tool_execution_params.TimeRange | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LogCreateToolExecutionResponse:
        body_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "filters": filters,
                "time_range": time_range,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "post",
            "/api/v3.1/logs/tool_execution",
            cast_to=LogCreateToolExecutionResponse,
            operation=_CREATE_TOOL_EXECUTION_OPERATION,
            body=body_data,
            body_model=LogCreateToolExecutionBody,
            options=options_data,
        )

    async def retrieve_tool_execution(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LogRetrieveToolExecutionResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            build_path(
                "/api/v3.1/logs/tool_execution/{id}",
                {"id": id},
            ),
            cast_to=LogRetrieveToolExecutionResponse,
            operation=_RETRIEVE_TOOL_EXECUTION_OPERATION,
            options=options_data,
        )


class LogsResourceWithRawResponse:
    def __init__(self, resource: LogsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def create_tool_execution(
        self,
        body: BodyParam | None = None,
        *,
        limit: float | Omit = omit,
        cursor: str | None | Omit = omit,
        filters: Iterable[log_create_tool_execution_params.Filter] | Omit = omit,
        time_range: log_create_tool_execution_params.TimeRange | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[LogCreateToolExecutionResponse]:
        body_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "filters": filters,
                "time_range": time_range,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "post",
            "/api/v3.1/logs/tool_execution",
            cast_to=LogCreateToolExecutionResponse,
            operation=_CREATE_TOOL_EXECUTION_OPERATION,
            body=body_data,
            body_model=LogCreateToolExecutionBody,
            options=options_data,
        )

    def retrieve_tool_execution(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[LogRetrieveToolExecutionResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            build_path(
                "/api/v3.1/logs/tool_execution/{id}",
                {"id": id},
            ),
            cast_to=LogRetrieveToolExecutionResponse,
            operation=_RETRIEVE_TOOL_EXECUTION_OPERATION,
            options=options_data,
        )


class AsyncLogsResourceWithRawResponse:
    def __init__(self, resource: AsyncLogsResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def create_tool_execution(
        self,
        body: BodyParam | None = None,
        *,
        limit: float | Omit = omit,
        cursor: str | None | Omit = omit,
        filters: Iterable[log_create_tool_execution_params.Filter] | Omit = omit,
        time_range: log_create_tool_execution_params.TimeRange | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[LogCreateToolExecutionResponse]:
        body_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "filters": filters,
                "time_range": time_range,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "post",
            "/api/v3.1/logs/tool_execution",
            cast_to=LogCreateToolExecutionResponse,
            operation=_CREATE_TOOL_EXECUTION_OPERATION,
            body=body_data,
            body_model=LogCreateToolExecutionBody,
            options=options_data,
        )

    async def retrieve_tool_execution(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[LogRetrieveToolExecutionResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            build_path(
                "/api/v3.1/logs/tool_execution/{id}",
                {"id": id},
            ),
            cast_to=LogRetrieveToolExecutionResponse,
            operation=_RETRIEVE_TOOL_EXECUTION_OPERATION,
            options=options_data,
        )


class LogsResourceWithStreamingResponse:
    def __init__(self, resource: LogsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def create_tool_execution(
        self,
        body: BodyParam | None = None,
        *,
        limit: float | Omit = omit,
        cursor: str | None | Omit = omit,
        filters: Iterable[log_create_tool_execution_params.Filter] | Omit = omit,
        time_range: log_create_tool_execution_params.TimeRange | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[LogCreateToolExecutionResponse]]:
        body_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "filters": filters,
                "time_range": time_range,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return ResponseContextManager(
            lambda: self._client._request_raw(
                "post",
                "/api/v3.1/logs/tool_execution",
                cast_to=LogCreateToolExecutionResponse,
                operation=_CREATE_TOOL_EXECUTION_OPERATION,
                body=body_data,
                body_model=LogCreateToolExecutionBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_tool_execution(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[LogRetrieveToolExecutionResponse]]:
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
                build_path(
                    "/api/v3.1/logs/tool_execution/{id}",
                    {"id": id},
                ),
                cast_to=LogRetrieveToolExecutionResponse,
                operation=_RETRIEVE_TOOL_EXECUTION_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncLogsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncLogsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def create_tool_execution(
        self,
        body: BodyParam | None = None,
        *,
        limit: float | Omit = omit,
        cursor: str | None | Omit = omit,
        filters: Iterable[log_create_tool_execution_params.Filter] | Omit = omit,
        time_range: log_create_tool_execution_params.TimeRange | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[LogCreateToolExecutionResponse]]:
        body_fields = compact(
            {
                "limit": limit,
                "cursor": cursor,
                "filters": filters,
                "time_range": time_range,
            }
        )
        body_data = merge_body(body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return AsyncResponseContextManager(
            self._client._request_raw(
                "post",
                "/api/v3.1/logs/tool_execution",
                cast_to=LogCreateToolExecutionResponse,
                operation=_CREATE_TOOL_EXECUTION_OPERATION,
                body=body_data,
                body_model=LogCreateToolExecutionBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_tool_execution(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[LogRetrieveToolExecutionResponse]]:
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
                build_path(
                    "/api/v3.1/logs/tool_execution/{id}",
                    {"id": id},
                ),
                cast_to=LogRetrieveToolExecutionResponse,
                operation=_RETRIEVE_TOOL_EXECUTION_OPERATION,
                options=options_data,
                stream=True,
            )
        )
