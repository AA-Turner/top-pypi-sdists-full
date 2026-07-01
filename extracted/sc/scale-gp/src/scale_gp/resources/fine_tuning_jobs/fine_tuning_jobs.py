# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .events import (
    EventsResource,
    AsyncEventsResource,
    EventsResourceWithRawResponse,
    AsyncEventsResourceWithRawResponse,
    EventsResourceWithStreamingResponse,
    AsyncEventsResourceWithStreamingResponse,
)
from ...types import fine_tuning_job_list_params, fine_tuning_job_create_params
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
from ...pagination import SyncPageResponse, AsyncPageResponse
from ..._base_client import AsyncPaginator, make_request_options
from ...types.fine_tuning_job import FineTuningJob
from ...types.shared.generic_delete_response import GenericDeleteResponse

__all__ = ["FineTuningJobsResource", "AsyncFineTuningJobsResource"]


class FineTuningJobsResource(SyncAPIResource):
    @cached_property
    def events(self) -> EventsResource:
        return EventsResource(self._client)

    @cached_property
    def with_raw_response(self) -> FineTuningJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return FineTuningJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FineTuningJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return FineTuningJobsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        training_dataset_id: str,
        base_model_id: str | Omit = omit,
        fine_tuned_model_id: str | Omit = omit,
        validation_dataset_id: str | Omit = omit,
        vendor_configuration: fine_tuning_job_create_params.VendorConfiguration | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FineTuningJob:
        """
        ### Description

        Model fine tuning jobs.

        ### Details

        TODO

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/fine-tuning-jobs",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "training_dataset_id": training_dataset_id,
                    "base_model_id": base_model_id,
                    "fine_tuned_model_id": fine_tuned_model_id,
                    "validation_dataset_id": validation_dataset_id,
                    "vendor_configuration": vendor_configuration,
                },
                fine_tuning_job_create_params.FineTuningJobCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FineTuningJob,
        )

    def retrieve(
        self,
        fine_tuning_job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FineTuningJob:
        """
        ### Description

        Gets the details of a fine tuning job

        ### Details

        This API can be used to get information about a single fine tuning job by ID. To
        use this API, pass in the `id` that was returned from your Create Fine Tuning
        Job API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not fine_tuning_job_id:
            raise ValueError(f"Expected a non-empty value for `fine_tuning_job_id` but received {fine_tuning_job_id!r}")
        return self._get(
            path_template("/v4/fine-tuning-jobs/{fine_tuning_job_id}", fine_tuning_job_id=fine_tuning_job_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FineTuningJob,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[FineTuningJob]:
        """
        ### Description

        Lists all fine tuning jobs accessible to the user.

        ### Details

        This API can be used to list fine tuning jobs. If a user has access to multiple
        accounts, all fine tuning jobs from all accounts the user is associated with
        will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v4/fine-tuning-jobs",
            page=SyncPageResponse[FineTuningJob],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    fine_tuning_job_list_params.FineTuningJobListParams,
                ),
            ),
            model=FineTuningJob,
        )

    def delete(
        self,
        fine_tuning_job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a fine tuning job

        ### Details

        This API can be used to delete a fine tuning job by ID. To use this API, pass in
        the `id` that was returned from your Create Fine Tuning Job API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not fine_tuning_job_id:
            raise ValueError(f"Expected a non-empty value for `fine_tuning_job_id` but received {fine_tuning_job_id!r}")
        return self._delete(
            path_template("/v4/fine-tuning-jobs/{fine_tuning_job_id}", fine_tuning_job_id=fine_tuning_job_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class AsyncFineTuningJobsResource(AsyncAPIResource):
    @cached_property
    def events(self) -> AsyncEventsResource:
        return AsyncEventsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFineTuningJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFineTuningJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFineTuningJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncFineTuningJobsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        training_dataset_id: str,
        base_model_id: str | Omit = omit,
        fine_tuned_model_id: str | Omit = omit,
        validation_dataset_id: str | Omit = omit,
        vendor_configuration: fine_tuning_job_create_params.VendorConfiguration | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FineTuningJob:
        """
        ### Description

        Model fine tuning jobs.

        ### Details

        TODO

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/fine-tuning-jobs",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "training_dataset_id": training_dataset_id,
                    "base_model_id": base_model_id,
                    "fine_tuned_model_id": fine_tuned_model_id,
                    "validation_dataset_id": validation_dataset_id,
                    "vendor_configuration": vendor_configuration,
                },
                fine_tuning_job_create_params.FineTuningJobCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FineTuningJob,
        )

    async def retrieve(
        self,
        fine_tuning_job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FineTuningJob:
        """
        ### Description

        Gets the details of a fine tuning job

        ### Details

        This API can be used to get information about a single fine tuning job by ID. To
        use this API, pass in the `id` that was returned from your Create Fine Tuning
        Job API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not fine_tuning_job_id:
            raise ValueError(f"Expected a non-empty value for `fine_tuning_job_id` but received {fine_tuning_job_id!r}")
        return await self._get(
            path_template("/v4/fine-tuning-jobs/{fine_tuning_job_id}", fine_tuning_job_id=fine_tuning_job_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FineTuningJob,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[FineTuningJob, AsyncPageResponse[FineTuningJob]]:
        """
        ### Description

        Lists all fine tuning jobs accessible to the user.

        ### Details

        This API can be used to list fine tuning jobs. If a user has access to multiple
        accounts, all fine tuning jobs from all accounts the user is associated with
        will be returned.

        Args:
          limit: Maximum number of artifacts to be returned by the given endpoint. Defaults to
              100 and cannot be greater than 10k.

          page: Page number for pagination to be returned by the given endpoint. Starts at page
              1

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v4/fine-tuning-jobs",
            page=AsyncPageResponse[FineTuningJob],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    fine_tuning_job_list_params.FineTuningJobListParams,
                ),
            ),
            model=FineTuningJob,
        )

    async def delete(
        self,
        fine_tuning_job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Deletes a fine tuning job

        ### Details

        This API can be used to delete a fine tuning job by ID. To use this API, pass in
        the `id` that was returned from your Create Fine Tuning Job API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not fine_tuning_job_id:
            raise ValueError(f"Expected a non-empty value for `fine_tuning_job_id` but received {fine_tuning_job_id!r}")
        return await self._delete(
            path_template("/v4/fine-tuning-jobs/{fine_tuning_job_id}", fine_tuning_job_id=fine_tuning_job_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class FineTuningJobsResourceWithRawResponse:
    def __init__(self, fine_tuning_jobs: FineTuningJobsResource) -> None:
        self._fine_tuning_jobs = fine_tuning_jobs

        self.create = to_raw_response_wrapper(
            fine_tuning_jobs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            fine_tuning_jobs.retrieve,
        )
        self.list = to_raw_response_wrapper(
            fine_tuning_jobs.list,
        )
        self.delete = to_raw_response_wrapper(
            fine_tuning_jobs.delete,
        )

    @cached_property
    def events(self) -> EventsResourceWithRawResponse:
        return EventsResourceWithRawResponse(self._fine_tuning_jobs.events)


class AsyncFineTuningJobsResourceWithRawResponse:
    def __init__(self, fine_tuning_jobs: AsyncFineTuningJobsResource) -> None:
        self._fine_tuning_jobs = fine_tuning_jobs

        self.create = async_to_raw_response_wrapper(
            fine_tuning_jobs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            fine_tuning_jobs.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            fine_tuning_jobs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            fine_tuning_jobs.delete,
        )

    @cached_property
    def events(self) -> AsyncEventsResourceWithRawResponse:
        return AsyncEventsResourceWithRawResponse(self._fine_tuning_jobs.events)


class FineTuningJobsResourceWithStreamingResponse:
    def __init__(self, fine_tuning_jobs: FineTuningJobsResource) -> None:
        self._fine_tuning_jobs = fine_tuning_jobs

        self.create = to_streamed_response_wrapper(
            fine_tuning_jobs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            fine_tuning_jobs.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            fine_tuning_jobs.list,
        )
        self.delete = to_streamed_response_wrapper(
            fine_tuning_jobs.delete,
        )

    @cached_property
    def events(self) -> EventsResourceWithStreamingResponse:
        return EventsResourceWithStreamingResponse(self._fine_tuning_jobs.events)


class AsyncFineTuningJobsResourceWithStreamingResponse:
    def __init__(self, fine_tuning_jobs: AsyncFineTuningJobsResource) -> None:
        self._fine_tuning_jobs = fine_tuning_jobs

        self.create = async_to_streamed_response_wrapper(
            fine_tuning_jobs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            fine_tuning_jobs.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            fine_tuning_jobs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            fine_tuning_jobs.delete,
        )

    @cached_property
    def events(self) -> AsyncEventsResourceWithStreamingResponse:
        return AsyncEventsResourceWithStreamingResponse(self._fine_tuning_jobs.events)
