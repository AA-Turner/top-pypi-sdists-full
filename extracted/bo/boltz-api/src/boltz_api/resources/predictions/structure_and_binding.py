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
from ...types.predictions import (
    structure_and_binding_list_params,
    structure_and_binding_start_params,
    structure_and_binding_retrieve_params,
    structure_and_binding_estimate_cost_params,
)
from ...types.predictions.structure_and_binding_list_response import StructureAndBindingListResponse
from ...types.predictions.structure_and_binding_start_response import StructureAndBindingStartResponse
from ...types.predictions.structure_and_binding_retrieve_response import StructureAndBindingRetrieveResponse
from ...types.predictions.structure_and_binding_delete_data_response import StructureAndBindingDeleteDataResponse
from ...types.predictions.structure_and_binding_estimate_cost_response import StructureAndBindingEstimateCostResponse

# <boltz-api-custom-code>
if _t.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path
# </boltz-api-custom-code>
__all__ = ["StructureAndBindingResource", "AsyncStructureAndBindingResource"]


class StructureAndBindingResource(SyncAPIResource):
    """
    Predict 3D structure coordinates, per-residue confidence scores, and binding metrics for a molecular complex. Supports explicit glycan graphs and covalent attachments, optional template-guided folding, and per-protein MSA control.
    """

    # <boltz-api-custom-code>
    if _t.TYPE_CHECKING:

        def run(
            self,
            *,
            input: structure_and_binding_start_params.Input,
            model: Literal["boltz-2.1"],
            root_dir: str | PathLike[str] = "boltz-experiments",
            name: str | None = None,
            workspace_id: str | Omit = omit,
            quiet: bool = False,
            poll_interval_seconds: float = 5.0,
        ) -> Path: ...
    # </boltz-api-custom-code>

    @cached_property
    def with_raw_response(self) -> StructureAndBindingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return StructureAndBindingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> StructureAndBindingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return StructureAndBindingResourceWithStreamingResponse(self)

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
    ) -> StructureAndBindingRetrieveResponse:
        """
        Retrieve a prediction by ID, including its status and results.

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
            path_template("/compute/v1/predictions/structure-and-binding/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"workspace_id": workspace_id},
                    structure_and_binding_retrieve_params.StructureAndBindingRetrieveParams,
                ),
            ),
            cast_to=StructureAndBindingRetrieveResponse,
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
    ) -> SyncCursorPage[StructureAndBindingListResponse]:
        """
        List structure and binding predictions, optionally filtered by workspace

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
            "/compute/v1/predictions/structure-and-binding",
            page=SyncCursorPage[StructureAndBindingListResponse],
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
                    structure_and_binding_list_params.StructureAndBindingListParams,
                ),
            ),
            model=StructureAndBindingListResponse,
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
    ) -> StructureAndBindingDeleteDataResponse:
        """
        Permanently delete the input, output, and result data associated with this
        prediction. The prediction record itself is retained with a `data_deleted_at`
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
            path_template("/compute/v1/predictions/structure-and-binding/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StructureAndBindingDeleteDataResponse,
        )

    def estimate_cost(
        self,
        *,
        input: structure_and_binding_estimate_cost_params.Input,
        model: Literal["boltz-2.1"],
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StructureAndBindingEstimateCostResponse:
        """
        Estimate the cost of a prediction without creating any resource or consuming
        GPU.

        Args:
          model: Model to use for prediction

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/compute/v1/predictions/structure-and-binding/estimate-cost",
            body=maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                structure_and_binding_estimate_cost_params.StructureAndBindingEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StructureAndBindingEstimateCostResponse,
        )

    def start(
        self,
        *,
        input: structure_and_binding_start_params.Input,
        model: Literal["boltz-2.1"],
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StructureAndBindingStartResponse:
        """
        Submit a prediction job that produces 3D structure coordinates and confidence
        scores for the input molecular complex, with optional binding metrics. Protein
        entities can use automatic MSA generation, custom A3M/CSV MSAs, or empty MSA
        mode. Boltz-2.1 predictions can also include up to 4 CIF or PDB templates to
        guide protein-chain geometry.

        Args:
          model: Model to use for prediction

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/compute/v1/predictions/structure-and-binding",
            body=maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                structure_and_binding_start_params.StructureAndBindingStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StructureAndBindingStartResponse,
        )


class AsyncStructureAndBindingResource(AsyncAPIResource):
    """
    Predict 3D structure coordinates, per-residue confidence scores, and binding metrics for a molecular complex. Supports explicit glycan graphs and covalent attachments, optional template-guided folding, and per-protein MSA control.
    """

    @cached_property
    def with_raw_response(self) -> AsyncStructureAndBindingResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncStructureAndBindingResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncStructureAndBindingResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncStructureAndBindingResourceWithStreamingResponse(self)

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
    ) -> StructureAndBindingRetrieveResponse:
        """
        Retrieve a prediction by ID, including its status and results.

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
            path_template("/compute/v1/predictions/structure-and-binding/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"workspace_id": workspace_id},
                    structure_and_binding_retrieve_params.StructureAndBindingRetrieveParams,
                ),
            ),
            cast_to=StructureAndBindingRetrieveResponse,
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
    ) -> AsyncPaginator[StructureAndBindingListResponse, AsyncCursorPage[StructureAndBindingListResponse]]:
        """
        List structure and binding predictions, optionally filtered by workspace

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
            "/compute/v1/predictions/structure-and-binding",
            page=AsyncCursorPage[StructureAndBindingListResponse],
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
                    structure_and_binding_list_params.StructureAndBindingListParams,
                ),
            ),
            model=StructureAndBindingListResponse,
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
    ) -> StructureAndBindingDeleteDataResponse:
        """
        Permanently delete the input, output, and result data associated with this
        prediction. The prediction record itself is retained with a `data_deleted_at`
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
            path_template("/compute/v1/predictions/structure-and-binding/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StructureAndBindingDeleteDataResponse,
        )

    async def estimate_cost(
        self,
        *,
        input: structure_and_binding_estimate_cost_params.Input,
        model: Literal["boltz-2.1"],
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StructureAndBindingEstimateCostResponse:
        """
        Estimate the cost of a prediction without creating any resource or consuming
        GPU.

        Args:
          model: Model to use for prediction

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/compute/v1/predictions/structure-and-binding/estimate-cost",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                structure_and_binding_estimate_cost_params.StructureAndBindingEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StructureAndBindingEstimateCostResponse,
        )

    async def start(
        self,
        *,
        input: structure_and_binding_start_params.Input,
        model: Literal["boltz-2.1"],
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> StructureAndBindingStartResponse:
        """
        Submit a prediction job that produces 3D structure coordinates and confidence
        scores for the input molecular complex, with optional binding metrics. Protein
        entities can use automatic MSA generation, custom A3M/CSV MSAs, or empty MSA
        mode. Boltz-2.1 predictions can also include up to 4 CIF or PDB templates to
        guide protein-chain geometry.

        Args:
          model: Model to use for prediction

          idempotency_key: Client-provided key to prevent duplicate submissions on retries

          workspace_id: Target workspace ID (admin keys only; ignored for workspace keys)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/compute/v1/predictions/structure-and-binding",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                structure_and_binding_start_params.StructureAndBindingStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StructureAndBindingStartResponse,
        )


class StructureAndBindingResourceWithRawResponse:
    def __init__(self, structure_and_binding: StructureAndBindingResource) -> None:
        self._structure_and_binding = structure_and_binding

        self.retrieve = to_raw_response_wrapper(
            structure_and_binding.retrieve,
        )
        self.list = to_raw_response_wrapper(
            structure_and_binding.list,
        )
        self.delete_data = to_raw_response_wrapper(
            structure_and_binding.delete_data,
        )
        self.estimate_cost = to_raw_response_wrapper(
            structure_and_binding.estimate_cost,
        )
        self.start = to_raw_response_wrapper(
            structure_and_binding.start,
        )


class AsyncStructureAndBindingResourceWithRawResponse:
    def __init__(self, structure_and_binding: AsyncStructureAndBindingResource) -> None:
        self._structure_and_binding = structure_and_binding

        self.retrieve = async_to_raw_response_wrapper(
            structure_and_binding.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            structure_and_binding.list,
        )
        self.delete_data = async_to_raw_response_wrapper(
            structure_and_binding.delete_data,
        )
        self.estimate_cost = async_to_raw_response_wrapper(
            structure_and_binding.estimate_cost,
        )
        self.start = async_to_raw_response_wrapper(
            structure_and_binding.start,
        )


class StructureAndBindingResourceWithStreamingResponse:
    def __init__(self, structure_and_binding: StructureAndBindingResource) -> None:
        self._structure_and_binding = structure_and_binding

        self.retrieve = to_streamed_response_wrapper(
            structure_and_binding.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            structure_and_binding.list,
        )
        self.delete_data = to_streamed_response_wrapper(
            structure_and_binding.delete_data,
        )
        self.estimate_cost = to_streamed_response_wrapper(
            structure_and_binding.estimate_cost,
        )
        self.start = to_streamed_response_wrapper(
            structure_and_binding.start,
        )


class AsyncStructureAndBindingResourceWithStreamingResponse:
    def __init__(self, structure_and_binding: AsyncStructureAndBindingResource) -> None:
        self._structure_and_binding = structure_and_binding

        self.retrieve = async_to_streamed_response_wrapper(
            structure_and_binding.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            structure_and_binding.list,
        )
        self.delete_data = async_to_streamed_response_wrapper(
            structure_and_binding.delete_data,
        )
        self.estimate_cost = async_to_streamed_response_wrapper(
            structure_and_binding.estimate_cost,
        )
        self.start = async_to_streamed_response_wrapper(
            structure_and_binding.start,
        )
