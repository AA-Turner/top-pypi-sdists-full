# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.webhook_endpoints`` — the generated resource classes.

``WebhookEndpointsResource`` (sync) and ``AsyncWebhookEndpointsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, QueryParam, RequestOptions
from .._models import WebhookEndpointCreateBody, WebhookEndpointReplaceBody, WebhookEndpointUpdateBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ..types.webhook_endpoint_create_response import WebhookEndpointCreateResponse
from ..types.webhook_endpoint_list_response import WebhookEndpointListResponse
from ..types.webhook_endpoint_replace_response import WebhookEndpointReplaceResponse
from ..types.webhook_endpoint_retrieve_response import WebhookEndpointRetrieveResponse
from ..types.webhook_endpoint_update_response import WebhookEndpointUpdateResponse
from ._base import (
    AsyncAPIResource,
    SyncAPIResource,
    build_path,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
    require_fields,
)

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("webhook_endpoints", "create")]
_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("webhook_endpoints", "retrieve")]
_UPDATE_OPERATION = OPERATIONS_BY_CHAIN[("webhook_endpoints", "update")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("webhook_endpoints", "list")]
_REPLACE_OPERATION = OPERATIONS_BY_CHAIN[("webhook_endpoints", "replace")]


class WebhookEndpointsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhookEndpointsResourceWithRawResponse:
        return WebhookEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhookEndpointsResourceWithStreamingResponse:
        return WebhookEndpointsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        client_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointCreateResponse:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "client_id": client_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "client_id"),
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
            "/api/v3.1/webhook_endpoints",
            cast_to=WebhookEndpointCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointRetrieveResponse:
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
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    @overload
    def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointUpdateResponse: ...

    @overload
    def update(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointUpdateResponse: ...

    def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointUpdateResponse:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
            "patch",
            build_path(
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointUpdateBody,
            options=options_data,
        )

    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointListResponse:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
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
            "/api/v3.1/webhook_endpoints",
            cast_to=WebhookEndpointListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointReplaceResponse: ...

    @overload
    def replace(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointReplaceResponse: ...

    def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointReplaceResponse:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
            build_path(
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointReplaceResponse,
            operation=_REPLACE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointReplaceBody,
            options=options_data,
        )


class AsyncWebhookEndpointsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhookEndpointsResourceWithRawResponse:
        return AsyncWebhookEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhookEndpointsResourceWithStreamingResponse:
        return AsyncWebhookEndpointsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        client_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointCreateResponse:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "client_id": client_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "client_id"),
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
            "/api/v3.1/webhook_endpoints",
            cast_to=WebhookEndpointCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointRetrieveResponse:
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
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    @overload
    async def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointUpdateResponse: ...

    @overload
    async def update(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointUpdateResponse: ...

    async def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointUpdateResponse:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
            "patch",
            build_path(
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointUpdateBody,
            options=options_data,
        )

    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointListResponse:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
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
            "/api/v3.1/webhook_endpoints",
            cast_to=WebhookEndpointListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointReplaceResponse: ...

    @overload
    async def replace(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointReplaceResponse: ...

    async def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookEndpointReplaceResponse:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
            build_path(
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointReplaceResponse,
            operation=_REPLACE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointReplaceBody,
            options=options_data,
        )


class WebhookEndpointsResourceWithRawResponse:
    def __init__(self, resource: WebhookEndpointsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        client_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointCreateResponse]:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "client_id": client_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "client_id"),
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
            "/api/v3.1/webhook_endpoints",
            cast_to=WebhookEndpointCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointRetrieveResponse]:
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
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    @overload
    def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointUpdateResponse]: ...

    @overload
    def update(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointUpdateResponse]: ...

    def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointUpdateResponse]:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
            "patch",
            build_path(
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointUpdateBody,
            options=options_data,
        )

    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointListResponse]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
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
            "/api/v3.1/webhook_endpoints",
            cast_to=WebhookEndpointListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointReplaceResponse]: ...

    @overload
    def replace(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointReplaceResponse]: ...

    def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookEndpointReplaceResponse]:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
            build_path(
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointReplaceResponse,
            operation=_REPLACE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointReplaceBody,
            options=options_data,
        )


class AsyncWebhookEndpointsResourceWithRawResponse:
    def __init__(self, resource: AsyncWebhookEndpointsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        client_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointCreateResponse]:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "client_id": client_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "client_id"),
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
            "/api/v3.1/webhook_endpoints",
            cast_to=WebhookEndpointCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointRetrieveResponse]:
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
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    @overload
    async def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointUpdateResponse]: ...

    @overload
    async def update(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointUpdateResponse]: ...

    async def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointUpdateResponse]:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
            "patch",
            build_path(
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointUpdateBody,
            options=options_data,
        )

    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointListResponse]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
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
            "/api/v3.1/webhook_endpoints",
            cast_to=WebhookEndpointListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointReplaceResponse]: ...

    @overload
    async def replace(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointReplaceResponse]: ...

    async def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookEndpointReplaceResponse]:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
            build_path(
                "/api/v3.1/webhook_endpoints/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=WebhookEndpointReplaceResponse,
            operation=_REPLACE_OPERATION,
            body=body_data,
            body_model=WebhookEndpointReplaceBody,
            options=options_data,
        )


class WebhookEndpointsResourceWithStreamingResponse:
    def __init__(self, resource: WebhookEndpointsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        client_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointCreateResponse]]:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "client_id": client_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "client_id"),
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
                "/api/v3.1/webhook_endpoints",
                cast_to=WebhookEndpointCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=WebhookEndpointCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointRetrieveResponse]]:
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
                    "/api/v3.1/webhook_endpoints/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=WebhookEndpointRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointUpdateResponse]]: ...

    @overload
    def update(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointUpdateResponse]]: ...

    def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointUpdateResponse]]:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
                "patch",
                build_path(
                    "/api/v3.1/webhook_endpoints/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=WebhookEndpointUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=WebhookEndpointUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointListResponse]]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
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
                "/api/v3.1/webhook_endpoints",
                cast_to=WebhookEndpointListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointReplaceResponse]]: ...

    @overload
    def replace(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointReplaceResponse]]: ...

    def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookEndpointReplaceResponse]]:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
                build_path(
                    "/api/v3.1/webhook_endpoints/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=WebhookEndpointReplaceResponse,
                operation=_REPLACE_OPERATION,
                body=body_data,
                body_model=WebhookEndpointReplaceBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncWebhookEndpointsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncWebhookEndpointsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        client_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        client_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointCreateResponse]]:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "client_id": client_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "client_id"),
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
                "/api/v3.1/webhook_endpoints",
                cast_to=WebhookEndpointCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=WebhookEndpointCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointRetrieveResponse]]:
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
                    "/api/v3.1/webhook_endpoints/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=WebhookEndpointRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointUpdateResponse]]: ...

    @overload
    def update(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointUpdateResponse]]: ...

    def update(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointUpdateResponse]]:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
                "patch",
                build_path(
                    "/api/v3.1/webhook_endpoints/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=WebhookEndpointUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=WebhookEndpointUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointListResponse]]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
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
                "/api/v3.1/webhook_endpoints",
                cast_to=WebhookEndpointListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointReplaceResponse]]: ...

    @overload
    def replace(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointReplaceResponse]]: ...

    def replace(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        data: dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookEndpointReplaceResponse]]:
        body_fields = compact(
            {
                "data": data,
            }
        )
        require_fields(
            body,
            body_fields,
            ("data",),
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
                build_path(
                    "/api/v3.1/webhook_endpoints/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=WebhookEndpointReplaceResponse,
                operation=_REPLACE_OPERATION,
                body=body_data,
                body_model=WebhookEndpointReplaceBody,
                options=options_data,
                stream=True,
            )
        )
