"""Tests for the filtered Python-file iterator."""

import os
from pathlib import Path

from agentic_devtools.cli.checks.file_length import _iter_source_python_files


def test_prunes_gitignored_agent_state_runtime_directories(tmp_path: Path, monkeypatch) -> None:
    source_root = tmp_path / ".agdt"
    expected = source_root / "maintained.py"
    uppercase_extension = source_root / "uppercase.PY"
    dotfile = source_root / ".py"
    nested = source_root / "skills" / "tracked.py"
    ignored = (
        source_root / "workflows" / "generated.py",
        source_root / "cache" / "generated.py",
    )
    directory_with_python_suffix = source_root / "package.py"
    non_python = source_root / "notes.txt"
    for path in (expected, uppercase_extension, dotfile, nested, *ignored, non_python):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    directory_with_python_suffix.mkdir()

    original_walk = os.walk
    visited: list[Path] = []

    def track_walk(directory):
        for current, directory_names, file_names in original_walk(directory):
            visited.append(Path(current))
            yield current, directory_names, file_names

    monkeypatch.setattr(os, "walk", track_walk)
    files = list(_iter_source_python_files(tmp_path, source_root))

    rglob_matches = set(source_root.rglob("*.py"))
    expected_files = [
        (path.relative_to(tmp_path).as_posix(), path)
        for path in (expected, uppercase_extension, dotfile, directory_with_python_suffix, nested)
        if path in rglob_matches and path.is_file()
    ]

    assert sorted(files) == sorted(expected_files)
    assert source_root in visited
    assert source_root / "skills" in visited
    assert source_root / "workflows" not in visited
    assert source_root / "cache" not in visited
