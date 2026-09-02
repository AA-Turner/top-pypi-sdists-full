"""Tests for _verify_trusted."""

import json

from agentic_devtools.cli.copilot.trust import _normalize_path, _verify_trusted


class TestVerifyTrusted:
    """Tests for _verify_trusted."""

    def test_missing_file_returns_false(self, tmp_path):
        """A missing config file fails verification."""
        assert _verify_trusted(tmp_path / "nope.json", str(tmp_path), subtree_trust=False) is False

    def test_malformed_returns_false(self, tmp_path):
        """Malformed JSON fails verification."""
        cfg = tmp_path / "config.json"
        cfg.write_text("{bad", encoding="utf-8")
        assert _verify_trusted(cfg, str(tmp_path), subtree_trust=False) is False

    def test_not_dict_returns_false(self, tmp_path):
        """A non-object JSON body fails verification."""
        cfg = tmp_path / "config.json"
        cfg.write_text("[1]", encoding="utf-8")
        assert _verify_trusted(cfg, str(tmp_path), subtree_trust=False) is False

    def test_folders_not_list_returns_false(self, tmp_path):
        """A non-list trustedFolders fails verification."""
        cfg = tmp_path / "config.json"
        cfg.write_text(json.dumps({"trustedFolders": "x"}), encoding="utf-8")
        assert _verify_trusted(cfg, str(tmp_path), subtree_trust=False) is False

    def test_empty_body_returns_false(self, tmp_path):
        """A whitespace-only body fails verification."""
        cfg = tmp_path / "config.json"
        cfg.write_text("   ", encoding="utf-8")
        assert _verify_trusted(cfg, str(tmp_path), subtree_trust=False) is False

    def test_present_returns_true(self, tmp_path):
        """A present entry passes verification."""
        cfg = tmp_path / "config.json"
        target = _normalize_path(str(tmp_path))
        cfg.write_text(json.dumps({"trustedFolders": [target]}), encoding="utf-8")
        assert _verify_trusted(cfg, str(tmp_path), subtree_trust=False) is True
