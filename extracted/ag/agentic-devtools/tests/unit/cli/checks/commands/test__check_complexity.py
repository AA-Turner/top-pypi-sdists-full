"""Tests for the complexity-check result wrapper."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.checks.commands import _check_complexity


def test_wraps_complexity_result(tmp_path: Path) -> None:
    with patch("agentic_devtools.cli.checks.commands.ComplexityChecker") as checker_type:
        checker_type.return_value.check.return_value = (False, "new finding")

        result = _check_complexity(tmp_path)

    checker_type.assert_called_once_with(tmp_path)
    assert result.label == "Ruff complexity"
    assert result.passed is False
    assert result.output == "new finding"
    assert result.duration >= 0
