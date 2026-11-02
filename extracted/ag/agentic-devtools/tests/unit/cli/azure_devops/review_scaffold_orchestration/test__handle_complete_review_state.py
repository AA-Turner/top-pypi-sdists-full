"""Tests for _handle_complete_review_state."""

from datetime import UTC, datetime
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.review_scaffold_orchestration import _handle_complete_review_state
from tests.unit.cli.azure_devops.review_scaffold_orchestration._test_helpers import make_config, make_state


def test_routes_first_review_state_to_compatibility_skip():
    state = make_state()
    with patch(
        "agentic_devtools.cli.azure_devops.review_scaffold_orchestration._check_session_status",
        return_value="first_review",
    ):
        handled, result = _handle_complete_review_state(
            state,
            123,
            ["/src/a.ts"],
            make_config(),
            "repo",
            "repo",
            1,
            None,
            {},
            True,
            "commit",
            "model",
            False,
            False,
            datetime(2026, 10, 20, tzinfo=UTC),
        )

    assert handled is True
    assert result is state
