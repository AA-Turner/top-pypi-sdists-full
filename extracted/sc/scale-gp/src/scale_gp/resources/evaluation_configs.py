# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, overload

import httpx

from ..types import evaluation_config_list_params, evaluation_config_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, required_args, maybe_transform, async_maybe_transform
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
from ..types.evaluation_config import EvaluationConfig
from ..types.shared.generic_delete_response import GenericDeleteResponse
from ..types.shared_params.auto_evaluation_parameters import AutoEvaluationParameters

__all__ = ["EvaluationConfigsResource", "AsyncEvaluationConfigsResource"]


class EvaluationConfigsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EvaluationConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return EvaluationConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EvaluationConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return EvaluationConfigsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        account_id: str,
        question_set_id: str,
        auto_evaluation_model: Literal[
            "llama-3-1-70b-instruct",
            "gpt-4-turbo-2024-04-09",
            "llama-3-70b-instruct-bedrock",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "gpt-5-nano",
            "gpt-5-mini",
            "gpt-5",
            "gpt-5.1",
            "gpt-5.2",
            "o1",
            "o3",
            "o3-mini",
            "o4-mini",
        ]
        | Omit = omit,
        auto_evaluation_parameters: AutoEvaluationParameters | Omit = omit,
        evaluation_type: Literal["llm_auto", "llm_benchmark"] | Omit = omit,
        studio_project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationConfig:
        """
        ### Description

        Creates a evaluation config

        ### Details

        This API can be used to create a evaluation config. To use this API, review the
        request schema and pass in all fields that are required to create a evaluation
        config.

        Args:
          account_id: The ID of the account that owns the given entity.

          auto_evaluation_model: The name of the model to be used for auto-evaluation

          auto_evaluation_parameters: Execution parameters for auto-evaluation

          evaluation_type: Evaluation type

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
        question_set_id: str,
        auto_evaluation_model: None | Omit = omit,
        auto_evaluation_parameters: AutoEvaluationParameters | Omit = omit,
        evaluation_type: Literal["studio", "human"] | Omit = omit,
        studio_project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationConfig:
        """
        ### Description

        Creates a evaluation config

        ### Details

        This API can be used to create a evaluation config. To use this API, review the
        request schema and pass in all fields that are required to create a evaluation
        config.

        Args:
          account_id: The ID of the account that owns the given entity.

          auto_evaluation_model: The name of the model to be used for auto-evaluation. Not applicable for manual
              evaluations.

          auto_evaluation_parameters: Execution parameters for auto-evaluation

          evaluation_type: Evaluation type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["account_id", "question_set_id"])
    def create(
        self,
        *,
        account_id: str,
        question_set_id: str,
        auto_evaluation_model: Literal[
            "llama-3-1-70b-instruct",
            "gpt-4-turbo-2024-04-09",
            "llama-3-70b-instruct-bedrock",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "gpt-5-nano",
            "gpt-5-mini",
            "gpt-5",
            "gpt-5.1",
            "gpt-5.2",
            "o1",
            "o3",
            "o3-mini",
            "o4-mini",
        ]
        | None
        | Omit = omit,
        auto_evaluation_parameters: AutoEvaluationParameters | Omit = omit,
        evaluation_type: Literal["llm_auto", "llm_benchmark"] | Literal["studio", "human"] | Omit = omit,
        studio_project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationConfig:
        return self._post(
            "/v4/evaluation-configs",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "question_set_id": question_set_id,
                    "auto_evaluation_model": auto_evaluation_model,
                    "auto_evaluation_parameters": auto_evaluation_parameters,
                    "evaluation_type": evaluation_type,
                    "studio_project_id": studio_project_id,
                },
                evaluation_config_create_params.EvaluationConfigCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationConfig,
        )

    def retrieve(
        self,
        evaluation_config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationConfig:
        """
        ### Description

        Gets the details of a evaluation config

        ### Details

        This API can be used to get information about a single evaluation config by ID.
        To use this API, pass in the `id` that was returned from your Create Evaluation
        Config API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_config_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_config_id` but received {evaluation_config_id!r}"
            )
        return self._get(
            path_template("/v4/evaluation-configs/{evaluation_config_id}", evaluation_config_id=evaluation_config_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationConfig,
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
    ) -> SyncPageResponse[EvaluationConfig]:
        """
        ### Description

        Lists all evaluation configs accessible to the user.

        ### Details

        This API can be used to list evaluation configs. If a user has access to
        multiple accounts, all evaluation configs from all accounts the user is
        associated with will be returned.

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
            "/v4/evaluation-configs",
            page=SyncPageResponse[EvaluationConfig],
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
                    evaluation_config_list_params.EvaluationConfigListParams,
                ),
            ),
            model=EvaluationConfig,
        )

    def delete(
        self,
        evaluation_config_id: str,
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

        Deletes a evaluation config

        ### Details

        This API can be used to delete a evaluation config by ID. To use this API, pass
        in the `id` that was returned from your Create Evaluation Config API call as a
        path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_config_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_config_id` but received {evaluation_config_id!r}"
            )
        return self._delete(
            path_template("/v4/evaluation-configs/{evaluation_config_id}", evaluation_config_id=evaluation_config_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class AsyncEvaluationConfigsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEvaluationConfigsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEvaluationConfigsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEvaluationConfigsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncEvaluationConfigsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        account_id: str,
        question_set_id: str,
        auto_evaluation_model: Literal[
            "llama-3-1-70b-instruct",
            "gpt-4-turbo-2024-04-09",
            "llama-3-70b-instruct-bedrock",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "gpt-5-nano",
            "gpt-5-mini",
            "gpt-5",
            "gpt-5.1",
            "gpt-5.2",
            "o1",
            "o3",
            "o3-mini",
            "o4-mini",
        ]
        | Omit = omit,
        auto_evaluation_parameters: AutoEvaluationParameters | Omit = omit,
        evaluation_type: Literal["llm_auto", "llm_benchmark"] | Omit = omit,
        studio_project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationConfig:
        """
        ### Description

        Creates a evaluation config

        ### Details

        This API can be used to create a evaluation config. To use this API, review the
        request schema and pass in all fields that are required to create a evaluation
        config.

        Args:
          account_id: The ID of the account that owns the given entity.

          auto_evaluation_model: The name of the model to be used for auto-evaluation

          auto_evaluation_parameters: Execution parameters for auto-evaluation

          evaluation_type: Evaluation type

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
        question_set_id: str,
        auto_evaluation_model: None | Omit = omit,
        auto_evaluation_parameters: AutoEvaluationParameters | Omit = omit,
        evaluation_type: Literal["studio", "human"] | Omit = omit,
        studio_project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationConfig:
        """
        ### Description

        Creates a evaluation config

        ### Details

        This API can be used to create a evaluation config. To use this API, review the
        request schema and pass in all fields that are required to create a evaluation
        config.

        Args:
          account_id: The ID of the account that owns the given entity.

          auto_evaluation_model: The name of the model to be used for auto-evaluation. Not applicable for manual
              evaluations.

          auto_evaluation_parameters: Execution parameters for auto-evaluation

          evaluation_type: Evaluation type

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["account_id", "question_set_id"])
    async def create(
        self,
        *,
        account_id: str,
        question_set_id: str,
        auto_evaluation_model: Literal[
            "llama-3-1-70b-instruct",
            "gpt-4-turbo-2024-04-09",
            "llama-3-70b-instruct-bedrock",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4.1-nano",
            "gpt-5-nano",
            "gpt-5-mini",
            "gpt-5",
            "gpt-5.1",
            "gpt-5.2",
            "o1",
            "o3",
            "o3-mini",
            "o4-mini",
        ]
        | None
        | Omit = omit,
        auto_evaluation_parameters: AutoEvaluationParameters | Omit = omit,
        evaluation_type: Literal["llm_auto", "llm_benchmark"] | Literal["studio", "human"] | Omit = omit,
        studio_project_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationConfig:
        return await self._post(
            "/v4/evaluation-configs",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "question_set_id": question_set_id,
                    "auto_evaluation_model": auto_evaluation_model,
                    "auto_evaluation_parameters": auto_evaluation_parameters,
                    "evaluation_type": evaluation_type,
                    "studio_project_id": studio_project_id,
                },
                evaluation_config_create_params.EvaluationConfigCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationConfig,
        )

    async def retrieve(
        self,
        evaluation_config_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> EvaluationConfig:
        """
        ### Description

        Gets the details of a evaluation config

        ### Details

        This API can be used to get information about a single evaluation config by ID.
        To use this API, pass in the `id` that was returned from your Create Evaluation
        Config API call as a path parameter.

        Review the response schema to see the fields that will be returned.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_config_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_config_id` but received {evaluation_config_id!r}"
            )
        return await self._get(
            path_template("/v4/evaluation-configs/{evaluation_config_id}", evaluation_config_id=evaluation_config_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EvaluationConfig,
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
    ) -> AsyncPaginator[EvaluationConfig, AsyncPageResponse[EvaluationConfig]]:
        """
        ### Description

        Lists all evaluation configs accessible to the user.

        ### Details

        This API can be used to list evaluation configs. If a user has access to
        multiple accounts, all evaluation configs from all accounts the user is
        associated with will be returned.

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
            "/v4/evaluation-configs",
            page=AsyncPageResponse[EvaluationConfig],
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
                    evaluation_config_list_params.EvaluationConfigListParams,
                ),
            ),
            model=EvaluationConfig,
        )

    async def delete(
        self,
        evaluation_config_id: str,
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

        Deletes a evaluation config

        ### Details

        This API can be used to delete a evaluation config by ID. To use this API, pass
        in the `id` that was returned from your Create Evaluation Config API call as a
        path parameter.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not evaluation_config_id:
            raise ValueError(
                f"Expected a non-empty value for `evaluation_config_id` but received {evaluation_config_id!r}"
            )
        return await self._delete(
            path_template("/v4/evaluation-configs/{evaluation_config_id}", evaluation_config_id=evaluation_config_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GenericDeleteResponse,
        )


class EvaluationConfigsResourceWithRawResponse:
    def __init__(self, evaluation_configs: EvaluationConfigsResource) -> None:
        self._evaluation_configs = evaluation_configs

        self.create = to_raw_response_wrapper(
            evaluation_configs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            evaluation_configs.retrieve,
        )
        self.list = to_raw_response_wrapper(
            evaluation_configs.list,
        )
        self.delete = to_raw_response_wrapper(
            evaluation_configs.delete,
        )


class AsyncEvaluationConfigsResourceWithRawResponse:
    def __init__(self, evaluation_configs: AsyncEvaluationConfigsResource) -> None:
        self._evaluation_configs = evaluation_configs

        self.create = async_to_raw_response_wrapper(
            evaluation_configs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            evaluation_configs.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            evaluation_configs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            evaluation_configs.delete,
        )


class EvaluationConfigsResourceWithStreamingResponse:
    def __init__(self, evaluation_configs: EvaluationConfigsResource) -> None:
        self._evaluation_configs = evaluation_configs

        self.create = to_streamed_response_wrapper(
            evaluation_configs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            evaluation_configs.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            evaluation_configs.list,
        )
        self.delete = to_streamed_response_wrapper(
            evaluation_configs.delete,
        )


class AsyncEvaluationConfigsResourceWithStreamingResponse:
    def __init__(self, evaluation_configs: AsyncEvaluationConfigsResource) -> None:
        self._evaluation_configs = evaluation_configs

        self.create = async_to_streamed_response_wrapper(
            evaluation_configs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            evaluation_configs.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            evaluation_configs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            evaluation_configs.delete,
        )
