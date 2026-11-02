"""Git paths are checked, never normalized."""

from agentic_devtools.cli.ci.pipeline.conflict_reconciliation import _validate_path


def test_valid_path():
    assert _validate_path("src/file with spaces.py") is None
