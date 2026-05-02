# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal

import httpx

from ..types import question_list_params, question_create_params
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
from ..types.question import Question
from ..types.shared_params.categorical_choice import CategoricalChoice

__all__ = ["QuestionsResource", "AsyncQuestionsResource"]


class QuestionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> QuestionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return QuestionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> QuestionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return QuestionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        account_id: str,
        prompt: str,
        title: str,
        type: Literal["categorical", "free_text", "rating", "number", "form", "timestamp"],
        allow_multi_timestamps: bool | Omit = omit,
        choices: Iterable[CategoricalChoice] | Omit = omit,
        conditions: Iterable[Dict[str, object]] | Omit = omit,
        default: object | Omit = omit,
        dropdown: bool | Omit = omit,
        form_schema: Dict[str, object] | Omit = omit,
        free_text_options: question_create_params.FreeTextOptions | Omit = omit,
        multi: bool | Omit = omit,
        number_options: question_create_params.NumberOptions | Omit = omit,
        rating_options: question_create_params.RatingOptions | Omit = omit,
        required: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        ### Description

        Creates a question

        ### Details

        This API can be used to create a question. To use this API, review the request
        schema and pass in all fields that are required to create a question.

        Args:
          account_id: The ID of the account that owns the given entity.

          type: The type of question

          allow_multi_timestamps: Whether to allow multiple media timestamps for timestamp questions.

          choices: List of choices for the question. Required for CATEGORICAL questions.

          conditions: Conditions for the question to be shown.

          default: The default value for the question.

          dropdown: Whether the question is displayed as a dropdown in the UI.

          form_schema: The schema for the question.

          free_text_options: Options for free text questions.

          multi: Whether the question allows multiple answers. For categorical questions, this
              enables multi-select. For timestamp questions, this allows multiple timestamps.

          number_options: Options for number questions.

          rating_options: Options for rating questions.

          required: [To be deprecated in favor of question set question_id_to_config] Whether the
              question is required.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/questions",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "prompt": prompt,
                    "title": title,
                    "type": type,
                    "allow_multi_timestamps": allow_multi_timestamps,
                    "choices": choices,
                    "conditions": conditions,
                    "default": default,
                    "dropdown": dropdown,
                    "form_schema": form_schema,
                    "free_text_options": free_text_options,
                    "multi": multi,
                    "number_options": number_options,
                    "rating_options": rating_options,
                    "required": required,
                },
                question_create_params.QuestionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Question,
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
        ### Description

        Gets the details of a question

        ### Details

        This API can be used to get information about a single question by ID. To use
        this API, pass in the `id` that was returned from your Create Question API call
        as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return self._get(
            f"/v4/questions/{question_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Question,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncPageResponse[Question]:
        """
        ### Description

        Lists all questions accessible to the user.

        ### Details

        This API can be used to list questions. If a user has access to multiple
        accounts, all questions from all accounts the user is associated with will be
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
            "/v4/questions",
            page=SyncPageResponse[Question],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    question_list_params.QuestionListParams,
                ),
            ),
            model=Question,
        )


class AsyncQuestionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncQuestionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncQuestionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncQuestionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncQuestionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        account_id: str,
        prompt: str,
        title: str,
        type: Literal["categorical", "free_text", "rating", "number", "form", "timestamp"],
        allow_multi_timestamps: bool | Omit = omit,
        choices: Iterable[CategoricalChoice] | Omit = omit,
        conditions: Iterable[Dict[str, object]] | Omit = omit,
        default: object | Omit = omit,
        dropdown: bool | Omit = omit,
        form_schema: Dict[str, object] | Omit = omit,
        free_text_options: question_create_params.FreeTextOptions | Omit = omit,
        multi: bool | Omit = omit,
        number_options: question_create_params.NumberOptions | Omit = omit,
        rating_options: question_create_params.RatingOptions | Omit = omit,
        required: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Question:
        """
        ### Description

        Creates a question

        ### Details

        This API can be used to create a question. To use this API, review the request
        schema and pass in all fields that are required to create a question.

        Args:
          account_id: The ID of the account that owns the given entity.

          type: The type of question

          allow_multi_timestamps: Whether to allow multiple media timestamps for timestamp questions.

          choices: List of choices for the question. Required for CATEGORICAL questions.

          conditions: Conditions for the question to be shown.

          default: The default value for the question.

          dropdown: Whether the question is displayed as a dropdown in the UI.

          form_schema: The schema for the question.

          free_text_options: Options for free text questions.

          multi: Whether the question allows multiple answers. For categorical questions, this
              enables multi-select. For timestamp questions, this allows multiple timestamps.

          number_options: Options for number questions.

          rating_options: Options for rating questions.

          required: [To be deprecated in favor of question set question_id_to_config] Whether the
              question is required.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/questions",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "prompt": prompt,
                    "title": title,
                    "type": type,
                    "allow_multi_timestamps": allow_multi_timestamps,
                    "choices": choices,
                    "conditions": conditions,
                    "default": default,
                    "dropdown": dropdown,
                    "form_schema": form_schema,
                    "free_text_options": free_text_options,
                    "multi": multi,
                    "number_options": number_options,
                    "rating_options": rating_options,
                    "required": required,
                },
                question_create_params.QuestionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Question,
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
        ### Description

        Gets the details of a question

        ### Details

        This API can be used to get information about a single question by ID. To use
        this API, pass in the `id` that was returned from your Create Question API call
        as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not question_id:
            raise ValueError(f"Expected a non-empty value for `question_id` but received {question_id!r}")
        return await self._get(
            f"/v4/questions/{question_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Question,
        )

    def list(
        self,
        *,
        account_id: str | Omit = omit,
        limit: int | Omit = omit,
        page: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Question, AsyncPageResponse[Question]]:
        """
        ### Description

        Lists all questions accessible to the user.

        ### Details

        This API can be used to list questions. If a user has access to multiple
        accounts, all questions from all accounts the user is associated with will be
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
            "/v4/questions",
            page=AsyncPageResponse[Question],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "account_id": account_id,
                        "limit": limit,
                        "page": page,
                    },
                    question_list_params.QuestionListParams,
                ),
            ),
            model=Question,
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
        self.list = to_raw_response_wrapper(
            questions.list,
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
        self.list = async_to_raw_response_wrapper(
            questions.list,
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
        self.list = to_streamed_response_wrapper(
            questions.list,
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
        self.list = async_to_streamed_response_wrapper(
            questions.list,
        )
