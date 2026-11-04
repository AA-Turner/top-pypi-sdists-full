# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""``client.tool_router.session.files`` — the generated resource classes.

``FilesResource`` (sync) and ``AsyncFilesResource`` (async),
dispatching through the hand-written httpx kernel with Stainless-style
flat request fields and raw / streaming response wrappers.
"""

from __future__ import annotations

from functools import cached_property

import httpx
from typing_extensions import overload

from ...._base_client import BodyParam, QueryParam, RequestOptions
from ...._models import FileCreateDownloadURLBody, FileCreateUploadURLBody, FileDeleteBody
from ...._operations import OPERATIONS_BY_CHAIN
from ...._response import APIResponse, AsyncAPIResponse, AsyncResponseContextManager, ResponseContextManager
from ...._types import NOT_GIVEN, Body, Headers, NotGiven, Omit, Query, omit
from ....types.tool_router.session.file_create_download_url_response import FileCreateDownloadURLResponse
from ....types.tool_router.session.file_create_upload_url_response import FileCreateUploadURLResponse
from ....types.tool_router.session.file_delete_response import FileDeleteResponse
from ....types.tool_router.session.file_list_response import FileListResponse
from ..._base import (
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

_LIST_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "files", "list")]
_DELETE_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "files", "delete")]
_CREATE_DOWNLOAD_URL_OPERATION = OPERATIONS_BY_CHAIN[
    ("tool_router", "session", "files", "create_download_url")
]
_CREATE_UPLOAD_URL_OPERATION = OPERATIONS_BY_CHAIN[("tool_router", "session", "files", "create_upload_url")]


class FilesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FilesResourceWithRawResponse:
        return FilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesResourceWithStreamingResponse:
        return FilesResourceWithStreamingResponse(self)

    @overload
    def list(
        self,
        mount_id: str,
        *,
        session_id: str,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileListResponse: ...

    @overload
    def list(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileListResponse: ...

    def list(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileListResponse:
        mount_id, (session_id,), _legacy_body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            accepts_body=False,
        )
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "mount_relative_prefix": mount_relative_prefix,
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/items",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    @overload
    def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    def delete(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/delete",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileDeleteResponse,
            operation=_DELETE_OPERATION,
            body=body_data,
            body_model=FileDeleteBody,
            options=options_data,
        )

    @overload
    def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    def create_download_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/download_url",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileCreateDownloadURLResponse,
            operation=_CREATE_DOWNLOAD_URL_OPERATION,
            body=body_data,
            body_model=FileCreateDownloadURLBody,
            options=options_data,
        )

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    def create_upload_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
                "mimetype": mimetype,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/upload_url",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileCreateUploadURLResponse,
            operation=_CREATE_UPLOAD_URL_OPERATION,
            body=body_data,
            body_model=FileCreateUploadURLBody,
            options=options_data,
        )


class AsyncFilesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFilesResourceWithRawResponse:
        return AsyncFilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesResourceWithStreamingResponse:
        return AsyncFilesResourceWithStreamingResponse(self)

    @overload
    async def list(
        self,
        mount_id: str,
        *,
        session_id: str,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileListResponse: ...

    @overload
    async def list(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileListResponse: ...

    async def list(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> FileListResponse:
        mount_id, (session_id,), _legacy_body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            accepts_body=False,
        )
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "mount_relative_prefix": mount_relative_prefix,
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/items",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    @overload
    async def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    @overload
    async def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    @overload
    async def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    @overload
    async def delete(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse: ...

    async def delete(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileDeleteResponse:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/delete",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileDeleteResponse,
            operation=_DELETE_OPERATION,
            body=body_data,
            body_model=FileDeleteBody,
            options=options_data,
        )

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse: ...

    async def create_download_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateDownloadURLResponse:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/download_url",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileCreateDownloadURLResponse,
            operation=_CREATE_DOWNLOAD_URL_OPERATION,
            body=body_data,
            body_model=FileCreateDownloadURLBody,
            options=options_data,
        )

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse: ...

    async def create_upload_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> FileCreateUploadURLResponse:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
                "mimetype": mimetype,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/upload_url",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileCreateUploadURLResponse,
            operation=_CREATE_UPLOAD_URL_OPERATION,
            body=body_data,
            body_model=FileCreateUploadURLBody,
            options=options_data,
        )


class FilesResourceWithRawResponse:
    def __init__(self, resource: FilesResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def list(
        self,
        mount_id: str,
        *,
        session_id: str,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileListResponse]: ...

    @overload
    def list(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileListResponse]: ...

    def list(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileListResponse]:
        mount_id, (session_id,), _legacy_body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            accepts_body=False,
        )
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "mount_relative_prefix": mount_relative_prefix,
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/items",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileDeleteResponse]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileDeleteResponse]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileDeleteResponse]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileDeleteResponse]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileDeleteResponse]: ...

    def delete(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileDeleteResponse]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/delete",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileDeleteResponse,
            operation=_DELETE_OPERATION,
            body=body_data,
            body_model=FileDeleteBody,
            options=options_data,
        )

    @overload
    def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateDownloadURLResponse]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateDownloadURLResponse]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateDownloadURLResponse]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateDownloadURLResponse]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateDownloadURLResponse]: ...

    def create_download_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateDownloadURLResponse]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/download_url",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileCreateDownloadURLResponse,
            operation=_CREATE_DOWNLOAD_URL_OPERATION,
            body=body_data,
            body_model=FileCreateDownloadURLBody,
            options=options_data,
        )

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateUploadURLResponse]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateUploadURLResponse]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateUploadURLResponse]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateUploadURLResponse]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateUploadURLResponse]: ...

    def create_upload_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> APIResponse[FileCreateUploadURLResponse]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
                "mimetype": mimetype,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/upload_url",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileCreateUploadURLResponse,
            operation=_CREATE_UPLOAD_URL_OPERATION,
            body=body_data,
            body_model=FileCreateUploadURLBody,
            options=options_data,
        )


class AsyncFilesResourceWithRawResponse:
    def __init__(self, resource: AsyncFilesResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    async def list(
        self,
        mount_id: str,
        *,
        session_id: str,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileListResponse]: ...

    @overload
    async def list(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileListResponse]: ...

    async def list(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileListResponse]:
        mount_id, (session_id,), _legacy_body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            accepts_body=False,
        )
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "mount_relative_prefix": mount_relative_prefix,
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/items",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileListResponse,
            operation=_LIST_OPERATION,
            query=query_data,
            options=options_data,
        )

    @overload
    async def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileDeleteResponse]: ...

    @overload
    async def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileDeleteResponse]: ...

    @overload
    async def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileDeleteResponse]: ...

    @overload
    async def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileDeleteResponse]: ...

    @overload
    async def delete(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileDeleteResponse]: ...

    async def delete(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileDeleteResponse]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/delete",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileDeleteResponse,
            operation=_DELETE_OPERATION,
            body=body_data,
            body_model=FileDeleteBody,
            options=options_data,
        )

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateDownloadURLResponse]: ...

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateDownloadURLResponse]: ...

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateDownloadURLResponse]: ...

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateDownloadURLResponse]: ...

    @overload
    async def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateDownloadURLResponse]: ...

    async def create_download_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateDownloadURLResponse]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/download_url",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileCreateDownloadURLResponse,
            operation=_CREATE_DOWNLOAD_URL_OPERATION,
            body=body_data,
            body_model=FileCreateDownloadURLBody,
            options=options_data,
        )

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateUploadURLResponse]: ...

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateUploadURLResponse]: ...

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateUploadURLResponse]: ...

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateUploadURLResponse]: ...

    @overload
    async def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateUploadURLResponse]: ...

    async def create_upload_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncAPIResponse[FileCreateUploadURLResponse]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
                "mimetype": mimetype,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/upload_url",
                {"session_id": session_id, "mount_id": mount_id},
            ),
            cast_to=FileCreateUploadURLResponse,
            operation=_CREATE_UPLOAD_URL_OPERATION,
            body=body_data,
            body_model=FileCreateUploadURLBody,
            options=options_data,
        )


class FilesResourceWithStreamingResponse:
    def __init__(self, resource: FilesResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def list(
        self,
        mount_id: str,
        *,
        session_id: str,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileListResponse]]: ...

    @overload
    def list(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileListResponse]]: ...

    def list(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileListResponse]]:
        mount_id, (session_id,), _legacy_body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            accepts_body=False,
        )
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "mount_relative_prefix": mount_relative_prefix,
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
                    "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/items",
                    {"session_id": session_id, "mount_id": mount_id},
                ),
                cast_to=FileListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileDeleteResponse]]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileDeleteResponse]]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileDeleteResponse]]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileDeleteResponse]]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileDeleteResponse]]: ...

    def delete(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileDeleteResponse]]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                    "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/delete",
                    {"session_id": session_id, "mount_id": mount_id},
                ),
                cast_to=FileDeleteResponse,
                operation=_DELETE_OPERATION,
                body=body_data,
                body_model=FileDeleteBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateDownloadURLResponse]]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateDownloadURLResponse]]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateDownloadURLResponse]]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateDownloadURLResponse]]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateDownloadURLResponse]]: ...

    def create_download_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateDownloadURLResponse]]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                    "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/download_url",
                    {"session_id": session_id, "mount_id": mount_id},
                ),
                cast_to=FileCreateDownloadURLResponse,
                operation=_CREATE_DOWNLOAD_URL_OPERATION,
                body=body_data,
                body_model=FileCreateDownloadURLBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateUploadURLResponse]]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateUploadURLResponse]]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateUploadURLResponse]]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateUploadURLResponse]]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateUploadURLResponse]]: ...

    def create_upload_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> ResponseContextManager[APIResponse[FileCreateUploadURLResponse]]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
                "mimetype": mimetype,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                    "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/upload_url",
                    {"session_id": session_id, "mount_id": mount_id},
                ),
                cast_to=FileCreateUploadURLResponse,
                operation=_CREATE_UPLOAD_URL_OPERATION,
                body=body_data,
                body_model=FileCreateUploadURLBody,
                options=options_data,
                stream=True,
            )
        )


class AsyncFilesResourceWithStreamingResponse:
    def __init__(self, resource: AsyncFilesResource) -> None:
        self._resource = resource
        self._client = resource._client

    @overload
    def list(
        self,
        mount_id: str,
        *,
        session_id: str,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileListResponse]]: ...

    @overload
    def list(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileListResponse]]: ...

    def list(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        cursor: str | Omit = omit,
        limit: float | Omit = omit,
        mount_relative_prefix: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        query: QueryParam | None = None,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileListResponse]]:
        mount_id, (session_id,), _legacy_body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            accepts_body=False,
        )
        query_fields = compact(
            {
                "cursor": cursor,
                "limit": limit,
                "mount_relative_prefix": mount_relative_prefix,
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
                    "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/items",
                    {"session_id": session_id, "mount_id": mount_id},
                ),
                cast_to=FileListResponse,
                operation=_LIST_OPERATION,
                query=query_data,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileDeleteResponse]]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileDeleteResponse]]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileDeleteResponse]]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileDeleteResponse]]: ...

    @overload
    def delete(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileDeleteResponse]]: ...

    def delete(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileDeleteResponse]]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                    "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/delete",
                    {"session_id": session_id, "mount_id": mount_id},
                ),
                cast_to=FileDeleteResponse,
                operation=_DELETE_OPERATION,
                body=body_data,
                body_model=FileDeleteBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateDownloadURLResponse]]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateDownloadURLResponse]]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateDownloadURLResponse]]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateDownloadURLResponse]]: ...

    @overload
    def create_download_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateDownloadURLResponse]]: ...

    def create_download_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateDownloadURLResponse]]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                    "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/download_url",
                    {"session_id": session_id, "mount_id": mount_id},
                ),
                cast_to=FileCreateDownloadURLResponse,
                operation=_CREATE_DOWNLOAD_URL_OPERATION,
                body=body_data,
                body_model=FileCreateDownloadURLBody,
                options=options_data,
                stream=True,
            )
        )

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateUploadURLResponse]]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        *,
        session_id: str,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateUploadURLResponse]]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateUploadURLResponse]]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateUploadURLResponse]]: ...

    @overload
    def create_upload_url(
        self,
        mount_id: str,
        legacy_path: str,
        legacy_body: BodyParam,
        /,
        *,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateUploadURLResponse]]: ...

    def create_upload_url(
        self,
        mount_id: str,
        *legacy_args: object,
        session_id: str | None = None,
        mount_relative_path: str | Omit = omit,
        mimetype: str | Omit = omit,
        body: BodyParam | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        request_options: RequestOptions | None = None,
    ) -> AsyncResponseContextManager[AsyncAPIResponse[FileCreateUploadURLResponse]]:
        mount_id, (session_id,), body = normalize_path_arguments(
            mount_id,
            legacy_args,
            leading_values=(session_id,),
            leading_names=("session_id",),
            trailing_name="mount_id",
            body=body,
            accepts_body=True,
        )
        body_fields = compact(
            {
                "mount_relative_path": mount_relative_path,
                "mimetype": mimetype,
            }
        )
        require_fields(
            body,
            body_fields,
            ("mount_relative_path",),
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
                    "/api/v3.1/tool_router/session/{session_id}/mounts/{mount_id}/upload_url",
                    {"session_id": session_id, "mount_id": mount_id},
                ),
                cast_to=FileCreateUploadURLResponse,
                operation=_CREATE_UPLOAD_URL_OPERATION,
                body=body_data,
                body_model=FileCreateUploadURLBody,
                options=options_data,
                stream=True,
            )
        )
