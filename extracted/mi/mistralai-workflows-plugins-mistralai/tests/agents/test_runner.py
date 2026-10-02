import pytest
from mistralai.client import models as mistralai_models

from mistralai.workflows.plugins.mistralai import Agent
from mistralai.workflows.plugins.mistralai.runner import Runner
from mistralai.workflows.plugins.mistralai.session import MockSession


def _tool_call_message(tool_call_id: str) -> mistralai_models.AssistantMessage:
    return mistralai_models.AssistantMessage(
        tool_calls=[
            mistralai_models.ToolCall(
                id=tool_call_id,
                type="function",
                function=mistralai_models.FunctionCall(name="lookup", arguments="{}"),
            )
        ]
    )


def _chat_response(message: mistralai_models.AssistantMessage) -> mistralai_models.ChatCompletionResponse:
    return mistralai_models.ChatCompletionResponse.model_construct(
        id="chatcmpl-test",
        object="chat.completion",
        model="mistral-test",
        usage=None,
        created=0,
        choices=[
            mistralai_models.ChatCompletionChoice.model_construct(
                index=0,
                finish_reason="stop",
                message=message,
            )
        ],
    )


@pytest.mark.asyncio
async def test_runner_second_run_works_after_max_turns_exhausted() -> None:
    """After max_turns stops a run with pending tool calls, the session must stay usable."""
    requests: list[mistralai_models.ChatCompletionRequest] = []
    first_run_finished = False

    async def lookup() -> str:
        """Look up a test value."""
        return "lookup result"

    async def execute_tool(tool_name: str, tool_arguments: str | dict) -> str:
        assert tool_name == "lookup"
        return await lookup()

    async def chat_complete(
        request: mistralai_models.ChatCompletionRequest,
    ) -> mistralai_models.ChatCompletionResponse:
        requests.append(request)
        if not first_run_finished:
            return _chat_response(_tool_call_message(f"call-{len(requests)}"))
        return _chat_response(mistralai_models.AssistantMessage(content="All done"))

    session = MockSession(chat_complete_callback=chat_complete, tool_execute_callback=execute_tool)
    agent = Agent(model="mistral-test", name="test-agent", tools=[lookup])

    first_outputs = await Runner.run(agent=agent, inputs="Use the lookup tool", max_turns=1, session=session)
    first_run_finished = True

    second_outputs = await Runner.run(agent=agent, inputs="Please continue", session=session)

    assert first_outputs == []
    assert len(requests) == 3
    assert any(
        isinstance(message, mistralai_models.ToolMessage)
        and message.content == "Operation interrupted: pending tool call was cancelled before continuing."
        for message in requests[2].messages
    )
    assert len(second_outputs) == 1
    assert isinstance(second_outputs[0], mistralai_models.TextChunk)
    assert second_outputs[0].text == "All done"
