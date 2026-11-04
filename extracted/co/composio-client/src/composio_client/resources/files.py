# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.files`` — the generated resource classes.

``FilesResource`` (sync) and ``AsyncFilesResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from .._base_client import BodyParam, QueryParam, RequestOptions
from .._models import FileCreatePresignedURLBody
from .._operations import OPERATIONS_BY_CHAIN
from .._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from .._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ..types.file_create_presigned_url_response import FileCreatePresignedURLResponse
from ..types.file_list_response import FileListResponse
from ._base import (
    AsyncAPIResource,
    SyncAPIResource,
    compact,
    make_request_options,
    merge_body,
    merge_mapping,
    require_fields,
)

_LIST_OPERATION = OPERATIONS_BY_CHAIN[("files", "list")]
_CREATE_PRESIGNED_URL_OPERATION = OPERATIONS_BY_CHAIN[("files", "create_presigned_url")]


class FilesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FilesResourceWithRawResponse:
        return FilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesResourceWithStreamingResponse:
        return FilesResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileListResponse:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
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
            "/api/v3.1/files/list",
            cast_to=FileListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        tool_slug: str,
        filename: str,
        mimetype: str,
        md5: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreatePresignedURLResponse: ...

    @overload
    def create_presigned_url(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreatePresignedURLResponse: ...

    def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreatePresignedURLResponse:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
                "filename": filename,
                "mimetype": mimetype,
                "md5": md5,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "tool_slug", "filename", "mimetype", "md5"),
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
            "/api/v3.1/files/upload/request",
            cast_to=FileCreatePresignedURLResponse,
            operation=_CREATE_PRESIGNED_URL_OPERATION,
            body=body_data,
            body_model=FileCreatePresignedURLBody,
            options=options_data,
        )


class AsyncFilesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFilesResourceWithRawResponse:
        return AsyncFilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesResourceWithStreamingResponse:
        return AsyncFilesResourceWithStreamingResponse(self)

    # Deprecated in the input OpenAPI schema.
    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileListResponse:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
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
            "/api/v3.1/files/list",
            cast_to=FileListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        tool_slug: str,
        filename: str,
        mimetype: str,
        md5: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreatePresignedURLResponse: ...

    @overload
    async def create_presigned_url(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreatePresignedURLResponse: ...

    async def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreatePresignedURLResponse:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
                "filename": filename,
                "mimetype": mimetype,
                "md5": md5,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "tool_slug", "filename", "mimetype", "md5"),
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
            "/api/v3.1/files/upload/request",
            cast_to=FileCreatePresignedURLResponse,
            operation=_CREATE_PRESIGNED_URL_OPERATION,
            body=body_data,
            body_model=FileCreatePresignedURLBody,
            options=options_data,
        )


class FilesResourceWithRawResponse:
    def __init__(self, resource: FilesResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileListResponse]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
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
            "/api/v3.1/files/list",
            cast_to=FileListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        tool_slug: str,
        filename: str,
        mimetype: str,
        md5: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreatePresignedURLResponse]: ...

    @overload
    def create_presigned_url(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreatePresignedURLResponse]: ...

    def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreatePresignedURLResponse]:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
                "filename": filename,
                "mimetype": mimetype,
                "md5": md5,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "tool_slug", "filename", "mimetype", "md5"),
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
            "/api/v3.1/files/upload/request",
            cast_to=FileCreatePresignedURLResponse,
            operation=_CREATE_PRESIGNED_URL_OPERATION,
            body=body_data,
            body_model=FileCreatePresignedURLBody,
            options=options_data,
        )


class AsyncFilesResourceWithRawResponse:
    def __init__(self, resource: AsyncFilesResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    async def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileListResponse]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
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
            "/api/v3.1/files/list",
            cast_to=FileListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        tool_slug: str,
        filename: str,
        mimetype: str,
        md5: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreatePresignedURLResponse]: ...

    @overload
    async def create_presigned_url(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreatePresignedURLResponse]: ...

    async def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreatePresignedURLResponse]:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
                "filename": filename,
                "mimetype": mimetype,
                "md5": md5,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "tool_slug", "filename", "mimetype", "md5"),
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
            "/api/v3.1/files/upload/request",
            cast_to=FileCreatePresignedURLResponse,
            operation=_CREATE_PRESIGNED_URL_OPERATION,
            body=body_data,
            body_model=FileCreatePresignedURLBody,
            options=options_data,
        )


class FilesResourceWithStreamingResponse:
    def __init__(self, resource: FilesResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileListResponse]]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
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
                "/api/v3.1/files/list",
                cast_to=FileListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        tool_slug: str,
        filename: str,
        mimetype: str,
        md5: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreatePresignedURLResponse]]: ...

    @overload
    def create_presigned_url(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreatePresignedURLResponse]]: ...

    def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreatePresignedURLResponse]]:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
                "filename": filename,
                "mimetype": mimetype,
                "md5": md5,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "tool_slug", "filename", "mimetype", "md5"),
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
                "/api/v3.1/files/upload/request",
                cast_to=FileCreatePresignedURLResponse,
                operation=_CREATE_PRESIGNED_URL_OPERATION,
                body=body_data,
                body_model=FileCreatePresignedURLBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncFilesResourceWithStreamingResponse:
    def __init__(self, resource: AsyncFilesResource) -> None:
        self._resource = resource
        self._client = resource._client

    # Deprecated in the input OpenAPI schema.
    def list(
        self,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        limit: float | None | Omit = omit,
        cursor: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileListResponse]]:
        query_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
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
                "/api/v3.1/files/list",
                cast_to=FileListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str,
        tool_slug: str,
        filename: str,
        mimetype: str,
        md5: str,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreatePresignedURLResponse]]: ...

    @overload
    def create_presigned_url(
        self,
        body: BodyParam,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreatePresignedURLResponse]]: ...

    def create_presigned_url(
        self,
        body: BodyParam | None = None,
        *,
        toolkit_slug: str | Omit = omit,
        tool_slug: str | Omit = omit,
        filename: str | Omit = omit,
        mimetype: str | Omit = omit,
        md5: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreatePresignedURLResponse]]:
        body_fields = compact(
            {
                "toolkit_slug": toolkit_slug,
                "tool_slug": tool_slug,
                "filename": filename,
                "mimetype": mimetype,
                "md5": md5,
            }
        )
        require_fields(
            body,
            body_fields,
            ("toolkit_slug", "tool_slug", "filename", "mimetype", "md5"),
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
                "/api/v3.1/files/upload/request",
                cast_to=FileCreatePresignedURLResponse,
                operation=_CREATE_PRESIGNED_URL_OPERATION,
                body=body_data,
                body_model=FileCreatePresignedURLBody,
                options=options_data,
                stream=True,
            )
        )
