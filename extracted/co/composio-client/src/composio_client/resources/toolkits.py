# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.toolkits`` — the generated resource classes.

``ToolkitsResource`` (sync) and ``AsyncToolkitsResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import Literal

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, QueryParam, RequestOptions
from .._models import ToolkitRecommendScopesBody, ToolkitRetrieveMultiBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, SequenceNotStr, omit
from ..types.toolkit_list_response import ToolkitListResponse
from ..types.toolkit_recommend_scopes_response import ToolkitRecommendScopesResponse
from ..types.toolkit_retrieve_categories_response import ToolkitRetrieveCategoriesResponse
from ..types.toolkit_retrieve_changelog_response import ToolkitRetrieveChangelogResponse
from ..types.toolkit_retrieve_multi_response import ToolkitRetrieveMultiResponse
from ..types.toolkit_retrieve_response import ToolkitRetrieveResponse
from ..types.toolkit_retrieve_scopes_grant_context_response import ToolkitRetrieveScopesGrantContextResponse
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

_RETRIEVE_OPERATION = OPERATIONS_BY_CHAIN[("toolkits", "retrieve")]
_LIST_OPERATION = OPERATIONS_BY_CHAIN[("toolkits", "list")]
_RECOMMEND_SCOPES_OPERATION = OPERATIONS_BY_CHAIN[("toolkits", "recommend_scopes")]
_RETRIEVE_CATEGORIES_OPERATION = OPERATIONS_BY_CHAIN[("toolkits", "retrieve_categories")]
_RETRIEVE_CHANGELOG_OPERATION = OPERATIONS_BY_CHAIN[("toolkits", "retrieve_changelog")]
_RETRIEVE_MULTI_OPERATION = OPERATIONS_BY_CHAIN[("toolkits", "retrieve_multi")]
_RETRIEVE_SCOPES_GRANT_CONTEXT_OPERATION = OPERATIONS_BY_CHAIN[("toolkits", "retrieve_scopes_grant_context")]


class ToolkitsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ToolkitsResourceWithRawResponse:
        return ToolkitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ToolkitsResourceWithStreamingResponse:
        return ToolkitsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        slug: str,
        *,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveResponse:
        query_fields = compact(
            {
                "version": version,
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
                "/api/v3.1/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=ToolkitRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    def list(
        self,
        *,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        type: Literal["native", "custom", "all"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        include_deprecated: bool | None | Omit = omit,
        search: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolkitListResponse:
        query_fields = compact(
            {
                "category": category,
                "managed_by": managed_by,
                "type": type,
                "sort_by": sort_by,
                "include_deprecated": include_deprecated,
                "search": search,
                "user_id": user_id,
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
            "/api/v3.1/toolkits",
            cast_to=ToolkitListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRecommendScopesResponse: ...

    @overload
    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRecommendScopesResponse: ...

    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRecommendScopesResponse:
        body_fields = compact(
            {
                "tools": tools,
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
                "grant_context": grant_context,
                "include": include,
                "exclude": exclude,
                "available_scopes": available_scopes,
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
            build_path(
                "/api/v3.1/toolkits/{toolkit_slug}/scopes/recommended",
                {"toolkit_slug": toolkit_slug},
            ),
            cast_to=ToolkitRecommendScopesResponse,
            operation=_RECOMMEND_SCOPES_OPERATION,
            body=body_data,
            body_model=ToolkitRecommendScopesBody,
            options=options_data,
        )

    def retrieve_categories(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveCategoriesResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/toolkits/categories",
            cast_to=ToolkitRetrieveCategoriesResponse,
            operation=_RETRIEVE_CATEGORIES_OPERATION,
            options=options_data,
        )

    def retrieve_changelog(
        self,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveChangelogResponse:
        query_fields = compact(
            {
                "user_id": user_id,
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
            "/api/v3.1/toolkits/changelog",
            cast_to=ToolkitRetrieveChangelogResponse,
            operation=_RETRIEVE_CHANGELOG_OPERATION,
            query=query_data,
            options=options_data,
        )

    def retrieve_multi(
        self,
        body: BodyParam | None = None,
        *,
        toolkits: SequenceNotStr[str] | Omit = omit,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveMultiResponse:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "category": category,
                "managed_by": managed_by,
                "sort_by": sort_by,
                "limit": limit,
                "cursor": cursor,
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
            "/api/v3.1/toolkits/multi",
            cast_to=ToolkitRetrieveMultiResponse,
            operation=_RETRIEVE_MULTI_OPERATION,
            body=body_data,
            body_model=ToolkitRetrieveMultiBody,
            options=options_data,
        )

    def retrieve_scopes_grant_context(
        self,
        toolkit_slug: str,
        *,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveScopesGrantContextResponse:
        query_fields = compact(
            {
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
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
                "/api/v3.1/toolkits/{toolkit_slug}/scopes/grant_context",
                {"toolkit_slug": toolkit_slug},
            ),
            cast_to=ToolkitRetrieveScopesGrantContextResponse,
            operation=_RETRIEVE_SCOPES_GRANT_CONTEXT_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncToolkitsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncToolkitsResourceWithRawResponse:
        return AsyncToolkitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncToolkitsResourceWithStreamingResponse:
        return AsyncToolkitsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        slug: str,
        *,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveResponse:
        query_fields = compact(
            {
                "version": version,
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
                "/api/v3.1/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=ToolkitRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def list(
        self,
        *,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        type: Literal["native", "custom", "all"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        include_deprecated: bool | None | Omit = omit,
        search: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolkitListResponse:
        query_fields = compact(
            {
                "category": category,
                "managed_by": managed_by,
                "type": type,
                "sort_by": sort_by,
                "include_deprecated": include_deprecated,
                "search": search,
                "user_id": user_id,
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
            "/api/v3.1/toolkits",
            cast_to=ToolkitListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRecommendScopesResponse: ...

    @overload
    async def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRecommendScopesResponse: ...

    async def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRecommendScopesResponse:
        body_fields = compact(
            {
                "tools": tools,
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
                "grant_context": grant_context,
                "include": include,
                "exclude": exclude,
                "available_scopes": available_scopes,
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
            build_path(
                "/api/v3.1/toolkits/{toolkit_slug}/scopes/recommended",
                {"toolkit_slug": toolkit_slug},
            ),
            cast_to=ToolkitRecommendScopesResponse,
            operation=_RECOMMEND_SCOPES_OPERATION,
            body=body_data,
            body_model=ToolkitRecommendScopesBody,
            options=options_data,
        )

    async def retrieve_categories(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveCategoriesResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/toolkits/categories",
            cast_to=ToolkitRetrieveCategoriesResponse,
            operation=_RETRIEVE_CATEGORIES_OPERATION,
            options=options_data,
        )

    async def retrieve_changelog(
        self,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveChangelogResponse:
        query_fields = compact(
            {
                "user_id": user_id,
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
            "/api/v3.1/toolkits/changelog",
            cast_to=ToolkitRetrieveChangelogResponse,
            operation=_RETRIEVE_CHANGELOG_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def retrieve_multi(
        self,
        body: BodyParam | None = None,
        *,
        toolkits: SequenceNotStr[str] | Omit = omit,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveMultiResponse:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "category": category,
                "managed_by": managed_by,
                "sort_by": sort_by,
                "limit": limit,
                "cursor": cursor,
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
            "/api/v3.1/toolkits/multi",
            cast_to=ToolkitRetrieveMultiResponse,
            operation=_RETRIEVE_MULTI_OPERATION,
            body=body_data,
            body_model=ToolkitRetrieveMultiBody,
            options=options_data,
        )

    async def retrieve_scopes_grant_context(
        self,
        toolkit_slug: str,
        *,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ToolkitRetrieveScopesGrantContextResponse:
        query_fields = compact(
            {
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
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
                "/api/v3.1/toolkits/{toolkit_slug}/scopes/grant_context",
                {"toolkit_slug": toolkit_slug},
            ),
            cast_to=ToolkitRetrieveScopesGrantContextResponse,
            operation=_RETRIEVE_SCOPES_GRANT_CONTEXT_OPERATION,
            query=query_data,
            options=options_data,
        )


class ToolkitsResourceWithRawResponse:
    def __init__(self, resource: ToolkitsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        slug: str,
        *,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitRetrieveResponse]:
        query_fields = compact(
            {
                "version": version,
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
                "/api/v3.1/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=ToolkitRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    def list(
        self,
        *,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        type: Literal["native", "custom", "all"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        include_deprecated: bool | None | Omit = omit,
        search: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitListResponse]:
        query_fields = compact(
            {
                "category": category,
                "managed_by": managed_by,
                "type": type,
                "sort_by": sort_by,
                "include_deprecated": include_deprecated,
                "search": search,
                "user_id": user_id,
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
            "/api/v3.1/toolkits",
            cast_to=ToolkitListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitRecommendScopesResponse]: ...

    @overload
    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitRecommendScopesResponse]: ...

    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitRecommendScopesResponse]:
        body_fields = compact(
            {
                "tools": tools,
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
                "grant_context": grant_context,
                "include": include,
                "exclude": exclude,
                "available_scopes": available_scopes,
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
            build_path(
                "/api/v3.1/toolkits/{toolkit_slug}/scopes/recommended",
                {"toolkit_slug": toolkit_slug},
            ),
            cast_to=ToolkitRecommendScopesResponse,
            operation=_RECOMMEND_SCOPES_OPERATION,
            body=body_data,
            body_model=ToolkitRecommendScopesBody,
            options=options_data,
        )

    def retrieve_categories(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitRetrieveCategoriesResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/toolkits/categories",
            cast_to=ToolkitRetrieveCategoriesResponse,
            operation=_RETRIEVE_CATEGORIES_OPERATION,
            options=options_data,
        )

    def retrieve_changelog(
        self,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitRetrieveChangelogResponse]:
        query_fields = compact(
            {
                "user_id": user_id,
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
            "/api/v3.1/toolkits/changelog",
            cast_to=ToolkitRetrieveChangelogResponse,
            operation=_RETRIEVE_CHANGELOG_OPERATION,
            query=query_data,
            options=options_data,
        )

    def retrieve_multi(
        self,
        body: BodyParam | None = None,
        *,
        toolkits: SequenceNotStr[str] | Omit = omit,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitRetrieveMultiResponse]:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "category": category,
                "managed_by": managed_by,
                "sort_by": sort_by,
                "limit": limit,
                "cursor": cursor,
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
            "/api/v3.1/toolkits/multi",
            cast_to=ToolkitRetrieveMultiResponse,
            operation=_RETRIEVE_MULTI_OPERATION,
            body=body_data,
            body_model=ToolkitRetrieveMultiBody,
            options=options_data,
        )

    def retrieve_scopes_grant_context(
        self,
        toolkit_slug: str,
        *,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ToolkitRetrieveScopesGrantContextResponse]:
        query_fields = compact(
            {
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
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
                "/api/v3.1/toolkits/{toolkit_slug}/scopes/grant_context",
                {"toolkit_slug": toolkit_slug},
            ),
            cast_to=ToolkitRetrieveScopesGrantContextResponse,
            operation=_RETRIEVE_SCOPES_GRANT_CONTEXT_OPERATION,
            query=query_data,
            options=options_data,
        )


class AsyncToolkitsResourceWithRawResponse:
    def __init__(self, resource: AsyncToolkitsResource) -> None:
        self._resource = resource
        self._client = resource._client

    async def retrieve(
        self,
        slug: str,
        *,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitRetrieveResponse]:
        query_fields = compact(
            {
                "version": version,
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
                "/api/v3.1/toolkits/{slug}",
                {"slug": slug},
            ),
            cast_to=ToolkitRetrieveResponse,
            operation=_RETRIEVE_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def list(
        self,
        *,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        type: Literal["native", "custom", "all"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        include_deprecated: bool | None | Omit = omit,
        search: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitListResponse]:
        query_fields = compact(
            {
                "category": category,
                "managed_by": managed_by,
                "type": type,
                "sort_by": sort_by,
                "include_deprecated": include_deprecated,
                "search": search,
                "user_id": user_id,
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
            "/api/v3.1/toolkits",
            cast_to=ToolkitListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitRecommendScopesResponse]: ...

    @overload
    async def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitRecommendScopesResponse]: ...

    async def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitRecommendScopesResponse]:
        body_fields = compact(
            {
                "tools": tools,
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
                "grant_context": grant_context,
                "include": include,
                "exclude": exclude,
                "available_scopes": available_scopes,
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
            build_path(
                "/api/v3.1/toolkits/{toolkit_slug}/scopes/recommended",
                {"toolkit_slug": toolkit_slug},
            ),
            cast_to=ToolkitRecommendScopesResponse,
            operation=_RECOMMEND_SCOPES_OPERATION,
            body=body_data,
            body_model=ToolkitRecommendScopesBody,
            options=options_data,
        )

    async def retrieve_categories(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitRetrieveCategoriesResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/toolkits/categories",
            cast_to=ToolkitRetrieveCategoriesResponse,
            operation=_RETRIEVE_CATEGORIES_OPERATION,
            options=options_data,
        )

    async def retrieve_changelog(
        self,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitRetrieveChangelogResponse]:
        query_fields = compact(
            {
                "user_id": user_id,
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
            "/api/v3.1/toolkits/changelog",
            cast_to=ToolkitRetrieveChangelogResponse,
            operation=_RETRIEVE_CHANGELOG_OPERATION,
            query=query_data,
            options=options_data,
        )

    async def retrieve_multi(
        self,
        body: BodyParam | None = None,
        *,
        toolkits: SequenceNotStr[str] | Omit = omit,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitRetrieveMultiResponse]:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "category": category,
                "managed_by": managed_by,
                "sort_by": sort_by,
                "limit": limit,
                "cursor": cursor,
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
            "/api/v3.1/toolkits/multi",
            cast_to=ToolkitRetrieveMultiResponse,
            operation=_RETRIEVE_MULTI_OPERATION,
            body=body_data,
            body_model=ToolkitRetrieveMultiBody,
            options=options_data,
        )

    async def retrieve_scopes_grant_context(
        self,
        toolkit_slug: str,
        *,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ToolkitRetrieveScopesGrantContextResponse]:
        query_fields = compact(
            {
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
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
                "/api/v3.1/toolkits/{toolkit_slug}/scopes/grant_context",
                {"toolkit_slug": toolkit_slug},
            ),
            cast_to=ToolkitRetrieveScopesGrantContextResponse,
            operation=_RETRIEVE_SCOPES_GRANT_CONTEXT_OPERATION,
            query=query_data,
            options=options_data,
        )


class ToolkitsResourceWithStreamingResponse:
    def __init__(self, resource: ToolkitsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        slug: str,
        *,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitRetrieveResponse]]:
        query_fields = compact(
            {
                "version": version,
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
                    "/api/v3.1/toolkits/{slug}",
                    {"slug": slug},
                ),
                cast_to=ToolkitRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        type: Literal["native", "custom", "all"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        include_deprecated: bool | None | Omit = omit,
        search: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitListResponse]]:
        query_fields = compact(
            {
                "category": category,
                "managed_by": managed_by,
                "type": type,
                "sort_by": sort_by,
                "include_deprecated": include_deprecated,
                "search": search,
                "user_id": user_id,
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
                "/api/v3.1/toolkits",
                cast_to=ToolkitListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitRecommendScopesResponse]]: ...

    @overload
    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitRecommendScopesResponse]]: ...

    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitRecommendScopesResponse]]:
        body_fields = compact(
            {
                "tools": tools,
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
                "grant_context": grant_context,
                "include": include,
                "exclude": exclude,
                "available_scopes": available_scopes,
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
                build_path(
                    "/api/v3.1/toolkits/{toolkit_slug}/scopes/recommended",
                    {"toolkit_slug": toolkit_slug},
                ),
                cast_to=ToolkitRecommendScopesResponse,
                operation=_RECOMMEND_SCOPES_OPERATION,
                body=body_data,
                body_model=ToolkitRecommendScopesBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_categories(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitRetrieveCategoriesResponse]]:
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
                "/api/v3.1/toolkits/categories",
                cast_to=ToolkitRetrieveCategoriesResponse,
                operation=_RETRIEVE_CATEGORIES_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_changelog(
        self,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitRetrieveChangelogResponse]]:
        query_fields = compact(
            {
                "user_id": user_id,
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
                "/api/v3.1/toolkits/changelog",
                cast_to=ToolkitRetrieveChangelogResponse,
                operation=_RETRIEVE_CHANGELOG_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_multi(
        self,
        body: BodyParam | None = None,
        *,
        toolkits: SequenceNotStr[str] | Omit = omit,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitRetrieveMultiResponse]]:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "category": category,
                "managed_by": managed_by,
                "sort_by": sort_by,
                "limit": limit,
                "cursor": cursor,
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
                "/api/v3.1/toolkits/multi",
                cast_to=ToolkitRetrieveMultiResponse,
                operation=_RETRIEVE_MULTI_OPERATION,
                body=body_data,
                body_model=ToolkitRetrieveMultiBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_scopes_grant_context(
        self,
        toolkit_slug: str,
        *,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ToolkitRetrieveScopesGrantContextResponse]]:
        query_fields = compact(
            {
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
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
                    "/api/v3.1/toolkits/{toolkit_slug}/scopes/grant_context",
                    {"toolkit_slug": toolkit_slug},
                ),
                cast_to=ToolkitRetrieveScopesGrantContextResponse,
                operation=_RETRIEVE_SCOPES_GRANT_CONTEXT_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )


class AsyncToolkitsResourceWithStreamingResponse:
    def __init__(self, resource: AsyncToolkitsResource) -> None:
        self._resource = resource
        self._client = resource._client

    def retrieve(
        self,
        slug: str,
        *,
        version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitRetrieveResponse]]:
        query_fields = compact(
            {
                "version": version,
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
                    "/api/v3.1/toolkits/{slug}",
                    {"slug": slug},
                ),
                cast_to=ToolkitRetrieveResponse,
                operation=_RETRIEVE_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def list(
        self,
        *,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        type: Literal["native", "custom", "all"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        include_deprecated: bool | None | Omit = omit,
        search: str | Omit = omit,
        user_id: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitListResponse]]:
        query_fields = compact(
            {
                "category": category,
                "managed_by": managed_by,
                "type": type,
                "sort_by": sort_by,
                "include_deprecated": include_deprecated,
                "search": search,
                "user_id": user_id,
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
                "/api/v3.1/toolkits",
                cast_to=ToolkitListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str],
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitRecommendScopesResponse]]: ...

    @overload
    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitRecommendScopesResponse]]: ...

    def recommend_scopes(
        self,
        toolkit_slug: str,
        body: BodyParam | None = None,
        *,
        tools: SequenceNotStr[str] | Omit = omit,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        grant_context: dict[str, str] | Omit = omit,
        include: SequenceNotStr[str] | Omit = omit,
        exclude: SequenceNotStr[str] | Omit = omit,
        available_scopes: SequenceNotStr[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitRecommendScopesResponse]]:
        body_fields = compact(
            {
                "tools": tools,
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
                "grant_context": grant_context,
                "include": include,
                "exclude": exclude,
                "available_scopes": available_scopes,
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
                build_path(
                    "/api/v3.1/toolkits/{toolkit_slug}/scopes/recommended",
                    {"toolkit_slug": toolkit_slug},
                ),
                cast_to=ToolkitRecommendScopesResponse,
                operation=_RECOMMEND_SCOPES_OPERATION,
                body=body_data,
                body_model=ToolkitRecommendScopesBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_categories(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitRetrieveCategoriesResponse]]:
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
                "/api/v3.1/toolkits/categories",
                cast_to=ToolkitRetrieveCategoriesResponse,
                operation=_RETRIEVE_CATEGORIES_OPERATION,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_changelog(
        self,
        *,
        user_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitRetrieveChangelogResponse]]:
        query_fields = compact(
            {
                "user_id": user_id,
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
                "/api/v3.1/toolkits/changelog",
                cast_to=ToolkitRetrieveChangelogResponse,
                operation=_RETRIEVE_CHANGELOG_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_multi(
        self,
        body: BodyParam | None = None,
        *,
        toolkits: SequenceNotStr[str] | Omit = omit,
        category: str | Omit = omit,
        managed_by: Literal["composio", "all", "project"] | Omit = omit,
        sort_by: Literal["usage", "alphabetically"] | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitRetrieveMultiResponse]]:
        body_fields = compact(
            {
                "toolkits": toolkits,
                "category": category,
                "managed_by": managed_by,
                "sort_by": sort_by,
                "limit": limit,
                "cursor": cursor,
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
                "/api/v3.1/toolkits/multi",
                cast_to=ToolkitRetrieveMultiResponse,
                operation=_RETRIEVE_MULTI_OPERATION,
                body=body_data,
                body_model=ToolkitRetrieveMultiBody,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_scopes_grant_context(
        self,
        toolkit_slug: str,
        *,
        auth_scheme: Literal[
            "OAUTH2",
            "OAUTH1",
            "API_KEY",
            "BASIC",
            "BILLCOM_AUTH",
            "BEARER_TOKEN",
            "GOOGLE_SERVICE_ACCOUNT",
            "NO_AUTH",
            "BASIC_WITH_JWT",
            "CALCOM_AUTH",
            "SERVICE_ACCOUNT",
            "SAML",
            "DCR_OAUTH",
            "CIMD_OAUTH",
            "S2S_OAUTH2",
        ]
        | Omit = omit,
        toolkit_version: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ToolkitRetrieveScopesGrantContextResponse]]:
        query_fields = compact(
            {
                "auth_scheme": auth_scheme,
                "toolkit_version": toolkit_version,
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
                    "/api/v3.1/toolkits/{toolkit_slug}/scopes/grant_context",
                    {"toolkit_slug": toolkit_slug},
                ),
                cast_to=ToolkitRetrieveScopesGrantContextResponse,
                operation=_RETRIEVE_SCOPES_GRANT_CONTEXT_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )
