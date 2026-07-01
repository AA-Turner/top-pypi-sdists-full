# MockSession: a test-friendly session that never calls Mistral APIs.
# It delegates chat completion and tool execution to user-provided callables.

from collections.abc import Awaitable, Callable

from mistralai.client import models as mistralai_models
from mistralai.workflows.plugins.mistralai.session.local_session import (
    SYSTEM_PROMPT_AGENT_HANDOFF,
    LocalSession,
)
from mistralai.workflows.plugins.mistralai.session.session import Inputs, Outputs

Message = mistralai_models.ChatCompletionRequestMessage
MockSessionInputs = Inputs[Message]
MockSessionOutputs = Outputs[Message]

# Callback type for non-streaming: receives a ChatCompletionRequest, returns a ChatCompletionResponse.
ChatCompleteCallback = Callable[
    [mistralai_models.ChatCompletionRequest],
    Awaitable[mistralai_models.ChatCompletionResponse],
]

# Callback type for streaming: receives a ChatCompletionRequest, returns an AssistantMessage.
ChatStreamCallback = Callable[
    [mistralai_models.ChatCompletionRequest],
    Awaitable[mistralai_models.AssistantMessage],
]

# Callback type for tool execution: receives (tool_name, arguments), returns the tool result string.
ToolExecuteCallback = Callable[
    [str, str | dict],
    Awaitable[str],
]


class MockSession(LocalSession):
    """A session that never hits the network.

    Supply your own callbacks for chat completion and (optionally) tool execution.
    Everything else (handoff logic, message management) is inherited from ``LocalSession``.
    """

    def __init__(
        self,
        chat_complete_callback: ChatCompleteCallback,
        chat_stream_callback: ChatStreamCallback | None = None,
        tool_execute_callback: ToolExecuteCallback | None = None,
        system_prompt_agent_handoff: str = SYSTEM_PROMPT_AGENT_HANDOFF,
        raise_on_tool_fail: bool = True,
        stream: bool = False,
    ) -> None:
        super().__init__(
            system_prompt_agent_handoff=system_prompt_agent_handoff,
            raise_on_tool_fail=raise_on_tool_fail,
            stream=stream,
        )
        self._chat_complete_callback = chat_complete_callback
        self._chat_stream_callback = chat_stream_callback
        self._tool_execute_callback = tool_execute_callback

    async def _call_chat_complete(
        self, request: mistralai_models.ChatCompletionRequest
    ) -> mistralai_models.ChatCompletionResponse:
        return await self._chat_complete_callback(request)

    async def _call_chat_stream(
        self, request: mistralai_models.ChatCompletionRequest
    ) -> mistralai_models.AssistantMessage:
        if self._chat_stream_callback is None:
            raise ValueError("MockSession created with stream=True but no chat_stream_callback provided")
        return await self._chat_stream_callback(request)

    async def _execute_tool(self, tool_name: str, tool_arguments: str | dict) -> str:
        if self._tool_execute_callback is not None:
            return await self._tool_execute_callback(tool_name, tool_arguments)
        return f"mock result for {tool_name}"
