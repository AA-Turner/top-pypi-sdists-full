"""Tests for remove_trusted_folder."""

import json

from agentic_devtools.cli.copilot.trust import is_trusted_folder, remove_trusted_folder


class TestRemoveTrustedFolder:
    """Tests for remove_trusted_folder."""

    def test_removes_trusted_folder_and_preserves_jsonc_header(self, tmp_path, monkeypatch):
        """Remove an exact trusted-folder entry without dropping the JSONC header."""
        config_path = tmp_path / "config.json"
        target = tmp_path / "target"
        other = tmp_path / "other"
        config_path.write_text(
            "// Copilot configuration\n" + json.dumps({"trustedFolders": [str(target), str(other)]}),
            encoding="utf-8",
        )
        monkeypatch.setattr("agentic_devtools.cli.copilot.trust.get_copilot_config_path", lambda: config_path)

        assert remove_trusted_folder(str(target)) is True
        assert is_trusted_folder(str(target)) is False
        assert is_trusted_folder(str(other)) is True
        assert config_path.read_text(encoding="utf-8").startswith("// Copilot configuration\n")

    def test_remove_returns_false_when_folder_is_not_present(self, tmp_path, monkeypatch):
        """Do not rewrite configuration when the exact folder is absent."""
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"trustedFolders": []}), encoding="utf-8")
        monkeypatch.setattr("agentic_devtools.cli.copilot.trust.get_copilot_config_path", lambda: config_path)

        assert remove_trusted_folder(str(tmp_path / "missing")) is False

    def test_remove_returns_false_for_invalid_configuration(self, tmp_path, monkeypatch):
        """Return false when the configuration cannot be parsed or has no folder list."""
        config_path = tmp_path / "config.json"
        monkeypatch.setattr("agentic_devtools.cli.copilot.trust.get_copilot_config_path", lambda: config_path)

        config_path.write_text("not json", encoding="utf-8")
        assert remove_trusted_folder(str(tmp_path / "target")) is False

        config_path.write_text("[]", encoding="utf-8")
        assert remove_trusted_folder(str(tmp_path / "target")) is False

        config_path.write_text(json.dumps({"trustedFolders": "invalid"}), encoding="utf-8")
        assert remove_trusted_folder(str(tmp_path / "target")) is False
