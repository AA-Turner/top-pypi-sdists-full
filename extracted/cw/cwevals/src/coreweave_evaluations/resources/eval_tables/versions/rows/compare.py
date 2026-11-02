# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ....._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
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
from .....types.eval_tables.versions.rows import compare_list_params, compare_search_params
from .....types.eval_tables.versions.rows.compare_list_response import CompareListResponse
from .....types.eval_tables.versions.rows.compare_search_response import CompareSearchResponse

__all__ = ["CompareResource", "AsyncCompareResource"]


class CompareResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompareResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return CompareResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompareResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return CompareResourceWithStreamingResponse(self)

    def list(
        self,
        evaluation_version_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        compare_to: Optional[SequenceNotStr[str]],
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
    ) -> CompareListResponse:
        """
        Matches the reference version's rows with each compared version's rows by
        example key, and pages through the union. A case logged without an example key
        but with an input matches by the key derived from that input when it was
        appended as an eval table row or written with `example_key_fields`. Any other
        case without an example key matches only itself, in versions that read its
        dataset. The k-th copy of an example key in one version matches the k-th copy in
        another. Each version reads its cases and selected scores at its own cutoff. A
        row written before the service hashed example keys matches no other row.

        `filter` uses the rows operations' columns, without a version qualifier. Each
        version's row is tested on its own, and a row is kept, with every version's
        values, when any version's row passes. A version without a filter column reads
        as null in it.

        `order_by` names one column of one compared version, as in
        `v."<evaluation_version_id>".s.accuracy desc` or
        `v."<evaluation_version_id>".example_key`. Rows without that version sort last.
        Without `order_by`, rows follow the reference's order, then each later version's
        rows that earlier versions lack. Filtering and ordering apply before pagination,
        and every page reports the total.

        The encoded request target (path and query string) must be at most 8000 bytes.
        Larger requests return 414 URI Too Long with error code `request_uri_too_long`.
        Retry the same parameters through the corresponding POST `/rows/compare/search`
        operation.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          compare_to: Comma-separated EvaluationVersion IDs to compare with the reference, in result
              order.

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
        if not evaluation_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_version_id` but received {evaluation_version_id!r}"
            )
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/eval-table-versions/{evaluation_version_id}/rows/compare",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "compare_to": compare_to,
                        "cursor": cursor,
                        "filter": filter,
                        "limit": limit,
                        "order_by": order_by,
                    },
                    compare_list_params.CompareListParams,
                ),
            ),
            cast_to=CompareListResponse,
        )

    def search(
        self,
        evaluation_version_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        compare_to: SequenceNotStr[str],
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
    ) -> CompareSearchResponse:
        """
        Returns the same comparison as compare-eval-table-version-rows, with the
        parameters supplied in a JSON body. Use this operation when the parameters are
        too large for a URL.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          compare_to: EvaluationVersion IDs to compare with the reference, in result order.

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
        if not evaluation_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_version_id` but received {evaluation_version_id!r}"
            )
        return self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/eval-table-versions/{evaluation_version_id}/rows/compare/search",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
            ),
            body=maybe_transform(
                {
                    "compare_to": compare_to,
                    "cursor": cursor,
                    "filter": filter,
                    "limit": limit,
                    "order_by": order_by,
                },
                compare_search_params.CompareSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CompareSearchResponse,
        )


class AsyncCompareResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompareResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncCompareResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompareResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncCompareResourceWithStreamingResponse(self)

    async def list(
        self,
        evaluation_version_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        compare_to: Optional[SequenceNotStr[str]],
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
    ) -> CompareListResponse:
        """
        Matches the reference version's rows with each compared version's rows by
        example key, and pages through the union. A case logged without an example key
        but with an input matches by the key derived from that input when it was
        appended as an eval table row or written with `example_key_fields`. Any other
        case without an example key matches only itself, in versions that read its
        dataset. The k-th copy of an example key in one version matches the k-th copy in
        another. Each version reads its cases and selected scores at its own cutoff. A
        row written before the service hashed example keys matches no other row.

        `filter` uses the rows operations' columns, without a version qualifier. Each
        version's row is tested on its own, and a row is kept, with every version's
        values, when any version's row passes. A version without a filter column reads
        as null in it.

        `order_by` names one column of one compared version, as in
        `v."<evaluation_version_id>".s.accuracy desc` or
        `v."<evaluation_version_id>".example_key`. Rows without that version sort last.
        Without `order_by`, rows follow the reference's order, then each later version's
        rows that earlier versions lack. Filtering and ordering apply before pagination,
        and every page reports the total.

        The encoded request target (path and query string) must be at most 8000 bytes.
        Larger requests return 414 URI Too Long with error code `request_uri_too_long`.
        Retry the same parameters through the corresponding POST `/rows/compare/search`
        operation.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          compare_to: Comma-separated EvaluationVersion IDs to compare with the reference, in result
              order.

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
        if not evaluation_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_version_id` but received {evaluation_version_id!r}"
            )
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/eval-table-versions/{evaluation_version_id}/rows/compare",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "compare_to": compare_to,
                        "cursor": cursor,
                        "filter": filter,
                        "limit": limit,
                        "order_by": order_by,
                    },
                    compare_list_params.CompareListParams,
                ),
            ),
            cast_to=CompareListResponse,
        )

    async def search(
        self,
        evaluation_version_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        compare_to: SequenceNotStr[str],
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
    ) -> CompareSearchResponse:
        """
        Returns the same comparison as compare-eval-table-version-rows, with the
        parameters supplied in a JSON body. Use this operation when the parameters are
        too large for a URL.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          compare_to: EvaluationVersion IDs to compare with the reference, in result order.

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
        if not evaluation_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_version_id` but received {evaluation_version_id!r}"
            )
        return await self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/eval-table-versions/{evaluation_version_id}/rows/compare/search",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
            ),
            body=await async_maybe_transform(
                {
                    "compare_to": compare_to,
                    "cursor": cursor,
                    "filter": filter,
                    "limit": limit,
                    "order_by": order_by,
                },
                compare_search_params.CompareSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CompareSearchResponse,
        )


class CompareResourceWithRawResponse:
    def __init__(self, compare: CompareResource) -> None:
        self._compare = compare

        self.list = to_raw_response_wrapper(
            compare.list,
        )
        self.search = to_raw_response_wrapper(
            compare.search,
        )


class AsyncCompareResourceWithRawResponse:
    def __init__(self, compare: AsyncCompareResource) -> None:
        self._compare = compare

        self.list = async_to_raw_response_wrapper(
            compare.list,
        )
        self.search = async_to_raw_response_wrapper(
            compare.search,
        )


class CompareResourceWithStreamingResponse:
    def __init__(self, compare: CompareResource) -> None:
        self._compare = compare

        self.list = to_streamed_response_wrapper(
            compare.list,
        )
        self.search = to_streamed_response_wrapper(
            compare.search,
        )


class AsyncCompareResourceWithStreamingResponse:
    def __init__(self, compare: AsyncCompareResource) -> None:
        self._compare = compare

        self.list = async_to_streamed_response_wrapper(
            compare.list,
        )
        self.search = async_to_streamed_response_wrapper(
            compare.search,
        )
