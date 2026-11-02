from __future__ import annotations

from agentic_devtools.cli.azure_devops.commands import ReviewStateNotFoundError


def test_inherits_file_not_found_error() -> None:
    error = ReviewStateNotFoundError("missing")
    assert isinstance(error, FileNotFoundError)


def test_preserves_message() -> None:
    error = ReviewStateNotFoundError("missing")
    assert str(error) == "missing"
