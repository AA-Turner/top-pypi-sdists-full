# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.mcp.generate`` — the generated resource classes.

``GenerateResource`` (sync) and ``AsyncGenerateResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from ..._base_client import BodyParam, RequestOptions
from ..._models import GenerateURLBody
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ...types.mcp.generate_url_response import GenerateURLResponse
from .._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_body,
    require_fields,
)

_URL_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "generate", "url")]


class GenerateResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GenerateResourceWithRawResponse:
        return GenerateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GenerateResourceWithStreamingResponse:
        return GenerateResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    @overload
    def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> GenerateURLResponse: ...

    @overload
    def url(
        self,
        body: BodyParam,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> GenerateURLResponse: ...

    def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> GenerateURLResponse:
        body_fields = compact(
            {
                "mcp_server_id": mcp_server_id,
                "managed_auth_by_composio": managed_auth_by_composio,
                "user_ids": user_ids,
                "connected_account_ids": connected_account_ids,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mcp_server_id",),
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
            "/api/v3.1/mcp/servers/generate",
            cast_to=GenerateURLResponse,
            operation=_URL_OPERATION,
            body=body_data,
            body_model=GenerateURLBody,
            options=options_data,
        )


class AsyncGenerateResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGenerateResourceWithRawResponse:
        return AsyncGenerateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGenerateResourceWithStreamingResponse:
        return AsyncGenerateResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    @overload
    async def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> GenerateURLResponse: ...

    @overload
    async def url(
        self,
        body: BodyParam,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> GenerateURLResponse: ...

    async def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> GenerateURLResponse:
        body_fields = compact(
            {
                "mcp_server_id": mcp_server_id,
                "managed_auth_by_composio": managed_auth_by_composio,
                "user_ids": user_ids,
                "connected_account_ids": connected_account_ids,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mcp_server_id",),
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
            "/api/v3.1/mcp/servers/generate",
            cast_to=GenerateURLResponse,
            operation=_URL_OPERATION,
            body=body_data,
            body_model=GenerateURLBody,
            options=options_data,
        )


class GenerateResourceWithRawResponse:
    def __init__(self, resource: GenerateResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[GenerateURLResponse]: ...

    @overload
    def url(
        self,
        body: BodyParam,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[GenerateURLResponse]: ...

    def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[GenerateURLResponse]:
        body_fields = compact(
            {
                "mcp_server_id": mcp_server_id,
                "managed_auth_by_composio": managed_auth_by_composio,
                "user_ids": user_ids,
                "connected_account_ids": connected_account_ids,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mcp_server_id",),
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
            "/api/v3.1/mcp/servers/generate",
            cast_to=GenerateURLResponse,
            operation=_URL_OPERATION,
            body=body_data,
            body_model=GenerateURLBody,
            options=options_data,
        )


class AsyncGenerateResourceWithRawResponse:
    def __init__(self, resource: AsyncGenerateResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    async def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[GenerateURLResponse]: ...

    @overload
    async def url(
        self,
        body: BodyParam,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[GenerateURLResponse]: ...

    async def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[GenerateURLResponse]:
        body_fields = compact(
            {
                "mcp_server_id": mcp_server_id,
                "managed_auth_by_composio": managed_auth_by_composio,
                "user_ids": user_ids,
                "connected_account_ids": connected_account_ids,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mcp_server_id",),
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
            "/api/v3.1/mcp/servers/generate",
            cast_to=GenerateURLResponse,
            operation=_URL_OPERATION,
            body=body_data,
            body_model=GenerateURLBody,
            options=options_data,
        )


class GenerateResourceWithStreamingResponse:
    def __init__(self, resource: GenerateResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[GenerateURLResponse]]: ...

    @overload
    def url(
        self,
        body: BodyParam,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[GenerateURLResponse]]: ...

    def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[GenerateURLResponse]]:
        body_fields = compact(
            {
                "mcp_server_id": mcp_server_id,
                "managed_auth_by_composio": managed_auth_by_composio,
                "user_ids": user_ids,
                "connected_account_ids": connected_account_ids,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mcp_server_id",),
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
                "/api/v3.1/mcp/servers/generate",
                cast_to=GenerateURLResponse,
                operation=_URL_OPERATION,
                body=body_data,
                body_model=GenerateURLBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncGenerateResourceWithStreamingResponse:
    def __init__(self, resource: AsyncGenerateResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[GenerateURLResponse]]: ...

    @overload
    def url(
        self,
        body: BodyParam,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[GenerateURLResponse]]: ...

    def url(
        self,
        body: BodyParam | None = None,
        *,
        mcp_server_id: str | Omit = omit,
        managed_auth_by_composio: bool | Omit = omit,
        user_ids: SequenceNotStr[str] | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[GenerateURLResponse]]:
        body_fields = compact(
            {
                "mcp_server_id": mcp_server_id,
                "managed_auth_by_composio": managed_auth_by_composio,
                "user_ids": user_ids,
                "connected_account_ids": connected_account_ids,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mcp_server_id",),
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
                "/api/v3.1/mcp/servers/generate",
                cast_to=GenerateURLResponse,
                operation=_URL_OPERATION,
                body=body_data,
                body_model=GenerateURLBody,
                options=options_data,
                stream=True,
            )
        )
