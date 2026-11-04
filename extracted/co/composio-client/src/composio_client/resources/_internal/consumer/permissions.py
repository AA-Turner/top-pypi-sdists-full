# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.consumer.permissions`` — the generated resource classes.

``PermissionsResource`` (sync) and ``AsyncPermissionsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import Literal

import httpx

from ...._base_client import BodyParam, RequestOptions
from ...._models import PermissionsResolveBody
from ...._operations import OPERATIONS_BY_CHAIN
from ...._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ....types.consumer.permissions_resolve_response import PermissionsResolveResponse
from ..._base import AsyncAPIResource, SyncAPIResource, compact, make_request_options, merge_body

_RESOLVE_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "consumer", "permissions", "resolve")]


class PermissionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PermissionsResourceWithRawResponse:
        return PermissionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PermissionsResourceWithStreamingResponse:
        return PermissionsResourceWithStreamingResponse(self)

    def resolve(
        self,
        body: BodyParam | None = None,
        *,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        default: Literal["allow_all", "ask_every_call", "ask_once_per_session"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> PermissionsResolveResponse:
        body_fields = compact(
            {
                "connected_account_ids": connected_account_ids,
                "connected_accounts": connected_accounts,
                "default": default,
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
            "/api/v3.1/consumer/permissions/resolve",
            cast_to=PermissionsResolveResponse,
            operation=_RESOLVE_OPERATION,
            body=body_data,
            body_model=PermissionsResolveBody,
            options=options_data,
        )


class AsyncPermissionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPermissionsResourceWithRawResponse:
        return AsyncPermissionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPermissionsResourceWithStreamingResponse:
        return AsyncPermissionsResourceWithStreamingResponse(self)

    async def resolve(
        self,
        body: BodyParam | None = None,
        *,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        default: Literal["allow_all", "ask_every_call", "ask_once_per_session"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> PermissionsResolveResponse:
        body_fields = compact(
            {
                "connected_account_ids": connected_account_ids,
                "connected_accounts": connected_accounts,
                "default": default,
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
            "/api/v3.1/consumer/permissions/resolve",
            cast_to=PermissionsResolveResponse,
            operation=_RESOLVE_OPERATION,
            body=body_data,
            body_model=PermissionsResolveBody,
            options=options_data,
        )


class PermissionsResourceWithRawResponse:
    def __init__(self, resource: PermissionsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def resolve(
        self,
        body: BodyParam | None = None,
        *,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        default: Literal["allow_all", "ask_every_call", "ask_once_per_session"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[PermissionsResolveResponse]:
        body_fields = compact(
            {
                "connected_account_ids": connected_account_ids,
                "connected_accounts": connected_accounts,
                "default": default,
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
            "/api/v3.1/consumer/permissions/resolve",
            cast_to=PermissionsResolveResponse,
            operation=_RESOLVE_OPERATION,
            body=body_data,
            body_model=PermissionsResolveBody,
            options=options_data,
        )


class AsyncPermissionsResourceWithRawResponse:
    def __init__(self, resource: AsyncPermissionsResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def resolve(
        self,
        body: BodyParam | None = None,
        *,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        default: Literal["allow_all", "ask_every_call", "ask_once_per_session"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[PermissionsResolveResponse]:
        body_fields = compact(
            {
                "connected_account_ids": connected_account_ids,
                "connected_accounts": connected_accounts,
                "default": default,
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
            "/api/v3.1/consumer/permissions/resolve",
            cast_to=PermissionsResolveResponse,
            operation=_RESOLVE_OPERATION,
            body=body_data,
            body_model=PermissionsResolveBody,
            options=options_data,
        )


class PermissionsResourceWithStreamingResponse:
    def __init__(self, resource: PermissionsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def resolve(
        self,
        body: BodyParam | None = None,
        *,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        default: Literal["allow_all", "ask_every_call", "ask_once_per_session"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[PermissionsResolveResponse]]:
        body_fields = compact(
            {
                "connected_account_ids": connected_account_ids,
                "connected_accounts": connected_accounts,
                "default": default,
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
                "/api/v3.1/consumer/permissions/resolve",
                cast_to=PermissionsResolveResponse,
                operation=_RESOLVE_OPERATION,
                body=body_data,
                body_model=PermissionsResolveBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncPermissionsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncPermissionsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def resolve(
        self,
        body: BodyParam | None = None,
        *,
        connected_account_ids: SequenceNotStr[str] | Omit = omit,
        connected_accounts: dict[str, SequenceNotStr[str]] | Omit = omit,
        default: Literal["allow_all", "ask_every_call", "ask_once_per_session"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[PermissionsResolveResponse]]:
        body_fields = compact(
            {
                "connected_account_ids": connected_account_ids,
                "connected_accounts": connected_accounts,
                "default": default,
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
                "/api/v3.1/consumer/permissions/resolve",
                cast_to=PermissionsResolveResponse,
                operation=_RESOLVE_OPERATION,
                body=body_data,
                body_model=PermissionsResolveBody,
                options=options_data,
                stream=True,
            )
        )
