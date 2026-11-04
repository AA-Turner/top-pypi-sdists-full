# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.link`` — the generated resource classes.

``LinkResource`` (sync) and ``AsyncLinkResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, RequestOptions
from .._models import LinkCreateBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ..types import link_create_params
from ..types.link_create_response import LinkCreateResponse
from ._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_body,
    require_fields,
)

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("link", "create")]


class LinkResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LinkResourceWithRawResponse:
        return LinkResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LinkResourceWithStreamingResponse:
        return LinkResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str,
        user_id: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LinkCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LinkCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LinkCreateResponse:
        body_fields = compact(
            {
                "auth_config_id": auth_config_id,
                "user_id": user_id,
                "alias": alias,
                "callback_url": callback_url,
                "connection_data": connection_data,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config_id", "user_id"),
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
            "/api/v3.1/connected_accounts/link",
            cast_to=LinkCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=LinkCreateBody,
            options=options_data,
        )


class AsyncLinkResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLinkResourceWithRawResponse:
        return AsyncLinkResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLinkResourceWithStreamingResponse:
        return AsyncLinkResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str,
        user_id: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LinkCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LinkCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> LinkCreateResponse:
        body_fields = compact(
            {
                "auth_config_id": auth_config_id,
                "user_id": user_id,
                "alias": alias,
                "callback_url": callback_url,
                "connection_data": connection_data,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config_id", "user_id"),
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
            "/api/v3.1/connected_accounts/link",
            cast_to=LinkCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=LinkCreateBody,
            options=options_data,
        )


class LinkResourceWithRawResponse:
    def __init__(self, resource: LinkResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str,
        user_id: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[LinkCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[LinkCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[LinkCreateResponse]:
        body_fields = compact(
            {
                "auth_config_id": auth_config_id,
                "user_id": user_id,
                "alias": alias,
                "callback_url": callback_url,
                "connection_data": connection_data,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config_id", "user_id"),
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
            "/api/v3.1/connected_accounts/link",
            cast_to=LinkCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=LinkCreateBody,
            options=options_data,
        )


class AsyncLinkResourceWithRawResponse:
    def __init__(self, resource: AsyncLinkResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str,
        user_id: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[LinkCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[LinkCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[LinkCreateResponse]:
        body_fields = compact(
            {
                "auth_config_id": auth_config_id,
                "user_id": user_id,
                "alias": alias,
                "callback_url": callback_url,
                "connection_data": connection_data,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config_id", "user_id"),
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
            "/api/v3.1/connected_accounts/link",
            cast_to=LinkCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=LinkCreateBody,
            options=options_data,
        )


class LinkResourceWithStreamingResponse:
    def __init__(self, resource: LinkResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str,
        user_id: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[LinkCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[LinkCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[LinkCreateResponse]]:
        body_fields = compact(
            {
                "auth_config_id": auth_config_id,
                "user_id": user_id,
                "alias": alias,
                "callback_url": callback_url,
                "connection_data": connection_data,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config_id", "user_id"),
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
                "/api/v3.1/connected_accounts/link",
                cast_to=LinkCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=LinkCreateBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncLinkResourceWithStreamingResponse:
    def __init__(self, resource: AsyncLinkResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str,
        user_id: str,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[LinkCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[LinkCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config_id: str | Omit = omit,
        user_id: str | Omit = omit,
        alias: str | Omit = omit,
        callback_url: str | Omit = omit,
        connection_data: link_create_params.ConnectionData | Omit = omit,
        experimental: link_create_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[LinkCreateResponse]]:
        body_fields = compact(
            {
                "auth_config_id": auth_config_id,
                "user_id": user_id,
                "alias": alias,
                "callback_url": callback_url,
                "connection_data": connection_data,
                "experimental": experimental,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config_id", "user_id"),
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
                "/api/v3.1/connected_accounts/link",
                cast_to=LinkCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=LinkCreateBody,
                options=options_data,
                stream=True,
            )
        )
