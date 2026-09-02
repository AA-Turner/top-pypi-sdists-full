"""Tests for load_review_decision_policy()."""

from agentic_devtools.config import load_review_decision_policy


class TestLoadReviewDecisionPolicy:
    """Tests for loading review decision policy from config."""

    def test_returns_empty_dict_when_no_config(self, tmp_path) -> None:
        """Returns empty dict when no agdt-config.json exists."""
        result = load_review_decision_policy(str(tmp_path))
        assert result == {}

    def test_returns_empty_dict_when_no_review_section(self, tmp_path) -> None:
        """Returns empty dict when config has no review section."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"other": "stuff"}')

        result = load_review_decision_policy(str(tmp_path))
        assert result == {}

    def test_returns_empty_dict_when_no_decision_policy(self, tmp_path) -> None:
        """Returns empty dict when review section has no decision-policy."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"review": {"focus-areas-file": "test.md"}}')

        result = load_review_decision_policy(str(tmp_path))
        assert result == {}

    def test_returns_policy_dict(self, tmp_path) -> None:
        """Returns the decision-policy dict when configured with hyphen key."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"decision-policy": {"max-high-severity": 0, "max-medium-severity": null}}}'
        )

        result = load_review_decision_policy(str(tmp_path))
        assert result == {"max-high-severity": 0, "max-medium-severity": None}

    def test_returns_policy_dict_via_underscore_alias(self, tmp_path) -> None:
        """Returns the policy dict when configured with underscore alias key."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"review": {"decision_policy": {"max-high-severity": 1}}}')

        result = load_review_decision_policy(str(tmp_path))
        assert result == {"max-high-severity": 1}

    def test_hyphen_key_takes_precedence_over_underscore_alias(self, tmp_path) -> None:
        """Hyphen form takes precedence over underscore alias when both are present."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"decision-policy": {"max-high-severity": 0}, "decision_policy": {"max-high-severity": 99}}}'
        )

        result = load_review_decision_policy(str(tmp_path))
        assert result == {"max-high-severity": 0}

    def test_empty_hyphen_key_takes_precedence_and_returns_empty(self, tmp_path) -> None:
        """Empty decision-policy dict wins over underscore alias (key-presence beats falsiness)."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"decision-policy": {}, "decision_policy": {"max-high-severity": 99}}}'
        )

        result = load_review_decision_policy(str(tmp_path))
        assert result == {}

    def test_returns_empty_when_review_not_dict(self, tmp_path) -> None:
        """Returns empty dict when review section is not a dict."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"review": "invalid"}')

        result = load_review_decision_policy(str(tmp_path))
        assert result == {}
