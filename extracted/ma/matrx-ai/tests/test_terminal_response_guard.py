"""Terminal provider responses must contain something the user can see."""

from matrx_ai.config import (
    TextContent,
    ThinkingContent,
    ToolCallContent,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.orchestrator.executor import _terminal_response_problem


def test_reasoning_only_stop_is_not_a_success() -> None:
    response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[ThinkingContent(text="I should investigate this.")],
            )
        ],
        finish_reason="stop",
    )

    assert _terminal_response_problem(response) == (
        "empty_assistant_response",
        "The model ended without producing a visible answer. Please retry or "
        "use another model.",
    )


def test_pseudo_tool_markup_in_reasoning_gets_specific_failure() -> None:
    response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    ThinkingContent(
                        text="<tool_call><function=web>{}</function></tool_call>"
                    )
                ],
            )
        ],
        finish_reason="stop",
    )

    problem = _terminal_response_problem(response)

    assert problem is not None
    assert problem[0] == "unparsed_tool_call"


def test_visible_text_or_real_tool_call_is_valid() -> None:
    text_response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    ThinkingContent(text="reasoning"),
                    TextContent(text="Here is the answer."),
                ],
            )
        ]
    )
    tool_response = UnifiedResponse(
        messages=[
            UnifiedMessage(
                role="assistant",
                content=[
                    ToolCallContent(
                        id="call-1",
                        name="web",
                        arguments={"action": "search"},
                    )
                ],
            )
        ]
    )

    assert _terminal_response_problem(text_response) is None
    assert _terminal_response_problem(tool_response) is None
