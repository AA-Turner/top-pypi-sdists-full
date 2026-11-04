# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.logs.tools`` — the generated resource classes.

``ToolsResource`` (sync) and ``AsyncToolsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import cached_property

import httpx
from typing_extensions import overload

from ...._base_client import BodyParam, RequestOptions
from ...._models import LogsToolListBody
from ...._operations import OPERATIONS_BY_CHAIN
from ...._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ....types.logs import tool_list_params
from ....types.logs.tool_list_fields_response import ToolListFieldsResponse
from ....types.logs.tool_list_response import ToolListResponse
from ....types.logs.tool_retrieve_response import ToolRetrieveResponse
from ..._base import (
    AsyncAPIResource,
    SyncAPIResource,
    build_path,
    compact,
    make_request_options,
    merge_body,
    require_fields,
)

_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "logs", "tools", "retrieve")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "logs", "tools", "list")]
_LIST_FIELDS_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "logs", "tools", "list_fields")]


class ToolsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ToolsResourceWithRawResponse:
        return ToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ToolsResourceWithStreamingResponse:
        return ToolsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveResponse:
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
                "/api/v3.1/internal/action_execution/log/{id}",
                {"id": id},
            ),
            cast_to=ToolRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse: ...

    @overload
    def list(
        self,
        body: BodyParam,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse: ...

    def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse:
        body_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "case_sensitive": case_sensitive,
                "from": from_,
                "to": to,
                "search_params": search_params,
            }
        )
        require_fields(
            body,
            body_fields,
            ("cursor",),
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
            "/api/v3.1/internal/action_execution/logs",
            cast_to=ToolListResponse,
            operation=_LIST_OPERATION,
            body=body_data,
            body_model=LogsToolListBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def list_fields(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListFieldsResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/internal/action_execution/fields",
            cast_to=ToolListFieldsResponse,
            operation=_LIST_FIELDS_OPERATION,
            options=options_data,
        )


class AsyncToolsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncToolsResourceWithRawResponse:
        return AsyncToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncToolsResourceWithStreamingResponse:
        return AsyncToolsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveResponse:
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
                "/api/v3.1/internal/action_execution/log/{id}",
                {"id": id},
            ),
            cast_to=ToolRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse: ...

    @overload
    async def list(
        self,
        body: BodyParam,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse: ...

    async def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse:
        body_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "case_sensitive": case_sensitive,
                "from": from_,
                "to": to,
                "search_params": search_params,
            }
        )
        require_fields(
            body,
            body_fields,
            ("cursor",),
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
            "/api/v3.1/internal/action_execution/logs",
            cast_to=ToolListResponse,
            operation=_LIST_OPERATION,
            body=body_data,
            body_model=LogsToolListBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def list_fields(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListFieldsResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/internal/action_execution/fields",
            cast_to=ToolListFieldsResponse,
            operation=_LIST_FIELDS_OPERATION,
            options=options_data,
        )


class ToolsResourceWithRawResponse:
    def __init__(self, resource: ToolsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolRetrieveResponse]:
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
                "/api/v3.1/internal/action_execution/log/{id}",
                {"id": id},
            ),
            cast_to=ToolRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolListResponse]: ...

    @overload
    def list(
        self,
        body: BodyParam,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolListResponse]: ...

    def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolListResponse]:
        body_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "case_sensitive": case_sensitive,
                "from": from_,
                "to": to,
                "search_params": search_params,
            }
        )
        require_fields(
            body,
            body_fields,
            ("cursor",),
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
            "/api/v3.1/internal/action_execution/logs",
            cast_to=ToolListResponse,
            operation=_LIST_OPERATION,
            body=body_data,
            body_model=LogsToolListBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def list_fields(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolListFieldsResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/internal/action_execution/fields",
            cast_to=ToolListFieldsResponse,
            operation=_LIST_FIELDS_OPERATION,
            options=options_data,
        )


class AsyncToolsResourceWithRawResponse:
    def __init__(self, resource: AsyncToolsResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolRetrieveResponse]:
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
                "/api/v3.1/internal/action_execution/log/{id}",
                {"id": id},
            ),
            cast_to=ToolRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolListResponse]: ...

    @overload
    async def list(
        self,
        body: BodyParam,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolListResponse]: ...

    async def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolListResponse]:
        body_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "case_sensitive": case_sensitive,
                "from": from_,
                "to": to,
                "search_params": search_params,
            }
        )
        require_fields(
            body,
            body_fields,
            ("cursor",),
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
            "/api/v3.1/internal/action_execution/logs",
            cast_to=ToolListResponse,
            operation=_LIST_OPERATION,
            body=body_data,
            body_model=LogsToolListBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def list_fields(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolListFieldsResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/internal/action_execution/fields",
            cast_to=ToolListFieldsResponse,
            operation=_LIST_FIELDS_OPERATION,
            options=options_data,
        )


class ToolsResourceWithStreamingResponse:
    def __init__(self, resource: ToolsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolRetrieveResponse]]:
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
                    "/api/v3.1/internal/action_execution/log/{id}",
                    {"id": id},
                ),
                cast_to=ToolRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolListResponse]]: ...

    @overload
    def list(
        self,
        body: BodyParam,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolListResponse]]: ...

    def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolListResponse]]:
        body_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "case_sensitive": case_sensitive,
                "from": from_,
                "to": to,
                "search_params": search_params,
            }
        )
        require_fields(
            body,
            body_fields,
            ("cursor",),
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
                "/api/v3.1/internal/action_execution/logs",
                cast_to=ToolListResponse,
                operation=_LIST_OPERATION,
                body=body_data,
                body_model=LogsToolListBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def list_fields(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolListFieldsResponse]]:
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
                "/api/v3.1/internal/action_execution/fields",
                cast_to=ToolListFieldsResponse,
                operation=_LIST_FIELDS_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncToolsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncToolsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolRetrieveResponse]]:
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
                    "/api/v3.1/internal/action_execution/log/{id}",
                    {"id": id},
                ),
                cast_to=ToolRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolListResponse]]: ...

    @overload
    def list(
        self,
        body: BodyParam,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolListResponse]]: ...

    def list(
        self,
        body: BodyParam | None = None,
        *,
        cursor: float | None | Omit = omit,
        limit: float | Omit = omit,
        case_sensitive: bool | None | Omit = omit,
        from_: float | Omit = omit,
        to: float | Omit = omit,
        search_params: Iterable[tool_list_params.SearchParam] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolListResponse]]:
        body_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "case_sensitive": case_sensitive,
                "from": from_,
                "to": to,
                "search_params": search_params,
            }
        )
        require_fields(
            body,
            body_fields,
            ("cursor",),
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
                "/api/v3.1/internal/action_execution/logs",
                cast_to=ToolListResponse,
                operation=_LIST_OPERATION,
                body=body_data,
                body_model=LogsToolListBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def list_fields(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolListFieldsResponse]]:
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
                "/api/v3.1/internal/action_execution/fields",
                cast_to=ToolListFieldsResponse,
                operation=_LIST_FIELDS_OPERATION,
                options=options_data,
                stream=True,
            )
        )
