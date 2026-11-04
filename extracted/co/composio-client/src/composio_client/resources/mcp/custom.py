# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.mcp.custom`` — the generated resource classes.

``CustomResource`` (sync) and ``AsyncCustomResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from ..._base_client import BodyParam, RequestOptions
from ..._models import CustomCreateBody
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ...types.mcp.custom_create_response import CustomCreateResponse
from .._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_body,
    require_fields,
)

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "custom", "create")]


class CustomResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CustomResourceWithRawResponse:
        return CustomResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomResourceWithStreamingResponse:
        return CustomResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateResponse:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "custom_tools": custom_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
            "/api/v3.1/mcp/servers/custom",
            cast_to=CustomCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=CustomCreateBody,
            options=options_data,
        )


class AsyncCustomResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCustomResourceWithRawResponse:
        return AsyncCustomResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomResourceWithStreamingResponse:
        return AsyncCustomResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateResponse:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "custom_tools": custom_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
            "/api/v3.1/mcp/servers/custom",
            cast_to=CustomCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=CustomCreateBody,
            options=options_data,
        )


class CustomResourceWithRawResponse:
    def __init__(self, resource: CustomResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomCreateResponse]:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "custom_tools": custom_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
            "/api/v3.1/mcp/servers/custom",
            cast_to=CustomCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=CustomCreateBody,
            options=options_data,
        )


class AsyncCustomResourceWithRawResponse:
    def __init__(self, resource: AsyncCustomResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomCreateResponse]:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "custom_tools": custom_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
            "/api/v3.1/mcp/servers/custom",
            cast_to=CustomCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=CustomCreateBody,
            options=options_data,
        )


class CustomResourceWithStreamingResponse:
    def __init__(self, resource: CustomResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomCreateResponse]]:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "custom_tools": custom_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
                "/api/v3.1/mcp/servers/custom",
                cast_to=CustomCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=CustomCreateBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncCustomResourceWithStreamingResponse:
    def __init__(self, resource: AsyncCustomResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        custom_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomCreateResponse]]:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "custom_tools": custom_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
                "/api/v3.1/mcp/servers/custom",
                cast_to=CustomCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=CustomCreateBody,
                options=options_data,
                stream=True,
            )
        )
