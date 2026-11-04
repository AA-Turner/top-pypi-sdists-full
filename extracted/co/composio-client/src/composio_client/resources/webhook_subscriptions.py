# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.webhook_subscriptions`` — the generated resource classes.

``WebhookSubscriptionsResource`` (sync) and ``AsyncWebhookSubscriptionsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import Literal

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, QueryParam, RequestOptions
from .._models import WebhookSubscriptionCreateBody, WebhookSubscriptionUpdateBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ..types.webhook_subscription_create_response import WebhookSubscriptionCreateResponse
from ..types.webhook_subscription_delete_response import WebhookSubscriptionDeleteResponse
from ..types.webhook_subscription_list_event_types_response import WebhookSubscriptionListEventTypesResponse
from ..types.webhook_subscription_list_response import WebhookSubscriptionListResponse
from ..types.webhook_subscription_retrieve_response import WebhookSubscriptionRetrieveResponse
from ..types.webhook_subscription_rotate_secret_response import WebhookSubscriptionRotateSecretResponse
from ..types.webhook_subscription_update_response import WebhookSubscriptionUpdateResponse
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

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("webhook_subscriptions", "create")]
_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("webhook_subscriptions", "retrieve")]
_UPDATE_OPERATION = OPERATIONS_BY_CHAIN[("webhook_subscriptions", "update")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("webhook_subscriptions", "list")]
_DELETE_OPERATION = OPERATIONS_BY_CHAIN[("webhook_subscriptions", "delete")]
_LIST_EVENT_TYPES_OPERATION = OPERATIONS_BY_CHAIN[("webhook_subscriptions", "list_event_types")]
_ROTATE_SECRET_OPERATION = OPERATIONS_BY_CHAIN[("webhook_subscriptions", "rotate_secret")]


class WebhookSubscriptionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhookSubscriptionsResourceWithRawResponse:
        return WebhookSubscriptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhookSubscriptionsResourceWithStreamingResponse:
        return WebhookSubscriptionsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str,
        enabled_events: SequenceNotStr[str],
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionCreateResponse:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("webhook_url", "enabled_events"),
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
            "/api/v3.1/webhook_subscriptions",
            cast_to=WebhookSubscriptionCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=WebhookSubscriptionCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionRetrieveResponse:
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
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionUpdateResponse:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
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
            "patch",
            build_path(
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=WebhookSubscriptionUpdateBody,
            options=options_data,
        )

    def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionListResponse:
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
            "/api/v3.1/webhook_subscriptions",
            cast_to=WebhookSubscriptionListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionDeleteResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "delete",
            build_path(
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    def list_event_types(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionListEventTypesResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/webhook_subscriptions/event_types",
            cast_to=WebhookSubscriptionListEventTypesResponse,
            operation=_LIST_EVENT_TYPES_OPERATION,
            options=options_data,
        )

    def rotate_secret(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionRotateSecretResponse:
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
                "/api/v3.1/webhook_subscriptions/{id}/rotate_secret",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionRotateSecretResponse,
            operation=_ROTATE_SECRET_OPERATION,
            options=options_data,
        )


class AsyncWebhookSubscriptionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhookSubscriptionsResourceWithRawResponse:
        return AsyncWebhookSubscriptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhookSubscriptionsResourceWithStreamingResponse:
        return AsyncWebhookSubscriptionsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str,
        enabled_events: SequenceNotStr[str],
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionCreateResponse:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("webhook_url", "enabled_events"),
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
            "/api/v3.1/webhook_subscriptions",
            cast_to=WebhookSubscriptionCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=WebhookSubscriptionCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionRetrieveResponse:
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
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionUpdateResponse:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
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
            "patch",
            build_path(
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=WebhookSubscriptionUpdateBody,
            options=options_data,
        )

    async def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionListResponse:
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
            "/api/v3.1/webhook_subscriptions",
            cast_to=WebhookSubscriptionListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionDeleteResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "delete",
            build_path(
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    async def list_event_types(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionListEventTypesResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/webhook_subscriptions/event_types",
            cast_to=WebhookSubscriptionListEventTypesResponse,
            operation=_LIST_EVENT_TYPES_OPERATION,
            options=options_data,
        )

    async def rotate_secret(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> WebhookSubscriptionRotateSecretResponse:
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
                "/api/v3.1/webhook_subscriptions/{id}/rotate_secret",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionRotateSecretResponse,
            operation=_ROTATE_SECRET_OPERATION,
            options=options_data,
        )


class WebhookSubscriptionsResourceWithRawResponse:
    def __init__(self, resource: WebhookSubscriptionsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str,
        enabled_events: SequenceNotStr[str],
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionCreateResponse]:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("webhook_url", "enabled_events"),
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
            "/api/v3.1/webhook_subscriptions",
            cast_to=WebhookSubscriptionCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=WebhookSubscriptionCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionRetrieveResponse]:
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
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionUpdateResponse]:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
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
            "patch",
            build_path(
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=WebhookSubscriptionUpdateBody,
            options=options_data,
        )

    def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionListResponse]:
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
            "/api/v3.1/webhook_subscriptions",
            cast_to=WebhookSubscriptionListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionDeleteResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "delete",
            build_path(
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    def list_event_types(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionListEventTypesResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/webhook_subscriptions/event_types",
            cast_to=WebhookSubscriptionListEventTypesResponse,
            operation=_LIST_EVENT_TYPES_OPERATION,
            options=options_data,
        )

    def rotate_secret(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[WebhookSubscriptionRotateSecretResponse]:
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
                "/api/v3.1/webhook_subscriptions/{id}/rotate_secret",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionRotateSecretResponse,
            operation=_ROTATE_SECRET_OPERATION,
            options=options_data,
        )


class AsyncWebhookSubscriptionsResourceWithRawResponse:
    def __init__(self, resource: AsyncWebhookSubscriptionsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str,
        enabled_events: SequenceNotStr[str],
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionCreateResponse]:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("webhook_url", "enabled_events"),
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
            "/api/v3.1/webhook_subscriptions",
            cast_to=WebhookSubscriptionCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=WebhookSubscriptionCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionRetrieveResponse]:
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
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionUpdateResponse]:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
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
            "patch",
            build_path(
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=WebhookSubscriptionUpdateBody,
            options=options_data,
        )

    async def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionListResponse]:
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
            "/api/v3.1/webhook_subscriptions",
            cast_to=WebhookSubscriptionListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionDeleteResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "delete",
            build_path(
                "/api/v3.1/webhook_subscriptions/{id}",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    async def list_event_types(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionListEventTypesResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/webhook_subscriptions/event_types",
            cast_to=WebhookSubscriptionListEventTypesResponse,
            operation=_LIST_EVENT_TYPES_OPERATION,
            options=options_data,
        )

    async def rotate_secret(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[WebhookSubscriptionRotateSecretResponse]:
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
                "/api/v3.1/webhook_subscriptions/{id}/rotate_secret",
                {"id": id},
            ),
            cast_to=WebhookSubscriptionRotateSecretResponse,
            operation=_ROTATE_SECRET_OPERATION,
            options=options_data,
        )


class WebhookSubscriptionsResourceWithStreamingResponse:
    def __init__(self, resource: WebhookSubscriptionsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str,
        enabled_events: SequenceNotStr[str],
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionCreateResponse]]:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("webhook_url", "enabled_events"),
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
                "/api/v3.1/webhook_subscriptions",
                cast_to=WebhookSubscriptionCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=WebhookSubscriptionCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionRetrieveResponse]]:
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
                    "/api/v3.1/webhook_subscriptions/{id}",
                    {"id": id},
                ),
                cast_to=WebhookSubscriptionRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionUpdateResponse]]:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
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
                "patch",
                build_path(
                    "/api/v3.1/webhook_subscriptions/{id}",
                    {"id": id},
                ),
                cast_to=WebhookSubscriptionUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=WebhookSubscriptionUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionListResponse]]:
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
                "/api/v3.1/webhook_subscriptions",
                cast_to=WebhookSubscriptionListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionDeleteResponse]]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return ResponseContextManager(
            lambda: self._client._request_raw(
                "delete",
                build_path(
                    "/api/v3.1/webhook_subscriptions/{id}",
                    {"id": id},
                ),
                cast_to=WebhookSubscriptionDeleteResponse,
                operation=_DELETE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list_event_types(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionListEventTypesResponse]]:
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
                "/api/v3.1/webhook_subscriptions/event_types",
                cast_to=WebhookSubscriptionListEventTypesResponse,
                operation=_LIST_EVENT_TYPES_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def rotate_secret(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[WebhookSubscriptionRotateSecretResponse]]:
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
                    "/api/v3.1/webhook_subscriptions/{id}/rotate_secret",
                    {"id": id},
                ),
                cast_to=WebhookSubscriptionRotateSecretResponse,
                operation=_ROTATE_SECRET_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncWebhookSubscriptionsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncWebhookSubscriptionsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str,
        enabled_events: SequenceNotStr[str],
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionCreateResponse]]:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("webhook_url", "enabled_events"),
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
                "/api/v3.1/webhook_subscriptions",
                cast_to=WebhookSubscriptionCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=WebhookSubscriptionCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionRetrieveResponse]]:
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
                    "/api/v3.1/webhook_subscriptions/{id}",
                    {"id": id},
                ),
                cast_to=WebhookSubscriptionRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        webhook_url: str | Omit = omit,
        enabled_events: SequenceNotStr[str] | Omit = omit,
        version: Literal["V1", "V2", "V3"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionUpdateResponse]]:
        body_fields = compact(
            {
                "webhook_url": webhook_url,
                "enabled_events": enabled_events,
                "version": version,
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
                "patch",
                build_path(
                    "/api/v3.1/webhook_subscriptions/{id}",
                    {"id": id},
                ),
                cast_to=WebhookSubscriptionUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=WebhookSubscriptionUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionListResponse]]:
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
                "/api/v3.1/webhook_subscriptions",
                cast_to=WebhookSubscriptionListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionDeleteResponse]]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return AsyncResponseContextManager(
            self._client._request_raw(
                "delete",
                build_path(
                    "/api/v3.1/webhook_subscriptions/{id}",
                    {"id": id},
                ),
                cast_to=WebhookSubscriptionDeleteResponse,
                operation=_DELETE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list_event_types(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionListEventTypesResponse]]:
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
                "/api/v3.1/webhook_subscriptions/event_types",
                cast_to=WebhookSubscriptionListEventTypesResponse,
                operation=_LIST_EVENT_TYPES_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def rotate_secret(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[WebhookSubscriptionRotateSecretResponse]]:
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
                    "/api/v3.1/webhook_subscriptions/{id}/rotate_secret",
                    {"id": id},
                ),
                cast_to=WebhookSubscriptionRotateSecretResponse,
                operation=_ROTATE_SECRET_OPERATION,
                options=options_data,
                stream=True,
            )
        )
