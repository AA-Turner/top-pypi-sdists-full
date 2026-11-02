"""Tests for rest_discover function."""

from __future__ import annotations

from unittest.mock import MagicMock

from agentic_devtools.cli.ci.pipeline.discovery.models import DiscoveryOutcome
from agentic_devtools.cli.ci.pipeline.discovery.rest_strategy import (
    parse_suggestion_blocks,
    rest_discover,
)
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


class TestParseSuggestionBlocks:
    """Tests for parse_suggestion_blocks helper."""

    def test_extracts_replacement_content(self) -> None:
        body = "Some text\n```suggestion\nnew_code()\n```\nmore text"
        result = parse_suggestion_blocks(body)
        assert result == "new_code()\n"

    def test_returns_none_when_no_block(self) -> None:
        body = "This is a regular comment without suggestions"
        result = parse_suggestion_blocks(body)
        assert result is None

    def test_empty_suggestion_is_valid_delete(self) -> None:
        body = "Delete this line:\n```suggestion\n```\nend"
        result = parse_suggestion_blocks(body)
        assert result == ""

    def test_indented_suggestion_block_is_parsed(self) -> None:
        """Leading whitespace before opening and closing fences must be handled."""
        body = "Some text\n    ```suggestion\n    new_code()\n    ```\nmore text"
        result = parse_suggestion_blocks(body)
        assert result == "    new_code()\n"


class TestRestDiscover:
    """Tests for rest_discover function."""

    def test_returns_empty_when_no_review_id(self) -> None:
        provider = MagicMock()
        suggestions, attempt = rest_discover(provider, 1, 0)
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY
        assert attempt.method == "rest-rederivation"
        assert attempt.error_message == ""
        assert attempt.details == {"reason": "No review_id provided"}

    def test_returns_error_on_api_exception(self) -> None:
        provider = MagicMock()
        provider.list_review_comments.side_effect = RuntimeError("API error")
        suggestions, attempt = rest_discover(provider, 1, 100)
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ERROR
        assert "API error" in attempt.error_message

    def test_propagates_rate_limit_error(self) -> None:
        """Rate-limit errors escape discovery so the caller can persist cooldown state."""
        provider = MagicMock()
        error = ProviderRateLimitError(provider="github")
        provider.list_review_comments.side_effect = error

        try:
            rest_discover(provider, 1, 100)
        except ProviderRateLimitError as raised:
            assert raised is error
        else:
            raise AssertionError("ProviderRateLimitError should be propagated")

    def test_parses_suggestion_from_comment_body(self) -> None:
        provider = MagicMock()
        comment = MagicMock()
        comment.body = "Fix this:\n```suggestion\nfixed_code()\n```"
        comment.path = "src/main.py"
        comment.id = 42
        comment.line = 10
        comment.start_line = 10
        provider.list_review_comments.return_value = [comment]

        suggestions, attempt = rest_discover(provider, 1, 100)
        assert len(suggestions) == 1
        assert suggestions[0].suggestion_id == "REST_42"
        assert suggestions[0].path == "src/main.py"
        assert suggestions[0].replacement == "fixed_code()\n"
        assert suggestions[0].discovery_source == "rest-rederivation"
        assert attempt.outcome == DiscoveryOutcome.SUCCESS

    def test_detects_anchored_no_replacement(self) -> None:
        provider = MagicMock()
        comment = MagicMock()
        comment.body = "This code could be improved but no suggestion block"
        comment.path = "src/main.py"
        comment.id = 42
        comment.line = 10
        comment.start_line = 10
        provider.list_review_comments.return_value = [comment]

        suggestions, attempt = rest_discover(provider, 1, 100)
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.ANCHORED_NO_REPLACEMENT

    def test_skips_comments_without_path(self) -> None:
        provider = MagicMock()
        comment = MagicMock()
        comment.body = "```suggestion\ncode()\n```"
        comment.path = ""
        comment.id = 42
        comment.line = 10
        comment.start_line = 10
        provider.list_review_comments.return_value = [comment]

        suggestions, attempt = rest_discover(provider, 1, 100)
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY

    def test_skips_suggestion_block_without_closing_fence(self) -> None:
        """Suggestion opener found but parse_suggestion_blocks returns None (unclosed)."""
        provider = MagicMock()
        comment = MagicMock()
        # Has opening fence but no closing fence — parse_suggestion_blocks returns None
        comment.body = "```suggestion\nincomplete code without closing"
        comment.path = "src/main.py"
        comment.id = 55
        comment.line = 5
        comment.start_line = 5
        provider.list_review_comments.return_value = [comment]

        suggestions, attempt = rest_discover(provider, 1, 100)
        assert suggestions == []
        assert attempt.outcome == DiscoveryOutcome.EMPTY

    def test_parses_indented_suggestion_block(self) -> None:
        """Indented suggestion opener/closer must be parsed by rest_discover."""
        provider = MagicMock()
        comment = MagicMock()
        comment.body = "Fix:\n    ```suggestion\n    fixed_code()\n    ```"
        comment.path = "src/utils.py"
        comment.id = 77
        comment.line = 20
        comment.start_line = 20
        provider.list_review_comments.return_value = [comment]

        suggestions, attempt = rest_discover(provider, 1, 100)
        assert len(suggestions) == 1
        assert suggestions[0].replacement == "    fixed_code()\n"
        assert attempt.outcome == DiscoveryOutcome.SUCCESS
