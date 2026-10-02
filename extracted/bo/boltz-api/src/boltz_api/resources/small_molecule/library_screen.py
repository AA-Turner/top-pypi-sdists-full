# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing as _t  # boltz-api-custom-line
from typing import Iterable

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
from ...types.small_molecule import (
    library_screen_list_params,
    library_screen_start_params,
    library_screen_retrieve_params,
    library_screen_list_results_params,
    library_screen_estimate_cost_params,
)
from ...types.small_molecule.library_screen_list_response import LibraryScreenListResponse
from ...types.small_molecule.library_screen_stop_response import LibraryScreenStopResponse
from ...types.small_molecule.library_screen_start_response import LibraryScreenStartResponse
from ...types.small_molecule.library_screen_resume_response import LibraryScreenResumeResponse
from ...types.small_molecule.library_screen_retrieve_response import LibraryScreenRetrieveResponse
from ...types.small_molecule.library_screen_delete_data_response import LibraryScreenDeleteDataResponse
from ...types.small_molecule.library_screen_list_results_response import LibraryScreenListResultsResponse
from ...types.small_molecule.library_screen_estimate_cost_response import LibraryScreenEstimateCostResponse

# <boltz-api-custom-code>
if _t.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path

    from ...experiments._state import DownloadMode
# </boltz-api-custom-code>
__all__ = ["LibraryScreenResource", "AsyncLibraryScreenResource"]


class LibraryScreenResource(SyncAPIResource):
    """Screen an existing library of small molecules against a protein target.

    Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
    """

    # <boltz-api-custom-code>
    if _t.TYPE_CHECKING:

        def run(
            self,
            *,
            molecules: Iterable[library_screen_start_params.Molecule],
            target: library_screen_start_params.Target,
            molecule_filters: library_screen_start_params.MoleculeFilters | None = None,
            root_dir: str | PathLike[str] = "boltz-experiments",
            name: str | None = None,
            workspace_id: str | Omit = omit,
            download_mode: DownloadMode | str | None = None,
            quiet: bool = False,
            poll_interval_seconds: float = 5.0,
        ) -> Path: ...
    # </boltz-api-custom-code>

    @cached_property
    def with_raw_response(self) -> LibraryScreenResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return LibraryScreenResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LibraryScreenResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return LibraryScreenResourceWithStreamingResponse(self)

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
    ) -> LibraryScreenRetrieveResponse:
        """
        Retrieve a library screen by ID, including progress and status

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
            path_template("/compute/v1/small-molecule/library-screen/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"workspace_id": workspace_id}, library_screen_retrieve_params.LibraryScreenRetrieveParams
                ),
            ),
            cast_to=LibraryScreenRetrieveResponse,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        limit: int | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorPage[LibraryScreenListResponse]:
        """
        List small molecule library screens, optionally filtered by workspace

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          limit: Max items to return. Defaults to 100.

          workspace_id: Filter by workspace ID. Only used with admin API keys. If not provided, defaults
              to the workspace associated with the API key, or the default workspace for admin
              keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/compute/v1/small-molecule/library-screen",
            page=SyncCursorPage[LibraryScreenListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                        "workspace_id": workspace_id,
                    },
                    library_screen_list_params.LibraryScreenListParams,
                ),
            ),
            model=LibraryScreenListResponse,
        )

    def delete_data(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LibraryScreenDeleteDataResponse:
        """
        Permanently delete the input, output, and result data associated with this
        library screen. The library screen record itself is retained with a
        `data_deleted_at` timestamp. This action is irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/small-molecule/library-screen/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenDeleteDataResponse,
        )

    def estimate_cost(
        self,
        *,
        molecules: Iterable[library_screen_estimate_cost_params.Molecule],
        target: library_screen_estimate_cost_params.Target,
        idempotency_key: str | Omit = omit,
        molecule_filters: library_screen_estimate_cost_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LibraryScreenEstimateCostResponse:
        """
        Estimate the cost of a small molecule library screen without creating any
        resource or consuming GPU.

        Args:
          molecules: List of small molecules to screen.

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
            "/compute/v1/small-molecule/library-screen/estimate-cost",
            body=maybe_transform(
                {
                    "molecules": molecules,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                library_screen_estimate_cost_params.LibraryScreenEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenEstimateCostResponse,
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
    ) -> SyncCursorPage[LibraryScreenListResultsResponse]:
        """
        Retrieve paginated results from a library screen

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
            path_template("/compute/v1/small-molecule/library-screen/{id}/results", id=id),
            page=SyncCursorPage[LibraryScreenListResultsResponse],
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
                    library_screen_list_results_params.LibraryScreenListResultsParams,
                ),
            ),
            model=LibraryScreenListResultsResponse,
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
    ) -> LibraryScreenResumeResponse:
        """
        Resume a stopped small molecule library screen from its last checkpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/small-molecule/library-screen/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenResumeResponse,
        )

    def start(
        self,
        *,
        molecules: Iterable[library_screen_start_params.Molecule],
        target: library_screen_start_params.Target,
        idempotency_key: str | Omit = omit,
        molecule_filters: library_screen_start_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LibraryScreenStartResponse:
        """
        Screen a set of small molecule candidates against a protein target

        Args:
          molecules: List of small molecules to screen.

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
            "/compute/v1/small-molecule/library-screen",
            body=maybe_transform(
                {
                    "molecules": molecules,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                library_screen_start_params.LibraryScreenStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenStartResponse,
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
    ) -> LibraryScreenStopResponse:
        """
        Stop an in-progress library screen early

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/small-molecule/library-screen/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenStopResponse,
        )


class AsyncLibraryScreenResource(AsyncAPIResource):
    """Screen an existing library of small molecules against a protein target.

    Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
    """

    @cached_property
    def with_raw_response(self) -> AsyncLibraryScreenResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLibraryScreenResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLibraryScreenResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncLibraryScreenResourceWithStreamingResponse(self)

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
    ) -> LibraryScreenRetrieveResponse:
        """
        Retrieve a library screen by ID, including progress and status

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
            path_template("/compute/v1/small-molecule/library-screen/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"workspace_id": workspace_id}, library_screen_retrieve_params.LibraryScreenRetrieveParams
                ),
            ),
            cast_to=LibraryScreenRetrieveResponse,
        )

    def list(
        self,
        *,
        after_id: str | Omit = omit,
        before_id: str | Omit = omit,
        limit: int | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[LibraryScreenListResponse, AsyncCursorPage[LibraryScreenListResponse]]:
        """
        List small molecule library screens, optionally filtered by workspace

        Args:
          after_id: Return results after this ID

          before_id: Return results before this ID

          limit: Max items to return. Defaults to 100.

          workspace_id: Filter by workspace ID. Only used with admin API keys. If not provided, defaults
              to the workspace associated with the API key, or the default workspace for admin
              keys.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/compute/v1/small-molecule/library-screen",
            page=AsyncCursorPage[LibraryScreenListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "after_id": after_id,
                        "before_id": before_id,
                        "limit": limit,
                        "workspace_id": workspace_id,
                    },
                    library_screen_list_params.LibraryScreenListParams,
                ),
            ),
            model=LibraryScreenListResponse,
        )

    async def delete_data(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LibraryScreenDeleteDataResponse:
        """
        Permanently delete the input, output, and result data associated with this
        library screen. The library screen record itself is retained with a
        `data_deleted_at` timestamp. This action is irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/small-molecule/library-screen/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenDeleteDataResponse,
        )

    async def estimate_cost(
        self,
        *,
        molecules: Iterable[library_screen_estimate_cost_params.Molecule],
        target: library_screen_estimate_cost_params.Target,
        idempotency_key: str | Omit = omit,
        molecule_filters: library_screen_estimate_cost_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LibraryScreenEstimateCostResponse:
        """
        Estimate the cost of a small molecule library screen without creating any
        resource or consuming GPU.

        Args:
          molecules: List of small molecules to screen.

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
            "/compute/v1/small-molecule/library-screen/estimate-cost",
            body=await async_maybe_transform(
                {
                    "molecules": molecules,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                library_screen_estimate_cost_params.LibraryScreenEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenEstimateCostResponse,
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
    ) -> AsyncPaginator[LibraryScreenListResultsResponse, AsyncCursorPage[LibraryScreenListResultsResponse]]:
        """
        Retrieve paginated results from a library screen

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
            path_template("/compute/v1/small-molecule/library-screen/{id}/results", id=id),
            page=AsyncCursorPage[LibraryScreenListResultsResponse],
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
                    library_screen_list_results_params.LibraryScreenListResultsParams,
                ),
            ),
            model=LibraryScreenListResultsResponse,
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
    ) -> LibraryScreenResumeResponse:
        """
        Resume a stopped small molecule library screen from its last checkpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/small-molecule/library-screen/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenResumeResponse,
        )

    async def start(
        self,
        *,
        molecules: Iterable[library_screen_start_params.Molecule],
        target: library_screen_start_params.Target,
        idempotency_key: str | Omit = omit,
        molecule_filters: library_screen_start_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> LibraryScreenStartResponse:
        """
        Screen a set of small molecule candidates against a protein target

        Args:
          molecules: List of small molecules to screen.

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
            "/compute/v1/small-molecule/library-screen",
            body=await async_maybe_transform(
                {
                    "molecules": molecules,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                library_screen_start_params.LibraryScreenStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenStartResponse,
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
    ) -> LibraryScreenStopResponse:
        """
        Stop an in-progress library screen early

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/small-molecule/library-screen/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LibraryScreenStopResponse,
        )


class LibraryScreenResourceWithRawResponse:
    def __init__(self, library_screen: LibraryScreenResource) -> None:
        self._library_screen = library_screen

        self.retrieve = to_raw_response_wrapper(
            library_screen.retrieve,
        )
        self.list = to_raw_response_wrapper(
            library_screen.list,
        )
        self.delete_data = to_raw_response_wrapper(
            library_screen.delete_data,
        )
        self.estimate_cost = to_raw_response_wrapper(
            library_screen.estimate_cost,
        )
        self.list_results = to_raw_response_wrapper(
            library_screen.list_results,
        )
        self.resume = to_raw_response_wrapper(
            library_screen.resume,
        )
        self.start = to_raw_response_wrapper(
            library_screen.start,
        )
        self.stop = to_raw_response_wrapper(
            library_screen.stop,
        )


class AsyncLibraryScreenResourceWithRawResponse:
    def __init__(self, library_screen: AsyncLibraryScreenResource) -> None:
        self._library_screen = library_screen

        self.retrieve = async_to_raw_response_wrapper(
            library_screen.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            library_screen.list,
        )
        self.delete_data = async_to_raw_response_wrapper(
            library_screen.delete_data,
        )
        self.estimate_cost = async_to_raw_response_wrapper(
            library_screen.estimate_cost,
        )
        self.list_results = async_to_raw_response_wrapper(
            library_screen.list_results,
        )
        self.resume = async_to_raw_response_wrapper(
            library_screen.resume,
        )
        self.start = async_to_raw_response_wrapper(
            library_screen.start,
        )
        self.stop = async_to_raw_response_wrapper(
            library_screen.stop,
        )


class LibraryScreenResourceWithStreamingResponse:
    def __init__(self, library_screen: LibraryScreenResource) -> None:
        self._library_screen = library_screen

        self.retrieve = to_streamed_response_wrapper(
            library_screen.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            library_screen.list,
        )
        self.delete_data = to_streamed_response_wrapper(
            library_screen.delete_data,
        )
        self.estimate_cost = to_streamed_response_wrapper(
            library_screen.estimate_cost,
        )
        self.list_results = to_streamed_response_wrapper(
            library_screen.list_results,
        )
        self.resume = to_streamed_response_wrapper(
            library_screen.resume,
        )
        self.start = to_streamed_response_wrapper(
            library_screen.start,
        )
        self.stop = to_streamed_response_wrapper(
            library_screen.stop,
        )


class AsyncLibraryScreenResourceWithStreamingResponse:
    def __init__(self, library_screen: AsyncLibraryScreenResource) -> None:
        self._library_screen = library_screen

        self.retrieve = async_to_streamed_response_wrapper(
            library_screen.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            library_screen.list,
        )
        self.delete_data = async_to_streamed_response_wrapper(
            library_screen.delete_data,
        )
        self.estimate_cost = async_to_streamed_response_wrapper(
            library_screen.estimate_cost,
        )
        self.list_results = async_to_streamed_response_wrapper(
            library_screen.list_results,
        )
        self.resume = async_to_streamed_response_wrapper(
            library_screen.resume,
        )
        self.start = async_to_streamed_response_wrapper(
            library_screen.start,
        )
        self.stop = async_to_streamed_response_wrapper(
            library_screen.stop,
        )
