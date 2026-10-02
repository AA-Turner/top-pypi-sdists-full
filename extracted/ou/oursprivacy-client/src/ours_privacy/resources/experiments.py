# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Optional, cast

import httpx

from ..types import experiment_assignment_params, experiment_personalization_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ..types.experiment_assignment_response import ExperimentAssignmentResponse
from ..types.experiment_personalization_response import ExperimentPersonalizationResponse

__all__ = ["ExperimentsResource", "AsyncExperimentsResource"]


class ExperimentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ExperimentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ExperimentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExperimentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#with_streaming_response
        """
        return ExperimentsResourceWithStreamingResponse(self)

    def assignment(
        self,
        experiment_key: str,
        *,
        token: str,
        visitor_id: str,
        context: Optional[experiment_assignment_params.Context] | Omit = omit,
        track_impression: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExperimentAssignmentResponse:
        """
        Return the server-side variant assignment for a visitor in a single A/B or
        multivariate experiment, identified by its experiment key. Bucketing is
        deterministic on `visitor_id` and is sticky across calls. Tracking an impression
        is the default — pass `track_impression: false` to read without recording. The
        browser SDK and this endpoint converge on the same variant for the same visitor.

        Args:
          experiment_key: The experiment's stable key. Surfaced in the dashboard under each experiment's
              setup tab.

          token: The experiment token (`exp_*`) for the experiment settings holding this
              experiment. Available from the dashboard.

          visitor_id: Stable identifier for the visitor — typically the Ours visitor id from your
              browser cookie, or your own server-side user id if you keep the same id
              consistent across browser and server.

          context: Optional page context for URL + query-param eligibility. Variant bucketing is
              deterministic on `visitor_id` regardless of context.

          track_impression: When true (default), an `$experiment_impression` event is enqueued and the
              visitor's `experiment_assignments` map is updated. Set to false to read the
              assignment without recording an impression — useful for in-test diagnostics.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not experiment_key:
            raise ValueError(f"Expected a non-empty value for `experiment_key` but received {experiment_key!r}")
        return cast(
            ExperimentAssignmentResponse,
            self._post(
                ("https://api.oursprivacy.com/api/v1" if not self._client._base_url_overridden else "")
                + path_template("/experiments/assignments/{experiment_key}", experiment_key=experiment_key),
                body=maybe_transform(
                    {
                        "token": token,
                        "visitor_id": visitor_id,
                        "context": context,
                        "track_impression": track_impression,
                    },
                    experiment_assignment_params.ExperimentAssignmentParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ExperimentAssignmentResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def personalization(
        self,
        *,
        token: str,
        visitor_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExperimentPersonalizationResponse:
        """
        Return the visitor traits accumulated by personalization property rules.
        Read-only and never records an impression. Use the properties to select
        personalized server-rendered copy or targeting; the browser experiment runtime
        receives the same bag at initialization.

        Args:
          token: The experiment token (`exp_*`).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/experiments/personalization"
            if self._client._base_url_overridden
            else "https://api.oursprivacy.com/api/v1/experiments/personalization",
            body=maybe_transform(
                {
                    "token": token,
                    "visitor_id": visitor_id,
                },
                experiment_personalization_params.ExperimentPersonalizationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExperimentPersonalizationResponse,
        )


class AsyncExperimentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncExperimentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncExperimentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExperimentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/with-ours/ingest-sdk-python#with_streaming_response
        """
        return AsyncExperimentsResourceWithStreamingResponse(self)

    async def assignment(
        self,
        experiment_key: str,
        *,
        token: str,
        visitor_id: str,
        context: Optional[experiment_assignment_params.Context] | Omit = omit,
        track_impression: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExperimentAssignmentResponse:
        """
        Return the server-side variant assignment for a visitor in a single A/B or
        multivariate experiment, identified by its experiment key. Bucketing is
        deterministic on `visitor_id` and is sticky across calls. Tracking an impression
        is the default — pass `track_impression: false` to read without recording. The
        browser SDK and this endpoint converge on the same variant for the same visitor.

        Args:
          experiment_key: The experiment's stable key. Surfaced in the dashboard under each experiment's
              setup tab.

          token: The experiment token (`exp_*`) for the experiment settings holding this
              experiment. Available from the dashboard.

          visitor_id: Stable identifier for the visitor — typically the Ours visitor id from your
              browser cookie, or your own server-side user id if you keep the same id
              consistent across browser and server.

          context: Optional page context for URL + query-param eligibility. Variant bucketing is
              deterministic on `visitor_id` regardless of context.

          track_impression: When true (default), an `$experiment_impression` event is enqueued and the
              visitor's `experiment_assignments` map is updated. Set to false to read the
              assignment without recording an impression — useful for in-test diagnostics.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not experiment_key:
            raise ValueError(f"Expected a non-empty value for `experiment_key` but received {experiment_key!r}")
        return cast(
            ExperimentAssignmentResponse,
            await self._post(
                ("https://api.oursprivacy.com/api/v1" if not self._client._base_url_overridden else "")
                + path_template("/experiments/assignments/{experiment_key}", experiment_key=experiment_key),
                body=await async_maybe_transform(
                    {
                        "token": token,
                        "visitor_id": visitor_id,
                        "context": context,
                        "track_impression": track_impression,
                    },
                    experiment_assignment_params.ExperimentAssignmentParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(
                    Any, ExperimentAssignmentResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def personalization(
        self,
        *,
        token: str,
        visitor_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExperimentPersonalizationResponse:
        """
        Return the visitor traits accumulated by personalization property rules.
        Read-only and never records an impression. Use the properties to select
        personalized server-rendered copy or targeting; the browser experiment runtime
        receives the same bag at initialization.

        Args:
          token: The experiment token (`exp_*`).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/experiments/personalization"
            if self._client._base_url_overridden
            else "https://api.oursprivacy.com/api/v1/experiments/personalization",
            body=await async_maybe_transform(
                {
                    "token": token,
                    "visitor_id": visitor_id,
                },
                experiment_personalization_params.ExperimentPersonalizationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExperimentPersonalizationResponse,
        )


class ExperimentsResourceWithRawResponse:
    def __init__(self, experiments: ExperimentsResource) -> None:
        self._experiments = experiments

        self.assignment = to_raw_response_wrapper(
            experiments.assignment,
        )
        self.personalization = to_raw_response_wrapper(
            experiments.personalization,
        )


class AsyncExperimentsResourceWithRawResponse:
    def __init__(self, experiments: AsyncExperimentsResource) -> None:
        self._experiments = experiments

        self.assignment = async_to_raw_response_wrapper(
            experiments.assignment,
        )
        self.personalization = async_to_raw_response_wrapper(
            experiments.personalization,
        )


class ExperimentsResourceWithStreamingResponse:
    def __init__(self, experiments: ExperimentsResource) -> None:
        self._experiments = experiments

        self.assignment = to_streamed_response_wrapper(
            experiments.assignment,
        )
        self.personalization = to_streamed_response_wrapper(
            experiments.personalization,
        )


class AsyncExperimentsResourceWithStreamingResponse:
    def __init__(self, experiments: AsyncExperimentsResource) -> None:
        self._experiments = experiments

        self.assignment = async_to_streamed_response_wrapper(
            experiments.assignment,
        )
        self.personalization = async_to_streamed_response_wrapper(
            experiments.personalization,
        )
