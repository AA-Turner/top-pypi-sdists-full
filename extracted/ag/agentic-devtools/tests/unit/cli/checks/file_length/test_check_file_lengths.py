"""Tests for the repository Python file-length guard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import IO, Any
from unittest.mock import patch

from agentic_devtools.cli.checks.file_length import check_file_lengths


def _write_baseline(root: Path, file_lengths: dict[str, object]) -> None:
    (root / "quality-baseline.json").write_text(
        json.dumps({"schema_version": 1, "file_length": file_lengths, "complexity": {}}),
        encoding="utf-8",
    )


def _write_python_file(root: Path, relative_path: str, line_count: int) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n" * line_count, encoding="utf-8")
    return path


class TestCheckFileLengths:
    """Behavioral contract of check_file_lengths."""

    def test_counts_physical_lines_and_warns_above_200(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        _write_python_file(tmp_path, "agentic_devtools/sample.py", 201)
        _write_python_file(tmp_path, "tests/sample_test.py", 200)

        passed, output = check_file_lengths(tmp_path)

        assert passed is True
        assert "agentic_devtools/sample.py: 201 lines" in output
        assert "warning" in output.lower()
        assert "tests/sample_test.py" not in output

    def test_includes_root_level_python_files(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {"setup_script.py": 201})
        _write_python_file(tmp_path, "setup_script.py", 201)

        passed, output = check_file_lengths(tmp_path)

        assert passed is True
        assert "setup_script.py: 201 lines" in output

    def test_scans_agent_and_state_python_roots(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        _write_python_file(tmp_path, ".agents/maintained.py", 201)
        _write_python_file(tmp_path, ".agdt/maintained.py", 202)

        passed, output = check_file_lengths(tmp_path)

        assert passed is True
        assert ".agents/maintained.py: 201 lines" in output
        assert ".agdt/maintained.py: 202 lines" in output

    def test_ignores_gitignored_agent_runtime_python_directories(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        for directory in ("workflows", "cache"):
            _write_python_file(tmp_path, f".agdt/{directory}/generated.py", 501)

        passed, output = check_file_lengths(tmp_path)

        assert passed is True
        assert output == "OK — no Python files exceed the configured thresholds."

    def test_fails_when_a_baselined_file_grows(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {"agentic_devtools/sample.py": 201})
        _write_python_file(tmp_path, "agentic_devtools/sample.py", 202)

        passed, output = check_file_lengths(tmp_path)

        assert passed is False
        assert "exceeds its baseline of 201 lines" in output

    def test_fails_for_new_file_above_500_lines(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        _write_python_file(tmp_path, "tests/new_test.py", 501)

        passed, output = check_file_lengths(tmp_path)

        assert passed is False
        assert "501 lines exceeds the 500-line hard limit" in output
        assert "WARNING" not in output

    def test_does_not_warn_when_a_baselined_file_growth_fails(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {"tests/sample_test.py": 201})
        _write_python_file(tmp_path, "tests/sample_test.py", 202)

        passed, output = check_file_lengths(tmp_path)

        assert passed is False
        assert "exceeds its baseline of 201 lines" in output
        assert "WARNING" not in output

    def test_allows_unbaselined_file_at_hard_limit(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        _write_python_file(tmp_path, "tests/new_test.py", 500)

        passed, output = check_file_lengths(tmp_path)

        assert passed is True
        assert "500 lines" in output
        assert "warning" in output.lower()

    def test_does_not_count_unicode_line_separator_as_physical_line(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        path = tmp_path / "tests/new_test.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('value = "before\u2028after"\n' + "x\n" * 499, encoding="utf-8")

        passed, output = check_file_lengths(tmp_path)

        assert passed is True
        assert "500 lines" in output
        assert "501 lines" not in output

    def test_warns_when_baseline_entries_are_compliant_or_missing(self, tmp_path: Path) -> None:
        _write_baseline(
            tmp_path,
            {
                "agentic_devtools/compliant.py": 250,
                "tests/removed_test.py": 300,
            },
        )
        _write_python_file(tmp_path, "agentic_devtools/compliant.py", 200)

        passed, output = check_file_lengths(tmp_path)

        assert passed is True
        assert "agentic_devtools/compliant.py is now compliant" in output
        assert "tests/removed_test.py is missing" in output

    def test_fails_when_baseline_is_missing(self, tmp_path: Path) -> None:
        passed, output = check_file_lengths(tmp_path)

        assert passed is False
        assert "quality-baseline.json" in output

    def test_fails_when_baseline_cannot_be_read(self, tmp_path: Path) -> None:
        (tmp_path / "quality-baseline.json").write_text("{}", encoding="utf-8")
        original_read_text = Path.read_text

        def fail_for_baseline(self: Path, encoding: str | None = None, errors: str | None = None) -> str:
            if self.name == "quality-baseline.json":
                raise OSError("read denied")
            return original_read_text(self, encoding, errors)

        with patch.object(Path, "read_text", fail_for_baseline):
            passed, output = check_file_lengths(tmp_path)

        assert passed is False
        assert "Could not read quality-baseline.json" in output

    def test_fails_when_baseline_json_is_invalid(self, tmp_path: Path) -> None:
        (tmp_path / "quality-baseline.json").write_text("{", encoding="utf-8")

        passed, output = check_file_lengths(tmp_path)

        assert passed is False
        assert "Invalid quality baseline" in output

    def test_fails_when_baseline_schema_or_entry_is_invalid(self, tmp_path: Path) -> None:
        invalid_baselines: list[object] = [
            [],
            {"schema_version": 2, "file_length": {}, "complexity": {}},
            {"schema_version": True, "file_length": {}, "complexity": {}},
            {"schema_version": 1.0, "file_length": {}, "complexity": {}},
            {"schema_version": 1, "file_length": [], "complexity": {}},
            {"schema_version": 1, "file_length": {"tests/sample.py": "1"}, "complexity": {}},
            {"schema_version": 1, "file_length": {"tests/sample.py": True}, "complexity": {}},
            {"schema_version": 1, "file_length": {"tests/sample.py": -1}, "complexity": {}},
            {"schema_version": 1, "file_length": {}},
            {"schema_version": 1, "file_length": {}, "complexity": []},
        ]

        for baseline in invalid_baselines:
            (tmp_path / "quality-baseline.json").write_text(json.dumps(baseline), encoding="utf-8")
            passed, output = check_file_lengths(tmp_path)
            assert passed is False
            assert "Invalid quality baseline" in output

    def test_fails_when_source_file_cannot_be_read(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        path = _write_python_file(tmp_path, "tests/unreadable.py", 1)
        original_open = Path.open

        def fail_for_source_file(
            self: Path,
            mode: str = "r",
            buffering: int = -1,
            encoding: str | None = None,
            errors: str | None = None,
            newline: str | None = None,
        ) -> IO[Any]:
            if self == path:
                raise OSError("read denied")
            return original_open(self, mode, buffering, encoding, errors, newline)

        with patch.object(Path, "open", fail_for_source_file):
            passed, output = check_file_lengths(tmp_path)

        assert passed is False
        assert "Could not read tests/unreadable.py" in output

    def test_passes_when_source_roots_are_absent(self, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})

        passed, output = check_file_lengths(tmp_path)

        assert passed is True
        assert output == "OK — no Python files exceed the configured thresholds."
