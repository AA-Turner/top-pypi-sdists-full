# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable, Optional
from typing_extensions import Literal

import httpx

from ..types import (
    evaluation_search_params,
    evaluation_evaluate_params,
    evaluation_batch_create_params,
    evaluation_batch_delete_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.evaluation_search_response import EvaluationSearchResponse
from ..types.evaluation_evaluate_response import EvaluationEvaluateResponse
from ..types.evaluation_retrieve_response import EvaluationRetrieveResponse
from ..types.evaluation_batch_create_response import EvaluationBatchCreateResponse

__all__ = ["EvaluationsResource", "AsyncEvaluationsResource"]


class EvaluationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return EvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return EvaluationsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationRetrieveResponse:
        """
        Get Evaluation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/v1/evaluations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationRetrieveResponse,
        )

    def delete(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Evaluation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/v1/evaluations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def batch_create(
        self,
        *,
        evaluations: Iterable[evaluation_batch_create_params.Evaluation],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationBatchCreateResponse:
        """
        Batch Create Evaluations endpoint allows to import client evaluation into
        Patronus AI Platform.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/evaluations/batch",
            body=maybe_transform(
                {"evaluations": evaluations}, evaluation_batch_create_params.EvaluationBatchCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationBatchCreateResponse,
        )

    def batch_delete(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        batch_size: int | NotGiven = NOT_GIVEN,
        evaluator_criteria_id: Optional[str] | NotGiven = NOT_GIVEN,
        evaluator_family: Optional[str] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[int] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Batch Delete Evaluations

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            "/v1/evaluations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "app": app,
                        "batch_size": batch_size,
                        "evaluator_criteria_id": evaluator_criteria_id,
                        "evaluator_family": evaluator_family,
                        "experiment_id": experiment_id,
                        "project_id": project_id,
                        "trace_id": trace_id,
                    },
                    evaluation_batch_delete_params.EvaluationBatchDeleteParams,
                ),
            ),
            cast_to=object,
        )

    def evaluate(
        self,
        *,
        evaluators: Iterable[evaluation_evaluate_params.Evaluator],
        app: Optional[str] | NotGiven = NOT_GIVEN,
        capture: Literal["all", "fails-only", "none"] | NotGiven = NOT_GIVEN,
        confidence_interval_strategy: Literal["none", "full-history"] | NotGiven = NOT_GIVEN,
        dataset_id: Optional[str] | NotGiven = NOT_GIVEN,
        dataset_sample_id: Optional[str] | NotGiven = NOT_GIVEN,
        evaluated_model_attachments: Optional[Iterable[evaluation_evaluate_params.EvaluatedModelAttachment]]
        | NotGiven = NOT_GIVEN,
        experiment_id: Optional[str] | NotGiven = NOT_GIVEN,
        gold_answer: Optional[str] | NotGiven = NOT_GIVEN,
        log_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        span_id: Optional[str] | NotGiven = NOT_GIVEN,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        task_context: Union[List[str], str, None] | NotGiven = NOT_GIVEN,
        task_input: Optional[str] | NotGiven = NOT_GIVEN,
        task_output: Optional[str] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationEvaluateResponse:
        """Requires either **input** or **output** field to be specified.

        Absence of both
        leads to an HTTP_422 (Unprocessable Entity) error.

        Args:
          evaluators: List of evaluators to evaluate against.

          app: Assigns evaluation results to the app.

              - `app` cannot be used together with `experiment_id`.
              - If `app` and `experiment_id` is omitted, `app` is set automatically to
                "default" on capture.
              - Automatically creates an app if it doesn't exist.
              - Only relevant for captured results. If will capture the results under given
                app.

          capture:
              Capture evaluation result based on given option, default is none:

              - `all` captures the result of all evaluations (pass + failed).
              - `fails-only` captures the evaluation result when evaluation failed.
              - `none` does not capture evaluation result

          confidence_interval_strategy:
              Create confidence intervals based on one of the following strategies:

              - 'none': returns None
              - 'full-history': calculates upper boundary, median, and lower boundary of
                confidence interval based on all available historic records.
              - 'generated': calculates upper boundary, median, and lower boundary of
                confidence interval based on on-flight generated sample of evaluations.

          dataset_id: The ID of the dataset from which the evaluated sample originates. This field
              serves as metadata for the evaluation. This endpoint does not ensure data
              consistency for this field. There is no guarantee that the dataset with the
              given ID is present in the Patronus AI platform, as this is a self-reported
              value.

          dataset_sample_id: The ID of the sample within the dataset. This field serves as metadata for the
              evaluation. This endpoint does not ensure data consistency for this field. There
              is no guarantee that the dataset and sample are present in the Patronus AI
              platform, as this is a self-reported value.

          evaluated_model_attachments: Optional list of attachments to be associated with the evaluation sample. This
              will be added to all evaluation results in this request. Each attachment is a
              dictionary with the following keys:

              - `url`: URL of the attachment.
              - `media_type`: Media type of the attachment (e.g., "image/jpeg", "image/png").
              - `usage_type`: Type of the attachment (e.g., "evaluated_model_system_prompt",
                "evaluated_model_input").

          experiment_id: Assign evaluation results to the experiment.

              - `experiment_id` cannot be used together with `app`.
              - Only relevant for captured results. If will capture the results under
                experiment.

          gold_answer: Gold answer for given evaluated model input

          project_id: Attach project with given ID to the evaluation.

              **Note**: This parameter is ignored in case project_name or experiment_id is
              provided.

          project_name: Attach project with given name to the evaluation. If project with given name
              doesn't exist, one will be created.

              **Note:** This parameter is ignored in case experiment_id is provided.

              **Note:** This parameter takes precedence over project_id.

          system_prompt: The system prompt provided to the LLM.

          tags: Tags are key-value pairs used to label resources

          task_context: Optional context retrieved from vector database. This is a list of strings, with
              the following restrictions:

              - Number of items must be less/equal than 50.
              - The sum of tokens in all elements must be less/equal than 120000, using
                o200k_base tiktoken encoding

          task_input: The input (prompt) provided to LLM.

          task_output: LLM's response to the given input.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/evaluate",
            body=maybe_transform(
                {
                    "evaluators": evaluators,
                    "app": app,
                    "capture": capture,
                    "confidence_interval_strategy": confidence_interval_strategy,
                    "dataset_id": dataset_id,
                    "dataset_sample_id": dataset_sample_id,
                    "evaluated_model_attachments": evaluated_model_attachments,
                    "experiment_id": experiment_id,
                    "gold_answer": gold_answer,
                    "log_id": log_id,
                    "project_id": project_id,
                    "project_name": project_name,
                    "span_id": span_id,
                    "system_prompt": system_prompt,
                    "tags": tags,
                    "task_context": task_context,
                    "task_input": task_input,
                    "task_output": task_output,
                    "trace_id": trace_id,
                },
                evaluation_evaluate_params.EvaluationEvaluateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationEvaluateResponse,
        )

    def search(
        self,
        *,
        filters: Optional[Iterable[evaluation_search_params.Filter]] | NotGiven = NOT_GIVEN,
        log_id_in: Optional[List[str]] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationSearchResponse:
        """
        Search Evaluations

        Args:
          log_id_in: Deprecated, please use 'filters' instead.

          trace_id: Deprecated, please use 'filters' instead.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/evaluations/search",
            body=maybe_transform(
                {
                    "filters": filters,
                    "log_id_in": log_id_in,
                    "trace_id": trace_id,
                },
                evaluation_search_params.EvaluationSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationSearchResponse,
        )


class AsyncEvaluationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/patronus-ai/patronus-api-python#with_streaming_response
        """
        return AsyncEvaluationsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationRetrieveResponse:
        """
        Get Evaluation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/v1/evaluations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationRetrieveResponse,
        )

    async def delete(
        self,
        id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete Evaluation

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/v1/evaluations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def batch_create(
        self,
        *,
        evaluations: Iterable[evaluation_batch_create_params.Evaluation],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationBatchCreateResponse:
        """
        Batch Create Evaluations endpoint allows to import client evaluation into
        Patronus AI Platform.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/evaluations/batch",
            body=await async_maybe_transform(
                {"evaluations": evaluations}, evaluation_batch_create_params.EvaluationBatchCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationBatchCreateResponse,
        )

    async def batch_delete(
        self,
        *,
        app: Optional[str] | NotGiven = NOT_GIVEN,
        batch_size: int | NotGiven = NOT_GIVEN,
        evaluator_criteria_id: Optional[str] | NotGiven = NOT_GIVEN,
        evaluator_family: Optional[str] | NotGiven = NOT_GIVEN,
        experiment_id: Optional[int] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Batch Delete Evaluations

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            "/v1/evaluations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "app": app,
                        "batch_size": batch_size,
                        "evaluator_criteria_id": evaluator_criteria_id,
                        "evaluator_family": evaluator_family,
                        "experiment_id": experiment_id,
                        "project_id": project_id,
                        "trace_id": trace_id,
                    },
                    evaluation_batch_delete_params.EvaluationBatchDeleteParams,
                ),
            ),
            cast_to=object,
        )

    async def evaluate(
        self,
        *,
        evaluators: Iterable[evaluation_evaluate_params.Evaluator],
        app: Optional[str] | NotGiven = NOT_GIVEN,
        capture: Literal["all", "fails-only", "none"] | NotGiven = NOT_GIVEN,
        confidence_interval_strategy: Literal["none", "full-history"] | NotGiven = NOT_GIVEN,
        dataset_id: Optional[str] | NotGiven = NOT_GIVEN,
        dataset_sample_id: Optional[str] | NotGiven = NOT_GIVEN,
        evaluated_model_attachments: Optional[Iterable[evaluation_evaluate_params.EvaluatedModelAttachment]]
        | NotGiven = NOT_GIVEN,
        experiment_id: Optional[str] | NotGiven = NOT_GIVEN,
        gold_answer: Optional[str] | NotGiven = NOT_GIVEN,
        log_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_id: Optional[str] | NotGiven = NOT_GIVEN,
        project_name: Optional[str] | NotGiven = NOT_GIVEN,
        span_id: Optional[str] | NotGiven = NOT_GIVEN,
        system_prompt: Optional[str] | NotGiven = NOT_GIVEN,
        tags: object | NotGiven = NOT_GIVEN,
        task_context: Union[List[str], str, None] | NotGiven = NOT_GIVEN,
        task_input: Optional[str] | NotGiven = NOT_GIVEN,
        task_output: Optional[str] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationEvaluateResponse:
        """Requires either **input** or **output** field to be specified.

        Absence of both
        leads to an HTTP_422 (Unprocessable Entity) error.

        Args:
          evaluators: List of evaluators to evaluate against.

          app: Assigns evaluation results to the app.

              - `app` cannot be used together with `experiment_id`.
              - If `app` and `experiment_id` is omitted, `app` is set automatically to
                "default" on capture.
              - Automatically creates an app if it doesn't exist.
              - Only relevant for captured results. If will capture the results under given
                app.

          capture:
              Capture evaluation result based on given option, default is none:

              - `all` captures the result of all evaluations (pass + failed).
              - `fails-only` captures the evaluation result when evaluation failed.
              - `none` does not capture evaluation result

          confidence_interval_strategy:
              Create confidence intervals based on one of the following strategies:

              - 'none': returns None
              - 'full-history': calculates upper boundary, median, and lower boundary of
                confidence interval based on all available historic records.
              - 'generated': calculates upper boundary, median, and lower boundary of
                confidence interval based on on-flight generated sample of evaluations.

          dataset_id: The ID of the dataset from which the evaluated sample originates. This field
              serves as metadata for the evaluation. This endpoint does not ensure data
              consistency for this field. There is no guarantee that the dataset with the
              given ID is present in the Patronus AI platform, as this is a self-reported
              value.

          dataset_sample_id: The ID of the sample within the dataset. This field serves as metadata for the
              evaluation. This endpoint does not ensure data consistency for this field. There
              is no guarantee that the dataset and sample are present in the Patronus AI
              platform, as this is a self-reported value.

          evaluated_model_attachments: Optional list of attachments to be associated with the evaluation sample. This
              will be added to all evaluation results in this request. Each attachment is a
              dictionary with the following keys:

              - `url`: URL of the attachment.
              - `media_type`: Media type of the attachment (e.g., "image/jpeg", "image/png").
              - `usage_type`: Type of the attachment (e.g., "evaluated_model_system_prompt",
                "evaluated_model_input").

          experiment_id: Assign evaluation results to the experiment.

              - `experiment_id` cannot be used together with `app`.
              - Only relevant for captured results. If will capture the results under
                experiment.

          gold_answer: Gold answer for given evaluated model input

          project_id: Attach project with given ID to the evaluation.

              **Note**: This parameter is ignored in case project_name or experiment_id is
              provided.

          project_name: Attach project with given name to the evaluation. If project with given name
              doesn't exist, one will be created.

              **Note:** This parameter is ignored in case experiment_id is provided.

              **Note:** This parameter takes precedence over project_id.

          system_prompt: The system prompt provided to the LLM.

          tags: Tags are key-value pairs used to label resources

          task_context: Optional context retrieved from vector database. This is a list of strings, with
              the following restrictions:

              - Number of items must be less/equal than 50.
              - The sum of tokens in all elements must be less/equal than 120000, using
                o200k_base tiktoken encoding

          task_input: The input (prompt) provided to LLM.

          task_output: LLM's response to the given input.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/evaluate",
            body=await async_maybe_transform(
                {
                    "evaluators": evaluators,
                    "app": app,
                    "capture": capture,
                    "confidence_interval_strategy": confidence_interval_strategy,
                    "dataset_id": dataset_id,
                    "dataset_sample_id": dataset_sample_id,
                    "evaluated_model_attachments": evaluated_model_attachments,
                    "experiment_id": experiment_id,
                    "gold_answer": gold_answer,
                    "log_id": log_id,
                    "project_id": project_id,
                    "project_name": project_name,
                    "span_id": span_id,
                    "system_prompt": system_prompt,
                    "tags": tags,
                    "task_context": task_context,
                    "task_input": task_input,
                    "task_output": task_output,
                    "trace_id": trace_id,
                },
                evaluation_evaluate_params.EvaluationEvaluateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationEvaluateResponse,
        )

    async def search(
        self,
        *,
        filters: Optional[Iterable[evaluation_search_params.Filter]] | NotGiven = NOT_GIVEN,
        log_id_in: Optional[List[str]] | NotGiven = NOT_GIVEN,
        trace_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EvaluationSearchResponse:
        """
        Search Evaluations

        Args:
          log_id_in: Deprecated, please use 'filters' instead.

          trace_id: Deprecated, please use 'filters' instead.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/evaluations/search",
            body=await async_maybe_transform(
                {
                    "filters": filters,
                    "log_id_in": log_id_in,
                    "trace_id": trace_id,
                },
                evaluation_search_params.EvaluationSearchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationSearchResponse,
        )


class EvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.retrieve = to_raw_response_wrapper(
            evaluations.retrieve,
        )
        self.delete = to_raw_response_wrapper(
            evaluations.delete,
        )
        self.batch_create = to_raw_response_wrapper(
            evaluations.batch_create,
        )
        self.batch_delete = to_raw_response_wrapper(
            evaluations.batch_delete,
        )
        self.evaluate = to_raw_response_wrapper(
            evaluations.evaluate,
        )
        self.search = to_raw_response_wrapper(
            evaluations.search,
        )


class AsyncEvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.retrieve = async_to_raw_response_wrapper(
            evaluations.retrieve,
        )
        self.delete = async_to_raw_response_wrapper(
            evaluations.delete,
        )
        self.batch_create = async_to_raw_response_wrapper(
            evaluations.batch_create,
        )
        self.batch_delete = async_to_raw_response_wrapper(
            evaluations.batch_delete,
        )
        self.evaluate = async_to_raw_response_wrapper(
            evaluations.evaluate,
        )
        self.search = async_to_raw_response_wrapper(
            evaluations.search,
        )


class EvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.retrieve = to_streamed_response_wrapper(
            evaluations.retrieve,
        )
        self.delete = to_streamed_response_wrapper(
            evaluations.delete,
        )
        self.batch_create = to_streamed_response_wrapper(
            evaluations.batch_create,
        )
        self.batch_delete = to_streamed_response_wrapper(
            evaluations.batch_delete,
        )
        self.evaluate = to_streamed_response_wrapper(
            evaluations.evaluate,
        )
        self.search = to_streamed_response_wrapper(
            evaluations.search,
        )


class AsyncEvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.retrieve = async_to_streamed_response_wrapper(
            evaluations.retrieve,
        )
        self.delete = async_to_streamed_response_wrapper(
            evaluations.delete,
        )
        self.batch_create = async_to_streamed_response_wrapper(
            evaluations.batch_create,
        )
        self.batch_delete = async_to_streamed_response_wrapper(
            evaluations.batch_delete,
        )
        self.evaluate = async_to_streamed_response_wrapper(
            evaluations.evaluate,
        )
        self.search = async_to_streamed_response_wrapper(
            evaluations.search,
        )
