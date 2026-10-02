# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing as _t  # boltz-api-custom-line
from typing_extensions import Literal

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
    design_list_params,
    design_start_params,
    design_retrieve_params,
    design_list_results_params,
    design_estimate_cost_params,
)
from ...types.small_molecule.design_list_response import DesignListResponse
from ...types.small_molecule.design_stop_response import DesignStopResponse
from ...types.small_molecule.design_start_response import DesignStartResponse
from ...types.small_molecule.design_resume_response import DesignResumeResponse
from ...types.small_molecule.design_retrieve_response import DesignRetrieveResponse
from ...types.small_molecule.design_delete_data_response import DesignDeleteDataResponse
from ...types.small_molecule.design_list_results_response import DesignListResultsResponse
from ...types.small_molecule.design_estimate_cost_response import DesignEstimateCostResponse

# <boltz-api-custom-code>
if _t.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path

    from ...experiments._state import DownloadMode
# </boltz-api-custom-code>
__all__ = ["DesignResource", "AsyncDesignResource"]


class DesignResource(SyncAPIResource):
    """Generate novel small molecules optimized for binding to a protein target.

    Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
    """

    # <boltz-api-custom-code>
    if _t.TYPE_CHECKING:

        def run(
            self,
            *,
            num_molecules: int,
            target: design_start_params.Target,
            chemical_space: Literal["enamine_real"] | None = None,
            molecule_filters: design_start_params.MoleculeFilters | None = None,
            root_dir: str | PathLike[str] = "boltz-experiments",
            name: str | None = None,
            workspace_id: str | Omit = omit,
            download_mode: DownloadMode | str | None = None,
            quiet: bool = False,
            poll_interval_seconds: float = 5.0,
        ) -> Path: ...
    # </boltz-api-custom-code>

    @cached_property
    def with_raw_response(self) -> DesignResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return DesignResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DesignResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return DesignResourceWithStreamingResponse(self)

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
    ) -> DesignRetrieveResponse:
        """
        Retrieve a design run by ID, including progress and status

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
            path_template("/compute/v1/small-molecule/design/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"workspace_id": workspace_id}, design_retrieve_params.DesignRetrieveParams),
            ),
            cast_to=DesignRetrieveResponse,
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
    ) -> SyncCursorPage[DesignListResponse]:
        """
        List small molecule design runs, optionally filtered by workspace

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
            "/compute/v1/small-molecule/design",
            page=SyncCursorPage[DesignListResponse],
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
                    design_list_params.DesignListParams,
                ),
            ),
            model=DesignListResponse,
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
    ) -> DesignDeleteDataResponse:
        """
        Permanently delete the input, output, and result data associated with this
        design run. The design run record itself is retained with a `data_deleted_at`
        timestamp. This action is irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/small-molecule/design/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignDeleteDataResponse,
        )

    def estimate_cost(
        self,
        *,
        num_molecules: int,
        target: design_estimate_cost_params.Target,
        chemical_space: Literal["enamine_real", "none"] | Omit = omit,
        idempotency_key: str | Omit = omit,
        molecule_filters: design_estimate_cost_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        """
        Estimate the billed cost of a small molecule design run without creating any
        resource or consuming GPU. Includes generation charges implied by the scheduler
        iteration cap plus structure-scoring charges for each requested molecule.

        Args:
          num_molecules: Number of molecules to generate. Must be between 10 and 1,000,000.

          target: Target protein sequences for small molecule design or screening.

          chemical_space: Chemical space to constrain generated molecules. Use 'enamine_real' for the
              Enamine REAL chemical space, 'wuxi_galaxi' for the WuXi GalaXi chemical space
              when enabled for your organization, or 'none' to disable chemical-space
              filtering.

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
            "/compute/v1/small-molecule/design/estimate-cost",
            body=maybe_transform(
                {
                    "num_molecules": num_molecules,
                    "target": target,
                    "chemical_space": chemical_space,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                design_estimate_cost_params.DesignEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignEstimateCostResponse,
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
    ) -> SyncCursorPage[DesignListResultsResponse]:
        """
        Retrieve paginated results from a design run

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
            path_template("/compute/v1/small-molecule/design/{id}/results", id=id),
            page=SyncCursorPage[DesignListResultsResponse],
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
                    design_list_results_params.DesignListResultsParams,
                ),
            ),
            model=DesignListResultsResponse,
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
    ) -> DesignResumeResponse:
        """
        Resume a stopped small molecule design run from its last checkpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/small-molecule/design/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignResumeResponse,
        )

    def start(
        self,
        *,
        num_molecules: int,
        target: design_start_params.Target,
        chemical_space: Literal["enamine_real", "none"] | Omit = omit,
        idempotency_key: str | Omit = omit,
        molecule_filters: design_start_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        """
        Create a new design run that generates novel small molecule candidates for a
        protein target

        Args:
          num_molecules: Number of molecules to generate. Must be between 10 and 1,000,000.

          target: Target protein sequences for small molecule design or screening.

          chemical_space: Chemical space to constrain generated molecules. Use 'enamine_real' for the
              Enamine REAL chemical space, 'wuxi_galaxi' for the WuXi GalaXi chemical space
              when enabled for your organization, or 'none' to disable chemical-space
              filtering.

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
            "/compute/v1/small-molecule/design",
            body=maybe_transform(
                {
                    "num_molecules": num_molecules,
                    "target": target,
                    "chemical_space": chemical_space,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                design_start_params.DesignStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignStartResponse,
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
    ) -> DesignStopResponse:
        """
        Stop an in-progress design run early

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/small-molecule/design/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignStopResponse,
        )


class AsyncDesignResource(AsyncAPIResource):
    """Generate novel small molecules optimized for binding to a protein target.

    Results are scored by binding confidence (likelihood of binding, for hit discovery), optimization score (binding strength ranking, for lead optimization), and structure confidence.
    """

    @cached_property
    def with_raw_response(self) -> AsyncDesignResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDesignResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDesignResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncDesignResourceWithStreamingResponse(self)

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
    ) -> DesignRetrieveResponse:
        """
        Retrieve a design run by ID, including progress and status

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
            path_template("/compute/v1/small-molecule/design/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"workspace_id": workspace_id}, design_retrieve_params.DesignRetrieveParams
                ),
            ),
            cast_to=DesignRetrieveResponse,
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
    ) -> AsyncPaginator[DesignListResponse, AsyncCursorPage[DesignListResponse]]:
        """
        List small molecule design runs, optionally filtered by workspace

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
            "/compute/v1/small-molecule/design",
            page=AsyncCursorPage[DesignListResponse],
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
                    design_list_params.DesignListParams,
                ),
            ),
            model=DesignListResponse,
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
    ) -> DesignDeleteDataResponse:
        """
        Permanently delete the input, output, and result data associated with this
        design run. The design run record itself is retained with a `data_deleted_at`
        timestamp. This action is irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/small-molecule/design/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignDeleteDataResponse,
        )

    async def estimate_cost(
        self,
        *,
        num_molecules: int,
        target: design_estimate_cost_params.Target,
        chemical_space: Literal["enamine_real", "none"] | Omit = omit,
        idempotency_key: str | Omit = omit,
        molecule_filters: design_estimate_cost_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        """
        Estimate the billed cost of a small molecule design run without creating any
        resource or consuming GPU. Includes generation charges implied by the scheduler
        iteration cap plus structure-scoring charges for each requested molecule.

        Args:
          num_molecules: Number of molecules to generate. Must be between 10 and 1,000,000.

          target: Target protein sequences for small molecule design or screening.

          chemical_space: Chemical space to constrain generated molecules. Use 'enamine_real' for the
              Enamine REAL chemical space, 'wuxi_galaxi' for the WuXi GalaXi chemical space
              when enabled for your organization, or 'none' to disable chemical-space
              filtering.

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
            "/compute/v1/small-molecule/design/estimate-cost",
            body=await async_maybe_transform(
                {
                    "num_molecules": num_molecules,
                    "target": target,
                    "chemical_space": chemical_space,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                design_estimate_cost_params.DesignEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignEstimateCostResponse,
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
    ) -> AsyncPaginator[DesignListResultsResponse, AsyncCursorPage[DesignListResultsResponse]]:
        """
        Retrieve paginated results from a design run

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
            path_template("/compute/v1/small-molecule/design/{id}/results", id=id),
            page=AsyncCursorPage[DesignListResultsResponse],
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
                    design_list_results_params.DesignListResultsParams,
                ),
            ),
            model=DesignListResultsResponse,
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
    ) -> DesignResumeResponse:
        """
        Resume a stopped small molecule design run from its last checkpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/small-molecule/design/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignResumeResponse,
        )

    async def start(
        self,
        *,
        num_molecules: int,
        target: design_start_params.Target,
        chemical_space: Literal["enamine_real", "none"] | Omit = omit,
        idempotency_key: str | Omit = omit,
        molecule_filters: design_start_params.MoleculeFilters | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        """
        Create a new design run that generates novel small molecule candidates for a
        protein target

        Args:
          num_molecules: Number of molecules to generate. Must be between 10 and 1,000,000.

          target: Target protein sequences for small molecule design or screening.

          chemical_space: Chemical space to constrain generated molecules. Use 'enamine_real' for the
              Enamine REAL chemical space, 'wuxi_galaxi' for the WuXi GalaXi chemical space
              when enabled for your organization, or 'none' to disable chemical-space
              filtering.

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
            "/compute/v1/small-molecule/design",
            body=await async_maybe_transform(
                {
                    "num_molecules": num_molecules,
                    "target": target,
                    "chemical_space": chemical_space,
                    "idempotency_key": idempotency_key,
                    "molecule_filters": molecule_filters,
                    "workspace_id": workspace_id,
                },
                design_start_params.DesignStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignStartResponse,
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
    ) -> DesignStopResponse:
        """
        Stop an in-progress design run early

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/small-molecule/design/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignStopResponse,
        )


class DesignResourceWithRawResponse:
    def __init__(self, design: DesignResource) -> None:
        self._design = design

        self.retrieve = to_raw_response_wrapper(
            design.retrieve,
        )
        self.list = to_raw_response_wrapper(
            design.list,
        )
        self.delete_data = to_raw_response_wrapper(
            design.delete_data,
        )
        self.estimate_cost = to_raw_response_wrapper(
            design.estimate_cost,
        )
        self.list_results = to_raw_response_wrapper(
            design.list_results,
        )
        self.resume = to_raw_response_wrapper(
            design.resume,
        )
        self.start = to_raw_response_wrapper(
            design.start,
        )
        self.stop = to_raw_response_wrapper(
            design.stop,
        )


class AsyncDesignResourceWithRawResponse:
    def __init__(self, design: AsyncDesignResource) -> None:
        self._design = design

        self.retrieve = async_to_raw_response_wrapper(
            design.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            design.list,
        )
        self.delete_data = async_to_raw_response_wrapper(
            design.delete_data,
        )
        self.estimate_cost = async_to_raw_response_wrapper(
            design.estimate_cost,
        )
        self.list_results = async_to_raw_response_wrapper(
            design.list_results,
        )
        self.resume = async_to_raw_response_wrapper(
            design.resume,
        )
        self.start = async_to_raw_response_wrapper(
            design.start,
        )
        self.stop = async_to_raw_response_wrapper(
            design.stop,
        )


class DesignResourceWithStreamingResponse:
    def __init__(self, design: DesignResource) -> None:
        self._design = design

        self.retrieve = to_streamed_response_wrapper(
            design.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            design.list,
        )
        self.delete_data = to_streamed_response_wrapper(
            design.delete_data,
        )
        self.estimate_cost = to_streamed_response_wrapper(
            design.estimate_cost,
        )
        self.list_results = to_streamed_response_wrapper(
            design.list_results,
        )
        self.resume = to_streamed_response_wrapper(
            design.resume,
        )
        self.start = to_streamed_response_wrapper(
            design.start,
        )
        self.stop = to_streamed_response_wrapper(
            design.stop,
        )


class AsyncDesignResourceWithStreamingResponse:
    def __init__(self, design: AsyncDesignResource) -> None:
        self._design = design

        self.retrieve = async_to_streamed_response_wrapper(
            design.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            design.list,
        )
        self.delete_data = async_to_streamed_response_wrapper(
            design.delete_data,
        )
        self.estimate_cost = async_to_streamed_response_wrapper(
            design.estimate_cost,
        )
        self.list_results = async_to_streamed_response_wrapper(
            design.list_results,
        )
        self.resume = async_to_streamed_response_wrapper(
            design.resume,
        )
        self.start = async_to_streamed_response_wrapper(
            design.start,
        )
        self.stop = async_to_streamed_response_wrapper(
            design.stop,
        )
