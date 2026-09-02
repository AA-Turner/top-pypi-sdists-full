"""Tests for _find_existing_spec_dir in retro_spec/commands.py."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.retro_spec.commands import _find_existing_spec_dir


class TestFindExistingSpecDir:
    """Tests for recursive existing-spec discovery."""

    def test_returns_matching_nested_directory(self, tmp_path: Path) -> None:
        """Existing flat specs are found regardless of their current slug."""
        existing = tmp_path / "nested" / "42-old-name"
        existing.mkdir(parents=True)

        assert _find_existing_spec_dir(tmp_path, 42) == existing

    def test_supports_legacy_numeric_directory(self, tmp_path: Path) -> None:
        """Legacy specs/42 directories are also protected from overwrite."""
        existing = tmp_path / "42"
        existing.mkdir()

        assert _find_existing_spec_dir(tmp_path, 42) == existing
