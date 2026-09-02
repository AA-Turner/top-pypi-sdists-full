"""Tests for :func:`agentic_devtools.cli.setup.provider_connectivity._check_markdown_connectivity`."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.setup.provider_connectivity import _check_markdown_connectivity


class TestCheckMarkdownConnectivity:
    """Exercise markdown provider pre-flight checks."""

    def test_success_for_valid_directory(self, tmp_path: Path) -> None:
        """Markdown provider validates only that the repo directory is usable."""
        assert _check_markdown_connectivity(tmp_path, timeout=5.0) == (True, None)

    def test_fails_for_missing_path(self, tmp_path: Path) -> None:
        """Markdown reject missing workspace roots before any network calls are attempted."""
        missing = tmp_path / "does-not-exist"

        is_connected, error = _check_markdown_connectivity(missing, timeout=5.0)

        assert is_connected is False
        assert "does not exist" in (error or "")

    def test_fails_for_invalid_directory(self, tmp_path: Path) -> None:
        """Markdown check rejects file paths as non-directory workspace roots without network calls."""
        file_path = tmp_path / "not_a_directory.txt"
        file_path.write_text("this is a file", encoding="utf-8")

        is_connected, error = _check_markdown_connectivity(file_path, timeout=5.0)

        assert is_connected is False
        assert "not a directory" in (error or "")

    def test_fails_for_unreadable_directory(self, tmp_path: Path) -> None:
        """Permission errors during directory reads are surfaced gracefully."""
        with patch.object(Path, "iterdir", side_effect=PermissionError("permission denied")):
            is_connected, error = _check_markdown_connectivity(tmp_path, timeout=5.0)

        assert is_connected is False
        assert "permission denied" in (error or "")
