# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, Dict, Iterable, cast
from typing_extensions import Literal, overload

import httpx

from .history import (
    HistoryResource,
    AsyncHistoryResource,
    HistoryResourceWithRawResponse,
    AsyncHistoryResourceWithRawResponse,
    HistoryResourceWithStreamingResponse,
    AsyncHistoryResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, required_args, maybe_transform, async_maybe_transform
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
from ....types.evaluation_datasets import (
    test_case_list_params,
    test_case_batch_params,
    test_case_create_params,
    test_case_update_params,
)
from ....types.evaluation_datasets.test_case import TestCase
from ....types.shared.generic_delete_response import GenericDeleteResponse
from ....types.evaluation_datasets.test_case_batch_response import TestCaseBatchResponse

__all__ = ["TestCasesResource", "AsyncTestCasesResource"]


class TestCasesResource(SyncAPIResource):
    __test__ = False

    @cached_property
    def history(self) -> HistoryResource:
        return HistoryResource(self._client)

    @cached_property
    def with_raw_response(self) -> TestCasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return TestCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TestCasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return TestCasesResourceWithStreamingResponse(self)

    def create(
        self,
        evaluation_dataset_id: str,
        *,
        test_case_data: test_case_create_params.TestCaseData,
        account_id: str | Omit = omit,
        chat_history: Dict[str, object] | Omit = omit,
        test_case_metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        """
        ### Description

        Create a test case for a selected dataset.

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
        return cast(
            TestCase,
            self._post(
                path_template(
                    "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases",
                    evaluation_dataset_id=evaluation_dataset_id,
                ),
                body=maybe_transform(
                    {
                        "test_case_data": test_case_data,
                        "account_id": account_id,
                        "chat_history": chat_history,
                        "test_case_metadata": test_case_metadata,
                    },
                    test_case_create_params.TestCaseCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCase),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        """
        ### Description

        Get the test case by its id.

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
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return cast(
            TestCase,
            self._get(
                path_template(
                    "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
                    evaluation_dataset_id=evaluation_dataset_id,
                    test_case_id=test_case_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCase),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        account_id: str | Omit = omit,
        chat_history: Dict[str, object] | Omit = omit,
        restore: Literal[False] | Omit = omit,
        test_case_data: test_case_update_params.PartialTestCaseVersionRequestTestCaseData | Omit = omit,
        test_case_metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        """
        ### Description

        Update a test case.

        Args:
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
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        """
        ### Description

        Update a test case.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["evaluation_dataset_id"], ["evaluation_dataset_id", "restore"])
    def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        account_id: str | Omit = omit,
        chat_history: Dict[str, object] | Omit = omit,
        restore: Literal[False] | Literal[True] | Omit = omit,
        test_case_data: test_case_update_params.PartialTestCaseVersionRequestTestCaseData | Omit = omit,
        test_case_metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return cast(
            TestCase,
            self._patch(
                path_template(
                    "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
                    evaluation_dataset_id=evaluation_dataset_id,
                    test_case_id=test_case_id,
                ),
                body=maybe_transform(
                    {
                        "account_id": account_id,
                        "chat_history": chat_history,
                        "restore": restore,
                        "test_case_data": test_case_data,
                        "test_case_metadata": test_case_metadata,
                    },
                    test_case_update_params.TestCaseUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCase),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        evaluation_dataset_id: str,
        *,
        account_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[TestCase]:
        """
        ### Description

        List all test cases for a selected dataset.

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
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        return self._get_api_list(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases",
                evaluation_dataset_id=evaluation_dataset_id,
            ),
            page=SyncPageResponse[TestCase],
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
                    },
                    test_case_list_params.TestCaseListParams,
                ),
            ),
            model=cast(Any, TestCase),  # Union types cannot be passed in as arguments in the type system
        )

    def delete(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Delete a specified test case -- retaining older version belonging to older
        dataset versions.

        ### Details

        This request shouldn't be used when deleting due to compliance reasons. See Wipe
        action.

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
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return self._delete(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
                evaluation_dataset_id=evaluation_dataset_id,
                test_case_id=test_case_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )

    def batch(
        self,
        evaluation_dataset_id: str,
        *,
        items: Iterable[test_case_batch_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseBatchResponse:
        """
        ### Description

        Creates a batch of test cases

        ### Details

        This API can be used to create multiple test cases so users do not have to the
        incur the cost of repeated network calls. To use this API, pass in a list of
        test cases in the request body.

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
        return self._post(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/batch",
                evaluation_dataset_id=evaluation_dataset_id,
            ),
            body=maybe_transform(items, Iterable[test_case_batch_params.Item]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseBatchResponse,
        )


class AsyncTestCasesResource(AsyncAPIResource):
    @cached_property
    def history(self) -> AsyncHistoryResource:
        return AsyncHistoryResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTestCasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTestCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTestCasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncTestCasesResourceWithStreamingResponse(self)

    async def create(
        self,
        evaluation_dataset_id: str,
        *,
        test_case_data: test_case_create_params.TestCaseData,
        account_id: str | Omit = omit,
        chat_history: Dict[str, object] | Omit = omit,
        test_case_metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        """
        ### Description

        Create a test case for a selected dataset.

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
        return cast(
            TestCase,
            await self._post(
                path_template(
                    "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases",
                    evaluation_dataset_id=evaluation_dataset_id,
                ),
                body=await async_maybe_transform(
                    {
                        "test_case_data": test_case_data,
                        "account_id": account_id,
                        "chat_history": chat_history,
                        "test_case_metadata": test_case_metadata,
                    },
                    test_case_create_params.TestCaseCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCase),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        """
        ### Description

        Get the test case by its id.

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
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return cast(
            TestCase,
            await self._get(
                path_template(
                    "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
                    evaluation_dataset_id=evaluation_dataset_id,
                    test_case_id=test_case_id,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCase),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    async def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        account_id: str | Omit = omit,
        chat_history: Dict[str, object] | Omit = omit,
        restore: Literal[False] | Omit = omit,
        test_case_data: test_case_update_params.PartialTestCaseVersionRequestTestCaseData | Omit = omit,
        test_case_metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        """
        ### Description

        Update a test case.

        Args:
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
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        """
        ### Description

        Update a test case.

        Args:
          restore: Set to true to restore the entity from the database.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["evaluation_dataset_id"], ["evaluation_dataset_id", "restore"])
    async def update(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        account_id: str | Omit = omit,
        chat_history: Dict[str, object] | Omit = omit,
        restore: Literal[False] | Literal[True] | Omit = omit,
        test_case_data: test_case_update_params.PartialTestCaseVersionRequestTestCaseData | Omit = omit,
        test_case_metadata: Dict[str, object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCase:
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return cast(
            TestCase,
            await self._patch(
                path_template(
                    "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
                    evaluation_dataset_id=evaluation_dataset_id,
                    test_case_id=test_case_id,
                ),
                body=await async_maybe_transform(
                    {
                        "account_id": account_id,
                        "chat_history": chat_history,
                        "restore": restore,
                        "test_case_data": test_case_data,
                        "test_case_metadata": test_case_metadata,
                    },
                    test_case_update_params.TestCaseUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, TestCase),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        evaluation_dataset_id: str,
        *,
        account_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[TestCase, AsyncPageResponse[TestCase]]:
        """
        ### Description

        List all test cases for a selected dataset.

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
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        return self._get_api_list(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases",
                evaluation_dataset_id=evaluation_dataset_id,
            ),
            page=AsyncPageResponse[TestCase],
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
                    },
                    test_case_list_params.TestCaseListParams,
                ),
            ),
            model=cast(Any, TestCase),  # Union types cannot be passed in as arguments in the type system
        )

    async def delete(
        self,
        test_case_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GenericDeleteResponse:
        """
        ### Description

        Delete a specified test case -- retaining older version belonging to older
        dataset versions.

        ### Details

        This request shouldn't be used when deleting due to compliance reasons. See Wipe
        action.

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
        if not test_case_id:
            raise ValueError(f"Expected a non-empty value for `test_case_id` but received {test_case_id!r}")
        return await self._delete(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/{test_case_id}",
                evaluation_dataset_id=evaluation_dataset_id,
                test_case_id=test_case_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )

    async def batch(
        self,
        evaluation_dataset_id: str,
        *,
        items: Iterable[test_case_batch_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> TestCaseBatchResponse:
        """
        ### Description

        Creates a batch of test cases

        ### Details

        This API can be used to create multiple test cases so users do not have to the
        incur the cost of repeated network calls. To use this API, pass in a list of
        test cases in the request body.

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
        return await self._post(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/test-cases/batch",
                evaluation_dataset_id=evaluation_dataset_id,
            ),
            body=await async_maybe_transform(items, Iterable[test_case_batch_params.Item]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TestCaseBatchResponse,
        )


class TestCasesResourceWithRawResponse:
    __test__ = False

    def __init__(self, test_cases: TestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = to_raw_response_wrapper(
            test_cases.create,
        )
        self.retrieve = to_raw_response_wrapper(
            test_cases.retrieve,
        )
        self.update = to_raw_response_wrapper(
            test_cases.update,
        )
        self.list = to_raw_response_wrapper(
            test_cases.list,
        )
        self.delete = to_raw_response_wrapper(
            test_cases.delete,
        )
        self.batch = to_raw_response_wrapper(
            test_cases.batch,
        )

    @cached_property
    def history(self) -> HistoryResourceWithRawResponse:
        return HistoryResourceWithRawResponse(self._test_cases.history)


class AsyncTestCasesResourceWithRawResponse:
    def __init__(self, test_cases: AsyncTestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = async_to_raw_response_wrapper(
            test_cases.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            test_cases.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            test_cases.update,
        )
        self.list = async_to_raw_response_wrapper(
            test_cases.list,
        )
        self.delete = async_to_raw_response_wrapper(
            test_cases.delete,
        )
        self.batch = async_to_raw_response_wrapper(
            test_cases.batch,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithRawResponse:
        return AsyncHistoryResourceWithRawResponse(self._test_cases.history)


class TestCasesResourceWithStreamingResponse:
    __test__ = False

    def __init__(self, test_cases: TestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = to_streamed_response_wrapper(
            test_cases.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            test_cases.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            test_cases.update,
        )
        self.list = to_streamed_response_wrapper(
            test_cases.list,
        )
        self.delete = to_streamed_response_wrapper(
            test_cases.delete,
        )
        self.batch = to_streamed_response_wrapper(
            test_cases.batch,
        )

    @cached_property
    def history(self) -> HistoryResourceWithStreamingResponse:
        return HistoryResourceWithStreamingResponse(self._test_cases.history)


class AsyncTestCasesResourceWithStreamingResponse:
    def __init__(self, test_cases: AsyncTestCasesResource) -> None:
        self._test_cases = test_cases

        self.create = async_to_streamed_response_wrapper(
            test_cases.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            test_cases.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            test_cases.update,
        )
        self.list = async_to_streamed_response_wrapper(
            test_cases.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            test_cases.delete,
        )
        self.batch = async_to_streamed_response_wrapper(
            test_cases.batch,
        )

    @cached_property
    def history(self) -> AsyncHistoryResourceWithStreamingResponse:
        return AsyncHistoryResourceWithStreamingResponse(self._test_cases.history)
