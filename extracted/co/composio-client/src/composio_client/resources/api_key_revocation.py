# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.api_key_revocation`` — the generated resource classes.

``ApiKeyRevocationResource`` (sync) and ``AsyncApiKeyRevocationResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, RequestOptions
from .._models import ApiKeyRevocationCreateBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ..types.api_key_revocation_create_response import ApiKeyRevocationCreateResponse
from ._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_body,
    require_fields,
)

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("api_key_revocation", "create")]


class ApiKeyRevocationResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApiKeyRevocationResourceWithRawResponse:
        return ApiKeyRevocationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApiKeyRevocationResourceWithStreamingResponse:
        return ApiKeyRevocationResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ApiKeyRevocationCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ApiKeyRevocationCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ApiKeyRevocationCreateResponse:
        body_fields = compact(
            {
                "api_keys": api_keys,
            }
        )
        require_fields(
            body,
            body_fields,
            ("api_keys",),
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
            "/api/v3.1/api_key_revocation",
            cast_to=ApiKeyRevocationCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ApiKeyRevocationCreateBody,
            options=options_data,
        )


class AsyncApiKeyRevocationResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApiKeyRevocationResourceWithRawResponse:
        return AsyncApiKeyRevocationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApiKeyRevocationResourceWithStreamingResponse:
        return AsyncApiKeyRevocationResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ApiKeyRevocationCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ApiKeyRevocationCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ApiKeyRevocationCreateResponse:
        body_fields = compact(
            {
                "api_keys": api_keys,
            }
        )
        require_fields(
            body,
            body_fields,
            ("api_keys",),
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
            "/api/v3.1/api_key_revocation",
            cast_to=ApiKeyRevocationCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ApiKeyRevocationCreateBody,
            options=options_data,
        )


class ApiKeyRevocationResourceWithRawResponse:
    def __init__(self, resource: ApiKeyRevocationResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ApiKeyRevocationCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ApiKeyRevocationCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ApiKeyRevocationCreateResponse]:
        body_fields = compact(
            {
                "api_keys": api_keys,
            }
        )
        require_fields(
            body,
            body_fields,
            ("api_keys",),
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
            "/api/v3.1/api_key_revocation",
            cast_to=ApiKeyRevocationCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ApiKeyRevocationCreateBody,
            options=options_data,
        )


class AsyncApiKeyRevocationResourceWithRawResponse:
    def __init__(self, resource: AsyncApiKeyRevocationResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ApiKeyRevocationCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ApiKeyRevocationCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ApiKeyRevocationCreateResponse]:
        body_fields = compact(
            {
                "api_keys": api_keys,
            }
        )
        require_fields(
            body,
            body_fields,
            ("api_keys",),
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
            "/api/v3.1/api_key_revocation",
            cast_to=ApiKeyRevocationCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ApiKeyRevocationCreateBody,
            options=options_data,
        )


class ApiKeyRevocationResourceWithStreamingResponse:
    def __init__(self, resource: ApiKeyRevocationResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ApiKeyRevocationCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ApiKeyRevocationCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ApiKeyRevocationCreateResponse]]:
        body_fields = compact(
            {
                "api_keys": api_keys,
            }
        )
        require_fields(
            body,
            body_fields,
            ("api_keys",),
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
                "/api/v3.1/api_key_revocation",
                cast_to=ApiKeyRevocationCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=ApiKeyRevocationCreateBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncApiKeyRevocationResourceWithStreamingResponse:
    def __init__(self, resource: AsyncApiKeyRevocationResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str],
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ApiKeyRevocationCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ApiKeyRevocationCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        api_keys: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ApiKeyRevocationCreateResponse]]:
        body_fields = compact(
            {
                "api_keys": api_keys,
            }
        )
        require_fields(
            body,
            body_fields,
            ("api_keys",),
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
                "/api/v3.1/api_key_revocation",
                cast_to=ApiKeyRevocationCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=ApiKeyRevocationCreateBody,
                options=options_data,
                stream=True,
            )
        )
