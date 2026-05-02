# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.knowledge_bases import data_source_connection_delete_params
from ...types.knowledge_bases.delete_knowledge_base_data_source_connection_response import (
    DeleteKnowledgeBaseDataSourceConnectionResponse,
)

__all__ = ["DataSourceConnectionsResource", "AsyncDataSourceConnectionsResource"]


class DataSourceConnectionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DataSourceConnectionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return DataSourceConnectionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DataSourceConnectionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return DataSourceConnectionsResourceWithStreamingResponse(self)

    def delete(
        self,
        knowledge_base_data_source_id: str,
        *,
        knowledge_base_id: str,
        dry_run: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteKnowledgeBaseDataSourceConnectionResponse:
        """
        Delete Knowledge Base Data Source Connection

        Args:
          dry_run: Dryrun query parameter to determine first how many things will be deleted

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not knowledge_base_data_source_id:
            raise ValueError(
                f"Expected a non-empty value for `knowledge_base_data_source_id` but received {knowledge_base_data_source_id!r}"
            )
        return self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/data-source-connections/{knowledge_base_data_source_id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"dry_run": dry_run}, data_source_connection_delete_params.DataSourceConnectionDeleteParams
                ),
            ),
            cast_to=DeleteKnowledgeBaseDataSourceConnectionResponse,
        )


class AsyncDataSourceConnectionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDataSourceConnectionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDataSourceConnectionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDataSourceConnectionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncDataSourceConnectionsResourceWithStreamingResponse(self)

    async def delete(
        self,
        knowledge_base_data_source_id: str,
        *,
        knowledge_base_id: str,
        dry_run: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DeleteKnowledgeBaseDataSourceConnectionResponse:
        """
        Delete Knowledge Base Data Source Connection

        Args:
          dry_run: Dryrun query parameter to determine first how many things will be deleted

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not knowledge_base_id:
            raise ValueError(f"Expected a non-empty value for `knowledge_base_id` but received {knowledge_base_id!r}")
        if not knowledge_base_data_source_id:
            raise ValueError(
                f"Expected a non-empty value for `knowledge_base_data_source_id` but received {knowledge_base_data_source_id!r}"
            )
        return await self._post(
            f"/v4/knowledge-bases/{knowledge_base_id}/data-source-connections/{knowledge_base_data_source_id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"dry_run": dry_run}, data_source_connection_delete_params.DataSourceConnectionDeleteParams
                ),
            ),
            cast_to=DeleteKnowledgeBaseDataSourceConnectionResponse,
        )


class DataSourceConnectionsResourceWithRawResponse:
    def __init__(self, data_source_connections: DataSourceConnectionsResource) -> None:
        self._data_source_connections = data_source_connections

        self.delete = to_raw_response_wrapper(
            data_source_connections.delete,
        )


class AsyncDataSourceConnectionsResourceWithRawResponse:
    def __init__(self, data_source_connections: AsyncDataSourceConnectionsResource) -> None:
        self._data_source_connections = data_source_connections

        self.delete = async_to_raw_response_wrapper(
            data_source_connections.delete,
        )


class DataSourceConnectionsResourceWithStreamingResponse:
    def __init__(self, data_source_connections: DataSourceConnectionsResource) -> None:
        self._data_source_connections = data_source_connections

        self.delete = to_streamed_response_wrapper(
            data_source_connections.delete,
        )


class AsyncDataSourceConnectionsResourceWithStreamingResponse:
    def __init__(self, data_source_connections: AsyncDataSourceConnectionsResource) -> None:
        self._data_source_connections = data_source_connections

        self.delete = async_to_streamed_response_wrapper(
            data_source_connections.delete,
        )
