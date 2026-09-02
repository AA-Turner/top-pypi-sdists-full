"""Tests for ``path_reference_exists()``."""

from pathlib import Path

from agentic_devtools.cli.speckit.verify_artifacts import path_reference_exists


class TestPathReferenceExists:
    """Resolving a referenced path against the repository."""

    def test_resolves_path_relative_to_repo_root(self, tmp_path: Path) -> None:
        (tmp_path / "pkg").mkdir()
        (tmp_path / "pkg" / "mod.py").write_text("", encoding="utf-8")

        assert path_reference_exists("pkg/mod.py", tmp_path, ()) is True

    def test_resolves_shorthand_via_tracked_suffix(self, tmp_path: Path) -> None:
        tracked = ("agentic_devtools/cli/runner.py",)

        assert path_reference_exists("cli/runner.py", tmp_path, tracked) is True

    def test_resolves_dotfile_whose_leading_dot_was_dropped(self, tmp_path: Path) -> None:
        (tmp_path / ".github").mkdir()
        (tmp_path / ".github" / "agdt-config.json").write_text("{}", encoding="utf-8")

        assert path_reference_exists("github/agdt-config.json", tmp_path, ()) is True

    def test_resolves_dropped_dot_via_tracked_suffix(self, tmp_path: Path) -> None:
        tracked = ("nested/.github/workflows/ci.yml",)

        assert path_reference_exists("github/workflows/ci.yml", tmp_path, tracked) is True

    def test_returns_false_for_unknown_path(self, tmp_path: Path) -> None:
        assert path_reference_exists("pkg/absent.py", tmp_path, ("other/file.py",)) is False

    def test_suffix_match_requires_a_path_separator(self, tmp_path: Path) -> None:
        tracked = ("agentic_devtools/cli/xrunner.py",)

        assert path_reference_exists("runner.py", tmp_path, tracked) is False

    def test_resolves_directory_reference(self, tmp_path: Path) -> None:
        (tmp_path / "docs").mkdir()

        assert path_reference_exists("docs", tmp_path, ()) is True

    def test_rejects_ambiguous_suffix_match(self, tmp_path: Path) -> None:
        tracked = (
            "agentic_devtools/cli/runner.py",
            "tests/unit/cli/runner.py",
        )

        assert path_reference_exists("cli/runner.py", tmp_path, tracked) is False
