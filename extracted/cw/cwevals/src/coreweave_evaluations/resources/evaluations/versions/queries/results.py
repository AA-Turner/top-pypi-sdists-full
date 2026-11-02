# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ....._utils import path_template, maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.evaluations.versions.queries import result_list_params
from .....types.evaluations.versions.queries.result_list_response import ResultListResponse

__all__ = ["ResultsResource", "AsyncResultsResource"]


class ResultsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ResultsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return ResultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResultsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return ResultsResourceWithStreamingResponse(self)

    def list(
        self,
        evaluation_query_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        evaluation_version_id: str,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResultListResponse:
        """
        Runs one of the evaluation's saved aggregation queries against the data and
        scores captured in this evaluation version.

        **Version compatibility**

        Returns 400 if the dataset snapshot lacks a grouping field, or if the evaluation
        version does not select a scorer used by a metric or score grouping.

        **Grouping and ordering**

        - Rows sort by the `group_by` columns in order, ascending, with nulls last.
        - A missing grouping value and an explicit null belong to the same group.
        - Without grouping, the response has one row with an empty `group` array, even
          for an empty dataset.
        - With grouping, an empty dataset returns no rows.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: The previous response's next_cursor value. Omit for the first page.

          limit: Maximum number of results to return in one page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        if scope_id is None:
            scope_id = self._client._get_scope_id_path_param()
        if not scope_id:
            raise ValueError(f"Expected a non-empty value for `scope_id` but received {scope_id!r}")
        if not evaluation_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_version_id` but received {evaluation_version_id!r}"
            )
        if not evaluation_query_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_query_id` but received {evaluation_query_id!r}"
            )
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluation-versions/{evaluation_version_id}/queries/{evaluation_query_id}/results",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
                evaluation_query_id=evaluation_query_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    result_list_params.ResultListParams,
                ),
            ),
            cast_to=ResultListResponse,
        )


class AsyncResultsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResultsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncResultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResultsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncResultsResourceWithStreamingResponse(self)

    async def list(
        self,
        evaluation_query_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        evaluation_version_id: str,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ResultListResponse:
        """
        Runs one of the evaluation's saved aggregation queries against the data and
        scores captured in this evaluation version.

        **Version compatibility**

        Returns 400 if the dataset snapshot lacks a grouping field, or if the evaluation
        version does not select a scorer used by a metric or score grouping.

        **Grouping and ordering**

        - Rows sort by the `group_by` columns in order, ascending, with nulls last.
        - A missing grouping value and an explicit null belong to the same group.
        - Without grouping, the response has one row with an empty `group` array, even
          for an empty dataset.
        - With grouping, an empty dataset returns no rows.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: The previous response's next_cursor value. Omit for the first page.

          limit: Maximum number of results to return in one page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if namespace is None:
            namespace = self._client._get_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        if scope_id is None:
            scope_id = self._client._get_scope_id_path_param()
        if not scope_id:
            raise ValueError(f"Expected a non-empty value for `scope_id` but received {scope_id!r}")
        if not evaluation_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_version_id` but received {evaluation_version_id!r}"
            )
        if not evaluation_query_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_query_id` but received {evaluation_query_id!r}"
            )
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluation-versions/{evaluation_version_id}/queries/{evaluation_query_id}/results",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
                evaluation_query_id=evaluation_query_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "limit": limit,
                    },
                    result_list_params.ResultListParams,
                ),
            ),
            cast_to=ResultListResponse,
        )


class ResultsResourceWithRawResponse:
    def __init__(self, results: ResultsResource) -> None:
        self._results = results

        self.list = to_raw_response_wrapper(
            results.list,
        )


class AsyncResultsResourceWithRawResponse:
    def __init__(self, results: AsyncResultsResource) -> None:
        self._results = results

        self.list = async_to_raw_response_wrapper(
            results.list,
        )


class ResultsResourceWithStreamingResponse:
    def __init__(self, results: ResultsResource) -> None:
        self._results = results

        self.list = to_streamed_response_wrapper(
            results.list,
        )


class AsyncResultsResourceWithStreamingResponse:
    def __init__(self, results: AsyncResultsResource) -> None:
        self._results = results

        self.list = async_to_streamed_response_wrapper(
            results.list,
        )
