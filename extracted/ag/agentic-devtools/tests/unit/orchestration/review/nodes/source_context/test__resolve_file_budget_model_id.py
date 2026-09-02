"""Tests for _resolve_file_budget_model_id helper."""

from __future__ import annotations

import sys
from unittest.mock import patch

from agentic_devtools.orchestration.review.nodes.source_context import _resolve_file_budget_model_id


class TestResolveFileBudgetModelId:
    """Tests for _resolve_file_budget_model_id."""

    def test_uses_file_routing_when_rules_match(self) -> None:
        """Routing resolves to per-file rule model when pattern matches."""
        result = _resolve_file_budget_model_id(
            "/src/app.py",
            {"default-model": "gpt-4o", "rules": [{"pattern": "*.py", "model": "gpt-4"}]},
        )
        assert result == "gpt-4"

    def test_non_dict_model_config_uses_routing(self) -> None:
        """A non-dict model_config_raw passes None to resolver; returns None when ImportError."""
        with patch.dict(sys.modules, {"agentic_devtools.orchestration.review.model_routing": None}):
            result = _resolve_file_budget_model_id("/src/app.py", None)
        assert result is None

    @patch("agentic_devtools.orchestration.review.model_routing.resolve_model_for_file", return_value=123)
    def test_returns_none_when_routing_result_is_not_string(self, mock_resolve_model) -> None:
        """Non-string routing results are rejected."""
        result = _resolve_file_budget_model_id("/src/app.py", {"default-model": "gpt-4o"})
        assert result is None
        mock_resolve_model.assert_called_once()

    def test_returns_none_when_model_routing_import_fails(self) -> None:
        """Import failures fall back to None so TokenBudget uses its default model handling."""
        with patch.dict(sys.modules, {"agentic_devtools.orchestration.review.model_routing": None}):
            assert _resolve_file_budget_model_id("/src/app.py", {}) is None

    @patch("agentic_devtools.orchestration.review.model_routing.resolve_model_for_file")
    def test_passes_provider_default_model_as_default(self, mock_resolve_model) -> None:
        """provider_default_model is forwarded to resolve_model_for_file as default_model."""
        mock_resolve_model.return_value = "gpt-4o"
        result = _resolve_file_budget_model_id(
            "/src/app.py",
            {},
            provider_default_model="gpt-4o",
        )
        assert result == "gpt-4o"
        mock_resolve_model.assert_called_once_with(
            "/src/app.py",
            {},
            default_model="gpt-4o",
        )

    @patch("agentic_devtools.orchestration.review.model_routing.resolve_model_for_file")
    def test_provider_default_model_used_when_no_per_file_rule(self, mock_resolve_model) -> None:
        """When no per-file routing rule matches, provider_default_model is the effective fallback."""
        mock_resolve_model.return_value = "gpt-4o"
        result = _resolve_file_budget_model_id(
            "/src/app.py",
            None,
            provider_default_model="gpt-4o",
        )
        assert result == "gpt-4o"
        mock_resolve_model.assert_called_once_with(
            "/src/app.py",
            None,
            default_model="gpt-4o",
        )

    @patch("agentic_devtools.orchestration.review.model_routing.resolve_model_for_file")
    def test_none_provider_default_model_passes_none_to_resolver(self, mock_resolve_model) -> None:
        """Absence of provider_default_model passes None to resolve_model_for_file unchanged."""
        mock_resolve_model.return_value = "gpt-4o"
        _resolve_file_budget_model_id("/src/app.py", {})
        mock_resolve_model.assert_called_once_with(
            "/src/app.py",
            {},
            default_model=None,
        )

    @patch("agentic_devtools.orchestration.review.model_routing.resolve_model_for_file")
    def test_requested_model_takes_precedence_over_provider_default(self, mock_resolve_model) -> None:
        """Source-context budgeting mirrors the review runner's requested-model precedence."""
        result = _resolve_file_budget_model_id(
            "/src/app.py",
            {},
            requested_model="gemini-3.7-flash",
            provider_default_model="gpt-4o",
        )
        assert result == "gemini-3.7-flash"
        mock_resolve_model.assert_not_called()
