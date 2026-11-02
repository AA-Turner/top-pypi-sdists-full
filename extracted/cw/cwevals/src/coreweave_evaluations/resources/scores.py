# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..types import score_create_params
from .._types import Body, Query, Headers, NotGiven, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.score_get_response import ScoreGetResponse
from ..types.score_create_response import ScoreCreateResponse

__all__ = ["ScoresResource", "AsyncScoresResource"]


class ScoresResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ScoresResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return ScoresResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ScoresResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return ScoresResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        scores: Iterable[score_create_params.Score],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScoreCreateResponse:
        """
        Stores score values that your application has calculated for existing targets.

        - Each value must match the referenced scorer version's `value_type`.
        - Each target must already be published and have a kind allowed by that scorer
          version.
        - The response includes `publish_operation_id`, `commit_id`, and `score_ids`.
          Score IDs follow request order.

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
        return self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/scores", namespace=namespace, scope_id=scope_id
            ),
            body=maybe_transform({"scores": scores}, score_create_params.ScoreCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScoreCreateResponse,
        )

    def get(
        self,
        score_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScoreGetResponse:
        """Returns one score published in the requested scope.

        `value` contains the stored
        value as JSON. `value_type` distinguishes an integer score from a number score.

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
        if not score_id:
            raise ValueError(f"Expected a non-empty value for `score_id` but received {score_id!r}")
        return self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/scores/{score_id}",
                namespace=namespace,
                scope_id=scope_id,
                score_id=score_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScoreGetResponse,
        )


class AsyncScoresResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncScoresResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncScoresResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncScoresResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncScoresResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        scores: Iterable[score_create_params.Score],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScoreCreateResponse:
        """
        Stores score values that your application has calculated for existing targets.

        - Each value must match the referenced scorer version's `value_type`.
        - Each target must already be published and have a kind allowed by that scorer
          version.
        - The response includes `publish_operation_id`, `commit_id`, and `score_ids`.
          Score IDs follow request order.

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
        return await self._post(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/scores", namespace=namespace, scope_id=scope_id
            ),
            body=await async_maybe_transform({"scores": scores}, score_create_params.ScoreCreateParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScoreCreateResponse,
        )

    async def get(
        self,
        score_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ScoreGetResponse:
        """Returns one score published in the requested scope.

        `value` contains the stored
        value as JSON. `value_type` distinguishes an integer score from a number score.

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
        if not score_id:
            raise ValueError(f"Expected a non-empty value for `score_id` but received {score_id!r}")
        return await self._get(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/scores/{score_id}",
                namespace=namespace,
                scope_id=scope_id,
                score_id=score_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ScoreGetResponse,
        )


class ScoresResourceWithRawResponse:
    def __init__(self, scores: ScoresResource) -> None:
        self._scores = scores

        self.create = to_raw_response_wrapper(
            scores.create,
        )
        self.get = to_raw_response_wrapper(
            scores.get,
        )


class AsyncScoresResourceWithRawResponse:
    def __init__(self, scores: AsyncScoresResource) -> None:
        self._scores = scores

        self.create = async_to_raw_response_wrapper(
            scores.create,
        )
        self.get = async_to_raw_response_wrapper(
            scores.get,
        )


class ScoresResourceWithStreamingResponse:
    def __init__(self, scores: ScoresResource) -> None:
        self._scores = scores

        self.create = to_streamed_response_wrapper(
            scores.create,
        )
        self.get = to_streamed_response_wrapper(
            scores.get,
        )


class AsyncScoresResourceWithStreamingResponse:
    def __init__(self, scores: AsyncScoresResource) -> None:
        self._scores = scores

        self.create = async_to_streamed_response_wrapper(
            scores.create,
        )
        self.get = async_to_streamed_response_wrapper(
            scores.get,
        )
