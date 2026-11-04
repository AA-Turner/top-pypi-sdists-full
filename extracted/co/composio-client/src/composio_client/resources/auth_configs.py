# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.auth_configs`` — the generated resource classes.

``AuthConfigsResource`` (sync) and ``AsyncAuthConfigsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import Literal

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, QueryParam, RequestOptions
from .._models import AuthConfigCreateBody, AuthConfigUpdateBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ..types import auth_config_create_params, auth_config_update_params
from ..types.auth_config_create_response import AuthConfigCreateResponse
from ..types.auth_config_delete_response import AuthConfigDeleteResponse
from ..types.auth_config_list_response import AuthConfigListResponse
from ..types.auth_config_retrieve_response import AuthConfigRetrieveResponse
from ..types.auth_config_update_response import AuthConfigUpdateResponse
from ..types.auth_config_update_status_response import AuthConfigUpdateStatusResponse
from ._base import (
    AsyncAPIResource,
    SyncAPIResource,
    build_path,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
    normalize_path_arguments,
    require_fields,
)

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("auth_configs", "create")]
_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("auth_configs", "retrieve")]
_UPDATE_OPERATION = OPERATIONS_BY_CHAIN[("auth_configs", "update")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("auth_configs", "list")]
_DELETE_OPERATION = OPERATIONS_BY_CHAIN[("auth_configs", "delete")]
_UPDATE_STATUS_OPERATION = OPERATIONS_BY_CHAIN[("auth_configs", "update_status")]


class AuthConfigsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AuthConfigsResourceWithRawResponse:
        return AuthConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AuthConfigsResourceWithStreamingResponse:
        return AuthConfigsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigCreateResponse:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "auth_config": auth_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
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
            "/api/v3.1/auth_configs",
            cast_to=AuthConfigCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=AuthConfigCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigRetrieveResponse:
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
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    @overload
    def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"],
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateResponse: ...

    @overload
    def update(
        self,
        nanoid: str,
        body: BodyParam,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateResponse: ...

    def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateResponse:
        body_fields = compact(
            {
                "type": type,
                "name": name,
                "credentials": credentials,
                "sealed_credentials": sealed_credentials,
                "proxy_config": proxy_config,
                "restrict_to_following_tools": restrict_to_following_tools,
                "tool_access_config": tool_access_config,
                "shared_credentials": shared_credentials,
                "shared_connection_fields": shared_connection_fields,
                "is_enabled_for_tool_router": is_enabled_for_tool_router,
                "scopes": scopes,
                "user_scopes": user_scopes,
            }
        )
        require_fields(
            body,
            body_fields,
            ("type",),
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
            "patch",
            build_path(
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=AuthConfigUpdateBody,
            options=options_data,
        )

    def list(
        self,
        *,
        is_composio_managed: str | bool | Omit = omit,
        toolkit_slug: str | Omit = omit,
        deprecated_app_id: str | Omit = omit,
        deprecated_status: str | Omit = omit,
        show_disabled: bool | None | Omit = omit,
        search: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigListResponse:
        query_fields = compact(
            {
                "is_composio_managed": is_composio_managed,
                "toolkit_slug": toolkit_slug,
                "deprecated_app_id": deprecated_app_id,
                "deprecated_status": deprecated_status,
                "show_disabled": show_disabled,
                "search": search,
                "limit": limit,
                "cursor": cursor,
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
            "/api/v3.1/auth_configs",
            cast_to=AuthConfigListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    def delete(
        self,
        nanoid: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigDeleteResponse:
        query_fields = compact(
            {
                "revoke_on_delete": revoke_on_delete,
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
            "delete",
            build_path(
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def update_status(
        self,
        status: Literal["ENABLED", "DISABLED"],
        *,
        nanoid: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateStatusResponse: ...

    @overload
    def update_status(
        self,
        status: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateStatusResponse: ...

    def update_status(
        self,
        status: str,
        *legacy_args: object,
        nanoid: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateStatusResponse:
        status, (nanoid,), _legacy_body = normalize_path_arguments(
            status,
            legacy_args,
            leading_values=(nanoid,),
            leading_names=("nanoid",),
            trailing_name="status",
            accepts_body=False,
        )
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
                "/api/v3.1/auth_configs/{nanoid}/{status}",
                {"nanoid": nanoid, "status": status},
            ),
            cast_to=AuthConfigUpdateStatusResponse,
            operation=_UPDATE_STATUS_OPERATION,
            options=options_data,
        )


class AsyncAuthConfigsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAuthConfigsResourceWithRawResponse:
        return AsyncAuthConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAuthConfigsResourceWithStreamingResponse:
        return AsyncAuthConfigsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigCreateResponse:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "auth_config": auth_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
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
            "/api/v3.1/auth_configs",
            cast_to=AuthConfigCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=AuthConfigCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigRetrieveResponse:
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
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    @overload
    async def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"],
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateResponse: ...

    @overload
    async def update(
        self,
        nanoid: str,
        body: BodyParam,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateResponse: ...

    async def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateResponse:
        body_fields = compact(
            {
                "type": type,
                "name": name,
                "credentials": credentials,
                "sealed_credentials": sealed_credentials,
                "proxy_config": proxy_config,
                "restrict_to_following_tools": restrict_to_following_tools,
                "tool_access_config": tool_access_config,
                "shared_credentials": shared_credentials,
                "shared_connection_fields": shared_connection_fields,
                "is_enabled_for_tool_router": is_enabled_for_tool_router,
                "scopes": scopes,
                "user_scopes": user_scopes,
            }
        )
        require_fields(
            body,
            body_fields,
            ("type",),
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
            "patch",
            build_path(
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=AuthConfigUpdateBody,
            options=options_data,
        )

    async def list(
        self,
        *,
        is_composio_managed: str | bool | Omit = omit,
        toolkit_slug: str | Omit = omit,
        deprecated_app_id: str | Omit = omit,
        deprecated_status: str | Omit = omit,
        show_disabled: bool | None | Omit = omit,
        search: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigListResponse:
        query_fields = compact(
            {
                "is_composio_managed": is_composio_managed,
                "toolkit_slug": toolkit_slug,
                "deprecated_app_id": deprecated_app_id,
                "deprecated_status": deprecated_status,
                "show_disabled": show_disabled,
                "search": search,
                "limit": limit,
                "cursor": cursor,
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
            "/api/v3.1/auth_configs",
            cast_to=AuthConfigListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def delete(
        self,
        nanoid: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigDeleteResponse:
        query_fields = compact(
            {
                "revoke_on_delete": revoke_on_delete,
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
            "delete",
            build_path(
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def update_status(
        self,
        status: Literal["ENABLED", "DISABLED"],
        *,
        nanoid: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateStatusResponse: ...

    @overload
    async def update_status(
        self,
        status: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateStatusResponse: ...

    async def update_status(
        self,
        status: str,
        *legacy_args: object,
        nanoid: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AuthConfigUpdateStatusResponse:
        status, (nanoid,), _legacy_body = normalize_path_arguments(
            status,
            legacy_args,
            leading_values=(nanoid,),
            leading_names=("nanoid",),
            trailing_name="status",
            accepts_body=False,
        )
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
                "/api/v3.1/auth_configs/{nanoid}/{status}",
                {"nanoid": nanoid, "status": status},
            ),
            cast_to=AuthConfigUpdateStatusResponse,
            operation=_UPDATE_STATUS_OPERATION,
            options=options_data,
        )


class AuthConfigsResourceWithRawResponse:
    def __init__(self, resource: AuthConfigsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigCreateResponse]:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "auth_config": auth_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
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
            "/api/v3.1/auth_configs",
            cast_to=AuthConfigCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=AuthConfigCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigRetrieveResponse]:
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
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    @overload
    def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"],
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigUpdateResponse]: ...

    @overload
    def update(
        self,
        nanoid: str,
        body: BodyParam,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigUpdateResponse]: ...

    def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigUpdateResponse]:
        body_fields = compact(
            {
                "type": type,
                "name": name,
                "credentials": credentials,
                "sealed_credentials": sealed_credentials,
                "proxy_config": proxy_config,
                "restrict_to_following_tools": restrict_to_following_tools,
                "tool_access_config": tool_access_config,
                "shared_credentials": shared_credentials,
                "shared_connection_fields": shared_connection_fields,
                "is_enabled_for_tool_router": is_enabled_for_tool_router,
                "scopes": scopes,
                "user_scopes": user_scopes,
            }
        )
        require_fields(
            body,
            body_fields,
            ("type",),
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
            "patch",
            build_path(
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=AuthConfigUpdateBody,
            options=options_data,
        )

    def list(
        self,
        *,
        is_composio_managed: str | bool | Omit = omit,
        toolkit_slug: str | Omit = omit,
        deprecated_app_id: str | Omit = omit,
        deprecated_status: str | Omit = omit,
        show_disabled: bool | None | Omit = omit,
        search: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigListResponse]:
        query_fields = compact(
            {
                "is_composio_managed": is_composio_managed,
                "toolkit_slug": toolkit_slug,
                "deprecated_app_id": deprecated_app_id,
                "deprecated_status": deprecated_status,
                "show_disabled": show_disabled,
                "search": search,
                "limit": limit,
                "cursor": cursor,
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
            "/api/v3.1/auth_configs",
            cast_to=AuthConfigListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    def delete(
        self,
        nanoid: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigDeleteResponse]:
        query_fields = compact(
            {
                "revoke_on_delete": revoke_on_delete,
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
            "delete",
            build_path(
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def update_status(
        self,
        status: Literal["ENABLED", "DISABLED"],
        *,
        nanoid: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigUpdateStatusResponse]: ...

    @overload
    def update_status(
        self,
        status: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigUpdateStatusResponse]: ...

    def update_status(
        self,
        status: str,
        *legacy_args: object,
        nanoid: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[AuthConfigUpdateStatusResponse]:
        status, (nanoid,), _legacy_body = normalize_path_arguments(
            status,
            legacy_args,
            leading_values=(nanoid,),
            leading_names=("nanoid",),
            trailing_name="status",
            accepts_body=False,
        )
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
                "/api/v3.1/auth_configs/{nanoid}/{status}",
                {"nanoid": nanoid, "status": status},
            ),
            cast_to=AuthConfigUpdateStatusResponse,
            operation=_UPDATE_STATUS_OPERATION,
            options=options_data,
        )


class AsyncAuthConfigsResourceWithRawResponse:
    def __init__(self, resource: AsyncAuthConfigsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigCreateResponse]:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "auth_config": auth_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
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
            "/api/v3.1/auth_configs",
            cast_to=AuthConfigCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=AuthConfigCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigRetrieveResponse]:
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
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    @overload
    async def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"],
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigUpdateResponse]: ...

    @overload
    async def update(
        self,
        nanoid: str,
        body: BodyParam,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigUpdateResponse]: ...

    async def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigUpdateResponse]:
        body_fields = compact(
            {
                "type": type,
                "name": name,
                "credentials": credentials,
                "sealed_credentials": sealed_credentials,
                "proxy_config": proxy_config,
                "restrict_to_following_tools": restrict_to_following_tools,
                "tool_access_config": tool_access_config,
                "shared_credentials": shared_credentials,
                "shared_connection_fields": shared_connection_fields,
                "is_enabled_for_tool_router": is_enabled_for_tool_router,
                "scopes": scopes,
                "user_scopes": user_scopes,
            }
        )
        require_fields(
            body,
            body_fields,
            ("type",),
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
            "patch",
            build_path(
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=AuthConfigUpdateBody,
            options=options_data,
        )

    async def list(
        self,
        *,
        is_composio_managed: str | bool | Omit = omit,
        toolkit_slug: str | Omit = omit,
        deprecated_app_id: str | Omit = omit,
        deprecated_status: str | Omit = omit,
        show_disabled: bool | None | Omit = omit,
        search: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigListResponse]:
        query_fields = compact(
            {
                "is_composio_managed": is_composio_managed,
                "toolkit_slug": toolkit_slug,
                "deprecated_app_id": deprecated_app_id,
                "deprecated_status": deprecated_status,
                "show_disabled": show_disabled,
                "search": search,
                "limit": limit,
                "cursor": cursor,
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
            "/api/v3.1/auth_configs",
            cast_to=AuthConfigListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def delete(
        self,
        nanoid: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigDeleteResponse]:
        query_fields = compact(
            {
                "revoke_on_delete": revoke_on_delete,
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
            "delete",
            build_path(
                "/api/v3.1/auth_configs/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=AuthConfigDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def update_status(
        self,
        status: Literal["ENABLED", "DISABLED"],
        *,
        nanoid: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigUpdateStatusResponse]: ...

    @overload
    async def update_status(
        self,
        status: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigUpdateStatusResponse]: ...

    async def update_status(
        self,
        status: str,
        *legacy_args: object,
        nanoid: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[AuthConfigUpdateStatusResponse]:
        status, (nanoid,), _legacy_body = normalize_path_arguments(
            status,
            legacy_args,
            leading_values=(nanoid,),
            leading_names=("nanoid",),
            trailing_name="status",
            accepts_body=False,
        )
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
                "/api/v3.1/auth_configs/{nanoid}/{status}",
                {"nanoid": nanoid, "status": status},
            ),
            cast_to=AuthConfigUpdateStatusResponse,
            operation=_UPDATE_STATUS_OPERATION,
            options=options_data,
        )


class AuthConfigsResourceWithStreamingResponse:
    def __init__(self, resource: AuthConfigsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigCreateResponse]]:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "auth_config": auth_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
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
                "/api/v3.1/auth_configs",
                cast_to=AuthConfigCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=AuthConfigCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigRetrieveResponse]]:
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
                    "/api/v3.1/auth_configs/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=AuthConfigRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"],
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigUpdateResponse]]: ...

    @overload
    def update(
        self,
        nanoid: str,
        body: BodyParam,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigUpdateResponse]]: ...

    def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigUpdateResponse]]:
        body_fields = compact(
            {
                "type": type,
                "name": name,
                "credentials": credentials,
                "sealed_credentials": sealed_credentials,
                "proxy_config": proxy_config,
                "restrict_to_following_tools": restrict_to_following_tools,
                "tool_access_config": tool_access_config,
                "shared_credentials": shared_credentials,
                "shared_connection_fields": shared_connection_fields,
                "is_enabled_for_tool_router": is_enabled_for_tool_router,
                "scopes": scopes,
                "user_scopes": user_scopes,
            }
        )
        require_fields(
            body,
            body_fields,
            ("type",),
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
                "patch",
                build_path(
                    "/api/v3.1/auth_configs/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=AuthConfigUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=AuthConfigUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        is_composio_managed: str | bool | Omit = omit,
        toolkit_slug: str | Omit = omit,
        deprecated_app_id: str | Omit = omit,
        deprecated_status: str | Omit = omit,
        show_disabled: bool | None | Omit = omit,
        search: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigListResponse]]:
        query_fields = compact(
            {
                "is_composio_managed": is_composio_managed,
                "toolkit_slug": toolkit_slug,
                "deprecated_app_id": deprecated_app_id,
                "deprecated_status": deprecated_status,
                "show_disabled": show_disabled,
                "search": search,
                "limit": limit,
                "cursor": cursor,
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
                "/api/v3.1/auth_configs",
                cast_to=AuthConfigListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        nanoid: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigDeleteResponse]]:
        query_fields = compact(
            {
                "revoke_on_delete": revoke_on_delete,
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
                "delete",
                build_path(
                    "/api/v3.1/auth_configs/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=AuthConfigDeleteResponse,
                operation=_DELETE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def update_status(
        self,
        status: Literal["ENABLED", "DISABLED"],
        *,
        nanoid: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigUpdateStatusResponse]]: ...

    @overload
    def update_status(
        self,
        status: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigUpdateStatusResponse]]: ...

    def update_status(
        self,
        status: str,
        *legacy_args: object,
        nanoid: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[AuthConfigUpdateStatusResponse]]:
        status, (nanoid,), _legacy_body = normalize_path_arguments(
            status,
            legacy_args,
            leading_values=(nanoid,),
            leading_names=("nanoid",),
            trailing_name="status",
            accepts_body=False,
        )
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
                    "/api/v3.1/auth_configs/{nanoid}/{status}",
                    {"nanoid": nanoid, "status": status},
                ),
                cast_to=AuthConfigUpdateStatusResponse,
                operation=_UPDATE_STATUS_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncAuthConfigsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncAuthConfigsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        toolkit: auth_config_create_params.Toolkit | Omit = omit,
        auth_config: auth_config_create_params.AuthConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigCreateResponse]]:
        body_fields = compact(
            {
                "toolkit": toolkit,
                "auth_config": auth_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit",),
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
                "/api/v3.1/auth_configs",
                cast_to=AuthConfigCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=AuthConfigCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigRetrieveResponse]]:
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
                    "/api/v3.1/auth_configs/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=AuthConfigRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"],
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigUpdateResponse]]: ...

    @overload
    def update(
        self,
        nanoid: str,
        body: BodyParam,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigUpdateResponse]]: ...

    def update(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        type: Literal["custom"] | Literal["default"] | Omit = omit,
        name: str | Omit = omit,
        credentials: auth_config_update_params.Variant0Credentials | Omit = omit,
        sealed_credentials: dict[str, str] | Omit = omit,
        proxy_config: auth_config_update_params.Variant0ProxyConfig | None | Omit = omit,
        restrict_to_following_tools: SequenceNotStr[str] | Omit = omit,
        tool_access_config: auth_config_update_params.Variant0ToolAccessConfig
        | auth_config_update_params.Variant1ToolAccessConfig
        | Omit = omit,
        shared_credentials: dict[str, object | None] | Omit = omit,
        shared_connection_fields: dict[str, object | None] | Omit = omit,
        is_enabled_for_tool_router: bool | Omit = omit,
        scopes: str | SequenceNotStr[str] | Omit = omit,
        user_scopes: str | SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigUpdateResponse]]:
        body_fields = compact(
            {
                "type": type,
                "name": name,
                "credentials": credentials,
                "sealed_credentials": sealed_credentials,
                "proxy_config": proxy_config,
                "restrict_to_following_tools": restrict_to_following_tools,
                "tool_access_config": tool_access_config,
                "shared_credentials": shared_credentials,
                "shared_connection_fields": shared_connection_fields,
                "is_enabled_for_tool_router": is_enabled_for_tool_router,
                "scopes": scopes,
                "user_scopes": user_scopes,
            }
        )
        require_fields(
            body,
            body_fields,
            ("type",),
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
                "patch",
                build_path(
                    "/api/v3.1/auth_configs/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=AuthConfigUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=AuthConfigUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        is_composio_managed: str | bool | Omit = omit,
        toolkit_slug: str | Omit = omit,
        deprecated_app_id: str | Omit = omit,
        deprecated_status: str | Omit = omit,
        show_disabled: bool | None | Omit = omit,
        search: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigListResponse]]:
        query_fields = compact(
            {
                "is_composio_managed": is_composio_managed,
                "toolkit_slug": toolkit_slug,
                "deprecated_app_id": deprecated_app_id,
                "deprecated_status": deprecated_status,
                "show_disabled": show_disabled,
                "search": search,
                "limit": limit,
                "cursor": cursor,
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
                "/api/v3.1/auth_configs",
                cast_to=AuthConfigListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        nanoid: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigDeleteResponse]]:
        query_fields = compact(
            {
                "revoke_on_delete": revoke_on_delete,
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
                "delete",
                build_path(
                    "/api/v3.1/auth_configs/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=AuthConfigDeleteResponse,
                operation=_DELETE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def update_status(
        self,
        status: Literal["ENABLED", "DISABLED"],
        *,
        nanoid: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigUpdateStatusResponse]]: ...

    @overload
    def update_status(
        self,
        status: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigUpdateStatusResponse]]: ...

    def update_status(
        self,
        status: str,
        *legacy_args: object,
        nanoid: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[AuthConfigUpdateStatusResponse]]:
        status, (nanoid,), _legacy_body = normalize_path_arguments(
            status,
            legacy_args,
            leading_values=(nanoid,),
            leading_names=("nanoid",),
            trailing_name="status",
            accepts_body=False,
        )
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
                    "/api/v3.1/auth_configs/{nanoid}/{status}",
                    {"nanoid": nanoid, "status": status},
                ),
                cast_to=AuthConfigUpdateStatusResponse,
                operation=_UPDATE_STATUS_OPERATION,
                options=options_data,
                stream=True,
            )
        )
