# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.session_configs`` — the generated resource classes.

``SessionConfigsResource`` (sync) and ``AsyncSessionConfigsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx

from .._base_client import QueryParam, RequestOptions
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ..types.session_configs_list_response import SessionConfigsListResponse
from ..types.session_configs_retrieve_response import SessionConfigsRetrieveResponse
from ._base import AsyncAPIResource, SyncAPIResource, build_path, compact, make_request_options, merge_mapping

_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("session_configs", "retrieve")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("session_configs", "list")]


class SessionConfigsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SessionConfigsResourceWithRawResponse:
        return SessionConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionConfigsResourceWithStreamingResponse:
        return SessionConfigsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        session_config_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionConfigsRetrieveResponse:
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
                "/api/v3.1/session_configs/{session_config_id}",
                {"session_config_id": session_config_id},
            ),
            cast_to=SessionConfigsRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def list(
        self,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        archived: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> SessionConfigsListResponse:
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "archived": archived,
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
            "/api/v3.1/session_configs",
            cast_to=SessionConfigsListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncSessionConfigsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSessionConfigsResourceWithRawResponse:
        return AsyncSessionConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionConfigsResourceWithStreamingResponse:
        return AsyncSessionConfigsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        session_config_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionConfigsRetrieveResponse:
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
                "/api/v3.1/session_configs/{session_config_id}",
                {"session_config_id": session_config_id},
            ),
            cast_to=SessionConfigsRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def list(
        self,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        archived: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> SessionConfigsListResponse:
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "archived": archived,
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
            "/api/v3.1/session_configs",
            cast_to=SessionConfigsListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class SessionConfigsResourceWithRawResponse:
    def __init__(self, resource: SessionConfigsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        session_config_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionConfigsRetrieveResponse]:
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
                "/api/v3.1/session_configs/{session_config_id}",
                {"session_config_id": session_config_id},
            ),
            cast_to=SessionConfigsRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def list(
        self,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        archived: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionConfigsListResponse]:
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "archived": archived,
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
            "/api/v3.1/session_configs",
            cast_to=SessionConfigsListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncSessionConfigsResourceWithRawResponse:
    def __init__(self, resource: AsyncSessionConfigsResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def retrieve(
        self,
        session_config_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionConfigsRetrieveResponse]:
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
                "/api/v3.1/session_configs/{session_config_id}",
                {"session_config_id": session_config_id},
            ),
            cast_to=SessionConfigsRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def list(
        self,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        archived: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionConfigsListResponse]:
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "archived": archived,
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
            "/api/v3.1/session_configs",
            cast_to=SessionConfigsListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )


class SessionConfigsResourceWithStreamingResponse:
    def __init__(self, resource: SessionConfigsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        session_config_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionConfigsRetrieveResponse]]:
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
                    "/api/v3.1/session_configs/{session_config_id}",
                    {"session_config_id": session_config_id},
                ),
                cast_to=SessionConfigsRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        archived: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionConfigsListResponse]]:
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "archived": archived,
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
                "/api/v3.1/session_configs",
                cast_to=SessionConfigsListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )


class AsyncSessionConfigsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncSessionConfigsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        session_config_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionConfigsRetrieveResponse]]:
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
                    "/api/v3.1/session_configs/{session_config_id}",
                    {"session_config_id": session_config_id},
                ),
                cast_to=SessionConfigsRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        archived: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionConfigsListResponse]]:
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "archived": archived,
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
                "/api/v3.1/session_configs",
                cast_to=SessionConfigsListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )
