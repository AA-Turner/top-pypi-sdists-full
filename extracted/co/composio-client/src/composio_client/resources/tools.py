# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.tools`` — the generated resource classes.

``ToolsResource`` (sync) and ``AsyncToolsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import cached_property
from typing import Literal

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, HeaderParam, QueryParam, RequestOptions
from .._models import ToolExecuteBody, ToolGetInputBody, ToolProxyBody, ToolRetrieveRequiredScopesBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ..types import tool_execute_params, tool_proxy_params
from ..types.tool_execute_response import ToolExecuteResponse
from ..types.tool_get_input_response import ToolGetInputResponse
from ..types.tool_list_response import ToolListResponse
from ..types.tool_proxy_response import ToolProxyResponse
from ..types.tool_retrieve_enum_response import ToolRetrieveEnumResponse
from ..types.tool_retrieve_required_scopes_response import ToolRetrieveRequiredScopesResponse
from ..types.tool_retrieve_response import ToolRetrieveResponse
from ._base import (
    AsyncAPIResource,
    SyncAPIResource,
    build_path,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
    normalize_body_argument,
    require_fields,
    split_body_argument,
    split_mapping_argument,
)

_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("tools", "retrieve")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("tools", "list")]
_EXECUTE_OPERATION = OPERATIONS_BY_CHAIN[("tools", "execute")]
_GET_INPUT_OPERATION = OPERATIONS_BY_CHAIN[("tools", "get_input")]
_PROXY_OPERATION = OPERATIONS_BY_CHAIN[("tools", "proxy")]
_RETRIEVE_ENUM_OPERATION = OPERATIONS_BY_CHAIN[("tools", "retrieve_enum")]
_RETRIEVE_REQUIRED_SCOPES_OPERATION = OPERATIONS_BY_CHAIN[("tools", "retrieve_required_scopes")]


class ToolsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ToolsResourceWithRawResponse:
        return ToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ToolsResourceWithStreamingResponse:
        return ToolsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        tool_slug: str,
        *,
        include_pricing: bool | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveResponse:
        query_fields = compact(
            {
                "include_pricing": include_pricing,
                "version": version,
                "toolkit_versions": toolkit_versions,
            }
        )
        query_data = merge_mapping(query, query_fields)
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
                "/api/v3.1/tools/{tool_slug}",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse: ...

    @overload
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: QueryParam,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse: ...

    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | QueryParam | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slugs": tool_slugs,
                "auth_config_ids": auth_config_ids,
                "important": important,
                "tags": tags,
                "scopes": scopes,
                "search": search,
                "include_deprecated": include_deprecated,
                "include_pricing": include_pricing,
                "toolkit_versions": toolkit_versions,
                "limit": limit,
                "cursor": cursor,
            }
        )
        aggregate_query, query_value = split_mapping_argument(query)
        query_fields.update(compact({"query": query_value}))
        query_data = merge_mapping(aggregate_query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/tools",
            cast_to=ToolListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Declared header parameter(s): x-llm-gateway-headers.
    def execute(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        connected_account_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        version: str | Omit = omit,
        custom_auth_params: tool_execute_params.CustomAuthParams | Omit = omit,
        custom_connection_data: tool_execute_params.CustomConnectionData | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        text: str | Omit = omit,
        allow_tracing: bool | None | Omit = omit,
        x_llm_gateway_headers: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolExecuteResponse:
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "entity_id": entity_id,
                "user_id": user_id,
                "version": version,
                "custom_auth_params": custom_auth_params,
                "custom_connection_data": custom_connection_data,
                "arguments": arguments,
                "text": text,
                "allow_tracing": allow_tracing,
            }
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-llm-gateway-headers": x_llm_gateway_headers,
            }
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
            build_path(
                "/api/v3.1/tools/execute/{tool_slug}",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolExecuteResponse,
            operation=_EXECUTE_OPERATION,
            body=body_data,
            body_model=ToolExecuteBody,
            headers=headers_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolGetInputResponse: ...

    @overload
    def get_input(
        self,
        tool_slug: str,
        body: BodyParam,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolGetInputResponse: ...

    def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolGetInputResponse:
        body_fields = compact(
            {
                "text": text,
                "custom_description": custom_description,
                "system_prompt": system_prompt,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("text",),
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
            build_path(
                "/api/v3.1/tools/execute/{tool_slug}/input",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolGetInputResponse,
            operation=_GET_INPUT_OPERATION,
            body=body_data,
            body_model=ToolGetInputBody,
            options=options_data,
        )

    @overload
    def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolProxyResponse: ...

    @overload
    def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolProxyResponse: ...

    @overload
    def proxy(
        self,
        legacy_body: BodyParam,
        /,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolProxyResponse: ...

    def proxy(
        self,
        *legacy_body: object,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolProxyResponse:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "connected_account_id",
                "user_id",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "post",
            "/api/v3.1/tools/execute/proxy",
            cast_to=ToolProxyResponse,
            operation=_PROXY_OPERATION,
            body=body_data,
            body_model=ToolProxyBody,
            options=options_data,
        )

    def retrieve_enum(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveEnumResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/tools/enum",
            cast_to=ToolRetrieveEnumResponse,
            operation=_RETRIEVE_ENUM_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveRequiredScopesResponse: ...

    @overload
    def retrieve_required_scopes(
        self,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveRequiredScopesResponse: ...

    def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveRequiredScopesResponse:
        body_fields = compact(
            {
                "tools": tools,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tools",),
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
            "/api/v3.1/tools/scopes/required",
            cast_to=ToolRetrieveRequiredScopesResponse,
            operation=_RETRIEVE_REQUIRED_SCOPES_OPERATION,
            body=body_data,
            body_model=ToolRetrieveRequiredScopesBody,
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
        tool_slug: str,
        *,
        include_pricing: bool | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveResponse:
        query_fields = compact(
            {
                "include_pricing": include_pricing,
                "version": version,
                "toolkit_versions": toolkit_versions,
            }
        )
        query_data = merge_mapping(query, query_fields)
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
                "/api/v3.1/tools/{tool_slug}",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse: ...

    @overload
    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: QueryParam,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse: ...

    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | QueryParam | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolListResponse:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slugs": tool_slugs,
                "auth_config_ids": auth_config_ids,
                "important": important,
                "tags": tags,
                "scopes": scopes,
                "search": search,
                "include_deprecated": include_deprecated,
                "include_pricing": include_pricing,
                "toolkit_versions": toolkit_versions,
                "limit": limit,
                "cursor": cursor,
            }
        )
        aggregate_query, query_value = split_mapping_argument(query)
        query_fields.update(compact({"query": query_value}))
        query_data = merge_mapping(aggregate_query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/tools",
            cast_to=ToolListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Declared header parameter(s): x-llm-gateway-headers.
    async def execute(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        connected_account_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        version: str | Omit = omit,
        custom_auth_params: tool_execute_params.CustomAuthParams | Omit = omit,
        custom_connection_data: tool_execute_params.CustomConnectionData | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        text: str | Omit = omit,
        allow_tracing: bool | None | Omit = omit,
        x_llm_gateway_headers: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolExecuteResponse:
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "entity_id": entity_id,
                "user_id": user_id,
                "version": version,
                "custom_auth_params": custom_auth_params,
                "custom_connection_data": custom_connection_data,
                "arguments": arguments,
                "text": text,
                "allow_tracing": allow_tracing,
            }
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-llm-gateway-headers": x_llm_gateway_headers,
            }
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
            build_path(
                "/api/v3.1/tools/execute/{tool_slug}",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolExecuteResponse,
            operation=_EXECUTE_OPERATION,
            body=body_data,
            body_model=ToolExecuteBody,
            headers=headers_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolGetInputResponse: ...

    @overload
    async def get_input(
        self,
        tool_slug: str,
        body: BodyParam,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolGetInputResponse: ...

    async def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolGetInputResponse:
        body_fields = compact(
            {
                "text": text,
                "custom_description": custom_description,
                "system_prompt": system_prompt,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("text",),
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
            build_path(
                "/api/v3.1/tools/execute/{tool_slug}/input",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolGetInputResponse,
            operation=_GET_INPUT_OPERATION,
            body=body_data,
            body_model=ToolGetInputBody,
            options=options_data,
        )

    @overload
    async def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolProxyResponse: ...

    @overload
    async def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolProxyResponse: ...

    @overload
    async def proxy(
        self,
        legacy_body: BodyParam,
        /,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolProxyResponse: ...

    async def proxy(
        self,
        *legacy_body: object,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolProxyResponse:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "connected_account_id",
                "user_id",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "post",
            "/api/v3.1/tools/execute/proxy",
            cast_to=ToolProxyResponse,
            operation=_PROXY_OPERATION,
            body=body_data,
            body_model=ToolProxyBody,
            options=options_data,
        )

    async def retrieve_enum(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveEnumResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/tools/enum",
            cast_to=ToolRetrieveEnumResponse,
            operation=_RETRIEVE_ENUM_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveRequiredScopesResponse: ...

    @overload
    async def retrieve_required_scopes(
        self,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveRequiredScopesResponse: ...

    async def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolRetrieveRequiredScopesResponse:
        body_fields = compact(
            {
                "tools": tools,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tools",),
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
            "/api/v3.1/tools/scopes/required",
            cast_to=ToolRetrieveRequiredScopesResponse,
            operation=_RETRIEVE_REQUIRED_SCOPES_OPERATION,
            body=body_data,
            body_model=ToolRetrieveRequiredScopesBody,
            options=options_data,
        )


class ToolsResourceWithRawResponse:
    def __init__(self, resource: ToolsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        tool_slug: str,
        *,
        include_pricing: bool | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolRetrieveResponse]:
        query_fields = compact(
            {
                "include_pricing": include_pricing,
                "version": version,
                "toolkit_versions": toolkit_versions,
            }
        )
        query_data = merge_mapping(query, query_fields)
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
                "/api/v3.1/tools/{tool_slug}",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolListResponse]: ...

    @overload
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: QueryParam,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolListResponse]: ...

    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | QueryParam | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolListResponse]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slugs": tool_slugs,
                "auth_config_ids": auth_config_ids,
                "important": important,
                "tags": tags,
                "scopes": scopes,
                "search": search,
                "include_deprecated": include_deprecated,
                "include_pricing": include_pricing,
                "toolkit_versions": toolkit_versions,
                "limit": limit,
                "cursor": cursor,
            }
        )
        aggregate_query, query_value = split_mapping_argument(query)
        query_fields.update(compact({"query": query_value}))
        query_data = merge_mapping(aggregate_query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/tools",
            cast_to=ToolListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Declared header parameter(s): x-llm-gateway-headers.
    def execute(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        connected_account_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        version: str | Omit = omit,
        custom_auth_params: tool_execute_params.CustomAuthParams | Omit = omit,
        custom_connection_data: tool_execute_params.CustomConnectionData | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        text: str | Omit = omit,
        allow_tracing: bool | None | Omit = omit,
        x_llm_gateway_headers: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolExecuteResponse]:
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "entity_id": entity_id,
                "user_id": user_id,
                "version": version,
                "custom_auth_params": custom_auth_params,
                "custom_connection_data": custom_connection_data,
                "arguments": arguments,
                "text": text,
                "allow_tracing": allow_tracing,
            }
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-llm-gateway-headers": x_llm_gateway_headers,
            }
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
            build_path(
                "/api/v3.1/tools/execute/{tool_slug}",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolExecuteResponse,
            operation=_EXECUTE_OPERATION,
            body=body_data,
            body_model=ToolExecuteBody,
            headers=headers_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolGetInputResponse]: ...

    @overload
    def get_input(
        self,
        tool_slug: str,
        body: BodyParam,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolGetInputResponse]: ...

    def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolGetInputResponse]:
        body_fields = compact(
            {
                "text": text,
                "custom_description": custom_description,
                "system_prompt": system_prompt,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("text",),
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
            build_path(
                "/api/v3.1/tools/execute/{tool_slug}/input",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolGetInputResponse,
            operation=_GET_INPUT_OPERATION,
            body=body_data,
            body_model=ToolGetInputBody,
            options=options_data,
        )

    @overload
    def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolProxyResponse]: ...

    @overload
    def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolProxyResponse]: ...

    @overload
    def proxy(
        self,
        legacy_body: BodyParam,
        /,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolProxyResponse]: ...

    def proxy(
        self,
        *legacy_body: object,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolProxyResponse]:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "connected_account_id",
                "user_id",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "post",
            "/api/v3.1/tools/execute/proxy",
            cast_to=ToolProxyResponse,
            operation=_PROXY_OPERATION,
            body=body_data,
            body_model=ToolProxyBody,
            options=options_data,
        )

    def retrieve_enum(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolRetrieveEnumResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/tools/enum",
            cast_to=ToolRetrieveEnumResponse,
            operation=_RETRIEVE_ENUM_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolRetrieveRequiredScopesResponse]: ...

    @overload
    def retrieve_required_scopes(
        self,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolRetrieveRequiredScopesResponse]: ...

    def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolRetrieveRequiredScopesResponse]:
        body_fields = compact(
            {
                "tools": tools,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tools",),
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
            "/api/v3.1/tools/scopes/required",
            cast_to=ToolRetrieveRequiredScopesResponse,
            operation=_RETRIEVE_REQUIRED_SCOPES_OPERATION,
            body=body_data,
            body_model=ToolRetrieveRequiredScopesBody,
            options=options_data,
        )


class AsyncToolsResourceWithRawResponse:
    def __init__(self, resource: AsyncToolsResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def retrieve(
        self,
        tool_slug: str,
        *,
        include_pricing: bool | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolRetrieveResponse]:
        query_fields = compact(
            {
                "include_pricing": include_pricing,
                "version": version,
                "toolkit_versions": toolkit_versions,
            }
        )
        query_data = merge_mapping(query, query_fields)
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
                "/api/v3.1/tools/{tool_slug}",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolListResponse]: ...

    @overload
    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: QueryParam,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolListResponse]: ...

    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | QueryParam | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolListResponse]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slugs": tool_slugs,
                "auth_config_ids": auth_config_ids,
                "important": important,
                "tags": tags,
                "scopes": scopes,
                "search": search,
                "include_deprecated": include_deprecated,
                "include_pricing": include_pricing,
                "toolkit_versions": toolkit_versions,
                "limit": limit,
                "cursor": cursor,
            }
        )
        aggregate_query, query_value = split_mapping_argument(query)
        query_fields.update(compact({"query": query_value}))
        query_data = merge_mapping(aggregate_query, query_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/tools",
            cast_to=ToolListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Declared header parameter(s): x-llm-gateway-headers.
    async def execute(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        connected_account_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        version: str | Omit = omit,
        custom_auth_params: tool_execute_params.CustomAuthParams | Omit = omit,
        custom_connection_data: tool_execute_params.CustomConnectionData | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        text: str | Omit = omit,
        allow_tracing: bool | None | Omit = omit,
        x_llm_gateway_headers: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolExecuteResponse]:
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "entity_id": entity_id,
                "user_id": user_id,
                "version": version,
                "custom_auth_params": custom_auth_params,
                "custom_connection_data": custom_connection_data,
                "arguments": arguments,
                "text": text,
                "allow_tracing": allow_tracing,
            }
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-llm-gateway-headers": x_llm_gateway_headers,
            }
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
            build_path(
                "/api/v3.1/tools/execute/{tool_slug}",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolExecuteResponse,
            operation=_EXECUTE_OPERATION,
            body=body_data,
            body_model=ToolExecuteBody,
            headers=headers_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolGetInputResponse]: ...

    @overload
    async def get_input(
        self,
        tool_slug: str,
        body: BodyParam,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolGetInputResponse]: ...

    async def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolGetInputResponse]:
        body_fields = compact(
            {
                "text": text,
                "custom_description": custom_description,
                "system_prompt": system_prompt,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("text",),
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
            build_path(
                "/api/v3.1/tools/execute/{tool_slug}/input",
                {"tool_slug": tool_slug},
            ),
            cast_to=ToolGetInputResponse,
            operation=_GET_INPUT_OPERATION,
            body=body_data,
            body_model=ToolGetInputBody,
            options=options_data,
        )

    @overload
    async def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolProxyResponse]: ...

    @overload
    async def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolProxyResponse]: ...

    @overload
    async def proxy(
        self,
        legacy_body: BodyParam,
        /,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolProxyResponse]: ...

    async def proxy(
        self,
        *legacy_body: object,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolProxyResponse]:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "connected_account_id",
                "user_id",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "post",
            "/api/v3.1/tools/execute/proxy",
            cast_to=ToolProxyResponse,
            operation=_PROXY_OPERATION,
            body=body_data,
            body_model=ToolProxyBody,
            options=options_data,
        )

    async def retrieve_enum(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolRetrieveEnumResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/tools/enum",
            cast_to=ToolRetrieveEnumResponse,
            operation=_RETRIEVE_ENUM_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolRetrieveRequiredScopesResponse]: ...

    @overload
    async def retrieve_required_scopes(
        self,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolRetrieveRequiredScopesResponse]: ...

    async def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolRetrieveRequiredScopesResponse]:
        body_fields = compact(
            {
                "tools": tools,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tools",),
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
            "/api/v3.1/tools/scopes/required",
            cast_to=ToolRetrieveRequiredScopesResponse,
            operation=_RETRIEVE_REQUIRED_SCOPES_OPERATION,
            body=body_data,
            body_model=ToolRetrieveRequiredScopesBody,
            options=options_data,
        )


class ToolsResourceWithStreamingResponse:
    def __init__(self, resource: ToolsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        tool_slug: str,
        *,
        include_pricing: bool | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolRetrieveResponse]]:
        query_fields = compact(
            {
                "include_pricing": include_pricing,
                "version": version,
                "toolkit_versions": toolkit_versions,
            }
        )
        query_data = merge_mapping(query, query_fields)
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
                    "/api/v3.1/tools/{tool_slug}",
                    {"tool_slug": tool_slug},
                ),
                cast_to=ToolRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolListResponse]]: ...

    @overload
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: QueryParam,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolListResponse]]: ...

    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | QueryParam | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolListResponse]]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slugs": tool_slugs,
                "auth_config_ids": auth_config_ids,
                "important": important,
                "tags": tags,
                "scopes": scopes,
                "search": search,
                "include_deprecated": include_deprecated,
                "include_pricing": include_pricing,
                "toolkit_versions": toolkit_versions,
                "limit": limit,
                "cursor": cursor,
            }
        )
        aggregate_query, query_value = split_mapping_argument(query)
        query_fields.update(compact({"query": query_value}))
        query_data = merge_mapping(aggregate_query, query_fields)
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
                "/api/v3.1/tools",
                cast_to=ToolListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    # Declared header parameter(s): x-llm-gateway-headers.
    def execute(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        connected_account_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        version: str | Omit = omit,
        custom_auth_params: tool_execute_params.CustomAuthParams | Omit = omit,
        custom_connection_data: tool_execute_params.CustomConnectionData | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        text: str | Omit = omit,
        allow_tracing: bool | None | Omit = omit,
        x_llm_gateway_headers: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolExecuteResponse]]:
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "entity_id": entity_id,
                "user_id": user_id,
                "version": version,
                "custom_auth_params": custom_auth_params,
                "custom_connection_data": custom_connection_data,
                "arguments": arguments,
                "text": text,
                "allow_tracing": allow_tracing,
            }
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-llm-gateway-headers": x_llm_gateway_headers,
            }
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
                build_path(
                    "/api/v3.1/tools/execute/{tool_slug}",
                    {"tool_slug": tool_slug},
                ),
                cast_to=ToolExecuteResponse,
                operation=_EXECUTE_OPERATION,
                body=body_data,
                body_model=ToolExecuteBody,
                headers=headers_data,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolGetInputResponse]]: ...

    @overload
    def get_input(
        self,
        tool_slug: str,
        body: BodyParam,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolGetInputResponse]]: ...

    def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolGetInputResponse]]:
        body_fields = compact(
            {
                "text": text,
                "custom_description": custom_description,
                "system_prompt": system_prompt,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("text",),
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
                build_path(
                    "/api/v3.1/tools/execute/{tool_slug}/input",
                    {"tool_slug": tool_slug},
                ),
                cast_to=ToolGetInputResponse,
                operation=_GET_INPUT_OPERATION,
                body=body_data,
                body_model=ToolGetInputBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolProxyResponse]]: ...

    @overload
    def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolProxyResponse]]: ...

    @overload
    def proxy(
        self,
        legacy_body: BodyParam,
        /,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolProxyResponse]]: ...

    def proxy(
        self,
        *legacy_body: object,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolProxyResponse]]:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "connected_account_id",
                "user_id",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
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
                "/api/v3.1/tools/execute/proxy",
                cast_to=ToolProxyResponse,
                operation=_PROXY_OPERATION,
                body=body_data,
                body_model=ToolProxyBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_enum(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolRetrieveEnumResponse]]:
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
                "/api/v3.1/tools/enum",
                cast_to=ToolRetrieveEnumResponse,
                operation=_RETRIEVE_ENUM_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolRetrieveRequiredScopesResponse]]: ...

    @overload
    def retrieve_required_scopes(
        self,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolRetrieveRequiredScopesResponse]]: ...

    def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolRetrieveRequiredScopesResponse]]:
        body_fields = compact(
            {
                "tools": tools,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tools",),
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
                "/api/v3.1/tools/scopes/required",
                cast_to=ToolRetrieveRequiredScopesResponse,
                operation=_RETRIEVE_REQUIRED_SCOPES_OPERATION,
                body=body_data,
                body_model=ToolRetrieveRequiredScopesBody,
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
        tool_slug: str,
        *,
        include_pricing: bool | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolRetrieveResponse]]:
        query_fields = compact(
            {
                "include_pricing": include_pricing,
                "version": version,
                "toolkit_versions": toolkit_versions,
            }
        )
        query_data = merge_mapping(query, query_fields)
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
                    "/api/v3.1/tools/{tool_slug}",
                    {"tool_slug": tool_slug},
                ),
                cast_to=ToolRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolListResponse]]: ...

    @overload
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: QueryParam,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolListResponse]]: ...

    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slugs: str | Omit = omit,
        auth_config_ids: str | SequenceNotStr[str] | Omit = omit,
        important: Literal["true", "false"] | Omit = omit,
        tags: SequenceNotStr[str] | Omit = omit,
        scopes: SequenceNotStr[str] | None | Omit = omit,
        query: str | QueryParam | Omit = omit,
        search: str | Omit = omit,
        include_deprecated: bool | Omit = omit,
        include_pricing: bool | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolListResponse]]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slugs": tool_slugs,
                "auth_config_ids": auth_config_ids,
                "important": important,
                "tags": tags,
                "scopes": scopes,
                "search": search,
                "include_deprecated": include_deprecated,
                "include_pricing": include_pricing,
                "toolkit_versions": toolkit_versions,
                "limit": limit,
                "cursor": cursor,
            }
        )
        aggregate_query, query_value = split_mapping_argument(query)
        query_fields.update(compact({"query": query_value}))
        query_data = merge_mapping(aggregate_query, query_fields)
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
                "/api/v3.1/tools",
                cast_to=ToolListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    # Declared header parameter(s): x-llm-gateway-headers.
    def execute(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        connected_account_id: str | Omit = omit,
        entity_id: str | Omit = omit,
        user_id: str | Omit = omit,
        version: str | Omit = omit,
        custom_auth_params: tool_execute_params.CustomAuthParams | Omit = omit,
        custom_connection_data: tool_execute_params.CustomConnectionData | Omit = omit,
        arguments: dict[str, object | None] | Omit = omit,
        text: str | Omit = omit,
        allow_tracing: bool | None | Omit = omit,
        x_llm_gateway_headers: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolExecuteResponse]]:
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "entity_id": entity_id,
                "user_id": user_id,
                "version": version,
                "custom_auth_params": custom_auth_params,
                "custom_connection_data": custom_connection_data,
                "arguments": arguments,
                "text": text,
                "allow_tracing": allow_tracing,
            }
        )
        body_data = merge_body(body, body_fields)
        header_fields = compact(
            {
                "x-llm-gateway-headers": x_llm_gateway_headers,
            }
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
                build_path(
                    "/api/v3.1/tools/execute/{tool_slug}",
                    {"tool_slug": tool_slug},
                ),
                cast_to=ToolExecuteResponse,
                operation=_EXECUTE_OPERATION,
                body=body_data,
                body_model=ToolExecuteBody,
                headers=headers_data,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolGetInputResponse]]: ...

    @overload
    def get_input(
        self,
        tool_slug: str,
        body: BodyParam,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolGetInputResponse]]: ...

    def get_input(
        self,
        tool_slug: str,
        body: BodyParam | None = None,
        *,
        text: str | Omit = omit,
        custom_description: str | Omit = omit,
        system_prompt: str | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolGetInputResponse]]:
        body_fields = compact(
            {
                "text": text,
                "custom_description": custom_description,
                "system_prompt": system_prompt,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("text",),
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
                build_path(
                    "/api/v3.1/tools/execute/{tool_slug}/input",
                    {"tool_slug": tool_slug},
                ),
                cast_to=ToolGetInputResponse,
                operation=_GET_INPUT_OPERATION,
                body=body_data,
                body_model=ToolGetInputBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"],
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolProxyResponse]]: ...

    @overload
    def proxy(
        self,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolProxyResponse]]: ...

    @overload
    def proxy(
        self,
        legacy_body: BodyParam,
        /,
        *,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolProxyResponse]]: ...

    def proxy(
        self,
        *legacy_body: object,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        endpoint: str | Omit = omit,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"] | Omit = omit,
        binary_body: tool_proxy_params.BinaryBody | Omit = omit,
        parameters: Iterable[tool_proxy_params.Parameter] | Omit = omit,
        custom_connection_data: tool_proxy_params.CustomConnectionData | Omit = omit,
        body: object | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolProxyResponse]]:
        body = normalize_body_argument(body, legacy_body)
        body_fields = compact(
            {
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "endpoint": endpoint,
                "method": method,
                "binary_body": binary_body,
                "parameters": parameters,
                "custom_connection_data": custom_connection_data,
            }
        )
        aggregate_body, body_value = split_body_argument(
            body,
            body_fields,
            (
                "connected_account_id",
                "user_id",
                "endpoint",
                "method",
                "body",
                "binary_body",
                "parameters",
                "custom_connection_data",
            ),
        )
        body_fields.update(compact({"body": body_value}))
        require_fields(
            aggregate_body,
            body_fields,
            ("endpoint", "method"),
            "body",
        )
        body_data = merge_body(aggregate_body, body_fields)
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
                "/api/v3.1/tools/execute/proxy",
                cast_to=ToolProxyResponse,
                operation=_PROXY_OPERATION,
                body=body_data,
                body_model=ToolProxyBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_enum(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolRetrieveEnumResponse]]:
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
                "/api/v3.1/tools/enum",
                cast_to=ToolRetrieveEnumResponse,
                operation=_RETRIEVE_ENUM_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolRetrieveRequiredScopesResponse]]: ...

    @overload
    def retrieve_required_scopes(
        self,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolRetrieveRequiredScopesResponse]]: ...

    def retrieve_required_scopes(
        self,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolRetrieveRequiredScopesResponse]]:
        body_fields = compact(
            {
                "tools": tools,
                "version": version,
            }
        )
        require_fields(
            body,
            body_fields,
            ("tools",),
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
                "/api/v3.1/tools/scopes/required",
                cast_to=ToolRetrieveRequiredScopesResponse,
                operation=_RETRIEVE_REQUIRED_SCOPES_OPERATION,
                body=body_data,
                body_model=ToolRetrieveRequiredScopesBody,
                options=options_data,
                stream=True,
            )
        )
