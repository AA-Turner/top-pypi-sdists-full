"""Tests for ``normalize_path``."""

from __future__ import annotations

from agentic_devtools.cli.checks.customization_quality import normalize_path


class TestNormalizePath:
    def test_leaves_a_posix_path_untouched(self) -> None:
        """A repository-relative POSIX path is returned unchanged."""
        assert normalize_path(".github/instructions/a.md") == ".github/instructions/a.md"

    def test_converts_windows_separators(self) -> None:
        """Backslash separators become forward slashes."""
        assert normalize_path(".github\\instructions\\a.md") == ".github/instructions/a.md"

    def test_strips_repeated_dot_slash_prefixes(self) -> None:
        """Every leading ``./`` prefix is removed."""
        assert normalize_path("././docs/agent-customization/a.md") == "docs/agent-customization/a.md"
