# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, overload

import httpx

from ..types import completion_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import required_args, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._streaming import Stream, AsyncStream
from .._base_client import make_request_options
from ..types.completions_response import CompletionsResponse
from ..types.shared.completion_response import CompletionResponse
from ..types.shared_params.model_parameters import ModelParameters

__all__ = ["CompletionsResource", "AsyncCompletionsResource"]


class CompletionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return CompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return CompletionsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        model: Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ],
        prompt: str,
        account_id: str | Omit = omit,
        images: Iterable[completion_create_params.Image] | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionsResponse:
        """
        ### Description

        Given a user's input, runs LLM inference to produce the model's response.

        ### Details

        LLM [completions](https://scale-egp.readme.io/docs/completions-1) have many use
        cases, such as content summarization, question-answering, and text generation.

        The `model` parameter determines which LLM will be used to generate the
        completion. Keep in mind that different models have varying sizes, costs, and
        may perform differently across different tasks.

        The user input, commonly referred to as the "prompt", is a required field in the
        request body. The quality of the model's response can vary greatly depending on
        the input prompt. Good prompt engineering can significantly enhance the response
        quality. If you encounter suboptimal results, consider writing more specific
        instructions or providing examples to the LLM before trying more expensive
        techniques such as swapping in other models or finetuning.

        By default, the endpoint will return the entire response as one whole object. If
        you would prefer to stream the completion in real-time, you can achieve this by
        setting the `stream` flag to `true`.

        Args:
          model: The ID of the model to use for completions.

              Users have two options:

              - Option 1: Use one of the supported models from the dropdown.
              - Option 2: Enter the ID of a custom model.

              Note: For custom models we currently only support models finetuned using using
              the Scale-hosted LLM-Engine API.

          prompt: Prompt for which to generate the completion.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing a more
              specific prompt here before trying more expensive techniques such as swapping in
              other models or finetuning the underlying LLM.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          images: List of image urls to be used for image based completions. Leave empty for text
              based completions.

          model_parameters: Configuration parameters for the completion model, such as temperature,
              max_tokens, and stop_sequences.

              If not specified, the default value are:

              - temperature: 0.2
              - max_tokens: None (limited by the model's max tokens)
              - stop_sequences: None

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

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
        model: Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ],
        prompt: str,
        stream: Literal[True],
        account_id: str | Omit = omit,
        images: Iterable[completion_create_params.Image] | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[CompletionResponse]:
        """
        ### Description

        Given a user's input, runs LLM inference to produce the model's response.

        ### Details

        LLM [completions](https://scale-egp.readme.io/docs/completions-1) have many use
        cases, such as content summarization, question-answering, and text generation.

        The `model` parameter determines which LLM will be used to generate the
        completion. Keep in mind that different models have varying sizes, costs, and
        may perform differently across different tasks.

        The user input, commonly referred to as the "prompt", is a required field in the
        request body. The quality of the model's response can vary greatly depending on
        the input prompt. Good prompt engineering can significantly enhance the response
        quality. If you encounter suboptimal results, consider writing more specific
        instructions or providing examples to the LLM before trying more expensive
        techniques such as swapping in other models or finetuning.

        By default, the endpoint will return the entire response as one whole object. If
        you would prefer to stream the completion in real-time, you can achieve this by
        setting the `stream` flag to `true`.

        Args:
          model: The ID of the model to use for completions.

              Users have two options:

              - Option 1: Use one of the supported models from the dropdown.
              - Option 2: Enter the ID of a custom model.

              Note: For custom models we currently only support models finetuned using using
              the Scale-hosted LLM-Engine API.

          prompt: Prompt for which to generate the completion.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing a more
              specific prompt here before trying more expensive techniques such as swapping in
              other models or finetuning the underlying LLM.

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          images: List of image urls to be used for image based completions. Leave empty for text
              based completions.

          model_parameters: Configuration parameters for the completion model, such as temperature,
              max_tokens, and stop_sequences.

              If not specified, the default value are:

              - temperature: 0.2
              - max_tokens: None (limited by the model's max tokens)
              - stop_sequences: None

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
        model: Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ],
        prompt: str,
        stream: bool,
        account_id: str | Omit = omit,
        images: Iterable[completion_create_params.Image] | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionsResponse | Stream[CompletionResponse]:
        """
        ### Description

        Given a user's input, runs LLM inference to produce the model's response.

        ### Details

        LLM [completions](https://scale-egp.readme.io/docs/completions-1) have many use
        cases, such as content summarization, question-answering, and text generation.

        The `model` parameter determines which LLM will be used to generate the
        completion. Keep in mind that different models have varying sizes, costs, and
        may perform differently across different tasks.

        The user input, commonly referred to as the "prompt", is a required field in the
        request body. The quality of the model's response can vary greatly depending on
        the input prompt. Good prompt engineering can significantly enhance the response
        quality. If you encounter suboptimal results, consider writing more specific
        instructions or providing examples to the LLM before trying more expensive
        techniques such as swapping in other models or finetuning.

        By default, the endpoint will return the entire response as one whole object. If
        you would prefer to stream the completion in real-time, you can achieve this by
        setting the `stream` flag to `true`.

        Args:
          model: The ID of the model to use for completions.

              Users have two options:

              - Option 1: Use one of the supported models from the dropdown.
              - Option 2: Enter the ID of a custom model.

              Note: For custom models we currently only support models finetuned using using
              the Scale-hosted LLM-Engine API.

          prompt: Prompt for which to generate the completion.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing a more
              specific prompt here before trying more expensive techniques such as swapping in
              other models or finetuning the underlying LLM.

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          images: List of image urls to be used for image based completions. Leave empty for text
              based completions.

          model_parameters: Configuration parameters for the completion model, such as temperature,
              max_tokens, and stop_sequences.

              If not specified, the default value are:

              - temperature: 0.2
              - max_tokens: None (limited by the model's max tokens)
              - stop_sequences: None

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    def create(
        self,
        *,
        model: Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ],
        prompt: str,
        account_id: str | Omit = omit,
        images: Iterable[completion_create_params.Image] | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionsResponse | Stream[CompletionResponse]:
        return self._post(
            "/v4/completions",
            body=maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "account_id": account_id,
                    "images": images,
                    "model_parameters": model_parameters,
                    "stream": stream,
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompletionsResponse,
            stream=stream or False,
            stream_cls=Stream[CompletionResponse],
        )


class AsyncCompletionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncCompletionsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        model: Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ],
        prompt: str,
        account_id: str | Omit = omit,
        images: Iterable[completion_create_params.Image] | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionsResponse:
        """
        ### Description

        Given a user's input, runs LLM inference to produce the model's response.

        ### Details

        LLM [completions](https://scale-egp.readme.io/docs/completions-1) have many use
        cases, such as content summarization, question-answering, and text generation.

        The `model` parameter determines which LLM will be used to generate the
        completion. Keep in mind that different models have varying sizes, costs, and
        may perform differently across different tasks.

        The user input, commonly referred to as the "prompt", is a required field in the
        request body. The quality of the model's response can vary greatly depending on
        the input prompt. Good prompt engineering can significantly enhance the response
        quality. If you encounter suboptimal results, consider writing more specific
        instructions or providing examples to the LLM before trying more expensive
        techniques such as swapping in other models or finetuning.

        By default, the endpoint will return the entire response as one whole object. If
        you would prefer to stream the completion in real-time, you can achieve this by
        setting the `stream` flag to `true`.

        Args:
          model: The ID of the model to use for completions.

              Users have two options:

              - Option 1: Use one of the supported models from the dropdown.
              - Option 2: Enter the ID of a custom model.

              Note: For custom models we currently only support models finetuned using using
              the Scale-hosted LLM-Engine API.

          prompt: Prompt for which to generate the completion.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing a more
              specific prompt here before trying more expensive techniques such as swapping in
              other models or finetuning the underlying LLM.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          images: List of image urls to be used for image based completions. Leave empty for text
              based completions.

          model_parameters: Configuration parameters for the completion model, such as temperature,
              max_tokens, and stop_sequences.

              If not specified, the default value are:

              - temperature: 0.2
              - max_tokens: None (limited by the model's max tokens)
              - stop_sequences: None

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

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
        model: Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ],
        prompt: str,
        stream: Literal[True],
        account_id: str | Omit = omit,
        images: Iterable[completion_create_params.Image] | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[CompletionResponse]:
        """
        ### Description

        Given a user's input, runs LLM inference to produce the model's response.

        ### Details

        LLM [completions](https://scale-egp.readme.io/docs/completions-1) have many use
        cases, such as content summarization, question-answering, and text generation.

        The `model` parameter determines which LLM will be used to generate the
        completion. Keep in mind that different models have varying sizes, costs, and
        may perform differently across different tasks.

        The user input, commonly referred to as the "prompt", is a required field in the
        request body. The quality of the model's response can vary greatly depending on
        the input prompt. Good prompt engineering can significantly enhance the response
        quality. If you encounter suboptimal results, consider writing more specific
        instructions or providing examples to the LLM before trying more expensive
        techniques such as swapping in other models or finetuning.

        By default, the endpoint will return the entire response as one whole object. If
        you would prefer to stream the completion in real-time, you can achieve this by
        setting the `stream` flag to `true`.

        Args:
          model: The ID of the model to use for completions.

              Users have two options:

              - Option 1: Use one of the supported models from the dropdown.
              - Option 2: Enter the ID of a custom model.

              Note: For custom models we currently only support models finetuned using using
              the Scale-hosted LLM-Engine API.

          prompt: Prompt for which to generate the completion.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing a more
              specific prompt here before trying more expensive techniques such as swapping in
              other models or finetuning the underlying LLM.

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          images: List of image urls to be used for image based completions. Leave empty for text
              based completions.

          model_parameters: Configuration parameters for the completion model, such as temperature,
              max_tokens, and stop_sequences.

              If not specified, the default value are:

              - temperature: 0.2
              - max_tokens: None (limited by the model's max tokens)
              - stop_sequences: None

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
        model: Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ],
        prompt: str,
        stream: bool,
        account_id: str | Omit = omit,
        images: Iterable[completion_create_params.Image] | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionsResponse | AsyncStream[CompletionResponse]:
        """
        ### Description

        Given a user's input, runs LLM inference to produce the model's response.

        ### Details

        LLM [completions](https://scale-egp.readme.io/docs/completions-1) have many use
        cases, such as content summarization, question-answering, and text generation.

        The `model` parameter determines which LLM will be used to generate the
        completion. Keep in mind that different models have varying sizes, costs, and
        may perform differently across different tasks.

        The user input, commonly referred to as the "prompt", is a required field in the
        request body. The quality of the model's response can vary greatly depending on
        the input prompt. Good prompt engineering can significantly enhance the response
        quality. If you encounter suboptimal results, consider writing more specific
        instructions or providing examples to the LLM before trying more expensive
        techniques such as swapping in other models or finetuning.

        By default, the endpoint will return the entire response as one whole object. If
        you would prefer to stream the completion in real-time, you can achieve this by
        setting the `stream` flag to `true`.

        Args:
          model: The ID of the model to use for completions.

              Users have two options:

              - Option 1: Use one of the supported models from the dropdown.
              - Option 2: Enter the ID of a custom model.

              Note: For custom models we currently only support models finetuned using using
              the Scale-hosted LLM-Engine API.

          prompt: Prompt for which to generate the completion.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing a more
              specific prompt here before trying more expensive techniques such as swapping in
              other models or finetuning the underlying LLM.

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          images: List of image urls to be used for image based completions. Leave empty for text
              based completions.

          model_parameters: Configuration parameters for the completion model, such as temperature,
              max_tokens, and stop_sequences.

              If not specified, the default value are:

              - temperature: 0.2
              - max_tokens: None (limited by the model's max tokens)
              - stop_sequences: None

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["model", "prompt"], ["model", "prompt", "stream"])
    async def create(
        self,
        *,
        model: Union[
            Literal[
                "gpt-oss-120b",
                "gpt-oss-20b",
                "gpt-4",
                "gpt-4-0613",
                "gpt-4-32k",
                "gpt-4-32k-0613",
                "gpt-4-vision-preview",
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4o-2024-08-06",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-0613",
                "gpt-3.5-turbo-16k",
                "gpt-3.5-turbo-16k-0613",
                "gemini-pro",
                "gemini-1.5-pro-001",
                "gemini-1.5-pro-002",
                "gemini-1.5-pro-preview-0409",
                "gemini-1.5-pro-preview-0514",
                "text-davinci-003",
                "text-davinci-002",
                "text-curie-001",
                "text-babbage-001",
                "text-ada-001",
                "claude-instant-1",
                "claude-instant-1.1",
                "claude-2",
                "claude-2.0",
                "llama-7b",
                "llama-2-7b",
                "llama-2-7b-chat",
                "llama-2-13b",
                "llama-2-13b-chat",
                "llama-2-70b",
                "llama-2-70b-chat",
                "llama-3-8b",
                "llama-3-8b-instruct",
                "llama-3-1-8b-instruct",
                "llama-3-1-70b-instruct",
                "llama-3-70b-instruct",
                "llama-3-2-1b-instruct",
                "llama-3-2-3b-instruct",
                "llama-3-3-70b-instruct",
                "Meta-Llama-3-8B-Instruct-RMU",
                "Meta-Llama-3-8B-Instruct-RR",
                "Meta-Llama-3-8B-Instruct-DERTA",
                "Meta-Llama-3-8B-Instruct-LAT",
                "falcon-7b",
                "falcon-7b-instruct",
                "falcon-40b",
                "falcon-40b-instruct",
                "mpt-7b",
                "mpt-7b-instruct",
                "flan-t5-xxl",
                "mistral-7b",
                "mistral-7b-instruct",
                "mixtral-8x7b",
                "mixtral-8x7b-instruct",
                "mixtral-8x22b-instruct",
                "llm-jp-13b-instruct-full",
                "llm-jp-13b-instruct-full-dolly",
                "zephyr-7b-alpha",
                "zephyr-7b-beta",
                "zephyr-cat-merged",
                "codellama-7b",
                "codellama-7b-instruct",
                "codellama-13b",
                "codellama-13b-instruct",
                "codellama-34b",
                "codellama-34b-instruct",
                "phi-3-mini-4k-instruct",
                "phi-3-cat-merged",
                "dolphin-2.9-llama3-8b",
                "dolphin-2.9-llama3-70b",
                "defense-llama-3-8b-instruct",
                "donovan-combat-llama",
            ],
            str,
        ],
        prompt: str,
        account_id: str | Omit = omit,
        images: Iterable[completion_create_params.Image] | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionsResponse | AsyncStream[CompletionResponse]:
        return await self._post(
            "/v4/completions",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "account_id": account_id,
                    "images": images,
                    "model_parameters": model_parameters,
                    "stream": stream,
                },
                completion_create_params.CompletionCreateParamsStreaming
                if stream
                else completion_create_params.CompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompletionsResponse,
            stream=stream or False,
            stream_cls=AsyncStream[CompletionResponse],
        )


class CompletionsResourceWithRawResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_raw_response_wrapper(
            completions.create,
        )


class AsyncCompletionsResourceWithRawResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_raw_response_wrapper(
            completions.create,
        )


class CompletionsResourceWithStreamingResponse:
    def __init__(self, completions: CompletionsResource) -> None:
        self._completions = completions

        self.create = to_streamed_response_wrapper(
            completions.create,
        )


class AsyncCompletionsResourceWithStreamingResponse:
    def __init__(self, completions: AsyncCompletionsResource) -> None:
        self._completions = completions

        self.create = async_to_streamed_response_wrapper(
            completions.create,
        )
