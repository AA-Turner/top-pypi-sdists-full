"""Tests for write_spec_file in retro_spec/synthesis.py."""

from __future__ import annotations

from pathlib import Path

from agentic_devtools.cli.speckit.retro_spec.synthesis import write_spec_file


class TestWriteSpecFile:
    """Tests for the write_spec_file function."""

    def test_creates_spec_with_retroactive_header(self, tmp_path: Path) -> None:
        """Test that spec.md includes the retroactive metadata header."""
        target = tmp_path / "142"
        write_spec_file("## Summary\n\nThis is the spec.", target)

        spec_file = target / "spec.md"
        assert spec_file.exists()
        content = spec_file.read_text(encoding="utf-8")
        assert "**Generated**: retroactive" in content
        assert "Retroactive Spec" in content
        assert "## Summary" in content

    def test_creates_directory_if_missing(self, tmp_path: Path) -> None:
        """Test that the target directory is created."""
        target = tmp_path / "deep" / "nested" / "path"
        write_spec_file("content", target)
        assert (target / "spec.md").exists()

    def test_retroactive_banner_present(self, tmp_path: Path) -> None:
        """Test that the visible banner is in the document body."""
        target = tmp_path / "test"
        write_spec_file("content", target)
        content = (target / "spec.md").read_text(encoding="utf-8")
        assert "forward-looking design document" in content
