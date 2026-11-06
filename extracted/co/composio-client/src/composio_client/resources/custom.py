# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.custom`` — the generated resource classes.

``CustomResource`` (sync) and ``AsyncCustomResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import cached_property
from typing import Literal

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, QueryParam, RequestOptions
from .._models import CustomCreateToolkitBody, CustomSyncBody, CustomUpdateToolkitsBody, CustomUpsertBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ..types import custom_create_toolkit_params, custom_update_toolkits_params, custom_upsert_params
from ..types.custom_create_toolkit_response import CustomCreateToolkitResponse
from ..types.custom_delete_toolkit_response import CustomDeleteToolkitResponse
from ..types.custom_sync_response import CustomSyncResponse
from ..types.custom_update_toolkits_response import CustomUpdateToolkitsResponse
from ..types.custom_upsert_response import CustomUpsertResponse
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

_CREATE_TOOLKIT_OPERATION = OPERATIONS_BY_CHAIN[("custom", "create_toolkit")]
_DELETE_TOOLKIT_OPERATION = OPERATIONS_BY_CHAIN[("custom", "delete_toolkit")]
_SYNC_OPERATION = OPERATIONS_BY_CHAIN[("custom", "sync")]
_UPDATE_TOOLKITS_OPERATION = OPERATIONS_BY_CHAIN[("custom", "update_toolkits")]
_UPSERT_OPERATION = OPERATIONS_BY_CHAIN[("custom", "upsert")]


class CustomResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CustomResourceWithRawResponse:
        return CustomResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomResourceWithStreamingResponse:
        return CustomResourceWithStreamingResponse(self)

    @overload
    def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        mcp_url: str,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ],
        user_id: Literal["all"] | str,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateToolkitResponse: ...

    @overload
    def create_toolkit(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateToolkitResponse: ...

    def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateToolkitResponse:
        body_fields = compact(
            {
                "name": name,
                "mcp_url": mcp_url,
                "logo_file": logo_file,
                "auth_schemes": auth_schemes,
                "user_id": user_id,
                "callback_url": callback_url,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "mcp_url", "auth_schemes", "user_id"),
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
            "/api/v3.1/custom/toolkits",
            cast_to=CustomCreateToolkitResponse,
            operation=_CREATE_TOOLKIT_OPERATION,
            body=body_data,
            body_model=CustomCreateToolkitBody,
            options=options_data,
        )

    def delete_toolkit(
        self,
        slug: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CustomDeleteToolkitResponse:
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
                "/api/v3.1/custom/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=CustomDeleteToolkitResponse,
            operation=_DELETE_TOOLKIT_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomSyncResponse: ...

    @overload
    def sync(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomSyncResponse: ...

    def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomSyncResponse:
        body_fields = compact(
            {
                "slug": slug,
                "connected_account_id": connected_account_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
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
            "/api/v3.1/custom/toolkits/sync",
            cast_to=CustomSyncResponse,
            operation=_SYNC_OPERATION,
            body=body_data,
            body_model=CustomSyncBody,
            options=options_data,
        )

    def update_toolkits(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        logo_file: custom_update_toolkits_params.LogoFile | Omit = omit,
        api_key_field: custom_update_toolkits_params.ApiKeyField | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomUpdateToolkitsResponse:
        body_fields = compact(
            {
                "name": name,
                "logo_file": logo_file,
                "api_key_field": api_key_field,
                "user_id": user_id,
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
                "/api/v3.1/custom/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=CustomUpdateToolkitsResponse,
            operation=_UPDATE_TOOLKITS_OPERATION,
            body=body_data,
            body_model=CustomUpdateToolkitsBody,
            options=options_data,
        )

    @overload
    def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        toolkit_config: custom_upsert_params.ToolkitConfig,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomUpsertResponse: ...

    @overload
    def upsert(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomUpsertResponse: ...

    def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomUpsertResponse:
        body_fields = compact(
            {
                "slug": slug,
                "toolkit_config": toolkit_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug", "toolkit_config"),
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
            "/api/v3.1/custom/toolkits/upsert",
            cast_to=CustomUpsertResponse,
            operation=_UPSERT_OPERATION,
            body=body_data,
            body_model=CustomUpsertBody,
            options=options_data,
        )


class AsyncCustomResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCustomResourceWithRawResponse:
        return AsyncCustomResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomResourceWithStreamingResponse:
        return AsyncCustomResourceWithStreamingResponse(self)

    @overload
    async def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        mcp_url: str,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ],
        user_id: Literal["all"] | str,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateToolkitResponse: ...

    @overload
    async def create_toolkit(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateToolkitResponse: ...

    async def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomCreateToolkitResponse:
        body_fields = compact(
            {
                "name": name,
                "mcp_url": mcp_url,
                "logo_file": logo_file,
                "auth_schemes": auth_schemes,
                "user_id": user_id,
                "callback_url": callback_url,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "mcp_url", "auth_schemes", "user_id"),
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
            "/api/v3.1/custom/toolkits",
            cast_to=CustomCreateToolkitResponse,
            operation=_CREATE_TOOLKIT_OPERATION,
            body=body_data,
            body_model=CustomCreateToolkitBody,
            options=options_data,
        )

    async def delete_toolkit(
        self,
        slug: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> CustomDeleteToolkitResponse:
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
                "/api/v3.1/custom/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=CustomDeleteToolkitResponse,
            operation=_DELETE_TOOLKIT_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomSyncResponse: ...

    @overload
    async def sync(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomSyncResponse: ...

    async def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomSyncResponse:
        body_fields = compact(
            {
                "slug": slug,
                "connected_account_id": connected_account_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
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
            "/api/v3.1/custom/toolkits/sync",
            cast_to=CustomSyncResponse,
            operation=_SYNC_OPERATION,
            body=body_data,
            body_model=CustomSyncBody,
            options=options_data,
        )

    async def update_toolkits(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        logo_file: custom_update_toolkits_params.LogoFile | Omit = omit,
        api_key_field: custom_update_toolkits_params.ApiKeyField | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomUpdateToolkitsResponse:
        body_fields = compact(
            {
                "name": name,
                "logo_file": logo_file,
                "api_key_field": api_key_field,
                "user_id": user_id,
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
                "/api/v3.1/custom/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=CustomUpdateToolkitsResponse,
            operation=_UPDATE_TOOLKITS_OPERATION,
            body=body_data,
            body_model=CustomUpdateToolkitsBody,
            options=options_data,
        )

    @overload
    async def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        toolkit_config: custom_upsert_params.ToolkitConfig,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomUpsertResponse: ...

    @overload
    async def upsert(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomUpsertResponse: ...

    async def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> CustomUpsertResponse:
        body_fields = compact(
            {
                "slug": slug,
                "toolkit_config": toolkit_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug", "toolkit_config"),
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
            "/api/v3.1/custom/toolkits/upsert",
            cast_to=CustomUpsertResponse,
            operation=_UPSERT_OPERATION,
            body=body_data,
            body_model=CustomUpsertBody,
            options=options_data,
        )


class CustomResourceWithRawResponse:
    def __init__(self, resource: CustomResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        mcp_url: str,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ],
        user_id: Literal["all"] | str,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomCreateToolkitResponse]: ...

    @overload
    def create_toolkit(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomCreateToolkitResponse]: ...

    def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomCreateToolkitResponse]:
        body_fields = compact(
            {
                "name": name,
                "mcp_url": mcp_url,
                "logo_file": logo_file,
                "auth_schemes": auth_schemes,
                "user_id": user_id,
                "callback_url": callback_url,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "mcp_url", "auth_schemes", "user_id"),
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
            "/api/v3.1/custom/toolkits",
            cast_to=CustomCreateToolkitResponse,
            operation=_CREATE_TOOLKIT_OPERATION,
            body=body_data,
            body_model=CustomCreateToolkitBody,
            options=options_data,
        )

    def delete_toolkit(
        self,
        slug: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomDeleteToolkitResponse]:
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
                "/api/v3.1/custom/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=CustomDeleteToolkitResponse,
            operation=_DELETE_TOOLKIT_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomSyncResponse]: ...

    @overload
    def sync(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomSyncResponse]: ...

    def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomSyncResponse]:
        body_fields = compact(
            {
                "slug": slug,
                "connected_account_id": connected_account_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
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
            "/api/v3.1/custom/toolkits/sync",
            cast_to=CustomSyncResponse,
            operation=_SYNC_OPERATION,
            body=body_data,
            body_model=CustomSyncBody,
            options=options_data,
        )

    def update_toolkits(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        logo_file: custom_update_toolkits_params.LogoFile | Omit = omit,
        api_key_field: custom_update_toolkits_params.ApiKeyField | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomUpdateToolkitsResponse]:
        body_fields = compact(
            {
                "name": name,
                "logo_file": logo_file,
                "api_key_field": api_key_field,
                "user_id": user_id,
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
                "/api/v3.1/custom/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=CustomUpdateToolkitsResponse,
            operation=_UPDATE_TOOLKITS_OPERATION,
            body=body_data,
            body_model=CustomUpdateToolkitsBody,
            options=options_data,
        )

    @overload
    def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        toolkit_config: custom_upsert_params.ToolkitConfig,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomUpsertResponse]: ...

    @overload
    def upsert(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomUpsertResponse]: ...

    def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[CustomUpsertResponse]:
        body_fields = compact(
            {
                "slug": slug,
                "toolkit_config": toolkit_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug", "toolkit_config"),
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
            "/api/v3.1/custom/toolkits/upsert",
            cast_to=CustomUpsertResponse,
            operation=_UPSERT_OPERATION,
            body=body_data,
            body_model=CustomUpsertBody,
            options=options_data,
        )


class AsyncCustomResourceWithRawResponse:
    def __init__(self, resource: AsyncCustomResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        mcp_url: str,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ],
        user_id: Literal["all"] | str,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomCreateToolkitResponse]: ...

    @overload
    async def create_toolkit(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomCreateToolkitResponse]: ...

    async def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomCreateToolkitResponse]:
        body_fields = compact(
            {
                "name": name,
                "mcp_url": mcp_url,
                "logo_file": logo_file,
                "auth_schemes": auth_schemes,
                "user_id": user_id,
                "callback_url": callback_url,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "mcp_url", "auth_schemes", "user_id"),
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
            "/api/v3.1/custom/toolkits",
            cast_to=CustomCreateToolkitResponse,
            operation=_CREATE_TOOLKIT_OPERATION,
            body=body_data,
            body_model=CustomCreateToolkitBody,
            options=options_data,
        )

    async def delete_toolkit(
        self,
        slug: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomDeleteToolkitResponse]:
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
                "/api/v3.1/custom/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=CustomDeleteToolkitResponse,
            operation=_DELETE_TOOLKIT_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomSyncResponse]: ...

    @overload
    async def sync(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomSyncResponse]: ...

    async def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomSyncResponse]:
        body_fields = compact(
            {
                "slug": slug,
                "connected_account_id": connected_account_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
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
            "/api/v3.1/custom/toolkits/sync",
            cast_to=CustomSyncResponse,
            operation=_SYNC_OPERATION,
            body=body_data,
            body_model=CustomSyncBody,
            options=options_data,
        )

    async def update_toolkits(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        logo_file: custom_update_toolkits_params.LogoFile | Omit = omit,
        api_key_field: custom_update_toolkits_params.ApiKeyField | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomUpdateToolkitsResponse]:
        body_fields = compact(
            {
                "name": name,
                "logo_file": logo_file,
                "api_key_field": api_key_field,
                "user_id": user_id,
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
                "/api/v3.1/custom/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=CustomUpdateToolkitsResponse,
            operation=_UPDATE_TOOLKITS_OPERATION,
            body=body_data,
            body_model=CustomUpdateToolkitsBody,
            options=options_data,
        )

    @overload
    async def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        toolkit_config: custom_upsert_params.ToolkitConfig,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomUpsertResponse]: ...

    @overload
    async def upsert(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomUpsertResponse]: ...

    async def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[CustomUpsertResponse]:
        body_fields = compact(
            {
                "slug": slug,
                "toolkit_config": toolkit_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug", "toolkit_config"),
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
            "/api/v3.1/custom/toolkits/upsert",
            cast_to=CustomUpsertResponse,
            operation=_UPSERT_OPERATION,
            body=body_data,
            body_model=CustomUpsertBody,
            options=options_data,
        )


class CustomResourceWithStreamingResponse:
    def __init__(self, resource: CustomResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        mcp_url: str,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ],
        user_id: Literal["all"] | str,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomCreateToolkitResponse]]: ...

    @overload
    def create_toolkit(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomCreateToolkitResponse]]: ...

    def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomCreateToolkitResponse]]:
        body_fields = compact(
            {
                "name": name,
                "mcp_url": mcp_url,
                "logo_file": logo_file,
                "auth_schemes": auth_schemes,
                "user_id": user_id,
                "callback_url": callback_url,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "mcp_url", "auth_schemes", "user_id"),
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
                "/api/v3.1/custom/toolkits",
                cast_to=CustomCreateToolkitResponse,
                operation=_CREATE_TOOLKIT_OPERATION,
                body=body_data,
                body_model=CustomCreateToolkitBody,
                options=options_data,
                stream=True,
            )
        )

    def delete_toolkit(
        self,
        slug: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomDeleteToolkitResponse]]:
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
                    "/api/v3.1/custom/toolkits/{slug}",
                    {"slug": slug},
                ),
                cast_to=CustomDeleteToolkitResponse,
                operation=_DELETE_TOOLKIT_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomSyncResponse]]: ...

    @overload
    def sync(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomSyncResponse]]: ...

    def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomSyncResponse]]:
        body_fields = compact(
            {
                "slug": slug,
                "connected_account_id": connected_account_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
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
                "/api/v3.1/custom/toolkits/sync",
                cast_to=CustomSyncResponse,
                operation=_SYNC_OPERATION,
                body=body_data,
                body_model=CustomSyncBody,
                options=options_data,
                stream=True,
            )
        )

    def update_toolkits(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        logo_file: custom_update_toolkits_params.LogoFile | Omit = omit,
        api_key_field: custom_update_toolkits_params.ApiKeyField | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomUpdateToolkitsResponse]]:
        body_fields = compact(
            {
                "name": name,
                "logo_file": logo_file,
                "api_key_field": api_key_field,
                "user_id": user_id,
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
                    "/api/v3.1/custom/toolkits/{slug}",
                    {"slug": slug},
                ),
                cast_to=CustomUpdateToolkitsResponse,
                operation=_UPDATE_TOOLKITS_OPERATION,
                body=body_data,
                body_model=CustomUpdateToolkitsBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        toolkit_config: custom_upsert_params.ToolkitConfig,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomUpsertResponse]]: ...

    @overload
    def upsert(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomUpsertResponse]]: ...

    def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[CustomUpsertResponse]]:
        body_fields = compact(
            {
                "slug": slug,
                "toolkit_config": toolkit_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug", "toolkit_config"),
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
                "/api/v3.1/custom/toolkits/upsert",
                cast_to=CustomUpsertResponse,
                operation=_UPSERT_OPERATION,
                body=body_data,
                body_model=CustomUpsertBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncCustomResourceWithStreamingResponse:
    def __init__(self, resource: AsyncCustomResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        mcp_url: str,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ],
        user_id: Literal["all"] | str,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomCreateToolkitResponse]]: ...

    @overload
    def create_toolkit(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomCreateToolkitResponse]]: ...

    def create_toolkit(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        mcp_url: str | Omit = omit,
        logo_file: custom_create_toolkit_params.LogoFile | Omit = omit,
        auth_schemes: Iterable[
            custom_create_toolkit_params.AuthSchemeVariant0
            | custom_create_toolkit_params.AuthSchemeVariant1
            | custom_create_toolkit_params.AuthSchemeVariant2
        ]
        | Omit = omit,
        user_id: Literal["all"] | str | Omit = omit,
        callback_url: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomCreateToolkitResponse]]:
        body_fields = compact(
            {
                "name": name,
                "mcp_url": mcp_url,
                "logo_file": logo_file,
                "auth_schemes": auth_schemes,
                "user_id": user_id,
                "callback_url": callback_url,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "mcp_url", "auth_schemes", "user_id"),
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
                "/api/v3.1/custom/toolkits",
                cast_to=CustomCreateToolkitResponse,
                operation=_CREATE_TOOLKIT_OPERATION,
                body=body_data,
                body_model=CustomCreateToolkitBody,
                options=options_data,
                stream=True,
            )
        )

    def delete_toolkit(
        self,
        slug: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomDeleteToolkitResponse]]:
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
                    "/api/v3.1/custom/toolkits/{slug}",
                    {"slug": slug},
                ),
                cast_to=CustomDeleteToolkitResponse,
                operation=_DELETE_TOOLKIT_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomSyncResponse]]: ...

    @overload
    def sync(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomSyncResponse]]: ...

    def sync(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        connected_account_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomSyncResponse]]:
        body_fields = compact(
            {
                "slug": slug,
                "connected_account_id": connected_account_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug",),
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
                "/api/v3.1/custom/toolkits/sync",
                cast_to=CustomSyncResponse,
                operation=_SYNC_OPERATION,
                body=body_data,
                body_model=CustomSyncBody,
                options=options_data,
                stream=True,
            )
        )

    def update_toolkits(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        logo_file: custom_update_toolkits_params.LogoFile | Omit = omit,
        api_key_field: custom_update_toolkits_params.ApiKeyField | Omit = omit,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomUpdateToolkitsResponse]]:
        body_fields = compact(
            {
                "name": name,
                "logo_file": logo_file,
                "api_key_field": api_key_field,
                "user_id": user_id,
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
                    "/api/v3.1/custom/toolkits/{slug}",
                    {"slug": slug},
                ),
                cast_to=CustomUpdateToolkitsResponse,
                operation=_UPDATE_TOOLKITS_OPERATION,
                body=body_data,
                body_model=CustomUpdateToolkitsBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str,
        toolkit_config: custom_upsert_params.ToolkitConfig,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomUpsertResponse]]: ...

    @overload
    def upsert(
        self,
        body: BodyParam,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomUpsertResponse]]: ...

    def upsert(
        self,
        body: BodyParam | None = None,
        *,
        slug: str | Omit = omit,
        toolkit_config: custom_upsert_params.ToolkitConfig | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[CustomUpsertResponse]]:
        body_fields = compact(
            {
                "slug": slug,
                "toolkit_config": toolkit_config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("slug", "toolkit_config"),
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
                "/api/v3.1/custom/toolkits/upsert",
                cast_to=CustomUpsertResponse,
                operation=_UPSERT_OPERATION,
                body=body_data,
                body_model=CustomUpsertBody,
                options=options_data,
                stream=True,
            )
        )
