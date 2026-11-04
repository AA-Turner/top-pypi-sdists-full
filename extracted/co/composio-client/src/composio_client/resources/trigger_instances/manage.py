# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.trigger_instances.manage`` — the generated resource classes.

``ManageResource`` (sync) and ``AsyncManageResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import Literal

import httpx

from ..._base_client import BodyParam, RequestOptions
from ..._models import ManageUpdateBody
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ...types.trigger_instances.manage_delete_response import ManageDeleteResponse
from ...types.trigger_instances.manage_update_response import ManageUpdateResponse
from .._base import AsyncAPIResource, SyncAPIResource, build_path, compact, make_request_options, merge_body

_UPDATE_OPERATION = OPERATIONS_BY_CHAIN[("trigger_instances", "manage", "update")]
_DELETE_OPERATION = OPERATIONS_BY_CHAIN[("trigger_instances", "manage", "delete")]


class ManageResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ManageResourceWithRawResponse:
        return ManageResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ManageResourceWithStreamingResponse:
        return ManageResourceWithStreamingResponse(self)

    def update(
        self,
        trigger_id: str,
        body: BodyParam | None = None,
        *,
        status: Literal["enable", "disable"] | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ManageUpdateResponse:
        body_fields = compact(
            {
                "status": status,
                "user_id": user_id,
                "egress_url": egress_url,
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
                "/api/v3.1/trigger_instances/manage/{triggerId}",
                {"triggerId": trigger_id},
            ),
            cast_to=ManageUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=ManageUpdateBody,
            options=options_data,
        )

    def delete(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ManageDeleteResponse:
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
                "/api/v3.1/trigger_instances/manage/{triggerId}",
                {"triggerId": trigger_id},
            ),
            cast_to=ManageDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )


class AsyncManageResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncManageResourceWithRawResponse:
        return AsyncManageResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncManageResourceWithStreamingResponse:
        return AsyncManageResourceWithStreamingResponse(self)

    async def update(
        self,
        trigger_id: str,
        body: BodyParam | None = None,
        *,
        status: Literal["enable", "disable"] | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ManageUpdateResponse:
        body_fields = compact(
            {
                "status": status,
                "user_id": user_id,
                "egress_url": egress_url,
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
                "/api/v3.1/trigger_instances/manage/{triggerId}",
                {"triggerId": trigger_id},
            ),
            cast_to=ManageUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=ManageUpdateBody,
            options=options_data,
        )

    async def delete(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ManageDeleteResponse:
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
                "/api/v3.1/trigger_instances/manage/{triggerId}",
                {"triggerId": trigger_id},
            ),
            cast_to=ManageDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )


class ManageResourceWithRawResponse:
    def __init__(self, resource: ManageResource) -> None:
        self._resource = resource
        self._client = resource._client

    def update(
        self,
        trigger_id: str,
        body: BodyParam | None = None,
        *,
        status: Literal["enable", "disable"] | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ManageUpdateResponse]:
        body_fields = compact(
            {
                "status": status,
                "user_id": user_id,
                "egress_url": egress_url,
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
                "/api/v3.1/trigger_instances/manage/{triggerId}",
                {"triggerId": trigger_id},
            ),
            cast_to=ManageUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=ManageUpdateBody,
            options=options_data,
        )

    def delete(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ManageDeleteResponse]:
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
                "/api/v3.1/trigger_instances/manage/{triggerId}",
                {"triggerId": trigger_id},
            ),
            cast_to=ManageDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )


class AsyncManageResourceWithRawResponse:
    def __init__(self, resource: AsyncManageResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def update(
        self,
        trigger_id: str,
        body: BodyParam | None = None,
        *,
        status: Literal["enable", "disable"] | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ManageUpdateResponse]:
        body_fields = compact(
            {
                "status": status,
                "user_id": user_id,
                "egress_url": egress_url,
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
                "/api/v3.1/trigger_instances/manage/{triggerId}",
                {"triggerId": trigger_id},
            ),
            cast_to=ManageUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=ManageUpdateBody,
            options=options_data,
        )

    async def delete(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ManageDeleteResponse]:
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
                "/api/v3.1/trigger_instances/manage/{triggerId}",
                {"triggerId": trigger_id},
            ),
            cast_to=ManageDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )


class ManageResourceWithStreamingResponse:
    def __init__(self, resource: ManageResource) -> None:
        self._resource = resource
        self._client = resource._client

    def update(
        self,
        trigger_id: str,
        body: BodyParam | None = None,
        *,
        status: Literal["enable", "disable"] | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ManageUpdateResponse]]:
        body_fields = compact(
            {
                "status": status,
                "user_id": user_id,
                "egress_url": egress_url,
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
                    "/api/v3.1/trigger_instances/manage/{triggerId}",
                    {"triggerId": trigger_id},
                ),
                cast_to=ManageUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=ManageUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ManageDeleteResponse]]:
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
                    "/api/v3.1/trigger_instances/manage/{triggerId}",
                    {"triggerId": trigger_id},
                ),
                cast_to=ManageDeleteResponse,
                operation=_DELETE_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncManageResourceWithStreamingResponse:
    def __init__(self, resource: AsyncManageResource) -> None:
        self._resource = resource
        self._client = resource._client

    def update(
        self,
        trigger_id: str,
        body: BodyParam | None = None,
        *,
        status: Literal["enable", "disable"] | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ManageUpdateResponse]]:
        body_fields = compact(
            {
                "status": status,
                "user_id": user_id,
                "egress_url": egress_url,
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
                    "/api/v3.1/trigger_instances/manage/{triggerId}",
                    {"triggerId": trigger_id},
                ),
                cast_to=ManageUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=ManageUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        trigger_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ManageDeleteResponse]]:
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
                    "/api/v3.1/trigger_instances/manage/{triggerId}",
                    {"triggerId": trigger_id},
                ),
                cast_to=ManageDeleteResponse,
                operation=_DELETE_OPERATION,
                options=options_data,
                stream=True,
            )
        )
