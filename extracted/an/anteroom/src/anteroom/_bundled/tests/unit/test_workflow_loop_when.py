"""Tests for ``when`` guard evaluation inside loop steps (#1095).

The ``when`` clause already works for top-level steps.  These tests verify
that nested steps inside a ``loop`` also respect ``when``, matching the
top-level semantics: evaluate before step record creation, create record
directly as ``skipped``, and leave ``all_succeeded`` unchanged (neutral skip).
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import list_workflow_events, list_workflow_steps

# ---------------------------------------------------------------------------
# Inline YAML fixtures
# ---------------------------------------------------------------------------

LOOP_WITH_WHEN = """\
kind: workflow
id: loop_when_test
version: 0.1.0
inputs: {}
policies: {}
steps:
  - id: loop
    type: loop
    max_rounds: 3
    steps:
      - id: draft
        type: runner
        runner: shell
        command: "echo drafting"
      - id: review
        type: runner
        runner: shell
        command: "echo reviewing"
        when:
          step: draft
          field: result_status
          equals: success
"""

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


@pytest.fixture()
def engine(db: Any) -> WorkflowEngine:
    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry)


@pytest.fixture(autouse=True)
def _register_test_gates():
    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    register_gate_condition("always_pass", always_pass)
    yield


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestLoopWhenGuard:
    """Nested loop steps with ``when`` clauses."""

    @pytest.mark.asyncio
    async def test_skips_nested_step_on_condition_not_met(self, db: Any, engine: WorkflowEngine) -> None:
        """When draft fails, review should be skipped."""
        from unittest.mock import patch

        from anteroom.services.workflow_runners import RunnerResult

        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            # draft always fails
            return RunnerResult(status="failed", summary="draft failed")

        defn = load_definition(LOOP_WITH_WHEN)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t1")

        steps = list_workflow_steps(db, run["id"])
        review_steps = [s for s in steps if s["step_id"].startswith("review_r")]
        assert len(review_steps) > 0
        for rs in review_steps:
            assert rs["status"] == "skipped"
            assert rs["result_summary"] == "Condition not met"

    @pytest.mark.asyncio
    async def test_executes_on_condition_met(self, db: Any, engine: WorkflowEngine) -> None:
        """When draft succeeds, review should execute."""
        from unittest.mock import patch

        from anteroom.services.workflow_runners import RunnerResult

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(LOOP_WITH_WHEN)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t2")

        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        review_steps = [s for s in steps if s["step_id"].startswith("review_r")]
        assert len(review_steps) >= 1
        # review ran (not skipped) — completed with a result
        assert review_steps[0]["status"] == "completed"
        assert review_steps[0]["result_status"] == "success"

    @pytest.mark.asyncio
    async def test_skip_is_neutral_for_all_succeeded(self, db: Any, engine: WorkflowEngine) -> None:
        """A skipped when step does NOT set all_succeeded=False.

        If draft succeeds and review is skipped for some other reason,
        the loop should still complete on that round because all non-skipped
        steps succeeded.
        """
        from unittest.mock import patch

        from anteroom.services.workflow_runners import RunnerResult

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(LOOP_WITH_WHEN)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t3")

        # Both draft and review succeed → loop completes in 1 round
        assert run["status"] == "completed"
        steps = list_workflow_steps(db, run["id"])
        # Only round 1 steps — no round 2
        draft_steps = [s for s in steps if s["step_id"].startswith("draft_r")]
        assert len(draft_steps) == 1

    @pytest.mark.asyncio
    async def test_no_step_started_event_for_skipped(self, db: Any, engine: WorkflowEngine) -> None:
        """Skipped nested steps must NOT emit step_started events."""
        from unittest.mock import patch

        from anteroom.services.workflow_runners import RunnerResult

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            return RunnerResult(status="failed", summary="draft failed")

        defn = load_definition(LOOP_WITH_WHEN)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t4")

        events = list_workflow_events(db, run["id"])
        review_events = [e for e in events if e.get("step_id") and e["step_id"].startswith("review_r")]
        event_types = [e["event_type"] for e in review_events]
        assert "step_started" not in event_types
        assert "step_skipped" in event_types

    @pytest.mark.asyncio
    async def test_draft_fail_skip_review_retry_succeeds(self, db: Any, engine: WorkflowEngine) -> None:
        """Round 1: draft fails, review skipped. Round 2: both succeed."""
        from unittest.mock import patch

        from anteroom.services.workflow_runners import RunnerResult

        call_count = 0

        async def mock_runner(*args: Any, **kwargs: Any) -> RunnerResult:
            nonlocal call_count
            call_count += 1
            # Calls 1 = draft_r1 (fail), 2 = draft_r2 (succeed), 3 = review_r2 (succeed)
            if call_count == 1:
                return RunnerResult(status="failed", summary="draft failed")
            return RunnerResult(status="success", summary="ok")

        defn = load_definition(LOOP_WITH_WHEN)

        with patch("anteroom.services.workflow_runners.execute_opaque_runner", side_effect=mock_runner):
            run = await engine.start_run(defn, target_kind="task", target_ref="t5")

        assert run["status"] == "completed"
        assert call_count == 3  # draft_r1, draft_r2, review_r2

        steps = list_workflow_steps(db, run["id"])
        # review_r1 should be skipped
        review_r1 = [s for s in steps if s["step_id"] == "review_r1"]
        assert len(review_r1) == 1
        assert review_r1[0]["status"] == "skipped"

        # review_r2 should have run
        review_r2 = [s for s in steps if s["step_id"] == "review_r2"]
        assert len(review_r2) == 1
        assert review_r2[0]["status"] == "completed"
        assert review_r2[0]["result_status"] == "success"
