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
from ..._base_client import make_request_options
from ...types.evaluations import row_list_params, row_search_params
from ...types.evaluations.row_list_response import RowListResponse
from ...types.evaluations.row_search_response import RowSearchResponse

__all__ = ["RowsResource", "AsyncRowsResource"]


class RowsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RowsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return RowsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RowsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return RowsResourceWithStreamingResponse(self)

    def list(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cursor: str | Omit = omit,
        filter: str | Omit = omit,
        limit: int | Omit = omit,
        order_by: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RowListResponse:
        """
        Reads the Evaluation's latest data without cutting an EvaluationVersion: the
        registered Scorers and every Score published so far, over the fixed
        DatasetVersion's Cases or every Case published to a live Evaluation's Dataset
        head. The first page pins that data, and later pages read the same Cases and
        Scores. If the Evaluation's Scorer selection changes between pages, such as when
        a new Score column appears, a continuation returns 400 and the read must start
        again without a cursor. `filter` and `order_by` use the same syntax as
        list-evaluation-version-rows.

        The encoded request target (path and query string) must be at most 8000 bytes.
        Larger requests return 414 URI Too Long with error code `request_uri_too_long`.
        Retry the same parameters through the corresponding POST `/rows/search`
        operation.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: The previous response's next_cursor value. Omit for the first page.

          filter: Selects rows using column comparisons joined with AND, OR, and NOT. Parentheses
              group expressions. NOT and - bind tighter than AND and OR, and mixing AND and OR
              at one level needs parentheses. Parentheses nest at most 32 deep.

              For string comparisons with = or !=, use these patterns:

                  *    matches zero or more characters

              - matches a literal asterisk \\ matches a literal backslash

              A filter can contain at most 100 predicates and 65,536 bytes of normalized JSON
              literals in total.

              Example for an evaluation with an accuracy score column:

                  variant = "model-a" AND s.accuracy >= 0.8

          limit: Maximum number of results to return in one page.

          order_by: Column to sort by, optionally followed by desc for descending order. Without
              desc, sorting is ascending. Omit to use the operation's standard order.

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
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/rows",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cursor": cursor,
                        "filter": filter,
                        "limit": limit,
                        "order_by": order_by,
                    },
                    row_list_params.RowListParams,
                ),
            ),
            cast_to=RowListResponse,
        )

    def search(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cursor: str | Omit = omit,
        filter: str | Omit = omit,
        limit: int | Omit = omit,
        order_by: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> RowSearchResponse:
        """Reads the same latest data as list-evaluation-rows.

        `filter` and `order_by` use
        the same AIP-style syntax as the GET route. Filtering and ordering apply before
        pagination.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: The previous response's next_cursor value. Omit for the first page.

          filter: Selects rows using column comparisons joined with AND, OR, and NOT. Parentheses
              group expressions. NOT and - bind tighter than AND and OR, and mixing AND and OR
              at one level needs parentheses. Parentheses nest at most 32 deep.

              For string comparisons with = or !=, use these patterns:

                  *    matches zero or more characters

              - matches a literal asterisk \\ matches a literal backslash

              A filter can contain at most 100 predicates and 65,536 bytes of normalized JSON
              literals in total.

              Example for an evaluation with an accuracy score column:

                  variant = "model-a" AND s.accuracy >= 0.8

          limit: Maximum number of results to return in one page.

          order_by: Column to sort by, optionally followed by desc for descending order. Without
              desc, sorting is ascending. Omit to use the operation's standard order.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if namespace is None:
            namespace = self._client._get_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        if scope_id is None:
            scope_id = self._client._get_scope_id_path_param()
        if not scope_id:
            raise ValueError(f"Expected a non-empty value for `scope_id` but received {scope_id!r}")
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/rows/search",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            body=maybe_transform(
                {
                    "cursor": cursor,
                    "filter": filter,
                    "limit": limit,
                    "order_by": order_by,
                },
                row_search_params.RowSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=RowSearchResponse,
        )


class AsyncRowsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRowsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncRowsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRowsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncRowsResourceWithStreamingResponse(self)

    async def list(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cursor: str | Omit = omit,
        filter: str | Omit = omit,
        limit: int | Omit = omit,
        order_by: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RowListResponse:
        """
        Reads the Evaluation's latest data without cutting an EvaluationVersion: the
        registered Scorers and every Score published so far, over the fixed
        DatasetVersion's Cases or every Case published to a live Evaluation's Dataset
        head. The first page pins that data, and later pages read the same Cases and
        Scores. If the Evaluation's Scorer selection changes between pages, such as when
        a new Score column appears, a continuation returns 400 and the read must start
        again without a cursor. `filter` and `order_by` use the same syntax as
        list-evaluation-version-rows.

        The encoded request target (path and query string) must be at most 8000 bytes.
        Larger requests return 414 URI Too Long with error code `request_uri_too_long`.
        Retry the same parameters through the corresponding POST `/rows/search`
        operation.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: The previous response's next_cursor value. Omit for the first page.

          filter: Selects rows using column comparisons joined with AND, OR, and NOT. Parentheses
              group expressions. NOT and - bind tighter than AND and OR, and mixing AND and OR
              at one level needs parentheses. Parentheses nest at most 32 deep.

              For string comparisons with = or !=, use these patterns:

                  *    matches zero or more characters

              - matches a literal asterisk \\ matches a literal backslash

              A filter can contain at most 100 predicates and 65,536 bytes of normalized JSON
              literals in total.

              Example for an evaluation with an accuracy score column:

                  variant = "model-a" AND s.accuracy >= 0.8

          limit: Maximum number of results to return in one page.

          order_by: Column to sort by, optionally followed by desc for descending order. Without
              desc, sorting is ascending. Omit to use the operation's standard order.

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
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/rows",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cursor": cursor,
                        "filter": filter,
                        "limit": limit,
                        "order_by": order_by,
                    },
                    row_list_params.RowListParams,
                ),
            ),
            cast_to=RowListResponse,
        )

    async def search(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cursor: str | Omit = omit,
        filter: str | Omit = omit,
        limit: int | Omit = omit,
        order_by: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> RowSearchResponse:
        """Reads the same latest data as list-evaluation-rows.

        `filter` and `order_by` use
        the same AIP-style syntax as the GET route. Filtering and ordering apply before
        pagination.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: The previous response's next_cursor value. Omit for the first page.

          filter: Selects rows using column comparisons joined with AND, OR, and NOT. Parentheses
              group expressions. NOT and - bind tighter than AND and OR, and mixing AND and OR
              at one level needs parentheses. Parentheses nest at most 32 deep.

              For string comparisons with = or !=, use these patterns:

                  *    matches zero or more characters

              - matches a literal asterisk \\ matches a literal backslash

              A filter can contain at most 100 predicates and 65,536 bytes of normalized JSON
              literals in total.

              Example for an evaluation with an accuracy score column:

                  variant = "model-a" AND s.accuracy >= 0.8

          limit: Maximum number of results to return in one page.

          order_by: Column to sort by, optionally followed by desc for descending order. Without
              desc, sorting is ascending. Omit to use the operation's standard order.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if namespace is None:
            namespace = self._client._get_namespace_path_param()
        if not namespace:
            raise ValueError(f"Expected a non-empty value for `namespace` but received {namespace!r}")
        if scope_id is None:
            scope_id = self._client._get_scope_id_path_param()
        if not scope_id:
            raise ValueError(f"Expected a non-empty value for `scope_id` but received {scope_id!r}")
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/rows/search",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            body=await async_maybe_transform(
                {
                    "cursor": cursor,
                    "filter": filter,
                    "limit": limit,
                    "order_by": order_by,
                },
                row_search_params.RowSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=RowSearchResponse,
        )


class RowsResourceWithRawResponse:
    def __init__(self, rows: RowsResource) -> None:
        self._rows = rows

        self.list = to_raw_response_wrapper(
            rows.list,
        )
        self.search = to_raw_response_wrapper(
            rows.search,
        )


class AsyncRowsResourceWithRawResponse:
    def __init__(self, rows: AsyncRowsResource) -> None:
        self._rows = rows

        self.list = async_to_raw_response_wrapper(
            rows.list,
        )
        self.search = async_to_raw_response_wrapper(
            rows.search,
        )


class RowsResourceWithStreamingResponse:
    def __init__(self, rows: RowsResource) -> None:
        self._rows = rows

        self.list = to_streamed_response_wrapper(
            rows.list,
        )
        self.search = to_streamed_response_wrapper(
            rows.search,
        )


class AsyncRowsResourceWithStreamingResponse:
    def __init__(self, rows: AsyncRowsResource) -> None:
        self._rows = rows

        self.list = async_to_streamed_response_wrapper(
            rows.list,
        )
        self.search = async_to_streamed_response_wrapper(
            rows.search,
        )
