# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import Literal, overload

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import path_template, required_args, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._streaming import Stream, AsyncStream
from ..._base_client import make_request_options
from ...types.models import chat_completion_create_params
from ...types.parameter_bindings_param import ParameterBindingsParam
from ...types.shared.completion_response import CompletionResponse
from ...types.evaluation_datasets.flexible_message_param import FlexibleMessageParam

__all__ = ["ChatCompletionsResource", "AsyncChatCompletionsResource"]


class ChatCompletionsResource(SyncAPIResource):
    """Model API."""

    @cached_property
    def with_raw_response(self) -> ChatCompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return ChatCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatCompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return ChatCompletionsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        model_deployment_id: str,
        *,
        chat_history: Iterable[FlexibleMessageParam],
        prompt: str,
        chat_template: str | Omit = omit,
        chat_template_kwargs: Dict[str, object] | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logprobs: bool | Omit = omit,
        max_tokens: int | Omit = omit,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        presence_penalty: float | Omit = omit,
        reasoning_effort: Literal["low", "medium", "high"] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        stream: Literal[False] | Omit = omit,
        temperature: float | Omit = omit,
        top_k: float | Omit = omit,
        top_logprobs: int | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionResponse:
        """
        ### Description

        Interact with the LLM model using the specified model_deployment_id. You can
        include a list of messages as the conversation history. The conversation can
        feature multiple messages from the roles user, assistant, and system. If the
        chosen model does not support chat completion, the API will revert to simple
        completion, disregarding the provided history. The endpoint manages context
        length exceedance optimistically: it estimates the token count from the provided
        history and prompt, and if it exceeds the context or approaches 80% of it, the
        exact token count will be calculated, and the history will be trimmed to fit the
        context.

        ```json
        {
          "prompt": "Generate 5 more",
          "chat_history": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" },
            {
              "role": "assistant",
              "content": "1. Olivia Bennett\n2. Ethan Carter\n3. Sophia Ramirez\n4. Liam Thompson\n5. Ava Mitchell"
            }
          ]
        }
        ```

        Args:
          chat_history: Chat history entries with roles and messages. If there's no history, pass an
              empty list.

          prompt: New user prompt. This will be sent to the model with a user role.

          chat_template: The chat template to use for the completion. Currently only supported for
              llmengine chat models.

          chat_template_kwargs: Additional keyword arguments for the chat template. Currently only supported for
              llmengine chat models.

          frequency_penalty: Penalize tokens based on how much they have already appeared in the text.
              Positive values encourage the model to generate new tokens and negative values
              encourage the model to repeat tokens. Available for models provided by LLM
              Engine and OpenAI.

          logprobs: Whether to return logprobs. Currently only supported for llmengine chat models.

          max_tokens: The maximum number of tokens to generate in the completion. The token count of
              your prompt plus max_tokens cannot exceed the model's context length. If not,
              specified, max_tokens will be determined based on the model used: | Model API
              family | Model API default | EGP applied default | | --- | --- | --- | | OpenAI
              Completions |
              [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens)
              | `context window - prompt size` | | OpenAI Chat Completions |
              [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens)
              | `context window - prompt size` | | LLM Engine |
              [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910)
              parameter is required | `100` | | Anthropic Claude 2 |
              [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post)
              parameter is required | `10000` |

          presence_penalty: Penalize tokens based on if they have already appeared in the text. Positive
              values encourage the model to generate new tokens and negative values encourage
              the model to repeat tokens. Available for models provided by LLM Engine and
              OpenAI.

          reasoning_effort: The reasoning effort to use for the completion. Currently only supported for
              openai models.

          stop_sequences: List of up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          stream: Flag indicating whether to stream the completion response

          temperature: What sampling temperature to use, between [0, 2]. Higher values like 1.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. Setting temperature=0.0 will enable fully
              deterministic (greedy) sampling.NOTE: The temperature parameter range for some
              model is limited to [0, 1] if the given value is above the available range, it
              defaults to the max value. Temperature is ignored for OpenAI reasoning models.

          top_k: Sample from the k most likely next tokens at each step. Lower k focuses on
              higher probability tokens. Available for models provided by Google and LLM
              Engine.

          top_logprobs: Number of top logprobs to return. Currently only supported for llmengine chat
              models.

          top_p: The cumulative probability cutoff for token selection. Lower values mean
              sampling from a smaller, more top-weighted nucleus. Available for models
              provided by Google, LLM Engine, and OpenAI.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        model_deployment_id: str,
        *,
        chat_history: Iterable[FlexibleMessageParam],
        prompt: str,
        stream: Literal[True],
        chat_template: str | Omit = omit,
        chat_template_kwargs: Dict[str, object] | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logprobs: bool | Omit = omit,
        max_tokens: int | Omit = omit,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        presence_penalty: float | Omit = omit,
        reasoning_effort: Literal["low", "medium", "high"] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        temperature: float | Omit = omit,
        top_k: float | Omit = omit,
        top_logprobs: int | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Stream[CompletionResponse]:
        """
        ### Description

        Interact with the LLM model using the specified model_deployment_id. You can
        include a list of messages as the conversation history. The conversation can
        feature multiple messages from the roles user, assistant, and system. If the
        chosen model does not support chat completion, the API will revert to simple
        completion, disregarding the provided history. The endpoint manages context
        length exceedance optimistically: it estimates the token count from the provided
        history and prompt, and if it exceeds the context or approaches 80% of it, the
        exact token count will be calculated, and the history will be trimmed to fit the
        context.

        ```json
        {
          "prompt": "Generate 5 more",
          "chat_history": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" },
            {
              "role": "assistant",
              "content": "1. Olivia Bennett\n2. Ethan Carter\n3. Sophia Ramirez\n4. Liam Thompson\n5. Ava Mitchell"
            }
          ]
        }
        ```

        Args:
          chat_history: Chat history entries with roles and messages. If there's no history, pass an
              empty list.

          prompt: New user prompt. This will be sent to the model with a user role.

          stream: Flag indicating whether to stream the completion response

          chat_template: The chat template to use for the completion. Currently only supported for
              llmengine chat models.

          chat_template_kwargs: Additional keyword arguments for the chat template. Currently only supported for
              llmengine chat models.

          frequency_penalty: Penalize tokens based on how much they have already appeared in the text.
              Positive values encourage the model to generate new tokens and negative values
              encourage the model to repeat tokens. Available for models provided by LLM
              Engine and OpenAI.

          logprobs: Whether to return logprobs. Currently only supported for llmengine chat models.

          max_tokens: The maximum number of tokens to generate in the completion. The token count of
              your prompt plus max_tokens cannot exceed the model's context length. If not,
              specified, max_tokens will be determined based on the model used: | Model API
              family | Model API default | EGP applied default | | --- | --- | --- | | OpenAI
              Completions |
              [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens)
              | `context window - prompt size` | | OpenAI Chat Completions |
              [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens)
              | `context window - prompt size` | | LLM Engine |
              [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910)
              parameter is required | `100` | | Anthropic Claude 2 |
              [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post)
              parameter is required | `10000` |

          presence_penalty: Penalize tokens based on if they have already appeared in the text. Positive
              values encourage the model to generate new tokens and negative values encourage
              the model to repeat tokens. Available for models provided by LLM Engine and
              OpenAI.

          reasoning_effort: The reasoning effort to use for the completion. Currently only supported for
              openai models.

          stop_sequences: List of up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          temperature: What sampling temperature to use, between [0, 2]. Higher values like 1.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. Setting temperature=0.0 will enable fully
              deterministic (greedy) sampling.NOTE: The temperature parameter range for some
              model is limited to [0, 1] if the given value is above the available range, it
              defaults to the max value. Temperature is ignored for OpenAI reasoning models.

          top_k: Sample from the k most likely next tokens at each step. Lower k focuses on
              higher probability tokens. Available for models provided by Google and LLM
              Engine.

          top_logprobs: Number of top logprobs to return. Currently only supported for llmengine chat
              models.

          top_p: The cumulative probability cutoff for token selection. Lower values mean
              sampling from a smaller, more top-weighted nucleus. Available for models
              provided by Google, LLM Engine, and OpenAI.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        model_deployment_id: str,
        *,
        chat_history: Iterable[FlexibleMessageParam],
        prompt: str,
        stream: bool,
        chat_template: str | Omit = omit,
        chat_template_kwargs: Dict[str, object] | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logprobs: bool | Omit = omit,
        max_tokens: int | Omit = omit,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        presence_penalty: float | Omit = omit,
        reasoning_effort: Literal["low", "medium", "high"] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        temperature: float | Omit = omit,
        top_k: float | Omit = omit,
        top_logprobs: int | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionResponse | Stream[CompletionResponse]:
        """
        ### Description

        Interact with the LLM model using the specified model_deployment_id. You can
        include a list of messages as the conversation history. The conversation can
        feature multiple messages from the roles user, assistant, and system. If the
        chosen model does not support chat completion, the API will revert to simple
        completion, disregarding the provided history. The endpoint manages context
        length exceedance optimistically: it estimates the token count from the provided
        history and prompt, and if it exceeds the context or approaches 80% of it, the
        exact token count will be calculated, and the history will be trimmed to fit the
        context.

        ```json
        {
          "prompt": "Generate 5 more",
          "chat_history": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" },
            {
              "role": "assistant",
              "content": "1. Olivia Bennett\n2. Ethan Carter\n3. Sophia Ramirez\n4. Liam Thompson\n5. Ava Mitchell"
            }
          ]
        }
        ```

        Args:
          chat_history: Chat history entries with roles and messages. If there's no history, pass an
              empty list.

          prompt: New user prompt. This will be sent to the model with a user role.

          stream: Flag indicating whether to stream the completion response

          chat_template: The chat template to use for the completion. Currently only supported for
              llmengine chat models.

          chat_template_kwargs: Additional keyword arguments for the chat template. Currently only supported for
              llmengine chat models.

          frequency_penalty: Penalize tokens based on how much they have already appeared in the text.
              Positive values encourage the model to generate new tokens and negative values
              encourage the model to repeat tokens. Available for models provided by LLM
              Engine and OpenAI.

          logprobs: Whether to return logprobs. Currently only supported for llmengine chat models.

          max_tokens: The maximum number of tokens to generate in the completion. The token count of
              your prompt plus max_tokens cannot exceed the model's context length. If not,
              specified, max_tokens will be determined based on the model used: | Model API
              family | Model API default | EGP applied default | | --- | --- | --- | | OpenAI
              Completions |
              [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens)
              | `context window - prompt size` | | OpenAI Chat Completions |
              [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens)
              | `context window - prompt size` | | LLM Engine |
              [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910)
              parameter is required | `100` | | Anthropic Claude 2 |
              [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post)
              parameter is required | `10000` |

          presence_penalty: Penalize tokens based on if they have already appeared in the text. Positive
              values encourage the model to generate new tokens and negative values encourage
              the model to repeat tokens. Available for models provided by LLM Engine and
              OpenAI.

          reasoning_effort: The reasoning effort to use for the completion. Currently only supported for
              openai models.

          stop_sequences: List of up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          temperature: What sampling temperature to use, between [0, 2]. Higher values like 1.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. Setting temperature=0.0 will enable fully
              deterministic (greedy) sampling.NOTE: The temperature parameter range for some
              model is limited to [0, 1] if the given value is above the available range, it
              defaults to the max value. Temperature is ignored for OpenAI reasoning models.

          top_k: Sample from the k most likely next tokens at each step. Lower k focuses on
              higher probability tokens. Available for models provided by Google and LLM
              Engine.

          top_logprobs: Number of top logprobs to return. Currently only supported for llmengine chat
              models.

          top_p: The cumulative probability cutoff for token selection. Lower values mean
              sampling from a smaller, more top-weighted nucleus. Available for models
              provided by Google, LLM Engine, and OpenAI.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["chat_history", "prompt"], ["chat_history", "prompt", "stream"])
    def create(
        self,
        model_deployment_id: str,
        *,
        chat_history: Iterable[FlexibleMessageParam],
        prompt: str,
        chat_template: str | Omit = omit,
        chat_template_kwargs: Dict[str, object] | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logprobs: bool | Omit = omit,
        max_tokens: int | Omit = omit,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        presence_penalty: float | Omit = omit,
        reasoning_effort: Literal["low", "medium", "high"] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        temperature: float | Omit = omit,
        top_k: float | Omit = omit,
        top_logprobs: int | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionResponse | Stream[CompletionResponse]:
        if not model_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `model_deployment_id` but received {model_deployment_id!r}"
            )
        return self._post(
            path_template("/v4/models/{model_deployment_id}/chat-completions", model_deployment_id=model_deployment_id),
            body=maybe_transform(
                {
                    "chat_history": chat_history,
                    "prompt": prompt,
                    "chat_template": chat_template,
                    "chat_template_kwargs": chat_template_kwargs,
                    "frequency_penalty": frequency_penalty,
                    "logprobs": logprobs,
                    "max_tokens": max_tokens,
                    "model_request_parameters": model_request_parameters,
                    "presence_penalty": presence_penalty,
                    "reasoning_effort": reasoning_effort,
                    "stop_sequences": stop_sequences,
                    "stream": stream,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                },
                chat_completion_create_params.ChatCompletionCreateParamsStreaming
                if stream
                else chat_completion_create_params.ChatCompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompletionResponse,
            stream=stream or False,
            stream_cls=Stream[CompletionResponse],
        )


class AsyncChatCompletionsResource(AsyncAPIResource):
    """Model API."""

    @cached_property
    def with_raw_response(self) -> AsyncChatCompletionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChatCompletionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatCompletionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncChatCompletionsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        model_deployment_id: str,
        *,
        chat_history: Iterable[FlexibleMessageParam],
        prompt: str,
        chat_template: str | Omit = omit,
        chat_template_kwargs: Dict[str, object] | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logprobs: bool | Omit = omit,
        max_tokens: int | Omit = omit,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        presence_penalty: float | Omit = omit,
        reasoning_effort: Literal["low", "medium", "high"] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        stream: Literal[False] | Omit = omit,
        temperature: float | Omit = omit,
        top_k: float | Omit = omit,
        top_logprobs: int | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionResponse:
        """
        ### Description

        Interact with the LLM model using the specified model_deployment_id. You can
        include a list of messages as the conversation history. The conversation can
        feature multiple messages from the roles user, assistant, and system. If the
        chosen model does not support chat completion, the API will revert to simple
        completion, disregarding the provided history. The endpoint manages context
        length exceedance optimistically: it estimates the token count from the provided
        history and prompt, and if it exceeds the context or approaches 80% of it, the
        exact token count will be calculated, and the history will be trimmed to fit the
        context.

        ```json
        {
          "prompt": "Generate 5 more",
          "chat_history": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" },
            {
              "role": "assistant",
              "content": "1. Olivia Bennett\n2. Ethan Carter\n3. Sophia Ramirez\n4. Liam Thompson\n5. Ava Mitchell"
            }
          ]
        }
        ```

        Args:
          chat_history: Chat history entries with roles and messages. If there's no history, pass an
              empty list.

          prompt: New user prompt. This will be sent to the model with a user role.

          chat_template: The chat template to use for the completion. Currently only supported for
              llmengine chat models.

          chat_template_kwargs: Additional keyword arguments for the chat template. Currently only supported for
              llmengine chat models.

          frequency_penalty: Penalize tokens based on how much they have already appeared in the text.
              Positive values encourage the model to generate new tokens and negative values
              encourage the model to repeat tokens. Available for models provided by LLM
              Engine and OpenAI.

          logprobs: Whether to return logprobs. Currently only supported for llmengine chat models.

          max_tokens: The maximum number of tokens to generate in the completion. The token count of
              your prompt plus max_tokens cannot exceed the model's context length. If not,
              specified, max_tokens will be determined based on the model used: | Model API
              family | Model API default | EGP applied default | | --- | --- | --- | | OpenAI
              Completions |
              [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens)
              | `context window - prompt size` | | OpenAI Chat Completions |
              [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens)
              | `context window - prompt size` | | LLM Engine |
              [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910)
              parameter is required | `100` | | Anthropic Claude 2 |
              [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post)
              parameter is required | `10000` |

          presence_penalty: Penalize tokens based on if they have already appeared in the text. Positive
              values encourage the model to generate new tokens and negative values encourage
              the model to repeat tokens. Available for models provided by LLM Engine and
              OpenAI.

          reasoning_effort: The reasoning effort to use for the completion. Currently only supported for
              openai models.

          stop_sequences: List of up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          stream: Flag indicating whether to stream the completion response

          temperature: What sampling temperature to use, between [0, 2]. Higher values like 1.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. Setting temperature=0.0 will enable fully
              deterministic (greedy) sampling.NOTE: The temperature parameter range for some
              model is limited to [0, 1] if the given value is above the available range, it
              defaults to the max value. Temperature is ignored for OpenAI reasoning models.

          top_k: Sample from the k most likely next tokens at each step. Lower k focuses on
              higher probability tokens. Available for models provided by Google and LLM
              Engine.

          top_logprobs: Number of top logprobs to return. Currently only supported for llmengine chat
              models.

          top_p: The cumulative probability cutoff for token selection. Lower values mean
              sampling from a smaller, more top-weighted nucleus. Available for models
              provided by Google, LLM Engine, and OpenAI.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        model_deployment_id: str,
        *,
        chat_history: Iterable[FlexibleMessageParam],
        prompt: str,
        stream: Literal[True],
        chat_template: str | Omit = omit,
        chat_template_kwargs: Dict[str, object] | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logprobs: bool | Omit = omit,
        max_tokens: int | Omit = omit,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        presence_penalty: float | Omit = omit,
        reasoning_effort: Literal["low", "medium", "high"] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        temperature: float | Omit = omit,
        top_k: float | Omit = omit,
        top_logprobs: int | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncStream[CompletionResponse]:
        """
        ### Description

        Interact with the LLM model using the specified model_deployment_id. You can
        include a list of messages as the conversation history. The conversation can
        feature multiple messages from the roles user, assistant, and system. If the
        chosen model does not support chat completion, the API will revert to simple
        completion, disregarding the provided history. The endpoint manages context
        length exceedance optimistically: it estimates the token count from the provided
        history and prompt, and if it exceeds the context or approaches 80% of it, the
        exact token count will be calculated, and the history will be trimmed to fit the
        context.

        ```json
        {
          "prompt": "Generate 5 more",
          "chat_history": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" },
            {
              "role": "assistant",
              "content": "1. Olivia Bennett\n2. Ethan Carter\n3. Sophia Ramirez\n4. Liam Thompson\n5. Ava Mitchell"
            }
          ]
        }
        ```

        Args:
          chat_history: Chat history entries with roles and messages. If there's no history, pass an
              empty list.

          prompt: New user prompt. This will be sent to the model with a user role.

          stream: Flag indicating whether to stream the completion response

          chat_template: The chat template to use for the completion. Currently only supported for
              llmengine chat models.

          chat_template_kwargs: Additional keyword arguments for the chat template. Currently only supported for
              llmengine chat models.

          frequency_penalty: Penalize tokens based on how much they have already appeared in the text.
              Positive values encourage the model to generate new tokens and negative values
              encourage the model to repeat tokens. Available for models provided by LLM
              Engine and OpenAI.

          logprobs: Whether to return logprobs. Currently only supported for llmengine chat models.

          max_tokens: The maximum number of tokens to generate in the completion. The token count of
              your prompt plus max_tokens cannot exceed the model's context length. If not,
              specified, max_tokens will be determined based on the model used: | Model API
              family | Model API default | EGP applied default | | --- | --- | --- | | OpenAI
              Completions |
              [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens)
              | `context window - prompt size` | | OpenAI Chat Completions |
              [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens)
              | `context window - prompt size` | | LLM Engine |
              [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910)
              parameter is required | `100` | | Anthropic Claude 2 |
              [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post)
              parameter is required | `10000` |

          presence_penalty: Penalize tokens based on if they have already appeared in the text. Positive
              values encourage the model to generate new tokens and negative values encourage
              the model to repeat tokens. Available for models provided by LLM Engine and
              OpenAI.

          reasoning_effort: The reasoning effort to use for the completion. Currently only supported for
              openai models.

          stop_sequences: List of up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          temperature: What sampling temperature to use, between [0, 2]. Higher values like 1.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. Setting temperature=0.0 will enable fully
              deterministic (greedy) sampling.NOTE: The temperature parameter range for some
              model is limited to [0, 1] if the given value is above the available range, it
              defaults to the max value. Temperature is ignored for OpenAI reasoning models.

          top_k: Sample from the k most likely next tokens at each step. Lower k focuses on
              higher probability tokens. Available for models provided by Google and LLM
              Engine.

          top_logprobs: Number of top logprobs to return. Currently only supported for llmengine chat
              models.

          top_p: The cumulative probability cutoff for token selection. Lower values mean
              sampling from a smaller, more top-weighted nucleus. Available for models
              provided by Google, LLM Engine, and OpenAI.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        model_deployment_id: str,
        *,
        chat_history: Iterable[FlexibleMessageParam],
        prompt: str,
        stream: bool,
        chat_template: str | Omit = omit,
        chat_template_kwargs: Dict[str, object] | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logprobs: bool | Omit = omit,
        max_tokens: int | Omit = omit,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        presence_penalty: float | Omit = omit,
        reasoning_effort: Literal["low", "medium", "high"] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        temperature: float | Omit = omit,
        top_k: float | Omit = omit,
        top_logprobs: int | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionResponse | AsyncStream[CompletionResponse]:
        """
        ### Description

        Interact with the LLM model using the specified model_deployment_id. You can
        include a list of messages as the conversation history. The conversation can
        feature multiple messages from the roles user, assistant, and system. If the
        chosen model does not support chat completion, the API will revert to simple
        completion, disregarding the provided history. The endpoint manages context
        length exceedance optimistically: it estimates the token count from the provided
        history and prompt, and if it exceeds the context or approaches 80% of it, the
        exact token count will be calculated, and the history will be trimmed to fit the
        context.

        ```json
        {
          "prompt": "Generate 5 more",
          "chat_history": [
            {
              "role": "system",
              "content": "You are a name generator. Do not generate anything else than names"
            },
            { "role": "user", "content": "Generate 5 names" },
            {
              "role": "assistant",
              "content": "1. Olivia Bennett\n2. Ethan Carter\n3. Sophia Ramirez\n4. Liam Thompson\n5. Ava Mitchell"
            }
          ]
        }
        ```

        Args:
          chat_history: Chat history entries with roles and messages. If there's no history, pass an
              empty list.

          prompt: New user prompt. This will be sent to the model with a user role.

          stream: Flag indicating whether to stream the completion response

          chat_template: The chat template to use for the completion. Currently only supported for
              llmengine chat models.

          chat_template_kwargs: Additional keyword arguments for the chat template. Currently only supported for
              llmengine chat models.

          frequency_penalty: Penalize tokens based on how much they have already appeared in the text.
              Positive values encourage the model to generate new tokens and negative values
              encourage the model to repeat tokens. Available for models provided by LLM
              Engine and OpenAI.

          logprobs: Whether to return logprobs. Currently only supported for llmengine chat models.

          max_tokens: The maximum number of tokens to generate in the completion. The token count of
              your prompt plus max_tokens cannot exceed the model's context length. If not,
              specified, max_tokens will be determined based on the model used: | Model API
              family | Model API default | EGP applied default | | --- | --- | --- | | OpenAI
              Completions |
              [`16`](https://platform.openai.com/docs/api-reference/completions/create#max_tokens)
              | `context window - prompt size` | | OpenAI Chat Completions |
              [`context window - prompt size`](https://platform.openai.com/docs/api-reference/chat/create#max_tokens)
              | `context window - prompt size` | | LLM Engine |
              [`max_new_tokens`](https://github.com/scaleapi/launch-python-client/blob/207adced1c88c1c2907266fa9dd1f1ff3ec0ea5b/launch/client.py#L2910)
              parameter is required | `100` | | Anthropic Claude 2 |
              [`max_tokens_to_sample`](https://docs.anthropic.com/claude/reference/complete_post)
              parameter is required | `10000` |

          presence_penalty: Penalize tokens based on if they have already appeared in the text. Positive
              values encourage the model to generate new tokens and negative values encourage
              the model to repeat tokens. Available for models provided by LLM Engine and
              OpenAI.

          reasoning_effort: The reasoning effort to use for the completion. Currently only supported for
              openai models.

          stop_sequences: List of up to 4 sequences where the API will stop generating further tokens. The
              returned text will not contain the stop sequence.

          temperature: What sampling temperature to use, between [0, 2]. Higher values like 1.8 will
              make the output more random, while lower values like 0.2 will make it more
              focused and deterministic. Setting temperature=0.0 will enable fully
              deterministic (greedy) sampling.NOTE: The temperature parameter range for some
              model is limited to [0, 1] if the given value is above the available range, it
              defaults to the max value. Temperature is ignored for OpenAI reasoning models.

          top_k: Sample from the k most likely next tokens at each step. Lower k focuses on
              higher probability tokens. Available for models provided by Google and LLM
              Engine.

          top_logprobs: Number of top logprobs to return. Currently only supported for llmengine chat
              models.

          top_p: The cumulative probability cutoff for token selection. Lower values mean
              sampling from a smaller, more top-weighted nucleus. Available for models
              provided by Google, LLM Engine, and OpenAI.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["chat_history", "prompt"], ["chat_history", "prompt", "stream"])
    async def create(
        self,
        model_deployment_id: str,
        *,
        chat_history: Iterable[FlexibleMessageParam],
        prompt: str,
        chat_template: str | Omit = omit,
        chat_template_kwargs: Dict[str, object] | Omit = omit,
        frequency_penalty: float | Omit = omit,
        logprobs: bool | Omit = omit,
        max_tokens: int | Omit = omit,
        model_request_parameters: ParameterBindingsParam | Omit = omit,
        presence_penalty: float | Omit = omit,
        reasoning_effort: Literal["low", "medium", "high"] | Omit = omit,
        stop_sequences: SequenceNotStr[str] | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        temperature: float | Omit = omit,
        top_k: float | Omit = omit,
        top_logprobs: int | Omit = omit,
        top_p: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompletionResponse | AsyncStream[CompletionResponse]:
        if not model_deployment_id:
            raise ValueError(
                f"Expected a non-empty value for `model_deployment_id` but received {model_deployment_id!r}"
            )
        return await self._post(
            path_template("/v4/models/{model_deployment_id}/chat-completions", model_deployment_id=model_deployment_id),
            body=await async_maybe_transform(
                {
                    "chat_history": chat_history,
                    "prompt": prompt,
                    "chat_template": chat_template,
                    "chat_template_kwargs": chat_template_kwargs,
                    "frequency_penalty": frequency_penalty,
                    "logprobs": logprobs,
                    "max_tokens": max_tokens,
                    "model_request_parameters": model_request_parameters,
                    "presence_penalty": presence_penalty,
                    "reasoning_effort": reasoning_effort,
                    "stop_sequences": stop_sequences,
                    "stream": stream,
                    "temperature": temperature,
                    "top_k": top_k,
                    "top_logprobs": top_logprobs,
                    "top_p": top_p,
                },
                chat_completion_create_params.ChatCompletionCreateParamsStreaming
                if stream
                else chat_completion_create_params.ChatCompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompletionResponse,
            stream=stream or False,
            stream_cls=AsyncStream[CompletionResponse],
        )


class ChatCompletionsResourceWithRawResponse:
    def __init__(self, chat_completions: ChatCompletionsResource) -> None:
        self._chat_completions = chat_completions

        self.create = to_raw_response_wrapper(
            chat_completions.create,
        )


class AsyncChatCompletionsResourceWithRawResponse:
    def __init__(self, chat_completions: AsyncChatCompletionsResource) -> None:
        self._chat_completions = chat_completions

        self.create = async_to_raw_response_wrapper(
            chat_completions.create,
        )


class ChatCompletionsResourceWithStreamingResponse:
    def __init__(self, chat_completions: ChatCompletionsResource) -> None:
        self._chat_completions = chat_completions

        self.create = to_streamed_response_wrapper(
            chat_completions.create,
        )


class AsyncChatCompletionsResourceWithStreamingResponse:
    def __init__(self, chat_completions: AsyncChatCompletionsResource) -> None:
        self._chat_completions = chat_completions

        self.create = async_to_streamed_response_wrapper(
            chat_completions.create,
        )
