"""Shared fixtures for orchestration/runner unit tests."""

from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def mock_runner_state(tmp_path):
    """Provide valid bootstrap state and a scoped state directory for all runner tests.

    The runner rejects unscoped fallback directories (_unscoped/.agdt-temp) and
    reads worktree_key from get_bootstrap_state() (FR-004).  This autouse fixture
    ensures every test that calls run_langchain_workflow() has both a properly-scoped
    state directory and a valid worktree key available without each test needing its
    own explicit patches.

    Tests that need different values can override either patch directly.  Tests that
    specifically exercise the unscoped-dir or missing-key failure paths should supply
    their own patches as fixtures or context managers.
    """
    scoped_dir = tmp_path / "test-worktree"
    scoped_dir.mkdir(parents=True, exist_ok=True)
    with (
        patch(
            "agentic_devtools.state.get_bootstrap_state",
            return_value={"worktree_key": "test-worktree"},
        ),
        patch(
            "agentic_devtools.state.get_state_dir",
            return_value=scoped_dir,
        ),
    ):
        yield scoped_dir
