# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.org.owner.project`` — the generated resource classes.

``ProjectResource`` (sync) and ``AsyncProjectResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import cached_property

import httpx
from typing_extensions import overload

from ...._base_client import BodyParam, QueryParam, RequestOptions
from ...._models import ProjectCreateBody
from ...._operations import OPERATIONS_BY_CHAIN
from ...._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ....types.org.owner import project_create_params
from ....types.org.owner.project_create_response import ProjectCreateResponse
from ....types.org.owner.project_delete_response import ProjectDeleteResponse
from ....types.org.owner.project_list_response import ProjectListResponse
from ....types.org.owner.project_regenerate_api_key_response import ProjectRegenerateAPIKeyResponse
from ....types.org.owner.project_retrieve_response import ProjectRetrieveResponse
from ..._base import (
    AsyncAPIResource,
    SyncAPIResource,
    build_path,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
    require_fields,
)

_CREATE_OPERATION = OPERATIONS_BY_CHAIN[("org", "owner", "project", "create")]
_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("org", "owner", "project", "retrieve")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("org", "owner", "project", "list")]
_DELETE_OPERATION = OPERATIONS_BY_CHAIN[("org", "owner", "project", "delete")]
_REGENERATE_API_KEY_OPERATION = OPERATIONS_BY_CHAIN[("org", "owner", "project", "regenerate_api_key")]


class ProjectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProjectResourceWithRawResponse:
        return ProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectResourceWithStreamingResponse:
        return ProjectResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectCreateResponse: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectCreateResponse: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectCreateResponse:
        body_fields = compact(
            {
                "name": name,
                "should_create_api_key": should_create_api_key,
                "api_key_allowed_ips": api_key_allowed_ips,
                "api_key_permissions": api_key_permissions,
                "config": config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
            "/api/v3.1/org/owner/project/new",
            cast_to=ProjectCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ProjectCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectRetrieveResponse:
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
                "/api/v3.1/org/owner/project/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectListResponse:
        query_fields = compact(
            {
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
            "/api/v3.1/org/owner/project/list",
            cast_to=ProjectListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    def delete(
        self,
        nano_id: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectDeleteResponse:
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
                "/api/v3.1/org/owner/project/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    def regenerate_api_key(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectRegenerateAPIKeyResponse:
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
                "/api/v3.1/org/owner/project/{nano_id}/regenerate_api_key",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectRegenerateAPIKeyResponse,
            operation=_REGENERATE_API_KEY_OPERATION,
            options=options_data,
        )


class AsyncProjectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProjectResourceWithRawResponse:
        return AsyncProjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectResourceWithStreamingResponse:
        return AsyncProjectResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectCreateResponse: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectCreateResponse: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectCreateResponse:
        body_fields = compact(
            {
                "name": name,
                "should_create_api_key": should_create_api_key,
                "api_key_allowed_ips": api_key_allowed_ips,
                "api_key_permissions": api_key_permissions,
                "config": config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
            "/api/v3.1/org/owner/project/new",
            cast_to=ProjectCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ProjectCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectRetrieveResponse:
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
                "/api/v3.1/org/owner/project/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectListResponse:
        query_fields = compact(
            {
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
            "/api/v3.1/org/owner/project/list",
            cast_to=ProjectListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def delete(
        self,
        nano_id: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ProjectDeleteResponse:
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
                "/api/v3.1/org/owner/project/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def regenerate_api_key(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ProjectRegenerateAPIKeyResponse:
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
                "/api/v3.1/org/owner/project/{nano_id}/regenerate_api_key",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectRegenerateAPIKeyResponse,
            operation=_REGENERATE_API_KEY_OPERATION,
            options=options_data,
        )


class ProjectResourceWithRawResponse:
    def __init__(self, resource: ProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectCreateResponse]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectCreateResponse]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectCreateResponse]:
        body_fields = compact(
            {
                "name": name,
                "should_create_api_key": should_create_api_key,
                "api_key_allowed_ips": api_key_allowed_ips,
                "api_key_permissions": api_key_permissions,
                "config": config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
            "/api/v3.1/org/owner/project/new",
            cast_to=ProjectCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ProjectCreateBody,
            options=options_data,
        )

    def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectRetrieveResponse]:
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
                "/api/v3.1/org/owner/project/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectListResponse]:
        query_fields = compact(
            {
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
            "/api/v3.1/org/owner/project/list",
            cast_to=ProjectListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    def delete(
        self,
        nano_id: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectDeleteResponse]:
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
                "/api/v3.1/org/owner/project/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    def regenerate_api_key(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ProjectRegenerateAPIKeyResponse]:
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
                "/api/v3.1/org/owner/project/{nano_id}/regenerate_api_key",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectRegenerateAPIKeyResponse,
            operation=_REGENERATE_API_KEY_OPERATION,
            options=options_data,
        )


class AsyncProjectResourceWithRawResponse:
    def __init__(self, resource: AsyncProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectCreateResponse]: ...

    @overload
    async def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectCreateResponse]: ...

    async def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectCreateResponse]:
        body_fields = compact(
            {
                "name": name,
                "should_create_api_key": should_create_api_key,
                "api_key_allowed_ips": api_key_allowed_ips,
                "api_key_permissions": api_key_permissions,
                "config": config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
            "/api/v3.1/org/owner/project/new",
            cast_to=ProjectCreateResponse,
            operation=_CREATE_OPERATION,
            body=body_data,
            body_model=ProjectCreateBody,
            options=options_data,
        )

    async def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectRetrieveResponse]:
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
                "/api/v3.1/org/owner/project/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            options=options_data,
        )

    async def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectListResponse]:
        query_fields = compact(
            {
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
            "/api/v3.1/org/owner/project/list",
            cast_to=ProjectListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def delete(
        self,
        nano_id: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectDeleteResponse]:
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
                "/api/v3.1/org/owner/project/{nano_id}",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectDeleteResponse,
            operation=_DELETE_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def regenerate_api_key(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ProjectRegenerateAPIKeyResponse]:
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
                "/api/v3.1/org/owner/project/{nano_id}/regenerate_api_key",
                {"nano_id": nano_id},
            ),
            cast_to=ProjectRegenerateAPIKeyResponse,
            operation=_REGENERATE_API_KEY_OPERATION,
            options=options_data,
        )


class ProjectResourceWithStreamingResponse:
    def __init__(self, resource: ProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectCreateResponse]]:
        body_fields = compact(
            {
                "name": name,
                "should_create_api_key": should_create_api_key,
                "api_key_allowed_ips": api_key_allowed_ips,
                "api_key_permissions": api_key_permissions,
                "config": config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
                "/api/v3.1/org/owner/project/new",
                cast_to=ProjectCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=ProjectCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectRetrieveResponse]]:
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
                    "/api/v3.1/org/owner/project/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=ProjectRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectListResponse]]:
        query_fields = compact(
            {
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
                "/api/v3.1/org/owner/project/list",
                cast_to=ProjectListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        nano_id: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectDeleteResponse]]:
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
                    "/api/v3.1/org/owner/project/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=ProjectDeleteResponse,
                operation=_DELETE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def regenerate_api_key(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ProjectRegenerateAPIKeyResponse]]:
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
                    "/api/v3.1/org/owner/project/{nano_id}/regenerate_api_key",
                    {"nano_id": nano_id},
                ),
                cast_to=ProjectRegenerateAPIKeyResponse,
                operation=_REGENERATE_API_KEY_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncProjectResourceWithStreamingResponse:
    def __init__(self, resource: AsyncProjectResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectCreateResponse]]: ...

    @overload
    def create(
        self,
        body: BodyParam,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectCreateResponse]]: ...

    def create(
        self,
        body: BodyParam | None = None,
        *,
        name: str | Omit = omit,
        should_create_api_key: bool | Omit = omit,
        api_key_allowed_ips: SequenceNotStr[str] | Omit = omit,
        api_key_permissions: Iterable[project_create_params.ApiKeyPermission] | Omit = omit,
        config: project_create_params.Config | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectCreateResponse]]:
        body_fields = compact(
            {
                "name": name,
                "should_create_api_key": should_create_api_key,
                "api_key_allowed_ips": api_key_allowed_ips,
                "api_key_permissions": api_key_permissions,
                "config": config,
            }
        )
        require_fields(
            body,
            body_fields,
            ("name",),
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
                "/api/v3.1/org/owner/project/new",
                cast_to=ProjectCreateResponse,
                operation=_CREATE_OPERATION,
                body=body_data,
                body_model=ProjectCreateBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectRetrieveResponse]]:
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
                    "/api/v3.1/org/owner/project/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=ProjectRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectListResponse]]:
        query_fields = compact(
            {
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
                "/api/v3.1/org/owner/project/list",
                cast_to=ProjectListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def delete(
        self,
        nano_id: str,
        *,
        revoke_on_delete: bool | None | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectDeleteResponse]]:
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
                    "/api/v3.1/org/owner/project/{nano_id}",
                    {"nano_id": nano_id},
                ),
                cast_to=ProjectDeleteResponse,
                operation=_DELETE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def regenerate_api_key(
        self,
        nano_id: str,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ProjectRegenerateAPIKeyResponse]]:
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
                    "/api/v3.1/org/owner/project/{nano_id}/regenerate_api_key",
                    {"nano_id": nano_id},
                ),
                cast_to=ProjectRegenerateAPIKeyResponse,
                operation=_REGENERATE_API_KEY_OPERATION,
                options=options_data,
                stream=True,
            )
        )
