"""Tests for _ensure_trusted_folder."""

import json

from agentic_devtools.cli.copilot.trust import (
    TrustMutationResult,
    _ensure_trusted_folder,
    _normalize_path,
    _split_jsonc_header,
)


def _read_folders(cfg):
    _, body = _split_jsonc_header(cfg.read_text(encoding="utf-8"))
    return json.loads(body)["trustedFolders"]


class TestEnsureTrustedFolderPrivate:
    """Tests for _ensure_trusted_folder."""

    def test_returns_added_true_when_entry_is_created(self, monkeypatch, tmp_path):
        """Reports ownership when the locked mutation creates a new trust entry."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        target = tmp_path / "ws"

        result = _ensure_trusted_folder(str(target))

        assert result == TrustMutationResult(True, True)
        assert _normalize_path(str(target)) in _read_folders(tmp_path / "config.json")

    def test_returns_added_false_when_entry_already_exists(self, monkeypatch, tmp_path):
        """Does not claim ownership when the locked mutation finds an existing entry."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        cfg = tmp_path / "config.json"
        target = _normalize_path(str(tmp_path / "ws"))
        cfg.write_text(json.dumps({"trustedFolders": [target]}), encoding="utf-8")

        result = _ensure_trusted_folder(str(tmp_path / "ws"))

        assert result == TrustMutationResult(True, False)
        assert _read_folders(cfg) == [target]
