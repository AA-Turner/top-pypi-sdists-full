# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.triggers_types`` — the generated resource classes.

``TriggersTypesResource`` (sync) and ``AsyncTriggersTypesResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx

from .._base_client import QueryParam, RequestOptions
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ..types.triggers_type_list_response import TriggersTypeListResponse
from ..types.triggers_type_retrieve_enum_response import TriggersTypeRetrieveEnumResponse
from ..types.triggers_type_retrieve_response import TriggersTypeRetrieveResponse
from ._base import AsyncAPIResource, SyncAPIResource, build_path, compact, make_request_options, merge_mapping

_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("triggers_types", "retrieve")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("triggers_types", "list")]
_RETRIEVE_ENUM_OPERATION = OPERATIONS_BY_CHAIN[("triggers_types", "retrieve_enum")]


class TriggersTypesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TriggersTypesResourceWithRawResponse:
        return TriggersTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TriggersTypesResourceWithStreamingResponse:
        return TriggersTypesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        slug: str,
        *,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> TriggersTypeRetrieveResponse:
        query_fields = compact(
            {
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
                "/api/v3.1/triggers_types/{slug}",
                {"slug": slug},
            ),
            cast_to=TriggersTypeRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> TriggersTypeListResponse:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "toolkit_versions": toolkit_versions,
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
            "/api/v3.1/triggers_types",
            cast_to=TriggersTypeListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
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
    ) -> TriggersTypeRetrieveEnumResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/triggers_types/list/enum",
            cast_to=TriggersTypeRetrieveEnumResponse,
            operation=_RETRIEVE_ENUM_OPERATION,
            options=options_data,
        )


class AsyncTriggersTypesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTriggersTypesResourceWithRawResponse:
        return AsyncTriggersTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTriggersTypesResourceWithStreamingResponse:
        return AsyncTriggersTypesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        slug: str,
        *,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> TriggersTypeRetrieveResponse:
        query_fields = compact(
            {
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
                "/api/v3.1/triggers_types/{slug}",
                {"slug": slug},
            ),
            cast_to=TriggersTypeRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> TriggersTypeListResponse:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "toolkit_versions": toolkit_versions,
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
            "/api/v3.1/triggers_types",
            cast_to=TriggersTypeListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
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
    ) -> TriggersTypeRetrieveEnumResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/triggers_types/list/enum",
            cast_to=TriggersTypeRetrieveEnumResponse,
            operation=_RETRIEVE_ENUM_OPERATION,
            options=options_data,
        )


class TriggersTypesResourceWithRawResponse:
    def __init__(self, resource: TriggersTypesResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        slug: str,
        *,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[TriggersTypeRetrieveResponse]:
        query_fields = compact(
            {
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
                "/api/v3.1/triggers_types/{slug}",
                {"slug": slug},
            ),
            cast_to=TriggersTypeRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[TriggersTypeListResponse]:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "toolkit_versions": toolkit_versions,
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
            "/api/v3.1/triggers_types",
            cast_to=TriggersTypeListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
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
    ) -> APIResponse[TriggersTypeRetrieveEnumResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/triggers_types/list/enum",
            cast_to=TriggersTypeRetrieveEnumResponse,
            operation=_RETRIEVE_ENUM_OPERATION,
            options=options_data,
        )


class AsyncTriggersTypesResourceWithRawResponse:
    def __init__(self, resource: AsyncTriggersTypesResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def retrieve(
        self,
        slug: str,
        *,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[TriggersTypeRetrieveResponse]:
        query_fields = compact(
            {
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
                "/api/v3.1/triggers_types/{slug}",
                {"slug": slug},
            ),
            cast_to=TriggersTypeRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[TriggersTypeListResponse]:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "toolkit_versions": toolkit_versions,
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
            "/api/v3.1/triggers_types",
            cast_to=TriggersTypeListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
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
    ) -> AsyncAPIResponse[TriggersTypeRetrieveEnumResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/triggers_types/list/enum",
            cast_to=TriggersTypeRetrieveEnumResponse,
            operation=_RETRIEVE_ENUM_OPERATION,
            options=options_data,
        )


class TriggersTypesResourceWithStreamingResponse:
    def __init__(self, resource: TriggersTypesResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        slug: str,
        *,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[TriggersTypeRetrieveResponse]]:
        query_fields = compact(
            {
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
                    "/api/v3.1/triggers_types/{slug}",
                    {"slug": slug},
                ),
                cast_to=TriggersTypeRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[TriggersTypeListResponse]]:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "toolkit_versions": toolkit_versions,
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
                "/api/v3.1/triggers_types",
                cast_to=TriggersTypeListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
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
    ) -> ResponseContextManager[APIResponse[TriggersTypeRetrieveEnumResponse]]:
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
                "/api/v3.1/triggers_types/list/enum",
                cast_to=TriggersTypeRetrieveEnumResponse,
                operation=_RETRIEVE_ENUM_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncTriggersTypesResourceWithStreamingResponse:
    def __init__(self, resource: AsyncTriggersTypesResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        slug: str,
        *,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[TriggersTypeRetrieveResponse]]:
        query_fields = compact(
            {
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
                    "/api/v3.1/triggers_types/{slug}",
                    {"slug": slug},
                ),
                cast_to=TriggersTypeRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        toolkit_slugs: SequenceNotStr[str] | None | Omit = omit,
        toolkit_versions: str | dict[str, str] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[TriggersTypeListResponse]]:
        query_fields = compact(
            {
                "toolkit_slugs": toolkit_slugs,
                "toolkit_versions": toolkit_versions,
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
                "/api/v3.1/triggers_types",
                cast_to=TriggersTypeListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
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
    ) -> AsyncResponseContextManager[AsyncAPIResponse[TriggersTypeRetrieveEnumResponse]]:
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
                "/api/v3.1/triggers_types/list/enum",
                cast_to=TriggersTypeRetrieveEnumResponse,
                operation=_RETRIEVE_ENUM_OPERATION,
                options=options_data,
                stream=True,
            )
        )
