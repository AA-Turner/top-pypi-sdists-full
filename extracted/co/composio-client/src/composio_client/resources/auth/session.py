# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.auth.session`` — the generated resource classes.

``SessionResource`` (sync) and ``AsyncSessionResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx

from ..._base_client import RequestOptions
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Query
from ...types.auth.session_retrieve_info_response import SessionRetrieveInfoResponse
from .._base import AsyncAPIResource, SyncAPIResource, make_request_options

_RETRIEVE_INFO_OPERATION = OPERATIONS_BY_CHAIN[("auth", "session", "retrieve_info")]


class SessionResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SessionResourceWithRawResponse:
        return SessionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionResourceWithStreamingResponse:
        return SessionResourceWithStreamingResponse(self)

    def retrieve_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionRetrieveInfoResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/auth/session/info",
            cast_to=SessionRetrieveInfoResponse,
            operation=_RETRIEVE_INFO_OPERATION,
            options=options_data,
        )


class AsyncSessionResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSessionResourceWithRawResponse:
        return AsyncSessionResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionResourceWithStreamingResponse:
        return AsyncSessionResourceWithStreamingResponse(self)

    async def retrieve_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> SessionRetrieveInfoResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/auth/session/info",
            cast_to=SessionRetrieveInfoResponse,
            operation=_RETRIEVE_INFO_OPERATION,
            options=options_data,
        )


class SessionResourceWithRawResponse:
    def __init__(self, resource: SessionResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[SessionRetrieveInfoResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/auth/session/info",
            cast_to=SessionRetrieveInfoResponse,
            operation=_RETRIEVE_INFO_OPERATION,
            options=options_data,
        )


class AsyncSessionResourceWithRawResponse:
    def __init__(self, resource: AsyncSessionResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def retrieve_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[SessionRetrieveInfoResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/auth/session/info",
            cast_to=SessionRetrieveInfoResponse,
            operation=_RETRIEVE_INFO_OPERATION,
            options=options_data,
        )


class SessionResourceWithStreamingResponse:
    def __init__(self, resource: SessionResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[SessionRetrieveInfoResponse]]:
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
                "/api/v3.1/auth/session/info",
                cast_to=SessionRetrieveInfoResponse,
                operation=_RETRIEVE_INFO_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncSessionResourceWithStreamingResponse:
    def __init__(self, resource: AsyncSessionResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[SessionRetrieveInfoResponse]]:
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
                "/api/v3.1/auth/session/info",
                cast_to=SessionRetrieveInfoResponse,
                operation=_RETRIEVE_INFO_OPERATION,
                options=options_data,
                stream=True,
            )
        )
