# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, overload

import httpx

from .tasks import (
    TasksResource,
    AsyncTasksResource,
    TasksResourceWithRawResponse,
    AsyncTasksResourceWithRawResponse,
    TasksResourceWithStreamingResponse,
    AsyncTasksResourceWithStreamingResponse,
)
from ...types import (
    evaluation_list_params,
    evaluation_create_params,
    evaluation_update_params,
    evaluation_retrieve_params,
    evaluation_claim_task_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import required_args, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncPageResponse, AsyncPageResponse
from ...types.task import Task
from ..._base_client import AsyncPaginator, make_request_options
from .evaluation_metrics import (
    EvaluationMetricsResource,
    AsyncEvaluationMetricsResource,
    EvaluationMetricsResourceWithRawResponse,
    AsyncEvaluationMetricsResourceWithRawResponse,
    EvaluationMetricsResourceWithStreamingResponse,
    AsyncEvaluationMetricsResourceWithStreamingResponse,
)
from .contributor_metrics import (
    ContributorMetricsResource,
    AsyncContributorMetricsResource,
    ContributorMetricsResourceWithRawResponse,
    AsyncContributorMetricsResourceWithRawResponse,
    ContributorMetricsResourceWithStreamingResponse,
    AsyncContributorMetricsResourceWithStreamingResponse,
)
from .hybrid_eval_metrics import (
    HybridEvalMetricsResource,
    AsyncHybridEvalMetricsResource,
    HybridEvalMetricsResourceWithRawResponse,
    AsyncHybridEvalMetricsResourceWithRawResponse,
    HybridEvalMetricsResourceWithStreamingResponse,
    AsyncHybridEvalMetricsResourceWithStreamingResponse,
)
from ...types.annotation_config_param import AnnotationConfigParam
from ...types.evaluation_list_response import EvaluationListResponse
from ...types.evaluation_create_response import EvaluationCreateResponse
from ...types.evaluation_update_response import EvaluationUpdateResponse
from .test_case_results.test_case_results import (
    TestCaseResultsResource,
    AsyncTestCaseResultsResource,
    TestCaseResultsResourceWithRawResponse,
    AsyncTestCaseResultsResourceWithRawResponse,
    TestCaseResultsResourceWithStreamingResponse,
    AsyncTestCaseResultsResourceWithStreamingResponse,
)
from ...types.evaluation_retrieve_response import EvaluationRetrieveResponse
from ...types.shared.generic_delete_response import GenericDeleteResponse

__all__ = ["EvaluationsResource", "AsyncEvaluationsResource"]


class EvaluationsResource(SyncAPIResource):
    @cached_property
    def tasks(self) -> TasksResource:
        return TasksResource(self._client)

    @cached_property
    def contributor_metrics(self) -> ContributorMetricsResource:
        return ContributorMetricsResource(self._client)

    @cached_property
    def evaluation_metrics(self) -> EvaluationMetricsResource:
        return EvaluationMetricsResource(self._client)

    @cached_property
    def hybrid_eval_metrics(self) -> HybridEvalMetricsResource:
        return HybridEvalMetricsResource(self._client)

    @cached_property
    def test_case_results(self) -> TestCaseResultsResource:
        return TestCaseResultsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EvaluationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return EvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return EvaluationsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        application_variant_id: str,
        description: str,
        evaluation_dataset_id: str,
        name: str,
        annotation_config: evaluation_create_params.EvaluationBuilderRequestAnnotationConfig | Omit = omit,
        application_test_case_output_group_id: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        evaluation_dataset_version: int | Omit = omit,
        metric_config: evaluation_create_params.EvaluationBuilderRequestMetricConfig | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        type: Literal["builder"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationCreateResponse:
        """
        ### Description

        Creates a evaluation

        ### Details

        This API can be used to create a evaluation. To use this API, review the request
        schema and pass in all fields that are required to create a evaluation.

        Args:
          account_id: The ID of the account that owns the given entity.

          annotation_config: Annotation configuration for tasking

          evaluation_config_id: The ID of the associated evaluation config.

          metric_config: Specifies the config for the metrics to be computed.

          question_id_to_annotation_config: Specifies the annotation configuration to use for specific questions.

          type: create standalone evaluation or build evaluation which will auto generate test
              case results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        description: str,
        name: str,
        annotation_config: evaluation_create_params.DefaultEvaluationRequestAnnotationConfig | Omit = omit,
        application_variant_id: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        metric_config: evaluation_create_params.DefaultEvaluationRequestMetricConfig | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        type: Literal["default"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationCreateResponse:
        """
        ### Description

        Creates a evaluation

        ### Details

        This API can be used to create a evaluation. To use this API, review the request
        schema and pass in all fields that are required to create a evaluation.

        Args:
          account_id: The ID of the account that owns the given entity.

          annotation_config: Annotation configuration for tasking

          evaluation_config_id: The ID of the associated evaluation config.

          metric_config: Specifies the config for the metrics to be computed.

          question_id_to_annotation_config: Specifies the annotation configuration to use for specific questions.

          type: create standalone evaluation or build evaluation which will auto generate test
              case results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["account_id", "application_spec_id", "application_variant_id", "description", "evaluation_dataset_id", "name"],
        ["account_id", "application_spec_id", "description", "name"],
    )
    def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        application_variant_id: str | Omit = omit,
        description: str,
        evaluation_dataset_id: str | Omit = omit,
        name: str,
        annotation_config: evaluation_create_params.EvaluationBuilderRequestAnnotationConfig
        | evaluation_create_params.DefaultEvaluationRequestAnnotationConfig
        | Omit = omit,
        application_test_case_output_group_id: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        evaluation_dataset_version: int | Omit = omit,
        metric_config: evaluation_create_params.EvaluationBuilderRequestMetricConfig
        | evaluation_create_params.DefaultEvaluationRequestMetricConfig
        | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        type: Literal["builder"] | Literal["default"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationCreateResponse:
        return self._post(
            "/v4/evaluations",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "application_spec_id": application_spec_id,
                    "application_variant_id": application_variant_id,
                    "description": description,
                    "evaluation_dataset_id": evaluation_dataset_id,
                    "name": name,
                    "annotation_config": annotation_config,
                    "application_test_case_output_group_id": application_test_case_output_group_id,
                    "evaluation_config": evaluation_config,
                    "evaluation_config_id": evaluation_config_id,
                    "evaluation_dataset_version": evaluation_dataset_version,
                    "metric_config": metric_config,
                    "question_id_to_annotation_config": question_id_to_annotation_config,
                    "tags": tags,
                    "type": type,
                },
                evaluation_create_params.EvaluationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationCreateResponse,
        )

    def retrieve(
        self,
        evaluation_id: str,
        *,
        view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "EvaluationDatasets"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationRetrieveResponse:
        """
        ### Description

        Gets the details of a evaluation

        ### Details

        This API can be used to get information about a single evaluation by ID. To use
        this API, pass in the `id` that was returned from your Create Evaluation API
        call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get(
            f"/v4/evaluations/{evaluation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"view": view}, evaluation_retrieve_params.EvaluationRetrieveParams),
            ),
            cast_to=EvaluationRetrieveResponse,
        )

    @overload
    def update(
        self,
        evaluation_id: str,
        *,
        annotation_config: evaluation_update_params.PartialPatchEvaluationRequestAnnotationConfig | Omit = omit,
        application_spec_id: str | Omit = omit,
        application_variant_id: str | Omit = omit,
        description: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        evaluation_type: Literal["llm_benchmark"] | Omit = omit,
        name: str | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        restore: Literal[False] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationUpdateResponse:
        """
        ### Description

        Updates a evaluation

        ### Details

        This API can be used to update the evaluation that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Evaluation API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          annotation_config: Annotation configuration for tasking

          evaluation_config_id: The ID of the associated evaluation config.

          evaluation_type: If llm_benchmark is provided, the evaluation will be updated to a hybrid
              evaluation. No-op on existing hybrid evaluations, and not available for studio
              evaluations.

          question_id_to_annotation_config: Specifies the annotation configuration to use for specific questions.

          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        evaluation_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationUpdateResponse:
        """
        ### Description

        Updates a evaluation

        ### Details

        This API can be used to update the evaluation that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Evaluation API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    def update(
        self,
        evaluation_id: str,
        *,
        annotation_config: evaluation_update_params.PartialPatchEvaluationRequestAnnotationConfig | Omit = omit,
        application_spec_id: str | Omit = omit,
        application_variant_id: str | Omit = omit,
        description: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        evaluation_type: Literal["llm_benchmark"] | Omit = omit,
        name: str | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        restore: Literal[False] | Literal[True] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationUpdateResponse:
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._patch(
            f"/v4/evaluations/{evaluation_id}",
            body=maybe_transform(
                {
                    "annotation_config": annotation_config,
                    "application_spec_id": application_spec_id,
                    "application_variant_id": application_variant_id,
                    "description": description,
                    "evaluation_config": evaluation_config,
                    "evaluation_config_id": evaluation_config_id,
                    "evaluation_type": evaluation_type,
                    "name": name,
                    "question_id_to_annotation_config": question_id_to_annotation_config,
                    "restore": restore,
                    "tags": tags,
                },
                evaluation_update_params.EvaluationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationUpdateResponse,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        application_spec_id: Union[int, str] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        sort_by: List[
            Literal[
                "status:asc",
                "status:desc",
                "application_spec_id:asc",
                "application_spec_id:desc",
                "application_spec:asc",
                "application_spec:desc",
                "application_variant_id:asc",
                "application_variant_id:desc",
                "application_variant:asc",
                "application_variant:desc",
                "evaluation_config_id:asc",
                "evaluation_config_id:desc",
                "completed_at:asc",
                "completed_at:desc",
                "total_test_case_result_count:asc",
                "total_test_case_result_count:desc",
                "completed_test_case_result_count:asc",
                "completed_test_case_result_count:desc",
                "annotation_config:asc",
                "annotation_config:desc",
                "question_id_to_annotation_config:asc",
                "question_id_to_annotation_config:desc",
                "metric_config:asc",
                "metric_config:desc",
                "evaluation_config_expanded:asc",
                "evaluation_config_expanded:desc",
                "test_case_results:asc",
                "test_case_results:desc",
                "async_jobs:asc",
                "async_jobs:desc",
                "evaluation_datasets:asc",
                "evaluation_datasets:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_identity_type:asc",
                "created_by_identity_type:desc",
                "archived_at:asc",
                "archived_at:desc",
                "name:asc",
                "name:desc",
                "description:asc",
                "description:desc",
                "tags:asc",
                "tags:desc",
                "evaluation_config:asc",
                "evaluation_config:desc",
            ]
        ]
        | Omit = omit,
        view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "EvaluationDatasets"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[EvaluationListResponse]:
        """
        ### Description

        Lists all evaluations accessible to the user.

        ### Details

        This API can be used to list evaluations. If a user has access to multiple
        accounts, all evaluations from all accounts the user is associated with will be
        returned.

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
            "/v4/evaluations",
            page=SyncPageResponse[EvaluationListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_spec_id": application_spec_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                        "sort_by": sort_by,
                        "view": view,
                    },
                    evaluation_list_params.EvaluationListParams,
                ),
            ),
            model=EvaluationListResponse,
        )

    def delete(
        self,
        evaluation_id: str,
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

        Deletes a evaluation

        ### Details

        This API can be used to delete a evaluation by ID. To use this API, pass in the
        `id` that was returned from your Create Evaluation API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._delete(
            f"/v4/evaluations/{evaluation_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )

    def claim_task(
        self,
        evaluation_id: str,
        *,
        task_type: Literal["EVALUATION_ANNOTATION", "EVALUATION_AUDIT", "CONTRIBUTOR_ANNOTATION", "CONTRIBUTOR_AUDIT"]
        | Omit = omit,
        skip_current: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[Task]:
        """
        Claim Evaluation Task

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._post(
            f"/v4/evaluations/{evaluation_id}/claim-task",
            body=maybe_transform(
                {"skip_current": skip_current}, evaluation_claim_task_params.EvaluationClaimTaskParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"task_type": task_type}, evaluation_claim_task_params.EvaluationClaimTaskParams),
            ),
            cast_to=Task,
        )


class AsyncEvaluationsResource(AsyncAPIResource):
    @cached_property
    def tasks(self) -> AsyncTasksResource:
        return AsyncTasksResource(self._client)

    @cached_property
    def contributor_metrics(self) -> AsyncContributorMetricsResource:
        return AsyncContributorMetricsResource(self._client)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResource:
        return AsyncEvaluationMetricsResource(self._client)

    @cached_property
    def hybrid_eval_metrics(self) -> AsyncHybridEvalMetricsResource:
        return AsyncHybridEvalMetricsResource(self._client)

    @cached_property
    def test_case_results(self) -> AsyncTestCaseResultsResource:
        return AsyncTestCaseResultsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEvaluationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncEvaluationsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        application_variant_id: str,
        description: str,
        evaluation_dataset_id: str,
        name: str,
        annotation_config: evaluation_create_params.EvaluationBuilderRequestAnnotationConfig | Omit = omit,
        application_test_case_output_group_id: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        evaluation_dataset_version: int | Omit = omit,
        metric_config: evaluation_create_params.EvaluationBuilderRequestMetricConfig | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        type: Literal["builder"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationCreateResponse:
        """
        ### Description

        Creates a evaluation

        ### Details

        This API can be used to create a evaluation. To use this API, review the request
        schema and pass in all fields that are required to create a evaluation.

        Args:
          account_id: The ID of the account that owns the given entity.

          annotation_config: Annotation configuration for tasking

          evaluation_config_id: The ID of the associated evaluation config.

          metric_config: Specifies the config for the metrics to be computed.

          question_id_to_annotation_config: Specifies the annotation configuration to use for specific questions.

          type: create standalone evaluation or build evaluation which will auto generate test
              case results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        description: str,
        name: str,
        annotation_config: evaluation_create_params.DefaultEvaluationRequestAnnotationConfig | Omit = omit,
        application_variant_id: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        metric_config: evaluation_create_params.DefaultEvaluationRequestMetricConfig | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        type: Literal["default"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationCreateResponse:
        """
        ### Description

        Creates a evaluation

        ### Details

        This API can be used to create a evaluation. To use this API, review the request
        schema and pass in all fields that are required to create a evaluation.

        Args:
          account_id: The ID of the account that owns the given entity.

          annotation_config: Annotation configuration for tasking

          evaluation_config_id: The ID of the associated evaluation config.

          metric_config: Specifies the config for the metrics to be computed.

          question_id_to_annotation_config: Specifies the annotation configuration to use for specific questions.

          type: create standalone evaluation or build evaluation which will auto generate test
              case results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["account_id", "application_spec_id", "application_variant_id", "description", "evaluation_dataset_id", "name"],
        ["account_id", "application_spec_id", "description", "name"],
    )
    async def create(
        self,
        *,
        account_id: str,
        application_spec_id: str,
        application_variant_id: str | Omit = omit,
        description: str,
        evaluation_dataset_id: str | Omit = omit,
        name: str,
        annotation_config: evaluation_create_params.EvaluationBuilderRequestAnnotationConfig
        | evaluation_create_params.DefaultEvaluationRequestAnnotationConfig
        | Omit = omit,
        application_test_case_output_group_id: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        evaluation_dataset_version: int | Omit = omit,
        metric_config: evaluation_create_params.EvaluationBuilderRequestMetricConfig
        | evaluation_create_params.DefaultEvaluationRequestMetricConfig
        | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        type: Literal["builder"] | Literal["default"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationCreateResponse:
        return await self._post(
            "/v4/evaluations",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "application_spec_id": application_spec_id,
                    "application_variant_id": application_variant_id,
                    "description": description,
                    "evaluation_dataset_id": evaluation_dataset_id,
                    "name": name,
                    "annotation_config": annotation_config,
                    "application_test_case_output_group_id": application_test_case_output_group_id,
                    "evaluation_config": evaluation_config,
                    "evaluation_config_id": evaluation_config_id,
                    "evaluation_dataset_version": evaluation_dataset_version,
                    "metric_config": metric_config,
                    "question_id_to_annotation_config": question_id_to_annotation_config,
                    "tags": tags,
                    "type": type,
                },
                evaluation_create_params.EvaluationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationCreateResponse,
        )

    async def retrieve(
        self,
        evaluation_id: str,
        *,
        view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "EvaluationDatasets"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationRetrieveResponse:
        """
        ### Description

        Gets the details of a evaluation

        ### Details

        This API can be used to get information about a single evaluation by ID. To use
        this API, pass in the `id` that was returned from your Create Evaluation API
        call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._get(
            f"/v4/evaluations/{evaluation_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"view": view}, evaluation_retrieve_params.EvaluationRetrieveParams),
            ),
            cast_to=EvaluationRetrieveResponse,
        )

    @overload
    async def update(
        self,
        evaluation_id: str,
        *,
        annotation_config: evaluation_update_params.PartialPatchEvaluationRequestAnnotationConfig | Omit = omit,
        application_spec_id: str | Omit = omit,
        application_variant_id: str | Omit = omit,
        description: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        evaluation_type: Literal["llm_benchmark"] | Omit = omit,
        name: str | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        restore: Literal[False] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationUpdateResponse:
        """
        ### Description

        Updates a evaluation

        ### Details

        This API can be used to update the evaluation that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Evaluation API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          annotation_config: Annotation configuration for tasking

          evaluation_config_id: The ID of the associated evaluation config.

          evaluation_type: If llm_benchmark is provided, the evaluation will be updated to a hybrid
              evaluation. No-op on existing hybrid evaluations, and not available for studio
              evaluations.

          question_id_to_annotation_config: Specifies the annotation configuration to use for specific questions.

          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        evaluation_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationUpdateResponse:
        """
        ### Description

        Updates a evaluation

        ### Details

        This API can be used to update the evaluation that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Evaluation API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    async def update(
        self,
        evaluation_id: str,
        *,
        annotation_config: evaluation_update_params.PartialPatchEvaluationRequestAnnotationConfig | Omit = omit,
        application_spec_id: str | Omit = omit,
        application_variant_id: str | Omit = omit,
        description: str | Omit = omit,
        evaluation_config: Dict[str, object] | Omit = omit,
        evaluation_config_id: str | Omit = omit,
        evaluation_type: Literal["llm_benchmark"] | Omit = omit,
        name: str | Omit = omit,
        question_id_to_annotation_config: Dict[str, AnnotationConfigParam] | Omit = omit,
        restore: Literal[False] | Literal[True] | Omit = omit,
        tags: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationUpdateResponse:
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._patch(
            f"/v4/evaluations/{evaluation_id}",
            body=await async_maybe_transform(
                {
                    "annotation_config": annotation_config,
                    "application_spec_id": application_spec_id,
                    "application_variant_id": application_variant_id,
                    "description": description,
                    "evaluation_config": evaluation_config,
                    "evaluation_config_id": evaluation_config_id,
                    "evaluation_type": evaluation_type,
                    "name": name,
                    "question_id_to_annotation_config": question_id_to_annotation_config,
                    "restore": restore,
                    "tags": tags,
                },
                evaluation_update_params.EvaluationUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationUpdateResponse,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        application_spec_id: Union[int, str] | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        sort_by: List[
            Literal[
                "status:asc",
                "status:desc",
                "application_spec_id:asc",
                "application_spec_id:desc",
                "application_spec:asc",
                "application_spec:desc",
                "application_variant_id:asc",
                "application_variant_id:desc",
                "application_variant:asc",
                "application_variant:desc",
                "evaluation_config_id:asc",
                "evaluation_config_id:desc",
                "completed_at:asc",
                "completed_at:desc",
                "total_test_case_result_count:asc",
                "total_test_case_result_count:desc",
                "completed_test_case_result_count:asc",
                "completed_test_case_result_count:desc",
                "annotation_config:asc",
                "annotation_config:desc",
                "question_id_to_annotation_config:asc",
                "question_id_to_annotation_config:desc",
                "metric_config:asc",
                "metric_config:desc",
                "evaluation_config_expanded:asc",
                "evaluation_config_expanded:desc",
                "test_case_results:asc",
                "test_case_results:desc",
                "async_jobs:asc",
                "async_jobs:desc",
                "evaluation_datasets:asc",
                "evaluation_datasets:desc",
                "id:asc",
                "id:desc",
                "created_at:asc",
                "created_at:desc",
                "account_id:asc",
                "account_id:desc",
                "created_by_user_id:asc",
                "created_by_user_id:desc",
                "created_by_identity_type:asc",
                "created_by_identity_type:desc",
                "archived_at:asc",
                "archived_at:desc",
                "name:asc",
                "name:desc",
                "description:asc",
                "description:desc",
                "tags:asc",
                "tags:desc",
                "evaluation_config:asc",
                "evaluation_config:desc",
            ]
        ]
        | Omit = omit,
        view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "EvaluationDatasets"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[EvaluationListResponse, AsyncPageResponse[EvaluationListResponse]]:
        """
        ### Description

        Lists all evaluations accessible to the user.

        ### Details

        This API can be used to list evaluations. If a user has access to multiple
        accounts, all evaluations from all accounts the user is associated with will be
        returned.

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
            "/v4/evaluations",
            page=AsyncPageResponse[EvaluationListResponse],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_spec_id": application_spec_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                        "sort_by": sort_by,
                        "view": view,
                    },
                    evaluation_list_params.EvaluationListParams,
                ),
            ),
            model=EvaluationListResponse,
        )

    async def delete(
        self,
        evaluation_id: str,
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

        Deletes a evaluation

        ### Details

        This API can be used to delete a evaluation by ID. To use this API, pass in the
        `id` that was returned from your Create Evaluation API call as a path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._delete(
            f"/v4/evaluations/{evaluation_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )

    async def claim_task(
        self,
        evaluation_id: str,
        *,
        task_type: Literal["EVALUATION_ANNOTATION", "EVALUATION_AUDIT", "CONTRIBUTOR_ANNOTATION", "CONTRIBUTOR_AUDIT"]
        | Omit = omit,
        skip_current: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Optional[Task]:
        """
        Claim Evaluation Task

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._post(
            f"/v4/evaluations/{evaluation_id}/claim-task",
            body=await async_maybe_transform(
                {"skip_current": skip_current}, evaluation_claim_task_params.EvaluationClaimTaskParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"task_type": task_type}, evaluation_claim_task_params.EvaluationClaimTaskParams
                ),
            ),
            cast_to=Task,
        )


class EvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = to_raw_response_wrapper(
            evaluations.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluations.retrieve,
        )
        self.update = to_raw_response_wrapper(
            evaluations.update,
        )
        self.list = to_raw_response_wrapper(
            evaluations.list,
        )
        self.delete = to_raw_response_wrapper(
            evaluations.delete,
        )
        self.claim_task = to_raw_response_wrapper(
            evaluations.claim_task,
        )

    @cached_property
    def tasks(self) -> TasksResourceWithRawResponse:
        return TasksResourceWithRawResponse(self._evaluations.tasks)

    @cached_property
    def contributor_metrics(self) -> ContributorMetricsResourceWithRawResponse:
        return ContributorMetricsResourceWithRawResponse(self._evaluations.contributor_metrics)

    @cached_property
    def evaluation_metrics(self) -> EvaluationMetricsResourceWithRawResponse:
        return EvaluationMetricsResourceWithRawResponse(self._evaluations.evaluation_metrics)

    @cached_property
    def hybrid_eval_metrics(self) -> HybridEvalMetricsResourceWithRawResponse:
        return HybridEvalMetricsResourceWithRawResponse(self._evaluations.hybrid_eval_metrics)

    @cached_property
    def test_case_results(self) -> TestCaseResultsResourceWithRawResponse:
        return TestCaseResultsResourceWithRawResponse(self._evaluations.test_case_results)


class AsyncEvaluationsResourceWithRawResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = async_to_raw_response_wrapper(
            evaluations.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluations.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            evaluations.update,
        )
        self.list = async_to_raw_response_wrapper(
            evaluations.list,
        )
        self.delete = async_to_raw_response_wrapper(
            evaluations.delete,
        )
        self.claim_task = async_to_raw_response_wrapper(
            evaluations.claim_task,
        )

    @cached_property
    def tasks(self) -> AsyncTasksResourceWithRawResponse:
        return AsyncTasksResourceWithRawResponse(self._evaluations.tasks)

    @cached_property
    def contributor_metrics(self) -> AsyncContributorMetricsResourceWithRawResponse:
        return AsyncContributorMetricsResourceWithRawResponse(self._evaluations.contributor_metrics)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResourceWithRawResponse:
        return AsyncEvaluationMetricsResourceWithRawResponse(self._evaluations.evaluation_metrics)

    @cached_property
    def hybrid_eval_metrics(self) -> AsyncHybridEvalMetricsResourceWithRawResponse:
        return AsyncHybridEvalMetricsResourceWithRawResponse(self._evaluations.hybrid_eval_metrics)

    @cached_property
    def test_case_results(self) -> AsyncTestCaseResultsResourceWithRawResponse:
        return AsyncTestCaseResultsResourceWithRawResponse(self._evaluations.test_case_results)


class EvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: EvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = to_streamed_response_wrapper(
            evaluations.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluations.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            evaluations.update,
        )
        self.list = to_streamed_response_wrapper(
            evaluations.list,
        )
        self.delete = to_streamed_response_wrapper(
            evaluations.delete,
        )
        self.claim_task = to_streamed_response_wrapper(
            evaluations.claim_task,
        )

    @cached_property
    def tasks(self) -> TasksResourceWithStreamingResponse:
        return TasksResourceWithStreamingResponse(self._evaluations.tasks)

    @cached_property
    def contributor_metrics(self) -> ContributorMetricsResourceWithStreamingResponse:
        return ContributorMetricsResourceWithStreamingResponse(self._evaluations.contributor_metrics)

    @cached_property
    def evaluation_metrics(self) -> EvaluationMetricsResourceWithStreamingResponse:
        return EvaluationMetricsResourceWithStreamingResponse(self._evaluations.evaluation_metrics)

    @cached_property
    def hybrid_eval_metrics(self) -> HybridEvalMetricsResourceWithStreamingResponse:
        return HybridEvalMetricsResourceWithStreamingResponse(self._evaluations.hybrid_eval_metrics)

    @cached_property
    def test_case_results(self) -> TestCaseResultsResourceWithStreamingResponse:
        return TestCaseResultsResourceWithStreamingResponse(self._evaluations.test_case_results)


class AsyncEvaluationsResourceWithStreamingResponse:
    def __init__(self, evaluations: AsyncEvaluationsResource) -> None:
        self._evaluations = evaluations

        self.create = async_to_streamed_response_wrapper(
            evaluations.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluations.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            evaluations.update,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluations.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            evaluations.delete,
        )
        self.claim_task = async_to_streamed_response_wrapper(
            evaluations.claim_task,
        )

    @cached_property
    def tasks(self) -> AsyncTasksResourceWithStreamingResponse:
        return AsyncTasksResourceWithStreamingResponse(self._evaluations.tasks)

    @cached_property
    def contributor_metrics(self) -> AsyncContributorMetricsResourceWithStreamingResponse:
        return AsyncContributorMetricsResourceWithStreamingResponse(self._evaluations.contributor_metrics)

    @cached_property
    def evaluation_metrics(self) -> AsyncEvaluationMetricsResourceWithStreamingResponse:
        return AsyncEvaluationMetricsResourceWithStreamingResponse(self._evaluations.evaluation_metrics)

    @cached_property
    def hybrid_eval_metrics(self) -> AsyncHybridEvalMetricsResourceWithStreamingResponse:
        return AsyncHybridEvalMetricsResourceWithStreamingResponse(self._evaluations.hybrid_eval_metrics)

    @cached_property
    def test_case_results(self) -> AsyncTestCaseResultsResourceWithStreamingResponse:
        return AsyncTestCaseResultsResourceWithStreamingResponse(self._evaluations.test_case_results)
