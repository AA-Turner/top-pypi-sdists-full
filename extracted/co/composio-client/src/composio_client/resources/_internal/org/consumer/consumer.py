# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client._internal.org.consumer`` — the generated resource classes.

``ConsumerResource`` (sync) and ``AsyncConsumerResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

import httpx
from typing_extensions import overload

from ....._base_client import HeaderParam, QueryParam, RequestOptions
from ....._operations import OPERATIONS_BY_CHAIN
from ....._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ....._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from .....types.org.consumer_list_connected_toolkits_response import ConsumerListConnectedToolkitsResponse
from .....types.org.consumer_retrieve_config_response import ConsumerRetrieveConfigResponse
from ...._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_mapping,
    require_fields,
)
from .project import AsyncProjectResource, ProjectResource

if TYPE_CHECKING:
    from ....._base_client import AsyncAPIClient, SyncAPIClient

_LIST_CONNECTED_TOOLKITS_OPERATION = OPERATIONS_BY_CHAIN[
    ("_internal", "org", "consumer", "list_connected_toolkits")
]
_RETRIEVE_CONFIG_OPERATION = OPERATIONS_BY_CHAIN[("_internal", "org", "consumer", "retrieve_config")]


class ConsumerResource(SyncAPIResource):
    project: ProjectResource

    def __init__(self, client: SyncAPIClient) -> None:
        super().__init__(client)
        self.project = ProjectResource(client)

    @cached_property
    def with_raw_response(self) -> ConsumerResourceWithRawResponse:
        return ConsumerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsumerResourceWithStreamingResponse:
        return ConsumerResourceWithStreamingResponse(self)

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse: ...

    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse:
        query_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("user_id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
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
            "get",
            "/api/v3.1/org/consumer/connected_toolkits",
            cast_to=ConsumerListConnectedToolkitsResponse,
            operation=_LIST_CONNECTED_TOOLKITS_OPERATION,
            query=query_data,
            operation_headers=headers_data,
            options=options_data,
        )

    def retrieve_config(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConsumerRetrieveConfigResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request(
            "get",
            "/api/v3.1/org/consumer/config",
            cast_to=ConsumerRetrieveConfigResponse,
            operation=_RETRIEVE_CONFIG_OPERATION,
            options=options_data,
        )


class AsyncConsumerResource(AsyncAPIResource):
    project: AsyncProjectResource

    def __init__(self, client: AsyncAPIClient) -> None:
        super().__init__(client)
        self.project = AsyncProjectResource(client)

    @cached_property
    def with_raw_response(self) -> AsyncConsumerResourceWithRawResponse:
        return AsyncConsumerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsumerResourceWithStreamingResponse:
        return AsyncConsumerResourceWithStreamingResponse(self)

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    async def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse: ...

    @overload
    async def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse: ...

    @overload
    async def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse: ...

    @overload
    async def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse: ...

    async def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ConsumerListConnectedToolkitsResponse:
        query_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("user_id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
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
            "get",
            "/api/v3.1/org/consumer/connected_toolkits",
            cast_to=ConsumerListConnectedToolkitsResponse,
            operation=_LIST_CONNECTED_TOOLKITS_OPERATION,
            query=query_data,
            operation_headers=headers_data,
            options=options_data,
        )

    async def retrieve_config(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ConsumerRetrieveConfigResponse:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request(
            "get",
            "/api/v3.1/org/consumer/config",
            cast_to=ConsumerRetrieveConfigResponse,
            operation=_RETRIEVE_CONFIG_OPERATION,
            options=options_data,
        )


class ConsumerResourceWithRawResponse:
    def __init__(self, resource: ConsumerResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConsumerListConnectedToolkitsResponse]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConsumerListConnectedToolkitsResponse]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConsumerListConnectedToolkitsResponse]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConsumerListConnectedToolkitsResponse]: ...

    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConsumerListConnectedToolkitsResponse]:
        query_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("user_id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
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
            "get",
            "/api/v3.1/org/consumer/connected_toolkits",
            cast_to=ConsumerListConnectedToolkitsResponse,
            operation=_LIST_CONNECTED_TOOLKITS_OPERATION,
            query=query_data,
            operation_headers=headers_data,
            options=options_data,
        )

    def retrieve_config(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[ConsumerRetrieveConfigResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return self._client._request_raw(
            "get",
            "/api/v3.1/org/consumer/config",
            cast_to=ConsumerRetrieveConfigResponse,
            operation=_RETRIEVE_CONFIG_OPERATION,
            options=options_data,
        )


class AsyncConsumerResourceWithRawResponse:
    def __init__(self, resource: AsyncConsumerResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    async def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]: ...

    @overload
    async def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]: ...

    @overload
    async def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]: ...

    @overload
    async def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]: ...

    async def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]:
        query_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("user_id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
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
            "get",
            "/api/v3.1/org/consumer/connected_toolkits",
            cast_to=ConsumerListConnectedToolkitsResponse,
            operation=_LIST_CONNECTED_TOOLKITS_OPERATION,
            query=query_data,
            operation_headers=headers_data,
            options=options_data,
        )

    async def retrieve_config(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[ConsumerRetrieveConfigResponse]:
        options_data = make_request_options(
            request_options,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return await self._client._request_raw(
            "get",
            "/api/v3.1/org/consumer/config",
            cast_to=ConsumerRetrieveConfigResponse,
            operation=_RETRIEVE_CONFIG_OPERATION,
            options=options_data,
        )


class ConsumerResourceWithStreamingResponse:
    def __init__(self, resource: ConsumerResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConsumerListConnectedToolkitsResponse]]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConsumerListConnectedToolkitsResponse]]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConsumerListConnectedToolkitsResponse]]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConsumerListConnectedToolkitsResponse]]: ...

    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConsumerListConnectedToolkitsResponse]]:
        query_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("user_id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
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
                "get",
                "/api/v3.1/org/consumer/connected_toolkits",
                cast_to=ConsumerListConnectedToolkitsResponse,
                operation=_LIST_CONNECTED_TOOLKITS_OPERATION,
                query=query_data,
                operation_headers=headers_data,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_config(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[ConsumerRetrieveConfigResponse]]:
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
                "/api/v3.1/org/consumer/config",
                cast_to=ConsumerRetrieveConfigResponse,
                operation=_RETRIEVE_CONFIG_OPERATION,
                options=options_data,
                stream=True,
            )
        )


class AsyncConsumerResourceWithStreamingResponse:
    def __init__(self, resource: AsyncConsumerResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Declared header parameter(s): x-user-api-key (required), x-org-id (required).
    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str,
        x_org_id: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]]: ...

    @overload
    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam,
        headers: HeaderParam,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]]: ...

    def list_connected_toolkits(
        self,
        *,
        user_id: str | Omit = omit,
        x_user_api_key: str | Omit = omit,
        x_org_id: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        headers: HeaderParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConsumerListConnectedToolkitsResponse]]:
        query_fields = compact(
            {
                "user_id": user_id,
            }
        )
        require_fields(
            query,
            query_fields,
            ("user_id",),
            "query",
        )
        query_data = merge_mapping(query, query_fields)
        header_fields = compact(
            {
                "x-user-api-key": x_user_api_key,
                "x-org-id": x_org_id,
            }
        )
        require_fields(
            headers,
            header_fields,
            ("x-user-api-key", "x-org-id"),
            "header",
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
                "get",
                "/api/v3.1/org/consumer/connected_toolkits",
                cast_to=ConsumerListConnectedToolkitsResponse,
                operation=_LIST_CONNECTED_TOOLKITS_OPERATION,
                query=query_data,
                operation_headers=headers_data,
                options=options_data,
                stream=True,
            )
        )

    def retrieve_config(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[ConsumerRetrieveConfigResponse]]:
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
                "/api/v3.1/org/consumer/config",
                cast_to=ConsumerRetrieveConfigResponse,
                operation=_RETRIEVE_CONFIG_OPERATION,
                options=options_data,
                stream=True,
            )
        )
