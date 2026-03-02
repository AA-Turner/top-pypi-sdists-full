"""Shared fixtures for integration tests."""

from __future__ import annotations

import os
import tempfile
import uuid
from collections.abc import Generator
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from plato.storage import RolloutStorage


# Skip tests that require PLATO_API_KEY
def pytest_collection_modifyitems(config, items):  # type: ignore[no-untyped-def]
    """Skip integration tests that require PLATO_API_KEY if not set.

    Tests in test_browser_agent.py and TestE2EBrowserAgentBasic do NOT require PLATO_API_KEY.
    """
    if not os.environ.get("PLATO_API_KEY"):
        skip_marker = pytest.mark.skip(reason="PLATO_API_KEY not set")
        for item in items:
            # Skip integration tests EXCEPT browser agent tests and basic E2E tests
            if "integration" in str(item.fspath):
                # Allow test_browser_agent.py
                if "test_browser_agent" in str(item.fspath):
                    continue
                # Allow TestE2EBrowserAgentBasic tests
                if "test_e2e_browser_agent" in str(item.fspath) and "TestE2EBrowserAgentBasic" in item.nodeid:
                    continue
                # Allow test_harbor_agent_runner.py (uses its own API keys)
                if "test_harbor_agent_runner" in str(item.fspath):
                    continue
                # Allow test_chronos_callback.py (uses its own API keys)
                if "test_chronos_callback" in str(item.fspath):
                    continue
                item.add_marker(skip_marker)


@pytest.fixture
def run_id() -> str:
    """Generate unique run ID for test."""
    return f"test-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def temp_db_path() -> Generator[Path, None, None]:
    """Create temporary database path for test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "test_rollouts.db"


@pytest.fixture
def storage(run_id: str, temp_db_path: Path) -> Generator[RolloutStorage, None, None]:
    """Create RolloutStorage for test."""
    from plato.storage import RolloutStorage

    storage = RolloutStorage(
        run_id=run_id,
        agent_type="test-agent",
        model="test-model",
        world_name="test-world",
        db_path=temp_db_path,
    )
    yield storage
    storage.close()


@pytest.fixture
def temp_workspace() -> Generator[Path, None, None]:
    """Create temporary workspace directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
