"""Tests for ReasoningProvider protocol conformance."""

from agentic_devtools.orchestration.execution.protocols import ReasoningProvider
from agentic_devtools.orchestration.execution.types import ReasoningResponse


class _MockReasoningProvider:
    """A concrete class satisfying the ReasoningProvider protocol."""

    def invoke(
        self,
        prompt: str,
        *,
        tools: list | None = None,
        output_schema: type | None = None,
        model: str | None = None,
    ) -> ReasoningResponse:
        return ReasoningResponse(raw_text=f"response to: {prompt}")


class TestReasoningProvider:
    def test_mock_satisfies_protocol(self) -> None:
        provider = _MockReasoningProvider()
        assert isinstance(provider, ReasoningProvider)

    def test_invoke_returns_reasoning_response(self) -> None:
        provider = _MockReasoningProvider()
        result = provider.invoke("hello")
        assert isinstance(result, ReasoningResponse)
        assert "hello" in result.raw_text

    def test_invoke_with_model_parameter(self) -> None:
        provider = _MockReasoningProvider()
        result = provider.invoke("test", model="gpt-4")
        assert isinstance(result, ReasoningResponse)

    def test_invoke_with_tools(self) -> None:
        provider = _MockReasoningProvider()
        result = provider.invoke("test", tools=[{"name": "tool1"}])
        assert isinstance(result, ReasoningResponse)

    def test_invoke_with_output_schema(self) -> None:
        provider = _MockReasoningProvider()
        result = provider.invoke("test", output_schema=dict)
        assert isinstance(result, ReasoningResponse)
