# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal

import httpx

from ...types import (
    EmbeddingModelName,
    vector_store_list_params,
    vector_store_count_params,
    vector_store_query_params,
    vector_store_create_params,
    vector_store_delete_params,
    vector_store_upsert_params,
    vector_store_configure_params,
)
from .vectors import (
    VectorsResource,
    AsyncVectorsResource,
    VectorsResourceWithRawResponse,
    AsyncVectorsResourceWithRawResponse,
    VectorsResourceWithStreamingResponse,
    AsyncVectorsResourceWithStreamingResponse,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorPageByName, AsyncCursorPageByName
from ...types.chat import SortOrder
from ..._base_client import AsyncPaginator, make_request_options
from ...types.vector_store import VectorStore
from ...types.chat.sort_order import SortOrder
from ...types.text_content_param import TextContentParam
from ...types.embedding_model_name import EmbeddingModelName
from ...types.embedding_config_param import EmbeddingConfigParam
from ...types.vector_store_drop_response import VectorStoreDropResponse
from ...types.vector_store_count_response import VectorStoreCountResponse
from ...types.vector_store_query_response import VectorStoreQueryResponse
from ...types.vector_store_delete_response import VectorStoreDeleteResponse
from ...types.vector_store_upsert_response import VectorStoreUpsertResponse

__all__ = ["VectorStoresResource", "AsyncVectorStoresResource"]


class VectorStoresResource(SyncAPIResource):
    @cached_property
    def vectors(self) -> VectorsResource:
        return VectorsResource(self._client)

    @cached_property
    def with_raw_response(self) -> VectorStoresResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return VectorStoresResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VectorStoresResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return VectorStoresResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        dimensions: int | Omit = omit,
        embedding_config: EmbeddingConfigParam | Omit = omit,
        embedding_model: EmbeddingModelName | Omit = omit,
        indexed_metadata_fields: Dict[str, Literal["string", "number", "boolean"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStore:
        """
        Create a new vector store for storing and querying document embeddings.

        The vector store name must be unique within your account and follow naming
        conventions (3-63 characters, alphanumeric with hyphens/underscores). Once
        created, the embedding configuration and dimensions are immutable and cannot be
        changed. To use a different model, you must create a new vector store.

        **Embedding Configuration:** Provide `embedding_config` (for base or custom
        model deployments), `embedding_model` (shorthand for a base model), or
        `dimensions` only (raw embeddings).

        - With `embedding_config` or `embedding_model`: dimensions are auto-derived, and
          documents can be upserted with text content (auto-embedded) or with
          pre-computed embeddings.
        - With `dimensions` only: the store accepts only pre-computed embeddings.
          Semantic/hybrid queries are not supported (lexical search only).

        **Indexed Fields:** Optionally specify metadata fields to index at creation
        time. Only indexed fields can be used for filtering -- indexing is required, not
        just a performance optimization. Additional indexed fields can be added later
        using the configure endpoint, but cannot be removed once added. Keep in mind
        that each indexed field increases write latency and storage overhead, so only
        index fields you actively filter on.

        Args:
          name: A unique name for the vector store within the account

          dimensions: Dimension size of embedding vectors. Required when neither 'embedding_config'
              nor 'embedding_model' is set. Automatically derived when an embedding model is
              provided.

          embedding_config: The embedding configuration. Either 'base' type with an embedding_model, or
              'models_api' type with a model_deployment_id for custom models.

          embedding_model: The base embedding model to use. Shorthand for embedding_config with type
              'base'. Provide either embedding_config or embedding_model, not both.

          indexed_metadata_fields: Dictionary mapping metadata field names to their types for efficient filtering.
              Only STRING, NUMBER, and BOOLEAN types can be indexed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v5/vector-stores/create",
            body=maybe_transform(
                {
                    "name": name,
                    "dimensions": dimensions,
                    "embedding_config": embedding_config,
                    "embedding_model": embedding_model,
                    "indexed_metadata_fields": indexed_metadata_fields,
                },
                vector_store_create_params.VectorStoreCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStore,
        )

    def retrieve(
        self,
        vector_store_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStore:
        """
        Retrieve detailed configuration and metadata for a specific vector store.

        Returns the store's embedding model, dimensions, indexed metadata field
        definitions, creation timestamp, and last update timestamp. Use this to verify
        store settings before performing operations or to display store information in
        your application.

        Args:
          vector_store_name: The name of the vector store

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._get(
            path_template("/v5/vector-stores/{vector_store_name}", vector_store_name=vector_store_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStore,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
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
    ) -> SyncCursorPageByName[VectorStore]:
        """
        List all vector stores in your account with pagination.

        Returns vector stores sorted by creation date (newest first). Each store
        includes its configuration, embedding model, dimensions, indexed fields, and
        timestamps.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/vector-stores",
            page=SyncCursorPageByName[VectorStore],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    vector_store_list_params.VectorStoreListParams,
                ),
            ),
            model=VectorStore,
        )

    def delete(
        self,
        vector_store_name: str,
        *,
        filter: Dict[str, object] | Omit = omit,
        ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreDeleteResponse:
        """
        Delete documents from a vector store by document IDs or metadata filter
        criteria.

        **Delete by IDs:** Provide an array of document IDs to delete specific
        documents. Non-existent documents are silently skipped.

        **Delete by Filter:** Use metadata filters to delete all documents matching the
        specified criteria (e.g., delete all documents where `status: "archived"`). The
        filter must specify at least one condition and cannot be empty. To delete all
        documents, use the drop endpoint instead.

        **Filter Operators:** Supports MongoDB-style operators including equality
        (`{"field": "value"}`), comparison (`$gt`, `$gte`, `$lt`, `$lte`, `$eq`, `$ne`),
        logical (`$and`, `$or`, `$not`), and membership (`$in`, `$nin`). Only indexed
        metadata fields can be used for filtering.

        **Best Practice:** Use the count endpoint with the same filter to preview the
        number of documents that will be deleted before executing the deletion
        operation.

        Args:
          vector_store_name: The name of the vector store

          filter: Metadata filter expression for deletion

          ids: Array of document IDs to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._post(
            path_template("/v5/vector-stores/{vector_store_name}/delete", vector_store_name=vector_store_name),
            body=maybe_transform(
                {
                    "filter": filter,
                    "ids": ids,
                },
                vector_store_delete_params.VectorStoreDeleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreDeleteResponse,
        )

    def configure(
        self,
        vector_store_name: str,
        *,
        indexed_metadata_fields: Dict[str, Literal["string", "number", "boolean"]],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStore:
        """
        Update the indexed metadata fields configuration for a vector store.

        This replaces the current set of indexed metadata fields. Only indexed fields
        can be used for filtering during query, list, and count operations; non-indexed
        fields are still stored and returned, but cannot be filtered on.

        **Field Types:** Only STRING, NUMBER, and BOOLEAN fields can be indexed (maximum
        20 fields). OBJECT and LIST types are stored but cannot be indexed for
        filtering.

        **Adding Fields:** New indexed fields can be added at any time. They are indexed
        for documents upserted after the change; to make existing documents filterable
        on a new field, re-upsert them.

        **Removing Fields:** Omitting a field removes it from this configuration, so it
        can no longer be filtered on. The underlying index is append-only, so removal
        does not reclaim storage or reduce write overhead; the field stays in the
        physical index until the store is recreated. Prefer indexing only the fields you
        filter on.

        **Note:** The `name` and `embedding_config` are immutable after creation.

        Args:
          vector_store_name: The name of the vector store

          indexed_metadata_fields: Dictionary mapping metadata field names to their types. Only STRING, NUMBER, and
              BOOLEAN types can be indexed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._post(
            path_template("/v5/vector-stores/{vector_store_name}/configure", vector_store_name=vector_store_name),
            body=maybe_transform(
                {"indexed_metadata_fields": indexed_metadata_fields},
                vector_store_configure_params.VectorStoreConfigureParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStore,
        )

    def count(
        self,
        vector_store_name: str,
        *,
        filter: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreCountResponse:
        """
        Count documents in a vector store, optionally filtered by metadata.

        **Use Cases:**

        - Monitor vector store size and growth over time
        - Preview the number of documents matching a filter before deletion
        - Validate data ingestion by comparing expected versus actual document counts
        - Analyze document distribution across metadata categories

        **Filtering:** Apply the same metadata filter syntax as delete and list
        operations. Only indexed fields can be used for filtering. An empty filter
        counts all documents in the store.

        Args:
          vector_store_name: The name of the vector store

          filter: Metadata filter expression

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._post(
            path_template("/v5/vector-stores/{vector_store_name}/count", vector_store_name=vector_store_name),
            body=maybe_transform({"filter": filter}, vector_store_count_params.VectorStoreCountParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreCountResponse,
        )

    def drop(
        self,
        vector_store_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreDropResponse:
        """
        Permanently delete a vector store and all its contents.

        **⚠️ WARNING:** This is a destructive operation that cannot be undone. All
        documents, embeddings, metadata, and index configurations will be permanently
        deleted. Data recovery is not possible after deletion.

        Args:
          vector_store_name: The name of the vector store

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._post(
            path_template("/v5/vector-stores/{vector_store_name}/drop", vector_store_name=vector_store_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreDropResponse,
        )

    def query(
        self,
        vector_store_name: str,
        *,
        content: TextContentParam,
        filter: Dict[str, object] | Omit = omit,
        include_vectors: bool | Omit = omit,
        query_type: Literal["semantic", "lexical", "hybrid"] | Omit = omit,
        rerank: bool | Omit = omit,
        rerank_config: vector_store_query_params.RerankConfig | Omit = omit,
        rerank_instruction: str | Omit = omit,
        rerank_model: str | Omit = omit,
        rerank_top_n: int | Omit = omit,
        top_k: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreQueryResponse:
        """
        Query documents using similarity search with optional reranking.

        Primary endpoint for semantic search, question-answering, and RAG
        (Retrieval-Augmented Generation) applications. Returns documents ranked by
        relevance to the query text with similarity scores.

        **Query Types:**

        - `semantic` (default): Approximate nearest-neighbor search using HNSW over
          cosine similarity of document embeddings. Optimal for question-answering,
          conceptual search, and finding semantically related content without requiring
          exact keyword matches.
        - `lexical`: Keyword-based text search (BM25 algorithm). Optimal for exact
          phrase matching, proper nouns, and scenarios where keyword presence is more
          important than semantic similarity.
        - `hybrid`: Combines semantic and lexical approaches with weighted scoring.
          Provides maximum recall by identifying documents matching either semantically
          or lexically.

        **Metadata Filtering:** Narrow the search scope by applying metadata filters
        (e.g., search only documents where `category: "technical"`). Only indexed fields
        can be used for filtering. Filters are applied before similarity search for
        optimal efficiency.

        **Reranking (Advanced):** Optionally enhance result quality using a
        cross-encoder reranking model. The reranker rescores the initial results using a
        more sophisticated model that evaluates the complete query-document pair (not
        solely embeddings). This adds 100-500ms latency but significantly improves
        precision for high-stakes applications.

        **Reranking Strategy:** Set `top_k` higher than the desired final count
        (e.g., 50) to retrieve more candidates from the initial search. Then configure
        `rerank_top_n` to the desired final count (e.g., 10) to return only the most
        relevant documents after reranking. This two-stage approach maximizes both
        recall and precision.

        **Performance Metrics:** The response includes detailed timing breakdowns
        (embedding generation time, index query time, reranking time) to facilitate
        search pipeline optimization and latency analysis.

        **Similarity Scores:** Each result includes a `score` field indicating
        relevance. Higher scores indicate greater relevance. Score ranges and semantics
        vary by query type (semantic scores use cosine similarity, lexical scores use
        BM25, hybrid scores combine both approaches).

        Args:
          vector_store_name: The name of the vector store

          content: Text content for documents.

          filter: Metadata filter expression

          include_vectors: Include embedding vectors in response

          query_type: Query type: semantic, lexical, or hybrid

          rerank: [Deprecated: use rerank_config] Enable reranking of search results

          rerank_config: Reranking configuration. Presence enables reranking; omit to disable. Pass an
              empty object ({}) to enable reranking with system defaults.

          rerank_instruction: [Deprecated: use rerank_config.instruction] Custom instruction for reranker

          rerank_model: [Deprecated: use rerank_config.model] Reranking model to use

          rerank_top_n: [Deprecated: use rerank_config.top_n] Number of results after reranking

          top_k: Number of search results to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._post(
            path_template("/v5/vector-stores/{vector_store_name}/query", vector_store_name=vector_store_name),
            body=maybe_transform(
                {
                    "content": content,
                    "filter": filter,
                    "include_vectors": include_vectors,
                    "query_type": query_type,
                    "rerank": rerank,
                    "rerank_config": rerank_config,
                    "rerank_instruction": rerank_instruction,
                    "rerank_model": rerank_model,
                    "rerank_top_n": rerank_top_n,
                    "top_k": top_k,
                },
                vector_store_query_params.VectorStoreQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreQueryResponse,
        )

    def upsert(
        self,
        vector_store_name: str,
        *,
        vectors: Iterable[vector_store_upsert_params.Vector],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreUpsertResponse:
        """
        Insert new documents or update existing documents in a vector store.

        **Upsert Behavior:** If a document ID already exists, it will be completely
        replaced with the new content and metadata. The previous document's text,
        embedding, and all metadata fields are discarded. If the ID does not exist, a
        new document is created.

        **Document Content:** Each document supports several modes:

        - `content` only: text is automatically embedded using the store's configured
          model.
        - `embedding` only: pre-computed embedding vector is used directly. Dimension
          must match the store's configuration.
        - Both `content` and `embedding`: the pre-computed embedding is stored and text
          is kept for retrieval/search.
        - Neither (metadata-only): only metadata is updated on an existing document
          without re-embedding. If the document does not exist, it will appear as a
          failure in the batch response.

        A store created without an embedding model (dimensions-only) only accepts
        documents with pre-computed `embedding`.

        **Batch Operations:** This endpoint supports batch operations with partial
        success handling and mixed document types (some with raw embeddings, some with
        content) in the same call.

        **Metadata:** Supports nested metadata with string, number, boolean, object, and
        array types. Null values are not permitted—omit the field or use an empty string
        instead.

        Args:
          vector_store_name: The name of the vector store

          vectors: Array of documents to upsert

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return self._post(
            path_template("/v5/vector-stores/{vector_store_name}/upsert", vector_store_name=vector_store_name),
            body=maybe_transform({"vectors": vectors}, vector_store_upsert_params.VectorStoreUpsertParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreUpsertResponse,
        )


class AsyncVectorStoresResource(AsyncAPIResource):
    @cached_property
    def vectors(self) -> AsyncVectorsResource:
        return AsyncVectorsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVectorStoresResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncVectorStoresResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVectorStoresResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncVectorStoresResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        dimensions: int | Omit = omit,
        embedding_config: EmbeddingConfigParam | Omit = omit,
        embedding_model: EmbeddingModelName | Omit = omit,
        indexed_metadata_fields: Dict[str, Literal["string", "number", "boolean"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStore:
        """
        Create a new vector store for storing and querying document embeddings.

        The vector store name must be unique within your account and follow naming
        conventions (3-63 characters, alphanumeric with hyphens/underscores). Once
        created, the embedding configuration and dimensions are immutable and cannot be
        changed. To use a different model, you must create a new vector store.

        **Embedding Configuration:** Provide `embedding_config` (for base or custom
        model deployments), `embedding_model` (shorthand for a base model), or
        `dimensions` only (raw embeddings).

        - With `embedding_config` or `embedding_model`: dimensions are auto-derived, and
          documents can be upserted with text content (auto-embedded) or with
          pre-computed embeddings.
        - With `dimensions` only: the store accepts only pre-computed embeddings.
          Semantic/hybrid queries are not supported (lexical search only).

        **Indexed Fields:** Optionally specify metadata fields to index at creation
        time. Only indexed fields can be used for filtering -- indexing is required, not
        just a performance optimization. Additional indexed fields can be added later
        using the configure endpoint, but cannot be removed once added. Keep in mind
        that each indexed field increases write latency and storage overhead, so only
        index fields you actively filter on.

        Args:
          name: A unique name for the vector store within the account

          dimensions: Dimension size of embedding vectors. Required when neither 'embedding_config'
              nor 'embedding_model' is set. Automatically derived when an embedding model is
              provided.

          embedding_config: The embedding configuration. Either 'base' type with an embedding_model, or
              'models_api' type with a model_deployment_id for custom models.

          embedding_model: The base embedding model to use. Shorthand for embedding_config with type
              'base'. Provide either embedding_config or embedding_model, not both.

          indexed_metadata_fields: Dictionary mapping metadata field names to their types for efficient filtering.
              Only STRING, NUMBER, and BOOLEAN types can be indexed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v5/vector-stores/create",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "dimensions": dimensions,
                    "embedding_config": embedding_config,
                    "embedding_model": embedding_model,
                    "indexed_metadata_fields": indexed_metadata_fields,
                },
                vector_store_create_params.VectorStoreCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStore,
        )

    async def retrieve(
        self,
        vector_store_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStore:
        """
        Retrieve detailed configuration and metadata for a specific vector store.

        Returns the store's embedding model, dimensions, indexed metadata field
        definitions, creation timestamp, and last update timestamp. Use this to verify
        store settings before performing operations or to display store information in
        your application.

        Args:
          vector_store_name: The name of the vector store

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return await self._get(
            path_template("/v5/vector-stores/{vector_store_name}", vector_store_name=vector_store_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStore,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
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
    ) -> AsyncPaginator[VectorStore, AsyncCursorPageByName[VectorStore]]:
        """
        List all vector stores in your account with pagination.

        Returns vector stores sorted by creation date (newest first). Each store
        includes its configuration, embedding model, dimensions, indexed fields, and
        timestamps.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/vector-stores",
            page=AsyncCursorPageByName[VectorStore],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    vector_store_list_params.VectorStoreListParams,
                ),
            ),
            model=VectorStore,
        )

    async def delete(
        self,
        vector_store_name: str,
        *,
        filter: Dict[str, object] | Omit = omit,
        ids: SequenceNotStr[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreDeleteResponse:
        """
        Delete documents from a vector store by document IDs or metadata filter
        criteria.

        **Delete by IDs:** Provide an array of document IDs to delete specific
        documents. Non-existent documents are silently skipped.

        **Delete by Filter:** Use metadata filters to delete all documents matching the
        specified criteria (e.g., delete all documents where `status: "archived"`). The
        filter must specify at least one condition and cannot be empty. To delete all
        documents, use the drop endpoint instead.

        **Filter Operators:** Supports MongoDB-style operators including equality
        (`{"field": "value"}`), comparison (`$gt`, `$gte`, `$lt`, `$lte`, `$eq`, `$ne`),
        logical (`$and`, `$or`, `$not`), and membership (`$in`, `$nin`). Only indexed
        metadata fields can be used for filtering.

        **Best Practice:** Use the count endpoint with the same filter to preview the
        number of documents that will be deleted before executing the deletion
        operation.

        Args:
          vector_store_name: The name of the vector store

          filter: Metadata filter expression for deletion

          ids: Array of document IDs to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return await self._post(
            path_template("/v5/vector-stores/{vector_store_name}/delete", vector_store_name=vector_store_name),
            body=await async_maybe_transform(
                {
                    "filter": filter,
                    "ids": ids,
                },
                vector_store_delete_params.VectorStoreDeleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreDeleteResponse,
        )

    async def configure(
        self,
        vector_store_name: str,
        *,
        indexed_metadata_fields: Dict[str, Literal["string", "number", "boolean"]],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStore:
        """
        Update the indexed metadata fields configuration for a vector store.

        This replaces the current set of indexed metadata fields. Only indexed fields
        can be used for filtering during query, list, and count operations; non-indexed
        fields are still stored and returned, but cannot be filtered on.

        **Field Types:** Only STRING, NUMBER, and BOOLEAN fields can be indexed (maximum
        20 fields). OBJECT and LIST types are stored but cannot be indexed for
        filtering.

        **Adding Fields:** New indexed fields can be added at any time. They are indexed
        for documents upserted after the change; to make existing documents filterable
        on a new field, re-upsert them.

        **Removing Fields:** Omitting a field removes it from this configuration, so it
        can no longer be filtered on. The underlying index is append-only, so removal
        does not reclaim storage or reduce write overhead; the field stays in the
        physical index until the store is recreated. Prefer indexing only the fields you
        filter on.

        **Note:** The `name` and `embedding_config` are immutable after creation.

        Args:
          vector_store_name: The name of the vector store

          indexed_metadata_fields: Dictionary mapping metadata field names to their types. Only STRING, NUMBER, and
              BOOLEAN types can be indexed.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return await self._post(
            path_template("/v5/vector-stores/{vector_store_name}/configure", vector_store_name=vector_store_name),
            body=await async_maybe_transform(
                {"indexed_metadata_fields": indexed_metadata_fields},
                vector_store_configure_params.VectorStoreConfigureParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStore,
        )

    async def count(
        self,
        vector_store_name: str,
        *,
        filter: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreCountResponse:
        """
        Count documents in a vector store, optionally filtered by metadata.

        **Use Cases:**

        - Monitor vector store size and growth over time
        - Preview the number of documents matching a filter before deletion
        - Validate data ingestion by comparing expected versus actual document counts
        - Analyze document distribution across metadata categories

        **Filtering:** Apply the same metadata filter syntax as delete and list
        operations. Only indexed fields can be used for filtering. An empty filter
        counts all documents in the store.

        Args:
          vector_store_name: The name of the vector store

          filter: Metadata filter expression

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return await self._post(
            path_template("/v5/vector-stores/{vector_store_name}/count", vector_store_name=vector_store_name),
            body=await async_maybe_transform({"filter": filter}, vector_store_count_params.VectorStoreCountParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreCountResponse,
        )

    async def drop(
        self,
        vector_store_name: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreDropResponse:
        """
        Permanently delete a vector store and all its contents.

        **⚠️ WARNING:** This is a destructive operation that cannot be undone. All
        documents, embeddings, metadata, and index configurations will be permanently
        deleted. Data recovery is not possible after deletion.

        Args:
          vector_store_name: The name of the vector store

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return await self._post(
            path_template("/v5/vector-stores/{vector_store_name}/drop", vector_store_name=vector_store_name),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreDropResponse,
        )

    async def query(
        self,
        vector_store_name: str,
        *,
        content: TextContentParam,
        filter: Dict[str, object] | Omit = omit,
        include_vectors: bool | Omit = omit,
        query_type: Literal["semantic", "lexical", "hybrid"] | Omit = omit,
        rerank: bool | Omit = omit,
        rerank_config: vector_store_query_params.RerankConfig | Omit = omit,
        rerank_instruction: str | Omit = omit,
        rerank_model: str | Omit = omit,
        rerank_top_n: int | Omit = omit,
        top_k: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreQueryResponse:
        """
        Query documents using similarity search with optional reranking.

        Primary endpoint for semantic search, question-answering, and RAG
        (Retrieval-Augmented Generation) applications. Returns documents ranked by
        relevance to the query text with similarity scores.

        **Query Types:**

        - `semantic` (default): Approximate nearest-neighbor search using HNSW over
          cosine similarity of document embeddings. Optimal for question-answering,
          conceptual search, and finding semantically related content without requiring
          exact keyword matches.
        - `lexical`: Keyword-based text search (BM25 algorithm). Optimal for exact
          phrase matching, proper nouns, and scenarios where keyword presence is more
          important than semantic similarity.
        - `hybrid`: Combines semantic and lexical approaches with weighted scoring.
          Provides maximum recall by identifying documents matching either semantically
          or lexically.

        **Metadata Filtering:** Narrow the search scope by applying metadata filters
        (e.g., search only documents where `category: "technical"`). Only indexed fields
        can be used for filtering. Filters are applied before similarity search for
        optimal efficiency.

        **Reranking (Advanced):** Optionally enhance result quality using a
        cross-encoder reranking model. The reranker rescores the initial results using a
        more sophisticated model that evaluates the complete query-document pair (not
        solely embeddings). This adds 100-500ms latency but significantly improves
        precision for high-stakes applications.

        **Reranking Strategy:** Set `top_k` higher than the desired final count
        (e.g., 50) to retrieve more candidates from the initial search. Then configure
        `rerank_top_n` to the desired final count (e.g., 10) to return only the most
        relevant documents after reranking. This two-stage approach maximizes both
        recall and precision.

        **Performance Metrics:** The response includes detailed timing breakdowns
        (embedding generation time, index query time, reranking time) to facilitate
        search pipeline optimization and latency analysis.

        **Similarity Scores:** Each result includes a `score` field indicating
        relevance. Higher scores indicate greater relevance. Score ranges and semantics
        vary by query type (semantic scores use cosine similarity, lexical scores use
        BM25, hybrid scores combine both approaches).

        Args:
          vector_store_name: The name of the vector store

          content: Text content for documents.

          filter: Metadata filter expression

          include_vectors: Include embedding vectors in response

          query_type: Query type: semantic, lexical, or hybrid

          rerank: [Deprecated: use rerank_config] Enable reranking of search results

          rerank_config: Reranking configuration. Presence enables reranking; omit to disable. Pass an
              empty object ({}) to enable reranking with system defaults.

          rerank_instruction: [Deprecated: use rerank_config.instruction] Custom instruction for reranker

          rerank_model: [Deprecated: use rerank_config.model] Reranking model to use

          rerank_top_n: [Deprecated: use rerank_config.top_n] Number of results after reranking

          top_k: Number of search results to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return await self._post(
            path_template("/v5/vector-stores/{vector_store_name}/query", vector_store_name=vector_store_name),
            body=await async_maybe_transform(
                {
                    "content": content,
                    "filter": filter,
                    "include_vectors": include_vectors,
                    "query_type": query_type,
                    "rerank": rerank,
                    "rerank_config": rerank_config,
                    "rerank_instruction": rerank_instruction,
                    "rerank_model": rerank_model,
                    "rerank_top_n": rerank_top_n,
                    "top_k": top_k,
                },
                vector_store_query_params.VectorStoreQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreQueryResponse,
        )

    async def upsert(
        self,
        vector_store_name: str,
        *,
        vectors: Iterable[vector_store_upsert_params.Vector],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VectorStoreUpsertResponse:
        """
        Insert new documents or update existing documents in a vector store.

        **Upsert Behavior:** If a document ID already exists, it will be completely
        replaced with the new content and metadata. The previous document's text,
        embedding, and all metadata fields are discarded. If the ID does not exist, a
        new document is created.

        **Document Content:** Each document supports several modes:

        - `content` only: text is automatically embedded using the store's configured
          model.
        - `embedding` only: pre-computed embedding vector is used directly. Dimension
          must match the store's configuration.
        - Both `content` and `embedding`: the pre-computed embedding is stored and text
          is kept for retrieval/search.
        - Neither (metadata-only): only metadata is updated on an existing document
          without re-embedding. If the document does not exist, it will appear as a
          failure in the batch response.

        A store created without an embedding model (dimensions-only) only accepts
        documents with pre-computed `embedding`.

        **Batch Operations:** This endpoint supports batch operations with partial
        success handling and mixed document types (some with raw embeddings, some with
        content) in the same call.

        **Metadata:** Supports nested metadata with string, number, boolean, object, and
        array types. Null values are not permitted—omit the field or use an empty string
        instead.

        Args:
          vector_store_name: The name of the vector store

          vectors: Array of documents to upsert

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not vector_store_name:
            raise ValueError(f"Expected a non-empty value for `vector_store_name` but received {vector_store_name!r}")
        return await self._post(
            path_template("/v5/vector-stores/{vector_store_name}/upsert", vector_store_name=vector_store_name),
            body=await async_maybe_transform({"vectors": vectors}, vector_store_upsert_params.VectorStoreUpsertParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VectorStoreUpsertResponse,
        )


class VectorStoresResourceWithRawResponse:
    def __init__(self, vector_stores: VectorStoresResource) -> None:
        self._vector_stores = vector_stores

        self.create = to_raw_response_wrapper(
            vector_stores.create,
        )
        self.retrieve = to_raw_response_wrapper(
            vector_stores.retrieve,
        )
        self.list = to_raw_response_wrapper(
            vector_stores.list,
        )
        self.delete = to_raw_response_wrapper(
            vector_stores.delete,
        )
        self.configure = to_raw_response_wrapper(
            vector_stores.configure,
        )
        self.count = to_raw_response_wrapper(
            vector_stores.count,
        )
        self.drop = to_raw_response_wrapper(
            vector_stores.drop,
        )
        self.query = to_raw_response_wrapper(
            vector_stores.query,
        )
        self.upsert = to_raw_response_wrapper(
            vector_stores.upsert,
        )

    @cached_property
    def vectors(self) -> VectorsResourceWithRawResponse:
        return VectorsResourceWithRawResponse(self._vector_stores.vectors)


class AsyncVectorStoresResourceWithRawResponse:
    def __init__(self, vector_stores: AsyncVectorStoresResource) -> None:
        self._vector_stores = vector_stores

        self.create = async_to_raw_response_wrapper(
            vector_stores.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            vector_stores.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            vector_stores.list,
        )
        self.delete = async_to_raw_response_wrapper(
            vector_stores.delete,
        )
        self.configure = async_to_raw_response_wrapper(
            vector_stores.configure,
        )
        self.count = async_to_raw_response_wrapper(
            vector_stores.count,
        )
        self.drop = async_to_raw_response_wrapper(
            vector_stores.drop,
        )
        self.query = async_to_raw_response_wrapper(
            vector_stores.query,
        )
        self.upsert = async_to_raw_response_wrapper(
            vector_stores.upsert,
        )

    @cached_property
    def vectors(self) -> AsyncVectorsResourceWithRawResponse:
        return AsyncVectorsResourceWithRawResponse(self._vector_stores.vectors)


class VectorStoresResourceWithStreamingResponse:
    def __init__(self, vector_stores: VectorStoresResource) -> None:
        self._vector_stores = vector_stores

        self.create = to_streamed_response_wrapper(
            vector_stores.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            vector_stores.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            vector_stores.list,
        )
        self.delete = to_streamed_response_wrapper(
            vector_stores.delete,
        )
        self.configure = to_streamed_response_wrapper(
            vector_stores.configure,
        )
        self.count = to_streamed_response_wrapper(
            vector_stores.count,
        )
        self.drop = to_streamed_response_wrapper(
            vector_stores.drop,
        )
        self.query = to_streamed_response_wrapper(
            vector_stores.query,
        )
        self.upsert = to_streamed_response_wrapper(
            vector_stores.upsert,
        )

    @cached_property
    def vectors(self) -> VectorsResourceWithStreamingResponse:
        return VectorsResourceWithStreamingResponse(self._vector_stores.vectors)


class AsyncVectorStoresResourceWithStreamingResponse:
    def __init__(self, vector_stores: AsyncVectorStoresResource) -> None:
        self._vector_stores = vector_stores

        self.create = async_to_streamed_response_wrapper(
            vector_stores.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            vector_stores.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            vector_stores.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            vector_stores.delete,
        )
        self.configure = async_to_streamed_response_wrapper(
            vector_stores.configure,
        )
        self.count = async_to_streamed_response_wrapper(
            vector_stores.count,
        )
        self.drop = async_to_streamed_response_wrapper(
            vector_stores.drop,
        )
        self.query = async_to_streamed_response_wrapper(
            vector_stores.query,
        )
        self.upsert = async_to_streamed_response_wrapper(
            vector_stores.upsert,
        )

    @cached_property
    def vectors(self) -> AsyncVectorsResourceWithStreamingResponse:
        return AsyncVectorsResourceWithStreamingResponse(self._vector_stores.vectors)
