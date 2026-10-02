# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
    sequence_redesign_list_params,
    sequence_redesign_start_params,
    sequence_redesign_retrieve_params,
    sequence_redesign_list_results_params,
    sequence_redesign_estimate_cost_params,
)
from ...types.protein.sequence_redesign_list_response import SequenceRedesignListResponse
from ...types.protein.sequence_redesign_stop_response import SequenceRedesignStopResponse
from ...types.protein.sequence_redesign_start_response import SequenceRedesignStartResponse
from ...types.protein.sequence_redesign_resume_response import SequenceRedesignResumeResponse
from ...types.protein.sequence_redesign_retrieve_response import SequenceRedesignRetrieveResponse
from ...types.protein.sequence_redesign_delete_data_response import SequenceRedesignDeleteDataResponse
from ...types.protein.sequence_redesign_list_results_response import SequenceRedesignListResultsResponse
from ...types.protein.sequence_redesign_estimate_cost_response import SequenceRedesignEstimateCostResponse

__all__ = ["SequenceRedesignResource", "AsyncSequenceRedesignResource"]


class SequenceRedesignResource(SyncAPIResource):
    """Redesign selected protein residues in one fixed CIF structure.

    Use the top-level type discriminator to choose binder redesign, with target and binder chain roles, or generic redesign. Every chain in the input structure must be assigned exactly once. Binder results include binding and structure metrics; generic results include structure and secondary-structure metrics.
    """

    @cached_property
    def with_raw_response(self) -> SequenceRedesignResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return SequenceRedesignResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SequenceRedesignResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return SequenceRedesignResourceWithStreamingResponse(self)

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
    ) -> SequenceRedesignRetrieveResponse:
        """
        Retrieve a sequence redesign run by ID, including progress and status

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
            path_template("/compute/v1/protein/sequence-redesign/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"workspace_id": workspace_id}, sequence_redesign_retrieve_params.SequenceRedesignRetrieveParams
                ),
            ),
            cast_to=SequenceRedesignRetrieveResponse,
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
    ) -> SyncCursorPage[SequenceRedesignListResponse]:
        """
        List protein sequence redesign runs, optionally filtered by workspace

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
            "/compute/v1/protein/sequence-redesign",
            page=SyncCursorPage[SequenceRedesignListResponse],
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
                    sequence_redesign_list_params.SequenceRedesignListParams,
                ),
            ),
            model=SequenceRedesignListResponse,
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
    ) -> SequenceRedesignDeleteDataResponse:
        """
        Permanently delete the input, output, and result data associated with this
        sequence redesign run. The sequence redesign run record itself is retained with
        a `data_deleted_at` timestamp. This action is irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/protein/sequence-redesign/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignDeleteDataResponse,
        )

    @overload
    def estimate_cost(
        self,
        *,
        entities: Iterable[sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputStructure,
        type: Literal["binder"],
        global_design_filters: Iterable[
            sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignEstimateCostResponse:
        """
        Estimate the cost of a protein sequence redesign run without creating any
        resource or consuming GPU.

        Args:
          entities: Every chain in the input CIF, assigned exactly once as target or binder.

          num_proteins: Number of unique filter-passing redesigned proteins to generate.

          structure: How to provide a CIF structure file. URLs are auto-detected; base64 uploads must
              use chemical/x-cif media type.

          global_design_filters: Filters applied to every redesigned region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Workspace to run this redesign in.

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
        entities: Iterable[sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputStructure,
        type: Literal["generic"],
        global_design_filters: Iterable[
            sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignEstimateCostResponse:
        """
        Estimate the cost of a protein sequence redesign run without creating any
        resource or consuming GPU.

        Args:
          entities: Every chain in the input CIF, assigned exactly once.

          num_proteins: Number of unique filter-passing redesigned proteins to generate.

          structure: How to provide a CIF structure file. URLs are auto-detected; base64 uploads must
              use chemical/x-cif media type.

          global_design_filters: Filters applied to every redesigned region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Workspace to run this redesign in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["entities", "num_proteins", "structure", "type"])
    def estimate_cost(
        self,
        *,
        entities: Iterable[sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputEntity]
        | Iterable[sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputStructure
        | sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputStructure,
        type: Literal["binder"] | Literal["generic"],
        global_design_filters: Iterable[
            sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Iterable[sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignEstimateCostResponse:
        return self._post(
            "/compute/v1/protein/sequence-redesign/estimate-cost",
            body=maybe_transform(
                {
                    "entities": entities,
                    "num_proteins": num_proteins,
                    "structure": structure,
                    "type": type,
                    "global_design_filters": global_design_filters,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                sequence_redesign_estimate_cost_params.SequenceRedesignEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignEstimateCostResponse,
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
    ) -> SyncCursorPage[SequenceRedesignListResultsResponse]:
        """
        Retrieve paginated results from a protein sequence redesign run

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
            path_template("/compute/v1/protein/sequence-redesign/{id}/results", id=id),
            page=SyncCursorPage[SequenceRedesignListResultsResponse],
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
                    sequence_redesign_list_results_params.SequenceRedesignListResultsParams,
                ),
            ),
            model=cast(
                Any, SequenceRedesignListResultsResponse
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
    ) -> SequenceRedesignResumeResponse:
        """
        Resume a stopped protein sequence redesign run from its last checkpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/protein/sequence-redesign/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignResumeResponse,
        )

    @overload
    def start(
        self,
        *,
        entities: Iterable[sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputStructure,
        type: Literal["binder"],
        global_design_filters: Iterable[
            sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignStartResponse:
        """
        Create a protein sequence redesign run from selected residues in a fixed input
        structure

        Args:
          entities: Every chain in the input CIF, assigned exactly once as target or binder.

          num_proteins: Number of unique filter-passing redesigned proteins to generate.

          structure: How to provide a CIF structure file. URLs are auto-detected; base64 uploads must
              use chemical/x-cif media type.

          global_design_filters: Filters applied to every redesigned region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Workspace to run this redesign in.

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
        entities: Iterable[sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputStructure,
        type: Literal["generic"],
        global_design_filters: Iterable[
            sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignStartResponse:
        """
        Create a protein sequence redesign run from selected residues in a fixed input
        structure

        Args:
          entities: Every chain in the input CIF, assigned exactly once.

          num_proteins: Number of unique filter-passing redesigned proteins to generate.

          structure: How to provide a CIF structure file. URLs are auto-detected; base64 uploads must
              use chemical/x-cif media type.

          global_design_filters: Filters applied to every redesigned region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Workspace to run this redesign in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["entities", "num_proteins", "structure", "type"])
    def start(
        self,
        *,
        entities: Iterable[sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputEntity]
        | Iterable[sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputStructure
        | sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputStructure,
        type: Literal["binder"] | Literal["generic"],
        global_design_filters: Iterable[
            sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Iterable[sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignStartResponse:
        return self._post(
            "/compute/v1/protein/sequence-redesign",
            body=maybe_transform(
                {
                    "entities": entities,
                    "num_proteins": num_proteins,
                    "structure": structure,
                    "type": type,
                    "global_design_filters": global_design_filters,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                sequence_redesign_start_params.SequenceRedesignStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignStartResponse,
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
    ) -> SequenceRedesignStopResponse:
        """
        Stop an in-progress protein sequence redesign run early

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/compute/v1/protein/sequence-redesign/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignStopResponse,
        )


class AsyncSequenceRedesignResource(AsyncAPIResource):
    """Redesign selected protein residues in one fixed CIF structure.

    Use the top-level type discriminator to choose binder redesign, with target and binder chain roles, or generic redesign. Every chain in the input structure must be assigned exactly once. Binder results include binding and structure metrics; generic results include structure and secondary-structure metrics.
    """

    @cached_property
    def with_raw_response(self) -> AsyncSequenceRedesignResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSequenceRedesignResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSequenceRedesignResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncSequenceRedesignResourceWithStreamingResponse(self)

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
    ) -> SequenceRedesignRetrieveResponse:
        """
        Retrieve a sequence redesign run by ID, including progress and status

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
            path_template("/compute/v1/protein/sequence-redesign/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"workspace_id": workspace_id}, sequence_redesign_retrieve_params.SequenceRedesignRetrieveParams
                ),
            ),
            cast_to=SequenceRedesignRetrieveResponse,
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
    ) -> AsyncPaginator[SequenceRedesignListResponse, AsyncCursorPage[SequenceRedesignListResponse]]:
        """
        List protein sequence redesign runs, optionally filtered by workspace

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
            "/compute/v1/protein/sequence-redesign",
            page=AsyncCursorPage[SequenceRedesignListResponse],
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
                    sequence_redesign_list_params.SequenceRedesignListParams,
                ),
            ),
            model=SequenceRedesignListResponse,
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
    ) -> SequenceRedesignDeleteDataResponse:
        """
        Permanently delete the input, output, and result data associated with this
        sequence redesign run. The sequence redesign run record itself is retained with
        a `data_deleted_at` timestamp. This action is irreversible.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/protein/sequence-redesign/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignDeleteDataResponse,
        )

    @overload
    async def estimate_cost(
        self,
        *,
        entities: Iterable[sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputStructure,
        type: Literal["binder"],
        global_design_filters: Iterable[
            sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignEstimateCostResponse:
        """
        Estimate the cost of a protein sequence redesign run without creating any
        resource or consuming GPU.

        Args:
          entities: Every chain in the input CIF, assigned exactly once as target or binder.

          num_proteins: Number of unique filter-passing redesigned proteins to generate.

          structure: How to provide a CIF structure file. URLs are auto-detected; base64 uploads must
              use chemical/x-cif media type.

          global_design_filters: Filters applied to every redesigned region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Workspace to run this redesign in.

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
        entities: Iterable[sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputStructure,
        type: Literal["generic"],
        global_design_filters: Iterable[
            sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignEstimateCostResponse:
        """
        Estimate the cost of a protein sequence redesign run without creating any
        resource or consuming GPU.

        Args:
          entities: Every chain in the input CIF, assigned exactly once.

          num_proteins: Number of unique filter-passing redesigned proteins to generate.

          structure: How to provide a CIF structure file. URLs are auto-detected; base64 uploads must
              use chemical/x-cif media type.

          global_design_filters: Filters applied to every redesigned region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Workspace to run this redesign in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["entities", "num_proteins", "structure", "type"])
    async def estimate_cost(
        self,
        *,
        entities: Iterable[sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputEntity]
        | Iterable[sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputStructure
        | sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputStructure,
        type: Literal["binder"] | Literal["generic"],
        global_design_filters: Iterable[
            sequence_redesign_estimate_cost_params.BinderProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Iterable[sequence_redesign_estimate_cost_params.GenericProteinSequenceRedesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignEstimateCostResponse:
        return await self._post(
            "/compute/v1/protein/sequence-redesign/estimate-cost",
            body=await async_maybe_transform(
                {
                    "entities": entities,
                    "num_proteins": num_proteins,
                    "structure": structure,
                    "type": type,
                    "global_design_filters": global_design_filters,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                sequence_redesign_estimate_cost_params.SequenceRedesignEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignEstimateCostResponse,
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
    ) -> AsyncPaginator[SequenceRedesignListResultsResponse, AsyncCursorPage[SequenceRedesignListResultsResponse]]:
        """
        Retrieve paginated results from a protein sequence redesign run

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
            path_template("/compute/v1/protein/sequence-redesign/{id}/results", id=id),
            page=AsyncCursorPage[SequenceRedesignListResultsResponse],
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
                    sequence_redesign_list_results_params.SequenceRedesignListResultsParams,
                ),
            ),
            model=cast(
                Any, SequenceRedesignListResultsResponse
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
    ) -> SequenceRedesignResumeResponse:
        """
        Resume a stopped protein sequence redesign run from its last checkpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/protein/sequence-redesign/{id}/resume", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignResumeResponse,
        )

    @overload
    async def start(
        self,
        *,
        entities: Iterable[sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputStructure,
        type: Literal["binder"],
        global_design_filters: Iterable[
            sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignStartResponse:
        """
        Create a protein sequence redesign run from selected residues in a fixed input
        structure

        Args:
          entities: Every chain in the input CIF, assigned exactly once as target or binder.

          num_proteins: Number of unique filter-passing redesigned proteins to generate.

          structure: How to provide a CIF structure file. URLs are auto-detected; base64 uploads must
              use chemical/x-cif media type.

          global_design_filters: Filters applied to every redesigned region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Workspace to run this redesign in.

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
        entities: Iterable[sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputStructure,
        type: Literal["generic"],
        global_design_filters: Iterable[
            sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignStartResponse:
        """
        Create a protein sequence redesign run from selected residues in a fixed input
        structure

        Args:
          entities: Every chain in the input CIF, assigned exactly once.

          num_proteins: Number of unique filter-passing redesigned proteins to generate.

          structure: How to provide a CIF structure file. URLs are auto-detected; base64 uploads must
              use chemical/x-cif media type.

          global_design_filters: Filters applied to every redesigned region. When omitted, cysteine is excluded.
              Pass [] to disable global filters.

          workspace_id: Workspace to run this redesign in.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["entities", "num_proteins", "structure", "type"])
    async def start(
        self,
        *,
        entities: Iterable[sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputEntity]
        | Iterable[sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputEntity],
        num_proteins: int,
        structure: sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputStructure
        | sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputStructure,
        type: Literal["binder"] | Literal["generic"],
        global_design_filters: Iterable[
            sequence_redesign_start_params.BinderProteinSequenceRedesignRunInputGlobalDesignFilter
        ]
        | Iterable[sequence_redesign_start_params.GenericProteinSequenceRedesignRunInputGlobalDesignFilter]
        | Omit = omit,
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SequenceRedesignStartResponse:
        return await self._post(
            "/compute/v1/protein/sequence-redesign",
            body=await async_maybe_transform(
                {
                    "entities": entities,
                    "num_proteins": num_proteins,
                    "structure": structure,
                    "type": type,
                    "global_design_filters": global_design_filters,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                sequence_redesign_start_params.SequenceRedesignStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignStartResponse,
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
    ) -> SequenceRedesignStopResponse:
        """
        Stop an in-progress protein sequence redesign run early

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/compute/v1/protein/sequence-redesign/{id}/stop", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SequenceRedesignStopResponse,
        )


class SequenceRedesignResourceWithRawResponse:
    def __init__(self, sequence_redesign: SequenceRedesignResource) -> None:
        self._sequence_redesign = sequence_redesign

        self.retrieve = to_raw_response_wrapper(
            sequence_redesign.retrieve,
        )
        self.list = to_raw_response_wrapper(
            sequence_redesign.list,
        )
        self.delete_data = to_raw_response_wrapper(
            sequence_redesign.delete_data,
        )
        self.estimate_cost = to_raw_response_wrapper(
            sequence_redesign.estimate_cost,
        )
        self.list_results = to_raw_response_wrapper(
            sequence_redesign.list_results,
        )
        self.resume = to_raw_response_wrapper(
            sequence_redesign.resume,
        )
        self.start = to_raw_response_wrapper(
            sequence_redesign.start,
        )
        self.stop = to_raw_response_wrapper(
            sequence_redesign.stop,
        )


class AsyncSequenceRedesignResourceWithRawResponse:
    def __init__(self, sequence_redesign: AsyncSequenceRedesignResource) -> None:
        self._sequence_redesign = sequence_redesign

        self.retrieve = async_to_raw_response_wrapper(
            sequence_redesign.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            sequence_redesign.list,
        )
        self.delete_data = async_to_raw_response_wrapper(
            sequence_redesign.delete_data,
        )
        self.estimate_cost = async_to_raw_response_wrapper(
            sequence_redesign.estimate_cost,
        )
        self.list_results = async_to_raw_response_wrapper(
            sequence_redesign.list_results,
        )
        self.resume = async_to_raw_response_wrapper(
            sequence_redesign.resume,
        )
        self.start = async_to_raw_response_wrapper(
            sequence_redesign.start,
        )
        self.stop = async_to_raw_response_wrapper(
            sequence_redesign.stop,
        )


class SequenceRedesignResourceWithStreamingResponse:
    def __init__(self, sequence_redesign: SequenceRedesignResource) -> None:
        self._sequence_redesign = sequence_redesign

        self.retrieve = to_streamed_response_wrapper(
            sequence_redesign.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            sequence_redesign.list,
        )
        self.delete_data = to_streamed_response_wrapper(
            sequence_redesign.delete_data,
        )
        self.estimate_cost = to_streamed_response_wrapper(
            sequence_redesign.estimate_cost,
        )
        self.list_results = to_streamed_response_wrapper(
            sequence_redesign.list_results,
        )
        self.resume = to_streamed_response_wrapper(
            sequence_redesign.resume,
        )
        self.start = to_streamed_response_wrapper(
            sequence_redesign.start,
        )
        self.stop = to_streamed_response_wrapper(
            sequence_redesign.stop,
        )


class AsyncSequenceRedesignResourceWithStreamingResponse:
    def __init__(self, sequence_redesign: AsyncSequenceRedesignResource) -> None:
        self._sequence_redesign = sequence_redesign

        self.retrieve = async_to_streamed_response_wrapper(
            sequence_redesign.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            sequence_redesign.list,
        )
        self.delete_data = async_to_streamed_response_wrapper(
            sequence_redesign.delete_data,
        )
        self.estimate_cost = async_to_streamed_response_wrapper(
            sequence_redesign.estimate_cost,
        )
        self.list_results = async_to_streamed_response_wrapper(
            sequence_redesign.list_results,
        )
        self.resume = async_to_streamed_response_wrapper(
            sequence_redesign.resume,
        )
        self.start = async_to_streamed_response_wrapper(
            sequence_redesign.start,
        )
        self.stop = async_to_streamed_response_wrapper(
            sequence_redesign.stop,
        )
