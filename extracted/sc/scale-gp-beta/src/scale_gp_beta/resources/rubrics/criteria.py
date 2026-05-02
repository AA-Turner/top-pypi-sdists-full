# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

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
from ...types.chat import SortOrder
from ..._base_client import make_request_options
from ...types.rubrics import criterion_create_params, criterion_update_params, criterion_list_versions_params
from ...types.chat.sort_order import SortOrder
from ...types.rubrics.rubric_criteria_response import RubricCriteriaResponse
from ...types.rubrics.criterion_list_versions_response import CriterionListVersionsResponse

__all__ = ["CriteriaResource", "AsyncCriteriaResource"]


class CriteriaResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CriteriaResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return CriteriaResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CriteriaResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return CriteriaResourceWithStreamingResponse(self)

    def create(
        self,
        rubric_id: str,
        *,
        title: str,
        annotations: Dict[str, object] | Omit = omit,
        weight: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricCriteriaResponse:
        """
        Add Criterion to Rubric

        Args:
          title: The Criteria text

          annotations: Free-form metadata for the Criteria

          weight: Weight multiplier for scoring

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        return self._post(
            path_template("/v5/rubrics/{rubric_id}/criteria", rubric_id=rubric_id),
            body=maybe_transform(
                {
                    "title": title,
                    "annotations": annotations,
                    "weight": weight,
                },
                criterion_create_params.CriterionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricCriteriaResponse,
        )

    def update(
        self,
        rubric_criteria_id: str,
        *,
        rubric_id: str,
        annotations: Dict[str, object] | Omit = omit,
        title: str | Omit = omit,
        weight: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricCriteriaResponse:
        """
        Update Criterion

        Args:
          annotations: Free-form metadata for the Criteria

          title: The Criteria text

          weight: Weight multiplier for scoring

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        if not rubric_criteria_id:
            raise ValueError(f"Expected a non-empty value for `rubric_criteria_id` but received {rubric_criteria_id!r}")
        return self._patch(
            path_template(
                "/v5/rubrics/{rubric_id}/criteria/{rubric_criteria_id}",
                rubric_id=rubric_id,
                rubric_criteria_id=rubric_criteria_id,
            ),
            body=maybe_transform(
                {
                    "annotations": annotations,
                    "title": title,
                    "weight": weight,
                },
                criterion_update_params.CriterionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricCriteriaResponse,
        )

    def list_versions(
        self,
        rubric_criteria_id: str,
        *,
        rubric_id: str,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CriterionListVersionsResponse:
        """
        List Criterion Versions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        if not rubric_criteria_id:
            raise ValueError(f"Expected a non-empty value for `rubric_criteria_id` but received {rubric_criteria_id!r}")
        return self._get(
            path_template(
                "/v5/rubrics/{rubric_id}/criteria/{rubric_criteria_id}/versions",
                rubric_id=rubric_id,
                rubric_criteria_id=rubric_criteria_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    criterion_list_versions_params.CriterionListVersionsParams,
                ),
            ),
            cast_to=CriterionListVersionsResponse,
        )


class AsyncCriteriaResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCriteriaResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncCriteriaResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCriteriaResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncCriteriaResourceWithStreamingResponse(self)

    async def create(
        self,
        rubric_id: str,
        *,
        title: str,
        annotations: Dict[str, object] | Omit = omit,
        weight: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricCriteriaResponse:
        """
        Add Criterion to Rubric

        Args:
          title: The Criteria text

          annotations: Free-form metadata for the Criteria

          weight: Weight multiplier for scoring

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        return await self._post(
            path_template("/v5/rubrics/{rubric_id}/criteria", rubric_id=rubric_id),
            body=await async_maybe_transform(
                {
                    "title": title,
                    "annotations": annotations,
                    "weight": weight,
                },
                criterion_create_params.CriterionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricCriteriaResponse,
        )

    async def update(
        self,
        rubric_criteria_id: str,
        *,
        rubric_id: str,
        annotations: Dict[str, object] | Omit = omit,
        title: str | Omit = omit,
        weight: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> RubricCriteriaResponse:
        """
        Update Criterion

        Args:
          annotations: Free-form metadata for the Criteria

          title: The Criteria text

          weight: Weight multiplier for scoring

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        if not rubric_criteria_id:
            raise ValueError(f"Expected a non-empty value for `rubric_criteria_id` but received {rubric_criteria_id!r}")
        return await self._patch(
            path_template(
                "/v5/rubrics/{rubric_id}/criteria/{rubric_criteria_id}",
                rubric_id=rubric_id,
                rubric_criteria_id=rubric_criteria_id,
            ),
            body=await async_maybe_transform(
                {
                    "annotations": annotations,
                    "title": title,
                    "weight": weight,
                },
                criterion_update_params.CriterionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RubricCriteriaResponse,
        )

    async def list_versions(
        self,
        rubric_criteria_id: str,
        *,
        rubric_id: str,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        sort_by: str | Omit = omit,
        sort_order: SortOrder | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CriterionListVersionsResponse:
        """
        List Criterion Versions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not rubric_id:
            raise ValueError(f"Expected a non-empty value for `rubric_id` but received {rubric_id!r}")
        if not rubric_criteria_id:
            raise ValueError(f"Expected a non-empty value for `rubric_criteria_id` but received {rubric_criteria_id!r}")
        return await self._get(
            path_template(
                "/v5/rubrics/{rubric_id}/criteria/{rubric_criteria_id}/versions",
                rubric_id=rubric_id,
                rubric_criteria_id=rubric_criteria_id,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    criterion_list_versions_params.CriterionListVersionsParams,
                ),
            ),
            cast_to=CriterionListVersionsResponse,
        )


class CriteriaResourceWithRawResponse:
    def __init__(self, criteria: CriteriaResource) -> None:
        self._criteria = criteria

        self.create = to_raw_response_wrapper(
            criteria.create,
        )
        self.update = to_raw_response_wrapper(
            criteria.update,
        )
        self.list_versions = to_raw_response_wrapper(
            criteria.list_versions,
        )


class AsyncCriteriaResourceWithRawResponse:
    def __init__(self, criteria: AsyncCriteriaResource) -> None:
        self._criteria = criteria

        self.create = async_to_raw_response_wrapper(
            criteria.create,
        )
        self.update = async_to_raw_response_wrapper(
            criteria.update,
        )
        self.list_versions = async_to_raw_response_wrapper(
            criteria.list_versions,
        )


class CriteriaResourceWithStreamingResponse:
    def __init__(self, criteria: CriteriaResource) -> None:
        self._criteria = criteria

        self.create = to_streamed_response_wrapper(
            criteria.create,
        )
        self.update = to_streamed_response_wrapper(
            criteria.update,
        )
        self.list_versions = to_streamed_response_wrapper(
            criteria.list_versions,
        )


class AsyncCriteriaResourceWithStreamingResponse:
    def __init__(self, criteria: AsyncCriteriaResource) -> None:
        self._criteria = criteria

        self.create = async_to_streamed_response_wrapper(
            criteria.create,
        )
        self.update = async_to_streamed_response_wrapper(
            criteria.update,
        )
        self.list_versions = async_to_streamed_response_wrapper(
            criteria.list_versions,
        )
