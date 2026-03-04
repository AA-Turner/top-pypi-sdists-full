"""Tests for plato.llm - LLM wrapper with ATIF tracing."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from plato.llm import (
    LLMResponse,
    TokenUsage,
    ToolCall,
    _convert_tools_to_openai_format,
    _emit_llm_span,
    _parse_response,
    acompletion,
    completion,
    reset_step_counter,
)

# =============================================================================
# Test tool format conversion
# =============================================================================


class TestConvertToolsToOpenAIFormat:
    def test_anthropic_format(self):
        """Anthropic-style tools get converted to OpenAI format."""
        tools = [
            {
                "name": "list_files",
                "description": "List files in a directory",
                "input_schema": {
                    "type": "object",
                    "properties": {"path": {"type": "string"}},
                    "required": ["path"],
                },
            }
        ]

        result = _convert_tools_to_openai_format(tools)

        assert len(result) == 1
        assert result[0]["type"] == "function"
        assert result[0]["function"]["name"] == "list_files"
        assert result[0]["function"]["description"] == "List files in a directory"
        assert result[0]["function"]["parameters"]["type"] == "object"
        assert "path" in result[0]["function"]["parameters"]["properties"]

    def test_openai_format_passthrough(self):
        """OpenAI-format tools pass through unchanged."""
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get weather",
                    "parameters": {
                        "type": "object",
                        "properties": {"location": {"type": "string"}},
                    },
                },
            }
        ]

        result = _convert_tools_to_openai_format(tools)

        assert result == tools

    def test_mixed_formats(self):
        """Mixed Anthropic and OpenAI tools both get converted."""
        tools = [
            {
                "name": "tool_a",
                "description": "Anthropic style",
                "input_schema": {"type": "object", "properties": {}},
            },
            {
                "type": "function",
                "function": {
                    "name": "tool_b",
                    "description": "OpenAI style",
                    "parameters": {"type": "object", "properties": {}},
                },
            },
        ]

        result = _convert_tools_to_openai_format(tools)

        assert len(result) == 2
        assert result[0]["type"] == "function"
        assert result[0]["function"]["name"] == "tool_a"
        assert result[1]["type"] == "function"
        assert result[1]["function"]["name"] == "tool_b"

    def test_empty_tools(self):
        """Empty tools list returns empty."""
        assert _convert_tools_to_openai_format([]) == []


# =============================================================================
# Test response parsing
# =============================================================================


def _make_mock_response(
    content: str = "Hello",
    tool_calls: list | None = None,
    prompt_tokens: int = 10,
    completion_tokens: int = 5,
    finish_reason: str = "stop",
):
    """Create a mock litellm ModelResponse."""
    message = MagicMock()
    message.content = content
    message.tool_calls = tool_calls

    choice = MagicMock()
    choice.message = message
    choice.finish_reason = finish_reason

    usage = MagicMock()
    usage.prompt_tokens = prompt_tokens
    usage.completion_tokens = completion_tokens
    usage.total_tokens = prompt_tokens + completion_tokens

    response = MagicMock()
    response.choices = [choice]
    response.usage = usage

    return response


class TestParseResponse:
    def test_text_response(self):
        """Parse a simple text response."""
        raw = _make_mock_response(content="Hello world")

        with patch("plato.llm.litellm") as mock_litellm:
            mock_litellm.completion_cost.return_value = 0.001
            result = _parse_response(raw, "test-model")

        assert result.text == "Hello world"
        assert result.tool_calls == []
        assert result.has_tool_calls is False
        assert result.usage.prompt_tokens == 10
        assert result.usage.completion_tokens == 5
        assert result.model == "test-model"
        assert result.stop_reason == "stop"

    def test_tool_call_response(self):
        """Parse a response with tool calls."""
        tc = MagicMock()
        tc.id = "call_123"
        tc.function.name = "get_weather"
        tc.function.arguments = '{"location": "NYC"}'

        raw = _make_mock_response(content="", tool_calls=[tc], finish_reason="tool_calls")

        with patch("plato.llm.litellm") as mock_litellm:
            mock_litellm.completion_cost.return_value = 0.002
            result = _parse_response(raw, "test-model")

        assert result.text == ""
        assert result.has_tool_calls is True
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0].id == "call_123"
        assert result.tool_calls[0].function_name == "get_weather"
        assert result.tool_calls[0].arguments == {"location": "NYC"}
        assert result.stop_reason == "tool_calls"

    def test_no_usage(self):
        """Handle response with no usage info."""
        raw = _make_mock_response()
        raw.usage = None

        with patch("plato.llm.litellm") as mock_litellm:
            mock_litellm.completion_cost.return_value = 0.0
            result = _parse_response(raw, "test-model")

        assert result.usage.prompt_tokens == 0
        assert result.usage.completion_tokens == 0

    def test_cost_error_handled(self):
        """Cost calculation errors don't crash parsing."""
        raw = _make_mock_response()

        with patch("plato.llm.litellm") as mock_litellm:
            mock_litellm.completion_cost.side_effect = Exception("unknown model")
            result = _parse_response(raw, "test-model")

        assert result.cost == 0.0
        assert result.text == "Hello"

    def test_structured_content_not_truncated(self):
        """Structured message content is flattened without truncation."""
        raw = _make_mock_response(content="")
        raw.choices[0].message.content = [
            {"type": "text", "text": "first part "},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64,abc"}},
            {"type": "text", "text": "second part"},
        ]

        with patch("plato.llm.litellm") as mock_litellm:
            mock_litellm.completion_cost.return_value = 0.0
            result = _parse_response(raw, "test-model")

        assert result.text == "first part second part"


# =============================================================================
# Test ATIF span emission
# =============================================================================


class TestEmitLLMSpan:
    def setup_method(self):
        reset_step_counter()

    def test_emits_span_with_attributes(self):
        """Verify span is created with correct ATIF attributes."""
        mock_span = MagicMock()
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_span)
        mock_context.__exit__ = MagicMock(return_value=False)

        mock_tracer = MagicMock()
        mock_tracer.start_as_current_span.return_value = mock_context

        with patch("plato.llm.get_tracer", return_value=mock_tracer):
            response = LLMResponse(
                text="Hello",
                usage=TokenUsage(prompt_tokens=100, completion_tokens=50, total_tokens=150),
                cost=0.005,
                model="anthropic/claude-haiku-4-5-20251001",
                stop_reason="stop",
            )

            _emit_llm_span(
                model="anthropic/claude-haiku-4-5-20251001",
                messages=[{"role": "user", "content": "Hi"}],
                response=response,
                duration_ms=250.0,
            )

        # Verify span was created
        mock_tracer.start_as_current_span.assert_called_once_with("atif.step.1")

        # Verify attributes
        calls = {call.args[0]: call.args[1] for call in mock_span.set_attribute.call_args_list}
        assert calls["atif.step.id"] == 1
        assert calls["atif.step.source"] == "agent"
        assert calls["atif.step.model_name"] == "anthropic/claude-haiku-4-5-20251001"
        assert calls["atif.step.prompt_tokens"] == 100
        assert calls["atif.step.completion_tokens"] == 50
        assert calls["atif.step.cost_usd"] == 0.005
        assert calls["llm.duration_ms"] == 250.0
        assert calls["llm.stop_reason"] == "stop"

    def test_step_counter_increments(self):
        """Step IDs increment across calls."""
        mock_span = MagicMock()
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_span)
        mock_context.__exit__ = MagicMock(return_value=False)

        mock_tracer = MagicMock()
        mock_tracer.start_as_current_span.return_value = mock_context

        response = LLMResponse(text="a", model="m")

        with patch("plato.llm.get_tracer", return_value=mock_tracer):
            _emit_llm_span("m", [], response, 0)
            _emit_llm_span("m", [], response, 0)
            _emit_llm_span("m", [], response, 0)

        span_names = [call.args[0] for call in mock_tracer.start_as_current_span.call_args_list]
        assert span_names == ["atif.step.1", "atif.step.2", "atif.step.3"]

    def test_tool_calls_in_span(self):
        """Tool calls are serialized into the span."""
        mock_span = MagicMock()
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_span)
        mock_context.__exit__ = MagicMock(return_value=False)

        mock_tracer = MagicMock()
        mock_tracer.start_as_current_span.return_value = mock_context

        response = LLMResponse(
            text="",
            tool_calls=[
                ToolCall(id="tc1", function_name="search", arguments={"q": "hello"}),
            ],
            model="m",
        )

        with patch("plato.llm.get_tracer", return_value=mock_tracer):
            _emit_llm_span("m", [], response, 0)

        calls = {call.args[0]: call.args[1] for call in mock_span.set_attribute.call_args_list}
        tool_calls_json = json.loads(calls["atif.step.tool_calls"])
        assert len(tool_calls_json) == 1
        assert tool_calls_json[0]["function_name"] == "search"
        assert tool_calls_json[0]["arguments"] == {"q": "hello"}

    def test_message_not_truncated(self):
        """Span message uses full response text without SDK-side truncation."""
        mock_span = MagicMock()
        mock_context = MagicMock()
        mock_context.__enter__ = MagicMock(return_value=mock_span)
        mock_context.__exit__ = MagicMock(return_value=False)

        mock_tracer = MagicMock()
        mock_tracer.start_as_current_span.return_value = mock_context

        long_text = "x" * 5000
        response = LLMResponse(text=long_text, model="m")

        with patch("plato.llm.get_tracer", return_value=mock_tracer):
            _emit_llm_span("m", [], response, 0)

        calls = [c for c in mock_span.set_attribute.call_args_list if c.args[0] == "atif.step.message"]
        assert len(calls) == 1
        assert calls[0].args[1] == long_text


# =============================================================================
# Test completion() and acompletion()
# =============================================================================


class TestCompletion:
    def setup_method(self):
        reset_step_counter()

    @patch("plato.llm.litellm")
    @patch("plato.llm._emit_llm_span")
    def test_basic_completion(self, mock_emit, mock_litellm):
        """Basic sync completion call."""
        mock_litellm.completion.return_value = _make_mock_response(content="Hi there")
        mock_litellm.completion_cost.return_value = 0.001

        result = completion(
            model="anthropic/claude-haiku-4-5-20251001",
            messages=[{"role": "user", "content": "Hello"}],
        )

        assert result.text == "Hi there"
        mock_litellm.completion.assert_called_once()
        mock_emit.assert_called_once()

    @patch("plato.llm.litellm")
    @patch("plato.llm._emit_llm_span")
    def test_system_prompt_prepended(self, mock_emit, mock_litellm):
        """System prompt is prepended as a system message."""
        mock_litellm.completion.return_value = _make_mock_response()
        mock_litellm.completion_cost.return_value = 0.0

        completion(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": "Hi"}],
            system="You are helpful.",
        )

        call_args = mock_litellm.completion.call_args
        messages = call_args.kwargs["messages"]
        assert messages[0] == {"role": "system", "content": "You are helpful."}
        assert messages[1] == {"role": "user", "content": "Hi"}

    @patch("plato.llm.litellm")
    @patch("plato.llm._emit_llm_span")
    def test_tools_converted(self, mock_emit, mock_litellm):
        """Anthropic-style tools are converted to OpenAI format."""
        mock_litellm.completion.return_value = _make_mock_response()
        mock_litellm.completion_cost.return_value = 0.0

        anthropic_tools = [
            {
                "name": "search",
                "description": "Search things",
                "input_schema": {"type": "object", "properties": {"q": {"type": "string"}}},
            }
        ]

        completion(
            model="anthropic/claude-haiku-4-5-20251001",
            messages=[{"role": "user", "content": "Hi"}],
            tools=anthropic_tools,
        )

        call_args = mock_litellm.completion.call_args
        tools = call_args.kwargs["tools"]
        assert tools[0]["type"] == "function"
        assert tools[0]["function"]["name"] == "search"

    @patch("plato.llm.litellm")
    @patch("plato.llm._emit_llm_span")
    def test_extra_kwargs_passed(self, mock_emit, mock_litellm):
        """Extra kwargs are forwarded to litellm."""
        mock_litellm.completion.return_value = _make_mock_response()
        mock_litellm.completion_cost.return_value = 0.0

        completion(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": "Hi"}],
            top_p=0.9,
            seed=42,
        )

        call_args = mock_litellm.completion.call_args
        assert call_args.kwargs["top_p"] == 0.9
        assert call_args.kwargs["seed"] == 42


@pytest.mark.asyncio
class TestACompletion:
    def setup_method(self):
        reset_step_counter()

    @patch("plato.llm.litellm")
    @patch("plato.llm._emit_llm_span")
    async def test_basic_acompletion(self, mock_emit, mock_litellm):
        """Basic async completion call."""
        mock_litellm.acompletion = AsyncMock(return_value=_make_mock_response(content="Async hi"))
        mock_litellm.completion_cost.return_value = 0.001

        result = await acompletion(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": "Hello"}],
        )

        assert result.text == "Async hi"
        mock_litellm.acompletion.assert_called_once()
        mock_emit.assert_called_once()

    @patch("plato.llm.litellm")
    @patch("plato.llm._emit_llm_span")
    async def test_async_with_tools(self, mock_emit, mock_litellm):
        """Async completion with tools."""
        tc = MagicMock()
        tc.id = "call_abc"
        tc.function.name = "read_file"
        tc.function.arguments = '{"path": "/tmp/a.txt"}'

        mock_litellm.acompletion = AsyncMock(
            return_value=_make_mock_response(content="", tool_calls=[tc], finish_reason="tool_calls")
        )
        mock_litellm.completion_cost.return_value = 0.0

        result = await acompletion(
            model="anthropic/claude-haiku-4-5-20251001",
            messages=[{"role": "user", "content": "Read the file"}],
            tools=[
                {
                    "name": "read_file",
                    "description": "Read a file",
                    "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}},
                }
            ],
        )

        assert result.has_tool_calls
        assert result.tool_calls[0].function_name == "read_file"
        assert result.tool_calls[0].arguments == {"path": "/tmp/a.txt"}


# =============================================================================
# Test LLMResponse dataclass
# =============================================================================


class TestLLMResponse:
    def test_has_tool_calls_false(self):
        r = LLMResponse(text="hello")
        assert r.has_tool_calls is False

    def test_has_tool_calls_true(self):
        r = LLMResponse(tool_calls=[ToolCall(id="1", function_name="f")])
        assert r.has_tool_calls is True

    def test_defaults(self):
        r = LLMResponse()
        assert r.text == ""
        assert r.tool_calls == []
        assert r.usage.prompt_tokens == 0
        assert r.cost == 0.0
        assert r.model == ""
        assert r.stop_reason == ""
        assert r.raw is None
