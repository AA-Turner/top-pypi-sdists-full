# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List
from typing_extensions import Literal, overload

import httpx

from ..types import question_set_list_params, question_set_create_params, question_set_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
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
from ..types.question_set import QuestionSet
from ..types.paginated_question_sets import Item
from ..types.question_set_with_questions import QuestionSetWithQuestions
from ..types.shared.generic_delete_response import GenericDeleteResponse
from ..types.shared_params.question_set_question_config import QuestionSetQuestionConfig

__all__ = ["QuestionSetsResource", "AsyncQuestionSetsResource"]


class QuestionSetsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> QuestionSetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return QuestionSetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QuestionSetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return QuestionSetsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        name: str,
        question_ids: SequenceNotStr[str],
        instructions: str | Omit = omit,
        question_id_to_config: Dict[str, QuestionSetQuestionConfig] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSet:
        """
        ### Description

        Creates a question set

        ### Details

        This API can be used to create a question set. To use this API, review the
        request schema and pass in all fields that are required to create a question
        set.

        Args:
          account_id: The ID of the account that owns the given entity.

          question_ids: IDs of questions in the question set

          instructions: Instructions to answer questions

          question_id_to_config: Specifies additional configurations to use for specific questions in the context
              of the question set. For example,
              `{<question_a_id>: {required: true}, <question_b_id>: {required: true}}` sets
              two questions as required.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/question-sets",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "name": name,
                    "question_ids": question_ids,
                    "instructions": instructions,
                    "question_id_to_config": question_id_to_config,
                },
                question_set_create_params.QuestionSetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSet,
        )

    def retrieve(
        self,
        question_set_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSetWithQuestions:
        """
        Get Question Set

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return self._get(
            path_template("/v4/question-sets/{question_set_id}", question_set_id=question_set_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSetWithQuestions,
        )

    @overload
    def update(
        self,
        question_set_id: str,
        *,
        instructions: str | Omit = omit,
        name: str | Omit = omit,
        question_ids: SequenceNotStr[str] | Omit = omit,
        restore: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSet:
        """
        ### Description

        Updates a question set

        ### Details

        This API can be used to update the question set that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Question Set API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          instructions: Instructions to answer questions

          question_ids: IDs of questions in the question set

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
        question_set_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSet:
        """
        ### Description

        Updates a question set

        ### Details

        This API can be used to update the question set that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Question Set API call as a path parameter.

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
        question_set_id: str,
        *,
        instructions: str | Omit = omit,
        name: str | Omit = omit,
        question_ids: SequenceNotStr[str] | Omit = omit,
        restore: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSet:
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return self._patch(
            path_template("/v4/question-sets/{question_set_id}", question_set_id=question_set_id),
            body=maybe_transform(
                {
                    "instructions": instructions,
                    "name": name,
                    "question_ids": question_ids,
                    "restore": restore,
                },
                question_set_update_params.QuestionSetUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSet,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        view: List[Literal["Questions"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[Item]:
        """
        ### Description

        Lists all question sets accessible to the user.

        ### Details

        This API can be used to list question sets. If a user has access to multiple
        accounts, all question sets from all accounts the user is associated with will
        be returned.

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
            "/v4/question-sets",
            page=SyncPageResponse[Item],
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
                    question_set_list_params.QuestionSetListParams,
                ),
            ),
            model=Item,
        )

    def delete(
        self,
        question_set_id: str,
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

        Deletes a question set

        ### Details

        This API can be used to delete a question set by ID. To use this API, pass in
        the `id` that was returned from your Create Question Set API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return self._delete(
            path_template("/v4/question-sets/{question_set_id}", question_set_id=question_set_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class AsyncQuestionSetsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncQuestionSetsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncQuestionSetsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQuestionSetsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncQuestionSetsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        name: str,
        question_ids: SequenceNotStr[str],
        instructions: str | Omit = omit,
        question_id_to_config: Dict[str, QuestionSetQuestionConfig] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSet:
        """
        ### Description

        Creates a question set

        ### Details

        This API can be used to create a question set. To use this API, review the
        request schema and pass in all fields that are required to create a question
        set.

        Args:
          account_id: The ID of the account that owns the given entity.

          question_ids: IDs of questions in the question set

          instructions: Instructions to answer questions

          question_id_to_config: Specifies additional configurations to use for specific questions in the context
              of the question set. For example,
              `{<question_a_id>: {required: true}, <question_b_id>: {required: true}}` sets
              two questions as required.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/question-sets",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "name": name,
                    "question_ids": question_ids,
                    "instructions": instructions,
                    "question_id_to_config": question_id_to_config,
                },
                question_set_create_params.QuestionSetCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSet,
        )

    async def retrieve(
        self,
        question_set_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSetWithQuestions:
        """
        Get Question Set

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return await self._get(
            path_template("/v4/question-sets/{question_set_id}", question_set_id=question_set_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSetWithQuestions,
        )

    @overload
    async def update(
        self,
        question_set_id: str,
        *,
        instructions: str | Omit = omit,
        name: str | Omit = omit,
        question_ids: SequenceNotStr[str] | Omit = omit,
        restore: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSet:
        """
        ### Description

        Updates a question set

        ### Details

        This API can be used to update the question set that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Question Set API call as a path parameter.

        Review the request schema to see the fields that can be updated.

        Args:
          instructions: Instructions to answer questions

          question_ids: IDs of questions in the question set

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
        question_set_id: str,
        *,
        restore: Literal[True],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSet:
        """
        ### Description

        Updates a question set

        ### Details

        This API can be used to update the question set that matches the ID that was
        passed in as a path parameter. To use this API, pass in the `id` that was
        returned from your Create Question Set API call as a path parameter.

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
        question_set_id: str,
        *,
        instructions: str | Omit = omit,
        name: str | Omit = omit,
        question_ids: SequenceNotStr[str] | Omit = omit,
        restore: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> QuestionSet:
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return await self._patch(
            path_template("/v4/question-sets/{question_set_id}", question_set_id=question_set_id),
            body=await async_maybe_transform(
                {
                    "instructions": instructions,
                    "name": name,
                    "question_ids": question_ids,
                    "restore": restore,
                },
                question_set_update_params.QuestionSetUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=QuestionSet,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        include_archived: bool | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        view: List[Literal["Questions"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Item, AsyncPageResponse[Item]]:
        """
        ### Description

        Lists all question sets accessible to the user.

        ### Details

        This API can be used to list question sets. If a user has access to multiple
        accounts, all question sets from all accounts the user is associated with will
        be returned.

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
            "/v4/question-sets",
            page=AsyncPageResponse[Item],
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
                    question_set_list_params.QuestionSetListParams,
                ),
            ),
            model=Item,
        )

    async def delete(
        self,
        question_set_id: str,
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

        Deletes a question set

        ### Details

        This API can be used to delete a question set by ID. To use this API, pass in
        the `id` that was returned from your Create Question Set API call as a path
        parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_set_id:
            raise ValueError(f"Expected a non-empty value for `question_set_id` but received {question_set_id!r}")
        return await self._delete(
            path_template("/v4/question-sets/{question_set_id}", question_set_id=question_set_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class QuestionSetsResourceWithRawResponse:
    def __init__(self, question_sets: QuestionSetsResource) -> None:
        self._question_sets = question_sets

        self.create = to_raw_response_wrapper(
            question_sets.create,
        )
        self.retrieve = to_raw_response_wrapper(
            question_sets.retrieve,
        )
        self.update = to_raw_response_wrapper(
            question_sets.update,
        )
        self.list = to_raw_response_wrapper(
            question_sets.list,
        )
        self.delete = to_raw_response_wrapper(
            question_sets.delete,
        )


class AsyncQuestionSetsResourceWithRawResponse:
    def __init__(self, question_sets: AsyncQuestionSetsResource) -> None:
        self._question_sets = question_sets

        self.create = async_to_raw_response_wrapper(
            question_sets.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            question_sets.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            question_sets.update,
        )
        self.list = async_to_raw_response_wrapper(
            question_sets.list,
        )
        self.delete = async_to_raw_response_wrapper(
            question_sets.delete,
        )


class QuestionSetsResourceWithStreamingResponse:
    def __init__(self, question_sets: QuestionSetsResource) -> None:
        self._question_sets = question_sets

        self.create = to_streamed_response_wrapper(
            question_sets.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            question_sets.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            question_sets.update,
        )
        self.list = to_streamed_response_wrapper(
            question_sets.list,
        )
        self.delete = to_streamed_response_wrapper(
            question_sets.delete,
        )


class AsyncQuestionSetsResourceWithStreamingResponse:
    def __init__(self, question_sets: AsyncQuestionSetsResource) -> None:
        self._question_sets = question_sets

        self.create = async_to_streamed_response_wrapper(
            question_sets.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            question_sets.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            question_sets.update,
        )
        self.list = async_to_streamed_response_wrapper(
            question_sets.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            question_sets.delete,
        )
