# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, List, Union, Iterable, cast
from typing_extensions import Literal

import httpx

from ..types import (
    application_test_case_output_list_params,
    application_test_case_output_batch_params,
    application_test_case_output_retrieve_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncPageResponse, AsyncPageResponse
from .._base_client import AsyncPaginator, make_request_options
from ..types.application_test_case_output_batch_response import ApplicationTestCaseOutputBatchResponse
from ..types.application_test_case_output_retrieve_response import ApplicationTestCaseOutputRetrieveResponse
from ..types.paginated_application_test_case_output_with_views import Item

__all__ = ["ApplicationTestCaseOutputsResource", "AsyncApplicationTestCaseOutputsResource"]


class ApplicationTestCaseOutputsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ApplicationTestCaseOutputsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationTestCaseOutputsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationTestCaseOutputsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ApplicationTestCaseOutputsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        application_test_case_output_id: str,
        *,
        view: List[Literal["MetricScores", "TestCaseVersion", "Trace"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationTestCaseOutputRetrieveResponse:
        """
        ### Description

        Gets the details of a application test case output

        ### Details

        This API can be used to get information about a single application test case
        output by ID. To use this API, pass in the `id` that was returned from your
        Create Application Test Case Output API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_test_case_output_id:
            raise ValueError(
                f"Expected a non-empty value for `application_test_case_output_id` but received {application_test_case_output_id!r}"
            )
        return cast(
            ApplicationTestCaseOutputRetrieveResponse,
            self._get(
                f"/v4/application-test-case-outputs/{application_test_case_output_id}",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform(
                        {"view": view},
                        application_test_case_output_retrieve_params.ApplicationTestCaseOutputRetrieveParams,
                    ),
                ),
                cast_to=cast(
                    Any, ApplicationTestCaseOutputRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        application_test_case_output_group_id: Union[int, str] | Omit = omit,
        application_variant_id: Union[int, str] | Omit = omit,
        application_variant_report_id: Union[int, str] | Omit = omit,
        evaluation_dataset_id: Union[int, str] | Omit = omit,
        evaluation_dataset_version_num: Union[int, str] | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        view: List[Literal["MetricScores", "TestCaseVersion", "Trace"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[Item]:
        """
        ### Description

        Lists all application test case outputs accessible to the user.

        ### Details

        This API can be used to list application test case outputs. If a user has access
        to multiple accounts, all application test case outputs from all accounts the
        user is associated with will be returned.

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
            "/v4/application-test-case-outputs",
            page=SyncPageResponse[Item],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_test_case_output_group_id": application_test_case_output_group_id,
                        "application_variant_id": application_variant_id,
                        "application_variant_report_id": application_variant_report_id,
                        "evaluation_dataset_id": evaluation_dataset_id,
                        "evaluation_dataset_version_num": evaluation_dataset_version_num,
                        "limit": limit,
                        "page": page,
                        "view": view,
                    },
                    application_test_case_output_list_params.ApplicationTestCaseOutputListParams,
                ),
            ),
            model=cast(Any, Item),  # Union types cannot be passed in as arguments in the type system
        )

    def batch(
        self,
        *,
        items: Iterable[application_test_case_output_batch_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationTestCaseOutputBatchResponse:
        """
        ### Description

        Creates a batch of application test case outputs

        ### Details

        This API can be used to create multiple application test case outputs so users
        do not have to the incur the cost of repeated network calls. To use this API,
        pass in a list of application test case outputs in the request body.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/application-test-case-outputs/batch",
            body=maybe_transform(items, Iterable[application_test_case_output_batch_params.Item]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationTestCaseOutputBatchResponse,
        )


class AsyncApplicationTestCaseOutputsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncApplicationTestCaseOutputsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationTestCaseOutputsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationTestCaseOutputsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncApplicationTestCaseOutputsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        application_test_case_output_id: str,
        *,
        view: List[Literal["MetricScores", "TestCaseVersion", "Trace"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationTestCaseOutputRetrieveResponse:
        """
        ### Description

        Gets the details of a application test case output

        ### Details

        This API can be used to get information about a single application test case
        output by ID. To use this API, pass in the `id` that was returned from your
        Create Application Test Case Output API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_test_case_output_id:
            raise ValueError(
                f"Expected a non-empty value for `application_test_case_output_id` but received {application_test_case_output_id!r}"
            )
        return cast(
            ApplicationTestCaseOutputRetrieveResponse,
            await self._get(
                f"/v4/application-test-case-outputs/{application_test_case_output_id}",
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform(
                        {"view": view},
                        application_test_case_output_retrieve_params.ApplicationTestCaseOutputRetrieveParams,
                    ),
                ),
                cast_to=cast(
                    Any, ApplicationTestCaseOutputRetrieveResponse
                ),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        application_test_case_output_group_id: Union[int, str] | Omit = omit,
        application_variant_id: Union[int, str] | Omit = omit,
        application_variant_report_id: Union[int, str] | Omit = omit,
        evaluation_dataset_id: Union[int, str] | Omit = omit,
        evaluation_dataset_version_num: Union[int, str] | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        view: List[Literal["MetricScores", "TestCaseVersion", "Trace"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Item, AsyncPageResponse[Item]]:
        """
        ### Description

        Lists all application test case outputs accessible to the user.

        ### Details

        This API can be used to list application test case outputs. If a user has access
        to multiple accounts, all application test case outputs from all accounts the
        user is associated with will be returned.

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
            "/v4/application-test-case-outputs",
            page=AsyncPageResponse[Item],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "application_test_case_output_group_id": application_test_case_output_group_id,
                        "application_variant_id": application_variant_id,
                        "application_variant_report_id": application_variant_report_id,
                        "evaluation_dataset_id": evaluation_dataset_id,
                        "evaluation_dataset_version_num": evaluation_dataset_version_num,
                        "limit": limit,
                        "page": page,
                        "view": view,
                    },
                    application_test_case_output_list_params.ApplicationTestCaseOutputListParams,
                ),
            ),
            model=cast(Any, Item),  # Union types cannot be passed in as arguments in the type system
        )

    async def batch(
        self,
        *,
        items: Iterable[application_test_case_output_batch_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ApplicationTestCaseOutputBatchResponse:
        """
        ### Description

        Creates a batch of application test case outputs

        ### Details

        This API can be used to create multiple application test case outputs so users
        do not have to the incur the cost of repeated network calls. To use this API,
        pass in a list of application test case outputs in the request body.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/application-test-case-outputs/batch",
            body=await async_maybe_transform(items, Iterable[application_test_case_output_batch_params.Item]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationTestCaseOutputBatchResponse,
        )


class ApplicationTestCaseOutputsResourceWithRawResponse:
    def __init__(self, application_test_case_outputs: ApplicationTestCaseOutputsResource) -> None:
        self._application_test_case_outputs = application_test_case_outputs

        self.retrieve = to_raw_response_wrapper(
            application_test_case_outputs.retrieve,
        )
        self.list = to_raw_response_wrapper(
            application_test_case_outputs.list,
        )
        self.batch = to_raw_response_wrapper(
            application_test_case_outputs.batch,
        )


class AsyncApplicationTestCaseOutputsResourceWithRawResponse:
    def __init__(self, application_test_case_outputs: AsyncApplicationTestCaseOutputsResource) -> None:
        self._application_test_case_outputs = application_test_case_outputs

        self.retrieve = async_to_raw_response_wrapper(
            application_test_case_outputs.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            application_test_case_outputs.list,
        )
        self.batch = async_to_raw_response_wrapper(
            application_test_case_outputs.batch,
        )


class ApplicationTestCaseOutputsResourceWithStreamingResponse:
    def __init__(self, application_test_case_outputs: ApplicationTestCaseOutputsResource) -> None:
        self._application_test_case_outputs = application_test_case_outputs

        self.retrieve = to_streamed_response_wrapper(
            application_test_case_outputs.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            application_test_case_outputs.list,
        )
        self.batch = to_streamed_response_wrapper(
            application_test_case_outputs.batch,
        )


class AsyncApplicationTestCaseOutputsResourceWithStreamingResponse:
    def __init__(self, application_test_case_outputs: AsyncApplicationTestCaseOutputsResource) -> None:
        self._application_test_case_outputs = application_test_case_outputs

        self.retrieve = async_to_streamed_response_wrapper(
            application_test_case_outputs.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            application_test_case_outputs.list,
        )
        self.batch = async_to_streamed_response_wrapper(
            application_test_case_outputs.batch,
        )
