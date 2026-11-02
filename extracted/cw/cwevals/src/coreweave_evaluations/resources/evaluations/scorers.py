# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..._types import Body, Query, Headers, NotGiven, not_given
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
from ...types.evaluations import scorer_add_params
from ...types.evaluations.scorer_add_response import ScorerAddResponse

__all__ = ["ScorersResource", "AsyncScorersResource"]


class ScorersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ScorersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return ScorersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ScorersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return ScorersResourceWithStreamingResponse(self)

    def add(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        scorers: Iterable[scorer_add_params.Scorer],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScorerAddResponse:
        """
        Atomically adds Scorers to the Evaluation's pending head or selects another
        version of an already registered Scorer. Published EvaluationVersions keep their
        selections. The Evaluation's latest data reads the selected versions' Scores.
        Saved EvaluationQueries name ScorerVersions, so create a new query when
        replacing a version used by an existing query. Every version must score cases or
        trajectories. A version that cannot score the targets of a saved query that
        groups by its scorer, or uses it as a pass_at_k task, returns 400. A missing
        Scorer or version returns 404, and a name already registered to another Scorer
        returns 409. Repeating the same selections changes nothing. If any item is
        invalid, no selections change.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          scorers: Scorer versions to add. Each Scorer ID must be unique. An already registered
              Scorer changes to the supplied version, which must keep its registered name and
              value type.

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
        return self._patch(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/scorers",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            body=maybe_transform({"scorers": scorers}, scorer_add_params.ScorerAddParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScorerAddResponse,
        )


class AsyncScorersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncScorersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/wandb/core#accessing-raw-response-data-eg-headers
        """
        return AsyncScorersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncScorersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/wandb/core#with_streaming_response
        """
        return AsyncScorersResourceWithStreamingResponse(self)

    async def add(
        self,
        evaluation_id: str,
        *,
        namespace: str | None = None,
        scope_id: str | None = None,
        scorers: Iterable[scorer_add_params.Scorer],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ScorerAddResponse:
        """
        Atomically adds Scorers to the Evaluation's pending head or selects another
        version of an already registered Scorer. Published EvaluationVersions keep their
        selections. The Evaluation's latest data reads the selected versions' Scores.
        Saved EvaluationQueries name ScorerVersions, so create a new query when
        replacing a version used by an existing query. Every version must score cases or
        trajectories. A version that cannot score the targets of a saved query that
        groups by its scorer, or uses it as a pass_at_k task, returns 400. A missing
        Scorer or version returns 404, and a name already registered to another Scorer
        returns 409. Repeating the same selections changes nothing. If any item is
        invalid, no selections change.

        Request bodies must be smaller than 1 MiB. Larger bodies are rejected with 413
        Request Entity Too Large.

        Args:
          namespace: Namespace that assigned the scope reference.

          scope_id: Project reference assigned by the namespace. For wandb, use the internal W&B
              project ID, not the project name or entity/project path.

              Percent-encode reserved characters so the reference occupies one URL path
              segment. Only printable ASCII is accepted. References are compared exactly,
              without parsing.

          scorers: Scorer versions to add. Each Scorer ID must be unique. An already registered
              Scorer changes to the supplied version, which must keep its registered name and
              value type.

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
        return await self._patch(
            path_template(
                "/v1/namespaces/{namespace}/scopes/{scope_id}/evaluations/{evaluation_id}/scorers",
                namespace=namespace,
                scope_id=scope_id,
                evaluation_id=evaluation_id,
            ),
            body=await async_maybe_transform({"scorers": scorers}, scorer_add_params.ScorerAddParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ScorerAddResponse,
        )


class ScorersResourceWithRawResponse:
    def __init__(self, scorers: ScorersResource) -> None:
        self._scorers = scorers

        self.add = to_raw_response_wrapper(
            scorers.add,
        )


class AsyncScorersResourceWithRawResponse:
    def __init__(self, scorers: AsyncScorersResource) -> None:
        self._scorers = scorers

        self.add = async_to_raw_response_wrapper(
            scorers.add,
        )


class ScorersResourceWithStreamingResponse:
    def __init__(self, scorers: ScorersResource) -> None:
        self._scorers = scorers

        self.add = to_streamed_response_wrapper(
            scorers.add,
        )


class AsyncScorersResourceWithStreamingResponse:
    def __init__(self, scorers: AsyncScorersResource) -> None:
        self._scorers = scorers

        self.add = async_to_streamed_response_wrapper(
            scorers.add,
        )
