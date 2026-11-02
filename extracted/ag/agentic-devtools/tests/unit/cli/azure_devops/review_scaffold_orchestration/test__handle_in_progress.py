"""Tests for _handle_in_progress."""

from datetime import UTC, datetime

from agentic_devtools.cli.azure_devops.review_scaffold_orchestration import _handle_in_progress
from tests.unit.cli.azure_devops.review_scaffold_orchestration._test_helpers import make_state


def test_dry_run_does_not_save_state():
    _handle_in_progress(
        make_state(),
        "model",
        "commit",
        "commit",
        123,
        True,
        True,
        None,
        {},
        "https://api/threads",
        datetime(2026, 10, 20, tzinfo=UTC),
    )
