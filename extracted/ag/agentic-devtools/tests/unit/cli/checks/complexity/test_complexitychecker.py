"""Tests for the Ruff complexity baseline guard."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.complexity import ComplexityChecker

MODULE = "agentic_devtools.cli.checks.complexity"


def _write_baseline(root: Path, complexity: dict[str, str]) -> None:
    (root / "quality-baseline.json").write_text(
        json.dumps({"schema_version": 1, "file_length": {}, "complexity": complexity}),
        encoding="utf-8",
    )


def _write_source(root: Path) -> Path:
    path = root / "agentic_devtools" / "example.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("def complicated():\n    return 1\n", encoding="utf-8")
    return path


def _write_raw_baseline(root: Path, content: str) -> None:
    (root / "quality-baseline.json").write_text(content, encoding="utf-8")


def _finding(path: Path, *, code: str = "C901", row: int = 1) -> dict[str, object]:
    message = {
        "C901": "`complicated` is too complex (11 > 10)",
        "PLR0912": "Too many branches (13 > 12)",
        "PLR0915": "Too many statements (51 > 50)",
    }[code]
    return {
        "code": code,
        "filename": str(path),
        "location": {"row": row, "column": 1},
        "message": message,
    }


class TestComplexityChecker:
    """Behavioral contract of ComplexityChecker."""

    @patch(f"{MODULE}.subprocess.run")
    def test_fails_for_untracked_finding(self, mock_run, tmp_path: Path) -> None:
        source = _write_source(tmp_path)
        _write_baseline(tmp_path, {})
        mock_run.return_value = CompletedProcess(
            args=[], returncode=1, stdout=json.dumps([_finding(source)]), stderr=""
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "New complexity violation" in output
        assert "agentic_devtools/example.py::C901::complicated" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_allows_individually_tracked_findings(self, mock_run, tmp_path: Path) -> None:
        source = _write_source(tmp_path)
        identifier = "agentic_devtools/example.py::C901::complicated"
        _write_baseline(tmp_path, {identifier: "`complicated` is too complex (11 > 10)"})
        mock_run.return_value = CompletedProcess(
            args=[], returncode=1, stdout=json.dumps([_finding(source)]), stderr=""
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is True
        assert "New complexity violation" not in output

    @pytest.mark.parametrize(
        ("code", "baseline_message", "current_message"),
        [
            ("C901", "`complicated` is too complex (15 > 10)", "`complicated` is too complex (12 > 10)"),
            ("PLR0912", "Too many branches (20 > 12)", "Too many branches (14 > 12)"),
            ("PLR0915", "Too many statements (60 > 50)", "Too many statements (55 > 50)"),
        ],
    )
    @patch(f"{MODULE}.subprocess.run")
    def test_allows_partially_improved_tracked_findings_without_baseline_edits(
        self, mock_run, code: str, baseline_message: str, current_message: str, tmp_path: Path
    ) -> None:
        source = _write_source(tmp_path)
        identifier = f"agentic_devtools/example.py::{code}::complicated"
        baseline = tmp_path / "quality-baseline.json"
        _write_baseline(tmp_path, {identifier: baseline_message})
        original_baseline = baseline.read_text(encoding="utf-8")
        finding = _finding(source, code=code)
        finding["message"] = current_message
        mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout=json.dumps([finding]), stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is True
        assert output == "OK — no unbaselined complexity violations."
        assert baseline.read_text(encoding="utf-8") == original_baseline

    @pytest.mark.parametrize(
        ("code", "baseline_message", "current_message"),
        [
            ("C901", "`complicated` is too complex (12 > 10)", "`complicated` is too complex (15 > 10)"),
            ("PLR0912", "Too many branches (14 > 12)", "Too many branches (20 > 12)"),
            ("PLR0915", "Too many statements (55 > 50)", "Too many statements (60 > 50)"),
        ],
    )
    @patch(f"{MODULE}.subprocess.run")
    def test_fails_when_tracked_complexity_metric_grows(
        self, mock_run, code: str, baseline_message: str, current_message: str, tmp_path: Path
    ) -> None:
        source = _write_source(tmp_path)
        identifier = f"agentic_devtools/example.py::{code}::complicated"
        _write_baseline(tmp_path, {identifier: baseline_message})
        finding = _finding(source, code=code)
        finding["message"] = current_message
        mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout=json.dumps([finding]), stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert f"Tracked complexity violation grew for {identifier}" in output

    @pytest.mark.parametrize(
        ("baseline_message", "current_message"),
        [
            ("not a complexity diagnostic", "`complicated` is too complex (11 > 10)"),
            ("`complicated` is too complex (10 > 10)", "`complicated` is too complex (11 > 10)"),
            ("`complicated` is too complex (11 > 9)", "`complicated` is too complex (11 > 10)"),
            ("`complicated` is too complex (11 > 10)", "unrecognized diagnostic"),
        ],
    )
    @patch(f"{MODULE}.subprocess.run")
    def test_reports_malformed_complexity_metric_data(
        self, mock_run, baseline_message: str, current_message: str, tmp_path: Path
    ) -> None:
        source = _write_source(tmp_path)
        identifier = "agentic_devtools/example.py::C901::complicated"
        _write_baseline(tmp_path, {identifier: baseline_message})
        finding = _finding(source)
        finding["message"] = current_message
        mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout=json.dumps([finding]), stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "complexity metric" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_warns_and_retains_stale_baseline_entries(self, mock_run, tmp_path: Path) -> None:
        _write_source(tmp_path)
        stale = "agentic_devtools/example.py::C901::removed"
        _write_baseline(tmp_path, {stale: "previous violation"})
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="[]", stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is True
        assert f"Baseline complexity entry {stale} is no longer present" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_passes_when_ruff_has_no_findings(self, mock_run, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="", stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is True
        assert output == "OK — no unbaselined complexity violations."

    @pytest.mark.parametrize(
        ("returncode", "stdout", "stderr", "expected"),
        [
            (2, "", "configuration error", "exited with code 2: configuration error"),
            (1, "", "", "failed without JSON diagnostics"),
            (1, "[]", "", "failed without diagnostics"),
        ],
    )
    @patch(f"{MODULE}.subprocess.run")
    def test_reports_ruff_failures_without_findings(
        self, mock_run, returncode: int, stdout: str, stderr: str, expected: str, tmp_path: Path
    ) -> None:
        _write_baseline(tmp_path, {})
        mock_run.return_value = CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr=stderr)

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert expected in output

    @patch(f"{MODULE}.subprocess.run")
    def test_reports_tool_execution_failure(self, mock_run, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        mock_run.side_effect = OSError("ruff unavailable")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "Could not run Ruff complexity check" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_reports_invalid_ruff_output(self, mock_run, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="not json", stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "Invalid Ruff complexity output" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_reports_non_array_ruff_output(self, mock_run, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        mock_run.return_value = CompletedProcess(args=[], returncode=0, stdout="{}", stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "expected a JSON array" in output

    @pytest.mark.parametrize(
        ("content", "expected"),
        [
            ("[]", "expected an object"),
            ('{"schema_version":1,"file_length":[],"complexity":{}}', "file_length must be an object"),
            ('{"schema_version":1,"file_length":{},"complexity":[]}', "complexity must be an object"),
            (
                '{"schema_version":1,"file_length":{},"complexity":{"key":1}}',
                "Invalid quality baseline complexity entry",
            ),
            (
                '{"schema_version":1,"file_length":{},"complexity":{"":"message"}}',
                "Invalid quality baseline complexity entry",
            ),
            (
                '{"schema_version":1,"file_length":{},"complexity":{"key":""}}',
                "Invalid quality baseline complexity entry",
            ),
        ],
    )
    def test_reports_invalid_baseline_contents(self, content: str, expected: str, tmp_path: Path) -> None:
        _write_raw_baseline(tmp_path, content)

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert expected in output

    def test_reports_missing_baseline(self, tmp_path: Path) -> None:
        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "quality-baseline.json is missing" in output

    @pytest.mark.parametrize("error", [OSError("read denied"), UnicodeError("invalid encoding")])
    def test_reports_baseline_read_errors(self, error: Exception, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        original_read_text = Path.read_text

        def fail_for_baseline(self: Path, encoding: str | None = None, errors: str | None = None) -> str:
            if self.name == "quality-baseline.json":
                raise error
            return original_read_text(self, encoding=encoding, errors=errors)

        with patch.object(Path, "read_text", fail_for_baseline):
            passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "Could not read quality-baseline.json" in output

    def test_reports_invalid_baseline_json(self, tmp_path: Path) -> None:
        _write_raw_baseline(tmp_path, "{")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "Invalid quality baseline JSON" in output

    @pytest.mark.parametrize("version", [True, "1", 2])
    def test_reports_invalid_baseline_schema_version(self, version: object, tmp_path: Path) -> None:
        (tmp_path / "quality-baseline.json").write_text(
            json.dumps({"schema_version": version, "file_length": {}, "complexity": {}}),
            encoding="utf-8",
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "Invalid quality baseline schema_version" in output

    @pytest.mark.parametrize(
        ("row", "expected"),
        [
            (True, "positive integer"),
            (0, "positive integer"),
            ("1", "positive integer"),
            (20, "no function encloses"),
        ],
    )
    @patch(f"{MODULE}.subprocess.run")
    def test_reports_findings_without_valid_function_locations(
        self, mock_run, row: object, expected: str, tmp_path: Path
    ) -> None:
        source = _write_source(tmp_path)
        _write_baseline(tmp_path, {})
        finding = _finding(source)
        finding["location"] = {"row": row, "column": 1}
        mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout=json.dumps([finding]), stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert expected in output

    @pytest.mark.parametrize(
        "finding",
        [
            None,
            {"code": "E501", "filename": "source.py", "location": {"row": 1}, "message": "invalid code"},
            {"code": "C901", "filename": None, "location": {"row": 1}, "message": "invalid filename"},
            {"code": "C901", "filename": "source.py", "location": {"row": 1}, "message": None},
            {"code": "C901", "filename": "source.py", "location": [], "message": "invalid location"},
        ],
    )
    @patch(f"{MODULE}.subprocess.run")
    def test_reports_malformed_findings(self, mock_run, finding: object, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout=json.dumps([finding]), stderr="")

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "Could not identify Ruff complexity finding" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_reports_findings_outside_repository(self, mock_run, tmp_path: Path) -> None:
        _write_baseline(tmp_path, {})
        outside_path = tmp_path.parent / "outside.py"
        mock_run.return_value = CompletedProcess(
            args=[], returncode=1, stdout=json.dumps([_finding(outside_path)]), stderr=""
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "finding path is outside the repository" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_tracks_each_rule_and_reuses_cached_function_names(self, mock_run, tmp_path: Path) -> None:
        source = _write_source(tmp_path)
        relative_source = source.relative_to(tmp_path).as_posix()
        _write_baseline(
            tmp_path,
            {
                "agentic_devtools/example.py::C901::complicated": "`complicated` is too complex (11 > 10)",
                "agentic_devtools/example.py::PLR0912::complicated": "Too many branches (13 > 12)",
            },
        )
        mock_run.return_value = CompletedProcess(
            args=[],
            returncode=1,
            stdout=json.dumps(
                [
                    _finding(source),
                    {**_finding(source, code="PLR0912"), "filename": relative_source},
                ]
            ),
            stderr="",
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is True
        assert "no unbaselined complexity violations" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_qualifies_class_method_findings(self, mock_run, tmp_path: Path) -> None:
        source = tmp_path / "agentic_devtools" / "example.py"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("class Worker:\n    def complicated(self):\n        return 1\n", encoding="utf-8")
        identifier = "agentic_devtools/example.py::C901::Worker.complicated"
        _write_baseline(tmp_path, {identifier: "`complicated` is too complex (11 > 10)"})
        mock_run.return_value = CompletedProcess(
            args=[], returncode=1, stdout=json.dumps([_finding(source, row=2)]), stderr=""
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is True
        assert "no unbaselined complexity violations" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_tracks_findings_in_source_with_utf8_bom(self, mock_run, tmp_path: Path) -> None:
        source = tmp_path / "agentic_devtools" / "example.py"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(b"\xef\xbb\xbfdef complicated():\n    return 1\n")
        identifier = "agentic_devtools/example.py::C901::complicated"
        _write_baseline(tmp_path, {identifier: "`complicated` is too complex (11 > 10)"})
        mock_run.return_value = CompletedProcess(
            args=[], returncode=1, stdout=json.dumps([_finding(source)]), stderr=""
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is True
        assert "no unbaselined complexity violations" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_identifies_duplicate_function_definitions_individually(self, mock_run, tmp_path: Path) -> None:
        source = tmp_path / "agentic_devtools" / "example.py"
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(
            "def complicated():\n    return 1\n\n"
            "def complicated():\n    return 2\n\n"
            "def complicated():\n    return 3\n",
            encoding="utf-8",
        )
        identifiers = {
            "agentic_devtools/example.py::C901::complicated#2": "`complicated` is too complex (11 > 10)",
            "agentic_devtools/example.py::C901::complicated#3": "`complicated` is too complex (11 > 10)",
        }
        _write_baseline(tmp_path, identifiers)
        mock_run.return_value = CompletedProcess(
            args=[],
            returncode=1,
            stdout=json.dumps([_finding(source, row=4), _finding(source, row=7)]),
            stderr="",
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is True
        assert "no unbaselined complexity violations" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_reports_duplicate_findings_and_syntax_errors(self, mock_run, tmp_path: Path) -> None:
        source = _write_source(tmp_path)
        _write_baseline(tmp_path, {})
        finding = _finding(source)
        mock_run.return_value = CompletedProcess(
            args=[], returncode=1, stdout=json.dumps([finding, finding]), stderr=""
        )

        passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "Duplicate Ruff complexity finding" in output

        source.write_text("def invalid(:\n", encoding="utf-8")
        mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout=json.dumps([finding]), stderr="")
        passed, output = ComplexityChecker(tmp_path).check()
        assert passed is False
        assert "Could not identify Ruff complexity finding" in output

    @patch(f"{MODULE}.subprocess.run")
    def test_reports_function_nodes_without_end_lines(self, mock_run, tmp_path: Path) -> None:
        source = _write_source(tmp_path)
        _write_baseline(tmp_path, {})
        tree = ast.parse(source.read_text(encoding="utf-8"))
        tree.body[0].end_lineno = None
        mock_run.return_value = CompletedProcess(
            args=[], returncode=1, stdout=json.dumps([_finding(source)]), stderr=""
        )

        with patch(f"{MODULE}.ast.parse", return_value=tree):
            passed, output = ComplexityChecker(tmp_path).check()

        assert passed is False
        assert "function has no end line" in output
