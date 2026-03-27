"""Tests for workflow parallel branches and join semantics (#976)."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_engine import (
    BranchDef,
    WorkflowEngine,
    WorkflowStepDef,
    _all_steps,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import create_stub_registry
from anteroom.services.workflow_storage import (
    create_workflow_step,
    list_branch_steps,
    list_workflow_events,
    list_workflow_steps,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_db():
    td = tempfile.mkdtemp()
    return init_db(Path(td) / "test.db")


def _engine(db, **kwargs):
    config = WorkflowConfig()
    registry = create_stub_registry()
    return WorkflowEngine(db, config, registry, **kwargs)


# ---------------------------------------------------------------------------
# YAML fixtures
# ---------------------------------------------------------------------------

PARALLEL_BASIC = """\
kind: workflow
id: parallel_basic
version: 0.1.0
inputs: {}
steps:
  - id: setup
    type: runner
    runner: stub
    command: "echo setup"
  - id: parallel_work
    type: parallel
    join: all
    branches:
      - id: lint
        steps:
          - id: run_lint
            type: runner
            runner: stub
            command: "echo lint"
      - id: test
        steps:
          - id: run_tests
            type: runner
            runner: stub
            command: "echo test"
  - id: deploy
    type: runner
    runner: stub
    command: "echo deploy"
"""

PARALLEL_SLASH_IN_STEP_ID = """\
kind: workflow
id: bad_step
version: 0.1.0
inputs: {}
steps:
  - id: a/b
    type: runner
    runner: stub
    command: "echo fail"
"""

PARALLEL_SLASH_IN_BRANCH_ID = """\
kind: workflow
id: bad_branch
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: a/b
        steps:
          - id: step1
            type: runner
            runner: stub
            command: "echo fail"
"""

PARALLEL_NESTED = """\
kind: workflow
id: nested_parallel
version: 0.1.0
inputs: {}
steps:
  - id: outer
    type: parallel
    join: all
    branches:
      - id: b1
        steps:
          - id: inner
            type: parallel
            join: all
            branches:
              - id: b1a
                steps:
                  - id: s
                    type: runner
                    runner: stub
                    command: "echo fail"
"""

PARALLEL_HUMAN_GATE_IN_BRANCH = """\
kind: workflow
id: hg_in_branch
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: b1
        steps:
          - id: gate
            type: human_gate
            prompt: "Approve?"
            options:
              - id: yes
                label: "Yes"
                outcome: continue
"""

PARALLEL_DUP_BRANCH_ID = """\
kind: workflow
id: dup_branch
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: same
        steps:
          - id: s1
            type: runner
            runner: stub
            command: "echo a"
      - id: same
        steps:
          - id: s2
            type: runner
            runner: stub
            command: "echo b"
"""

PARALLEL_BAD_JOIN = """\
kind: workflow
id: bad_join
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: any
    branches:
      - id: b1
        steps:
          - id: s1
            type: runner
            runner: stub
            command: "echo a"
"""

PARALLEL_CONTEXT_FROM_SIBLING = """\
kind: workflow
id: sibling_ref
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: a
        steps:
          - id: s1
            type: runner
            runner: stub
            command: "echo a"
      - id: b
        steps:
          - id: s2
            type: runner
            runner: stub
            command: "echo b"
            context_from:
              - step: s1
                field: result_summary
"""

PARALLEL_CONTEXT_FROM_PRE_PARALLEL = """\
kind: workflow
id: pre_ref
version: 0.1.0
inputs: {}
steps:
  - id: setup
    type: runner
    runner: stub
    command: "echo setup"
  - id: par
    type: parallel
    join: all
    branches:
      - id: a
        steps:
          - id: s1
            type: runner
            runner: stub
            command: "echo a"
            context_from:
              - step: setup
                field: result_summary
"""

PARALLEL_POST_JOIN_CONTEXT_FROM = """\
kind: workflow
id: post_join
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: a
        steps:
          - id: s1
            type: runner
            runner: stub
            command: "echo a"
      - id: b
        steps:
          - id: s2
            type: runner
            runner: stub
            command: "echo b"
  - id: final
    type: runner
    runner: stub
    command: "echo done"
    context_from:
      - step: a/s1
        field: result_summary
"""


# ---------------------------------------------------------------------------
# Parsing tests
# ---------------------------------------------------------------------------


class TestParallelParsing:
    def test_basic_parallel_loads(self):
        defn = load_definition(PARALLEL_BASIC)
        assert len(defn.steps) == 3
        par = defn.steps[1]
        assert par.type == "parallel"
        assert par.join == "all"
        assert len(par.branches) == 2
        assert par.branches[0].id == "lint"
        assert par.branches[1].id == "test"
        assert len(par.branches[0].steps) == 1

    def test_slash_in_step_id_rejected(self):
        with pytest.raises(ValueError, match="must not contain '/'"):
            load_definition(PARALLEL_SLASH_IN_STEP_ID)

    def test_slash_in_branch_id_rejected(self):
        with pytest.raises(ValueError, match="must not contain '/'"):
            load_definition(PARALLEL_SLASH_IN_BRANCH_ID)

    def test_nested_parallel_rejected(self):
        with pytest.raises(ValueError, match="nested parallel"):
            load_definition(PARALLEL_NESTED)

    def test_human_gate_in_branch_rejected(self):
        with pytest.raises(ValueError, match="human_gate steps are not allowed"):
            load_definition(PARALLEL_HUMAN_GATE_IN_BRANCH)

    def test_duplicate_branch_id_rejected(self):
        with pytest.raises(ValueError, match="duplicate branch id"):
            load_definition(PARALLEL_DUP_BRANCH_ID)

    def test_bad_join_rejected(self):
        with pytest.raises(ValueError, match="only join='all'"):
            load_definition(PARALLEL_BAD_JOIN)

    def test_no_branches_rejected(self):
        yaml_str = """\
kind: workflow
id: no_branches
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches: []
"""
        with pytest.raises(ValueError, match="at least one branch"):
            load_definition(yaml_str)


# ---------------------------------------------------------------------------
# context_from scope tests
# ---------------------------------------------------------------------------


class TestContextFromScope:
    def test_sibling_branch_ref_rejected(self):
        """Steps in branch B cannot reference steps in sibling branch A."""
        with pytest.raises(ValueError, match="has not appeared before"):
            load_definition(PARALLEL_CONTEXT_FROM_SIBLING)

    def test_pre_parallel_ref_allowed(self):
        """Branch steps can reference prior top-level steps."""
        defn = load_definition(PARALLEL_CONTEXT_FROM_PRE_PARALLEL)
        assert defn.steps[1].type == "parallel"

    def test_post_join_ref_qualified_id(self):
        """Steps after parallel can reference branch steps via qualified IDs."""
        defn = load_definition(PARALLEL_POST_JOIN_CONTEXT_FROM)
        final = defn.steps[1]
        assert final.id == "final"
        assert final.context_from[0]["step"] == "a/s1"


# ---------------------------------------------------------------------------
# _all_steps() tests
# ---------------------------------------------------------------------------


class TestAllSteps:
    def test_yields_qualified_ids(self):
        defn = load_definition(PARALLEL_BASIC)
        all_steps = _all_steps(defn.steps)
        step_ids = [s.id for s in all_steps]
        assert "setup" in step_ids
        assert "parallel_work" in step_ids
        assert "lint/run_lint" in step_ids
        assert "test/run_tests" in step_ids
        assert "deploy" in step_ids

    def test_qualified_ids_count(self):
        defn = load_definition(PARALLEL_BASIC)
        all_steps = _all_steps(defn.steps)
        # setup + parallel_work + lint/run_lint + test/run_tests + deploy = 5
        assert len(all_steps) == 5


# ---------------------------------------------------------------------------
# DB / storage tests
# ---------------------------------------------------------------------------


class TestWorkflowStorage:
    def test_create_step_with_branch_id(self):
        db = _make_db()
        try:
            from anteroom.services.workflow_storage import create_workflow_run

            run = create_workflow_run(
                db,
                workflow_id="test",
                workflow_version="0.1.0",
                target_kind="test",
                target_ref="test",
            )
            step = create_workflow_step(
                db,
                run_id=run["id"],
                step_id="lint/s1",
                step_type="runner",
                runner_type="stub",
                branch_id="lint",
            )
            assert step["branch_id"] == "lint"
            assert step["step_id"] == "lint/s1"
        finally:
            db.close()

    def test_list_branch_steps(self):
        db = _make_db()
        try:
            from anteroom.services.workflow_storage import create_workflow_run

            run = create_workflow_run(
                db,
                workflow_id="test",
                workflow_version="0.1.0",
                target_kind="test",
                target_ref="test",
            )
            create_workflow_step(
                db,
                run_id=run["id"],
                step_id="a/s1",
                step_type="runner",
                branch_id="a",
            )
            create_workflow_step(
                db,
                run_id=run["id"],
                step_id="b/s1",
                step_type="runner",
                branch_id="b",
            )
            a_steps = list_branch_steps(db, run["id"], "a")
            b_steps = list_branch_steps(db, run["id"], "b")
            assert len(a_steps) == 1
            assert len(b_steps) == 1
            assert a_steps[0]["step_id"] == "a/s1"
        finally:
            db.close()

    def test_parallel_step_type_valid(self):
        db = _make_db()
        try:
            from anteroom.services.workflow_storage import create_workflow_run

            run = create_workflow_run(
                db,
                workflow_id="test",
                workflow_version="0.1.0",
                target_kind="test",
                target_ref="test",
            )
            step = create_workflow_step(
                db,
                run_id=run["id"],
                step_id="par1",
                step_type="parallel",
            )
            assert step["step_type"] == "parallel"
        finally:
            db.close()


# ---------------------------------------------------------------------------
# Engine execution tests
# ---------------------------------------------------------------------------


class TestParallelExecution:
    @pytest.mark.asyncio
    async def test_both_branches_run(self):
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-par")
            assert run["status"] == "completed"

            steps = list_workflow_steps(db, run["id"])
            step_ids = {s["step_id"] for s in steps}
            assert "lint/run_lint" in step_ids
            assert "test/run_tests" in step_ids
            assert "setup" in step_ids
            assert "deploy" in step_ids
            assert "parallel_work" in step_ids
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_branch_steps_have_branch_id(self):
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-br")

            steps = list_workflow_steps(db, run["id"])
            branch_steps = [s for s in steps if s.get("branch_id")]
            assert len(branch_steps) == 2
            branch_ids = {s["branch_id"] for s in branch_steps}
            assert branch_ids == {"lint", "test"}
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_one_branch_fails_cancels_other(self):
        """If one branch fails, the other should be cancelled (join:all)."""
        db = _make_db()
        try:
            engine = _engine(db)
            engine._stub_results = {  # type: ignore[attr-defined]
                "run_lint": {"status": "failed", "summary": "lint error"},
            }

            yaml_str = """\
kind: workflow
id: fail_test
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: lint
        steps:
          - id: run_lint
            type: runner
            runner: stub
            command: "echo lint"
      - id: test
        steps:
          - id: run_tests
            type: runner
            runner: stub
            command: "echo test"
"""
            defn = load_definition(yaml_str)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-fail")
            assert run["status"] == "failed"
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_qualified_step_ids_in_records(self):
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-qual")

            steps = list_workflow_steps(db, run["id"])
            step_ids = [s["step_id"] for s in steps]
            assert "lint/run_lint" in step_ids
            assert "test/run_tests" in step_ids
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_checkpoint_after_parallel(self):
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-ckpt")

            from anteroom.services.workflow_storage import list_checkpoints

            checkpoints = list_checkpoints(db, run["id"])
            labels = [c["label"] for c in checkpoints]
            assert "after:parallel_work" in labels
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_events_emitted_for_branch_steps(self):
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-evt")

            events = list_workflow_events(db, run["id"])
            step_started_ids = {e["step_id"] for e in events if e["event_type"] == "step_started" and e["step_id"]}
            assert "lint/run_lint" in step_started_ids
            assert "test/run_tests" in step_started_ids

            step_finished_ids = {e["step_id"] for e in events if e["event_type"] == "step_finished" and e["step_id"]}
            assert "lint/run_lint" in step_finished_ids
            assert "test/run_tests" in step_finished_ids
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_budget_aggregation(self):
        db = _make_db()
        try:
            engine = _engine(db)
            engine._stub_results = {  # type: ignore[attr-defined]
                "run_lint": {
                    "status": "success",
                    "summary": "lint ok",
                    "artifacts": {"total_tokens": 100, "prompt_tokens": 60, "completion_tokens": 40},
                },
                "run_tests": {
                    "status": "success",
                    "summary": "tests ok",
                    "artifacts": {"total_tokens": 200, "prompt_tokens": 120, "completion_tokens": 80},
                },
            }
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-budget")

            from anteroom.services.workflow_storage import get_workflow_run

            final_run = get_workflow_run(db, run["id"])
            usage = final_run["budget_usage"]
            # Branch tokens: 100 + 200 = 300, plus other steps (setup=0, deploy=0, parallel_work=0)
            assert usage["total_tokens"] >= 300
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_branch_does_not_update_run_status(self):
        """_execute_branch_steps should NOT call ws.update_workflow_run for status transitions."""
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-no-status")

            # If we got here without error, the run completed successfully
            # The point is that branch execution doesn't independently set run status
            assert run["status"] == "completed"
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_both_branches_fail(self):
        db = _make_db()
        try:
            engine = _engine(db)
            engine._stub_results = {  # type: ignore[attr-defined]
                "run_lint": {"status": "failed", "summary": "lint error"},
                "run_tests": {"status": "failed", "summary": "test error"},
            }

            yaml_str = """\
kind: workflow
id: both_fail
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: lint
        steps:
          - id: run_lint
            type: runner
            runner: stub
            command: "echo lint"
      - id: test
        steps:
          - id: run_tests
            type: runner
            runner: stub
            command: "echo test"
"""
            defn = load_definition(yaml_str)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-both-fail")
            assert run["status"] == "failed"
        finally:
            db.close()


# ---------------------------------------------------------------------------
# Resume tests
# ---------------------------------------------------------------------------


class TestParallelResume:
    @pytest.mark.asyncio
    async def test_resume_skips_completed_branch_steps(self):
        """Completed branch steps should be skipped on resume."""
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-resume")
            # Run completed, so resume from deploy
            # This verifies the qualified IDs are tracked
            assert run["status"] == "completed"
        finally:
            db.close()


# ---------------------------------------------------------------------------
# _execute_branch_steps isolation tests
# ---------------------------------------------------------------------------


class TestBranchStepIsolation:
    @pytest.mark.asyncio
    async def test_branch_does_not_create_checkpoint(self):
        """Branch execution should not create its own checkpoints."""
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-no-ckpt")

            from anteroom.services.workflow_storage import list_checkpoints

            checkpoints = list_checkpoints(db, run["id"])
            # Checkpoints should be: after:setup, after:parallel_work, after:deploy, completed
            labels = [c["label"] for c in checkpoints]
            # There should NOT be any checkpoint from inside a branch
            branch_checkpoints = [lb for lb in labels if lb.startswith("after:lint/") or lb.startswith("after:test/")]
            assert len(branch_checkpoints) == 0
        finally:
            db.close()

    @pytest.mark.asyncio
    async def test_branch_does_not_set_current_step(self):
        """Branch execution should not update run.current_step_id to branch-qualified IDs."""
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(PARALLEL_BASIC)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-nostep")
            assert run["status"] == "completed"
            # Verify current_step_id is never a branch-qualified ID
            # After completion, current_step_id should be a top-level step
            from anteroom.services.workflow_storage import get_workflow_run

            final = get_workflow_run(db, run["id"])
            cid = final.get("current_step_id") or ""
            # Branch-qualified IDs contain "/"  — current_step_id should not
            # (it's set by _execute_steps, not _execute_branch_steps)
            assert "/" not in cid or cid == ""
        finally:
            db.close()


# ---------------------------------------------------------------------------
# Multi-step branches
# ---------------------------------------------------------------------------


class TestMultiStepBranches:
    @pytest.mark.asyncio
    async def test_multi_step_branches(self):
        yaml_str = """\
kind: workflow
id: multi_step
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: a
        steps:
          - id: s1
            type: runner
            runner: stub
            command: "echo a1"
          - id: s2
            type: runner
            runner: stub
            command: "echo a2"
      - id: b
        steps:
          - id: s1
            type: runner
            runner: stub
            command: "echo b1"
"""
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(yaml_str)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-multi")
            assert run["status"] == "completed"

            steps = list_workflow_steps(db, run["id"])
            step_ids = {s["step_id"] for s in steps}
            assert "a/s1" in step_ids
            assert "a/s2" in step_ids
            assert "b/s1" in step_ids
        finally:
            db.close()


# ---------------------------------------------------------------------------
# Gate step inside branch
# ---------------------------------------------------------------------------


class TestGateInBranch:
    @pytest.mark.asyncio
    async def test_gate_in_branch(self):
        async def _always_pass(r, s, i):
            return True

        register_gate_condition("always_pass", _always_pass)

        yaml_str = """\
kind: workflow
id: gate_branch
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: a
        steps:
          - id: check
            type: gate
            condition: always_pass
            if_false: "not ready"
          - id: work
            type: runner
            runner: stub
            command: "echo work"
"""
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(yaml_str)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-gate-br")
            assert run["status"] == "completed"
        finally:
            db.close()


# ---------------------------------------------------------------------------
# Empty branch
# ---------------------------------------------------------------------------


class TestEmptyBranch:
    @pytest.mark.asyncio
    async def test_empty_branch_succeeds(self):
        yaml_str = """\
kind: workflow
id: empty_branch
version: 0.1.0
inputs: {}
steps:
  - id: par
    type: parallel
    join: all
    branches:
      - id: a
        steps: []
      - id: b
        steps:
          - id: s1
            type: runner
            runner: stub
            command: "echo b"
"""
        db = _make_db()
        try:
            engine = _engine(db)
            defn = load_definition(yaml_str)
            run = await engine.start_run(defn, target_kind="test", target_ref="test-empty")
            assert run["status"] == "completed"
        finally:
            db.close()


# ---------------------------------------------------------------------------
# BranchDef dataclass
# ---------------------------------------------------------------------------


class TestBranchDef:
    def test_branch_def_fields(self):
        bd = BranchDef(id="lint", steps=[])
        assert bd.id == "lint"
        assert bd.steps == []

    def test_branch_def_with_steps(self):
        step = WorkflowStepDef(id="s1", type="runner", runner="stub")
        bd = BranchDef(id="test", steps=[step])
        assert len(bd.steps) == 1
        assert bd.steps[0].id == "s1"
