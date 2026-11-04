# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.trigger_instances`` — the generated resource classes.

``TriggerInstancesResource`` (sync) and ``AsyncTriggerInstancesResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, Literal

import httpx

from ..._base_client import BodyParam, QueryParam, RequestOptions
from ..._models import TriggerInstanceUpsertBody
from ..._operations import OPERATIONS_BY_CHAIN
from ..._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ..._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ...types.trigger_instance_list_active_response import TriggerInstanceListActiveResponse
from ...types.trigger_instance_upsert_response import TriggerInstanceUpsertResponse
from .._base import (
    AsyncAPIResource,
    SyncAPIResource,
    build_path,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
)
from .manage import AsyncManageResource, ManageResource

if TYPE_CHECKING:
    from ..._base_client import AsyncAPIClient, SyncAPIClient

_LIST_ACTIVE_OPERATION = OPERATIONS_BY_CHAIN[("trigger_instances", "list_active")]
_UPSERT_OPERATION = OPERATIONS_BY_CHAIN[("trigger_instances", "upsert")]


class TriggerInstancesResource(SyncAPIResource):
    manage: ManageResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.manage = ManageResource(client)

    @cached_property
    def with_raw_response(self) -> TriggerInstancesResourceWithRawResponse:
        return TriggerInstancesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TriggerInstancesResourceWithStreamingResponse:
        return TriggerInstancesResourceWithStreamingResponse(self)

    def list_active(
        self,
        *,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_names_1: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_1: bool | None | Omit = omit,
        query_trigger_names_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_2: bool | None | Omit = omit,
        deprecated_connected_account_uuids: SequenceNotStr[str] | None | Omit = omit,
        deprecated_auth_config_uuids: SequenceNotStr[str] | None | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> TriggerInstanceListActiveResponse:
        query_fields = compact(
            {
                "user_ids": user_ids,
                "connected_account_ids": query_connected_account_ids_1,
                "auth_config_ids": query_auth_config_ids_1,
                "trigger_ids": query_trigger_ids_1,
                "trigger_names": query_trigger_names_1,
                "connectedAccountIds": query_connected_account_ids_2,
                "authConfigIds": query_auth_config_ids_2,
                "triggerIds": query_trigger_ids_2,
                "show_disabled": query_show_disabled_1,
                "triggerNames": query_trigger_names_2,
                "showDisabled": query_show_disabled_2,
                "deprecatedConnectedAccountUuids": deprecated_connected_account_uuids,
                "deprecatedAuthConfigUuids": deprecated_auth_config_uuids,
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
            "/api/v3.1/trigger_instances/active",
            cast_to=TriggerInstanceListActiveResponse,
            operation=_LIST_ACTIVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    def upsert(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        connected_auth_id: str | Omit = omit,
        body_trigger_config_2: dict[str, object | None] | Omit = omit,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        body_trigger_config_1: dict[str, object | None] | Omit = omit,
        type: Literal["poll", "webhook"] | Omit = omit,
        polling_interval: int | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> TriggerInstanceUpsertResponse:
        body_fields = compact(
            {
                "connectedAuthId": connected_auth_id,
                "triggerConfig": body_trigger_config_2,
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "egress_url": egress_url,
                "trigger_config": body_trigger_config_1,
                "type": type,
                "polling_interval": polling_interval,
                "version": version,
                "toolkit_versions": toolkit_versions,
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
            build_path(
                "/api/v3.1/trigger_instances/{slug}/upsert",
                {"slug": slug},
            ),
            cast_to=TriggerInstanceUpsertResponse,
            operation=_UPSERT_OPERATION,
            body=body_data,
            body_model=TriggerInstanceUpsertBody,
            options=options_data,
        )


class AsyncTriggerInstancesResource(AsyncAPIResource):
    manage: AsyncManageResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.manage = AsyncManageResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncTriggerInstancesResourceWithRawResponse:
        return AsyncTriggerInstancesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTriggerInstancesResourceWithStreamingResponse:
        return AsyncTriggerInstancesResourceWithStreamingResponse(self)

    async def list_active(
        self,
        *,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_names_1: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_1: bool | None | Omit = omit,
        query_trigger_names_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_2: bool | None | Omit = omit,
        deprecated_connected_account_uuids: SequenceNotStr[str] | None | Omit = omit,
        deprecated_auth_config_uuids: SequenceNotStr[str] | None | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> TriggerInstanceListActiveResponse:
        query_fields = compact(
            {
                "user_ids": user_ids,
                "connected_account_ids": query_connected_account_ids_1,
                "auth_config_ids": query_auth_config_ids_1,
                "trigger_ids": query_trigger_ids_1,
                "trigger_names": query_trigger_names_1,
                "connectedAccountIds": query_connected_account_ids_2,
                "authConfigIds": query_auth_config_ids_2,
                "triggerIds": query_trigger_ids_2,
                "show_disabled": query_show_disabled_1,
                "triggerNames": query_trigger_names_2,
                "showDisabled": query_show_disabled_2,
                "deprecatedConnectedAccountUuids": deprecated_connected_account_uuids,
                "deprecatedAuthConfigUuids": deprecated_auth_config_uuids,
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
            "/api/v3.1/trigger_instances/active",
            cast_to=TriggerInstanceListActiveResponse,
            operation=_LIST_ACTIVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def upsert(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        connected_auth_id: str | Omit = omit,
        body_trigger_config_2: dict[str, object | None] | Omit = omit,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        body_trigger_config_1: dict[str, object | None] | Omit = omit,
        type: Literal["poll", "webhook"] | Omit = omit,
        polling_interval: int | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> TriggerInstanceUpsertResponse:
        body_fields = compact(
            {
                "connectedAuthId": connected_auth_id,
                "triggerConfig": body_trigger_config_2,
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "egress_url": egress_url,
                "trigger_config": body_trigger_config_1,
                "type": type,
                "polling_interval": polling_interval,
                "version": version,
                "toolkit_versions": toolkit_versions,
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
            build_path(
                "/api/v3.1/trigger_instances/{slug}/upsert",
                {"slug": slug},
            ),
            cast_to=TriggerInstanceUpsertResponse,
            operation=_UPSERT_OPERATION,
            body=body_data,
            body_model=TriggerInstanceUpsertBody,
            options=options_data,
        )


class TriggerInstancesResourceWithRawResponse:
    def __init__(self, resource: TriggerInstancesResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list_active(
        self,
        *,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_names_1: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_1: bool | None | Omit = omit,
        query_trigger_names_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_2: bool | None | Omit = omit,
        deprecated_connected_account_uuids: SequenceNotStr[str] | None | Omit = omit,
        deprecated_auth_config_uuids: SequenceNotStr[str] | None | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[TriggerInstanceListActiveResponse]:
        query_fields = compact(
            {
                "user_ids": user_ids,
                "connected_account_ids": query_connected_account_ids_1,
                "auth_config_ids": query_auth_config_ids_1,
                "trigger_ids": query_trigger_ids_1,
                "trigger_names": query_trigger_names_1,
                "connectedAccountIds": query_connected_account_ids_2,
                "authConfigIds": query_auth_config_ids_2,
                "triggerIds": query_trigger_ids_2,
                "show_disabled": query_show_disabled_1,
                "triggerNames": query_trigger_names_2,
                "showDisabled": query_show_disabled_2,
                "deprecatedConnectedAccountUuids": deprecated_connected_account_uuids,
                "deprecatedAuthConfigUuids": deprecated_auth_config_uuids,
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
            "/api/v3.1/trigger_instances/active",
            cast_to=TriggerInstanceListActiveResponse,
            operation=_LIST_ACTIVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    def upsert(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        connected_auth_id: str | Omit = omit,
        body_trigger_config_2: dict[str, object | None] | Omit = omit,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        body_trigger_config_1: dict[str, object | None] | Omit = omit,
        type: Literal["poll", "webhook"] | Omit = omit,
        polling_interval: int | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[TriggerInstanceUpsertResponse]:
        body_fields = compact(
            {
                "connectedAuthId": connected_auth_id,
                "triggerConfig": body_trigger_config_2,
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "egress_url": egress_url,
                "trigger_config": body_trigger_config_1,
                "type": type,
                "polling_interval": polling_interval,
                "version": version,
                "toolkit_versions": toolkit_versions,
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
            build_path(
                "/api/v3.1/trigger_instances/{slug}/upsert",
                {"slug": slug},
            ),
            cast_to=TriggerInstanceUpsertResponse,
            operation=_UPSERT_OPERATION,
            body=body_data,
            body_model=TriggerInstanceUpsertBody,
            options=options_data,
        )


class AsyncTriggerInstancesResourceWithRawResponse:
    def __init__(self, resource: AsyncTriggerInstancesResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def list_active(
        self,
        *,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_names_1: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_1: bool | None | Omit = omit,
        query_trigger_names_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_2: bool | None | Omit = omit,
        deprecated_connected_account_uuids: SequenceNotStr[str] | None | Omit = omit,
        deprecated_auth_config_uuids: SequenceNotStr[str] | None | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[TriggerInstanceListActiveResponse]:
        query_fields = compact(
            {
                "user_ids": user_ids,
                "connected_account_ids": query_connected_account_ids_1,
                "auth_config_ids": query_auth_config_ids_1,
                "trigger_ids": query_trigger_ids_1,
                "trigger_names": query_trigger_names_1,
                "connectedAccountIds": query_connected_account_ids_2,
                "authConfigIds": query_auth_config_ids_2,
                "triggerIds": query_trigger_ids_2,
                "show_disabled": query_show_disabled_1,
                "triggerNames": query_trigger_names_2,
                "showDisabled": query_show_disabled_2,
                "deprecatedConnectedAccountUuids": deprecated_connected_account_uuids,
                "deprecatedAuthConfigUuids": deprecated_auth_config_uuids,
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
            "/api/v3.1/trigger_instances/active",
            cast_to=TriggerInstanceListActiveResponse,
            operation=_LIST_ACTIVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def upsert(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        connected_auth_id: str | Omit = omit,
        body_trigger_config_2: dict[str, object | None] | Omit = omit,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        body_trigger_config_1: dict[str, object | None] | Omit = omit,
        type: Literal["poll", "webhook"] | Omit = omit,
        polling_interval: int | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[TriggerInstanceUpsertResponse]:
        body_fields = compact(
            {
                "connectedAuthId": connected_auth_id,
                "triggerConfig": body_trigger_config_2,
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "egress_url": egress_url,
                "trigger_config": body_trigger_config_1,
                "type": type,
                "polling_interval": polling_interval,
                "version": version,
                "toolkit_versions": toolkit_versions,
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
            build_path(
                "/api/v3.1/trigger_instances/{slug}/upsert",
                {"slug": slug},
            ),
            cast_to=TriggerInstanceUpsertResponse,
            operation=_UPSERT_OPERATION,
            body=body_data,
            body_model=TriggerInstanceUpsertBody,
            options=options_data,
        )


class TriggerInstancesResourceWithStreamingResponse:
    def __init__(self, resource: TriggerInstancesResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list_active(
        self,
        *,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_names_1: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_1: bool | None | Omit = omit,
        query_trigger_names_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_2: bool | None | Omit = omit,
        deprecated_connected_account_uuids: SequenceNotStr[str] | None | Omit = omit,
        deprecated_auth_config_uuids: SequenceNotStr[str] | None | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[TriggerInstanceListActiveResponse]]:
        query_fields = compact(
            {
                "user_ids": user_ids,
                "connected_account_ids": query_connected_account_ids_1,
                "auth_config_ids": query_auth_config_ids_1,
                "trigger_ids": query_trigger_ids_1,
                "trigger_names": query_trigger_names_1,
                "connectedAccountIds": query_connected_account_ids_2,
                "authConfigIds": query_auth_config_ids_2,
                "triggerIds": query_trigger_ids_2,
                "show_disabled": query_show_disabled_1,
                "triggerNames": query_trigger_names_2,
                "showDisabled": query_show_disabled_2,
                "deprecatedConnectedAccountUuids": deprecated_connected_account_uuids,
                "deprecatedAuthConfigUuids": deprecated_auth_config_uuids,
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
                "/api/v3.1/trigger_instances/active",
                cast_to=TriggerInstanceListActiveResponse,
                operation=_LIST_ACTIVE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def upsert(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        connected_auth_id: str | Omit = omit,
        body_trigger_config_2: dict[str, object | None] | Omit = omit,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        body_trigger_config_1: dict[str, object | None] | Omit = omit,
        type: Literal["poll", "webhook"] | Omit = omit,
        polling_interval: int | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[TriggerInstanceUpsertResponse]]:
        body_fields = compact(
            {
                "connectedAuthId": connected_auth_id,
                "triggerConfig": body_trigger_config_2,
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "egress_url": egress_url,
                "trigger_config": body_trigger_config_1,
                "type": type,
                "polling_interval": polling_interval,
                "version": version,
                "toolkit_versions": toolkit_versions,
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
                build_path(
                    "/api/v3.1/trigger_instances/{slug}/upsert",
                    {"slug": slug},
                ),
                cast_to=TriggerInstanceUpsertResponse,
                operation=_UPSERT_OPERATION,
                body=body_data,
                body_model=TriggerInstanceUpsertBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncTriggerInstancesResourceWithStreamingResponse:
    def __init__(self, resource: AsyncTriggerInstancesResource) -> None:
        self._resource = resource
        self._client = resource._client

    def list_active(
        self,
        *,
        user_ids: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_1: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_names_1: SequenceNotStr[str] | None | Omit = omit,
        query_connected_account_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_auth_config_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_trigger_ids_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_1: bool | None | Omit = omit,
        query_trigger_names_2: SequenceNotStr[str] | None | Omit = omit,
        query_show_disabled_2: bool | None | Omit = omit,
        deprecated_connected_account_uuids: SequenceNotStr[str] | None | Omit = omit,
        deprecated_auth_config_uuids: SequenceNotStr[str] | None | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[TriggerInstanceListActiveResponse]]:
        query_fields = compact(
            {
                "user_ids": user_ids,
                "connected_account_ids": query_connected_account_ids_1,
                "auth_config_ids": query_auth_config_ids_1,
                "trigger_ids": query_trigger_ids_1,
                "trigger_names": query_trigger_names_1,
                "connectedAccountIds": query_connected_account_ids_2,
                "authConfigIds": query_auth_config_ids_2,
                "triggerIds": query_trigger_ids_2,
                "show_disabled": query_show_disabled_1,
                "triggerNames": query_trigger_names_2,
                "showDisabled": query_show_disabled_2,
                "deprecatedConnectedAccountUuids": deprecated_connected_account_uuids,
                "deprecatedAuthConfigUuids": deprecated_auth_config_uuids,
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
                "/api/v3.1/trigger_instances/active",
                cast_to=TriggerInstanceListActiveResponse,
                operation=_LIST_ACTIVE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def upsert(
        self,
        slug: str,
        body: BodyParam | None = None,
        *,
        connected_auth_id: str | Omit = omit,
        body_trigger_config_2: dict[str, object | None] | Omit = omit,
        connected_account_id: str | Omit = omit,
        user_id: str | Omit = omit,
        egress_url: str | None | Omit = omit,
        body_trigger_config_1: dict[str, object | None] | Omit = omit,
        type: Literal["poll", "webhook"] | Omit = omit,
        polling_interval: int | Omit = omit,
        version: str | Omit = omit,
        toolkit_versions: str | dict[str, str] | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[TriggerInstanceUpsertResponse]]:
        body_fields = compact(
            {
                "connectedAuthId": connected_auth_id,
                "triggerConfig": body_trigger_config_2,
                "connected_account_id": connected_account_id,
                "user_id": user_id,
                "egress_url": egress_url,
                "trigger_config": body_trigger_config_1,
                "type": type,
                "polling_interval": polling_interval,
                "version": version,
                "toolkit_versions": toolkit_versions,
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
                build_path(
                    "/api/v3.1/trigger_instances/{slug}/upsert",
                    {"slug": slug},
                ),
                cast_to=TriggerInstanceUpsertResponse,
                operation=_UPSERT_OPERATION,
                body=body_data,
                body_model=TriggerInstanceUpsertBody,
                options=options_data,
                stream=True,
            )
        )
