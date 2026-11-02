"""Tests for _handle_different_model."""

from datetime import UTC, datetime

from agentic_devtools.cli.azure_devops.review_scaffold_orchestration import _handle_different_model
from tests.unit.cli.azure_devops.review_scaffold_orchestration._test_helpers import make_state


def test_dry_run_returns_existing_state():
    state = make_state()

    result = _handle_different_model(
        state,
        "model",
        "commit",
        123,
        True,
        None,
        {},
        "https://api/threads",
        "https://dev.azure.com/org/project/_git/repo/pullrequest/123",
        datetime(2026, 10, 20, tzinfo=UTC),
    )

    assert result is state
