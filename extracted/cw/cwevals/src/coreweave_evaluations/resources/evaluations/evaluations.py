# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal

import httpx

from .rows import (
    RowsResource,
    AsyncRowsResource,
    RowsResourceWithRawResponse,
    AsyncRowsResourceWithRawResponse,
    RowsResourceWithStreamingResponse,
    AsyncRowsResourceWithStreamingResponse,
)
from ...types import evaluation_list_params, evaluation_create_params
from .metrics import (
    MetricsResource,
    AsyncMetricsResource,
    MetricsResourceWithRawResponse,
    AsyncMetricsResourceWithRawResponse,
    MetricsResourceWithStreamingResponse,
    AsyncMetricsResourceWithStreamingResponse,
)
from .scorers import (
    ScorersResource,
    AsyncScorersResource,
    ScorersResourceWithRawResponse,
    AsyncScorersResourceWithRawResponse,
    ScorersResourceWithStreamingResponse,
    AsyncScorersResourceWithStreamingResponse,
)
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
from .queries.queries import (
    QueriesResource,
    AsyncQueriesResource,
    QueriesResourceWithRawResponse,
    AsyncQueriesResourceWithRawResponse,
    QueriesResourceWithStreamingResponse,
    AsyncQueriesResourceWithStreamingResponse,
)
from .versions.versions import (
    VersionsResource,
    AsyncVersionsResource,
    VersionsResourceWithRawResponse,
    AsyncVersionsResourceWithRawResponse,
    VersionsResourceWithStreamingResponse,
    AsyncVersionsResourceWithStreamingResponse,
)
from ...types.evaluation_get_response import EvaluationGetResponse
from ...types.evaluation_list_response import EvaluationListResponse
from ...types.evaluation_create_response import EvaluationCreateResponse

__all__ = ["EvaluationsResource", "AsyncEvaluationsResource"]


class EvaluationsResource(SyncAPIResource):
    @cached_property
    def metrics(self) -> MetricsResource:
        return MetricsResource(self._client)

    @cached_property
    def rows(self) -> RowsResource:
        return RowsResource(self._client)

    @cached_property
    def scorers(self) -> ScorersResource:
        return ScorersResource(self._client)

    @cached_property
    def queries(self) -> QueriesResource:
        return QueriesResource(self._client)

    @cached_property
    def versions(self) -> VersionsResource:
        return VersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EvaluationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return EvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return EvaluationsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        name: str,
        primary_target_kind: Literal["case", "trajectory"],
        source: evaluation_create_params.Source,
        attributes: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> EvaluationCreateResponse:
        """Defines which data and target kind an evaluation uses.

        This operation stores a
        definition. It does not run a model or calculate scores.

        Choose one source:

        - **Fixed:** Set `source.kind` to `fixed` and provide
          `source.dataset_version_id` to evaluate a specific dataset version.
        - **Live:** Set `source.kind` to `live` and provide `source.dataset_id` to
          follow a dataset's current head.

        Provide only the ID for the selected source kind. A source outside the requested
        scope returns 404. Attributes are stored as canonical JSON. An exact retry with
        the same idempotency key returns the original response.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          primary_target_kind: Whether this evaluation reads individual cases or trajectories from its source.

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
        return self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations", namespace=namespace, scope_id=scope_id
            ),
            body=maybe_transform(
                {
                    "name": name,
                    "primary_target_kind": primary_target_kind,
                    "source": source,
                    "attributes": attributes,
                },
                evaluation_create_params.EvaluationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=EvaluationCreateResponse,
        )

    def list(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationListResponse:
        """
        Returns evaluations in creation order, including evaluations created through the
        evaluation table API. A scope with no evaluations returns an empty page.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: Cursor from the previous page's next_cursor. Omit for the first page.

          name: Return only evaluations with exactly this name, including evaluation tables.
              Omit to list all evaluations in the scope.

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
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations", namespace=namespace, scope_id=scope_id
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
                        "name": name,
                    },
                    evaluation_list_params.EvaluationListParams,
                ),
            ),
            cast_to=EvaluationListResponse,
        )

    def get(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGetResponse:
        """
        Returns the immutable evaluation definition in the same form as the create
        response. An evaluation that does not exist or is outside the requested scope
        returns 404.

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
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGetResponse,
        )


class AsyncEvaluationsResource(AsyncAPIResource):
    @cached_property
    def metrics(self) -> AsyncMetricsResource:
        return AsyncMetricsResource(self._client)

    @cached_property
    def rows(self) -> AsyncRowsResource:
        return AsyncRowsResource(self._client)

    @cached_property
    def scorers(self) -> AsyncScorersResource:
        return AsyncScorersResource(self._client)

    @cached_property
    def queries(self) -> AsyncQueriesResource:
        return AsyncQueriesResource(self._client)

    @cached_property
    def versions(self) -> AsyncVersionsResource:
        return AsyncVersionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEvaluationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncEvaluationsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        name: str,
        primary_target_kind: Literal["case", "trajectory"],
        source: evaluation_create_params.Source,
        attributes: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> EvaluationCreateResponse:
        """Defines which data and target kind an evaluation uses.

        This operation stores a
        definition. It does not run a model or calculate scores.

        Choose one source:

        - **Fixed:** Set `source.kind` to `fixed` and provide
          `source.dataset_version_id` to evaluate a specific dataset version.
        - **Live:** Set `source.kind` to `live` and provide `source.dataset_id` to
          follow a dataset's current head.

        Provide only the ID for the selected source kind. A source outside the requested
        scope returns 404. Attributes are stored as canonical JSON. An exact retry with
        the same idempotency key returns the original response.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          primary_target_kind: Whether this evaluation reads individual cases or trajectories from its source.

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
        return await self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations", namespace=namespace, scope_id=scope_id
            ),
            body=await async_maybe_transform(
                {
                    "name": name,
                    "primary_target_kind": primary_target_kind,
                    "source": source,
                    "attributes": attributes,
                },
                evaluation_create_params.EvaluationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=EvaluationCreateResponse,
        )

    async def list(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        cursor: str | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationListResponse:
        """
        Returns evaluations in creation order, including evaluations created through the
        evaluation table API. A scope with no evaluations returns an empty page.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          cursor: Cursor from the previous page's next_cursor. Omit for the first page.

          name: Return only evaluations with exactly this name, including evaluation tables.
              Omit to list all evaluations in the scope.

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
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations", namespace=namespace, scope_id=scope_id
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
                        "name": name,
                    },
                    evaluation_list_params.EvaluationListParams,
                ),
            ),
            cast_to=EvaluationListResponse,
        )

    async def get(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationGetResponse:
        """
        Returns the immutable evaluation definition in the same form as the create
        response. An evaluation that does not exist or is outside the requested scope
        returns 404.

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
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationGetResponse,
        )


class EvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = to_raw_response_wrapper(
            evaluations.create,
        )
        self.list = to_raw_response_wrapper(
            evaluations.list,
        )
        self.get = to_raw_response_wrapper(
            evaluations.get,
        )

    @cached_property
    def metrics(self) -> MetricsResourceWithRawResponse:
        return MetricsResourceWithRawResponse(self._evaluations.metrics)

    @cached_property
    def rows(self) -> RowsResourceWithRawResponse:
        return RowsResourceWithRawResponse(self._evaluations.rows)

    @cached_property
    def scorers(self) -> ScorersResourceWithRawResponse:
        return ScorersResourceWithRawResponse(self._evaluations.scorers)

    @cached_property
    def queries(self) -> QueriesResourceWithRawResponse:
        return QueriesResourceWithRawResponse(self._evaluations.queries)

    @cached_property
    def versions(self) -> VersionsResourceWithRawResponse:
        return VersionsResourceWithRawResponse(self._evaluations.versions)


class AsyncEvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = async_to_raw_response_wrapper(
            evaluations.create,
        )
        self.list = async_to_raw_response_wrapper(
            evaluations.list,
        )
        self.get = async_to_raw_response_wrapper(
            evaluations.get,
        )

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithRawResponse:
        return AsyncMetricsResourceWithRawResponse(self._evaluations.metrics)

    @cached_property
    def rows(self) -> AsyncRowsResourceWithRawResponse:
        return AsyncRowsResourceWithRawResponse(self._evaluations.rows)

    @cached_property
    def scorers(self) -> AsyncScorersResourceWithRawResponse:
        return AsyncScorersResourceWithRawResponse(self._evaluations.scorers)

    @cached_property
    def queries(self) -> AsyncQueriesResourceWithRawResponse:
        return AsyncQueriesResourceWithRawResponse(self._evaluations.queries)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithRawResponse:
        return AsyncVersionsResourceWithRawResponse(self._evaluations.versions)


class EvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = to_streamed_response_wrapper(
            evaluations.create,
        )
        self.list = to_streamed_response_wrapper(
            evaluations.list,
        )
        self.get = to_streamed_response_wrapper(
            evaluations.get,
        )

    @cached_property
    def metrics(self) -> MetricsResourceWithStreamingResponse:
        return MetricsResourceWithStreamingResponse(self._evaluations.metrics)

    @cached_property
    def rows(self) -> RowsResourceWithStreamingResponse:
        return RowsResourceWithStreamingResponse(self._evaluations.rows)

    @cached_property
    def scorers(self) -> ScorersResourceWithStreamingResponse:
        return ScorersResourceWithStreamingResponse(self._evaluations.scorers)

    @cached_property
    def queries(self) -> QueriesResourceWithStreamingResponse:
        return QueriesResourceWithStreamingResponse(self._evaluations.queries)

    @cached_property
    def versions(self) -> VersionsResourceWithStreamingResponse:
        return VersionsResourceWithStreamingResponse(self._evaluations.versions)


class AsyncEvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = async_to_streamed_response_wrapper(
            evaluations.create,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluations.list,
        )
        self.get = async_to_streamed_response_wrapper(
            evaluations.get,
        )

    @cached_property
    def metrics(self) -> AsyncMetricsResourceWithStreamingResponse:
        return AsyncMetricsResourceWithStreamingResponse(self._evaluations.metrics)

    @cached_property
    def rows(self) -> AsyncRowsResourceWithStreamingResponse:
        return AsyncRowsResourceWithStreamingResponse(self._evaluations.rows)

    @cached_property
    def scorers(self) -> AsyncScorersResourceWithStreamingResponse:
        return AsyncScorersResourceWithStreamingResponse(self._evaluations.scorers)

    @cached_property
    def queries(self) -> AsyncQueriesResourceWithStreamingResponse:
        return AsyncQueriesResourceWithStreamingResponse(self._evaluations.queries)

    @cached_property
    def versions(self) -> AsyncVersionsResourceWithStreamingResponse:
        return AsyncVersionsResourceWithStreamingResponse(self._evaluations.versions)
