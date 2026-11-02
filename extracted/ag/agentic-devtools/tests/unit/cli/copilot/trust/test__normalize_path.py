"""Tests for _normalize_path."""

import os

from agentic_devtools.cli.copilot.trust import _normalize_path


class TestNormalizePath:
    """Tests for _normalize_path."""

    def test_returns_absolute_normalized(self, tmp_path):
        """Returns an absolute, normalized path string."""
        raw = str(tmp_path / "sub" / ".." / "leaf")
        result = _normalize_path(raw)
        assert result == os.path.normpath(os.path.abspath(raw))
        assert os.path.isabs(result)
