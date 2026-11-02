"""Tests for resolve_rubber_duck_models."""

import logging

from agentic_devtools.cli.azure_devops.review_reviewer_models import (
    AGENT_PICKS,
    resolve_rubber_duck_models,
)
from agentic_devtools.cli.config.pull_request_review_config import (
    PullRequestReviewConfig,
    RubberDuckConfig,
)


def _config(*, main=None, sub=None, enabled=True):
    """Build a PullRequestReviewConfig with the given rubber-duck layers."""
    rubber = RubberDuckConfig(
        enabled=enabled,
        mainAgent=main if main is not None else [],
        subagent=sub if sub is not None else [],
    )
    return PullRequestReviewConfig(rubberDuck=rubber)


class TestResolveRubberDuckModels:
    """Tests for resolve_rubber_duck_models."""

    def test_config_none_returns_agent_picks(self, caplog):
        """A None config never raises and returns the AGENT_PICKS sentinel."""
        with caplog.at_level(logging.WARNING):
            result = resolve_rubber_duck_models("mainAgent", "claude-opus-4.6", ["gpt-5.3-codex"], None)
        assert result is AGENT_PICKS
        assert any("not configured as a list" in r.message for r in caplog.records)

    def test_layer_not_a_list_returns_agent_picks(self, caplog):
        """A non-list layer (e.g. a string) returns AGENT_PICKS with a warning."""
        config = PullRequestReviewConfig(rubberDuck=RubberDuckConfig(mainAgent="oops"))
        with caplog.at_level(logging.WARNING):
            result = resolve_rubber_duck_models("mainAgent", None, ["gpt-5.3-codex"], config)
        assert result is AGENT_PICKS
        assert any("not configured as a list" in r.message for r in caplog.records)

    def test_valid_two_distinct_families_different_from_author(self):
        """Two valid, distinct-family models different from the author are returned."""
        config = _config(main=["gpt-5.3-codex", "gemini-3.1-pro-preview"])
        result = resolve_rubber_duck_models(
            "mainAgent",
            "claude-opus-4.6",
            ["gpt-5.3-codex", "gemini-3.1-pro-preview"],
            config,
        )
        assert result == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]

    def test_invalid_entries_are_dropped(self, caplog):
        """Non-string and blank entries are dropped with a warning."""
        config = _config(main=[123, "", "   ", "gpt-5.3-codex"])
        with caplog.at_level(logging.WARNING):
            result = resolve_rubber_duck_models("mainAgent", "claude-opus-4.6", ["gpt-5.3-codex"], config)
        assert result == ["gpt-5.3-codex"]
        assert any("invalid rubber-duck model entry" in r.message for r in caplog.records)

    def test_models_not_in_available_are_dropped(self, caplog):
        """Models absent from availableModels are dropped with a warning."""
        config = _config(main=["unknown-model", "gpt-5.3-codex"])
        with caplog.at_level(logging.WARNING):
            result = resolve_rubber_duck_models("mainAgent", "claude-opus-4.6", ["gpt-5.3-codex"], config)
        assert result == ["gpt-5.3-codex"]
        assert any("not in availableModels" in r.message for r in caplog.records)

    def test_duplicate_models_are_deduped(self):
        """Duplicate valid entries collapse to a single model."""
        config = _config(main=["gpt-5.3-codex", "gpt-5.3-codex"])
        result = resolve_rubber_duck_models("mainAgent", "claude-opus-4.6", ["gpt-5.3-codex"], config)
        assert result == ["gpt-5.3-codex"]

    def test_all_invalid_returns_agent_picks(self, caplog):
        """When every configured model is invalid, AGENT_PICKS is returned."""
        config = _config(main=["nope"])
        with caplog.at_level(logging.WARNING):
            result = resolve_rubber_duck_models("mainAgent", "claude-opus-4.6", ["gpt-5.3-codex"], config)
        assert result is AGENT_PICKS
        assert any("No valid rubber-duck models" in r.message for r in caplog.records)

    def test_available_models_none_returns_agent_picks(self):
        """A None availableModels inventory drops everything → AGENT_PICKS."""
        config = _config(main=["gpt-5.3-codex"])
        result = resolve_rubber_duck_models("mainAgent", "claude-opus-4.6", None, config)
        assert result is AGENT_PICKS

    def test_subagent_layer_is_resolved(self):
        """The 'subagent' layer is read from config.rubberDuck.subagent."""
        config = _config(sub=["gpt-5.3-codex"])
        result = resolve_rubber_duck_models("subagent", "claude-opus-4.6", ["gpt-5.3-codex"], config)
        assert result == ["gpt-5.3-codex"]

    def test_same_family_pair_filled_best_effort(self):
        """Two same-family models are both returned (best-effort, distinct preferred)."""
        config = _config(main=["gpt-5.3-codex", "gpt-4o"])
        result = resolve_rubber_duck_models(
            "mainAgent",
            "claude-opus-4.6",
            ["gpt-5.3-codex", "gpt-4o"],
            config,
        )
        assert result == ["gpt-5.3-codex", "gpt-4o"]

    def test_prefers_family_different_from_author(self):
        """A model sharing the author's family is deprioritised behind a different one."""
        config = _config(main=["claude-sonnet-4.6", "gpt-5.3-codex"])
        result = resolve_rubber_duck_models(
            "mainAgent",
            "claude-opus-4.6",
            ["claude-sonnet-4.6", "gpt-5.3-codex"],
            config,
        )
        assert result == ["gpt-5.3-codex", "claude-sonnet-4.6"]

    def test_author_model_none_returns_two_distinct(self):
        """A None author model still yields two distinct-family picks."""
        config = _config(main=["gpt-5.3-codex", "gemini-3.1-pro-preview"])
        result = resolve_rubber_duck_models(
            "mainAgent",
            None,
            ["gpt-5.3-codex", "gemini-3.1-pro-preview"],
            config,
        )
        assert result == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]

    def test_caps_at_two_even_with_three_valid_models(self):
        """At most two models are returned even when more are configured/valid."""
        models = ["gpt-5.3-codex", "gemini-3.1-pro-preview", "o4-mini"]
        config = _config(main=list(models))
        result = resolve_rubber_duck_models("mainAgent", "claude-opus-4.6", list(models), config)
        assert result == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]

    def test_rubber_duck_disabled_returns_agent_picks(self):
        """enabled=False short-circuits to AGENT_PICKS even when layers are populated."""
        config = _config(main=["gpt-5.3-codex", "gemini-3.1-pro-preview"], enabled=False)
        result = resolve_rubber_duck_models(
            "mainAgent",
            "claude-opus-4.6",
            ["gpt-5.3-codex", "gemini-3.1-pro-preview"],
            config,
        )
        assert result is AGENT_PICKS

    def test_rubber_duck_disabled_subagent_returns_agent_picks(self):
        """enabled=False short-circuits to AGENT_PICKS for the subagent layer too."""
        config = _config(sub=["gpt-5.3-codex"], enabled=False)
        result = resolve_rubber_duck_models(
            "subagent",
            "claude-opus-4.6",
            ["gpt-5.3-codex"],
            config,
        )
        assert result is AGENT_PICKS
