# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing as _t  # boltz-api-custom-line
from typing import Any, Iterable, cast
from typing_extensions import Literal, overload

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, required_args, maybe_transform, async_maybe_transform
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
from ...types.protein import (
    design_list_params,
    design_start_params,
    design_retrieve_params,
    design_list_results_params,
    design_estimate_cost_params,
    design_list_curated_specifications_params,
)
from ...types.protein.design_list_response import DesignListResponse
from ...types.protein.design_stop_response import DesignStopResponse
from ...types.protein.design_start_response import DesignStartResponse
from ...types.protein.design_resume_response import DesignResumeResponse
from ...types.protein.design_retrieve_response import DesignRetrieveResponse
from ...types.protein.design_delete_data_response import DesignDeleteDataResponse
from ...types.protein.design_list_results_response import DesignListResultsResponse
from ...types.protein.design_estimate_cost_response import DesignEstimateCostResponse
from ...types.protein.design_list_curated_specifications_response import DesignListCuratedSpecificationsResponse

# <boltz-api-custom-code>
if _t.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path

    from ...experiments._state import DownloadMode
# </boltz-api-custom-code>
__all__ = ["DesignResource", "AsyncDesignResource"]


class DesignResource(SyncAPIResource):
    """Generate binder or generic protein designs.

    New requests use the top-level type discriminator (`binder` or `generic`), while the legacy target plus binder_specification body remains accepted for migration. Binder requests can share one CIF across target and binder, sample uniformly across multiple specifications, or use Boltz-managed curated antibody and nanobody defaults. Results are discriminated by type: binder runs include binding metrics, while generic runs return structure and secondary-structure metrics only. A generic request can use a `fusion_protein` entity to concatenate two or more ordered fixed, designed, or template-backed protein segments into one output chain.
    """

    # <boltz-api-custom-code>
    if _t.TYPE_CHECKING:

        def run(
            self,
            *,
            binder_specification: design_start_params.ProteinDesignRunInputBinderSpecification,
            num_proteins: int,
            target: design_start_params.ProteinDesignRunInputTarget,
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
            path_template("/compute/v1/protein/design/{id}", id=id),
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
        List protein design runs, optionally filtered by workspace

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
            "/compute/v1/protein/design",
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
            path_template("/compute/v1/protein/design/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignDeleteDataResponse,
        )

    @overload
    def estimate_cost(
        self,
        *,
        binder_specification: design_estimate_cost_params.ProteinDesignRunInputBinderSpecification,
        num_proteins: int,
        target: design_estimate_cost_params.ProteinDesignRunInputTarget,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        """
        Estimate the cost of a protein design run without creating any resource or
        consuming GPU.

        Args:
          binder_specification: Binder specification for protein design. Use no_template for sequence-defined
              binders, structure_template for uploaded binder structures, boltz_curated for
              Boltz-managed nanobody and antibody defaults, or
              uniformly_sampled_specifications to sample uniformly across multiple binder
              specifications.

          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          target: Target specification (structure template or template-free)

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def estimate_cost(
        self,
        *,
        binder: design_estimate_cost_params.BinderProteinDesignRunInputBinder,
        num_proteins: int,
        target: design_estimate_cost_params.BinderProteinDesignRunInputTarget,
        templates: Iterable[design_estimate_cost_params.BinderProteinDesignRunInputTemplate],
        type: Literal["binder"],
        global_design_filters: Iterable[design_estimate_cost_params.BinderProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        """
        Estimate the cost of a protein design run without creating any resource or
        consuming GPU.

        Args:
          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          target: Fixed target entities. Binding annotations are entity-local so repeated chain
              IDs across templates remain unambiguous.

          global_design_filters: Filters applied to every designed region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def estimate_cost(
        self,
        *,
        entities: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputEntity],
        num_proteins: int,
        templates: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputTemplate],
        type: Literal["generic"],
        bonds: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputBond] | Omit = omit,
        global_design_filters: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        """
        Estimate the cost of a protein design run without creating any resource or
        consuming GPU.

        Args:
          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          global_design_filters: Filters applied to every designed region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["binder_specification", "num_proteins", "target"],
        ["binder", "num_proteins", "target", "templates", "type"],
        ["entities", "num_proteins", "templates", "type"],
    )
    def estimate_cost(
        self,
        *,
        binder_specification: design_estimate_cost_params.ProteinDesignRunInputBinderSpecification | Omit = omit,
        num_proteins: int,
        target: design_estimate_cost_params.ProteinDesignRunInputTarget
        | design_estimate_cost_params.BinderProteinDesignRunInputTarget
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        binder: design_estimate_cost_params.BinderProteinDesignRunInputBinder | Omit = omit,
        templates: Iterable[design_estimate_cost_params.BinderProteinDesignRunInputTemplate]
        | Iterable[design_estimate_cost_params.GenericProteinDesignRunInputTemplate]
        | Omit = omit,
        type: Literal["binder"] | Literal["generic"] | Omit = omit,
        global_design_filters: Iterable[design_estimate_cost_params.BinderProteinDesignRunInputGlobalDesignFilter]
        | Iterable[design_estimate_cost_params.GenericProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        entities: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputEntity] | Omit = omit,
        bonds: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputBond] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        return self._post(
            "/compute/v1/protein/design/estimate-cost",
            body=maybe_transform(
                {
                    "binder_specification": binder_specification,
                    "num_proteins": num_proteins,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                    "binder": binder,
                    "templates": templates,
                    "type": type,
                    "global_design_filters": global_design_filters,
                    "entities": entities,
                    "bonds": bonds,
                },
                design_estimate_cost_params.DesignEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignEstimateCostResponse,
        )

    def list_curated_specifications(
        self,
        *,
        type: Literal["nanobody", "antibody"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignListCuratedSpecificationsResponse:
        """
        List binder-side protein design specifications from Boltz-managed curated
        nanobody or antibody libraries.

        Args:
          type: Curated binder library to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/compute/v1/protein/design/curated-specifications",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"type": type}, design_list_curated_specifications_params.DesignListCuratedSpecificationsParams
                ),
            ),
            cast_to=DesignListCuratedSpecificationsResponse,
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
        Retrieve paginated results from a protein design run

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
            path_template("/compute/v1/protein/design/{id}/results", id=id),
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
            model=cast(
                Any, DesignListResultsResponse
            ),  # Union types cannot be passed in as arguments in the type system
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
        Resume a stopped protein design run from its last checkpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/protein/design/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignResumeResponse,
        )

    @overload
    def start(
        self,
        *,
        binder_specification: design_start_params.ProteinDesignRunInputBinderSpecification,
        num_proteins: int,
        target: design_start_params.ProteinDesignRunInputTarget,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        """Create a binder or generic protein design run.

        Generic runs may include
        `fusion_protein` entities. The deprecated legacy binder request remains accepted
        during migration.

        Args:
          binder_specification: Binder specification for protein design. Use no_template for sequence-defined
              binders, structure_template for uploaded binder structures, boltz_curated for
              Boltz-managed nanobody and antibody defaults, or
              uniformly_sampled_specifications to sample uniformly across multiple binder
              specifications.

          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          target: Target specification (structure template or template-free)

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def start(
        self,
        *,
        binder: design_start_params.BinderProteinDesignRunInputBinder,
        num_proteins: int,
        target: design_start_params.BinderProteinDesignRunInputTarget,
        templates: Iterable[design_start_params.BinderProteinDesignRunInputTemplate],
        type: Literal["binder"],
        global_design_filters: Iterable[design_start_params.BinderProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        """Create a binder or generic protein design run.

        Generic runs may include
        `fusion_protein` entities. The deprecated legacy binder request remains accepted
        during migration.

        Args:
          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          target: Fixed target entities. Binding annotations are entity-local so repeated chain
              IDs across templates remain unambiguous.

          global_design_filters: Filters applied to every designed region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def start(
        self,
        *,
        entities: Iterable[design_start_params.GenericProteinDesignRunInputEntity],
        num_proteins: int,
        templates: Iterable[design_start_params.GenericProteinDesignRunInputTemplate],
        type: Literal["generic"],
        bonds: Iterable[design_start_params.GenericProteinDesignRunInputBond] | Omit = omit,
        global_design_filters: Iterable[design_start_params.GenericProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        """Create a binder or generic protein design run.

        Generic runs may include
        `fusion_protein` entities. The deprecated legacy binder request remains accepted
        during migration.

        Args:
          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          global_design_filters: Filters applied to every designed region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["binder_specification", "num_proteins", "target"],
        ["binder", "num_proteins", "target", "templates", "type"],
        ["entities", "num_proteins", "templates", "type"],
    )
    def start(
        self,
        *,
        binder_specification: design_start_params.ProteinDesignRunInputBinderSpecification | Omit = omit,
        num_proteins: int,
        target: design_start_params.ProteinDesignRunInputTarget
        | design_start_params.BinderProteinDesignRunInputTarget
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        binder: design_start_params.BinderProteinDesignRunInputBinder | Omit = omit,
        templates: Iterable[design_start_params.BinderProteinDesignRunInputTemplate]
        | Iterable[design_start_params.GenericProteinDesignRunInputTemplate]
        | Omit = omit,
        type: Literal["binder"] | Literal["generic"] | Omit = omit,
        global_design_filters: Iterable[design_start_params.BinderProteinDesignRunInputGlobalDesignFilter]
        | Iterable[design_start_params.GenericProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        entities: Iterable[design_start_params.GenericProteinDesignRunInputEntity] | Omit = omit,
        bonds: Iterable[design_start_params.GenericProteinDesignRunInputBond] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        return self._post(
            "/compute/v1/protein/design",
            body=maybe_transform(
                {
                    "binder_specification": binder_specification,
                    "num_proteins": num_proteins,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                    "binder": binder,
                    "templates": templates,
                    "type": type,
                    "global_design_filters": global_design_filters,
                    "entities": entities,
                    "bonds": bonds,
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
        Stop an in-progress protein design run early

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/protein/design/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignStopResponse,
        )


class AsyncDesignResource(AsyncAPIResource):
    """Generate binder or generic protein designs.

    New requests use the top-level type discriminator (`binder` or `generic`), while the legacy target plus binder_specification body remains accepted for migration. Binder requests can share one CIF across target and binder, sample uniformly across multiple specifications, or use Boltz-managed curated antibody and nanobody defaults. Results are discriminated by type: binder runs include binding metrics, while generic runs return structure and secondary-structure metrics only. A generic request can use a `fusion_protein` entity to concatenate two or more ordered fixed, designed, or template-backed protein segments into one output chain.
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
            path_template("/compute/v1/protein/design/{id}", id=id),
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
        List protein design runs, optionally filtered by workspace

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
            "/compute/v1/protein/design",
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
            path_template("/compute/v1/protein/design/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignDeleteDataResponse,
        )

    @overload
    async def estimate_cost(
        self,
        *,
        binder_specification: design_estimate_cost_params.ProteinDesignRunInputBinderSpecification,
        num_proteins: int,
        target: design_estimate_cost_params.ProteinDesignRunInputTarget,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        """
        Estimate the cost of a protein design run without creating any resource or
        consuming GPU.

        Args:
          binder_specification: Binder specification for protein design. Use no_template for sequence-defined
              binders, structure_template for uploaded binder structures, boltz_curated for
              Boltz-managed nanobody and antibody defaults, or
              uniformly_sampled_specifications to sample uniformly across multiple binder
              specifications.

          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          target: Target specification (structure template or template-free)

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def estimate_cost(
        self,
        *,
        binder: design_estimate_cost_params.BinderProteinDesignRunInputBinder,
        num_proteins: int,
        target: design_estimate_cost_params.BinderProteinDesignRunInputTarget,
        templates: Iterable[design_estimate_cost_params.BinderProteinDesignRunInputTemplate],
        type: Literal["binder"],
        global_design_filters: Iterable[design_estimate_cost_params.BinderProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        """
        Estimate the cost of a protein design run without creating any resource or
        consuming GPU.

        Args:
          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          target: Fixed target entities. Binding annotations are entity-local so repeated chain
              IDs across templates remain unambiguous.

          global_design_filters: Filters applied to every designed region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def estimate_cost(
        self,
        *,
        entities: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputEntity],
        num_proteins: int,
        templates: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputTemplate],
        type: Literal["generic"],
        bonds: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputBond] | Omit = omit,
        global_design_filters: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        """
        Estimate the cost of a protein design run without creating any resource or
        consuming GPU.

        Args:
          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          global_design_filters: Filters applied to every designed region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["binder_specification", "num_proteins", "target"],
        ["binder", "num_proteins", "target", "templates", "type"],
        ["entities", "num_proteins", "templates", "type"],
    )
    async def estimate_cost(
        self,
        *,
        binder_specification: design_estimate_cost_params.ProteinDesignRunInputBinderSpecification | Omit = omit,
        num_proteins: int,
        target: design_estimate_cost_params.ProteinDesignRunInputTarget
        | design_estimate_cost_params.BinderProteinDesignRunInputTarget
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        binder: design_estimate_cost_params.BinderProteinDesignRunInputBinder | Omit = omit,
        templates: Iterable[design_estimate_cost_params.BinderProteinDesignRunInputTemplate]
        | Iterable[design_estimate_cost_params.GenericProteinDesignRunInputTemplate]
        | Omit = omit,
        type: Literal["binder"] | Literal["generic"] | Omit = omit,
        global_design_filters: Iterable[design_estimate_cost_params.BinderProteinDesignRunInputGlobalDesignFilter]
        | Iterable[design_estimate_cost_params.GenericProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        entities: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputEntity] | Omit = omit,
        bonds: Iterable[design_estimate_cost_params.GenericProteinDesignRunInputBond] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignEstimateCostResponse:
        return await self._post(
            "/compute/v1/protein/design/estimate-cost",
            body=await async_maybe_transform(
                {
                    "binder_specification": binder_specification,
                    "num_proteins": num_proteins,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                    "binder": binder,
                    "templates": templates,
                    "type": type,
                    "global_design_filters": global_design_filters,
                    "entities": entities,
                    "bonds": bonds,
                },
                design_estimate_cost_params.DesignEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignEstimateCostResponse,
        )

    async def list_curated_specifications(
        self,
        *,
        type: Literal["nanobody", "antibody"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignListCuratedSpecificationsResponse:
        """
        List binder-side protein design specifications from Boltz-managed curated
        nanobody or antibody libraries.

        Args:
          type: Curated binder library to retrieve.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/compute/v1/protein/design/curated-specifications",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"type": type}, design_list_curated_specifications_params.DesignListCuratedSpecificationsParams
                ),
            ),
            cast_to=DesignListCuratedSpecificationsResponse,
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
        Retrieve paginated results from a protein design run

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
            path_template("/compute/v1/protein/design/{id}/results", id=id),
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
            model=cast(
                Any, DesignListResultsResponse
            ),  # Union types cannot be passed in as arguments in the type system
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
        Resume a stopped protein design run from its last checkpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/protein/design/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DesignResumeResponse,
        )

    @overload
    async def start(
        self,
        *,
        binder_specification: design_start_params.ProteinDesignRunInputBinderSpecification,
        num_proteins: int,
        target: design_start_params.ProteinDesignRunInputTarget,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        """Create a binder or generic protein design run.

        Generic runs may include
        `fusion_protein` entities. The deprecated legacy binder request remains accepted
        during migration.

        Args:
          binder_specification: Binder specification for protein design. Use no_template for sequence-defined
              binders, structure_template for uploaded binder structures, boltz_curated for
              Boltz-managed nanobody and antibody defaults, or
              uniformly_sampled_specifications to sample uniformly across multiple binder
              specifications.

          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          target: Target specification (structure template or template-free)

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def start(
        self,
        *,
        binder: design_start_params.BinderProteinDesignRunInputBinder,
        num_proteins: int,
        target: design_start_params.BinderProteinDesignRunInputTarget,
        templates: Iterable[design_start_params.BinderProteinDesignRunInputTemplate],
        type: Literal["binder"],
        global_design_filters: Iterable[design_start_params.BinderProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        """Create a binder or generic protein design run.

        Generic runs may include
        `fusion_protein` entities. The deprecated legacy binder request remains accepted
        during migration.

        Args:
          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          target: Fixed target entities. Binding annotations are entity-local so repeated chain
              IDs across templates remain unambiguous.

          global_design_filters: Filters applied to every designed region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def start(
        self,
        *,
        entities: Iterable[design_start_params.GenericProteinDesignRunInputEntity],
        num_proteins: int,
        templates: Iterable[design_start_params.GenericProteinDesignRunInputTemplate],
        type: Literal["generic"],
        bonds: Iterable[design_start_params.GenericProteinDesignRunInputBond] | Omit = omit,
        global_design_filters: Iterable[design_start_params.GenericProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        """Create a binder or generic protein design run.

        Generic runs may include
        `fusion_protein` entities. The deprecated legacy binder request remains accepted
        during migration.

        Args:
          num_proteins: Number of protein designs to generate. Must be between 10 and 1,000,000.

          global_design_filters: Filters applied to every designed region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["binder_specification", "num_proteins", "target"],
        ["binder", "num_proteins", "target", "templates", "type"],
        ["entities", "num_proteins", "templates", "type"],
    )
    async def start(
        self,
        *,
        binder_specification: design_start_params.ProteinDesignRunInputBinderSpecification | Omit = omit,
        num_proteins: int,
        target: design_start_params.ProteinDesignRunInputTarget
        | design_start_params.BinderProteinDesignRunInputTarget
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        binder: design_start_params.BinderProteinDesignRunInputBinder | Omit = omit,
        templates: Iterable[design_start_params.BinderProteinDesignRunInputTemplate]
        | Iterable[design_start_params.GenericProteinDesignRunInputTemplate]
        | Omit = omit,
        type: Literal["binder"] | Literal["generic"] | Omit = omit,
        global_design_filters: Iterable[design_start_params.BinderProteinDesignRunInputGlobalDesignFilter]
        | Iterable[design_start_params.GenericProteinDesignRunInputGlobalDesignFilter]
        | Omit = omit,
        entities: Iterable[design_start_params.GenericProteinDesignRunInputEntity] | Omit = omit,
        bonds: Iterable[design_start_params.GenericProteinDesignRunInputBond] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DesignStartResponse:
        return await self._post(
            "/compute/v1/protein/design",
            body=await async_maybe_transform(
                {
                    "binder_specification": binder_specification,
                    "num_proteins": num_proteins,
                    "target": target,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                    "binder": binder,
                    "templates": templates,
                    "type": type,
                    "global_design_filters": global_design_filters,
                    "entities": entities,
                    "bonds": bonds,
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
        Stop an in-progress protein design run early

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/protein/design/{id}/stop", id=id),
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
        self.list_curated_specifications = to_raw_response_wrapper(
            design.list_curated_specifications,
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
        self.list_curated_specifications = async_to_raw_response_wrapper(
            design.list_curated_specifications,
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
        self.list_curated_specifications = to_streamed_response_wrapper(
            design.list_curated_specifications,
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
        self.list_curated_specifications = async_to_streamed_response_wrapper(
            design.list_curated_specifications,
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
