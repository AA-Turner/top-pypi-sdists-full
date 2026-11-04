# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.mcp`` — the generated resource classes.

``McpResource`` (sync) and ``AsyncMcpResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Literal

import httpx
from typing_extensions import overload

from ..._base_client import BodyParam, QueryParam, RequestOptions
from ..._models import McpCreateBody, McpCreateInstanceBody, McpUpdateBody
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ...types.mcp_create_instance_response import McpCreateInstanceResponse
from ...types.mcp_create_response import McpCreateResponse
from ...types.mcp_delete_instance_response import McpDeleteInstanceResponse
from ...types.mcp_delete_response import McpDeleteResponse
from ...types.mcp_list_instances_response import McpListInstancesResponse
from ...types.mcp_list_response import McpListResponse
from ...types.mcp_retrieve_app_response import McpRetrieveAppResponse
from ...types.mcp_retrieve_response import McpRetrieveResponse
from ...types.mcp_update_response import McpUpdateResponse
from .._base import (
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
from .custom import AsyncCustomResource, CustomResource
from .generate import AsyncGenerateResource, GenerateResource

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "create")]
_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "retrieve")]
_UPDATE_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "update")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "list")]
_DELETE_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "delete")]
_CREATE_INSTANCE_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "create_instance")]
_DELETE_INSTANCE_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "delete_instance")]
_LIST_INSTANCES_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "list_instances")]
_RETRIEVE_APP_OPERATION = OPERATIONS_BY_CHAIN[("mcp", "retrieve_app")]


class McpResource(SyncAPIResource):
    custom: CustomResource
    generate: GenerateResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.custom = CustomResource(client)
        self.generate = GenerateResource(client)

    @cached_property
    def with_raw_response(self) -> McpResourceWithRawResponse:
        return McpResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> McpResourceWithStreamingResponse:
        return McpResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str],
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateResponse:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "no_auth_apps": no_auth_apps,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "auth_config_ids"),
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
            "/api/v3.1/mcp/servers",
            cast_to=McpCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=McpCreateBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpRetrieveResponse:
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpUpdateResponse:
        body_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
                "auth_config_ids": auth_config_ids,
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=McpUpdateBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def list(
        self,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> McpListResponse:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
            "/api/v3.1/mcp/servers",
            cast_to=McpListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpDeleteResponse:
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateInstanceResponse: ...

    @overload
    def create_instance(
        self,
        server_id: str,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateInstanceResponse: ...

    def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateInstanceResponse:
        body_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
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
                "/api/v3.1/mcp/servers/{serverId}/instances",
                {"serverId": server_id},
            ),
            cast_to=McpCreateInstanceResponse,
            operation=_CREATE_INSTANCE_OPERATION,
            body=body_data,
            body_model=McpCreateInstanceBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def delete_instance(
        self,
        instance_id: str,
        *,
        server_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpDeleteInstanceResponse: ...

    @overload
    def delete_instance(
        self,
        instance_id: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpDeleteInstanceResponse: ...

    def delete_instance(
        self,
        instance_id: str,
        *legacy_args: object,
        server_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpDeleteInstanceResponse:
        instance_id, (server_id,), _legacy_body = normalize_path_arguments(
            instance_id,
            legacy_args,
            leading_values=(server_id,),
            leading_names=("server_id",),
            trailing_name="instance_id",
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
            "delete",
            build_path(
                "/api/v3.1/mcp/servers/{serverId}/instances/{instanceId}",
                {"serverId": server_id, "instanceId": instance_id},
            ),
            cast_to=McpDeleteInstanceResponse,
            operation=_DELETE_INSTANCE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def list_instances(
        self,
        server_id: str,
        *,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        search: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> McpListInstancesResponse:
        query_fields = compact(
            {
                "page_no": page_no,
                "limit": limit,
                "search": search,
                "order_by": order_by,
                "order_direction": order_direction,
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
                "/api/v3.1/mcp/servers/{serverId}/instances",
                {"serverId": server_id},
            ),
            cast_to=McpListInstancesResponse,
            operation=_LIST_INSTANCES_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def retrieve_app(
        self,
        app_key: str,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> McpRetrieveAppResponse:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
                "/api/v3.1/mcp/app/{appKey}",
                {"appKey": app_key},
            ),
            cast_to=McpRetrieveAppResponse,
            operation=_RETRIEVE_APP_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncMcpResource(AsyncAPIResource):
    custom: AsyncCustomResource
    generate: AsyncGenerateResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.custom = AsyncCustomResource(client)
        self.generate = AsyncGenerateResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncMcpResourceWithRawResponse:
        return AsyncMcpResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMcpResourceWithStreamingResponse:
        return AsyncMcpResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str],
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateResponse:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "no_auth_apps": no_auth_apps,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "auth_config_ids"),
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
            "/api/v3.1/mcp/servers",
            cast_to=McpCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=McpCreateBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpRetrieveResponse:
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpUpdateResponse:
        body_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
                "auth_config_ids": auth_config_ids,
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=McpUpdateBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def list(
        self,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> McpListResponse:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
            "/api/v3.1/mcp/servers",
            cast_to=McpListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpDeleteResponse:
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateInstanceResponse: ...

    @overload
    async def create_instance(
        self,
        server_id: str,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateInstanceResponse: ...

    async def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpCreateInstanceResponse:
        body_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
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
                "/api/v3.1/mcp/servers/{serverId}/instances",
                {"serverId": server_id},
            ),
            cast_to=McpCreateInstanceResponse,
            operation=_CREATE_INSTANCE_OPERATION,
            body=body_data,
            body_model=McpCreateInstanceBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def delete_instance(
        self,
        instance_id: str,
        *,
        server_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpDeleteInstanceResponse: ...

    @overload
    async def delete_instance(
        self,
        instance_id: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpDeleteInstanceResponse: ...

    async def delete_instance(
        self,
        instance_id: str,
        *legacy_args: object,
        server_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> McpDeleteInstanceResponse:
        instance_id, (server_id,), _legacy_body = normalize_path_arguments(
            instance_id,
            legacy_args,
            leading_values=(server_id,),
            leading_names=("server_id",),
            trailing_name="instance_id",
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
            "delete",
            build_path(
                "/api/v3.1/mcp/servers/{serverId}/instances/{instanceId}",
                {"serverId": server_id, "instanceId": instance_id},
            ),
            cast_to=McpDeleteInstanceResponse,
            operation=_DELETE_INSTANCE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def list_instances(
        self,
        server_id: str,
        *,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        search: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> McpListInstancesResponse:
        query_fields = compact(
            {
                "page_no": page_no,
                "limit": limit,
                "search": search,
                "order_by": order_by,
                "order_direction": order_direction,
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
                "/api/v3.1/mcp/servers/{serverId}/instances",
                {"serverId": server_id},
            ),
            cast_to=McpListInstancesResponse,
            operation=_LIST_INSTANCES_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def retrieve_app(
        self,
        app_key: str,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> McpRetrieveAppResponse:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
                "/api/v3.1/mcp/app/{appKey}",
                {"appKey": app_key},
            ),
            cast_to=McpRetrieveAppResponse,
            operation=_RETRIEVE_APP_OPERATION,
            query=query_data,
            options=options_data,
        )


class McpResourceWithRawResponse:
    def __init__(self, resource: McpResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str],
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpCreateResponse]:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "no_auth_apps": no_auth_apps,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "auth_config_ids"),
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
            "/api/v3.1/mcp/servers",
            cast_to=McpCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=McpCreateBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpRetrieveResponse]:
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpUpdateResponse]:
        body_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
                "auth_config_ids": auth_config_ids,
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=McpUpdateBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def list(
        self,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpListResponse]:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
            "/api/v3.1/mcp/servers",
            cast_to=McpListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpDeleteResponse]:
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpCreateInstanceResponse]: ...

    @overload
    def create_instance(
        self,
        server_id: str,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpCreateInstanceResponse]: ...

    def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpCreateInstanceResponse]:
        body_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
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
                "/api/v3.1/mcp/servers/{serverId}/instances",
                {"serverId": server_id},
            ),
            cast_to=McpCreateInstanceResponse,
            operation=_CREATE_INSTANCE_OPERATION,
            body=body_data,
            body_model=McpCreateInstanceBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def delete_instance(
        self,
        instance_id: str,
        *,
        server_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpDeleteInstanceResponse]: ...

    @overload
    def delete_instance(
        self,
        instance_id: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpDeleteInstanceResponse]: ...

    def delete_instance(
        self,
        instance_id: str,
        *legacy_args: object,
        server_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpDeleteInstanceResponse]:
        instance_id, (server_id,), _legacy_body = normalize_path_arguments(
            instance_id,
            legacy_args,
            leading_values=(server_id,),
            leading_names=("server_id",),
            trailing_name="instance_id",
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
            "delete",
            build_path(
                "/api/v3.1/mcp/servers/{serverId}/instances/{instanceId}",
                {"serverId": server_id, "instanceId": instance_id},
            ),
            cast_to=McpDeleteInstanceResponse,
            operation=_DELETE_INSTANCE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def list_instances(
        self,
        server_id: str,
        *,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        search: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpListInstancesResponse]:
        query_fields = compact(
            {
                "page_no": page_no,
                "limit": limit,
                "search": search,
                "order_by": order_by,
                "order_direction": order_direction,
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
                "/api/v3.1/mcp/servers/{serverId}/instances",
                {"serverId": server_id},
            ),
            cast_to=McpListInstancesResponse,
            operation=_LIST_INSTANCES_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    def retrieve_app(
        self,
        app_key: str,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[McpRetrieveAppResponse]:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
                "/api/v3.1/mcp/app/{appKey}",
                {"appKey": app_key},
            ),
            cast_to=McpRetrieveAppResponse,
            operation=_RETRIEVE_APP_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncMcpResourceWithRawResponse:
    def __init__(self, resource: AsyncMcpResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str],
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpCreateResponse]:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "no_auth_apps": no_auth_apps,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "auth_config_ids"),
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
            "/api/v3.1/mcp/servers",
            cast_to=McpCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=McpCreateBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpRetrieveResponse]:
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpUpdateResponse]:
        body_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
                "auth_config_ids": auth_config_ids,
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpUpdateResponse,
            operation=_UPDATE_OPERATION,
            body=body_data,
            body_model=McpUpdateBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def list(
        self,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpListResponse]:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
            "/api/v3.1/mcp/servers",
            cast_to=McpListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpDeleteResponse]:
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
                "/api/v3.1/mcp/{id}",
                {"id": id},
            ),
            cast_to=McpDeleteResponse,
            operation=_DELETE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpCreateInstanceResponse]: ...

    @overload
    async def create_instance(
        self,
        server_id: str,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpCreateInstanceResponse]: ...

    async def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpCreateInstanceResponse]:
        body_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
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
                "/api/v3.1/mcp/servers/{serverId}/instances",
                {"serverId": server_id},
            ),
            cast_to=McpCreateInstanceResponse,
            operation=_CREATE_INSTANCE_OPERATION,
            body=body_data,
            body_model=McpCreateInstanceBody,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    async def delete_instance(
        self,
        instance_id: str,
        *,
        server_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpDeleteInstanceResponse]: ...

    @overload
    async def delete_instance(
        self,
        instance_id: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpDeleteInstanceResponse]: ...

    async def delete_instance(
        self,
        instance_id: str,
        *legacy_args: object,
        server_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpDeleteInstanceResponse]:
        instance_id, (server_id,), _legacy_body = normalize_path_arguments(
            instance_id,
            legacy_args,
            leading_values=(server_id,),
            leading_names=("server_id",),
            trailing_name="instance_id",
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
            "delete",
            build_path(
                "/api/v3.1/mcp/servers/{serverId}/instances/{instanceId}",
                {"serverId": server_id, "instanceId": instance_id},
            ),
            cast_to=McpDeleteInstanceResponse,
            operation=_DELETE_INSTANCE_OPERATION,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def list_instances(
        self,
        server_id: str,
        *,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        search: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpListInstancesResponse]:
        query_fields = compact(
            {
                "page_no": page_no,
                "limit": limit,
                "search": search,
                "order_by": order_by,
                "order_direction": order_direction,
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
                "/api/v3.1/mcp/servers/{serverId}/instances",
                {"serverId": server_id},
            ),
            cast_to=McpListInstancesResponse,
            operation=_LIST_INSTANCES_OPERATION,
            query=query_data,
            options=options_data,
        )

    # Deprecated in the input OpenAPI schema.
    async def retrieve_app(
        self,
        app_key: str,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[McpRetrieveAppResponse]:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
                "/api/v3.1/mcp/app/{appKey}",
                {"appKey": app_key},
            ),
            cast_to=McpRetrieveAppResponse,
            operation=_RETRIEVE_APP_OPERATION,
            query=query_data,
            options=options_data,
        )


class McpResourceWithStreamingResponse:
    def __init__(self, resource: McpResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str],
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpCreateResponse]]:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "no_auth_apps": no_auth_apps,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "auth_config_ids"),
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
                "/api/v3.1/mcp/servers",
                cast_to=McpCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=McpCreateBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpRetrieveResponse]]:
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
                    "/api/v3.1/mcp/{id}",
                    {"id": id},
                ),
                cast_to=McpRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpUpdateResponse]]:
        body_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
                "auth_config_ids": auth_config_ids,
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
                    "/api/v3.1/mcp/{id}",
                    {"id": id},
                ),
                cast_to=McpUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=McpUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def list(
        self,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpListResponse]]:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
                "/api/v3.1/mcp/servers",
                cast_to=McpListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpDeleteResponse]]:
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
                    "/api/v3.1/mcp/{id}",
                    {"id": id},
                ),
                cast_to=McpDeleteResponse,
                operation=_DELETE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpCreateInstanceResponse]]: ...

    @overload
    def create_instance(
        self,
        server_id: str,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpCreateInstanceResponse]]: ...

    def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpCreateInstanceResponse]]:
        body_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
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
                    "/api/v3.1/mcp/servers/{serverId}/instances",
                    {"serverId": server_id},
                ),
                cast_to=McpCreateInstanceResponse,
                operation=_CREATE_INSTANCE_OPERATION,
                body=body_data,
                body_model=McpCreateInstanceBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def delete_instance(
        self,
        instance_id: str,
        *,
        server_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpDeleteInstanceResponse]]: ...

    @overload
    def delete_instance(
        self,
        instance_id: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpDeleteInstanceResponse]]: ...

    def delete_instance(
        self,
        instance_id: str,
        *legacy_args: object,
        server_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpDeleteInstanceResponse]]:
        instance_id, (server_id,), _legacy_body = normalize_path_arguments(
            instance_id,
            legacy_args,
            leading_values=(server_id,),
            leading_names=("server_id",),
            trailing_name="instance_id",
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
                "delete",
                build_path(
                    "/api/v3.1/mcp/servers/{serverId}/instances/{instanceId}",
                    {"serverId": server_id, "instanceId": instance_id},
                ),
                cast_to=McpDeleteInstanceResponse,
                operation=_DELETE_INSTANCE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def list_instances(
        self,
        server_id: str,
        *,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        search: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpListInstancesResponse]]:
        query_fields = compact(
            {
                "page_no": page_no,
                "limit": limit,
                "search": search,
                "order_by": order_by,
                "order_direction": order_direction,
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
                    "/api/v3.1/mcp/servers/{serverId}/instances",
                    {"serverId": server_id},
                ),
                cast_to=McpListInstancesResponse,
                operation=_LIST_INSTANCES_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def retrieve_app(
        self,
        app_key: str,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[McpRetrieveAppResponse]]:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
                    "/api/v3.1/mcp/app/{appKey}",
                    {"appKey": app_key},
                ),
                cast_to=McpRetrieveAppResponse,
                operation=_RETRIEVE_APP_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )


class AsyncMcpResourceWithStreamingResponse:
    def __init__(self, resource: AsyncMcpResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        auth_config_ids: SequenceNotStr[str],
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        no_auth_apps: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpCreateResponse]]:
        body_fields = compact(
            {
                "name": name,
                "auth_config_ids": auth_config_ids,
                "no_auth_apps": no_auth_apps,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name", "auth_config_ids"),
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
                "/api/v3.1/mcp/servers",
                cast_to=McpCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=McpCreateBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def retrieve(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpRetrieveResponse]]:
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
                    "/api/v3.1/mcp/{id}",
                    {"id": id},
                ),
                cast_to=McpRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def update(
        self,
        id: str,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        toolkits: SequenceNotStr[str] | Omit = omit,
        allowed_tools: SequenceNotStr[str] | Omit = omit,
        managed_auth_via_composio: bool | Omit = omit,
        auth_config_ids: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpUpdateResponse]]:
        body_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "allowed_tools": allowed_tools,
                "managed_auth_via_composio": managed_auth_via_composio,
                "auth_config_ids": auth_config_ids,
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
                    "/api/v3.1/mcp/{id}",
                    {"id": id},
                ),
                cast_to=McpUpdateResponse,
                operation=_UPDATE_OPERATION,
                body=body_data,
                body_model=McpUpdateBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def list(
        self,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpListResponse]]:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
                "/api/v3.1/mcp/servers",
                cast_to=McpListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def delete(
        self,
        id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpDeleteResponse]]:
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
                    "/api/v3.1/mcp/{id}",
                    {"id": id},
                ),
                cast_to=McpDeleteResponse,
                operation=_DELETE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpCreateInstanceResponse]]: ...

    @overload
    def create_instance(
        self,
        server_id: str,
        body: BodyParam,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpCreateInstanceResponse]]: ...

    def create_instance(
        self,
        server_id: str,
        body: BodyParam | None = None,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpCreateInstanceResponse]]:
        body_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            body,
            body_fields,
            ("user_id",),
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
                    "/api/v3.1/mcp/servers/{serverId}/instances",
                    {"serverId": server_id},
                ),
                cast_to=McpCreateInstanceResponse,
                operation=_CREATE_INSTANCE_OPERATION,
                body=body_data,
                body_model=McpCreateInstanceBody,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    @overload
    def delete_instance(
        self,
        instance_id: str,
        *,
        server_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpDeleteInstanceResponse]]: ...

    @overload
    def delete_instance(
        self,
        instance_id: str,
        legacy_path: str,
        /,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpDeleteInstanceResponse]]: ...

    def delete_instance(
        self,
        instance_id: str,
        *legacy_args: object,
        server_id: str | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpDeleteInstanceResponse]]:
        instance_id, (server_id,), _legacy_body = normalize_path_arguments(
            instance_id,
            legacy_args,
            leading_values=(server_id,),
            leading_names=("server_id",),
            trailing_name="instance_id",
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
                "delete",
                build_path(
                    "/api/v3.1/mcp/servers/{serverId}/instances/{instanceId}",
                    {"serverId": server_id, "instanceId": instance_id},
                ),
                cast_to=McpDeleteInstanceResponse,
                operation=_DELETE_INSTANCE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def list_instances(
        self,
        server_id: str,
        *,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        search: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpListInstancesResponse]]:
        query_fields = compact(
            {
                "page_no": page_no,
                "limit": limit,
                "search": search,
                "order_by": order_by,
                "order_direction": order_direction,
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
                    "/api/v3.1/mcp/servers/{serverId}/instances",
                    {"serverId": server_id},
                ),
                cast_to=McpListInstancesResponse,
                operation=_LIST_INSTANCES_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    # Deprecated in the input OpenAPI schema.
    def retrieve_app(
        self,
        app_key: str,
        *,
        name: str | Omit = omit,
        toolkits: str | Omit = omit,
        auth_config_ids: str | Omit = omit,
        order_by: Literal["created_at", "updated_at"] | Omit = omit,
        order_direction: Literal["asc", "desc"] | Omit = omit,
        page_no: float | None | Omit = omit,
        limit: float | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[McpRetrieveAppResponse]]:
        query_fields = compact(
            {
                "name": name,
                "toolkits": toolkits,
                "auth_config_ids": auth_config_ids,
                "order_by": order_by,
                "order_direction": order_direction,
                "page_no": page_no,
                "limit": limit,
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
                    "/api/v3.1/mcp/app/{appKey}",
                    {"appKey": app_key},
                ),
                cast_to=McpRetrieveAppResponse,
                operation=_RETRIEVE_APP_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )
