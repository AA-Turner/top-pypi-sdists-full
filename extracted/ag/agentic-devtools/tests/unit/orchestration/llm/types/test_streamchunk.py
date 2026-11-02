"""Tests for StreamChunk dataclass."""

from agentic_devtools.orchestration.llm.types import StreamChunk, TokenUsage


class TestStreamChunk:
    """Tests for StreamChunk."""

    def test_basic_creation(self):
        chunk = StreamChunk(text_delta="Hello")
        assert chunk.text_delta == "Hello"
        assert chunk.chunk_index is None
        assert chunk.finish_reason is None
        assert chunk.token_usage is None
        assert chunk.model is None

    def test_with_metadata(self):
        chunk = StreamChunk(text_delta="world", chunk_index=5, finish_reason=None, model="gemini-3.7-flash")
        assert chunk.chunk_index == 5
        assert chunk.finish_reason is None
        assert chunk.model == "gemini-3.7-flash"

    def test_final_chunk_with_usage(self):
        usage = TokenUsage(input_tokens=100, output_tokens=50, total_tokens=150)
        chunk = StreamChunk(
            text_delta="",
            chunk_index=10,
            finish_reason="stop",
            token_usage=usage,
        )
        assert chunk.finish_reason == "stop"
        assert chunk.token_usage == usage

    def test_frozen(self):
        chunk = StreamChunk(text_delta="x")
        try:
            chunk.text_delta = "y"  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass
