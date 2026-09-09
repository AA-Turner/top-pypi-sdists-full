"""Unit tests for _existing_files."""

from agentic_devtools.cli.checks.lint import _existing_files


def test__existing_files_filters_missing_paths_relative_to_cwd(tmp_path) -> None:
    (tmp_path / "present.py").touch()

    assert _existing_files(["present.py", "missing.py"], cwd=str(tmp_path)) == ["present.py"]
