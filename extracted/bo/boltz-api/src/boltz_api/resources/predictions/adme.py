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
from ...types.predictions import adme_list_params, adme_start_params, adme_retrieve_params, adme_estimate_cost_params
from ...types.predictions.adme_list_response import AdmeListResponse
from ...types.predictions.adme_start_response import AdmeStartResponse
from ...types.predictions.adme_retrieve_response import AdmeRetrieveResponse
from ...types.predictions.adme_delete_data_response import AdmeDeleteDataResponse
from ...types.predictions.adme_estimate_cost_response import AdmeEstimateCostResponse

# <boltz-api-custom-code>
if _t.TYPE_CHECKING:
    from os import PathLike
    from pathlib import Path
# </boltz-api-custom-code>
__all__ = ["AdmeResource", "AsyncAdmeResource"]


class AdmeResource(SyncAPIResource):
    """
    Predict Tier 1 ADME summary values for a batch of small molecules specified by SMILES.
    """

    # <boltz-api-custom-code>
    if _t.TYPE_CHECKING:

        def run(
            self,
            *,
            input: adme_start_params.Input,
            model: Literal["adme-v1"],
            root_dir: str | PathLike[str] = "boltz-experiments",
            name: str | None = None,
            workspace_id: str | Omit = omit,
            quiet: bool = False,
            poll_interval_seconds: float = 5.0,
        ) -> Path: ...
    # </boltz-api-custom-code>

    @cached_property
    def with_raw_response(self) -> AdmeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AdmeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AdmeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AdmeResourceWithStreamingResponse(self)

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
    ) -> AdmeRetrieveResponse:
        """
        Retrieve an ADME prediction by ID, including its status and results.

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
            path_template("/compute/v1/predictions/adme/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"workspace_id": workspace_id}, adme_retrieve_params.AdmeRetrieveParams),
            ),
            cast_to=AdmeRetrieveResponse,
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
    ) -> SyncCursorPage[AdmeListResponse]:
        """
        List ADME predictions, optionally filtered by workspace

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
            "/compute/v1/predictions/adme",
            page=SyncCursorPage[AdmeListResponse],
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
                    adme_list_params.AdmeListParams,
                ),
            ),
            model=AdmeListResponse,
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
    ) -> AdmeDeleteDataResponse:
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
            path_template("/compute/v1/predictions/adme/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdmeDeleteDataResponse,
        )

    def estimate_cost(
        self,
        *,
        input: adme_estimate_cost_params.Input,
        model: Literal["adme-v1"],
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AdmeEstimateCostResponse:
        """
        Estimate the cost of an ADME prediction without creating any resource or
        consuming GPU.

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
            "/compute/v1/predictions/adme/estimate-cost",
            body=maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                adme_estimate_cost_params.AdmeEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdmeEstimateCostResponse,
        )

    def start(
        self,
        *,
        input: adme_start_params.Input,
        model: Literal["adme-v1"],
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AdmeStartResponse:
        """
        Submit a prediction job that returns Tier 1 ADME summary values for each
        requested molecule.

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
            "/compute/v1/predictions/adme",
            body=maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                adme_start_params.AdmeStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdmeStartResponse,
        )


class AsyncAdmeResource(AsyncAPIResource):
    """
    Predict Tier 1 ADME summary values for a batch of small molecules specified by SMILES.
    """

    @cached_property
    def with_raw_response(self) -> AsyncAdmeResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAdmeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAdmeResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/boltz-bio/boltz-api-python#with_streaming_response
        """
        return AsyncAdmeResourceWithStreamingResponse(self)

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
    ) -> AdmeRetrieveResponse:
        """
        Retrieve an ADME prediction by ID, including its status and results.

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
            path_template("/compute/v1/predictions/adme/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"workspace_id": workspace_id}, adme_retrieve_params.AdmeRetrieveParams
                ),
            ),
            cast_to=AdmeRetrieveResponse,
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
    ) -> AsyncPaginator[AdmeListResponse, AsyncCursorPage[AdmeListResponse]]:
        """
        List ADME predictions, optionally filtered by workspace

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
            "/compute/v1/predictions/adme",
            page=AsyncCursorPage[AdmeListResponse],
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
                    adme_list_params.AdmeListParams,
                ),
            ),
            model=AdmeListResponse,
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
    ) -> AdmeDeleteDataResponse:
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
            path_template("/compute/v1/predictions/adme/{id}/delete-data", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdmeDeleteDataResponse,
        )

    async def estimate_cost(
        self,
        *,
        input: adme_estimate_cost_params.Input,
        model: Literal["adme-v1"],
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AdmeEstimateCostResponse:
        """
        Estimate the cost of an ADME prediction without creating any resource or
        consuming GPU.

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
            "/compute/v1/predictions/adme/estimate-cost",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                adme_estimate_cost_params.AdmeEstimateCostParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdmeEstimateCostResponse,
        )

    async def start(
        self,
        *,
        input: adme_start_params.Input,
        model: Literal["adme-v1"],
        idempotency_key: str | Omit = omit,
        workspace_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AdmeStartResponse:
        """
        Submit a prediction job that returns Tier 1 ADME summary values for each
        requested molecule.

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
            "/compute/v1/predictions/adme",
            body=await async_maybe_transform(
                {
                    "input": input,
                    "model": model,
                    "idempotency_key": idempotency_key,
                    "workspace_id": workspace_id,
                },
                adme_start_params.AdmeStartParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AdmeStartResponse,
        )


class AdmeResourceWithRawResponse:
    def __init__(self, adme: AdmeResource) -> None:
        self._adme = adme

        self.retrieve = to_raw_response_wrapper(
            adme.retrieve,
        )
        self.list = to_raw_response_wrapper(
            adme.list,
        )
        self.delete_data = to_raw_response_wrapper(
            adme.delete_data,
        )
        self.estimate_cost = to_raw_response_wrapper(
            adme.estimate_cost,
        )
        self.start = to_raw_response_wrapper(
            adme.start,
        )


class AsyncAdmeResourceWithRawResponse:
    def __init__(self, adme: AsyncAdmeResource) -> None:
        self._adme = adme

        self.retrieve = async_to_raw_response_wrapper(
            adme.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            adme.list,
        )
        self.delete_data = async_to_raw_response_wrapper(
            adme.delete_data,
        )
        self.estimate_cost = async_to_raw_response_wrapper(
            adme.estimate_cost,
        )
        self.start = async_to_raw_response_wrapper(
            adme.start,
        )


class AdmeResourceWithStreamingResponse:
    def __init__(self, adme: AdmeResource) -> None:
        self._adme = adme

        self.retrieve = to_streamed_response_wrapper(
            adme.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            adme.list,
        )
        self.delete_data = to_streamed_response_wrapper(
            adme.delete_data,
        )
        self.estimate_cost = to_streamed_response_wrapper(
            adme.estimate_cost,
        )
        self.start = to_streamed_response_wrapper(
            adme.start,
        )


class AsyncAdmeResourceWithStreamingResponse:
    def __init__(self, adme: AsyncAdmeResource) -> None:
        self._adme = adme

        self.retrieve = async_to_streamed_response_wrapper(
            adme.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            adme.list,
        )
        self.delete_data = async_to_streamed_response_wrapper(
            adme.delete_data,
        )
        self.estimate_cost = async_to_streamed_response_wrapper(
            adme.estimate_cost,
        )
        self.start = async_to_streamed_response_wrapper(
            adme.start,
        )
