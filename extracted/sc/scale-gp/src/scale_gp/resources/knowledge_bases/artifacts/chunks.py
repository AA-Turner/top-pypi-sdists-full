# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncPageResponse, AsyncPageResponse
from ...._base_client import AsyncPaginator, make_request_options
from ....types.knowledge_bases.artifacts import chunk_put_params, chunk_list_params, chunk_create_params
from ....types.knowledge_bases.artifacts.chunk_put_response import ChunkPutResponse
from ....types.knowledge_bases.artifacts.chunk_list_response import ChunkListResponse
from ....types.knowledge_bases.artifacts.chunk_create_response import ChunkCreateResponse
from ....types.knowledge_bases.artifacts.chunk_delete_response import ChunkDeleteResponse
from ....types.knowledge_bases.artifacts.chunk_retrieve_response import ChunkRetrieveResponse

__all__ = ["ChunksResource", "AsyncChunksResource"]


class ChunksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChunksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ChunksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChunksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ChunksResourceWithStreamingResponse(self)

    def create(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        chunk_position: int,
        text: str,
        metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChunkCreateResponse:
        """
        Create chunk for local chunk artifacts

        Args:
          chunk_position: Position of the chunk in the artifact.

          text: Associated text of the chunk.

          metadata: Additional metadata associated with the chunk.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks",
            body=maybe_transform(
                {
                    "chunk_position": chunk_position,
                    "text": text,
                    "metadata": metadata,
                },
                chunk_create_params.ChunkCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkCreateResponse,
        )

    def retrieve(
        self,
        chunk_id: str,
        *,
        knowledge_base_id: str,
        artifact_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChunkRetrieveResponse:
        """
        Get Single Chunk Information and status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        if not chunk_id:
            raise ValueError(f"Expected a non-empty value for `chunk_id` but received {chunk_id!r}")
        return self._get(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks/{chunk_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkRetrieveResponse,
        )

    def list(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        chunk_status: Literal["Pending", "Completed", "Failed"] | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[ChunkListResponse]:
        """### Description

        List chunks for a specific artifact.

        This API supports pagination and reads only
        from the data store to allow querying chunks that are failed as well to
        enumerate all chunks of a specific artifact.

        Args:
          chunk_status: Filter by the status of the chunks

          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return self._get_api_list(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks",
            page=SyncPageResponse[ChunkListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "chunk_status": chunk_status,
                        "limit": limit,
                        "page": page,
                    },
                    chunk_list_params.ChunkListParams,
                ),
            ),
            model=ChunkListResponse,
        )

    def delete(
        self,
        chunk_id: str,
        *,
        knowledge_base_id: str,
        artifact_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChunkDeleteResponse:
        """
        Delete Single Chunk from Local Artifact

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        if not chunk_id:
            raise ValueError(f"Expected a non-empty value for `chunk_id` but received {chunk_id!r}")
        return self._delete(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks/{chunk_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkDeleteResponse,
        )

    def put(
        self,
        chunk_id: str,
        *,
        knowledge_base_id: str,
        artifact_id: str,
        chunk_position: int,
        text: str,
        metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChunkPutResponse:
        """
        Update Single Chunk data for local artifact

        Args:
          chunk_position: Position of the chunk in the artifact.

          text: Associated text of the chunk.

          metadata: Additional metadata associated with the chunk.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        if not chunk_id:
            raise ValueError(f"Expected a non-empty value for `chunk_id` but received {chunk_id!r}")
        return self._put(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks/{chunk_id}",
            body=maybe_transform(
                {
                    "chunk_position": chunk_position,
                    "text": text,
                    "metadata": metadata,
                },
                chunk_put_params.ChunkPutParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkPutResponse,
        )


class AsyncChunksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChunksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChunksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChunksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncChunksResourceWithStreamingResponse(self)

    async def create(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        chunk_position: int,
        text: str,
        metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChunkCreateResponse:
        """
        Create chunk for local chunk artifacts

        Args:
          chunk_position: Position of the chunk in the artifact.

          text: Associated text of the chunk.

          metadata: Additional metadata associated with the chunk.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return await self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks",
            body=await async_maybe_transform(
                {
                    "chunk_position": chunk_position,
                    "text": text,
                    "metadata": metadata,
                },
                chunk_create_params.ChunkCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkCreateResponse,
        )

    async def retrieve(
        self,
        chunk_id: str,
        *,
        knowledge_base_id: str,
        artifact_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChunkRetrieveResponse:
        """
        Get Single Chunk Information and status

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        if not chunk_id:
            raise ValueError(f"Expected a non-empty value for `chunk_id` but received {chunk_id!r}")
        return await self._get(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks/{chunk_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkRetrieveResponse,
        )

    def list(
        self,
        artifact_id: str,
        *,
        knowledge_base_id: str,
        chunk_status: Literal["Pending", "Completed", "Failed"] | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ChunkListResponse, AsyncPageResponse[ChunkListResponse]]:
        """### Description

        List chunks for a specific artifact.

        This API supports pagination and reads only
        from the data store to allow querying chunks that are failed as well to
        enumerate all chunks of a specific artifact.

        Args:
          chunk_status: Filter by the status of the chunks

          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        return self._get_api_list(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks",
            page=AsyncPageResponse[ChunkListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "chunk_status": chunk_status,
                        "limit": limit,
                        "page": page,
                    },
                    chunk_list_params.ChunkListParams,
                ),
            ),
            model=ChunkListResponse,
        )

    async def delete(
        self,
        chunk_id: str,
        *,
        knowledge_base_id: str,
        artifact_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChunkDeleteResponse:
        """
        Delete Single Chunk from Local Artifact

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        if not chunk_id:
            raise ValueError(f"Expected a non-empty value for `chunk_id` but received {chunk_id!r}")
        return await self._delete(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks/{chunk_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkDeleteResponse,
        )

    async def put(
        self,
        chunk_id: str,
        *,
        knowledge_base_id: str,
        artifact_id: str,
        chunk_position: int,
        text: str,
        metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChunkPutResponse:
        """
        Update Single Chunk data for local artifact

        Args:
          chunk_position: Position of the chunk in the artifact.

          text: Associated text of the chunk.

          metadata: Additional metadata associated with the chunk.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not artifact_id:
            raise ValueError(f"Expected a non-empty value for `artifact_id` but received {artifact_id!r}")
        if not chunk_id:
            raise ValueError(f"Expected a non-empty value for `chunk_id` but received {chunk_id!r}")
        return await self._put(
            f"/v4/knowledge-bases/{knowledge_base_id}/artifacts/{artifact_id}/chunks/{chunk_id}",
            body=await async_maybe_transform(
                {
                    "chunk_position": chunk_position,
                    "text": text,
                    "metadata": metadata,
                },
                chunk_put_params.ChunkPutParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChunkPutResponse,
        )


class ChunksResourceWithRawResponse:
    def __init__(self, chunks: ChunksResource) -> None:
        self._chunks = chunks

        self.create = to_raw_response_wrapper(
            chunks.create,
        )
        self.retrieve = to_raw_response_wrapper(
            chunks.retrieve,
        )
        self.list = to_raw_response_wrapper(
            chunks.list,
        )
        self.delete = to_raw_response_wrapper(
            chunks.delete,
        )
        self.put = to_raw_response_wrapper(
            chunks.put,
        )


class AsyncChunksResourceWithRawResponse:
    def __init__(self, chunks: AsyncChunksResource) -> None:
        self._chunks = chunks

        self.create = async_to_raw_response_wrapper(
            chunks.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            chunks.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            chunks.list,
        )
        self.delete = async_to_raw_response_wrapper(
            chunks.delete,
        )
        self.put = async_to_raw_response_wrapper(
            chunks.put,
        )


class ChunksResourceWithStreamingResponse:
    def __init__(self, chunks: ChunksResource) -> None:
        self._chunks = chunks

        self.create = to_streamed_response_wrapper(
            chunks.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            chunks.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            chunks.list,
        )
        self.delete = to_streamed_response_wrapper(
            chunks.delete,
        )
        self.put = to_streamed_response_wrapper(
            chunks.put,
        )


class AsyncChunksResourceWithStreamingResponse:
    def __init__(self, chunks: AsyncChunksResource) -> None:
        self._chunks = chunks

        self.create = async_to_streamed_response_wrapper(
            chunks.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            chunks.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            chunks.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            chunks.delete,
        )
        self.put = async_to_streamed_response_wrapper(
            chunks.put,
        )
