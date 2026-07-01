# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, List, Union, Iterable, cast
from typing_extensions import Literal

import httpx

from .history import (
    HistoryResource,
    AsyncHistoryResource,
    HistoryResourceWithRawResponse,
    AsyncHistoryResourceWithRawResponse,
    HistoryResourceWithStreamingResponse,
    AsyncHistoryResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncPageResponse, AsyncPageResponse
from ...._base_client import AsyncPaginator, make_request_options
from ....types.evaluations import (
    test_case_result_list_params,
    test_case_result_batch_params,
    test_case_result_create_params,
    test_case_result_update_params,
    test_case_result_retrieve_params,
)
from ....types.evaluations.test_case_result import TestCaseResult
from ....types.evaluations.test_case_result_with_views import TestCaseResultWithViews
from ....types.evaluations.test_case_result_batch_response import TestCaseResultBatchResponse

__all__ = ["TestCaseResultsResource", "AsyncTestCaseResultsResource"]


class TestCaseResultsResource(SyncAPIResource):
    __test__ = False

    @cached_property
    def history(self) -> HistoryResource:
        return HistoryResource(self._client)

    @cached_property
    def with_raw_response(self) -> TestCaseResultsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return TestCaseResultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TestCaseResultsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return TestCaseResultsResourceWithStreamingResponse(self)

    def create(
        self,
        evaluation_id: str,
        *,
        application_spec_id: str,
        evaluation_dataset_version_num: str,
        test_case_evaluation_data: Dict[str, object],
        test_case_id: str,
        account_id: str | Omit = omit,
        annotated_by_identity_type: Literal["user", "service_account"] | Omit = omit,
        annotated_by_user_id: str | Omit = omit,
        audit_comment: str | Omit = omit,
        audit_required: bool | Omit = omit,
        audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"] | Omit = omit,
        edited_by_identity_type: Literal["user", "service_account"] | Omit = omit,
        label_status: Literal["PENDING", "COMPLETED", "FAILED"] | Omit = omit,
        result: Dict[str, Union[str, bool, float, SequenceNotStr[Union[str, float, bool]]]] | Omit = omit,
        time_spent_labeling_s: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseResult:
        """
        ### Description

        Creates a test case result

        ### Details

        This API can be used to create a test case result. To use this API, review the
        request schema and pass in all fields that are required to create a test case
        result.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return cast(
            TestCaseResult,
            self._post(
                path_template("/v4/evaluations/{evaluation_id}/test-case-results", evaluation_id=evaluation_id),
                body=maybe_transform(
                    {
                        "application_spec_id": application_spec_id,
                        "evaluation_dataset_version_num": evaluation_dataset_version_num,
                        "test_case_evaluation_data": test_case_evaluation_data,
                        "test_case_id": test_case_id,
                        "account_id": account_id,
                        "annotated_by_identity_type": annotated_by_identity_type,
                        "annotated_by_user_id": annotated_by_user_id,
                        "audit_comment": audit_comment,
                        "audit_required": audit_required,
                        "audit_status": audit_status,
                        "edited_by_identity_type": edited_by_identity_type,
                        "label_status": label_status,
                        "result": result,
                        "time_spent_labeling_s": time_spent_labeling_s,
                    },
                    test_case_result_create_params.TestCaseResultCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCaseResult),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        test_case_result_id: str,
        *,
        evaluation_id: str,
        view: List[
            Literal["AnnotationResults", "AuditTasks", "CustomMetrics", "Metrics", "Task", "TestCaseVersion", "Trace"]
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseResultWithViews:
        """
        ### Description

        Gets the details of a test case result

        ### Details

        This API can be used to get information about a single test case result by ID.
        To use this API, pass in the `id` that was returned from your Create Test Case
        Result API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not test_case_result_id:
            raise ValueError(
                f"Expected a non-empty value for `test_case_result_id` but received {test_case_result_id!r}"
            )
        return cast(
            TestCaseResultWithViews,
            self._get(
                path_template(
                    "/v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}",
                    evaluation_id=evaluation_id,
                    test_case_result_id=test_case_result_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {"view": view}, test_case_result_retrieve_params.TestCaseResultRetrieveParams
                    ),
                ),
                cast_to=cast(
                    Any, TestCaseResultWithViews
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def update(
        self,
        test_case_result_id: str,
        *,
        evaluation_id: str,
        account_id: str | Omit = omit,
        annotated_by_identity_type: Literal["user", "service_account"] | Omit = omit,
        annotated_by_user_id: str | Omit = omit,
        application_spec_id: str | Omit = omit,
        audit_comment: str | Omit = omit,
        audit_required: bool | Omit = omit,
        audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"] | Omit = omit,
        edited_by_identity_type: Literal["user", "service_account"] | Omit = omit,
        evaluation_dataset_version_num: str | Omit = omit,
        label_status: Literal["PENDING", "COMPLETED", "FAILED"] | Omit = omit,
        result: Dict[str, Union[str, bool, float, SequenceNotStr[Union[str, float, bool]]]] | Omit = omit,
        test_case_evaluation_data: Dict[str, object] | Omit = omit,
        test_case_id: str | Omit = omit,
        time_spent_labeling_s: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseResult:
        """
        ### Description

        Updates a test case result

        ### Details

        This API can be used to update the test case result that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Test Case Result API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not test_case_result_id:
            raise ValueError(
                f"Expected a non-empty value for `test_case_result_id` but received {test_case_result_id!r}"
            )
        return cast(
            TestCaseResult,
            self._patch(
                path_template(
                    "/v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}",
                    evaluation_id=evaluation_id,
                    test_case_result_id=test_case_result_id,
                ),
                body=maybe_transform(
                    {
                        "account_id": account_id,
                        "annotated_by_identity_type": annotated_by_identity_type,
                        "annotated_by_user_id": annotated_by_user_id,
                        "application_spec_id": application_spec_id,
                        "audit_comment": audit_comment,
                        "audit_required": audit_required,
                        "audit_status": audit_status,
                        "edited_by_identity_type": edited_by_identity_type,
                        "evaluation_dataset_version_num": evaluation_dataset_version_num,
                        "label_status": label_status,
                        "result": result,
                        "test_case_evaluation_data": test_case_evaluation_data,
                        "test_case_id": test_case_id,
                        "time_spent_labeling_s": time_spent_labeling_s,
                    },
                    test_case_result_update_params.TestCaseResultUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCaseResult),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        evaluation_id: str,
        *,
        account_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        view: List[
            Literal["AnnotationResults", "AuditTasks", "CustomMetrics", "Metrics", "Task", "TestCaseVersion", "Trace"]
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[TestCaseResultWithViews]:
        """
        ### Description

        Lists all test case results accessible to the user.

        ### Details

        This API can be used to list test case results. If a user has access to multiple
        accounts, all test case results from all accounts the user is associated with
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
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get_api_list(
            path_template("/v4/evaluations/{evaluation_id}/test-case-results", evaluation_id=evaluation_id),
            page=SyncPageResponse[TestCaseResultWithViews],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                        "view": view,
                    },
                    test_case_result_list_params.TestCaseResultListParams,
                ),
            ),
            model=cast(Any, TestCaseResultWithViews),  # Union types cannot be passed in as arguments in the type system
        )

    def batch(
        self,
        evaluation_id: str,
        *,
        items: Iterable[test_case_result_batch_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseResultBatchResponse:
        """
        ### Description

        Creates a batch of test case results

        ### Details

        This API can be used to create multiple test case results so users do not have
        to the incur the cost of repeated network calls. To use this API, pass in a list
        of test case results in the request body.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._post(
            path_template("/v4/evaluations/{evaluation_id}/test-case-results/batch", evaluation_id=evaluation_id),
            body=maybe_transform(items, Iterable[test_case_result_batch_params.Item]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseResultBatchResponse,
        )


class AsyncTestCaseResultsResource(AsyncAPIResource):
    @cached_property
    def history(self) -> AsyncHistoryResource:
        return AsyncHistoryResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTestCaseResultsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTestCaseResultsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTestCaseResultsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncTestCaseResultsResourceWithStreamingResponse(self)

    async def create(
        self,
        evaluation_id: str,
        *,
        application_spec_id: str,
        evaluation_dataset_version_num: str,
        test_case_evaluation_data: Dict[str, object],
        test_case_id: str,
        account_id: str | Omit = omit,
        annotated_by_identity_type: Literal["user", "service_account"] | Omit = omit,
        annotated_by_user_id: str | Omit = omit,
        audit_comment: str | Omit = omit,
        audit_required: bool | Omit = omit,
        audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"] | Omit = omit,
        edited_by_identity_type: Literal["user", "service_account"] | Omit = omit,
        label_status: Literal["PENDING", "COMPLETED", "FAILED"] | Omit = omit,
        result: Dict[str, Union[str, bool, float, SequenceNotStr[Union[str, float, bool]]]] | Omit = omit,
        time_spent_labeling_s: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseResult:
        """
        ### Description

        Creates a test case result

        ### Details

        This API can be used to create a test case result. To use this API, review the
        request schema and pass in all fields that are required to create a test case
        result.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return cast(
            TestCaseResult,
            await self._post(
                path_template("/v4/evaluations/{evaluation_id}/test-case-results", evaluation_id=evaluation_id),
                body=await async_maybe_transform(
                    {
                        "application_spec_id": application_spec_id,
                        "evaluation_dataset_version_num": evaluation_dataset_version_num,
                        "test_case_evaluation_data": test_case_evaluation_data,
                        "test_case_id": test_case_id,
                        "account_id": account_id,
                        "annotated_by_identity_type": annotated_by_identity_type,
                        "annotated_by_user_id": annotated_by_user_id,
                        "audit_comment": audit_comment,
                        "audit_required": audit_required,
                        "audit_status": audit_status,
                        "edited_by_identity_type": edited_by_identity_type,
                        "label_status": label_status,
                        "result": result,
                        "time_spent_labeling_s": time_spent_labeling_s,
                    },
                    test_case_result_create_params.TestCaseResultCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCaseResult),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        test_case_result_id: str,
        *,
        evaluation_id: str,
        view: List[
            Literal["AnnotationResults", "AuditTasks", "CustomMetrics", "Metrics", "Task", "TestCaseVersion", "Trace"]
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseResultWithViews:
        """
        ### Description

        Gets the details of a test case result

        ### Details

        This API can be used to get information about a single test case result by ID.
        To use this API, pass in the `id` that was returned from your Create Test Case
        Result API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not test_case_result_id:
            raise ValueError(
                f"Expected a non-empty value for `test_case_result_id` but received {test_case_result_id!r}"
            )
        return cast(
            TestCaseResultWithViews,
            await self._get(
                path_template(
                    "/v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}",
                    evaluation_id=evaluation_id,
                    test_case_result_id=test_case_result_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {"view": view}, test_case_result_retrieve_params.TestCaseResultRetrieveParams
                    ),
                ),
                cast_to=cast(
                    Any, TestCaseResultWithViews
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def update(
        self,
        test_case_result_id: str,
        *,
        evaluation_id: str,
        account_id: str | Omit = omit,
        annotated_by_identity_type: Literal["user", "service_account"] | Omit = omit,
        annotated_by_user_id: str | Omit = omit,
        application_spec_id: str | Omit = omit,
        audit_comment: str | Omit = omit,
        audit_required: bool | Omit = omit,
        audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"] | Omit = omit,
        edited_by_identity_type: Literal["user", "service_account"] | Omit = omit,
        evaluation_dataset_version_num: str | Omit = omit,
        label_status: Literal["PENDING", "COMPLETED", "FAILED"] | Omit = omit,
        result: Dict[str, Union[str, bool, float, SequenceNotStr[Union[str, float, bool]]]] | Omit = omit,
        test_case_evaluation_data: Dict[str, object] | Omit = omit,
        test_case_id: str | Omit = omit,
        time_spent_labeling_s: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseResult:
        """
        ### Description

        Updates a test case result

        ### Details

        This API can be used to update the test case result that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Test Case Result API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        if not test_case_result_id:
            raise ValueError(
                f"Expected a non-empty value for `test_case_result_id` but received {test_case_result_id!r}"
            )
        return cast(
            TestCaseResult,
            await self._patch(
                path_template(
                    "/v4/evaluations/{evaluation_id}/test-case-results/{test_case_result_id}",
                    evaluation_id=evaluation_id,
                    test_case_result_id=test_case_result_id,
                ),
                body=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "annotated_by_identity_type": annotated_by_identity_type,
                        "annotated_by_user_id": annotated_by_user_id,
                        "application_spec_id": application_spec_id,
                        "audit_comment": audit_comment,
                        "audit_required": audit_required,
                        "audit_status": audit_status,
                        "edited_by_identity_type": edited_by_identity_type,
                        "evaluation_dataset_version_num": evaluation_dataset_version_num,
                        "label_status": label_status,
                        "result": result,
                        "test_case_evaluation_data": test_case_evaluation_data,
                        "test_case_id": test_case_id,
                        "time_spent_labeling_s": time_spent_labeling_s,
                    },
                    test_case_result_update_params.TestCaseResultUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCaseResult),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        evaluation_id: str,
        *,
        account_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        view: List[
            Literal["AnnotationResults", "AuditTasks", "CustomMetrics", "Metrics", "Task", "TestCaseVersion", "Trace"]
        ]
        | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[TestCaseResultWithViews, AsyncPageResponse[TestCaseResultWithViews]]:
        """
        ### Description

        Lists all test case results accessible to the user.

        ### Details

        This API can be used to list test case results. If a user has access to multiple
        accounts, all test case results from all accounts the user is associated with
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
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return self._get_api_list(
            path_template("/v4/evaluations/{evaluation_id}/test-case-results", evaluation_id=evaluation_id),
            page=AsyncPageResponse[TestCaseResultWithViews],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "include_archived": include_archived,
                        "limit": limit,
                        "page": page,
                        "view": view,
                    },
                    test_case_result_list_params.TestCaseResultListParams,
                ),
            ),
            model=cast(Any, TestCaseResultWithViews),  # Union types cannot be passed in as arguments in the type system
        )

    async def batch(
        self,
        evaluation_id: str,
        *,
        items: Iterable[test_case_result_batch_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseResultBatchResponse:
        """
        ### Description

        Creates a batch of test case results

        ### Details

        This API can be used to create multiple test case results so users do not have
        to the incur the cost of repeated network calls. To use this API, pass in a list
        of test case results in the request body.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_id:
            raise ValueError(f"Expected a non-empty value for `evaluation_id` but received {evaluation_id!r}")
        return await self._post(
            path_template("/v4/evaluations/{evaluation_id}/test-case-results/batch", evaluation_id=evaluation_id),
            body=await async_maybe_transform(items, Iterable[test_case_result_batch_params.Item]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseResultBatchResponse,
        )


class TestCaseResultsResourceWithRawResponse:
    __test__ = False

    def __init__(self, test_case_results: TestCaseResultsResource) -> None:
        self._test_case_results = test_case_results

        self.create = to_raw_response_wrapper(
            test_case_results.create,
        )
        self.retrieve = to_raw_response_wrapper(
            test_case_results.retrieve,
        )
        self.update = to_raw_response_wrapper(
            test_case_results.update,
        )
        self.list = to_raw_response_wrapper(
            test_case_results.list,
        )
        self.batch = to_raw_response_wrapper(
            test_case_results.batch,
        )

    @cached_property
    def history(self) -> HistoryResourceWithRawResponse:
        return HistoryResourceWithRawResponse(self._test_case_results.history)


class AsyncTestCaseResultsResourceWithRawResponse:
    def __init__(self, test_case_results: AsyncTestCaseResultsResource) -> None:
        self._test_case_results = test_case_results

        self.create = async_to_raw_response_wrapper(
            test_case_results.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            test_case_results.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            test_case_results.update,
        )
        self.list = async_to_raw_response_wrapper(
            test_case_results.list,
        )
        self.batch = async_to_raw_response_wrapper(
            test_case_results.batch,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithRawResponse:
        return AsyncHistoryResourceWithRawResponse(self._test_case_results.history)


class TestCaseResultsResourceWithStreamingResponse:
    __test__ = False

    def __init__(self, test_case_results: TestCaseResultsResource) -> None:
        self._test_case_results = test_case_results

        self.create = to_streamed_response_wrapper(
            test_case_results.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            test_case_results.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            test_case_results.update,
        )
        self.list = to_streamed_response_wrapper(
            test_case_results.list,
        )
        self.batch = to_streamed_response_wrapper(
            test_case_results.batch,
        )

    @cached_property
    def history(self) -> HistoryResourceWithStreamingResponse:
        return HistoryResourceWithStreamingResponse(self._test_case_results.history)


class AsyncTestCaseResultsResourceWithStreamingResponse:
    def __init__(self, test_case_results: AsyncTestCaseResultsResource) -> None:
        self._test_case_results = test_case_results

        self.create = async_to_streamed_response_wrapper(
            test_case_results.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            test_case_results.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            test_case_results.update,
        )
        self.list = async_to_streamed_response_wrapper(
            test_case_results.list,
        )
        self.batch = async_to_streamed_response_wrapper(
            test_case_results.batch,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithStreamingResponse:
        return AsyncHistoryResourceWithStreamingResponse(self._test_case_results.history)
