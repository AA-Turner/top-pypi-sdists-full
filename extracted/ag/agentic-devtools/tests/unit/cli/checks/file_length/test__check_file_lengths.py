"""Tests for the file-length check result wrapper."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.checks.file_length import _check_file_lengths


def test_wraps_file_length_result(tmp_path: Path) -> None:
    with patch(
        "agentic_devtools.cli.checks.file_length.check_file_lengths",
        return_value=(False, "file grew"),
    ) as check:
        result = _check_file_lengths(tmp_path)

    check.assert_called_once_with(tmp_path)
    assert result.label == "File length"
    assert result.passed is False
    assert result.output == "file grew"
    assert result.duration >= 0
