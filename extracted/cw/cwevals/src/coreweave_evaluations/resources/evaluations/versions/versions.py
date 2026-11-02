# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .metrics import (
    MetricsResource,
    AsyncMetricsResource,
    MetricsResourceWithRawResponse,
    AsyncMetricsResourceWithRawResponse,
    MetricsResourceWithStreamingResponse,
    AsyncMetricsResourceWithStreamingResponse,
)
from .results import (
    ResultsResource,
    AsyncResultsResource,
    ResultsResourceWithRawResponse,
    AsyncResultsResourceWithRawResponse,
    ResultsResourceWithStreamingResponse,
    AsyncResultsResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from .rows.rows import (
    RowsResource,
    AsyncRowsResource,
    RowsResourceWithRawResponse,
    AsyncRowsResourceWithRawResponse,
    RowsResourceWithStreamingResponse,
    AsyncRowsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from .queries.queries import (
    QueriesResource,
    AsyncQueriesResource,
    QueriesResourceWithRawResponse,
    AsyncQueriesResourceWithRawResponse,
    QueriesResourceWithStreamingResponse,
    AsyncQueriesResourceWithStreamingResponse,
)
from ....types.evaluations import version_list_params, version_create_params
from ....types.evaluations.version_get_response import VersionGetResponse
from ....types.evaluations.version_list_response import VersionListResponse
from ....types.evaluations.version_create_response import VersionCreateResponse

__all__ = ["VersionsResource", "AsyncVersionsResource"]


class VersionsResource(SyncAPIResource):
    @cached_property
    def metrics(self) -> MetricsResource:
        return MetricsResource(self._client)

    @cached_property
    def results(self) -> ResultsResource:
        return ResultsResource(self._client)

    @cached_property
    def queries(self) -> QueriesResource:
        return QueriesResource(self._client)

    @cached_property
    def rows(self) -> RowsResource:
        return RowsResource(self._client)

    @cached_property
    def with_raw_response(self) -> VersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return VersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return VersionsResourceWithStreamingResponse(self)

    def create(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        dataset_version_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> VersionCreateResponse:
        """
        Creates an immutable snapshot of one dataset version and the evaluation's
        currently registered scorer versions. The snapshot also records a publication
        cutoff for scores and reported metrics.

        Later writes do not change the frozen results.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          dataset_version_id: Dataset version to freeze in the evaluation snapshot.

              - For a fixed evaluation, omit this field or supply its configured dataset
                version ID.
              - For a live evaluation, supply a dataset version ID, or omit the field to
                publish the dataset's head and use it. Supplying the head's ID also publishes
                it.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/versions",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            body=maybe_transform({"dataset_version_id": dataset_version_id}, version_create_params.VersionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=VersionCreateResponse,
        )

    def list(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VersionListResponse:
        """
        Returns published evaluation versions in publication order, with the same fields
        as the get-version operation. An evaluation that does not exist or is outside
        the requested scope returns 404.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: Cursor from the previous page's next_cursor. Omit for the first page.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/versions",
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
                        "limit": limit,
                    },
                    version_list_params.VersionListParams,
                ),
            ),
            cast_to=VersionListResponse,
        )

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
    ) -> VersionGetResponse:
        """
        Returns the frozen evaluation snapshot exactly as created, including its dataset
        version, selected scorer versions, and publication cutoff.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluation-versions/{evaluation_version_id}",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VersionGetResponse,
        )


class AsyncVersionsResource(AsyncAPIResource):
    @cached_property
    def metrics(self) -> AsyncMetricsResource:
        return AsyncMetricsResource(self._client)

    @cached_property
    def results(self) -> AsyncResultsResource:
        return AsyncResultsResource(self._client)

    @cached_property
    def queries(self) -> AsyncQueriesResource:
        return AsyncQueriesResource(self._client)

    @cached_property
    def rows(self) -> AsyncRowsResource:
        return AsyncRowsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        dataset_version_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> VersionCreateResponse:
        """
        Creates an immutable snapshot of one dataset version and the evaluation's
        currently registered scorer versions. The snapshot also records a publication
        cutoff for scores and reported metrics.

        Later writes do not change the frozen results.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          dataset_version_id: Dataset version to freeze in the evaluation snapshot.

              - For a fixed evaluation, omit this field or supply its configured dataset
                version ID.
              - For a live evaluation, supply a dataset version ID, or omit the field to
                publish the dataset's head and use it. Supplying the head's ID also publishes
                it.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/versions",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            body=await async_maybe_transform(
                {"dataset_version_id": dataset_version_id}, version_create_params.VersionCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=VersionCreateResponse,
        )

    async def list(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> VersionListResponse:
        """
        Returns published evaluation versions in publication order, with the same fields
        as the get-version operation. An evaluation that does not exist or is outside
        the requested scope returns 404.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: Cursor from the previous page's next_cursor. Omit for the first page.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/versions",
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
                        "limit": limit,
                    },
                    version_list_params.VersionListParams,
                ),
            ),
            cast_to=VersionListResponse,
        )

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
    ) -> VersionGetResponse:
        """
        Returns the frozen evaluation snapshot exactly as created, including its dataset
        version, selected scorer versions, and publication cutoff.

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
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluation-versions/{evaluation_version_id}",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_version_id=evaluation_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VersionGetResponse,
        )


class VersionsResourceWithRawResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.create = to_raw_response_wrapper(
            versions.create,
        )
        self.list = to_raw_response_wrapper(
            versions.list,
        )
        self.get = to_raw_response_wrapper(
            versions.get,
        )

    @cached_property
    def metrics(self) -> MetricsResourceWithRawResponse:
        return MetricsResourceWithRawResponse(self._versions.metrics)

    @cached_property
    def results(self) -> ResultsResourceWithRawResponse:
        return ResultsResourceWithRawResponse(self._versions.results)

    @cached_property
    def queries(self) -> QueriesResourceWithRawResponse:
        return QueriesResourceWithRawResponse(self._versions.queries)

    @cached_property
    def rows(self) -> RowsResourceWithRawResponse:
        return RowsResourceWithRawResponse(self._versions.rows)


class AsyncVersionsResourceWithRawResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.create = async_to_raw_response_wrapper(
            versions.create,
        )
        self.list = async_to_raw_response_wrapper(
            versions.list,
        )
        self.get = async_to_raw_response_wrapper(
            versions.get,
        )

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithRawResponse:
        return AsyncMetricsResourceWithRawResponse(self._versions.metrics)

    @cached_property
    def results(self) -> AsyncResultsResourceWithRawResponse:
        return AsyncResultsResourceWithRawResponse(self._versions.results)

    @cached_property
    def queries(self) -> AsyncQueriesResourceWithRawResponse:
        return AsyncQueriesResourceWithRawResponse(self._versions.queries)

    @cached_property
    def rows(self) -> AsyncRowsResourceWithRawResponse:
        return AsyncRowsResourceWithRawResponse(self._versions.rows)


class VersionsResourceWithStreamingResponse:
    def __init__(self, versions: VersionsResource) -> None:
        self._versions = versions

        self.create = to_streamed_response_wrapper(
            versions.create,
        )
        self.list = to_streamed_response_wrapper(
            versions.list,
        )
        self.get = to_streamed_response_wrapper(
            versions.get,
        )

    @cached_property
    def metrics(self) -> MetricsResourceWithStreamingResponse:
        return MetricsResourceWithStreamingResponse(self._versions.metrics)

    @cached_property
    def results(self) -> ResultsResourceWithStreamingResponse:
        return ResultsResourceWithStreamingResponse(self._versions.results)

    @cached_property
    def queries(self) -> QueriesResourceWithStreamingResponse:
        return QueriesResourceWithStreamingResponse(self._versions.queries)

    @cached_property
    def rows(self) -> RowsResourceWithStreamingResponse:
        return RowsResourceWithStreamingResponse(self._versions.rows)


class AsyncVersionsResourceWithStreamingResponse:
    def __init__(self, versions: AsyncVersionsResource) -> None:
        self._versions = versions

        self.create = async_to_streamed_response_wrapper(
            versions.create,
        )
        self.list = async_to_streamed_response_wrapper(
            versions.list,
        )
        self.get = async_to_streamed_response_wrapper(
            versions.get,
        )

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithStreamingResponse:
        return AsyncMetricsResourceWithStreamingResponse(self._versions.metrics)

    @cached_property
    def results(self) -> AsyncResultsResourceWithStreamingResponse:
        return AsyncResultsResourceWithStreamingResponse(self._versions.results)

    @cached_property
    def queries(self) -> AsyncQueriesResourceWithStreamingResponse:
        return AsyncQueriesResourceWithStreamingResponse(self._versions.queries)

    @cached_property
    def rows(self) -> AsyncRowsResourceWithStreamingResponse:
        return AsyncRowsResourceWithStreamingResponse(self._versions.rows)
