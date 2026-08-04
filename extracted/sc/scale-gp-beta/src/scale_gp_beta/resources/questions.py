# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, cast

import httpx

from ..types import question_list_params, question_create_params, question_update_params
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
        Create a new question owned by the caller's account.

        The question is one of six types selected by the required `question_type`
        discriminator (categorical, rating, number, free_text, form, or timestamp), and
        each type carries its own `configuration` block; `name` and `prompt` are
        required for every type. Questions are the reusable units that are grouped into
        question sets and referenced by rubrics, so create them before assembling a
        question set. The created question is scoped to the caller's account and records
        the creating identity. The question type and its configuration are set at
        creation time and cannot be changed afterward through the update endpoint.

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
        Retrieve a single question in the caller's account by its ID.

        Both active and archived questions are returned; the archived state is conveyed
        by the `archived_at` field on the response. The lookup is scoped to the caller's
        account, and a question that does not exist within that account results in a
        not-found error.

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
        Update a question's display name.

        Only the `name` is mutable through this endpoint; a question's type, prompt, and
        type-specific configuration are fixed at creation and cannot be changed here.
        Updating an archived question is rejected with a client error, so restore it
        first if it needs to be edited. The update is scoped to the caller's account.

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
        ids: SequenceNotStr[str] | Omit = omit,
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
        Return a paginated list of the caller's account's questions.

        Archived questions are excluded by default; set `include_archived` to true to
        include them alongside active ones. Pass `ids` to restrict the result to a
        specific set of question IDs. Results are paginated through the standard
        pagination parameters. Use this to discover existing questions before adding
        them to a question set, or to audit which questions have been archived.

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
                        "ids": ids,
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
        Soft-delete a question by setting its `archived_at` timestamp.

        This is not a permanent delete: the row is retained and can be brought back with
        the restore endpoint. Once archived, the question is excluded from list results
        by default (unless `include_archived` is set) and can no longer be updated until
        it is restored. The archived question is returned in the response with its
        `archived_at` populated.

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
        Restore a previously archived question, reversing an archive.

        This clears the question's `archived_at` timestamp, returning it to the active
        state so it reappears in default listings and becomes editable again. It is the
        inverse of the archive (DELETE) operation and is intended for questions that
        were archived by mistake or are needed again.

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
        Create a new question owned by the caller's account.

        The question is one of six types selected by the required `question_type`
        discriminator (categorical, rating, number, free_text, form, or timestamp), and
        each type carries its own `configuration` block; `name` and `prompt` are
        required for every type. Questions are the reusable units that are grouped into
        question sets and referenced by rubrics, so create them before assembling a
        question set. The created question is scoped to the caller's account and records
        the creating identity. The question type and its configuration are set at
        creation time and cannot be changed afterward through the update endpoint.

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
        Retrieve a single question in the caller's account by its ID.

        Both active and archived questions are returned; the archived state is conveyed
        by the `archived_at` field on the response. The lookup is scoped to the caller's
        account, and a question that does not exist within that account results in a
        not-found error.

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
        Update a question's display name.

        Only the `name` is mutable through this endpoint; a question's type, prompt, and
        type-specific configuration are fixed at creation and cannot be changed here.
        Updating an archived question is rejected with a client error, so restore it
        first if it needs to be edited. The update is scoped to the caller's account.

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
        ids: SequenceNotStr[str] | Omit = omit,
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
        Return a paginated list of the caller's account's questions.

        Archived questions are excluded by default; set `include_archived` to true to
        include them alongside active ones. Pass `ids` to restrict the result to a
        specific set of question IDs. Results are paginated through the standard
        pagination parameters. Use this to discover existing questions before adding
        them to a question set, or to audit which questions have been archived.

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
                        "ids": ids,
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
        Soft-delete a question by setting its `archived_at` timestamp.

        This is not a permanent delete: the row is retained and can be brought back with
        the restore endpoint. Once archived, the question is excluded from list results
        by default (unless `include_archived` is set) and can no longer be updated until
        it is restored. The archived question is returned in the response with its
        `archived_at` populated.

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
        Restore a previously archived question, reversing an archive.

        This clears the question's `archived_at` timestamp, returning it to the active
        state so it reappears in default listings and becomes editable again. It is the
        inverse of the archive (DELETE) operation and is intended for questions that
        were archived by mistake or are needed again.

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
