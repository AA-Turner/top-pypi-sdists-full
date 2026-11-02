# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import Body, Query, Headers, NotGiven, not_given
from ...._utils import path_template
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.eval_tables.versions.column_get_response import ColumnGetResponse

__all__ = ["ColumnsResource", "AsyncColumnsResource"]


class ColumnsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ColumnsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return ColumnsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ColumnsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return ColumnsResourceWithStreamingResponse(self)

    def get(
        self,
        evaluation_version_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ColumnGetResponse:
        """
        Returns the input, output, and score columns selected by the frozen evaluation
        table version.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/eval-table-versions/{evaluation_version_id}/columns",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ColumnGetResponse,
        )


class AsyncColumnsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncColumnsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncColumnsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncColumnsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncColumnsResourceWithStreamingResponse(self)

    async def get(
        self,
        evaluation_version_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ColumnGetResponse:
        """
        Returns the input, output, and score columns selected by the frozen evaluation
        table version.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/eval-table-versions/{evaluation_version_id}/columns",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ColumnGetResponse,
        )


class ColumnsResourceWithRawResponse:
    def __init__(self, columns: ColumnsResource) -> None:
        self._columns = columns

        self.get = to_raw_response_wrapper(
            columns.get,
        )


class AsyncColumnsResourceWithRawResponse:
    def __init__(self, columns: AsyncColumnsResource) -> None:
        self._columns = columns

        self.get = async_to_raw_response_wrapper(
            columns.get,
        )


class ColumnsResourceWithStreamingResponse:
    def __init__(self, columns: ColumnsResource) -> None:
        self._columns = columns

        self.get = to_streamed_response_wrapper(
            columns.get,
        )


class AsyncColumnsResourceWithStreamingResponse:
    def __init__(self, columns: AsyncColumnsResource) -> None:
        self._columns = columns

        self.get = async_to_streamed_response_wrapper(
            columns.get,
        )
