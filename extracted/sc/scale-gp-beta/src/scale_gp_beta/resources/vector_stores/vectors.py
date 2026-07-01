# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorPageVectors, AsyncCursorPageVectors
from ...types.chat import SortOrder
from ..._base_client import AsyncPaginator, make_request_options
from ...types.vector_stores import vector_list_params, vector_retrieve_params
from ...types.chat.sort_order import SortOrder
from ...types.vector_stores.vector_document import VectorDocument

__all__ = ["VectorsResource", "AsyncVectorsResource"]


class VectorsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VectorsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return VectorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VectorsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return VectorsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        vector_id: str,
        *,
        vector_store_name: str,
        include_vectors: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorDocument:
        """
        Retrieve a single document by its unique ID.

        Returns the document's full content, metadata, and optionally its embedding
        vector. Use this endpoint for direct lookups when the exact document ID is
        known. For content similarity search, use the query endpoint.

        Args:
          vector_store_name: The name of the vector store

          vector_id: The ID of the vector to retrieve

          include_vectors: Include embedding vectors

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        if not vector_id:
            raise ValueError(f"Expected a non-empty value for `vector_id` but received {vector_id!r}")
        return self._get(
            path_template(
                "/v5/vector-stores/{vector_store_name}/vectors/{vector_id}",
                vector_store_name=vector_store_name,
                vector_id=vector_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include_vectors": include_vectors}, vector_retrieve_params.VectorRetrieveParams
                ),
            ),
            cast_to=VectorDocument,
        )

    def list(
        self,
        vector_store_name: str,
        *,
        cursor: str | Omit = omit,
        ending_before: str | Omit = omit,
        filter: str | Omit = omit,
        include_vectors: bool | Omit = omit,
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
    ) -> SyncCursorPageVectors[VectorDocument]:
        """
        List documents in a vector store with cursor-based pagination.

        **Use Cases:** Browse documents, export content, audit stored data, or retrieve
        documents by metadata without semantic search.

        **Ordering:** Documents are returned in storage order (insertion order), not
        ranked by similarity. For similarity-based retrieval, use the query endpoint.

        **Filtering:** Apply metadata filters to narrow results to specific subsets
        (e.g., all documents where `category: "research"`). Only indexed fields can be
        used for filtering.

        **Pagination:** Uses cursor-based pagination for efficient traversal of large
        datasets. Pass the `next_cursor` from each response as `starting_after` to
        retrieve the next page, or `prev_cursor` as `ending_before` to retrieve the
        previous page. A null cursor indicates no further pages exist.

        **Embedding Vectors:** Setting `include_vectors=true` includes the full
        embedding vector arrays in the response. This significantly increases payload
        size and reduces the maximum page size from 1000 to 100 documents. Enable only
        when raw vectors are required for external processing.

        Args:
          vector_store_name: The name of the vector store

          cursor: Alias for starting_after. Use starting_after instead.

          filter: Metadata filter expression (JSON)

          include_vectors: Include embedding vectors

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._get_api_list(
            path_template("/v5/vector-stores/{vector_store_name}/vectors", vector_store_name=vector_store_name),
            page=SyncCursorPageVectors[VectorDocument],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "ending_before": ending_before,
                        "filter": filter,
                        "include_vectors": include_vectors,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    vector_list_params.VectorListParams,
                ),
            ),
            model=VectorDocument,
        )


class AsyncVectorsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVectorsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncVectorsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVectorsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncVectorsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        vector_id: str,
        *,
        vector_store_name: str,
        include_vectors: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorDocument:
        """
        Retrieve a single document by its unique ID.

        Returns the document's full content, metadata, and optionally its embedding
        vector. Use this endpoint for direct lookups when the exact document ID is
        known. For content similarity search, use the query endpoint.

        Args:
          vector_store_name: The name of the vector store

          vector_id: The ID of the vector to retrieve

          include_vectors: Include embedding vectors

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        if not vector_id:
            raise ValueError(f"Expected a non-empty value for `vector_id` but received {vector_id!r}")
        return await self._get(
            path_template(
                "/v5/vector-stores/{vector_store_name}/vectors/{vector_id}",
                vector_store_name=vector_store_name,
                vector_id=vector_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include_vectors": include_vectors}, vector_retrieve_params.VectorRetrieveParams
                ),
            ),
            cast_to=VectorDocument,
        )

    def list(
        self,
        vector_store_name: str,
        *,
        cursor: str | Omit = omit,
        ending_before: str | Omit = omit,
        filter: str | Omit = omit,
        include_vectors: bool | Omit = omit,
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
    ) -> AsyncPaginator[VectorDocument, AsyncCursorPageVectors[VectorDocument]]:
        """
        List documents in a vector store with cursor-based pagination.

        **Use Cases:** Browse documents, export content, audit stored data, or retrieve
        documents by metadata without semantic search.

        **Ordering:** Documents are returned in storage order (insertion order), not
        ranked by similarity. For similarity-based retrieval, use the query endpoint.

        **Filtering:** Apply metadata filters to narrow results to specific subsets
        (e.g., all documents where `category: "research"`). Only indexed fields can be
        used for filtering.

        **Pagination:** Uses cursor-based pagination for efficient traversal of large
        datasets. Pass the `next_cursor` from each response as `starting_after` to
        retrieve the next page, or `prev_cursor` as `ending_before` to retrieve the
        previous page. A null cursor indicates no further pages exist.

        **Embedding Vectors:** Setting `include_vectors=true` includes the full
        embedding vector arrays in the response. This significantly increases payload
        size and reduces the maximum page size from 1000 to 100 documents. Enable only
        when raw vectors are required for external processing.

        Args:
          vector_store_name: The name of the vector store

          cursor: Alias for starting_after. Use starting_after instead.

          filter: Metadata filter expression (JSON)

          include_vectors: Include embedding vectors

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._get_api_list(
            path_template("/v5/vector-stores/{vector_store_name}/vectors", vector_store_name=vector_store_name),
            page=AsyncCursorPageVectors[VectorDocument],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "ending_before": ending_before,
                        "filter": filter,
                        "include_vectors": include_vectors,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    vector_list_params.VectorListParams,
                ),
            ),
            model=VectorDocument,
        )


class VectorsResourceWithRawResponse:
    def __init__(self, vectors: VectorsResource) -> None:
        self._vectors = vectors

        self.retrieve = to_raw_response_wrapper(
            vectors.retrieve,
        )
        self.list = to_raw_response_wrapper(
            vectors.list,
        )


class AsyncVectorsResourceWithRawResponse:
    def __init__(self, vectors: AsyncVectorsResource) -> None:
        self._vectors = vectors

        self.retrieve = async_to_raw_response_wrapper(
            vectors.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            vectors.list,
        )


class VectorsResourceWithStreamingResponse:
    def __init__(self, vectors: VectorsResource) -> None:
        self._vectors = vectors

        self.retrieve = to_streamed_response_wrapper(
            vectors.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            vectors.list,
        )


class AsyncVectorsResourceWithStreamingResponse:
    def __init__(self, vectors: AsyncVectorsResource) -> None:
        self._vectors = vectors

        self.retrieve = async_to_streamed_response_wrapper(
            vectors.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            vectors.list,
        )
