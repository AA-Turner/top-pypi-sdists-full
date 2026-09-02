"""Tests for _path_key."""

from agentic_devtools.cli.copilot import trust
from agentic_devtools.cli.copilot.trust import _normalize_path, _path_key


class TestPathKey:
    """Tests for _path_key."""

    def test_lowercases_on_windows(self, monkeypatch):
        """Lowercases the normalized path when os.name == 'nt'."""
        monkeypatch.setattr(trust.os, "name", "nt")
        path = "Some/Mixed/Case"
        assert _path_key(path) == _normalize_path(path).lower()

    def test_preserves_case_on_posix(self, monkeypatch):
        """Preserves case when os.name != 'nt'."""
        monkeypatch.setattr(trust.os, "name", "posix")
        path = "Some/Mixed/Case"
        assert _path_key(path) == _normalize_path(path)
