# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from .cases import (
    CasesResource,
    AsyncCasesResource,
    CasesResourceWithRawResponse,
    AsyncCasesResourceWithRawResponse,
    CasesResourceWithStreamingResponse,
    AsyncCasesResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.datasets import trajectory_list_params, trajectory_create_params
from ....types.datasets.trajectory_get_response import TrajectoryGetResponse
from ....types.datasets.trajectory_list_response import TrajectoryListResponse
from ....types.datasets.trajectory_create_response import TrajectoryCreateResponse

__all__ = ["TrajectoriesResource", "AsyncTrajectoriesResource"]


class TrajectoriesResource(SyncAPIResource):
    @cached_property
    def cases(self) -> CasesResource:
        return CasesResource(self._client)

    @cached_property
    def with_raw_response(self) -> TrajectoriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return TrajectoriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TrajectoriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return TrajectoriesResourceWithStreamingResponse(self)

    def create(
        self,
        dataset_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        trajectories: Iterable[trajectory_create_params.Trajectory],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> TrajectoryCreateResponse:
        """Creates trajectories, each a run of the dataset's cases that follows a root
        case.

        Add cases to a trajectory with create-cases. A trajectory that names a
        parent_trajectory_id must start from one of the parent's cases, and it is nested
        one level below the parent.

        Request bodies must be smaller than 16 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

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
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/datasets/{dataset_id}/trajectories",
                namespace=namespace,
                scope_id=scope_id,
                dataset_id=dataset_id,
            ),
            body=maybe_transform({"trajectories": trajectories}, trajectory_create_params.TrajectoryCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TrajectoryCreateResponse,
        )

    def list(
        self,
        dataset_id: str,
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
    ) -> TrajectoryListResponse:
        """
        Returns the dataset's published trajectories in the order they were created.

        Pass the returned `next_cursor` as `cursor` to read the next page. The last page
        has no `next_cursor`.

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
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/datasets/{dataset_id}/trajectories",
                namespace=namespace,
                scope_id=scope_id,
                dataset_id=dataset_id,
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
                    trajectory_list_params.TrajectoryListParams,
                ),
            ),
            cast_to=TrajectoryListResponse,
        )

    def get(
        self,
        trajectory_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrajectoryGetResponse:
        """
        Returns one published trajectory, including its dataset, its root case, and the
        commit that published it.

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
        if not trajectory_id:
            raise ValueError(f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}")
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/trajectories/{trajectory_id}",
                namespace=namespace,
                scope_id=scope_id,
                trajectory_id=trajectory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrajectoryGetResponse,
        )


class AsyncTrajectoriesResource(AsyncAPIResource):
    @cached_property
    def cases(self) -> AsyncCasesResource:
        return AsyncCasesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTrajectoriesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncTrajectoriesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTrajectoriesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncTrajectoriesResourceWithStreamingResponse(self)

    async def create(
        self,
        dataset_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        trajectories: Iterable[trajectory_create_params.Trajectory],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> TrajectoryCreateResponse:
        """Creates trajectories, each a run of the dataset's cases that follows a root
        case.

        Add cases to a trajectory with create-cases. A trajectory that names a
        parent_trajectory_id must start from one of the parent's cases, and it is nested
        one level below the parent.

        Request bodies must be smaller than 16 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

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
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return await self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/datasets/{dataset_id}/trajectories",
                namespace=namespace,
                scope_id=scope_id,
                dataset_id=dataset_id,
            ),
            body=await async_maybe_transform(
                {"trajectories": trajectories}, trajectory_create_params.TrajectoryCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=TrajectoryCreateResponse,
        )

    async def list(
        self,
        dataset_id: str,
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
    ) -> TrajectoryListResponse:
        """
        Returns the dataset's published trajectories in the order they were created.

        Pass the returned `next_cursor` as `cursor` to read the next page. The last page
        has no `next_cursor`.

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
        if not dataset_id:
            raise ValueError(f"Expected a non-empty value for `dataset_id` but received {dataset_id!r}")
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/datasets/{dataset_id}/trajectories",
                namespace=namespace,
                scope_id=scope_id,
                dataset_id=dataset_id,
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
                    trajectory_list_params.TrajectoryListParams,
                ),
            ),
            cast_to=TrajectoryListResponse,
        )

    async def get(
        self,
        trajectory_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TrajectoryGetResponse:
        """
        Returns one published trajectory, including its dataset, its root case, and the
        commit that published it.

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
        if not trajectory_id:
            raise ValueError(f"Expected a non-empty value for `trajectory_id` but received {trajectory_id!r}")
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/trajectories/{trajectory_id}",
                namespace=namespace,
                scope_id=scope_id,
                trajectory_id=trajectory_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TrajectoryGetResponse,
        )


class TrajectoriesResourceWithRawResponse:
    def __init__(self, trajectories: TrajectoriesResource) -> None:
        self._trajectories = trajectories

        self.create = to_raw_response_wrapper(
            trajectories.create,
        )
        self.list = to_raw_response_wrapper(
            trajectories.list,
        )
        self.get = to_raw_response_wrapper(
            trajectories.get,
        )

    @cached_property
    def cases(self) -> CasesResourceWithRawResponse:
        return CasesResourceWithRawResponse(self._trajectories.cases)


class AsyncTrajectoriesResourceWithRawResponse:
    def __init__(self, trajectories: AsyncTrajectoriesResource) -> None:
        self._trajectories = trajectories

        self.create = async_to_raw_response_wrapper(
            trajectories.create,
        )
        self.list = async_to_raw_response_wrapper(
            trajectories.list,
        )
        self.get = async_to_raw_response_wrapper(
            trajectories.get,
        )

    @cached_property
    def cases(self) -> AsyncCasesResourceWithRawResponse:
        return AsyncCasesResourceWithRawResponse(self._trajectories.cases)


class TrajectoriesResourceWithStreamingResponse:
    def __init__(self, trajectories: TrajectoriesResource) -> None:
        self._trajectories = trajectories

        self.create = to_streamed_response_wrapper(
            trajectories.create,
        )
        self.list = to_streamed_response_wrapper(
            trajectories.list,
        )
        self.get = to_streamed_response_wrapper(
            trajectories.get,
        )

    @cached_property
    def cases(self) -> CasesResourceWithStreamingResponse:
        return CasesResourceWithStreamingResponse(self._trajectories.cases)


class AsyncTrajectoriesResourceWithStreamingResponse:
    def __init__(self, trajectories: AsyncTrajectoriesResource) -> None:
        self._trajectories = trajectories

        self.create = async_to_streamed_response_wrapper(
            trajectories.create,
        )
        self.list = async_to_streamed_response_wrapper(
            trajectories.list,
        )
        self.get = async_to_streamed_response_wrapper(
            trajectories.get,
        )

    @cached_property
    def cases(self) -> AsyncCasesResourceWithStreamingResponse:
        return AsyncCasesResourceWithStreamingResponse(self._trajectories.cases)
