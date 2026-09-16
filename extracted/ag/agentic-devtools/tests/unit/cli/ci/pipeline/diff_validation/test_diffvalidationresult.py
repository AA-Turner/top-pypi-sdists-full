"""Tests for DiffValidationResult."""

from dataclasses import FrozenInstanceError

import pytest

from agentic_devtools.cli.ci.pipeline.diff_validation import DiffValidationResult


class TestDiffValidationResult:
    """Unit tests for the diff validation result dataclass."""

    def test_defaults(self) -> None:
        result = DiffValidationResult(valid=True)
        assert result.valid is True
        assert result.missing_files == ()
        assert result.reason == ""

    def test_is_frozen(self) -> None:
        result = DiffValidationResult(valid=True)
        with pytest.raises(FrozenInstanceError):
            setattr(result, "reason", "mutated")
