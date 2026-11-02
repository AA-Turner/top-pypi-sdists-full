"""Tests for _graphql_error_text."""

from agentic_devtools.cli.ci.github_provider import _graphql_error_text


class TestGraphqlErrorText:
    """Tests for defensive rendering of a GraphQL error message field."""

    def test_returns_non_empty_string_message_unchanged(self) -> None:
        assert _graphql_error_text("field not found") == "field not found"

    def test_returns_placeholder_for_blank_string_message(self) -> None:
        assert _graphql_error_text("   ") == "Unknown GraphQL error"

    def test_returns_placeholder_for_missing_message(self) -> None:
        assert _graphql_error_text(None) == "Unknown GraphQL error"

    def test_renders_non_string_message(self) -> None:
        assert _graphql_error_text(503) == "503"
        assert _graphql_error_text({"code": "X"}) == "{'code': 'X'}"
