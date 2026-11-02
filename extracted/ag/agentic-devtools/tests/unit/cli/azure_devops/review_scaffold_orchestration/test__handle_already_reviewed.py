"""Tests for _handle_already_reviewed."""

from datetime import UTC, datetime

from agentic_devtools.cli.azure_devops.review_scaffold_orchestration import _handle_already_reviewed
from tests.unit.cli.azure_devops.review_scaffold_orchestration._test_helpers import make_config, make_state


def test_returns_state_for_dry_run_rereview():
    state = make_state()

    result = _handle_already_reviewed(
        state,
        True,
        True,
        False,
        "model",
        "commit",
        123,
        "commit",
        None,
        {},
        "https://api/threads",
        make_config(),
        "repo",
        datetime(2026, 10, 20, tzinfo=UTC),
    )

    assert result is state
