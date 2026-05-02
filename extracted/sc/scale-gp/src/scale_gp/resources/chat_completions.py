# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, overload

import httpx

from ..types import chat_completion_create_params
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
from ..types.chat_completions_response import ChatCompletionsResponse
from ..types.shared.completion_response import CompletionResponse
from ..types.shared_params.memory_strategy import MemoryStrategy
from ..types.shared_params.model_parameters import ModelParameters

__all__ = ["ChatCompletionsResource", "AsyncChatCompletionsResource"]


class ChatCompletionsResource(SyncAPIResource):
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
        *,
        messages: Iterable[chat_completion_create_params.Message],
        model: Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
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
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ],
        account_id: str | Omit = omit,
        chat_template: str | Omit = omit,
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCompletionsResponse:
        """
        ### Description

        Given a list of messages representing a conversation history, runs LLM inference
        to produce the next message.

        ### Details

        Like [completions](https://scale-egp.readme.io/docs/completions-1),
        [chat completions](https://scale-egp.readme.io/docs/chat-completions-intro)
        involve an LLM's response to input. However, chat completions take a
        conversation history as input, instead of a single prompt, which enables the LLM
        to create responses that take past context into account.

        ### Messages

        The primary input to the LLM is a list of messages represented by the `messages`
        array, which forms the conversation. The `messages` array must contain at least
        one `message` object. Each `message` object is attributed to a specific entity
        through its `role`. The available roles are:

        - `user`: Represents the human querying the model. - `assistant`: Represents the
          model responding to user. - `system`: Represents a non-user entity that
          provides information to guide the behavior of the assistant.

        When the `role` of a `message` is set to `user`, `assistant`, or `system`, the
        `message` must also contain a `content` field which is a string representing the
        actual text of the message itself. Semantically, when the `role` is `user`,
        `content` contains the user's query. When the `role` is `assistant`, `content`
        is the model's response to the user. When the `role` is `system`, `content`
        represents the instruction for the assistant.

        ### Instructions

        You may provide instructions to the assistant by supplying by supplying
        `instructions` in the HTTP request body or by specifying a `message` with `role`
        set to `system` in the `messages` array. By convention, the system message
        should be the first message in the array. Do **not** specify both an instruction
        and a system message in the `messages` array.

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The ID of the model to use for chat completions. We only support the models
              listed here so far.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          chat_template: Currently only supported for LLM-Engine models. A Jinja template string that
              defines how the chat completion API formats the string prompt. For Llama models,
              the template must take in at most a `messages` object, `bos_token` string, and
              `eos_token` string. The `messages` object is a list of dictionaries, each with
              keys `role` and `content`. For Mixtral models, the template must take in at most
              a `messages` object and `eos_token` string. The `messages` object looks
              identical to the Llama model's `messages` object, but the template can assume
              the `role` key takes on the values `user` or `assistant`, or `system` for the
              first message. The chat template either needs to handle this system message
              (which gets set via the `instructions` field or by the messages), or the
              `instructions` field must be set to `null` and the `messages` object must not
              contain any system messages.See the default chat template present in the Llama
              and Mixtral tokenizers for examples.

          instructions: The initial instructions to provide to the chat completion model.

              Use this to guide the model to act in more specific ways. For example, if you
              have specific rules you want to restrict the model to follow you can specify
              them here.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing more
              specific instructions here before trying more expensive techniques such as
              swapping in other models or finetuning the underlying LLM.

          memory_strategy: The memory strategy to use for the agent. A memory strategy is a way to prevent
              the underlying LLM's context limit from being exceeded. Each memory strategy
              uses a different technique to condense the input message list into a smaller
              payload for the underlying LLM.

              We only support the Last K memory strategy right now, but will be adding new
              strategies soon.

          model_parameters: Configuration parameters for the chat completion model, such as temperature,
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
        messages: Iterable[chat_completion_create_params.Message],
        model: Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
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
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ],
        stream: Literal[True],
        account_id: str | Omit = omit,
        chat_template: str | Omit = omit,
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
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

        Given a list of messages representing a conversation history, runs LLM inference
        to produce the next message.

        ### Details

        Like [completions](https://scale-egp.readme.io/docs/completions-1),
        [chat completions](https://scale-egp.readme.io/docs/chat-completions-intro)
        involve an LLM's response to input. However, chat completions take a
        conversation history as input, instead of a single prompt, which enables the LLM
        to create responses that take past context into account.

        ### Messages

        The primary input to the LLM is a list of messages represented by the `messages`
        array, which forms the conversation. The `messages` array must contain at least
        one `message` object. Each `message` object is attributed to a specific entity
        through its `role`. The available roles are:

        - `user`: Represents the human querying the model. - `assistant`: Represents the
          model responding to user. - `system`: Represents a non-user entity that
          provides information to guide the behavior of the assistant.

        When the `role` of a `message` is set to `user`, `assistant`, or `system`, the
        `message` must also contain a `content` field which is a string representing the
        actual text of the message itself. Semantically, when the `role` is `user`,
        `content` contains the user's query. When the `role` is `assistant`, `content`
        is the model's response to the user. When the `role` is `system`, `content`
        represents the instruction for the assistant.

        ### Instructions

        You may provide instructions to the assistant by supplying by supplying
        `instructions` in the HTTP request body or by specifying a `message` with `role`
        set to `system` in the `messages` array. By convention, the system message
        should be the first message in the array. Do **not** specify both an instruction
        and a system message in the `messages` array.

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The ID of the model to use for chat completions. We only support the models
              listed here so far.

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          chat_template: Currently only supported for LLM-Engine models. A Jinja template string that
              defines how the chat completion API formats the string prompt. For Llama models,
              the template must take in at most a `messages` object, `bos_token` string, and
              `eos_token` string. The `messages` object is a list of dictionaries, each with
              keys `role` and `content`. For Mixtral models, the template must take in at most
              a `messages` object and `eos_token` string. The `messages` object looks
              identical to the Llama model's `messages` object, but the template can assume
              the `role` key takes on the values `user` or `assistant`, or `system` for the
              first message. The chat template either needs to handle this system message
              (which gets set via the `instructions` field or by the messages), or the
              `instructions` field must be set to `null` and the `messages` object must not
              contain any system messages.See the default chat template present in the Llama
              and Mixtral tokenizers for examples.

          instructions: The initial instructions to provide to the chat completion model.

              Use this to guide the model to act in more specific ways. For example, if you
              have specific rules you want to restrict the model to follow you can specify
              them here.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing more
              specific instructions here before trying more expensive techniques such as
              swapping in other models or finetuning the underlying LLM.

          memory_strategy: The memory strategy to use for the agent. A memory strategy is a way to prevent
              the underlying LLM's context limit from being exceeded. Each memory strategy
              uses a different technique to condense the input message list into a smaller
              payload for the underlying LLM.

              We only support the Last K memory strategy right now, but will be adding new
              strategies soon.

          model_parameters: Configuration parameters for the chat completion model, such as temperature,
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
        messages: Iterable[chat_completion_create_params.Message],
        model: Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
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
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ],
        stream: bool,
        account_id: str | Omit = omit,
        chat_template: str | Omit = omit,
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCompletionsResponse | Stream[CompletionResponse]:
        """
        ### Description

        Given a list of messages representing a conversation history, runs LLM inference
        to produce the next message.

        ### Details

        Like [completions](https://scale-egp.readme.io/docs/completions-1),
        [chat completions](https://scale-egp.readme.io/docs/chat-completions-intro)
        involve an LLM's response to input. However, chat completions take a
        conversation history as input, instead of a single prompt, which enables the LLM
        to create responses that take past context into account.

        ### Messages

        The primary input to the LLM is a list of messages represented by the `messages`
        array, which forms the conversation. The `messages` array must contain at least
        one `message` object. Each `message` object is attributed to a specific entity
        through its `role`. The available roles are:

        - `user`: Represents the human querying the model. - `assistant`: Represents the
          model responding to user. - `system`: Represents a non-user entity that
          provides information to guide the behavior of the assistant.

        When the `role` of a `message` is set to `user`, `assistant`, or `system`, the
        `message` must also contain a `content` field which is a string representing the
        actual text of the message itself. Semantically, when the `role` is `user`,
        `content` contains the user's query. When the `role` is `assistant`, `content`
        is the model's response to the user. When the `role` is `system`, `content`
        represents the instruction for the assistant.

        ### Instructions

        You may provide instructions to the assistant by supplying by supplying
        `instructions` in the HTTP request body or by specifying a `message` with `role`
        set to `system` in the `messages` array. By convention, the system message
        should be the first message in the array. Do **not** specify both an instruction
        and a system message in the `messages` array.

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The ID of the model to use for chat completions. We only support the models
              listed here so far.

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          chat_template: Currently only supported for LLM-Engine models. A Jinja template string that
              defines how the chat completion API formats the string prompt. For Llama models,
              the template must take in at most a `messages` object, `bos_token` string, and
              `eos_token` string. The `messages` object is a list of dictionaries, each with
              keys `role` and `content`. For Mixtral models, the template must take in at most
              a `messages` object and `eos_token` string. The `messages` object looks
              identical to the Llama model's `messages` object, but the template can assume
              the `role` key takes on the values `user` or `assistant`, or `system` for the
              first message. The chat template either needs to handle this system message
              (which gets set via the `instructions` field or by the messages), or the
              `instructions` field must be set to `null` and the `messages` object must not
              contain any system messages.See the default chat template present in the Llama
              and Mixtral tokenizers for examples.

          instructions: The initial instructions to provide to the chat completion model.

              Use this to guide the model to act in more specific ways. For example, if you
              have specific rules you want to restrict the model to follow you can specify
              them here.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing more
              specific instructions here before trying more expensive techniques such as
              swapping in other models or finetuning the underlying LLM.

          memory_strategy: The memory strategy to use for the agent. A memory strategy is a way to prevent
              the underlying LLM's context limit from being exceeded. Each memory strategy
              uses a different technique to condense the input message list into a smaller
              payload for the underlying LLM.

              We only support the Last K memory strategy right now, but will be adding new
              strategies soon.

          model_parameters: Configuration parameters for the chat completion model, such as temperature,
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

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    def create(
        self,
        *,
        messages: Iterable[chat_completion_create_params.Message],
        model: Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
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
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ],
        account_id: str | Omit = omit,
        chat_template: str | Omit = omit,
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCompletionsResponse | Stream[CompletionResponse]:
        return self._post(
            "/v4/chat-completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "account_id": account_id,
                    "chat_template": chat_template,
                    "instructions": instructions,
                    "memory_strategy": memory_strategy,
                    "model_parameters": model_parameters,
                    "stream": stream,
                },
                chat_completion_create_params.ChatCompletionCreateParamsStreaming
                if stream
                else chat_completion_create_params.ChatCompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCompletionsResponse,
            stream=stream or False,
            stream_cls=Stream[CompletionResponse],
        )


class AsyncChatCompletionsResource(AsyncAPIResource):
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
        *,
        messages: Iterable[chat_completion_create_params.Message],
        model: Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
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
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ],
        account_id: str | Omit = omit,
        chat_template: str | Omit = omit,
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        stream: Literal[False] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCompletionsResponse:
        """
        ### Description

        Given a list of messages representing a conversation history, runs LLM inference
        to produce the next message.

        ### Details

        Like [completions](https://scale-egp.readme.io/docs/completions-1),
        [chat completions](https://scale-egp.readme.io/docs/chat-completions-intro)
        involve an LLM's response to input. However, chat completions take a
        conversation history as input, instead of a single prompt, which enables the LLM
        to create responses that take past context into account.

        ### Messages

        The primary input to the LLM is a list of messages represented by the `messages`
        array, which forms the conversation. The `messages` array must contain at least
        one `message` object. Each `message` object is attributed to a specific entity
        through its `role`. The available roles are:

        - `user`: Represents the human querying the model. - `assistant`: Represents the
          model responding to user. - `system`: Represents a non-user entity that
          provides information to guide the behavior of the assistant.

        When the `role` of a `message` is set to `user`, `assistant`, or `system`, the
        `message` must also contain a `content` field which is a string representing the
        actual text of the message itself. Semantically, when the `role` is `user`,
        `content` contains the user's query. When the `role` is `assistant`, `content`
        is the model's response to the user. When the `role` is `system`, `content`
        represents the instruction for the assistant.

        ### Instructions

        You may provide instructions to the assistant by supplying by supplying
        `instructions` in the HTTP request body or by specifying a `message` with `role`
        set to `system` in the `messages` array. By convention, the system message
        should be the first message in the array. Do **not** specify both an instruction
        and a system message in the `messages` array.

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The ID of the model to use for chat completions. We only support the models
              listed here so far.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          chat_template: Currently only supported for LLM-Engine models. A Jinja template string that
              defines how the chat completion API formats the string prompt. For Llama models,
              the template must take in at most a `messages` object, `bos_token` string, and
              `eos_token` string. The `messages` object is a list of dictionaries, each with
              keys `role` and `content`. For Mixtral models, the template must take in at most
              a `messages` object and `eos_token` string. The `messages` object looks
              identical to the Llama model's `messages` object, but the template can assume
              the `role` key takes on the values `user` or `assistant`, or `system` for the
              first message. The chat template either needs to handle this system message
              (which gets set via the `instructions` field or by the messages), or the
              `instructions` field must be set to `null` and the `messages` object must not
              contain any system messages.See the default chat template present in the Llama
              and Mixtral tokenizers for examples.

          instructions: The initial instructions to provide to the chat completion model.

              Use this to guide the model to act in more specific ways. For example, if you
              have specific rules you want to restrict the model to follow you can specify
              them here.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing more
              specific instructions here before trying more expensive techniques such as
              swapping in other models or finetuning the underlying LLM.

          memory_strategy: The memory strategy to use for the agent. A memory strategy is a way to prevent
              the underlying LLM's context limit from being exceeded. Each memory strategy
              uses a different technique to condense the input message list into a smaller
              payload for the underlying LLM.

              We only support the Last K memory strategy right now, but will be adding new
              strategies soon.

          model_parameters: Configuration parameters for the chat completion model, such as temperature,
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
        messages: Iterable[chat_completion_create_params.Message],
        model: Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
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
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ],
        stream: Literal[True],
        account_id: str | Omit = omit,
        chat_template: str | Omit = omit,
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
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

        Given a list of messages representing a conversation history, runs LLM inference
        to produce the next message.

        ### Details

        Like [completions](https://scale-egp.readme.io/docs/completions-1),
        [chat completions](https://scale-egp.readme.io/docs/chat-completions-intro)
        involve an LLM's response to input. However, chat completions take a
        conversation history as input, instead of a single prompt, which enables the LLM
        to create responses that take past context into account.

        ### Messages

        The primary input to the LLM is a list of messages represented by the `messages`
        array, which forms the conversation. The `messages` array must contain at least
        one `message` object. Each `message` object is attributed to a specific entity
        through its `role`. The available roles are:

        - `user`: Represents the human querying the model. - `assistant`: Represents the
          model responding to user. - `system`: Represents a non-user entity that
          provides information to guide the behavior of the assistant.

        When the `role` of a `message` is set to `user`, `assistant`, or `system`, the
        `message` must also contain a `content` field which is a string representing the
        actual text of the message itself. Semantically, when the `role` is `user`,
        `content` contains the user's query. When the `role` is `assistant`, `content`
        is the model's response to the user. When the `role` is `system`, `content`
        represents the instruction for the assistant.

        ### Instructions

        You may provide instructions to the assistant by supplying by supplying
        `instructions` in the HTTP request body or by specifying a `message` with `role`
        set to `system` in the `messages` array. By convention, the system message
        should be the first message in the array. Do **not** specify both an instruction
        and a system message in the `messages` array.

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The ID of the model to use for chat completions. We only support the models
              listed here so far.

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          chat_template: Currently only supported for LLM-Engine models. A Jinja template string that
              defines how the chat completion API formats the string prompt. For Llama models,
              the template must take in at most a `messages` object, `bos_token` string, and
              `eos_token` string. The `messages` object is a list of dictionaries, each with
              keys `role` and `content`. For Mixtral models, the template must take in at most
              a `messages` object and `eos_token` string. The `messages` object looks
              identical to the Llama model's `messages` object, but the template can assume
              the `role` key takes on the values `user` or `assistant`, or `system` for the
              first message. The chat template either needs to handle this system message
              (which gets set via the `instructions` field or by the messages), or the
              `instructions` field must be set to `null` and the `messages` object must not
              contain any system messages.See the default chat template present in the Llama
              and Mixtral tokenizers for examples.

          instructions: The initial instructions to provide to the chat completion model.

              Use this to guide the model to act in more specific ways. For example, if you
              have specific rules you want to restrict the model to follow you can specify
              them here.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing more
              specific instructions here before trying more expensive techniques such as
              swapping in other models or finetuning the underlying LLM.

          memory_strategy: The memory strategy to use for the agent. A memory strategy is a way to prevent
              the underlying LLM's context limit from being exceeded. Each memory strategy
              uses a different technique to condense the input message list into a smaller
              payload for the underlying LLM.

              We only support the Last K memory strategy right now, but will be adding new
              strategies soon.

          model_parameters: Configuration parameters for the chat completion model, such as temperature,
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
        messages: Iterable[chat_completion_create_params.Message],
        model: Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
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
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ],
        stream: bool,
        account_id: str | Omit = omit,
        chat_template: str | Omit = omit,
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCompletionsResponse | AsyncStream[CompletionResponse]:
        """
        ### Description

        Given a list of messages representing a conversation history, runs LLM inference
        to produce the next message.

        ### Details

        Like [completions](https://scale-egp.readme.io/docs/completions-1),
        [chat completions](https://scale-egp.readme.io/docs/chat-completions-intro)
        involve an LLM's response to input. However, chat completions take a
        conversation history as input, instead of a single prompt, which enables the LLM
        to create responses that take past context into account.

        ### Messages

        The primary input to the LLM is a list of messages represented by the `messages`
        array, which forms the conversation. The `messages` array must contain at least
        one `message` object. Each `message` object is attributed to a specific entity
        through its `role`. The available roles are:

        - `user`: Represents the human querying the model. - `assistant`: Represents the
          model responding to user. - `system`: Represents a non-user entity that
          provides information to guide the behavior of the assistant.

        When the `role` of a `message` is set to `user`, `assistant`, or `system`, the
        `message` must also contain a `content` field which is a string representing the
        actual text of the message itself. Semantically, when the `role` is `user`,
        `content` contains the user's query. When the `role` is `assistant`, `content`
        is the model's response to the user. When the `role` is `system`, `content`
        represents the instruction for the assistant.

        ### Instructions

        You may provide instructions to the assistant by supplying by supplying
        `instructions` in the HTTP request body or by specifying a `message` with `role`
        set to `system` in the `messages` array. By convention, the system message
        should be the first message in the array. Do **not** specify both an instruction
        and a system message in the `messages` array.

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The ID of the model to use for chat completions. We only support the models
              listed here so far.

          stream: Whether or not to stream the response.

              Setting this to True will stream the completion in real-time.

          account_id: The account ID to use for usage tracking. This will be gradually enforced.

          chat_template: Currently only supported for LLM-Engine models. A Jinja template string that
              defines how the chat completion API formats the string prompt. For Llama models,
              the template must take in at most a `messages` object, `bos_token` string, and
              `eos_token` string. The `messages` object is a list of dictionaries, each with
              keys `role` and `content`. For Mixtral models, the template must take in at most
              a `messages` object and `eos_token` string. The `messages` object looks
              identical to the Llama model's `messages` object, but the template can assume
              the `role` key takes on the values `user` or `assistant`, or `system` for the
              first message. The chat template either needs to handle this system message
              (which gets set via the `instructions` field or by the messages), or the
              `instructions` field must be set to `null` and the `messages` object must not
              contain any system messages.See the default chat template present in the Llama
              and Mixtral tokenizers for examples.

          instructions: The initial instructions to provide to the chat completion model.

              Use this to guide the model to act in more specific ways. For example, if you
              have specific rules you want to restrict the model to follow you can specify
              them here.

              Good prompt engineering is crucial to getting performant results from the model.
              If you are having trouble getting the model to perform well, try writing more
              specific instructions here before trying more expensive techniques such as
              swapping in other models or finetuning the underlying LLM.

          memory_strategy: The memory strategy to use for the agent. A memory strategy is a way to prevent
              the underlying LLM's context limit from being exceeded. Each memory strategy
              uses a different technique to condense the input message list into a smaller
              payload for the underlying LLM.

              We only support the Last K memory strategy right now, but will be adding new
              strategies soon.

          model_parameters: Configuration parameters for the chat completion model, such as temperature,
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

    @required_args(["messages", "model"], ["messages", "model", "stream"])
    async def create(
        self,
        *,
        messages: Iterable[chat_completion_create_params.Message],
        model: Literal[
            "gpt-oss-120b",
            "gpt-oss-20b",
            "o1",
            "o1-mini",
            "o3-mini",
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
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
            "llama-2-7b-chat",
            "llama-2-13b-chat",
            "llama-2-70b-chat",
            "llama-3-8b-instruct",
            "llama-3-70b-instruct",
            "llama-3-1-8b-instruct",
            "llama-3-1-70b-instruct",
            "llama-3-2-1b-instruct",
            "llama-3-2-3b-instruct",
            "llama-3-3-70b-instruct",
            "Meta-Llama-3-8B-Instruct-RMU",
            "Meta-Llama-3-8B-Instruct-RR",
            "Meta-Llama-3-8B-Instruct-DERTA",
            "Meta-Llama-3-8B-Instruct-LAT",
            "mixtral-8x7b-instruct",
            "mixtral-8x22b-instruct",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-sonnet-20241022",
            "mistral-large-latest",
            "phi-3-mini-4k-instruct",
            "phi-3-cat-merged",
            "zephyr-cat-merged",
            "dolphin-2.9-llama3-8b",
            "dolphin-2.9-llama3-70b",
            "defense-llama-3-8b-instruct",
            "donovan-combat-llama",
            "llama3-1-405b-instruct-v1",
        ],
        account_id: str | Omit = omit,
        chat_template: str | Omit = omit,
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        stream: Literal[False] | Literal[True] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCompletionsResponse | AsyncStream[CompletionResponse]:
        return await self._post(
            "/v4/chat-completions",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "account_id": account_id,
                    "chat_template": chat_template,
                    "instructions": instructions,
                    "memory_strategy": memory_strategy,
                    "model_parameters": model_parameters,
                    "stream": stream,
                },
                chat_completion_create_params.ChatCompletionCreateParamsStreaming
                if stream
                else chat_completion_create_params.ChatCompletionCreateParamsNonStreaming,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCompletionsResponse,
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
