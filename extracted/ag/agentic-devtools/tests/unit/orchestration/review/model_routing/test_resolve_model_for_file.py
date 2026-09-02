"""Tests for resolve_model_for_file()."""

from __future__ import annotations

from unittest.mock import patch

from agentic_devtools.orchestration.review.model_routing import resolve_model_for_file


class TestResolveModelForFile:
    """Tests for file-pattern-based model selection."""

    def test_default_model_when_no_config(self) -> None:
        """Returns default model when no config is provided."""
        with patch("agentic_devtools.state.get_value", return_value="test-model"):
            result = resolve_model_for_file("/src/main.py", None)
        assert result == "test-model"

    def test_explicit_default_model_takes_precedence_when_no_config(self) -> None:
        """A caller-supplied default model is used before state fallback."""
        with patch("agentic_devtools.state.get_value", return_value="state-model") as mock_get_value:
            result = resolve_model_for_file("/src/main.py", None, default_model="provider-model")
        assert result == "provider-model"
        mock_get_value.assert_not_called()

    def test_default_model_from_config(self) -> None:
        """Returns default-model from config when no rules match."""
        result = resolve_model_for_file(
            "/src/main.py",
            {"default-model": "gpt-4o", "rules": []},
        )
        assert result == "gpt-4o"

    def test_empty_config_default_falls_back_to_state_model(self) -> None:
        """An empty default-model falls back to the state-derived default."""
        with patch("agentic_devtools.state.get_value", return_value="state-model"):
            result = resolve_model_for_file(
                "/src/main.py",
                {"default-model": "", "rules": []},
            )

        assert result == "state-model"

    def test_non_list_rules_returns_default_model(self) -> None:
        """Invalid rules payloads are ignored in favor of the default."""
        result = resolve_model_for_file(
            "/src/main.py",
            {"default-model": "claude-sonnet", "rules": "*.py"},
        )
        assert result == "claude-sonnet"

    def test_pattern_match_python_file(self) -> None:
        """Matches *.py pattern and returns configured model."""
        config = {
            "default-model": "gpt-4o",
            "rules": [
                {"pattern": "*.py", "model": "claude-opus-4"},
                {"pattern": "*.ts", "model": "gpt-4o-mini"},
            ],
        }
        result = resolve_model_for_file("/src/main.py", config)
        assert result == "claude-opus-4"

    def test_pattern_match_typescript_file(self) -> None:
        """Matches *.ts pattern and returns configured model."""
        config = {
            "default-model": "gpt-4o",
            "rules": [
                {"pattern": "*.py", "model": "claude-opus-4"},
                {"pattern": "*.ts", "model": "gpt-4o-mini"},
            ],
        }
        result = resolve_model_for_file("/src/app.ts", config)
        assert result == "gpt-4o-mini"

    def test_no_matching_pattern_uses_default(self) -> None:
        """Falls back to default when no pattern matches."""
        config = {
            "default-model": "gpt-4o",
            "rules": [
                {"pattern": "*.py", "model": "claude-opus-4"},
            ],
        }
        result = resolve_model_for_file("/src/styles.css", config)
        assert result == "gpt-4o"

    def test_first_matching_rule_wins(self) -> None:
        """First matching rule takes precedence."""
        config = {
            "default-model": "default",
            "rules": [
                {"pattern": "*.py", "model": "first-match"},
                {"pattern": "*.py", "model": "second-match"},
            ],
        }
        result = resolve_model_for_file("test.py", config)
        assert result == "first-match"

    def test_empty_rules_uses_default(self) -> None:
        """Empty rules list uses default model."""
        config = {"default-model": "my-default", "rules": []}
        result = resolve_model_for_file("file.py", config)
        assert result == "my-default"

    def test_invalid_rule_skipped(self) -> None:
        """Invalid rules (non-dict) are skipped."""
        config = {
            "default-model": "fallback",
            "rules": ["not-a-dict", {"pattern": "*.py", "model": "valid"}],
        }
        result = resolve_model_for_file("test.py", config)
        assert result == "valid"

    def test_missing_pattern_or_model_is_ignored(self) -> None:
        """Partially defined rules do not match files."""
        config = {
            "default-model": "fallback",
            "rules": [
                {"pattern": "*.py"},
                {"model": "claude-opus-4"},
            ],
        }
        result = resolve_model_for_file("test.py", config)
        assert result == "fallback"

    def test_default_model_falls_back_to_builtin_when_state_lookup_fails(self) -> None:
        """State lookup failures still return the hard-coded model fallback."""
        with patch("agentic_devtools.state.get_value", side_effect=RuntimeError("boom")):
            result = resolve_model_for_file("/src/main.py", None)

        assert result == "gpt-4o"

    def test_empty_state_model_falls_back_to_builtin_default(self) -> None:
        """An empty state model still falls back to the hard-coded default."""
        with patch("agentic_devtools.state.get_value", return_value=""):
            result = resolve_model_for_file("/src/main.py", None)

        assert result == "gpt-4o"
