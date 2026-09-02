"""Tests for the ``_read_text()`` helper."""

from pathlib import Path

from agentic_devtools.cli.speckit.verify_artifacts import _read_text


class TestReadText:
    """Reading artifact files defensively."""

    def test_returns_file_content(self, tmp_path: Path) -> None:
        path = tmp_path / "spec.md"
        path.write_text("# Spec\n", encoding="utf-8")

        assert _read_text(path) == "# Spec\n"

    def test_returns_none_for_missing_file(self, tmp_path: Path) -> None:
        assert _read_text(tmp_path / "absent.md") is None

    def test_returns_none_for_directory(self, tmp_path: Path) -> None:
        directory = tmp_path / "checklists"
        directory.mkdir()

        assert _read_text(directory) is None

    def test_returns_none_for_undecodable_bytes(self, tmp_path: Path) -> None:
        path = tmp_path / "plan.md"
        path.write_bytes(b"\xff\xfe\x00binary")

        assert _read_text(path) is None
