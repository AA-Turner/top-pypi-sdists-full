"""Tests for _collect_candidate_models helper."""

from __future__ import annotations

from agentic_devtools.orchestration.review.nodes.source_context import _collect_candidate_models


class TestCollectCandidateModels:
    """Tests for _collect_candidate_models."""

    def test_returns_empty_when_no_config(self) -> None:
        """Non-dict inputs yield no candidates."""
        assert _collect_candidate_models(None, None) == []

    def test_includes_review_model_id_and_default(self) -> None:
        """Explicit override and default model are both collected."""
        result = _collect_candidate_models(
            {"model_id": "gpt-4o"},
            {"default-model": "gpt-4"},
        )
        assert result == ["gpt-4o", "gpt-4"]

    def test_includes_routing_rule_models(self) -> None:
        """Every routing rule model is collected after the default."""
        result = _collect_candidate_models(
            {},
            {
                "default-model": "gpt-4o",
                "rules": [
                    {"pattern": "*.py", "model": "gpt-4"},
                    {"pattern": "*.ts", "model": "gpt-3.5-turbo"},
                ],
            },
        )
        assert result == ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]

    def test_ignores_blank_and_non_string_and_non_dict_rules(self) -> None:
        """Blank, non-string, and malformed rule entries are skipped."""
        result = _collect_candidate_models(
            {"model_id": "   "},
            {
                "default-model": 123,
                "rules": ["not-a-dict", {"pattern": "*.py"}, {"model": ""}, {"model": "gpt-4"}],
            },
        )
        assert result == ["gpt-4"]

    def test_ignores_non_list_rules(self) -> None:
        """A non-list ``rules`` value is ignored."""
        result = _collect_candidate_models({}, {"default-model": "gpt-4o", "rules": "oops"})
        assert result == ["gpt-4o"]
