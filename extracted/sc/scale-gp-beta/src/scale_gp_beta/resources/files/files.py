# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Mapping, Iterable, cast

import httpx

from ...types import file_list_params, file_create_params, file_update_params, file_import_from_cloud_params
from .content import (
    ContentResource,
    AsyncContentResource,
    ContentResourceWithRawResponse,
    AsyncContentResourceWithRawResponse,
    ContentResourceWithStreamingResponse,
    AsyncContentResourceWithStreamingResponse,
)
from ..._files import deepcopy_with_paths
from ..._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from ..._utils import extract_files, path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorPage, AsyncCursorPage
from ...types.chat import SortOrder
from ..._base_client import AsyncPaginator, make_request_options
from ...types.sgp_file import SGPFile
from ...types.chat.sort_order import SortOrder
from ...types.file_delete_response import FileDeleteResponse
from ...types.file_import_from_cloud_response import FileImportFromCloudResponse

__all__ = ["FilesResource", "AsyncFilesResource"]


class FilesResource(SyncAPIResource):
    @cached_property
    def content(self) -> ContentResource:
        return ContentResource(self._client)

    @cached_property
    def with_raw_response(self) -> FilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return FilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return FilesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SGPFile:
        """
        Upload a file's bytes directly and create a file record.

        Send the file as multipart/form-data in the `file` field; the request body
        carries the raw bytes, unlike cloud_imports which only references blobs that
        already exist in cloud storage. The upload is rejected if it exceeds 25 MB;
        larger or direct-to-storage uploads use a separate upload flow. Content is
        deduplicated by checksum and MIME type, so uploading bytes identical to an
        existing file reuses the already-stored object instead of storing a second copy.
        Returns the created file's metadata.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths({"file": file}, [["file"]])
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/v5/files",
            body=maybe_transform(body, file_create_params.FileCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SGPFile,
        )

    def retrieve(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SGPFile:
        """
        Retrieve a single file's metadata by id.

        Returns the file record (id, filename, MIME type, size, tags, and related
        fields) but not the file's bytes; use the content endpoint to download the
        bytes.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._get(
            path_template("/v5/files/{file_id}", file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SGPFile,
        )

    def update(
        self,
        file_id: str,
        *,
        tags: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SGPFile:
        """
        Update a file's mutable metadata by id.

        Only the file's `tags` can be modified; filename, content, size, and other
        attributes are immutable through this endpoint. The supplied tags replace the
        file's existing tags. Returns the updated file metadata.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._patch(
            path_template("/v5/files/{file_id}", file_id=file_id),
            body=maybe_transform({"tags": tags}, file_update_params.FileUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SGPFile,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        filename: str | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[SGPFile]:
        """
        List the account's files with pagination.

        Optionally filter by `filename` (case-insensitive partial match). Results are
        scoped to the files the caller is authorized to read. Files marked hidden
        (internal or service-owned artifacts) are excluded from this listing but remain
        retrievable by id. Returns file metadata only, not content.

        Args:
          filename: Filter files by filename (case-insensitive partial match)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/files",
            page=SyncCursorPage[SGPFile],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "filename": filename,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    file_list_params.FileListParams,
                ),
            ),
            model=SGPFile,
        )

    def delete(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FileDeleteResponse:
        """
        Delete a file by id, removing its database record.

        This is a hard delete: the file's row is removed from the database, not
        soft-archived. The underlying stored object is deleted only when no other file
        record still references the same stored content (identical checksum and MIME
        type); when another record shares the blob, the blob is retained. If the id
        refers to an incomplete multipart upload placeholder, its staged parts are
        aborted instead. Returns a confirmation carrying the deleted file's id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._delete(
            path_template("/v5/files/{file_id}", file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileDeleteResponse,
        )

    def import_from_cloud(
        self,
        *,
        files: Iterable[file_import_from_cloud_params.File],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FileImportFromCloudResponse:
        """
        Register files that already exist in cloud blob storage as file records, in one
        batch.

        Unlike upload, this transfers no bytes: each entry references an existing object
        by its container/bucket, filepath, filename, and MIME type, and only a metadata
        record pointing at that object is created. Files are imported independently and
        the response reports a per-file status. The response is 200 when every import
        succeeds and 207 when results are mixed, with each result marked SUCCESS or a
        failure reason (file does not exist, invalid permissions, or unknown error).
        Failed entries carry only the submitted filename and MIME type rather than a
        full file record.

        Args:
          files: List of files to import from cloud storage

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/files/cloud_imports",
            body=maybe_transform({"files": files}, file_import_from_cloud_params.FileImportFromCloudParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileImportFromCloudResponse,
        )


class AsyncFilesResource(AsyncAPIResource):
    @cached_property
    def content(self) -> AsyncContentResource:
        return AsyncContentResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncFilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncFilesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SGPFile:
        """
        Upload a file's bytes directly and create a file record.

        Send the file as multipart/form-data in the `file` field; the request body
        carries the raw bytes, unlike cloud_imports which only references blobs that
        already exist in cloud storage. The upload is rejected if it exceeds 25 MB;
        larger or direct-to-storage uploads use a separate upload flow. Content is
        deduplicated by checksum and MIME type, so uploading bytes identical to an
        existing file reuses the already-stored object instead of storing a second copy.
        Returns the created file's metadata.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths({"file": file}, [["file"]])
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/v5/files",
            body=await async_maybe_transform(body, file_create_params.FileCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SGPFile,
        )

    async def retrieve(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SGPFile:
        """
        Retrieve a single file's metadata by id.

        Returns the file record (id, filename, MIME type, size, tags, and related
        fields) but not the file's bytes; use the content endpoint to download the
        bytes.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return await self._get(
            path_template("/v5/files/{file_id}", file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SGPFile,
        )

    async def update(
        self,
        file_id: str,
        *,
        tags: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SGPFile:
        """
        Update a file's mutable metadata by id.

        Only the file's `tags` can be modified; filename, content, size, and other
        attributes are immutable through this endpoint. The supplied tags replace the
        file's existing tags. Returns the updated file metadata.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return await self._patch(
            path_template("/v5/files/{file_id}", file_id=file_id),
            body=await async_maybe_transform({"tags": tags}, file_update_params.FileUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SGPFile,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        filename: str | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[SGPFile, AsyncCursorPage[SGPFile]]:
        """
        List the account's files with pagination.

        Optionally filter by `filename` (case-insensitive partial match). Results are
        scoped to the files the caller is authorized to read. Files marked hidden
        (internal or service-owned artifacts) are excluded from this listing but remain
        retrievable by id. Returns file metadata only, not content.

        Args:
          filename: Filter files by filename (case-insensitive partial match)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/files",
            page=AsyncCursorPage[SGPFile],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "filename": filename,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    file_list_params.FileListParams,
                ),
            ),
            model=SGPFile,
        )

    async def delete(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FileDeleteResponse:
        """
        Delete a file by id, removing its database record.

        This is a hard delete: the file's row is removed from the database, not
        soft-archived. The underlying stored object is deleted only when no other file
        record still references the same stored content (identical checksum and MIME
        type); when another record shares the blob, the blob is retained. If the id
        refers to an incomplete multipart upload placeholder, its staged parts are
        aborted instead. Returns a confirmation carrying the deleted file's id.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return await self._delete(
            path_template("/v5/files/{file_id}", file_id=file_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileDeleteResponse,
        )

    async def import_from_cloud(
        self,
        *,
        files: Iterable[file_import_from_cloud_params.File],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FileImportFromCloudResponse:
        """
        Register files that already exist in cloud blob storage as file records, in one
        batch.

        Unlike upload, this transfers no bytes: each entry references an existing object
        by its container/bucket, filepath, filename, and MIME type, and only a metadata
        record pointing at that object is created. Files are imported independently and
        the response reports a per-file status. The response is 200 when every import
        succeeds and 207 when results are mixed, with each result marked SUCCESS or a
        failure reason (file does not exist, invalid permissions, or unknown error).
        Failed entries carry only the submitted filename and MIME type rather than a
        full file record.

        Args:
          files: List of files to import from cloud storage

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/files/cloud_imports",
            body=await async_maybe_transform({"files": files}, file_import_from_cloud_params.FileImportFromCloudParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileImportFromCloudResponse,
        )


class FilesResourceWithRawResponse:
    def __init__(self, files: FilesResource) -> None:
        self._files = files

        self.create = to_raw_response_wrapper(
            files.create,
        )
        self.retrieve = to_raw_response_wrapper(
            files.retrieve,
        )
        self.update = to_raw_response_wrapper(
            files.update,
        )
        self.list = to_raw_response_wrapper(
            files.list,
        )
        self.delete = to_raw_response_wrapper(
            files.delete,
        )
        self.import_from_cloud = to_raw_response_wrapper(
            files.import_from_cloud,
        )

    @cached_property
    def content(self) -> ContentResourceWithRawResponse:
        return ContentResourceWithRawResponse(self._files.content)


class AsyncFilesResourceWithRawResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self._files = files

        self.create = async_to_raw_response_wrapper(
            files.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            files.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            files.update,
        )
        self.list = async_to_raw_response_wrapper(
            files.list,
        )
        self.delete = async_to_raw_response_wrapper(
            files.delete,
        )
        self.import_from_cloud = async_to_raw_response_wrapper(
            files.import_from_cloud,
        )

    @cached_property
    def content(self) -> AsyncContentResourceWithRawResponse:
        return AsyncContentResourceWithRawResponse(self._files.content)


class FilesResourceWithStreamingResponse:
    def __init__(self, files: FilesResource) -> None:
        self._files = files

        self.create = to_streamed_response_wrapper(
            files.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            files.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            files.update,
        )
        self.list = to_streamed_response_wrapper(
            files.list,
        )
        self.delete = to_streamed_response_wrapper(
            files.delete,
        )
        self.import_from_cloud = to_streamed_response_wrapper(
            files.import_from_cloud,
        )

    @cached_property
    def content(self) -> ContentResourceWithStreamingResponse:
        return ContentResourceWithStreamingResponse(self._files.content)


class AsyncFilesResourceWithStreamingResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self._files = files

        self.create = async_to_streamed_response_wrapper(
            files.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            files.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            files.update,
        )
        self.list = async_to_streamed_response_wrapper(
            files.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            files.delete,
        )
        self.import_from_cloud = async_to_streamed_response_wrapper(
            files.import_from_cloud,
        )

    @cached_property
    def content(self) -> AsyncContentResourceWithStreamingResponse:
        return AsyncContentResourceWithStreamingResponse(self._files.content)
