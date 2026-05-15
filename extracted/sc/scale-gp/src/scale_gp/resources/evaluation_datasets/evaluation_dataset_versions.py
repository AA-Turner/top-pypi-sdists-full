# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime

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
from ...pagination import SyncPageResponse, AsyncPageResponse
from ..._base_client import AsyncPaginator, make_request_options
from ...types.evaluation_datasets import (
    evaluation_dataset_version_list_params,
    evaluation_dataset_version_create_params,
    evaluation_dataset_version_publish_params,
)
from ...types.publish_evaluation_dataset_draft_response import PublishEvaluationDatasetDraftResponse
from ...types.evaluation_datasets.evaluation_dataset_version import EvaluationDatasetVersion

__all__ = ["EvaluationDatasetVersionsResource", "AsyncEvaluationDatasetVersionsResource"]


class EvaluationDatasetVersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluationDatasetVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return EvaluationDatasetVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationDatasetVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return EvaluationDatasetVersionsResourceWithStreamingResponse(self)

    def create(
        self,
        evaluation_dataset_id: str,
        *,
        account_id: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDatasetVersion:
        """
        ### Description

        Creates a evaluation dataset version

        ### Details

        This API can be used to create a evaluation dataset version. To use this API,
        review the request schema and pass in all fields that are required to create a
        evaluation dataset version.

        Args:
          account_id: The ID of the account that owns the given entity.

          draft: Boolean to check whether or not the evaluation dataset is in draft mode

          published_at: The date and time that all test case results for the evaluation were completed
              for the evaluation in ISO format.

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
                "/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions",
                evaluation_dataset_id=evaluation_dataset_id,
            ),
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "draft": draft,
                    "published_at": published_at,
                },
                evaluation_dataset_version_create_params.EvaluationDatasetVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetVersion,
        )

    def retrieve(
        self,
        evaluation_dataset_version_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDatasetVersion:
        """
        ### Description

        Gets the details of a evaluation dataset version

        ### Details

        This API can be used to get information about a single evaluation dataset
        version by ID. To use this API, pass in the `id` that was returned from your
        Create Evaluation Dataset Version API call as a path parameter.

        Review the response schema to see the fields that will be returned.

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
        if not evaluation_dataset_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_version_id` but received {evaluation_dataset_version_id!r}"
            )
        return self._get(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions/{evaluation_dataset_version_id}",
                evaluation_dataset_id=evaluation_dataset_id,
                evaluation_dataset_version_id=evaluation_dataset_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetVersion,
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
    ) -> SyncPageResponse[EvaluationDatasetVersion]:
        """
        ### Description

        Lists all evaluation dataset versions accessible to the user.

        ### Details

        This API can be used to list evaluation dataset versions. If a user has access
        to multiple accounts, all evaluation dataset versions from all accounts the user
        is associated with will be returned.

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
                "/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions",
                evaluation_dataset_id=evaluation_dataset_id,
            ),
            page=SyncPageResponse[EvaluationDatasetVersion],
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
                    evaluation_dataset_version_list_params.EvaluationDatasetVersionListParams,
                ),
            ),
            model=EvaluationDatasetVersion,
        )

    def publish(
        self,
        evaluation_dataset_version_id: str,
        *,
        evaluation_dataset_id: str,
        force: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PublishEvaluationDatasetDraftResponse:
        """
        Publish Evaluation Dataset Version

        Args:
          force: Force approve an evaluation dataset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not evaluation_dataset_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_version_id` but received {evaluation_dataset_version_id!r}"
            )
        return self._post(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions/{evaluation_dataset_version_id}/publish",
                evaluation_dataset_id=evaluation_dataset_id,
                evaluation_dataset_version_id=evaluation_dataset_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"force": force}, evaluation_dataset_version_publish_params.EvaluationDatasetVersionPublishParams
                ),
            ),
            cast_to=PublishEvaluationDatasetDraftResponse,
        )


class AsyncEvaluationDatasetVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluationDatasetVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationDatasetVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationDatasetVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncEvaluationDatasetVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        evaluation_dataset_id: str,
        *,
        account_id: str | Omit = omit,
        draft: bool | Omit = omit,
        published_at: Union[str, datetime] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDatasetVersion:
        """
        ### Description

        Creates a evaluation dataset version

        ### Details

        This API can be used to create a evaluation dataset version. To use this API,
        review the request schema and pass in all fields that are required to create a
        evaluation dataset version.

        Args:
          account_id: The ID of the account that owns the given entity.

          draft: Boolean to check whether or not the evaluation dataset is in draft mode

          published_at: The date and time that all test case results for the evaluation were completed
              for the evaluation in ISO format.

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
                "/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions",
                evaluation_dataset_id=evaluation_dataset_id,
            ),
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "draft": draft,
                    "published_at": published_at,
                },
                evaluation_dataset_version_create_params.EvaluationDatasetVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetVersion,
        )

    async def retrieve(
        self,
        evaluation_dataset_version_id: str,
        *,
        evaluation_dataset_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationDatasetVersion:
        """
        ### Description

        Gets the details of a evaluation dataset version

        ### Details

        This API can be used to get information about a single evaluation dataset
        version by ID. To use this API, pass in the `id` that was returned from your
        Create Evaluation Dataset Version API call as a path parameter.

        Review the response schema to see the fields that will be returned.

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
        if not evaluation_dataset_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_version_id` but received {evaluation_dataset_version_id!r}"
            )
        return await self._get(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions/{evaluation_dataset_version_id}",
                evaluation_dataset_id=evaluation_dataset_id,
                evaluation_dataset_version_id=evaluation_dataset_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationDatasetVersion,
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
    ) -> AsyncPaginator[EvaluationDatasetVersion, AsyncPageResponse[EvaluationDatasetVersion]]:
        """
        ### Description

        Lists all evaluation dataset versions accessible to the user.

        ### Details

        This API can be used to list evaluation dataset versions. If a user has access
        to multiple accounts, all evaluation dataset versions from all accounts the user
        is associated with will be returned.

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
                "/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions",
                evaluation_dataset_id=evaluation_dataset_id,
            ),
            page=AsyncPageResponse[EvaluationDatasetVersion],
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
                    evaluation_dataset_version_list_params.EvaluationDatasetVersionListParams,
                ),
            ),
            model=EvaluationDatasetVersion,
        )

    async def publish(
        self,
        evaluation_dataset_version_id: str,
        *,
        evaluation_dataset_id: str,
        force: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PublishEvaluationDatasetDraftResponse:
        """
        Publish Evaluation Dataset Version

        Args:
          force: Force approve an evaluation dataset

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_dataset_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_id` but received {evaluation_dataset_id!r}"
            )
        if not evaluation_dataset_version_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_dataset_version_id` but received {evaluation_dataset_version_id!r}"
            )
        return await self._post(
            path_template(
                "/v4/evaluation-datasets/{evaluation_dataset_id}/evaluation-dataset-versions/{evaluation_dataset_version_id}/publish",
                evaluation_dataset_id=evaluation_dataset_id,
                evaluation_dataset_version_id=evaluation_dataset_version_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"force": force}, evaluation_dataset_version_publish_params.EvaluationDatasetVersionPublishParams
                ),
            ),
            cast_to=PublishEvaluationDatasetDraftResponse,
        )


class EvaluationDatasetVersionsResourceWithRawResponse:
    def __init__(self, evaluation_dataset_versions: EvaluationDatasetVersionsResource) -> None:
        self._evaluation_dataset_versions = evaluation_dataset_versions

        self.create = to_raw_response_wrapper(
            evaluation_dataset_versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluation_dataset_versions.retrieve,
        )
        self.list = to_raw_response_wrapper(
            evaluation_dataset_versions.list,
        )
        self.publish = to_raw_response_wrapper(
            evaluation_dataset_versions.publish,
        )


class AsyncEvaluationDatasetVersionsResourceWithRawResponse:
    def __init__(self, evaluation_dataset_versions: AsyncEvaluationDatasetVersionsResource) -> None:
        self._evaluation_dataset_versions = evaluation_dataset_versions

        self.create = async_to_raw_response_wrapper(
            evaluation_dataset_versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluation_dataset_versions.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            evaluation_dataset_versions.list,
        )
        self.publish = async_to_raw_response_wrapper(
            evaluation_dataset_versions.publish,
        )


class EvaluationDatasetVersionsResourceWithStreamingResponse:
    def __init__(self, evaluation_dataset_versions: EvaluationDatasetVersionsResource) -> None:
        self._evaluation_dataset_versions = evaluation_dataset_versions

        self.create = to_streamed_response_wrapper(
            evaluation_dataset_versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluation_dataset_versions.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            evaluation_dataset_versions.list,
        )
        self.publish = to_streamed_response_wrapper(
            evaluation_dataset_versions.publish,
        )


class AsyncEvaluationDatasetVersionsResourceWithStreamingResponse:
    def __init__(self, evaluation_dataset_versions: AsyncEvaluationDatasetVersionsResource) -> None:
        self._evaluation_dataset_versions = evaluation_dataset_versions

        self.create = async_to_streamed_response_wrapper(
            evaluation_dataset_versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluation_dataset_versions.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluation_dataset_versions.list,
        )
        self.publish = async_to_streamed_response_wrapper(
            evaluation_dataset_versions.publish,
        )
