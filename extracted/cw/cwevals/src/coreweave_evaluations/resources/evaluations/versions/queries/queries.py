# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .results import (
    ResultsResource,
    AsyncResultsResource,
    ResultsResourceWithRawResponse,
    AsyncResultsResourceWithRawResponse,
    ResultsResourceWithStreamingResponse,
    AsyncResultsResourceWithStreamingResponse,
)
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["QueriesResource", "AsyncQueriesResource"]


class QueriesResource(SyncAPIResource):
    @cached_property
    def results(self) -> ResultsResource:
        return ResultsResource(self._client)

    @cached_property
    def with_raw_response(self) -> QueriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return QueriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QueriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return QueriesResourceWithStreamingResponse(self)


class AsyncQueriesResource(AsyncAPIResource):
    @cached_property
    def results(self) -> AsyncResultsResource:
        return AsyncResultsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncQueriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncQueriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQueriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncQueriesResourceWithStreamingResponse(self)


class QueriesResourceWithRawResponse:
    def __init__(self, queries: QueriesResource) -> None:
        self._queries = queries

    @cached_property
    def results(self) -> ResultsResourceWithRawResponse:
        return ResultsResourceWithRawResponse(self._queries.results)


class AsyncQueriesResourceWithRawResponse:
    def __init__(self, queries: AsyncQueriesResource) -> None:
        self._queries = queries

    @cached_property
    def results(self) -> AsyncResultsResourceWithRawResponse:
        return AsyncResultsResourceWithRawResponse(self._queries.results)


class QueriesResourceWithStreamingResponse:
    def __init__(self, queries: QueriesResource) -> None:
        self._queries = queries

    @cached_property
    def results(self) -> ResultsResourceWithStreamingResponse:
        return ResultsResourceWithStreamingResponse(self._queries.results)


class AsyncQueriesResourceWithStreamingResponse:
    def __init__(self, queries: AsyncQueriesResource) -> None:
        self._queries = queries

    @cached_property
    def results(self) -> AsyncResultsResourceWithStreamingResponse:
        return AsyncResultsResourceWithStreamingResponse(self._queries.results)
