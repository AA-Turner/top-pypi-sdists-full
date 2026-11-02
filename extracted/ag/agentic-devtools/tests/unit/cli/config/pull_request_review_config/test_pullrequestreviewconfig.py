"""Tests for PullRequestReviewConfig."""

from agentic_devtools.cli.config.pull_request_review_config import (
    PullRequestReviewConfig,
    RubberDuckConfig,
    TriageConfig,
)


class TestPullRequestReviewConfig:
    """Tests for PullRequestReviewConfig."""

    def test_defaults(self):
        """Defaults nest the rubber-duck/triage blocks and scalar policy."""
        config = PullRequestReviewConfig()
        assert config.rubberDuck == RubberDuckConfig()
        assert config.triage == TriageConfig()
        assert config.subagentTimeoutSeconds == 600
        assert config.subagentMaxRetries == 2

    def test_default_nested_configs_are_independent_instances(self):
        """Each instance gets its own nested config (no shared mutable default)."""
        a = PullRequestReviewConfig()
        b = PullRequestReviewConfig()
        a.rubberDuck.mainAgent.append("extra")
        assert b.rubberDuck.mainAgent == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]

    def test_to_dict_is_nested(self):
        """to_dict nests rubberDuck and triage dicts."""
        result = PullRequestReviewConfig().to_dict()
        assert isinstance(result["rubberDuck"], dict)
        assert isinstance(result["triage"], dict)
        assert result["subagentTimeoutSeconds"] == 600
        assert result["subagentMaxRetries"] == 2

    def test_to_dict_round_trips_through_from_dict(self):
        """from_dict(to_dict(default)) == default (the key acceptance criterion)."""
        default = PullRequestReviewConfig()
        assert PullRequestReviewConfig.from_dict(default.to_dict()) == default

    def test_from_dict_full(self):
        """from_dict reconstructs nested blocks and scalars."""
        config = PullRequestReviewConfig.from_dict(
            {
                "rubberDuck": {"enabled": False, "mainAgent": ["x"], "subagent": ["y"]},
                "triage": {"defaultDepth": "light"},
                "subagentTimeoutSeconds": 120,
                "subagentMaxRetries": 5,
            }
        )
        assert config.rubberDuck.enabled is False
        assert config.rubberDuck.mainAgent == ["x"]
        assert config.triage.defaultDepth == "light"
        assert config.subagentTimeoutSeconds == 120
        assert config.subagentMaxRetries == 5

    def test_from_dict_non_dict_returns_defaults(self):
        """Non-dict input yields a fully-defaulted config (tolerant)."""
        assert PullRequestReviewConfig.from_dict(42) == PullRequestReviewConfig()

    def test_from_dict_missing_nested_blocks_use_defaults(self):
        """Absent rubberDuck/triage blocks fall back to nested defaults."""
        config = PullRequestReviewConfig.from_dict({"subagentMaxRetries": 7})
        assert config.rubberDuck == RubberDuckConfig()
        assert config.triage == TriageConfig()
        assert config.subagentMaxRetries == 7

    def test_from_dict_wrong_typed_scalars_fall_back(self):
        """Non-int timeout/retry values fall back to defaults."""
        config = PullRequestReviewConfig.from_dict({"subagentTimeoutSeconds": "x", "subagentMaxRetries": None})
        assert config.subagentTimeoutSeconds == 600
        assert config.subagentMaxRetries == 2

    def test_from_dict_bool_scalars_fall_back(self):
        """Bool timeout/retry values fall back to int defaults."""
        config = PullRequestReviewConfig.from_dict({"subagentTimeoutSeconds": True, "subagentMaxRetries": False})
        assert config.subagentTimeoutSeconds == 600
        assert config.subagentMaxRetries == 2
