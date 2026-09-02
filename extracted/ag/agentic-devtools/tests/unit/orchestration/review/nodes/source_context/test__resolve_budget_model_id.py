"""Tests for _resolve_budget_model_id helper."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.source_context import _resolve_budget_model_id


class TestResolveBudgetModelId:
    """Tests for _resolve_budget_model_id."""

    def test_returns_none_when_no_candidates(self) -> None:
        """No configured models yields ``None``."""
        assert _resolve_budget_model_id(None, None) is None

    def test_picks_most_constrained_model(self) -> None:
        """The smallest-window routed model bounds the budget."""
        result = _resolve_budget_model_id(
            {},
            {
                "default-model": "gpt-4o",
                "rules": [{"pattern": "*.py", "model": "gpt-4"}],
            },
        )
        # gpt-4 has an 8192 window vs gpt-4o's 128000 window.
        assert result == "gpt-4"

    def test_single_known_model_returned(self) -> None:
        """A single resolvable model is returned unchanged."""
        assert _resolve_budget_model_id({"model_id": "gpt-4o"}, {}) == "gpt-4o"

    def test_ignores_unknown_window_candidates(self) -> None:
        """Candidates with an unknown window do not affect the minimum."""
        result = _resolve_budget_model_id(
            {"model_id": "claude-opus-4.8"},
            {"default-model": "gpt-4o"},
        )
        # claude-opus-4.8 has no known window, so gpt-4o wins.
        assert result == "gpt-4o"

    def test_keeps_earlier_smaller_window_over_later_larger(self) -> None:
        """A later candidate with a larger window does not replace the min."""
        result = _resolve_budget_model_id(
            {},
            {
                "default-model": "gpt-4",
                "rules": [{"pattern": "*.ts", "model": "gpt-4o"}],
            },
        )
        # gpt-4 (8192) is seen first; gpt-4o (128000) must not replace it.
        assert result == "gpt-4"

    def test_falls_back_to_first_candidate_when_all_unknown(self) -> None:
        """When no window is known, the first candidate is returned."""
        result = _resolve_budget_model_id(
            {"model_id": "unknown-model-a"},
            {"default-model": "unknown-model-b"},
        )
        assert result == "unknown-model-a"
