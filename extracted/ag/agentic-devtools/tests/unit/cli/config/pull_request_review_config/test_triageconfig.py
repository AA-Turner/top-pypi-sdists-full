"""Tests for TriageConfig."""

from agentic_devtools.cli.config.pull_request_review_config import TriageConfig


class TestTriageConfig:
    """Tests for TriageConfig."""

    def test_defaults(self):
        """Defaults match plan §7 schema with §15.8 cost-budget fields."""
        config = TriageConfig()
        assert config.enabled is True
        assert config.defaultDepth == "deep"
        assert config.deepGlobs == ["**/auth/**", "**/*.sql", "**/migrations/**"]
        assert config.lightGlobs == ["**/*.md", "**/*.lock", "**/__snapshots__/**"]
        assert config.minDiffLinesForDeep == 20
        assert config.maxDeepModelCalls == 90
        assert config.maxDeepTotalChangedLines == 5000
        assert config.maxReviewMinutes == 60

    def test_default_lists_are_independent_instances(self):
        """Each instance gets its own glob lists (no shared mutable default)."""
        a = TriageConfig()
        b = TriageConfig()
        a.deepGlobs.append("extra")
        assert b.deepGlobs == ["**/auth/**", "**/*.sql", "**/migrations/**"]

    def test_to_dict_round_trips_through_from_dict(self):
        """from_dict(to_dict(default)) == default."""
        default = TriageConfig()
        assert TriageConfig.from_dict(default.to_dict()) == default

    def test_to_dict_shape(self):
        """to_dict emits all camelCase keys."""
        result = TriageConfig().to_dict()
        assert set(result) == {
            "enabled",
            "defaultDepth",
            "deepGlobs",
            "lightGlobs",
            "minDiffLinesForDeep",
            "maxDeepModelCalls",
            "maxDeepTotalChangedLines",
            "maxReviewMinutes",
        }

    def test_from_dict_full(self):
        """from_dict reads every provided field."""
        config = TriageConfig.from_dict(
            {
                "enabled": False,
                "defaultDepth": "light",
                "deepGlobs": ["**/*.py"],
                "lightGlobs": ["**/*.txt"],
                "minDiffLinesForDeep": 5,
                "maxDeepModelCalls": 10,
                "maxDeepTotalChangedLines": 100,
                "maxReviewMinutes": 15,
            }
        )
        assert config.enabled is False
        assert config.defaultDepth == "light"
        assert config.deepGlobs == ["**/*.py"]
        assert config.lightGlobs == ["**/*.txt"]
        assert config.minDiffLinesForDeep == 5
        assert config.maxDeepModelCalls == 10
        assert config.maxDeepTotalChangedLines == 100
        assert config.maxReviewMinutes == 15

    def test_from_dict_non_dict_returns_defaults(self):
        """Non-dict input yields a fully-defaulted config (tolerant)."""
        assert TriageConfig.from_dict(None) == TriageConfig()

    def test_from_dict_wrong_types_fall_back(self):
        """Wrong-typed scalar and list fields fall back to defaults."""
        config = TriageConfig.from_dict({"defaultDepth": 123, "minDiffLinesForDeep": "x", "deepGlobs": "nope"})
        assert config.defaultDepth == "deep"
        assert config.minDiffLinesForDeep == 20
        assert config.deepGlobs == ["**/auth/**", "**/*.sql", "**/migrations/**"]

    def test_from_dict_invalid_depth_string_falls_back_to_deep(self):
        """A valid string that is not 'deep' or 'light' falls back to 'deep'."""
        config = TriageConfig.from_dict({"defaultDepth": "invalid"})
        assert config.defaultDepth == "deep"
