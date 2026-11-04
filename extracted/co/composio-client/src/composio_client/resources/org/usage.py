# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.org.usage`` — the generated resource classes.

``UsageResource`` (sync) and ``AsyncUsageResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import Literal

import httpx

from ..._base_client import BodyParam, RequestOptions
from ..._models import OrgUsageRetrieveBody, OrgUsageRetrieveSummaryBody
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ...types.org import usage_retrieve_params, usage_retrieve_summary_params
from ...types.org.usage_retrieve_response import UsageRetrieveResponse
from ...types.org.usage_retrieve_summary_response import UsageRetrieveSummaryResponse
from .._base import AsyncAPIResource, SyncAPIResource, build_path, compact, make_request_options, merge_body

_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("org", "usage", "retrieve")]
_RETRIEVE_SUMMARY_OPERATION = OPERATIONS_BY_CHAIN[("org", "usage", "retrieve_summary")]


class UsageResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UsageResourceWithRawResponse:
        return UsageResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsageResourceWithStreamingResponse:
        return UsageResourceWithStreamingResponse(self)

    def retrieve(
        self,
        entity_type: str,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        group_by: str | Omit = omit,
        order_by: Literal["key", "total_quantity", "event_count"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        limit: int | Omit = omit,
        filters: usage_retrieve_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> UsageRetrieveResponse:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "group_by": group_by,
                "order_by": order_by,
                "order_direction": order_direction,
                "limit": limit,
                "filters": filters,
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
            build_path(
                "/api/v3.1/org/usage/{entity_type}",
                {"entity_type": entity_type},
            ),
            cast_to=UsageRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            body=body_data,
            body_model=OrgUsageRetrieveBody,
            options=options_data,
        )

    def retrieve_summary(
        self,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        entity_types: SequenceNotStr[str] | Omit = omit,
        filters: usage_retrieve_summary_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> UsageRetrieveSummaryResponse:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "entity_types": entity_types,
                "filters": filters,
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
            "/api/v3.1/org/usage/summary",
            cast_to=UsageRetrieveSummaryResponse,
            operation=_RETRIEVE_SUMMARY_OPERATION,
            body=body_data,
            body_model=OrgUsageRetrieveSummaryBody,
            options=options_data,
        )


class AsyncUsageResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUsageResourceWithRawResponse:
        return AsyncUsageResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsageResourceWithStreamingResponse:
        return AsyncUsageResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        entity_type: str,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        group_by: str | Omit = omit,
        order_by: Literal["key", "total_quantity", "event_count"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        limit: int | Omit = omit,
        filters: usage_retrieve_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> UsageRetrieveResponse:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "group_by": group_by,
                "order_by": order_by,
                "order_direction": order_direction,
                "limit": limit,
                "filters": filters,
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
            build_path(
                "/api/v3.1/org/usage/{entity_type}",
                {"entity_type": entity_type},
            ),
            cast_to=UsageRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            body=body_data,
            body_model=OrgUsageRetrieveBody,
            options=options_data,
        )

    async def retrieve_summary(
        self,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        entity_types: SequenceNotStr[str] | Omit = omit,
        filters: usage_retrieve_summary_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> UsageRetrieveSummaryResponse:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "entity_types": entity_types,
                "filters": filters,
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
            "/api/v3.1/org/usage/summary",
            cast_to=UsageRetrieveSummaryResponse,
            operation=_RETRIEVE_SUMMARY_OPERATION,
            body=body_data,
            body_model=OrgUsageRetrieveSummaryBody,
            options=options_data,
        )


class UsageResourceWithRawResponse:
    def __init__(self, resource: UsageResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        entity_type: str,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        group_by: str | Omit = omit,
        order_by: Literal["key", "total_quantity", "event_count"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        limit: int | Omit = omit,
        filters: usage_retrieve_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[UsageRetrieveResponse]:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "group_by": group_by,
                "order_by": order_by,
                "order_direction": order_direction,
                "limit": limit,
                "filters": filters,
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
            build_path(
                "/api/v3.1/org/usage/{entity_type}",
                {"entity_type": entity_type},
            ),
            cast_to=UsageRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            body=body_data,
            body_model=OrgUsageRetrieveBody,
            options=options_data,
        )

    def retrieve_summary(
        self,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        entity_types: SequenceNotStr[str] | Omit = omit,
        filters: usage_retrieve_summary_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[UsageRetrieveSummaryResponse]:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "entity_types": entity_types,
                "filters": filters,
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
            "/api/v3.1/org/usage/summary",
            cast_to=UsageRetrieveSummaryResponse,
            operation=_RETRIEVE_SUMMARY_OPERATION,
            body=body_data,
            body_model=OrgUsageRetrieveSummaryBody,
            options=options_data,
        )


class AsyncUsageResourceWithRawResponse:
    def __init__(self, resource: AsyncUsageResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def retrieve(
        self,
        entity_type: str,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        group_by: str | Omit = omit,
        order_by: Literal["key", "total_quantity", "event_count"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        limit: int | Omit = omit,
        filters: usage_retrieve_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[UsageRetrieveResponse]:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "group_by": group_by,
                "order_by": order_by,
                "order_direction": order_direction,
                "limit": limit,
                "filters": filters,
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
            build_path(
                "/api/v3.1/org/usage/{entity_type}",
                {"entity_type": entity_type},
            ),
            cast_to=UsageRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            body=body_data,
            body_model=OrgUsageRetrieveBody,
            options=options_data,
        )

    async def retrieve_summary(
        self,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        entity_types: SequenceNotStr[str] | Omit = omit,
        filters: usage_retrieve_summary_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[UsageRetrieveSummaryResponse]:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "entity_types": entity_types,
                "filters": filters,
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
            "/api/v3.1/org/usage/summary",
            cast_to=UsageRetrieveSummaryResponse,
            operation=_RETRIEVE_SUMMARY_OPERATION,
            body=body_data,
            body_model=OrgUsageRetrieveSummaryBody,
            options=options_data,
        )


class UsageResourceWithStreamingResponse:
    def __init__(self, resource: UsageResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        entity_type: str,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        group_by: str | Omit = omit,
        order_by: Literal["key", "total_quantity", "event_count"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        limit: int | Omit = omit,
        filters: usage_retrieve_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[UsageRetrieveResponse]]:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "group_by": group_by,
                "order_by": order_by,
                "order_direction": order_direction,
                "limit": limit,
                "filters": filters,
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
                build_path(
                    "/api/v3.1/org/usage/{entity_type}",
                    {"entity_type": entity_type},
                ),
                cast_to=UsageRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                body=body_data,
                body_model=OrgUsageRetrieveBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_summary(
        self,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        entity_types: SequenceNotStr[str] | Omit = omit,
        filters: usage_retrieve_summary_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[UsageRetrieveSummaryResponse]]:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "entity_types": entity_types,
                "filters": filters,
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
                "/api/v3.1/org/usage/summary",
                cast_to=UsageRetrieveSummaryResponse,
                operation=_RETRIEVE_SUMMARY_OPERATION,
                body=body_data,
                body_model=OrgUsageRetrieveSummaryBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncUsageResourceWithStreamingResponse:
    def __init__(self, resource: AsyncUsageResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        entity_type: str,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        group_by: str | Omit = omit,
        order_by: Literal["key", "total_quantity", "event_count"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        limit: int | Omit = omit,
        filters: usage_retrieve_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[UsageRetrieveResponse]]:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "group_by": group_by,
                "order_by": order_by,
                "order_direction": order_direction,
                "limit": limit,
                "filters": filters,
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
                build_path(
                    "/api/v3.1/org/usage/{entity_type}",
                    {"entity_type": entity_type},
                ),
                cast_to=UsageRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                body=body_data,
                body_model=OrgUsageRetrieveBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_summary(
        self,
        body: BodyParam | None = None,
        *,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        entity_types: SequenceNotStr[str] | Omit = omit,
        filters: usage_retrieve_summary_params.Filters | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[UsageRetrieveSummaryResponse]]:
        body_fields = compact(
            {
                "from": from_,
                "to": to,
                "entity_types": entity_types,
                "filters": filters,
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
                "/api/v3.1/org/usage/summary",
                cast_to=UsageRetrieveSummaryResponse,
                operation=_RETRIEVE_SUMMARY_OPERATION,
                body=body_data,
                body_model=OrgUsageRetrieveSummaryBody,
                options=options_data,
                stream=True,
            )
        )
