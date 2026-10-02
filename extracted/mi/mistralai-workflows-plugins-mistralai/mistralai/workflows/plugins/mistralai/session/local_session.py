# ruff: noqa: E501
# Why `LocalSession` was built (vs. `RemoteSession` aka Agents SDK)?
# To address some temporary limitations of the Agents SDK, `LocalSession` was created to provide more control and
# flexibility. This is mostly experimental and will probably be removed in the future once the Agents SDK has the
# missing features.
#
# - [x] On-premises compatibility:
#   Agents SDK is not yet available for on-prem deployments; `LocalSession` operates independently, using only the
#   completion endpoint.
#
# - [ ] Full context control:
#   Zero-latency direct manipulation of `messages` list (no API roundtrips). Supports granular operations (e.g.,
#   selective message removal) not natively available in the Agents SDK.
#
# - [ ] Ad-hoc model compatibility:
#   Agents SDK rely on Mistral-specific features (e.g., `prompt_mode`, `prompt_data`), limiting compatibility with
#   non-Mistral models; `LocalSession` uses standard function-calling interfaces for broader experimentation.
#   References:
#   - https://github.com/mistralai/mistral/blob/8e69df1dcb826dbe4e9f8582f87f22282a604b72/common/mistral_common/protocol/system_prompt/templates/shared/additional_integrations.v2_6_8.jinja2#L22-L23
#   - https://github.com/mistralai/dashboard/blob/ea41933dd1705dfaa9cd81ceca6d394fee8400e1/bora/bora/services/completion.py#L532-L539
#
# - [ ] Full customization:
#   Direct access to system prompts and execution logic allowing full optimization of the full agent system.

import asyncio
import re
import uuid
from typing import cast

import structlog

from mistralai.client import UNSET
from mistralai.client import models as mistralai_models
from mistralai.workflows.plugins.mistralai.activities import mistralai_chat_complete, mistralai_chat_stream
from mistralai.workflows.plugins.mistralai.agent import Agent
from mistralai.workflows.plugins.mistralai.session.session import FinalOutputs, Inputs, Outputs, Session
from mistralai.workflows.plugins.mistralai.tool import (
    check_is_custom_tool,
    convert_tool_to_mistral_tool,
    execute_activity_tool,
    get_tool_name,
)

logger = structlog.get_logger(__name__)

Message = mistralai_models.ChatCompletionRequestMessage
LocalSessionInputs = Inputs[Message]
LocalSessionOutputs = Outputs[Message]


# inspired from https://github.com/mistralai/dashboard/blob/6d3dea5d527518e68b9fd159671e27a714437811/bora/bora/tools/handoff.py#L25
# ruff: noqa: W291, E501
SYSTEM_PROMPT_AGENT_HANDOFF = """
You are part of a multi-agent system, designed to make agent coordination and execution easy. An agent encompasses instructions and tools and can hand off a conversation to another agent when appropriate. Handoffs are achieved by calling a handoff function named `handoff_to_<agent_name>` with empty params (`{{}}`). Transfers between agents are handled seamlessly in the background; do not mention or draw attention to these transfers in your conversation with the user.

### When to transfer to another agent

When you don't have the capabilities or available tools to answer the request you can pick another agent that is better suited to add new information to the request.

### When to not transfer to another agent

If you are capable of answering the request, don't transfer it on to another agent and complete the request. Following are the available handoff tools:
{AGENT_HANDOFF_TOOLS}
""".strip()


# inspired from https://github.com/mistralai/dashboard/blob/6d3dea5d527518e68b9fd159671e27a714437811/bora/bora/protocol/v1/agents.py#L49-L83
def _get_agent_handoff_tool_description(agent: Agent) -> str:
    tool_names = [get_tool_name(tool) for tool in agent.tools or []]
    rep = (
        f"Invokes the Agent("
        f"name={agent.name}, "
        f"description={agent.description}, "
        f"available_tools={', '.join(tool_name for tool_name in tool_names if tool_name) if agent.tools else 'None'}"
        f")"
    )
    return rep


# inspired from https://github.com/mistralai/dashboard/blob/6d3dea5d527518e68b9fd159671e27a714437811/bora/bora/protocol/v1/agents.py#L49-L83
def _get_agent_handoff_tool_name(agent: Agent) -> str:
    snake_case_name = agent.name.replace("-", "_").replace(" ", "")
    snake_case_name = re.sub(r"(?<!^)(?=[A-Z])", "_", snake_case_name).lower()
    return f"handoff_to_{snake_case_name}"


def _get_agent_to_handoff_tool(agent_handoffs: list[Agent]) -> dict[Agent, mistralai_models.Tool]:
    return {
        agent: mistralai_models.Tool(
            type="function",
            function=mistralai_models.Function(
                name=_get_agent_handoff_tool_name(agent),
                description=_get_agent_handoff_tool_description(agent),
                parameters={},
            ),
        )
        for agent in agent_handoffs
    }


class LocalSession(Session[Message]):
    """A locally-managed session that calls the Mistral chat completion API.

    Subclasses can override ``_call_chat_complete``, ``_call_chat_stream``,
    and ``_execute_tool`` to customise behaviour (e.g. for testing).
    """

    def __init__(
        self,
        system_prompt_agent_handoff: str = SYSTEM_PROMPT_AGENT_HANDOFF,
        raise_on_tool_fail: bool = True,
        stream: bool = False,
    ) -> None:
        logger.warning(
            "You are using the experimental `LocalSession` class. We recommend using `RemoteSession` and ONLY use `LocalSession` if you hit some current limitations of the Agents SDK."
        )
        self._raise_on_tool_fail = raise_on_tool_fail
        self._system_prompt_agent_handoff = system_prompt_agent_handoff
        self._stream = stream
        self._conversation_id: str | None = None
        self._current_agent: Agent | None = None
        self._available_agents: list[Agent] = []
        self._handoff_function_name_to_agent: dict[str, Agent] = {}
        self._agent_to_handoff_tool: dict[Agent, mistralai_models.Tool] = {}
        self._agent_to_tools: dict[Agent, list[mistralai_models.Tool]] = {}
        self._pending_tool_call_ids: set[str] = set()
        self.messages: list[Message] = []

    async def _call_chat_complete(
        self, request: mistralai_models.ChatCompletionRequest
    ) -> mistralai_models.ChatCompletionResponse:
        return await mistralai_chat_complete(request)

    async def _call_chat_stream(
        self, request: mistralai_models.ChatCompletionRequest
    ) -> mistralai_models.AssistantMessage:
        return await mistralai_chat_stream(request)

    async def _execute_tool(self, tool_name: str, tool_arguments: str | dict) -> str:
        return await execute_activity_tool(tool_name, tool_arguments, self._raise_on_tool_fail)

    def is_conversation_active(self) -> bool:
        return self._conversation_id is not None

    async def initialize_conversation(self, agent: Agent, inputs: LocalSessionInputs) -> LocalSessionOutputs:
        if self._conversation_id:
            raise ValueError("Session already started")

        self._available_agents = list(agent.iterate_agents_deeply_in_handoffs(agent))
        self._agent_to_handoff_tool = _get_agent_to_handoff_tool(self._available_agents)
        self._handoff_function_name_to_agent = self._get_handoff_function_name_to_agent(self._agent_to_handoff_tool)
        self._agent_to_tools = self._compute_agent_to_tools(self._available_agents)
        self._current_agent = agent
        self._conversation_id = str(uuid.uuid4())

        return await self.append_messages(inputs)

    async def close_conversation(self) -> None:
        self._conversation_id = None
        self._current_agent = None
        self._available_agents = []
        self._handoff_function_name_to_agent = {}
        self._agent_to_handoff_tool = {}
        self._agent_to_tools = {}
        self._pending_tool_call_ids = set()
        self.messages = []

    async def append_messages(self, inputs: LocalSessionInputs) -> LocalSessionOutputs:
        if not self._conversation_id or not self._current_agent:
            raise ValueError("Session not started")

        agent = self._current_agent

        input_messages = self._convert_inputs_to_messages(inputs)
        missing_tool_messages = self._build_missing_tool_result_inputs(input_messages)
        if missing_tool_messages:
            input_messages = cast(LocalSessionOutputs, missing_tool_messages) + input_messages
        self.messages.extend(input_messages)

        untracked_messages: list[Message] = []

        if agent.instructions:
            untracked_messages.insert(0, mistralai_models.SystemMessage(content=agent.instructions))

        tools = self._agent_to_tools.get(agent, []).copy()

        if self._agent_to_handoff_tool and agent.handoffs:
            assert agent in self._agent_to_handoff_tool, (
                f"Agent '{agent.name}' not found in agent_to_handoff_tool but should be"
            )
            handoff_tools = [self._agent_to_handoff_tool[agent] for agent in agent.handoffs]
            tools.extend(handoff_tools)
            system_prompt_agent_handoff = self._system_prompt_agent_handoff.format(
                AGENT_HANDOFF_TOOLS="\n".join(
                    f"- {tool.function.name}: {_get_agent_handoff_tool_description(agent)}" for tool in handoff_tools
                )
            )
            untracked_messages.insert(0, mistralai_models.SystemMessage(content=system_prompt_agent_handoff))

        chat_request = mistralai_models.ChatCompletionRequest.model_validate(
            {
                "messages": untracked_messages + self.messages,
                "model": agent.model,
                "tools": tools or UNSET,
                **(agent.completion_args.model_dump(by_alias=True) if agent.completion_args else {}),
            }
        )

        output_messages: list[Message]
        if self._stream:
            assistant_message = await self._call_chat_stream(chat_request)
            output_messages = [assistant_message]
        else:
            response = await self._call_chat_complete(chat_request)
            output_messages = self._extract_output_messages(response)

        self.messages.extend(output_messages)
        self._remember_pending_tool_calls(output_messages)

        return cast(LocalSessionOutputs, output_messages)

    async def process_output(self, output: Message) -> LocalSessionOutputs:
        if output.role != "assistant":
            # no tool calls, so no next input entries
            return []

        activity_tools: list[mistralai_models.ToolCall] = []
        handoff_tools: list[mistralai_models.ToolCall] = []

        for tool_call in output.tool_calls or []:
            if tool_call.function.name in self._handoff_function_name_to_agent:
                handoff_tools.append(tool_call)
            else:
                activity_tools.append(tool_call)

        tool_responses = await asyncio.gather(
            *[self._execute_tool(tool_call.function.name, tool_call.function.arguments) for tool_call in activity_tools]
        )
        next_input_entries = [
            mistralai_models.ToolMessage(content=tool_response, tool_call_id=tool_call.id)
            for tool_call, tool_response in zip(activity_tools, tool_responses, strict=True)
        ]

        if handoff_tools:
            if len(handoff_tools) != 1:
                for tool in handoff_tools:
                    # For now we only support one handoff tool call at a time, as handoff is a function call,
                    # model is allowed to call multiple tools at once, but we don't support it yet,
                    # so we return error to model to make it them sequentially.
                    next_input_entries.append(
                        mistralai_models.ToolMessage(
                            content="ERROR: Only one handoff tool call is supported. Do them one by one.",
                            tool_call_id=tool.id,
                        )
                    )
            else:
                handoff_tool_name = handoff_tools[0].function.name
                assert handoff_tool_name in self._handoff_function_name_to_agent, (
                    f"Handoff tool '{handoff_tool_name}' not found but categorized as handoff tool above."
                )
                self._current_agent = self._handoff_function_name_to_agent[handoff_tool_name]
                next_input_entries.append(
                    mistralai_models.ToolMessage(
                        content=f"current assistant is now: {self._current_agent.name}",
                        tool_call_id=handoff_tools[0].id,
                    )
                )

        return cast(LocalSessionOutputs, next_input_entries)

    def _remember_pending_tool_calls(self, outputs: LocalSessionOutputs) -> None:
        self._pending_tool_call_ids = {
            tool_call.id
            for output in outputs
            if output.role == "assistant"
            for tool_call in output.tool_calls or []
            if isinstance(tool_call.id, str)
        }

    def _build_missing_tool_result_inputs(self, messages: LocalSessionOutputs) -> LocalSessionInputs:
        if not self._pending_tool_call_ids:
            return []
        provided = {
            message.tool_call_id
            for message in messages
            if isinstance(message, mistralai_models.ToolMessage) and isinstance(message.tool_call_id, str)
        }
        missing = self._pending_tool_call_ids - provided
        return cast(
            LocalSessionInputs,
            [
                mistralai_models.ToolMessage(
                    content="Operation interrupted: pending tool call was cancelled before continuing.",
                    tool_call_id=tool_call_id,
                )
                for tool_call_id in sorted(missing)
            ],
        )

    def format_final_outputs(self, outputs: LocalSessionOutputs) -> FinalOutputs:
        final_outputs: FinalOutputs = []
        for output in outputs:
            content = None
            if isinstance(output, mistralai_models.AssistantMessage):
                if output.tool_calls:
                    continue
                content = output.content
            elif isinstance(output, mistralai_models.DeltaMessage) and output.role == "assistant":
                content = output.content
            if content is None:
                continue
            if isinstance(content, str):
                final_outputs.append(mistralai_models.TextChunk(text=content))
            elif isinstance(content, list):
                final_outputs.extend(content)
        return final_outputs

    @staticmethod
    def _extract_output_messages(
        response: mistralai_models.ChatCompletionResponse,
    ) -> list[Message]:
        """Extract output messages from a chat completion response.

        Standard completions use ``choice.message``; multi-completions
        (returned when the API executes connector tools server-side)
        use ``choice.messages`` with server-side execution traces.
        Only the final assistant messages with content are kept.
        """
        output_messages: list[Message] = []
        if response.object == "chat.multi_completion":
            for choice in response.choices:
                for delta in choice.messages or []:
                    if delta.role == "assistant" and delta.content:
                        # Strip tool_calls — connector tools were already
                        # executed server-side in the multi-completion trace.
                        output_messages.append(mistralai_models.AssistantMessage(content=delta.content))
        else:
            for choice in response.choices:
                if choice.message is not None:
                    output_messages.append(choice.message)
        return output_messages

    def _get_handoff_function_name_to_agent(
        self,
        agent_to_handoff_tool: dict[Agent, mistralai_models.Tool],
    ) -> dict[str, Agent]:
        return {tool.function.name: agent for agent, tool in agent_to_handoff_tool.items()}

    def _compute_agent_to_tools(self, available_agents: list[Agent]) -> dict[Agent, list[mistralai_models.Tool]]:
        agent_to_tools: dict[Agent, list[mistralai_models.Tool]] = {}
        for agent in available_agents:
            tools: list[mistralai_models.Tool] = []
            if agent.tools:
                mistral_tools = self._get_mistralai_tools(agent)
                if mistral_tools:
                    tools.extend(mistral_tools)
            if agent.connectors:
                for slot in agent.connectors:
                    tools.append(
                        cast(mistralai_models.Tool, mistralai_models.CustomConnector(connector_id=slot.connector_name))
                    )
            if tools:
                agent_to_tools[agent] = tools
        return agent_to_tools

    def _get_mistralai_tools(self, agent: Agent) -> list[mistralai_models.Tool] | None:
        if not agent.tools:
            return None

        mistral_tools: list[mistralai_models.Tool] = []
        for tool in agent.tools:
            if not check_is_custom_tool(tool):
                logger.warning("Skipping built-in tool when running in local mode", tool=tool)
                continue
            mistral_tool = convert_tool_to_mistral_tool(tool)
            mistral_tools.append(cast(mistralai_models.Tool, mistral_tool))
        return mistral_tools

    def _convert_inputs_to_messages(self, inputs: LocalSessionInputs) -> LocalSessionOutputs:
        messages: LocalSessionOutputs = []
        for inp in inputs:
            if isinstance(inp, str):
                messages.append(mistralai_models.UserMessage(role="user", content=inp))
            elif isinstance(
                inp,
                (
                    mistralai_models.ImageURLChunk,
                    mistralai_models.DocumentURLChunk,
                    mistralai_models.TextChunk,
                    mistralai_models.ReferenceChunk,
                ),
            ):
                messages.append(mistralai_models.UserMessage(role="user", content=[inp]))
            elif isinstance(
                inp,
                (
                    mistralai_models.UserMessage,
                    mistralai_models.AssistantMessage,
                    mistralai_models.ToolMessage,
                    mistralai_models.SystemMessage,
                ),
            ):
                messages.append(inp)
            else:
                raise ValueError(f"Unsupported input type: {type(inp)}")
        return messages
