"""Tests for ensure_trusted_folder."""

import json
from unittest.mock import MagicMock

from agentic_devtools.cli.copilot import trust
from agentic_devtools.cli.copilot.trust import _normalize_path, _split_jsonc_header, ensure_trusted_folder
from agentic_devtools.file_locking import FileLockError


def _read_folders(cfg):
    _, body = _split_jsonc_header(cfg.read_text(encoding="utf-8"))
    return json.loads(body)["trustedFolders"]


class TestEnsureTrustedFolder:
    """Tests for ensure_trusted_folder."""

    def test_creates_and_adds_when_missing(self, monkeypatch, tmp_path):
        """Creates config.json and adds the target when absent."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        target = tmp_path / "ws"
        assert ensure_trusted_folder(str(target)) is True
        assert _normalize_path(str(target)) in _read_folders(tmp_path / "config.json")

    def test_idempotent_no_duplicate(self, monkeypatch, tmp_path):
        """A second call does not add a duplicate entry."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        target = str(tmp_path / "ws")
        assert ensure_trusted_folder(target) is True
        assert ensure_trusted_folder(target) is True
        assert _read_folders(tmp_path / "config.json").count(_normalize_path(target)) == 1

    def test_no_write_when_already_trusted(self, monkeypatch, tmp_path):
        """When the target is already trusted the config file is not rewritten."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        cfg = tmp_path / "config.json"
        target = _normalize_path(str(tmp_path / "ws"))
        cfg.write_text(json.dumps({"trustedFolders": [target]}), encoding="utf-8")
        mtime_before = cfg.stat().st_mtime_ns
        assert ensure_trusted_folder(str(tmp_path / "ws")) is True
        assert cfg.stat().st_mtime_ns == mtime_before, "config.json must not be rewritten when already trusted"

    def test_preserves_header_and_other_keys(self, monkeypatch, tmp_path):
        """The JSONC header and unrelated keys are preserved."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        cfg = tmp_path / "config.json"
        cfg.write_text('// hdr\n{\n  "loggedInUsers": [1]\n}\n', encoding="utf-8")
        assert ensure_trusted_folder(str(tmp_path / "ws")) is True
        raw = cfg.read_text(encoding="utf-8")
        assert raw.startswith("// hdr\n")
        body = json.loads(raw[raw.index("{") :])
        assert body["loggedInUsers"] == [1]
        assert body["trustedFolders"]

    def test_body_not_dict_returns_false(self, monkeypatch, tmp_path):
        """A non-object JSON body is rejected."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        (tmp_path / "config.json").write_text("[1, 2]", encoding="utf-8")
        assert ensure_trusted_folder(str(tmp_path / "ws")) is False

    def test_malformed_json_returns_false(self, monkeypatch, tmp_path):
        """Malformed JSON degrades to False."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        (tmp_path / "config.json").write_text("{not json", encoding="utf-8")
        assert ensure_trusted_folder(str(tmp_path / "ws")) is False

    def test_lock_error_returns_false(self, monkeypatch, tmp_path):
        """A FileLockError degrades to False."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        monkeypatch.setattr(trust, "locked_file", MagicMock(side_effect=FileLockError("locked")))
        assert ensure_trusted_folder(str(tmp_path / "ws")) is False

    def test_os_error_returns_false(self, monkeypatch, tmp_path):
        """An OSError degrades to False."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        monkeypatch.setattr(trust, "locked_file", MagicMock(side_effect=OSError("io")))
        assert ensure_trusted_folder(str(tmp_path / "ws")) is False

    def test_subtree_skips_append_when_ancestor_present(self, monkeypatch, tmp_path):
        """With subtree_trust, a covered child is not appended but verifies True."""
        monkeypatch.setenv("COPILOT_HOME", str(tmp_path))
        cfg = tmp_path / "config.json"
        parent = _normalize_path(str(tmp_path))
        cfg.write_text(json.dumps({"trustedFolders": [parent]}), encoding="utf-8")
        assert ensure_trusted_folder(str(tmp_path / "ws"), subtree_trust=True) is True
        assert _read_folders(cfg) == [parent]
