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
from ...pagination import SyncCursorPage, AsyncCursorPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.small_molecule import explore_start_params, explore_retrieve_params, explore_list_results_params
from ...types.small_molecule.explore_stop_response import ExploreStopResponse
from ...types.small_molecule.explore_start_response import ExploreStartResponse
from ...types.small_molecule.explore_resume_response import ExploreResumeResponse
from ...types.small_molecule.explore_retrieve_response import ExploreRetrieveResponse
from ...types.small_molecule.explore_list_results_response import ExploreListResultsResponse

__all__ = ["ExploreResource", "AsyncExploreResource"]


class ExploreResource(SyncAPIResource):
    """
    Explore a large library of small molecules against a protein target without screening all of it. Submit the whole library and a budget; molecules are chosen to score as results arrive, so each choice is informed by everything scored so far. Results use the same scores as a library screen, and progress reports the library size alongside the budget.
    """

    @cached_property
    def with_raw_response(self) -> ExploreResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return ExploreResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExploreResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return ExploreResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: str,
        *,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExploreRetrieveResponse:
        """Retrieve an exploration by ID.

        Once library preparation completes, progress
        reports the accepted library size alongside the budget.

        Args:
          workspace_id: Workspace ID. Only used with admin API keys. Ignored (or validated) for
              workspace-scoped keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/compute/v1/small-molecule/explore/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"workspace_id": workspace_id}, explore_retrieve_params.ExploreRetrieveParams),
            ),
            cast_to=ExploreRetrieveResponse,
        )

    def list_results(
        self,
        id: str,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        ids: str | Omit = omit,
        limit: int | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[ExploreListResultsResponse]:
        """Retrieve paginated results from an exploration.

        Results appear as molecules are
        scored, and remain retrievable if the run fails partway.

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          ids: Comma-separated list of result IDs to filter by (max 200). Only results whose ID
              matches one of these is returned; missing IDs are silently skipped. Composes
              with `limit`, `after_id`, and `before_id` — the filter is applied before
              pagination.

          limit: Max results to return. Defaults to 100.

          workspace_id: Workspace ID. Only used with admin API keys. Ignored (or validated) for
              workspace-scoped keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get_api_list(
            path_template("/compute/v1/small-molecule/explore/{id}/results", id=id),
            page=SyncCursorPage[ExploreListResultsResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "ids": ids,
                        "limit": limit,
                        "workspace_id": workspace_id,
                    },
                    explore_list_results_params.ExploreListResultsParams,
                ),
            ),
            model=ExploreListResultsResponse,
        )

    def resume(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExploreResumeResponse:
        """Resume a stopped exploration.

        Selection continues from the surrogate as it
        stood, so molecules already scored still inform what is chosen next.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/small-molecule/explore/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExploreResumeResponse,
        )

    def start(
        self,
        *,
        budget: int,
        library: explore_start_params.Library,
        target: explore_start_params.Target,
        idempotency_key: str | Omit = omit,
        molecule_filters: explore_start_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExploreStartResponse:
        """
        Explore a large library against a protein target without screening all of it.
        Submit the whole library and a budget; molecules are chosen to score as results
        arrive, so each choice is informed by everything scored before it.

        Args:
          budget: How many molecules to score. Each is chosen using everything scored before it,
              so a run recovers far more of the library's best-scoring molecules than
              screening the same number blindly. Scoring around 7% of the library is where
              that advantage is clearest. Must not exceed the accepted library size or
              5,000,000.

          library: CSV or TSV molecule library, limited to 375 MiB and 5,000,000 data records. URL
              sources can use the full file limit. Base64 sources are also subject to the
              API's 50 MiB JSON request-body limit, so use a URL source for larger files. The
              file must be UTF-8 and may contain only the selected SMILES and ID columns;
              column order does not matter. Candidate IDs are limited to 1,024 UTF-8 bytes;
              missing or blank IDs default to the zero-based data-record index.

          target: Target protein sequences for small molecule design or screening.

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          molecule_filters: Molecule filtering configuration. Controls both Boltz built-in SMARTS filtering
              and custom filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/compute/v1/small-molecule/explore",
            body=maybe_transform(
                {
                    "budget": budget,
                    "library": library,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                explore_start_params.ExploreStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExploreStartResponse,
        )

    def stop(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExploreStopResponse:
        """Stop an in-progress exploration early.

        Molecules already scored are kept and
        remain retrievable; no further molecules are selected.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/small-molecule/explore/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExploreStopResponse,
        )


class AsyncExploreResource(AsyncAPIResource):
    """
    Explore a large library of small molecules against a protein target without screening all of it. Submit the whole library and a budget; molecules are chosen to score as results arrive, so each choice is informed by everything scored so far. Results use the same scores as a library screen, and progress reports the library size alongside the budget.
    """

    @cached_property
    def with_raw_response(self) -> AsyncExploreResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncExploreResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExploreResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncExploreResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: str,
        *,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExploreRetrieveResponse:
        """Retrieve an exploration by ID.

        Once library preparation completes, progress
        reports the accepted library size alongside the budget.

        Args:
          workspace_id: Workspace ID. Only used with admin API keys. Ignored (or validated) for
              workspace-scoped keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/compute/v1/small-molecule/explore/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"workspace_id": workspace_id}, explore_retrieve_params.ExploreRetrieveParams
                ),
            ),
            cast_to=ExploreRetrieveResponse,
        )

    def list_results(
        self,
        id: str,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        ids: str | Omit = omit,
        limit: int | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ExploreListResultsResponse, AsyncCursorPage[ExploreListResultsResponse]]:
        """Retrieve paginated results from an exploration.

        Results appear as molecules are
        scored, and remain retrievable if the run fails partway.

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          ids: Comma-separated list of result IDs to filter by (max 200). Only results whose ID
              matches one of these is returned; missing IDs are silently skipped. Composes
              with `limit`, `after_id`, and `before_id` — the filter is applied before
              pagination.

          limit: Max results to return. Defaults to 100.

          workspace_id: Workspace ID. Only used with admin API keys. Ignored (or validated) for
              workspace-scoped keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get_api_list(
            path_template("/compute/v1/small-molecule/explore/{id}/results", id=id),
            page=AsyncCursorPage[ExploreListResultsResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "ids": ids,
                        "limit": limit,
                        "workspace_id": workspace_id,
                    },
                    explore_list_results_params.ExploreListResultsParams,
                ),
            ),
            model=ExploreListResultsResponse,
        )

    async def resume(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExploreResumeResponse:
        """Resume a stopped exploration.

        Selection continues from the surrogate as it
        stood, so molecules already scored still inform what is chosen next.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/small-molecule/explore/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExploreResumeResponse,
        )

    async def start(
        self,
        *,
        budget: int,
        library: explore_start_params.Library,
        target: explore_start_params.Target,
        idempotency_key: str | Omit = omit,
        molecule_filters: explore_start_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExploreStartResponse:
        """
        Explore a large library against a protein target without screening all of it.
        Submit the whole library and a budget; molecules are chosen to score as results
        arrive, so each choice is informed by everything scored before it.

        Args:
          budget: How many molecules to score. Each is chosen using everything scored before it,
              so a run recovers far more of the library's best-scoring molecules than
              screening the same number blindly. Scoring around 7% of the library is where
              that advantage is clearest. Must not exceed the accepted library size or
              5,000,000.

          library: CSV or TSV molecule library, limited to 375 MiB and 5,000,000 data records. URL
              sources can use the full file limit. Base64 sources are also subject to the
              API's 50 MiB JSON request-body limit, so use a URL source for larger files. The
              file must be UTF-8 and may contain only the selected SMILES and ID columns;
              column order does not matter. Candidate IDs are limited to 1,024 UTF-8 bytes;
              missing or blank IDs default to the zero-based data-record index.

          target: Target protein sequences for small molecule design or screening.

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          molecule_filters: Molecule filtering configuration. Controls both Boltz built-in SMARTS filtering
              and custom filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/compute/v1/small-molecule/explore",
            body=await async_maybe_transform(
                {
                    "budget": budget,
                    "library": library,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                explore_start_params.ExploreStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExploreStartResponse,
        )

    async def stop(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExploreStopResponse:
        """Stop an in-progress exploration early.

        Molecules already scored are kept and
        remain retrievable; no further molecules are selected.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/small-molecule/explore/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExploreStopResponse,
        )


class ExploreResourceWithRawResponse:
    def __init__(self, explore: ExploreResource) -> None:
        self._explore = explore

        self.retrieve = to_raw_response_wrapper(
            explore.retrieve,
        )
        self.list_results = to_raw_response_wrapper(
            explore.list_results,
        )
        self.resume = to_raw_response_wrapper(
            explore.resume,
        )
        self.start = to_raw_response_wrapper(
            explore.start,
        )
        self.stop = to_raw_response_wrapper(
            explore.stop,
        )


class AsyncExploreResourceWithRawResponse:
    def __init__(self, explore: AsyncExploreResource) -> None:
        self._explore = explore

        self.retrieve = async_to_raw_response_wrapper(
            explore.retrieve,
        )
        self.list_results = async_to_raw_response_wrapper(
            explore.list_results,
        )
        self.resume = async_to_raw_response_wrapper(
            explore.resume,
        )
        self.start = async_to_raw_response_wrapper(
            explore.start,
        )
        self.stop = async_to_raw_response_wrapper(
            explore.stop,
        )


class ExploreResourceWithStreamingResponse:
    def __init__(self, explore: ExploreResource) -> None:
        self._explore = explore

        self.retrieve = to_streamed_response_wrapper(
            explore.retrieve,
        )
        self.list_results = to_streamed_response_wrapper(
            explore.list_results,
        )
        self.resume = to_streamed_response_wrapper(
            explore.resume,
        )
        self.start = to_streamed_response_wrapper(
            explore.start,
        )
        self.stop = to_streamed_response_wrapper(
            explore.stop,
        )


class AsyncExploreResourceWithStreamingResponse:
    def __init__(self, explore: AsyncExploreResource) -> None:
        self._explore = explore

        self.retrieve = async_to_streamed_response_wrapper(
            explore.retrieve,
        )
        self.list_results = async_to_streamed_response_wrapper(
            explore.list_results,
        )
        self.resume = async_to_streamed_response_wrapper(
            explore.resume,
        )
        self.start = async_to_streamed_response_wrapper(
            explore.start,
        )
        self.stop = async_to_streamed_response_wrapper(
            explore.stop,
        )
