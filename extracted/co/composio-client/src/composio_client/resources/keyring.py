# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.keyring`` — the generated resource classes.

``KeyringResource`` (sync) and ``AsyncKeyringResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx

from .._base_client import RequestOptions
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Query
from ..types.keyring_list_transfer_keys_response import KeyringListTransferKeysResponse
from ._base import AsyncAPIResource, SyncAPIResource, make_request_options

_LIST_TRANSFER_KEYS_OPERATION = OPERATIONS_BY_CHAIN[("keyring", "list_transfer_keys")]


class KeyringResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> KeyringResourceWithRawResponse:
        return KeyringResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> KeyringResourceWithStreamingResponse:
        return KeyringResourceWithStreamingResponse(self)

    def list_transfer_keys(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> KeyringListTransferKeysResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/keyring/transfer_keys",
            cast_to=KeyringListTransferKeysResponse,
            operation=_LIST_TRANSFER_KEYS_OPERATION,
            options=options_data,
        )


class AsyncKeyringResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncKeyringResourceWithRawResponse:
        return AsyncKeyringResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncKeyringResourceWithStreamingResponse:
        return AsyncKeyringResourceWithStreamingResponse(self)

    async def list_transfer_keys(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> KeyringListTransferKeysResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/keyring/transfer_keys",
            cast_to=KeyringListTransferKeysResponse,
            operation=_LIST_TRANSFER_KEYS_OPERATION,
            options=options_data,
        )


class KeyringResourceWithRawResponse:
    def __init__(self, resource: KeyringResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list_transfer_keys(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[KeyringListTransferKeysResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/keyring/transfer_keys",
            cast_to=KeyringListTransferKeysResponse,
            operation=_LIST_TRANSFER_KEYS_OPERATION,
            options=options_data,
        )


class AsyncKeyringResourceWithRawResponse:
    def __init__(self, resource: AsyncKeyringResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def list_transfer_keys(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[KeyringListTransferKeysResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/keyring/transfer_keys",
            cast_to=KeyringListTransferKeysResponse,
            operation=_LIST_TRANSFER_KEYS_OPERATION,
            options=options_data,
        )


class KeyringResourceWithStreamingResponse:
    def __init__(self, resource: KeyringResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list_transfer_keys(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[KeyringListTransferKeysResponse]]:
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
                "/api/v3.1/keyring/transfer_keys",
                cast_to=KeyringListTransferKeysResponse,
                operation=_LIST_TRANSFER_KEYS_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncKeyringResourceWithStreamingResponse:
    def __init__(self, resource: AsyncKeyringResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list_transfer_keys(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[KeyringListTransferKeysResponse]]:
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
                "/api/v3.1/keyring/transfer_keys",
                cast_to=KeyringListTransferKeysResponse,
                operation=_LIST_TRANSFER_KEYS_OPERATION,
                options=options_data,
                stream=True,
            )
        )
