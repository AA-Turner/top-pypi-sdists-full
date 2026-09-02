"""Tests for RubberDuckConfig."""

from agentic_devtools.cli.config.pull_request_review_config import RubberDuckConfig


class TestRubberDuckConfig:
    """Tests for RubberDuckConfig."""

    def test_defaults(self):
        """Defaults match plan §7 (enabled + two-model layers)."""
        config = RubberDuckConfig()
        assert config.enabled is True
        assert config.mainAgent == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]
        assert config.subagent == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]

    def test_default_lists_are_independent_instances(self):
        """Each instance gets its own list (no shared mutable default)."""
        a = RubberDuckConfig()
        b = RubberDuckConfig()
        a.mainAgent.append("extra")
        assert b.mainAgent == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]

    def test_to_dict_round_trips_through_from_dict(self):
        """from_dict(to_dict(default)) == default."""
        default = RubberDuckConfig()
        assert RubberDuckConfig.from_dict(default.to_dict()) == default

    def test_to_dict_shape(self):
        """to_dict emits camelCase keys with copied lists."""
        config = RubberDuckConfig(enabled=False, mainAgent=["a"], subagent=["b"])
        result = config.to_dict()
        assert result == {"enabled": False, "mainAgent": ["a"], "subagent": ["b"]}

    def test_from_dict_full(self):
        """from_dict reads all provided fields."""
        config = RubberDuckConfig.from_dict({"enabled": False, "mainAgent": ["x"], "subagent": ["y", "z"]})
        assert config.enabled is False
        assert config.mainAgent == ["x"]
        assert config.subagent == ["y", "z"]

    def test_from_dict_non_dict_returns_defaults(self):
        """Non-dict input yields a fully-defaulted config (tolerant)."""
        assert RubberDuckConfig.from_dict("not-a-dict") == RubberDuckConfig()

    def test_from_dict_wrong_typed_enabled_falls_back(self):
        """A non-bool 'enabled' falls back to the default True."""
        config = RubberDuckConfig.from_dict({"enabled": "yes"})
        assert config.enabled is True

    def test_from_dict_wrong_typed_lists_fall_back(self):
        """Non-list model layers fall back to defaults."""
        config = RubberDuckConfig.from_dict({"mainAgent": "nope", "subagent": 5})
        assert config.mainAgent == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]
        assert config.subagent == ["gpt-5.3-codex", "gemini-3.1-pro-preview"]
