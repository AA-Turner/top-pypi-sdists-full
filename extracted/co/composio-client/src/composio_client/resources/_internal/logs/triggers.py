# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.logs.triggers`` — the generated resource classes.

``TriggersResource`` (sync) and ``AsyncTriggersResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import cached_property
from typing import Literal

import httpx

from ...._base_client import BodyParam, RequestOptions
from ...._models import TriggerListBody
from ...._operations import OPERATIONS_BY_CHAIN
from ...._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ....types.logs import trigger_list_params
from ....types.logs.trigger_list_response import TriggerListResponse
from ....types.logs.trigger_retrieve_response import TriggerRetrieveResponse
from ..._base import AsyncAPIResource, SyncAPIResource, build_path, compact, make_request_options, merge_body

_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "logs", "triggers", "retrieve")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "logs", "triggers", "list")]


class TriggersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TriggersResourceWithRawResponse:
        return TriggersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TriggersResourceWithStreamingResponse:
        return TriggersResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> TriggerRetrieveResponse:
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
                "/api/v3.1/internal/trigger/log/{id}",
                {"id": id},
            ),
            cast_to=TriggerRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def list(
        self,
        body: BodyParam | None = None,
        *,
        time: Literal["5m", "30m", "6h", "1d", "1w", "1month", "1y"] | Omit = omit,
        from_: float | None | Omit = omit,
        to: float | None | Omit = omit,
        status: Literal["all", "success", "error"] | Omit = omit,
        search: str | Omit = omit,
        integration_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | None | Omit = omit,
        search_params: Iterable[trigger_list_params.SearchParam] | Omit = omit,
        include_payload: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> TriggerListResponse:
        body_fields = compact(
            {
                "time": time,
                "from": from_,
                "to": to,
                "status": status,
                "search": search,
                "integrationId": integration_id,
                "entityId": entity_id,
                "userId": user_id,
                "limit": limit,
                "cursor": cursor,
                "search_params": search_params,
                "include_payload": include_payload,
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
            "/api/v3.1/internal/trigger/logs",
            cast_to=TriggerListResponse,
            operation=_LIST_OPERATION,
            body=body_data,
            body_model=TriggerListBody,
            options=options_data,
        )


class AsyncTriggersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTriggersResourceWithRawResponse:
        return AsyncTriggersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTriggersResourceWithStreamingResponse:
        return AsyncTriggersResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    async def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> TriggerRetrieveResponse:
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
                "/api/v3.1/internal/trigger/log/{id}",
                {"id": id},
            ),
            cast_to=TriggerRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def list(
        self,
        body: BodyParam | None = None,
        *,
        time: Literal["5m", "30m", "6h", "1d", "1w", "1month", "1y"] | Omit = omit,
        from_: float | None | Omit = omit,
        to: float | None | Omit = omit,
        status: Literal["all", "success", "error"] | Omit = omit,
        search: str | Omit = omit,
        integration_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | None | Omit = omit,
        search_params: Iterable[trigger_list_params.SearchParam] | Omit = omit,
        include_payload: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> TriggerListResponse:
        body_fields = compact(
            {
                "time": time,
                "from": from_,
                "to": to,
                "status": status,
                "search": search,
                "integrationId": integration_id,
                "entityId": entity_id,
                "userId": user_id,
                "limit": limit,
                "cursor": cursor,
                "search_params": search_params,
                "include_payload": include_payload,
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
            "/api/v3.1/internal/trigger/logs",
            cast_to=TriggerListResponse,
            operation=_LIST_OPERATION,
            body=body_data,
            body_model=TriggerListBody,
            options=options_data,
        )


class TriggersResourceWithRawResponse:
    def __init__(self, resource: TriggersResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[TriggerRetrieveResponse]:
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
                "/api/v3.1/internal/trigger/log/{id}",
                {"id": id},
            ),
            cast_to=TriggerRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def list(
        self,
        body: BodyParam | None = None,
        *,
        time: Literal["5m", "30m", "6h", "1d", "1w", "1month", "1y"] | Omit = omit,
        from_: float | None | Omit = omit,
        to: float | None | Omit = omit,
        status: Literal["all", "success", "error"] | Omit = omit,
        search: str | Omit = omit,
        integration_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | None | Omit = omit,
        search_params: Iterable[trigger_list_params.SearchParam] | Omit = omit,
        include_payload: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[TriggerListResponse]:
        body_fields = compact(
            {
                "time": time,
                "from": from_,
                "to": to,
                "status": status,
                "search": search,
                "integrationId": integration_id,
                "entityId": entity_id,
                "userId": user_id,
                "limit": limit,
                "cursor": cursor,
                "search_params": search_params,
                "include_payload": include_payload,
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
            "/api/v3.1/internal/trigger/logs",
            cast_to=TriggerListResponse,
            operation=_LIST_OPERATION,
            body=body_data,
            body_model=TriggerListBody,
            options=options_data,
        )


class AsyncTriggersResourceWithRawResponse:
    def __init__(self, resource: AsyncTriggersResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    async def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[TriggerRetrieveResponse]:
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
                "/api/v3.1/internal/trigger/log/{id}",
                {"id": id},
            ),
            cast_to=TriggerRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def list(
        self,
        body: BodyParam | None = None,
        *,
        time: Literal["5m", "30m", "6h", "1d", "1w", "1month", "1y"] | Omit = omit,
        from_: float | None | Omit = omit,
        to: float | None | Omit = omit,
        status: Literal["all", "success", "error"] | Omit = omit,
        search: str | Omit = omit,
        integration_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | None | Omit = omit,
        search_params: Iterable[trigger_list_params.SearchParam] | Omit = omit,
        include_payload: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[TriggerListResponse]:
        body_fields = compact(
            {
                "time": time,
                "from": from_,
                "to": to,
                "status": status,
                "search": search,
                "integrationId": integration_id,
                "entityId": entity_id,
                "userId": user_id,
                "limit": limit,
                "cursor": cursor,
                "search_params": search_params,
                "include_payload": include_payload,
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
            "/api/v3.1/internal/trigger/logs",
            cast_to=TriggerListResponse,
            operation=_LIST_OPERATION,
            body=body_data,
            body_model=TriggerListBody,
            options=options_data,
        )


class TriggersResourceWithStreamingResponse:
    def __init__(self, resource: TriggersResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[TriggerRetrieveResponse]]:
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
                    "/api/v3.1/internal/trigger/log/{id}",
                    {"id": id},
                ),
                cast_to=TriggerRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        body: BodyParam | None = None,
        *,
        time: Literal["5m", "30m", "6h", "1d", "1w", "1month", "1y"] | Omit = omit,
        from_: float | None | Omit = omit,
        to: float | None | Omit = omit,
        status: Literal["all", "success", "error"] | Omit = omit,
        search: str | Omit = omit,
        integration_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | None | Omit = omit,
        search_params: Iterable[trigger_list_params.SearchParam] | Omit = omit,
        include_payload: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[TriggerListResponse]]:
        body_fields = compact(
            {
                "time": time,
                "from": from_,
                "to": to,
                "status": status,
                "search": search,
                "integrationId": integration_id,
                "entityId": entity_id,
                "userId": user_id,
                "limit": limit,
                "cursor": cursor,
                "search_params": search_params,
                "include_payload": include_payload,
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
                "/api/v3.1/internal/trigger/logs",
                cast_to=TriggerListResponse,
                operation=_LIST_OPERATION,
                body=body_data,
                body_model=TriggerListBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncTriggersResourceWithStreamingResponse:
    def __init__(self, resource: AsyncTriggersResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[TriggerRetrieveResponse]]:
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
                    "/api/v3.1/internal/trigger/log/{id}",
                    {"id": id},
                ),
                cast_to=TriggerRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        body: BodyParam | None = None,
        *,
        time: Literal["5m", "30m", "6h", "1d", "1w", "1month", "1y"] | Omit = omit,
        from_: float | None | Omit = omit,
        to: float | None | Omit = omit,
        status: Literal["all", "success", "error"] | Omit = omit,
        search: str | Omit = omit,
        integration_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | None | Omit = omit,
        search_params: Iterable[trigger_list_params.SearchParam] | Omit = omit,
        include_payload: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[TriggerListResponse]]:
        body_fields = compact(
            {
                "time": time,
                "from": from_,
                "to": to,
                "status": status,
                "search": search,
                "integrationId": integration_id,
                "entityId": entity_id,
                "userId": user_id,
                "limit": limit,
                "cursor": cursor,
                "search_params": search_params,
                "include_payload": include_payload,
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
                "/api/v3.1/internal/trigger/logs",
                cast_to=TriggerListResponse,
                operation=_LIST_OPERATION,
                body=body_data,
                body_model=TriggerListBody,
                options=options_data,
                stream=True,
            )
        )
