# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncGenerationJobsPagination, AsyncGenerationJobsPagination
from ..._base_client import AsyncPaginator, make_request_options
from ...types.evaluation_datasets import generation_job_create_params
from ...types.evaluation_datasets.evaluation_dataset_generation_job import EvaluationDatasetGenerationJob
from ...types.evaluation_datasets.evaluation_dataset_generation_job_response import (
    EvaluationDatasetGenerationJobResponse,
)

__all__ = ["GenerationJobsResource", "AsyncGenerationJobsResource"]


class GenerationJobsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GenerationJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return GenerationJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GenerationJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return GenerationJobsResourceWithStreamingResponse(self)

    def create(
        self,
        evaluation_dataset_id: str,
        *,
        advanced_config: Dict[str, SequenceNotStr[str]] | Omit = omit,
        custom_instructions: str | Omit = omit,
        group_by_artifact_id: bool | Omit = omit,
        harms_list: SequenceNotStr[str] | Omit = omit,
        num_test_cases: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDatasetGenerationJobResponse:
        """
        Create Evaluation Dataset Generation Job

        Args:
          advanced_config: Advanced configuration for the evaluation dataset generation job.

          custom_instructions: Custom instructions for test case generation

          group_by_artifact_id: If this flag is true, for every generated test case, the chunks used to generate
              it will be guaranteed to be from the same document (artifact).

          harms_list: List of harms to be used for the evaluation dataset generation. If not provided,
              generation will use the knowledge base id.

          num_test_cases: Number of test cases to generate for the evaluation dataset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        return self._post(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs",
            body=maybe_transform(
                {
                    "advanced_config": advanced_config,
                    "custom_instructions": custom_instructions,
                    "group_by_artifact_id": group_by_artifact_id,
                    "harms_list": harms_list,
                    "num_test_cases": num_test_cases,
                },
                generation_job_create_params.GenerationJobCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetGenerationJobResponse,
        )

    def retrieve(
        self,
        generation_job_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDatasetGenerationJob:
        """
        Get Evaluation Dataset Generation Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not generation_job_id:
            raise ValueError(f"Expected a non-empty value for `generation_job_id` but received {generation_job_id!r}")
        return self._get(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs/{generation_job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetGenerationJob,
        )

    def list(
        self,
        evaluation_dataset_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncGenerationJobsPagination[EvaluationDatasetGenerationJob]:
        """
        Get Evaluation Dataset Generation Jobs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        return self._get_api_list(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs",
            page=SyncGenerationJobsPagination[EvaluationDatasetGenerationJob],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=EvaluationDatasetGenerationJob,
        )

    def cancel(
        self,
        generation_job_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Cancel Evaluation Dataset Generation Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not generation_job_id:
            raise ValueError(f"Expected a non-empty value for `generation_job_id` but received {generation_job_id!r}")
        return self._post(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs/{generation_job_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncGenerationJobsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGenerationJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGenerationJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGenerationJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncGenerationJobsResourceWithStreamingResponse(self)

    async def create(
        self,
        evaluation_dataset_id: str,
        *,
        advanced_config: Dict[str, SequenceNotStr[str]] | Omit = omit,
        custom_instructions: str | Omit = omit,
        group_by_artifact_id: bool | Omit = omit,
        harms_list: SequenceNotStr[str] | Omit = omit,
        num_test_cases: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDatasetGenerationJobResponse:
        """
        Create Evaluation Dataset Generation Job

        Args:
          advanced_config: Advanced configuration for the evaluation dataset generation job.

          custom_instructions: Custom instructions for test case generation

          group_by_artifact_id: If this flag is true, for every generated test case, the chunks used to generate
              it will be guaranteed to be from the same document (artifact).

          harms_list: List of harms to be used for the evaluation dataset generation. If not provided,
              generation will use the knowledge base id.

          num_test_cases: Number of test cases to generate for the evaluation dataset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        return await self._post(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs",
            body=await async_maybe_transform(
                {
                    "advanced_config": advanced_config,
                    "custom_instructions": custom_instructions,
                    "group_by_artifact_id": group_by_artifact_id,
                    "harms_list": harms_list,
                    "num_test_cases": num_test_cases,
                },
                generation_job_create_params.GenerationJobCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetGenerationJobResponse,
        )

    async def retrieve(
        self,
        generation_job_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDatasetGenerationJob:
        """
        Get Evaluation Dataset Generation Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not generation_job_id:
            raise ValueError(f"Expected a non-empty value for `generation_job_id` but received {generation_job_id!r}")
        return await self._get(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs/{generation_job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetGenerationJob,
        )

    def list(
        self,
        evaluation_dataset_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[EvaluationDatasetGenerationJob, AsyncGenerationJobsPagination[EvaluationDatasetGenerationJob]]:
        """
        Get Evaluation Dataset Generation Jobs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        return self._get_api_list(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs",
            page=AsyncGenerationJobsPagination[EvaluationDatasetGenerationJob],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=EvaluationDatasetGenerationJob,
        )

    async def cancel(
        self,
        generation_job_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> object:
        """
        Cancel Evaluation Dataset Generation Job

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not generation_job_id:
            raise ValueError(f"Expected a non-empty value for `generation_job_id` but received {generation_job_id!r}")
        return await self._post(
            f"/v4/evaluation-datasets/{evaluation_dataset_id}/generation-jobs/{generation_job_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class GenerationJobsResourceWithRawResponse:
    def __init__(self, generation_jobs: GenerationJobsResource) -> None:
        self._generation_jobs = generation_jobs

        self.create = to_raw_response_wrapper(
            generation_jobs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            generation_jobs.retrieve,
        )
        self.list = to_raw_response_wrapper(
            generation_jobs.list,
        )
        self.cancel = to_raw_response_wrapper(
            generation_jobs.cancel,
        )


class AsyncGenerationJobsResourceWithRawResponse:
    def __init__(self, generation_jobs: AsyncGenerationJobsResource) -> None:
        self._generation_jobs = generation_jobs

        self.create = async_to_raw_response_wrapper(
            generation_jobs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            generation_jobs.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            generation_jobs.list,
        )
        self.cancel = async_to_raw_response_wrapper(
            generation_jobs.cancel,
        )


class GenerationJobsResourceWithStreamingResponse:
    def __init__(self, generation_jobs: GenerationJobsResource) -> None:
        self._generation_jobs = generation_jobs

        self.create = to_streamed_response_wrapper(
            generation_jobs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            generation_jobs.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            generation_jobs.list,
        )
        self.cancel = to_streamed_response_wrapper(
            generation_jobs.cancel,
        )


class AsyncGenerationJobsResourceWithStreamingResponse:
    def __init__(self, generation_jobs: AsyncGenerationJobsResource) -> None:
        self._generation_jobs = generation_jobs

        self.create = async_to_streamed_response_wrapper(
            generation_jobs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            generation_jobs.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            generation_jobs.list,
        )
        self.cancel = async_to_streamed_response_wrapper(
            generation_jobs.cancel,
        )
