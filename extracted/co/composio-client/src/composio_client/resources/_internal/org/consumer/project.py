# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.org.consumer.project`` — the generated resource classes.

``ProjectResource`` (sync) and ``AsyncProjectResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from ....._base_client import HeaderParam, RequestOptions
from ....._operations import OPERATIONS_BY_CHAIN
from ....._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ....._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from .....types.org.consumer.project_resolve_response import ProjectResolveResponse
from ...._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_mapping,
    require_fields,
)

_RESOLVE_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "org", "consumer", "project", "resolve")]


class ProjectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProjectResourceWithRawResponse:
        return ProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectResourceWithStreamingResponse:
        return ProjectResourceWithStreamingResponse(self)

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    def resolve(
        self,
        *,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectResolveResponse: ...

    @overload
    def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ProjectResolveResponse: ...

    def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectResolveResponse:
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "post",
            "/api/v3.1/org/consumer/project/resolve",
            cast_to=ProjectResolveResponse,
            operation=_RESOLVE_OPERATION,
            operation_headers=headers_data,
            options=options_data,
        )


class AsyncProjectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProjectResourceWithRawResponse:
        return AsyncProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectResourceWithStreamingResponse:
        return AsyncProjectResourceWithStreamingResponse(self)

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    async def resolve(
        self,
        *,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectResolveResponse: ...

    @overload
    async def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ProjectResolveResponse: ...

    async def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectResolveResponse:
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "post",
            "/api/v3.1/org/consumer/project/resolve",
            cast_to=ProjectResolveResponse,
            operation=_RESOLVE_OPERATION,
            operation_headers=headers_data,
            options=options_data,
        )


class ProjectResourceWithRawResponse:
    def __init__(self, resource: ProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    def resolve(
        self,
        *,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectResolveResponse]: ...

    @overload
    def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectResolveResponse]: ...

    def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectResolveResponse]:
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "post",
            "/api/v3.1/org/consumer/project/resolve",
            cast_to=ProjectResolveResponse,
            operation=_RESOLVE_OPERATION,
            operation_headers=headers_data,
            options=options_data,
        )


class AsyncProjectResourceWithRawResponse:
    def __init__(self, resource: AsyncProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    async def resolve(
        self,
        *,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectResolveResponse]: ...

    @overload
    async def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectResolveResponse]: ...

    async def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectResolveResponse]:
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "post",
            "/api/v3.1/org/consumer/project/resolve",
            cast_to=ProjectResolveResponse,
            operation=_RESOLVE_OPERATION,
            operation_headers=headers_data,
            options=options_data,
        )


class ProjectResourceWithStreamingResponse:
    def __init__(self, resource: ProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    def resolve(
        self,
        *,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectResolveResponse]]: ...

    @overload
    def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectResolveResponse]]: ...

    def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectResolveResponse]]:
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
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
                "/api/v3.1/org/consumer/project/resolve",
                cast_to=ProjectResolveResponse,
                operation=_RESOLVE_OPERATION,
                operation_headers=headers_data,
                options=options_data,
                stream=True,
            )
        )


class AsyncProjectResourceWithStreamingResponse:
    def __init__(self, resource: AsyncProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    def resolve(
        self,
        *,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectResolveResponse]]: ...

    @overload
    def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectResolveResponse]]: ...

    def resolve(
        self,
        *,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectResolveResponse]]:
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
        )
        headers_data = merge_mapping(headers, header_fields)
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
                "/api/v3.1/org/consumer/project/resolve",
                cast_to=ProjectResolveResponse,
                operation=_RESOLVE_OPERATION,
                operation_headers=headers_data,
                options=options_data,
                stream=True,
            )
        )
