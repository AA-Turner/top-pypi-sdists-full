# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.connected_accounts`` — the generated resource classes.

``ConnectedAccountsResource`` (sync) and ``AsyncConnectedAccountsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import Literal

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, QueryParam, RequestOptions
from .._models import (
    ConnectedAccountCompleteAuthBody,
    ConnectedAccountCreateBody,
    ConnectedAccountPatchBody,
    ConnectedAccountRefreshBody,
    ConnectedAccountUpdateStatusBody,
)
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ..types import connected_account_create_params, connected_account_patch_params
from ..types.connected_account_complete_auth_response import ConnectedAccountCompleteAuthResponse
from ..types.connected_account_create_response import ConnectedAccountCreateResponse
from ..types.connected_account_delete_response import ConnectedAccountDeleteResponse
from ..types.connected_account_list_response import ConnectedAccountListResponse
from ..types.connected_account_patch_response import ConnectedAccountPatchResponse
from ..types.connected_account_refresh_response import ConnectedAccountRefreshResponse
from ..types.connected_account_retrieve_response import ConnectedAccountRetrieveResponse
from ..types.connected_account_revoke_response import ConnectedAccountRevokeResponse
from ..types.connected_account_update_status_response import ConnectedAccountUpdateStatusResponse
from ._base import (
    AsyncAPIResource,
    SyncAPIResource,
    build_path,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
    require_fields,
)

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "create")]
_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "retrieve")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "list")]
_DELETE_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "delete")]
_COMPLETE_AUTH_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "complete_auth")]
_PATCH_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "patch")]
_REFRESH_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "refresh")]
_REVOKE_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "revoke")]
_UPDATE_STATUS_OPERATION = OPERATIONS_BY_CHAIN[("connected_accounts", "update_status")]


class ConnectedAccountsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConnectedAccountsResourceWithRawResponse:
        return ConnectedAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConnectedAccountsResourceWithStreamingResponse:
        return ConnectedAccountsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig,
        connection: connected_account_create_params.Connection,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCreateResponse:
        body_fields = compact(
            {
                "auth_config": auth_config,
                "connection": connection,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config", "connection"),
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
            "/api/v3.1/connected_accounts",
            cast_to=ConnectedAccountCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ConnectedAccountCreateBody,
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
    ) -> ConnectedAccountRetrieveResponse:
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        statuses: list[
            Literal["INITIALIZING", "INITIATED", "ACTIVE", "FAILED", "EXPIRED", "INACTIVE", "REVOKED"]
        ]
        | None
        | Omit = omit,
        cursor: str | None | Omit = omit,
        limit: float | None | Omit = omit,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | None | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | None | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        account_type: Literal["PRIVATE", "SHARED", "ALL"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountListResponse:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "statuses": statuses,
                "cursor": cursor,
                "limit": limit,
                "user_ids": user_ids,
                "auth_config_ids": auth_config_ids,
                "connected_account_ids": connected_account_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "account_type": account_type,
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
            "/api/v3.1/connected_accounts",
            cast_to=ConnectedAccountListResponse,
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
    ) -> ConnectedAccountDeleteResponse:
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCompleteAuthResponse: ...

    @overload
    def complete_auth(
        self,
        body: BodyParam,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCompleteAuthResponse: ...

    def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCompleteAuthResponse:
        body_fields = compact(
            {
                "session_uri": session_uri,
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("session_uri", "user_id"),
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
            "/api/v3.1/connected_accounts/complete_auth",
            cast_to=ConnectedAccountCompleteAuthResponse,
            operation=_COMPLETE_AUTH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountCompleteAuthBody,
            options=options_data,
        )

    def patch(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        alias: str | Omit = omit,
        connection: connected_account_patch_params.Connection | Omit = omit,
        experimental: connected_account_patch_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountPatchResponse:
        body_fields = compact(
            {
                "alias": alias,
                "connection": connection,
                "experimental": experimental,
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountPatchResponse,
            operation=_PATCH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountPatchBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def refresh(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        query_redirect_url: str | Omit = omit,
        body_redirect_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountRefreshResponse:
        body_fields = compact(
            {
                "redirect_url": body_redirect_url,
            }
        )
        body_data = merge_body(body, body_fields)
        query_fields = compact(
            {
                "redirect_url": query_redirect_url,
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
            "post",
            build_path(
                "/api/v3.1/connected_accounts/{nanoid}/refresh",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRefreshResponse,
            operation=_REFRESH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountRefreshBody,
            query=query_data,
            options=options_data,
        )

    def revoke(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountRevokeResponse:
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
                "/api/v3.1/connected_accounts/{nanoid}/revoke",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRevokeResponse,
            operation=_REVOKE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountUpdateStatusResponse: ...

    @overload
    def update_status(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountUpdateStatusResponse: ...

    def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountUpdateStatusResponse:
        body_fields = compact(
            {
                "enabled": enabled,
            }
        )
        require_fields(
            body,
            body_fields,
            ("enabled",),
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
                "/api/v3.1/connected_accounts/{nanoId}/status",
                {"nanoId": nano_id},
            ),
            cast_to=ConnectedAccountUpdateStatusResponse,
            operation=_UPDATE_STATUS_OPERATION,
            body=body_data,
            body_model=ConnectedAccountUpdateStatusBody,
            options=options_data,
        )


class AsyncConnectedAccountsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConnectedAccountsResourceWithRawResponse:
        return AsyncConnectedAccountsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConnectedAccountsResourceWithStreamingResponse:
        return AsyncConnectedAccountsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig,
        connection: connected_account_create_params.Connection,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCreateResponse:
        body_fields = compact(
            {
                "auth_config": auth_config,
                "connection": connection,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config", "connection"),
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
            "/api/v3.1/connected_accounts",
            cast_to=ConnectedAccountCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ConnectedAccountCreateBody,
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
    ) -> ConnectedAccountRetrieveResponse:
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        statuses: list[
            Literal["INITIALIZING", "INITIATED", "ACTIVE", "FAILED", "EXPIRED", "INACTIVE", "REVOKED"]
        ]
        | None
        | Omit = omit,
        cursor: str | None | Omit = omit,
        limit: float | None | Omit = omit,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | None | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | None | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        account_type: Literal["PRIVATE", "SHARED", "ALL"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountListResponse:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "statuses": statuses,
                "cursor": cursor,
                "limit": limit,
                "user_ids": user_ids,
                "auth_config_ids": auth_config_ids,
                "connected_account_ids": connected_account_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "account_type": account_type,
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
            "/api/v3.1/connected_accounts",
            cast_to=ConnectedAccountListResponse,
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
    ) -> ConnectedAccountDeleteResponse:
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCompleteAuthResponse: ...

    @overload
    async def complete_auth(
        self,
        body: BodyParam,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCompleteAuthResponse: ...

    async def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountCompleteAuthResponse:
        body_fields = compact(
            {
                "session_uri": session_uri,
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("session_uri", "user_id"),
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
            "/api/v3.1/connected_accounts/complete_auth",
            cast_to=ConnectedAccountCompleteAuthResponse,
            operation=_COMPLETE_AUTH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountCompleteAuthBody,
            options=options_data,
        )

    async def patch(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        alias: str | Omit = omit,
        connection: connected_account_patch_params.Connection | Omit = omit,
        experimental: connected_account_patch_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountPatchResponse:
        body_fields = compact(
            {
                "alias": alias,
                "connection": connection,
                "experimental": experimental,
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountPatchResponse,
            operation=_PATCH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountPatchBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def refresh(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        query_redirect_url: str | Omit = omit,
        body_redirect_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountRefreshResponse:
        body_fields = compact(
            {
                "redirect_url": body_redirect_url,
            }
        )
        body_data = merge_body(body, body_fields)
        query_fields = compact(
            {
                "redirect_url": query_redirect_url,
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
            "post",
            build_path(
                "/api/v3.1/connected_accounts/{nanoid}/refresh",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRefreshResponse,
            operation=_REFRESH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountRefreshBody,
            query=query_data,
            options=options_data,
        )

    async def revoke(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountRevokeResponse:
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
                "/api/v3.1/connected_accounts/{nanoid}/revoke",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRevokeResponse,
            operation=_REVOKE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountUpdateStatusResponse: ...

    @overload
    async def update_status(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountUpdateStatusResponse: ...

    async def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConnectedAccountUpdateStatusResponse:
        body_fields = compact(
            {
                "enabled": enabled,
            }
        )
        require_fields(
            body,
            body_fields,
            ("enabled",),
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
                "/api/v3.1/connected_accounts/{nanoId}/status",
                {"nanoId": nano_id},
            ),
            cast_to=ConnectedAccountUpdateStatusResponse,
            operation=_UPDATE_STATUS_OPERATION,
            body=body_data,
            body_model=ConnectedAccountUpdateStatusBody,
            options=options_data,
        )


class ConnectedAccountsResourceWithRawResponse:
    def __init__(self, resource: ConnectedAccountsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig,
        connection: connected_account_create_params.Connection,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountCreateResponse]:
        body_fields = compact(
            {
                "auth_config": auth_config,
                "connection": connection,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config", "connection"),
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
            "/api/v3.1/connected_accounts",
            cast_to=ConnectedAccountCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ConnectedAccountCreateBody,
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
    ) -> APIResponse[ConnectedAccountRetrieveResponse]:
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        statuses: list[
            Literal["INITIALIZING", "INITIATED", "ACTIVE", "FAILED", "EXPIRED", "INACTIVE", "REVOKED"]
        ]
        | None
        | Omit = omit,
        cursor: str | None | Omit = omit,
        limit: float | None | Omit = omit,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | None | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | None | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        account_type: Literal["PRIVATE", "SHARED", "ALL"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountListResponse]:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "statuses": statuses,
                "cursor": cursor,
                "limit": limit,
                "user_ids": user_ids,
                "auth_config_ids": auth_config_ids,
                "connected_account_ids": connected_account_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "account_type": account_type,
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
            "/api/v3.1/connected_accounts",
            cast_to=ConnectedAccountListResponse,
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
    ) -> APIResponse[ConnectedAccountDeleteResponse]:
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountCompleteAuthResponse]: ...

    @overload
    def complete_auth(
        self,
        body: BodyParam,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountCompleteAuthResponse]: ...

    def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountCompleteAuthResponse]:
        body_fields = compact(
            {
                "session_uri": session_uri,
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("session_uri", "user_id"),
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
            "/api/v3.1/connected_accounts/complete_auth",
            cast_to=ConnectedAccountCompleteAuthResponse,
            operation=_COMPLETE_AUTH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountCompleteAuthBody,
            options=options_data,
        )

    def patch(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        alias: str | Omit = omit,
        connection: connected_account_patch_params.Connection | Omit = omit,
        experimental: connected_account_patch_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountPatchResponse]:
        body_fields = compact(
            {
                "alias": alias,
                "connection": connection,
                "experimental": experimental,
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountPatchResponse,
            operation=_PATCH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountPatchBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def refresh(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        query_redirect_url: str | Omit = omit,
        body_redirect_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountRefreshResponse]:
        body_fields = compact(
            {
                "redirect_url": body_redirect_url,
            }
        )
        body_data = merge_body(body, body_fields)
        query_fields = compact(
            {
                "redirect_url": query_redirect_url,
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
            "post",
            build_path(
                "/api/v3.1/connected_accounts/{nanoid}/refresh",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRefreshResponse,
            operation=_REFRESH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountRefreshBody,
            query=query_data,
            options=options_data,
        )

    def revoke(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountRevokeResponse]:
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
                "/api/v3.1/connected_accounts/{nanoid}/revoke",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRevokeResponse,
            operation=_REVOKE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountUpdateStatusResponse]: ...

    @overload
    def update_status(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountUpdateStatusResponse]: ...

    def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConnectedAccountUpdateStatusResponse]:
        body_fields = compact(
            {
                "enabled": enabled,
            }
        )
        require_fields(
            body,
            body_fields,
            ("enabled",),
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
                "/api/v3.1/connected_accounts/{nanoId}/status",
                {"nanoId": nano_id},
            ),
            cast_to=ConnectedAccountUpdateStatusResponse,
            operation=_UPDATE_STATUS_OPERATION,
            body=body_data,
            body_model=ConnectedAccountUpdateStatusBody,
            options=options_data,
        )


class AsyncConnectedAccountsResourceWithRawResponse:
    def __init__(self, resource: AsyncConnectedAccountsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig,
        connection: connected_account_create_params.Connection,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountCreateResponse]:
        body_fields = compact(
            {
                "auth_config": auth_config,
                "connection": connection,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config", "connection"),
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
            "/api/v3.1/connected_accounts",
            cast_to=ConnectedAccountCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ConnectedAccountCreateBody,
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
    ) -> AsyncAPIResponse[ConnectedAccountRetrieveResponse]:
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        statuses: list[
            Literal["INITIALIZING", "INITIATED", "ACTIVE", "FAILED", "EXPIRED", "INACTIVE", "REVOKED"]
        ]
        | None
        | Omit = omit,
        cursor: str | None | Omit = omit,
        limit: float | None | Omit = omit,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | None | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | None | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        account_type: Literal["PRIVATE", "SHARED", "ALL"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountListResponse]:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "statuses": statuses,
                "cursor": cursor,
                "limit": limit,
                "user_ids": user_ids,
                "auth_config_ids": auth_config_ids,
                "connected_account_ids": connected_account_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "account_type": account_type,
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
            "/api/v3.1/connected_accounts",
            cast_to=ConnectedAccountListResponse,
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
    ) -> AsyncAPIResponse[ConnectedAccountDeleteResponse]:
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountCompleteAuthResponse]: ...

    @overload
    async def complete_auth(
        self,
        body: BodyParam,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountCompleteAuthResponse]: ...

    async def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountCompleteAuthResponse]:
        body_fields = compact(
            {
                "session_uri": session_uri,
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("session_uri", "user_id"),
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
            "/api/v3.1/connected_accounts/complete_auth",
            cast_to=ConnectedAccountCompleteAuthResponse,
            operation=_COMPLETE_AUTH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountCompleteAuthBody,
            options=options_data,
        )

    async def patch(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        alias: str | Omit = omit,
        connection: connected_account_patch_params.Connection | Omit = omit,
        experimental: connected_account_patch_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountPatchResponse]:
        body_fields = compact(
            {
                "alias": alias,
                "connection": connection,
                "experimental": experimental,
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
                "/api/v3.1/connected_accounts/{nanoid}",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountPatchResponse,
            operation=_PATCH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountPatchBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def refresh(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        query_redirect_url: str | Omit = omit,
        body_redirect_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountRefreshResponse]:
        body_fields = compact(
            {
                "redirect_url": body_redirect_url,
            }
        )
        body_data = merge_body(body, body_fields)
        query_fields = compact(
            {
                "redirect_url": query_redirect_url,
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
            "post",
            build_path(
                "/api/v3.1/connected_accounts/{nanoid}/refresh",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRefreshResponse,
            operation=_REFRESH_OPERATION,
            body=body_data,
            body_model=ConnectedAccountRefreshBody,
            query=query_data,
            options=options_data,
        )

    async def revoke(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountRevokeResponse]:
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
                "/api/v3.1/connected_accounts/{nanoid}/revoke",
                {"nanoid": nanoid},
            ),
            cast_to=ConnectedAccountRevokeResponse,
            operation=_REVOKE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountUpdateStatusResponse]: ...

    @overload
    async def update_status(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountUpdateStatusResponse]: ...

    async def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConnectedAccountUpdateStatusResponse]:
        body_fields = compact(
            {
                "enabled": enabled,
            }
        )
        require_fields(
            body,
            body_fields,
            ("enabled",),
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
                "/api/v3.1/connected_accounts/{nanoId}/status",
                {"nanoId": nano_id},
            ),
            cast_to=ConnectedAccountUpdateStatusResponse,
            operation=_UPDATE_STATUS_OPERATION,
            body=body_data,
            body_model=ConnectedAccountUpdateStatusBody,
            options=options_data,
        )


class ConnectedAccountsResourceWithStreamingResponse:
    def __init__(self, resource: ConnectedAccountsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig,
        connection: connected_account_create_params.Connection,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountCreateResponse]]:
        body_fields = compact(
            {
                "auth_config": auth_config,
                "connection": connection,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config", "connection"),
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
                "/api/v3.1/connected_accounts",
                cast_to=ConnectedAccountCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=ConnectedAccountCreateBody,
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
    ) -> ResponseContextManager[APIResponse[ConnectedAccountRetrieveResponse]]:
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
                    "/api/v3.1/connected_accounts/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        statuses: list[
            Literal["INITIALIZING", "INITIATED", "ACTIVE", "FAILED", "EXPIRED", "INACTIVE", "REVOKED"]
        ]
        | None
        | Omit = omit,
        cursor: str | None | Omit = omit,
        limit: float | None | Omit = omit,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | None | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | None | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        account_type: Literal["PRIVATE", "SHARED", "ALL"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountListResponse]]:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "statuses": statuses,
                "cursor": cursor,
                "limit": limit,
                "user_ids": user_ids,
                "auth_config_ids": auth_config_ids,
                "connected_account_ids": connected_account_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "account_type": account_type,
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
                "/api/v3.1/connected_accounts",
                cast_to=ConnectedAccountListResponse,
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
    ) -> ResponseContextManager[APIResponse[ConnectedAccountDeleteResponse]]:
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
                    "/api/v3.1/connected_accounts/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountDeleteResponse,
                operation=_DELETE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountCompleteAuthResponse]]: ...

    @overload
    def complete_auth(
        self,
        body: BodyParam,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountCompleteAuthResponse]]: ...

    def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountCompleteAuthResponse]]:
        body_fields = compact(
            {
                "session_uri": session_uri,
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("session_uri", "user_id"),
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
                "/api/v3.1/connected_accounts/complete_auth",
                cast_to=ConnectedAccountCompleteAuthResponse,
                operation=_COMPLETE_AUTH_OPERATION,
                body=body_data,
                body_model=ConnectedAccountCompleteAuthBody,
                options=options_data,
                stream=True,
            )
        )

    def patch(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        alias: str | Omit = omit,
        connection: connected_account_patch_params.Connection | Omit = omit,
        experimental: connected_account_patch_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountPatchResponse]]:
        body_fields = compact(
            {
                "alias": alias,
                "connection": connection,
                "experimental": experimental,
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
                    "/api/v3.1/connected_accounts/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountPatchResponse,
                operation=_PATCH_OPERATION,
                body=body_data,
                body_model=ConnectedAccountPatchBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def refresh(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        query_redirect_url: str | Omit = omit,
        body_redirect_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountRefreshResponse]]:
        body_fields = compact(
            {
                "redirect_url": body_redirect_url,
            }
        )
        body_data = merge_body(body, body_fields)
        query_fields = compact(
            {
                "redirect_url": query_redirect_url,
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
                "post",
                build_path(
                    "/api/v3.1/connected_accounts/{nanoid}/refresh",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountRefreshResponse,
                operation=_REFRESH_OPERATION,
                body=body_data,
                body_model=ConnectedAccountRefreshBody,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def revoke(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountRevokeResponse]]:
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
                    "/api/v3.1/connected_accounts/{nanoid}/revoke",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountRevokeResponse,
                operation=_REVOKE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountUpdateStatusResponse]]: ...

    @overload
    def update_status(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountUpdateStatusResponse]]: ...

    def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConnectedAccountUpdateStatusResponse]]:
        body_fields = compact(
            {
                "enabled": enabled,
            }
        )
        require_fields(
            body,
            body_fields,
            ("enabled",),
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
                    "/api/v3.1/connected_accounts/{nanoId}/status",
                    {"nanoId": nano_id},
                ),
                cast_to=ConnectedAccountUpdateStatusResponse,
                operation=_UPDATE_STATUS_OPERATION,
                body=body_data,
                body_model=ConnectedAccountUpdateStatusBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncConnectedAccountsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncConnectedAccountsResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig,
        connection: connected_account_create_params.Connection,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        auth_config: connected_account_create_params.AuthConfig | Omit = omit,
        connection: connected_account_create_params.Connection | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountCreateResponse]]:
        body_fields = compact(
            {
                "auth_config": auth_config,
                "connection": connection,
            }
        )
        require_fields(
            body,
            body_fields,
            ("auth_config", "connection"),
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
                "/api/v3.1/connected_accounts",
                cast_to=ConnectedAccountCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=ConnectedAccountCreateBody,
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
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountRetrieveResponse]]:
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
                    "/api/v3.1/connected_accounts/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        statuses: list[
            Literal["INITIALIZING", "INITIATED", "ACTIVE", "FAILED", "EXPIRED", "INACTIVE", "REVOKED"]
        ]
        | None
        | Omit = omit,
        cursor: str | None | Omit = omit,
        limit: float | None | Omit = omit,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | None | Omit = omit,
        connected_account_ids: SequenceNotStr[str] | None | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        account_type: Literal["PRIVATE", "SHARED", "ALL"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountListResponse]]:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "statuses": statuses,
                "cursor": cursor,
                "limit": limit,
                "user_ids": user_ids,
                "auth_config_ids": auth_config_ids,
                "connected_account_ids": connected_account_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "account_type": account_type,
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
                "/api/v3.1/connected_accounts",
                cast_to=ConnectedAccountListResponse,
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
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountDeleteResponse]]:
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
                    "/api/v3.1/connected_accounts/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountDeleteResponse,
                operation=_DELETE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountCompleteAuthResponse]]: ...

    @overload
    def complete_auth(
        self,
        body: BodyParam,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountCompleteAuthResponse]]: ...

    def complete_auth(
        self,
        body: BodyParam | None = None,
        *,
        session_uri: str | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountCompleteAuthResponse]]:
        body_fields = compact(
            {
                "session_uri": session_uri,
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("session_uri", "user_id"),
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
                "/api/v3.1/connected_accounts/complete_auth",
                cast_to=ConnectedAccountCompleteAuthResponse,
                operation=_COMPLETE_AUTH_OPERATION,
                body=body_data,
                body_model=ConnectedAccountCompleteAuthBody,
                options=options_data,
                stream=True,
            )
        )

    def patch(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        alias: str | Omit = omit,
        connection: connected_account_patch_params.Connection | Omit = omit,
        experimental: connected_account_patch_params.Experimental | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountPatchResponse]]:
        body_fields = compact(
            {
                "alias": alias,
                "connection": connection,
                "experimental": experimental,
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
                    "/api/v3.1/connected_accounts/{nanoid}",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountPatchResponse,
                operation=_PATCH_OPERATION,
                body=body_data,
                body_model=ConnectedAccountPatchBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def refresh(
        self,
        nanoid: str,
        body: BodyParam | None = None,
        *,
        query_redirect_url: str | Omit = omit,
        body_redirect_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountRefreshResponse]]:
        body_fields = compact(
            {
                "redirect_url": body_redirect_url,
            }
        )
        body_data = merge_body(body, body_fields)
        query_fields = compact(
            {
                "redirect_url": query_redirect_url,
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
                "post",
                build_path(
                    "/api/v3.1/connected_accounts/{nanoid}/refresh",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountRefreshResponse,
                operation=_REFRESH_OPERATION,
                body=body_data,
                body_model=ConnectedAccountRefreshBody,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def revoke(
        self,
        nanoid: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountRevokeResponse]]:
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
                    "/api/v3.1/connected_accounts/{nanoid}/revoke",
                    {"nanoid": nanoid},
                ),
                cast_to=ConnectedAccountRevokeResponse,
                operation=_REVOKE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountUpdateStatusResponse]]: ...

    @overload
    def update_status(
        self,
        nano_id: str,
        body: BodyParam,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountUpdateStatusResponse]]: ...

    def update_status(
        self,
        nano_id: str,
        body: BodyParam | None = None,
        *,
        enabled: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConnectedAccountUpdateStatusResponse]]:
        body_fields = compact(
            {
                "enabled": enabled,
            }
        )
        require_fields(
            body,
            body_fields,
            ("enabled",),
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
                    "/api/v3.1/connected_accounts/{nanoId}/status",
                    {"nanoId": nano_id},
                ),
                cast_to=ConnectedAccountUpdateStatusResponse,
                operation=_UPDATE_STATUS_OPERATION,
                body=body_data,
                body_model=ConnectedAccountUpdateStatusBody,
                options=options_data,
                stream=True,
            )
        )
