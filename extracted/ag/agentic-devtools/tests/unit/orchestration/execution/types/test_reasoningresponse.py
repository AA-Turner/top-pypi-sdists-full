"""Tests for ReasoningResponse generic dataclass."""

from agentic_devtools.orchestration.execution.types import (
    JSONValue,
    ReasoningResponse,
    TokenUsage,
)


class TestReasoningResponse:
    def test_construction_minimal(self) -> None:
        resp: ReasoningResponse[JSONValue] = ReasoningResponse(raw_text="hello")
        assert resp.raw_text == "hello"
        assert resp.parsed_output is None
        assert resp.tool_calls == []
        assert resp.usage is None

    def test_construction_with_parsed_output(self) -> None:
        resp: ReasoningResponse[JSONValue] = ReasoningResponse(raw_text="raw", parsed_output={"key": "value"})
        assert resp.parsed_output == {"key": "value"}

    def test_generic_typing_str(self) -> None:
        resp: ReasoningResponse[str] = ReasoningResponse(raw_text="raw", parsed_output="typed")
        assert resp.parsed_output == "typed"

    def test_generic_typing_dict(self) -> None:
        data = {"plan": "step1"}
        resp: ReasoningResponse[dict[str, str]] = ReasoningResponse(raw_text="raw", parsed_output=data)
        assert resp.parsed_output == data

    def test_tool_calls_populated(self) -> None:
        calls: list[dict[str, JSONValue]] = [{"name": "tool1", "args": {"a": 1}}]
        resp: ReasoningResponse[JSONValue] = ReasoningResponse(raw_text="raw", tool_calls=calls)
        assert len(resp.tool_calls) == 1
        assert resp.tool_calls[0]["name"] == "tool1"

    def test_usage_populated(self) -> None:
        usage = TokenUsage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
        resp: ReasoningResponse[JSONValue] = ReasoningResponse(raw_text="raw", usage=usage)
        assert resp.usage is not None
        assert resp.usage.total_tokens == 30

    def test_is_frozen(self) -> None:
        resp: ReasoningResponse[JSONValue] = ReasoningResponse(raw_text="hello")
        try:
            resp.raw_text = "changed"  # type: ignore[misc]
            raise AssertionError("Expected FrozenInstanceError")
        except AttributeError:
            pass
