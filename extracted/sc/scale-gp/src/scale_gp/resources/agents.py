# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal

import httpx

from ..types import agent_execute_params
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
from .._base_client import make_request_options
from ..types.execute_agent_response import ExecuteAgentResponse
from ..types.shared_params.memory_strategy import MemoryStrategy
from ..types.shared_params.model_parameters import ModelParameters

__all__ = ["AgentsResource", "AsyncAgentsResource"]


class AgentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AgentsResourceWithStreamingResponse(self)

    def execute(
        self,
        *,
        messages: Iterable[agent_execute_params.Message],
        model: Literal[
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-16k-0613",
            "claude-instant-1",
            "claude-instant-1.1",
            "claude-2",
            "claude-2.0",
        ],
        tools: Iterable[agent_execute_params.Tool],
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExecuteAgentResponse:
        """### Description

        Executes one Agent inference step.

        Given a list of messages and a list of tools
        to ask for help from, the Agent will either respond with a final answer directly
        or ask the user to execute a tool to provide more information.

        ### Details

        An Agent is a component that utilizes a Language Model (LLM) as an interpreter
        and decision maker. Unlike asking an LLM for a direct response, communicating
        with an agent consists of a running dialogue where an agent can optionally ask
        the user to execute specialized tools for specific tasks, such as calculations,
        web searches, or accessing custom data from private knowledge bases.

        An agent is designed to be stateless, emitting outputs one step at a time. This
        means that client-side applications are responsible for managing message
        history, tool execution, and responses. This grants users greater flexibility to
        write and execute custom tools and maintain explicit control over their message
        history.

        #### Message Types

        - `User Message`: A message from the user to the agent.
        - `System Message`: An informational text message from the system to guide the
          agent. It is not a user message or agent message because it did not come from
          either entity.
        - `Agent Message`: A message from the agent to the client. It will contain
          either a final answer as `content` or a request for the user to execute a tool
          as a `tool_request`.
        - `Tool Message`: A message from the user to the agent that contains the output
          of a tool execution. The tool message will be processed by the agent and the
          agent will respond with either a final answer or another tool request.

        #### Agent Instructions

        Instructions are used to guide the agent's decision making process and output
        generation.

        Good prompt engineering is crucial to getting performant results from the agent.
        If you are having trouble getting the agent to perform well, try writing more
        specific instructions before trying more expensive techniques such as swapping
        in other models or finetuning the underlying LLM.

        For example, the default instructions we set for the agent are the following:

        > You are an AI assistant that helps users with their questions. You can answer
        > questions directly or acquire information from any of the attached tools to
        > assist you. Always answer the user's most recent query to the best of your
        > knowledge.

        > When asked about what tools are available, you must list each attached tool's
        > name and description. When asked about what you can do, mention that in
        > addition to your normal capabilities, you can also use the attached tools by
        > listing their names and descriptions. You cannot use any other tools other
        > than the ones provided to you explicitly.

        ### Restrictions and Limits

        **Message Limits**:

        - The message list is not limited by length, but by the context limit of the
          underlying language model. If you are getting an error regarding the
          underlying model's context limit, try using a memory strategy to condense the
          input messages.

        **Model Restrictions**:

        - Currently, only closed source models like GPT and Claude are supported due to
          the limitations of open source models when it comes to tool selection,
          generating tool arguments in valid JSON, and planning out multi-step tool
          execution. Specialized fine-tuning will likely be required to make open source
          models compatible with agents.

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The ID of the model to use for the agent. We only support the models listed here
              so far.

          tools: The list of specs of tools that the agent can use. Each spec must contain a
              `name` key set to the name of the tool, a `description` key set to the
              description of the tool, and an `arguments` key set to a JSON Schema compliant
              object describing the tool arguments.

              The name and description of each tool is used by the agent to decide when to use
              certain tools. Because some queries are complex and may require multiple tools
              to complete, it is important to make these descriptions as informative as
              possible. If a tool is not being chosen when it should, it is common practice to
              tune the description of the tool to make it more apparent to the agent when the
              tool can be used effectively.

          instructions: The initial instructions to provide to the agent.

              Use this to guide the agent to act in more specific ways. For example, if you
              have specific rules you want to restrict the agent to follow you can specify
              them here. For example, if I want the agent to always use certain tools before
              others, I can write that rule in these instructions.

              Good prompt engineering is crucial to getting performant results from the agent.
              If you are having trouble getting the agent to perform well, try writing more
              specific instructions here before trying more expensive techniques such as
              swapping in other models or finetuning the underlying LLM.

          memory_strategy: The memory strategy to use for the agent. A memory strategy is a way to prevent
              the underlying LLM's context limit from being exceeded. Each memory strategy
              uses a different technique to condense the input message list into a smaller
              payload for the underlying LLM.

              We only support the Last K memory strategy right now, but will be adding new
              strategies soon.

          model_parameters: Configuration parameters for the agent model, such as temperature, max_tokens,
              and stop_sequences.

              If not specified, the default value are:

              - temperature: 0.2
              - max_tokens: None (limited by the model's max tokens)
              - stop_sequences: None

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v4/agents/execute",
            body=maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "tools": tools,
                    "instructions": instructions,
                    "memory_strategy": memory_strategy,
                    "model_parameters": model_parameters,
                },
                agent_execute_params.AgentExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecuteAgentResponse,
        )


class AsyncAgentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAgentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/scaleapi/sgp-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAgentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAgentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/scaleapi/sgp-python#with_streaming_response
        """
        return AsyncAgentsResourceWithStreamingResponse(self)

    async def execute(
        self,
        *,
        messages: Iterable[agent_execute_params.Message],
        model: Literal[
            "gpt-4",
            "gpt-4-0613",
            "gpt-4-32k",
            "gpt-4-32k-0613",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k",
            "gpt-3.5-turbo-16k-0613",
            "claude-instant-1",
            "claude-instant-1.1",
            "claude-2",
            "claude-2.0",
        ],
        tools: Iterable[agent_execute_params.Tool],
        instructions: str | Omit = omit,
        memory_strategy: MemoryStrategy | Omit = omit,
        model_parameters: ModelParameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ExecuteAgentResponse:
        """### Description

        Executes one Agent inference step.

        Given a list of messages and a list of tools
        to ask for help from, the Agent will either respond with a final answer directly
        or ask the user to execute a tool to provide more information.

        ### Details

        An Agent is a component that utilizes a Language Model (LLM) as an interpreter
        and decision maker. Unlike asking an LLM for a direct response, communicating
        with an agent consists of a running dialogue where an agent can optionally ask
        the user to execute specialized tools for specific tasks, such as calculations,
        web searches, or accessing custom data from private knowledge bases.

        An agent is designed to be stateless, emitting outputs one step at a time. This
        means that client-side applications are responsible for managing message
        history, tool execution, and responses. This grants users greater flexibility to
        write and execute custom tools and maintain explicit control over their message
        history.

        #### Message Types

        - `User Message`: A message from the user to the agent.
        - `System Message`: An informational text message from the system to guide the
          agent. It is not a user message or agent message because it did not come from
          either entity.
        - `Agent Message`: A message from the agent to the client. It will contain
          either a final answer as `content` or a request for the user to execute a tool
          as a `tool_request`.
        - `Tool Message`: A message from the user to the agent that contains the output
          of a tool execution. The tool message will be processed by the agent and the
          agent will respond with either a final answer or another tool request.

        #### Agent Instructions

        Instructions are used to guide the agent's decision making process and output
        generation.

        Good prompt engineering is crucial to getting performant results from the agent.
        If you are having trouble getting the agent to perform well, try writing more
        specific instructions before trying more expensive techniques such as swapping
        in other models or finetuning the underlying LLM.

        For example, the default instructions we set for the agent are the following:

        > You are an AI assistant that helps users with their questions. You can answer
        > questions directly or acquire information from any of the attached tools to
        > assist you. Always answer the user's most recent query to the best of your
        > knowledge.

        > When asked about what tools are available, you must list each attached tool's
        > name and description. When asked about what you can do, mention that in
        > addition to your normal capabilities, you can also use the attached tools by
        > listing their names and descriptions. You cannot use any other tools other
        > than the ones provided to you explicitly.

        ### Restrictions and Limits

        **Message Limits**:

        - The message list is not limited by length, but by the context limit of the
          underlying language model. If you are getting an error regarding the
          underlying model's context limit, try using a memory strategy to condense the
          input messages.

        **Model Restrictions**:

        - Currently, only closed source models like GPT and Claude are supported due to
          the limitations of open source models when it comes to tool selection,
          generating tool arguments in valid JSON, and planning out multi-step tool
          execution. Specialized fine-tuning will likely be required to make open source
          models compatible with agents.

        Args:
          messages: The list of messages in the conversation.

              Expand each message type to see how it works and when to use it. Most
              conversations should begin with a single `user` message.

          model: The ID of the model to use for the agent. We only support the models listed here
              so far.

          tools: The list of specs of tools that the agent can use. Each spec must contain a
              `name` key set to the name of the tool, a `description` key set to the
              description of the tool, and an `arguments` key set to a JSON Schema compliant
              object describing the tool arguments.

              The name and description of each tool is used by the agent to decide when to use
              certain tools. Because some queries are complex and may require multiple tools
              to complete, it is important to make these descriptions as informative as
              possible. If a tool is not being chosen when it should, it is common practice to
              tune the description of the tool to make it more apparent to the agent when the
              tool can be used effectively.

          instructions: The initial instructions to provide to the agent.

              Use this to guide the agent to act in more specific ways. For example, if you
              have specific rules you want to restrict the agent to follow you can specify
              them here. For example, if I want the agent to always use certain tools before
              others, I can write that rule in these instructions.

              Good prompt engineering is crucial to getting performant results from the agent.
              If you are having trouble getting the agent to perform well, try writing more
              specific instructions here before trying more expensive techniques such as
              swapping in other models or finetuning the underlying LLM.

          memory_strategy: The memory strategy to use for the agent. A memory strategy is a way to prevent
              the underlying LLM's context limit from being exceeded. Each memory strategy
              uses a different technique to condense the input message list into a smaller
              payload for the underlying LLM.

              We only support the Last K memory strategy right now, but will be adding new
              strategies soon.

          model_parameters: Configuration parameters for the agent model, such as temperature, max_tokens,
              and stop_sequences.

              If not specified, the default value are:

              - temperature: 0.2
              - max_tokens: None (limited by the model's max tokens)
              - stop_sequences: None

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v4/agents/execute",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "model": model,
                    "tools": tools,
                    "instructions": instructions,
                    "memory_strategy": memory_strategy,
                    "model_parameters": model_parameters,
                },
                agent_execute_params.AgentExecuteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ExecuteAgentResponse,
        )


class AgentsResourceWithRawResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.execute = to_raw_response_wrapper(
            agents.execute,
        )


class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.execute = async_to_raw_response_wrapper(
            agents.execute,
        )


class AgentsResourceWithStreamingResponse:
    def __init__(self, agents: AgentsResource) -> None:
        self._agents = agents

        self.execute = to_streamed_response_wrapper(
            agents.execute,
        )


class AsyncAgentsResourceWithStreamingResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self._agents = agents

        self.execute = async_to_streamed_response_wrapper(
            agents.execute,
        )
