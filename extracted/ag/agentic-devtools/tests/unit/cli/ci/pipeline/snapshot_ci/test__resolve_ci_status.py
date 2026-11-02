"""Tests for _resolve_ci_status."""

import pytest

from agentic_devtools.cli.ci.pipeline.snapshot_ci import _resolve_ci_status


@pytest.mark.parametrize(
    ("checks", "codeql_seen", "codeql_configured", "failed", "expected"),
    [
        ([("build", "passing")], False, True, [], ("pending", [])),
        ([], False, False, [], ("pending", [])),
        ([("build", "pending"), ("test", "failing")], True, False, ["test"], ("pending", ["test"])),
        ([("build", "failing")], True, False, ["build"], ("failing", ["build"])),
        ([("build", "unknown")], True, False, [], ("unknown", [])),
        ([("build", "passing")], True, False, [], ("passing", [])),
        ([("build", "unknown"), ("test", "failing")], True, False, ["test"], ("failing", ["test"])),
    ],
)
def test_applies_codeql_requirement_and_status_precedence(
    checks: list[tuple[str, str]],
    codeql_seen: bool,
    codeql_configured: bool,
    failed: list[str],
    expected: tuple[str, list[str]],
) -> None:
    """Missing CodeQL, empty inventories, and mixed states follow pipeline precedence."""
    assert _resolve_ci_status(checks, codeql_seen, codeql_configured, failed) == expected
