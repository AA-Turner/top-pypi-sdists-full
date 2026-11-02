"""Tests for the shared quality-baseline loader."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.checks.quality_baseline import read_quality_baseline


def _write_baseline(path: Path, contents: object) -> None:
    path.write_text(json.dumps(contents), encoding="utf-8")


def test_reads_and_validates_shared_baseline(tmp_path: Path) -> None:
    baseline_path = tmp_path / "quality-baseline.json"
    _write_baseline(
        baseline_path,
        {
            "schema_version": 1,
            "file_length": {"agentic_devtools/sample.py": 201},
            "complexity": {"agentic_devtools/sample.py::C901::sample": "too complex"},
        },
    )

    file_lengths, complexity, error = read_quality_baseline(tmp_path)

    assert file_lengths == {"agentic_devtools/sample.py": 201}
    assert complexity == {"agentic_devtools/sample.py::C901::sample": "too complex"}
    assert error is None


def test_reports_missing_baseline(tmp_path: Path) -> None:
    file_lengths, complexity, error = read_quality_baseline(tmp_path)

    assert file_lengths == {}
    assert complexity == {}
    assert error == "ERROR: quality-baseline.json is missing."


@pytest.mark.parametrize("read_error", [OSError("read denied"), UnicodeError("invalid encoding")])
def test_reports_baseline_read_errors(tmp_path: Path, read_error: Exception) -> None:
    baseline_path = tmp_path / "quality-baseline.json"
    baseline_path.write_text("{}", encoding="utf-8")
    original_read_text = Path.read_text

    def fail_for_baseline(self: Path, encoding: str | None = None, errors: str | None = None) -> str:
        if self == baseline_path:
            raise read_error
        return original_read_text(self, encoding=encoding, errors=errors)

    with patch.object(Path, "read_text", fail_for_baseline):
        file_lengths, complexity, error = read_quality_baseline(tmp_path)

    assert file_lengths == {}
    assert complexity == {}
    assert error is not None
    assert "Could not read quality-baseline.json" in error


def test_reports_invalid_json(tmp_path: Path) -> None:
    (tmp_path / "quality-baseline.json").write_text("{", encoding="utf-8")

    _, _, error = read_quality_baseline(tmp_path)

    assert error is not None
    assert "Invalid quality baseline JSON" in error


def test_requires_an_object_root(tmp_path: Path) -> None:
    _write_baseline(tmp_path / "quality-baseline.json", [])

    _, _, error = read_quality_baseline(tmp_path)

    assert error == "ERROR: Invalid quality baseline: expected an object."


@pytest.mark.parametrize("version", [True, "1", 2])
def test_requires_supported_schema_version(tmp_path: Path, version: object) -> None:
    _write_baseline(
        tmp_path / "quality-baseline.json",
        {"schema_version": version, "file_length": {}, "complexity": {}},
    )

    _, _, error = read_quality_baseline(tmp_path)

    assert error is not None
    assert "Invalid quality baseline schema_version" in error


def test_requires_file_length_object(tmp_path: Path) -> None:
    _write_baseline(tmp_path / "quality-baseline.json", {"schema_version": 1, "file_length": [], "complexity": {}})

    _, _, error = read_quality_baseline(tmp_path)

    assert error == "ERROR: Invalid quality baseline: file_length must be an object."


def test_requires_complexity_object(tmp_path: Path) -> None:
    _write_baseline(tmp_path / "quality-baseline.json", {"schema_version": 1, "file_length": {}, "complexity": []})

    _, _, error = read_quality_baseline(tmp_path)

    assert error == "ERROR: Invalid quality baseline: complexity must be an object."


@pytest.mark.parametrize(
    "line_count",
    ["201", True, -1],
)
def test_rejects_invalid_file_length_entries(tmp_path: Path, line_count: object) -> None:
    _write_baseline(
        tmp_path / "quality-baseline.json",
        {"schema_version": 1, "file_length": {"sample.py": line_count}, "complexity": {}},
    )

    _, _, error = read_quality_baseline(tmp_path)

    assert error == "ERROR: Invalid quality baseline line count for 'sample.py'."


@pytest.mark.parametrize(
    ("identifier", "message"),
    [
        ("", "message"),
        ("sample.py::C901::sample", 1),
        ("sample.py::C901::sample", ""),
    ],
)
def test_rejects_invalid_complexity_entries(tmp_path: Path, identifier: str, message: object) -> None:
    _write_baseline(
        tmp_path / "quality-baseline.json",
        {"schema_version": 1, "file_length": {}, "complexity": {identifier: message}},
    )

    _, _, error = read_quality_baseline(tmp_path)

    assert error == f"ERROR: Invalid quality baseline complexity entry: {identifier!r}."
