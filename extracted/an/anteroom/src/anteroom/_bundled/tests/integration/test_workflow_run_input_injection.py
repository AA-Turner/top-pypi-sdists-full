"""Integration tests for workflow run input injection (#889).

Tests the fetch/ack durability guarantee: if ack fails after fetch,
the row remains unconsumed and is retried on the next drain cycle.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest

from anteroom.db import init_db
from anteroom.services.workflow_storage import (
    create_workflow_run,
    emit_workflow_run_input,
    fetch_pending_run_inputs,
    mark_run_input_consumed,
)


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _make_run(db: Any, **overrides: Any) -> dict[str, Any]:
    defaults = {
        "workflow_id": "issue_delivery",
        "workflow_version": "0.1.0",
        "target_kind": "issue",
        "target_ref": "889",
    }
    defaults.update(overrides)
    return create_workflow_run(db, **defaults)


class TestDrainerDurability:
    def test_drainer_resends_after_crash_between_enqueue_and_ack(self, db: Any) -> None:
        """If the ack step is skipped (simulating a crash), the row stays unconsumed."""
        run = _make_run(db)
        row_id = emit_workflow_run_input(db, run["id"], "follow-up message", "attach")

        # Simulate drainer cycle 1: fetch succeeds, but process crashes before ack
        pending = fetch_pending_run_inputs(db, run["id"])
        assert len(pending) == 1
        assert pending[0]["id"] == row_id
        # (ack never called — simulating crash)

        # Simulate drainer cycle 2: row should still be available
        still_pending = fetch_pending_run_inputs(db, run["id"])
        assert len(still_pending) == 1
        assert still_pending[0]["id"] == row_id

    def test_drainer_does_not_resend_after_successful_ack(self, db: Any) -> None:
        """After successful ack, the row is consumed and not re-fetched."""
        run = _make_run(db)
        row_id = emit_workflow_run_input(db, run["id"], "one-shot message", "update")

        pending = fetch_pending_run_inputs(db, run["id"])
        assert len(pending) == 1

        mark_run_input_consumed(db, row_id)

        pending_after = fetch_pending_run_inputs(db, run["id"])
        assert len(pending_after) == 0
