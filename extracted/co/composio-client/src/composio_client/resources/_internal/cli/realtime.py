# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.cli.realtime`` — the generated resource classes.

``RealtimeResource`` (sync) and ``AsyncRealtimeResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from ...._base_client import BodyParam, RequestOptions
from ...._models import RealtimeAuthBody
from ...._operations import OPERATIONS_BY_CHAIN
from ...._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ....types.cli.realtime_auth_response import RealtimeAuthResponse
from ....types.cli.realtime_credentials_response import RealtimeCredentialsResponse
from ..._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_body,
    require_fields,
)

_AUTH_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "cli", "realtime", "auth")]
_CREDENTIALS_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "cli", "realtime", "credentials")]


class RealtimeResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RealtimeResourceWithRawResponse:
        return RealtimeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RealtimeResourceWithStreamingResponse:
        return RealtimeResourceWithStreamingResponse(self)

    @overload
    def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str,
        socket_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> RealtimeAuthResponse: ...

    @overload
    def auth(
        self,
        body: BodyParam,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> RealtimeAuthResponse: ...

    def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> RealtimeAuthResponse:
        body_fields = compact(
            {
                "channel_name": channel_name,
                "socket_id": socket_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("channel_name", "socket_id"),
            "body",
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
            "/api/v3.1/cli/realtime/auth",
            cast_to=RealtimeAuthResponse,
            operation=_AUTH_OPERATION,
            body=body_data,
            body_model=RealtimeAuthBody,
            options=options_data,
        )

    def credentials(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> RealtimeCredentialsResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/cli/realtime/credentials",
            cast_to=RealtimeCredentialsResponse,
            operation=_CREDENTIALS_OPERATION,
            options=options_data,
        )


class AsyncRealtimeResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRealtimeResourceWithRawResponse:
        return AsyncRealtimeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRealtimeResourceWithStreamingResponse:
        return AsyncRealtimeResourceWithStreamingResponse(self)

    @overload
    async def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str,
        socket_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> RealtimeAuthResponse: ...

    @overload
    async def auth(
        self,
        body: BodyParam,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> RealtimeAuthResponse: ...

    async def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> RealtimeAuthResponse:
        body_fields = compact(
            {
                "channel_name": channel_name,
                "socket_id": socket_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("channel_name", "socket_id"),
            "body",
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
            "/api/v3.1/cli/realtime/auth",
            cast_to=RealtimeAuthResponse,
            operation=_AUTH_OPERATION,
            body=body_data,
            body_model=RealtimeAuthBody,
            options=options_data,
        )

    async def credentials(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> RealtimeCredentialsResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/cli/realtime/credentials",
            cast_to=RealtimeCredentialsResponse,
            operation=_CREDENTIALS_OPERATION,
            options=options_data,
        )


class RealtimeResourceWithRawResponse:
    def __init__(self, resource: RealtimeResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str,
        socket_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[RealtimeAuthResponse]: ...

    @overload
    def auth(
        self,
        body: BodyParam,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[RealtimeAuthResponse]: ...

    def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[RealtimeAuthResponse]:
        body_fields = compact(
            {
                "channel_name": channel_name,
                "socket_id": socket_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("channel_name", "socket_id"),
            "body",
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
            "/api/v3.1/cli/realtime/auth",
            cast_to=RealtimeAuthResponse,
            operation=_AUTH_OPERATION,
            body=body_data,
            body_model=RealtimeAuthBody,
            options=options_data,
        )

    def credentials(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[RealtimeCredentialsResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/cli/realtime/credentials",
            cast_to=RealtimeCredentialsResponse,
            operation=_CREDENTIALS_OPERATION,
            options=options_data,
        )


class AsyncRealtimeResourceWithRawResponse:
    def __init__(self, resource: AsyncRealtimeResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str,
        socket_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[RealtimeAuthResponse]: ...

    @overload
    async def auth(
        self,
        body: BodyParam,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[RealtimeAuthResponse]: ...

    async def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[RealtimeAuthResponse]:
        body_fields = compact(
            {
                "channel_name": channel_name,
                "socket_id": socket_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("channel_name", "socket_id"),
            "body",
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
            "/api/v3.1/cli/realtime/auth",
            cast_to=RealtimeAuthResponse,
            operation=_AUTH_OPERATION,
            body=body_data,
            body_model=RealtimeAuthBody,
            options=options_data,
        )

    async def credentials(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[RealtimeCredentialsResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/cli/realtime/credentials",
            cast_to=RealtimeCredentialsResponse,
            operation=_CREDENTIALS_OPERATION,
            options=options_data,
        )


class RealtimeResourceWithStreamingResponse:
    def __init__(self, resource: RealtimeResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str,
        socket_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[RealtimeAuthResponse]]: ...

    @overload
    def auth(
        self,
        body: BodyParam,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[RealtimeAuthResponse]]: ...

    def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[RealtimeAuthResponse]]:
        body_fields = compact(
            {
                "channel_name": channel_name,
                "socket_id": socket_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("channel_name", "socket_id"),
            "body",
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
                "/api/v3.1/cli/realtime/auth",
                cast_to=RealtimeAuthResponse,
                operation=_AUTH_OPERATION,
                body=body_data,
                body_model=RealtimeAuthBody,
                options=options_data,
                stream=True,
            )
        )

    def credentials(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[RealtimeCredentialsResponse]]:
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
                "/api/v3.1/cli/realtime/credentials",
                cast_to=RealtimeCredentialsResponse,
                operation=_CREDENTIALS_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncRealtimeResourceWithStreamingResponse:
    def __init__(self, resource: AsyncRealtimeResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str,
        socket_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[RealtimeAuthResponse]]: ...

    @overload
    def auth(
        self,
        body: BodyParam,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[RealtimeAuthResponse]]: ...

    def auth(
        self,
        body: BodyParam | None = None,
        *,
        channel_name: str | Omit = omit,
        socket_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[RealtimeAuthResponse]]:
        body_fields = compact(
            {
                "channel_name": channel_name,
                "socket_id": socket_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("channel_name", "socket_id"),
            "body",
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
                "/api/v3.1/cli/realtime/auth",
                cast_to=RealtimeAuthResponse,
                operation=_AUTH_OPERATION,
                body=body_data,
                body_model=RealtimeAuthBody,
                options=options_data,
                stream=True,
            )
        )

    def credentials(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[RealtimeCredentialsResponse]]:
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
                "/api/v3.1/cli/realtime/credentials",
                cast_to=RealtimeCredentialsResponse,
                operation=_CREDENTIALS_OPERATION,
                options=options_data,
                stream=True,
            )
        )
