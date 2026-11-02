from __future__ import annotations

from agentic_devtools.cli.azure_devops.commands import ReviewStateRepositoryMismatchError


def test_is_value_error() -> None:
    error = ReviewStateRepositoryMismatchError("mismatch")
    assert isinstance(error, ValueError)


def test_preserves_message() -> None:
    error = ReviewStateRepositoryMismatchError("mismatch")
    assert str(error) == "mismatch"
