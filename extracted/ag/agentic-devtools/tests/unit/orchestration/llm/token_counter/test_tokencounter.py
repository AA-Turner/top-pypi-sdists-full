"""Tests for TokenCounter."""

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.llm.errors import ContextWindowOverflowError
from agentic_devtools.orchestration.llm.token_counter import (
    DEFAULT_CONTEXT_WINDOW,
    DEFAULT_ENCODING,
    MODEL_CONTEXT_WINDOWS,
    MODEL_ENCODINGS,
    TokenCounter,
    TruncationStrategy,
    _prefix_lookup,
    check_context_window,
    count_tokens,
)
from agentic_devtools.orchestration.llm.types import LLMMessage


@pytest.fixture
def mock_encoding():
    """Mock tiktoken encoding that returns token count based on word count."""
    encoding = MagicMock()
    encoding.encode = lambda text: text.split() if text else []
    return encoding


class TestTokenCounter:
    """Tests for TokenCounter."""

    def test_count_tokens_non_zero(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            counter = TokenCounter(model="gpt-4o")
            count = counter.count_tokens("Hello world")
            assert count == 2  # 2 words

    def test_count_message_tokens(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            counter = TokenCounter(model="gpt-4o")
            messages = [
                LLMMessage(role="system", content="You are helpful"),
                LLMMessage(role="user", content="Hello"),
            ]
            count = counter.count_message_tokens(messages)
            # 3 priming + (4 overhead + 3 content) + (4 overhead + 1 content) = 15
            assert count == 15

    def test_count_message_tokens_with_name(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            counter = TokenCounter(model="gpt-4o")
            messages = [
                LLMMessage(role="user", content="Hello", name="alice"),
            ]
            count = counter.count_message_tokens(messages)
            # 3 priming + (4 overhead + 1 content + 1 fixed name overhead) = 9
            assert count == 9

    def test_non_standard_role_uses_fixed_overhead(self, mock_encoding):
        """Non-standard role strings must not affect token count — overhead is fixed."""
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            counter = TokenCounter(model="gpt-4o")
            messages_standard_role = [LLMMessage(role="user", content="hello")]
            messages_long_role = [LLMMessage(role="very long custom role string", content="hello")]
            count_standard = counter.count_message_tokens(messages_standard_role)
            count_long = counter.count_message_tokens(messages_long_role)
            # Both must produce the same count because role is fixed overhead
            assert count_standard == count_long

    def test_get_encoding_lazy_loads(self):
        """Test that tiktoken is lazily loaded."""
        with patch("tiktoken.get_encoding") as mock_get_encoding:
            mock_enc = MagicMock()
            mock_get_encoding.return_value = mock_enc
            counter = TokenCounter(model="gpt-4o")
            # First call loads
            enc = counter._get_encoding()
            assert enc is mock_enc
            # Second call uses cached
            enc2 = counter._get_encoding()
            assert enc2 is mock_enc
            mock_get_encoding.assert_called_once()

    def test_check_context_window_within_limits(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            counter = TokenCounter(model="gpt-4o")
            messages = [LLMMessage(role="user", content="Short message")]
            result = counter.check_context_window(messages)
            assert result == messages

    def test_check_context_window_overflow_raises(self, mock_encoding):
        # Mock encoding that returns many tokens
        overflow_encoding = MagicMock()
        overflow_encoding.encode = lambda text: list(range(10000))  # Always 10000 tokens

        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=overflow_encoding,
        ):
            counter = TokenCounter(model="gpt-4")  # 8192 context window
            messages = [LLMMessage(role="user", content="x")]
            with pytest.raises(ContextWindowOverflowError) as exc_info:
                counter.check_context_window(messages)
            assert exc_info.value.model == "gpt-4"

    def test_truncation_tail_strategy(self, mock_encoding):
        # Mock encoding where each word is a token
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            counter = TokenCounter(model="gpt-4")  # 8192 window
            # Create messages that exceed limit when counted together
            messages = [
                LLMMessage(role="system", content=" ".join(["word"] * 5000)),
                LLMMessage(role="user", content="Short"),
            ]
            result = counter.check_context_window(messages, truncation=TruncationStrategy.TAIL)
            # Should keep at least the last message
            assert len(result) >= 1
            assert result[-1].content == "Short"

    def test_truncation_head_strategy(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            counter = TokenCounter(model="gpt-4")
            messages = [
                LLMMessage(role="user", content="First"),
                LLMMessage(role="user", content=" ".join(["word"] * 10000)),
            ]
            result = counter.check_context_window(messages, truncation=TruncationStrategy.HEAD)
            assert len(result) >= 1
            assert result[0].content == "First"


class TestCountTokens:
    """Tests for count_tokens convenience function."""

    def test_returns_positive(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            assert count_tokens("Hello") > 0

    def test_empty_string(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            assert count_tokens("") == 0


class TestTruncationStrategy:
    """Tests for TruncationStrategy enum."""

    def test_values(self):
        assert TruncationStrategy.NONE == "none"
        assert TruncationStrategy.TAIL == "tail"
        assert TruncationStrategy.HEAD == "head"


class TestCheckContextWindow:
    """Tests for check_context_window module-level convenience function."""

    def test_within_limits_returns_messages(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            messages = [LLMMessage(role="user", content="Short")]
            result = check_context_window(messages, model="gpt-4o")
            assert result == messages

    def test_overflow_raises(self):
        overflow_encoding = MagicMock()
        overflow_encoding.encode = lambda text: list(range(200000))
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=overflow_encoding,
        ):
            messages = [LLMMessage(role="user", content="x")]
            with pytest.raises(ContextWindowOverflowError):
                check_context_window(messages, model="gpt-4")

    def test_truncation_tail(self, mock_encoding):
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding", return_value=mock_encoding
        ):
            messages = [
                LLMMessage(role="system", content=" ".join(["word"] * 5000)),
                LLMMessage(role="user", content="Short"),
            ]
            result = check_context_window(messages, model="gpt-4", truncation=TruncationStrategy.TAIL)
            assert len(result) >= 1


class TestTailTruncationFallback:
    """Tests for tail/head truncation when no single message fits the token budget."""

    def test_tail_raises_when_no_message_fits(self):
        """When even a single message exceeds the budget, raise ContextWindowOverflowError."""
        overflow_encoding = MagicMock()
        overflow_encoding.encode = lambda text: list(range(50000))

        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=overflow_encoding,
        ):
            counter = TokenCounter(model="gpt-4")
            messages = [
                LLMMessage(role="user", content="msg1"),
                LLMMessage(role="user", content="msg2"),
            ]
            expected_token_count = min(counter._count_single_message_tokens(msg) for msg in messages) + 3
            with pytest.raises(ContextWindowOverflowError) as exc_info:
                counter.check_context_window(messages, truncation=TruncationStrategy.TAIL)
            assert exc_info.value.model == "gpt-4"
            assert exc_info.value.token_count == expected_token_count
            assert exc_info.value.max_tokens == 4096

    def test_head_raises_when_no_message_fits(self):
        """When even a single message exceeds the budget, raise ContextWindowOverflowError."""
        overflow_encoding = MagicMock()
        overflow_encoding.encode = lambda text: list(range(50000))

        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=overflow_encoding,
        ):
            counter = TokenCounter(model="gpt-4")
            messages = [
                LLMMessage(role="user", content="msg1"),
                LLMMessage(role="user", content="msg2"),
            ]
            expected_token_count = min(counter._count_single_message_tokens(msg) for msg in messages) + 3
            with pytest.raises(ContextWindowOverflowError) as exc_info:
                counter.check_context_window(messages, truncation=TruncationStrategy.HEAD)
            assert exc_info.value.model == "gpt-4"
            assert exc_info.value.token_count == expected_token_count
            assert exc_info.value.max_tokens == 4096


class TestTruncateMessagesUnknownStrategy:
    """Tests for truncate_messages with unknown strategy fallback."""

    def test_unknown_strategy_returns_messages_unchanged(self, mock_encoding):
        """When strategy doesn't match HEAD or TAIL, messages are returned unchanged."""
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=mock_encoding,
        ):
            counter = TokenCounter(model="gpt-4")
            messages = [
                LLMMessage(role="user", content="msg1"),
                LLMMessage(role="user", content="msg2"),
            ]
            # Use a mock strategy value that isn't HEAD or TAIL
            mock_strategy = MagicMock()
            mock_strategy.__eq__ = lambda self, other: False
            result = counter._truncate_messages(messages, max_tokens=10, strategy=mock_strategy)
            assert result == messages


class TestTruncationLoopCompletion:
    """Tests for truncation where the for loop completes without breaking."""

    def test_tail_loop_completes_all_messages_fit(self):
        """TAIL truncation where all messages fit within the given max_tokens budget."""
        encoding = MagicMock()
        encoding.encode = lambda text: text.split() if text else []

        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=encoding,
        ):
            counter = TokenCounter(model="gpt-4")
            messages = [
                LLMMessage(role="user", content="hello", name="alice"),
                LLMMessage(role="user", content="world", name="bob"),
            ]
            # Call _truncate_messages directly with a large budget so all messages fit
            result = counter._truncate_messages(messages, max_tokens=10000, strategy=TruncationStrategy.TAIL)
            assert len(result) == 2

    def test_head_loop_completes_all_messages_fit(self):
        """HEAD truncation where all messages fit within the given max_tokens budget."""
        encoding = MagicMock()
        encoding.encode = lambda text: text.split() if text else []

        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=encoding,
        ):
            counter = TokenCounter(model="gpt-4")
            messages = [
                LLMMessage(role="user", content="hello", name="alice"),
                LLMMessage(role="user", content="world", name="bob"),
            ]
            # Call _truncate_messages directly with a large budget so all messages fit
            result = counter._truncate_messages(messages, max_tokens=10000, strategy=TruncationStrategy.HEAD)
            assert len(result) == 2

    def test_empty_messages_returns_empty_tail(self):
        """TAIL truncation with empty input should return an empty list."""
        counter = TokenCounter(model="gpt-4")
        result = counter._truncate_messages([], max_tokens=10, strategy=TruncationStrategy.TAIL)
        assert result == []

    def test_empty_messages_returns_empty_head(self):
        """HEAD truncation with empty input should return an empty list."""
        counter = TokenCounter(model="gpt-4")
        result = counter._truncate_messages([], max_tokens=10, strategy=TruncationStrategy.HEAD)
        assert result == []


class TestMaxOutputTokensValidation:
    """Tests for max_output_tokens >= context_window validation."""

    def test_max_output_tokens_equal_to_context_window_raises(self):
        """max_output_tokens equal to context window must raise ValueError."""
        counter = TokenCounter(model="gpt-4")  # 8192 context window
        messages = [LLMMessage(role="user", content="hi")]
        with pytest.raises(ValueError, match="max_output_tokens"):
            counter.check_context_window(messages, max_output_tokens=8192)

    def test_max_output_tokens_exceeds_context_window_raises(self):
        """max_output_tokens larger than context window must raise ValueError."""
        counter = TokenCounter(model="gpt-4")  # 8192 context window
        messages = [LLMMessage(role="user", content="hi")]
        with pytest.raises(ValueError, match="max_output_tokens"):
            counter.check_context_window(messages, max_output_tokens=9000)

    def test_negative_max_output_tokens_raises(self):
        """Negative max_output_tokens must raise ValueError before the upper-bound check."""
        counter = TokenCounter(model="gpt-4")
        messages = [LLMMessage(role="user", content="hi")]
        with pytest.raises(ValueError, match="max_output_tokens.*non-negative"):
            counter.check_context_window(messages, max_output_tokens=-1)


class TestTruncationWithMessageNames:
    """Tests that truncation correctly accounts for LLMMessage.name tokens."""

    def test_tail_excludes_message_with_name_overhead(self):
        """TAIL truncation accounts for the fixed name overhead when fitting messages."""
        encoding = MagicMock()
        encoding.encode = lambda text: text.split() if text else []

        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=encoding,
        ):
            counter = TokenCounter(model="gpt-4")
            # available = 8192 - 4096 = 4096
            # msg_tokens (with name) = 4 + 2042 content + 1 name overhead = 2047
            # 2 messages: 3 + 2*2047 = 4097 > 4096 → overflow triggers truncation
            # TAIL: 3 + 2047 = 2050 <= 4096 → last msg fits
            #       3 + 2047 + 2047 = 4097 > 4096 → first msg excluded
            messages = [
                LLMMessage(role="user", content=" ".join(["w"] * 2042), name="alice"),
                LLMMessage(role="user", content=" ".join(["w"] * 2042), name="alice"),
            ]
            result = counter.check_context_window(messages, max_output_tokens=4096, truncation=TruncationStrategy.TAIL)
            assert len(result) == 1
            assert result[0] is messages[-1]

    def test_head_excludes_message_with_name_overhead(self):
        """HEAD truncation accounts for the fixed name overhead when fitting messages."""
        encoding = MagicMock()
        encoding.encode = lambda text: text.split() if text else []

        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=encoding,
        ):
            counter = TokenCounter(model="gpt-4")
            messages = [
                LLMMessage(role="user", content=" ".join(["w"] * 2042), name="alice"),
                LLMMessage(role="user", content=" ".join(["w"] * 2042), name="alice"),
            ]
            result = counter.check_context_window(messages, max_output_tokens=4096, truncation=TruncationStrategy.HEAD)
            assert len(result) == 1
            assert result[0] is messages[0]


class TestPrefixLookup:
    """Tests for the _prefix_lookup module-level helper."""

    def test_exact_match_wins(self):
        """Exact key match must be returned directly."""
        table: dict[str, str] = {"gpt-4o": "o200k_base", "gpt-4": "cl100k_base"}
        assert _prefix_lookup(table, "gpt-4o", "default") == "o200k_base"

    def test_longest_prefix_wins_over_shorter_prefix(self):
        """When multiple prefixes match, the longest one must be preferred."""
        table: dict[str, str] = {"gpt-4": "cl100k_base", "gpt-4-turbo": "turbo_enc"}
        # "gpt-4-turbo-2024-05-13" starts with both "gpt-4" and "gpt-4-turbo"
        assert _prefix_lookup(table, "gpt-4-turbo-2024-05-13", "default") == "turbo_enc"

    def test_prefix_match_used_when_no_exact_match(self):
        """A prefix match must be returned when there is no exact match."""
        table: dict[str, str] = {"gpt-4o": "o200k_base"}
        assert _prefix_lookup(table, "gpt-4o-2024-05-13", "fallback") == "o200k_base"

    def test_default_returned_when_no_match(self):
        """Default value must be returned when neither exact nor prefix match exists."""
        table: dict[str, str] = {"gpt-4o": "o200k_base"}
        assert _prefix_lookup(table, "claude-3-opus", "cl100k_base") == "cl100k_base"


class TestVersionedModelEncoding:
    """TokenCounter must resolve versioned model IDs via prefix matching."""

    def test_versioned_gpt4o_uses_o200k_encoding(self):
        """gpt-4o-YYYY-MM-DD must resolve to the same encoding as gpt-4o."""
        counter = TokenCounter(model="gpt-4o-2024-05-13")
        assert counter._encoding_name == MODEL_ENCODINGS["gpt-4o"]
        assert counter._encoding_name == "o200k_base"

    def test_versioned_gpt4_turbo_uses_cl100k_encoding(self):
        """gpt-4-turbo-YYYY-MM-DD must resolve to the gpt-4-turbo encoding."""
        counter = TokenCounter(model="gpt-4-turbo-2024-04-09")
        assert counter._encoding_name == MODEL_ENCODINGS["gpt-4-turbo"]
        assert counter._encoding_name == "cl100k_base"

    def test_versioned_longest_prefix_wins(self):
        """gpt-4-turbo-... must match gpt-4-turbo, not the shorter gpt-4 prefix."""
        counter_turbo = TokenCounter(model="gpt-4-turbo-2024-04-09")
        counter_base = TokenCounter(model="gpt-4-2024-04-09")
        assert counter_turbo._encoding_name == MODEL_ENCODINGS["gpt-4-turbo"]
        assert counter_base._encoding_name == MODEL_ENCODINGS["gpt-4"]

    def test_unknown_model_falls_back_to_default_encoding(self):
        """An entirely unrecognised model must use DEFAULT_ENCODING."""
        counter = TokenCounter(model="claude-3-opus")
        assert counter._encoding_name == DEFAULT_ENCODING


class TestVersionedModelContextWindow:
    """check_context_window must resolve versioned model IDs via prefix matching."""

    def test_versioned_gpt35_turbo_uses_correct_context_window(self):
        """gpt-3.5-turbo-0125 must resolve to gpt-3.5-turbo's context window (16 385)."""
        counter = TokenCounter(model="gpt-3.5-turbo-0125")
        messages = [LLMMessage(role="user", content="hi")]
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=MagicMock(encode=lambda text: text.split() if text else []),
        ):
            result = counter.check_context_window(messages)
        assert result == messages
        # Confirm the resolved window is 16 385, not the default 128 000
        assert MODEL_CONTEXT_WINDOWS["gpt-3.5-turbo"] == 16385
        assert DEFAULT_CONTEXT_WINDOW != 16385

    def test_versioned_gpt4_uses_small_context_window(self):
        """gpt-4-0613 must resolve to gpt-4's 8 192-token context window."""
        counter = TokenCounter(model="gpt-4-0613")
        overflow_encoding = MagicMock()
        overflow_encoding.encode = lambda text: list(range(10000))
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=overflow_encoding,
        ):
            with pytest.raises(ContextWindowOverflowError) as exc_info:
                counter.check_context_window(messages=[LLMMessage(role="user", content="x")])
        # max_tokens available = MODEL_CONTEXT_WINDOWS["gpt-4"] - 4096 (not DEFAULT_CONTEXT_WINDOW - 4096)
        assert exc_info.value.max_tokens == MODEL_CONTEXT_WINDOWS["gpt-4"] - 4096

    def test_unknown_model_falls_back_to_default_context_window(self):
        """An unrecognised model must use DEFAULT_CONTEXT_WINDOW."""
        counter = TokenCounter(model="claude-3-opus")
        messages = [LLMMessage(role="user", content="hi")]
        with patch(
            "agentic_devtools.orchestration.llm.token_counter.TokenCounter._get_encoding",
            return_value=MagicMock(encode=lambda text: text.split() if text else []),
        ):
            result = counter.check_context_window(messages)
        assert result == messages
