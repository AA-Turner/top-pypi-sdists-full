# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast

import httpx

from ..types import question_list_params, question_create_params, question_update_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorPage, AsyncCursorPage
from ..types.chat import SortOrder
from .._base_client import AsyncPaginator, make_request_options
from ..types.question import Question
from ..types.chat.sort_order import SortOrder

__all__ = ["QuestionsResource", "AsyncQuestionsResource"]


class QuestionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> QuestionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return QuestionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QuestionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return QuestionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        question: question_create_params.Question,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Create Question

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            Question,
            self._post(
                "/v5/questions",
                body=maybe_transform(question, question_create_params.QuestionCreateParams),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        question_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Get Question

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return cast(
            Question,
            self._get(
                path_template("/v5/questions/{question_id}", question_id=question_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def update(
        self,
        question_id: str,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Update Question

        Args:
          name: Display name for the question

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return cast(
            Question,
            self._patch(
                path_template("/v5/questions/{question_id}", question_id=question_id),
                body=maybe_transform({"name": name}, question_update_params.QuestionUpdateParams),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        include_archived: bool | Omit = omit,
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
    ) -> SyncCursorPage[Question]:
        """
        List Questions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/questions",
            page=SyncCursorPage[Question],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    question_list_params.QuestionListParams,
                ),
            ),
            model=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
        )

    def archive(
        self,
        question_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Archive a question by setting archived_at in the db

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return cast(
            Question,
            self._delete(
                path_template("/v5/questions/{question_id}", question_id=question_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def restore(
        self,
        question_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Restore Archived Question

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return cast(
            Question,
            self._post(
                path_template("/v5/questions/{question_id}/restore", question_id=question_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class AsyncQuestionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncQuestionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#accessing-raw-response-data-eg-headers
        """
        return AsyncQuestionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQuestionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python-beta#with_streaming_response
        """
        return AsyncQuestionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        question: question_create_params.Question,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Create Question

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return cast(
            Question,
            await self._post(
                "/v5/questions",
                body=await async_maybe_transform(question, question_create_params.QuestionCreateParams),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        question_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Get Question

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return cast(
            Question,
            await self._get(
                path_template("/v5/questions/{question_id}", question_id=question_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def update(
        self,
        question_id: str,
        *,
        name: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Update Question

        Args:
          name: Display name for the question

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return cast(
            Question,
            await self._patch(
                path_template("/v5/questions/{question_id}", question_id=question_id),
                body=await async_maybe_transform({"name": name}, question_update_params.QuestionUpdateParams),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        include_archived: bool | Omit = omit,
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
    ) -> AsyncPaginator[Question, AsyncCursorPage[Question]]:
        """
        List Questions

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v5/questions",
            page=AsyncCursorPage[Question],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "include_archived": include_archived,
                        "limit": limit,
                        "sort_by": sort_by,
                        "sort_order": sort_order,
                        "starting_after": starting_after,
                    },
                    question_list_params.QuestionListParams,
                ),
            ),
            model=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
        )

    async def archive(
        self,
        question_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Archive a question by setting archived_at in the db

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return cast(
            Question,
            await self._delete(
                path_template("/v5/questions/{question_id}", question_id=question_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def restore(
        self,
        question_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        Restore Archived Question

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return cast(
            Question,
            await self._post(
                path_template("/v5/questions/{question_id}/restore", question_id=question_id),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Question),  # Union types cannot be passed in as arguments in the type system
            ),
        )


class QuestionsResourceWithRawResponse:
    def __init__(self, questions: QuestionsResource) -> None:
        self._questions = questions

        self.create = to_raw_response_wrapper(
            questions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            questions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            questions.update,
        )
        self.list = to_raw_response_wrapper(
            questions.list,
        )
        self.archive = to_raw_response_wrapper(
            questions.archive,
        )
        self.restore = to_raw_response_wrapper(
            questions.restore,
        )


class AsyncQuestionsResourceWithRawResponse:
    def __init__(self, questions: AsyncQuestionsResource) -> None:
        self._questions = questions

        self.create = async_to_raw_response_wrapper(
            questions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            questions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            questions.update,
        )
        self.list = async_to_raw_response_wrapper(
            questions.list,
        )
        self.archive = async_to_raw_response_wrapper(
            questions.archive,
        )
        self.restore = async_to_raw_response_wrapper(
            questions.restore,
        )


class QuestionsResourceWithStreamingResponse:
    def __init__(self, questions: QuestionsResource) -> None:
        self._questions = questions

        self.create = to_streamed_response_wrapper(
            questions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            questions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            questions.update,
        )
        self.list = to_streamed_response_wrapper(
            questions.list,
        )
        self.archive = to_streamed_response_wrapper(
            questions.archive,
        )
        self.restore = to_streamed_response_wrapper(
            questions.restore,
        )


class AsyncQuestionsResourceWithStreamingResponse:
    def __init__(self, questions: AsyncQuestionsResource) -> None:
        self._questions = questions

        self.create = async_to_streamed_response_wrapper(
            questions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            questions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            questions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            questions.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            questions.archive,
        )
        self.restore = async_to_streamed_response_wrapper(
            questions.restore,
        )
