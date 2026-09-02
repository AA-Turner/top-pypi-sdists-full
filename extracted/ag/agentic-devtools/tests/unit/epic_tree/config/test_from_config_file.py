"""Tests for EpicTreeConfig.from_config_file classmethod."""

from pathlib import Path

from agentic_devtools.epic_tree.config import EpicTreeConfig


class TestFromConfigFile:
    """Tests for the from_config_file factory classmethod."""

    def test_missing_file_returns_defaults(self, tmp_path: Path):
        """When config file is missing, returns default config."""
        config = EpicTreeConfig.from_config_file(tmp_path)
        assert config.max_depth == 3
        assert config.default_issue_types == {0: "Epic", 1: "Feature", 2: "Subtask"}
        assert config.default_labels == {0: ["epic"], 1: ["feature"], 2: ["subtask"]}

    def test_missing_epic_tree_key_returns_defaults(self, tmp_path: Path):
        """When epicTree key is absent in config, returns defaults."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"other": "value"}')
        config = EpicTreeConfig.from_config_file(tmp_path)
        assert config.max_depth == 3

    def test_valid_overrides_parsed(self, tmp_path: Path):
        """Valid epicTree overrides are parsed correctly."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"epicTree": {"maxDepth": 2, "defaultIssueTypes": {"0": "Initiative", "1": "Story"}}}'
        )
        config = EpicTreeConfig.from_config_file(tmp_path)
        assert config.max_depth == 2
        assert config.default_issue_types == {0: "Initiative", 1: "Story"}

    def test_max_depth_exceeds_3_raises(self, tmp_path: Path):
        """maxDepth > 3 raises ConfigError."""
        import pytest

        from agentic_devtools.epic_tree.errors import ConfigError

        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"epicTree": {"maxDepth": 5}}')
        with pytest.raises(ConfigError):
            EpicTreeConfig.from_config_file(tmp_path)
