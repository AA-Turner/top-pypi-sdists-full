"""Unit tests for spec gate conditions — phase status checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from anteroom.services.spec_schema import SpecPhaseStatus
from anteroom.services.workflow_engine import GateResult

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


@pytest.fixture()
def _register_gates(db: Any) -> None:
    from anteroom.services.spec_gates import register_spec_gates

    register_spec_gates(db)


@pytest.fixture()
def spec_fqn(db: Any) -> str:
    from anteroom.services.spec_service import create_spec

    create_spec(db, "ns", "feat", VALID_SPEC_YAML)
    return "@ns/spec/feat"


# ---------------------------------------------------------------------------
# Gate condition: spec_requirements_approved
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("_register_gates")
class TestSpecRequirementsApproved:
    @pytest.mark.asyncio
    async def test_draft_returns_failed(self, spec_fqn: str) -> None:
        from anteroom.services.workflow_engine import get_gate_condition

        fn = get_gate_condition("spec_requirements_approved")
        assert fn is not None
        result = await fn({}, None, {"spec_fqn": spec_fqn})
        assert isinstance(result, GateResult)
        assert result.passed is False
        assert "'draft'" in result.reason

    @pytest.mark.asyncio
    async def test_approved_returns_passed(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import approve_phase
        from anteroom.services.workflow_engine import get_gate_condition

        approve_phase(db, spec_fqn, "requirements", "troy")
        fn = get_gate_condition("spec_requirements_approved")
        result = await fn({}, None, {"spec_fqn": spec_fqn})
        assert isinstance(result, GateResult)
        assert result.passed is True

    @pytest.mark.asyncio
    async def test_stale_returns_failed(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.spec_schema import set_phase_status
        from anteroom.services.workflow_engine import get_gate_condition

        # Manually set to stale via metadata
        art = artifact_storage.get_artifact_by_fqn(db, spec_fqn)
        new_meta = set_phase_status(art["metadata"], "requirements", SpecPhaseStatus.STALE)
        artifact_storage.update_artifact(db, art["id"], metadata=new_meta)

        fn = get_gate_condition("spec_requirements_approved")
        result = await fn({}, None, {"spec_fqn": spec_fqn})
        assert result.passed is False
        assert "'stale'" in result.reason


# ---------------------------------------------------------------------------
# Gate condition: spec_design_approved
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("_register_gates")
class TestSpecDesignApproved:
    @pytest.mark.asyncio
    async def test_draft_returns_failed(self, spec_fqn: str) -> None:
        from anteroom.services.workflow_engine import get_gate_condition

        fn = get_gate_condition("spec_design_approved")
        result = await fn({}, None, {"spec_fqn": spec_fqn})
        assert result.passed is False

    @pytest.mark.asyncio
    async def test_approved_returns_passed(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import approve_phase
        from anteroom.services.workflow_engine import get_gate_condition

        approve_phase(db, spec_fqn, "design", "troy")
        fn = get_gate_condition("spec_design_approved")
        result = await fn({}, None, {"spec_fqn": spec_fqn})
        assert result.passed is True


# ---------------------------------------------------------------------------
# Gate condition: spec_tasks_approved
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("_register_gates")
class TestSpecTasksApproved:
    @pytest.mark.asyncio
    async def test_draft_returns_failed(self, spec_fqn: str) -> None:
        from anteroom.services.workflow_engine import get_gate_condition

        fn = get_gate_condition("spec_tasks_approved")
        result = await fn({}, None, {"spec_fqn": spec_fqn})
        assert result.passed is False

    @pytest.mark.asyncio
    async def test_approved_returns_passed(self, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import approve_phase
        from anteroom.services.workflow_engine import get_gate_condition

        approve_phase(db, spec_fqn, "tasks", "troy")
        fn = get_gate_condition("spec_tasks_approved")
        result = await fn({}, None, {"spec_fqn": spec_fqn})
        assert result.passed is True


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------


@pytest.mark.usefixtures("_register_gates")
class TestSpecGateErrors:
    @pytest.mark.asyncio
    async def test_missing_spec_fqn_input(self) -> None:
        from anteroom.services.workflow_engine import get_gate_condition

        fn = get_gate_condition("spec_requirements_approved")
        result = await fn({}, None, {})
        assert result.passed is False
        assert "No 'spec_fqn'" in result.reason

    @pytest.mark.asyncio
    async def test_nonexistent_spec(self) -> None:
        from anteroom.services.workflow_engine import get_gate_condition

        fn = get_gate_condition("spec_requirements_approved")
        result = await fn({}, None, {"spec_fqn": "@ns/spec/nope"})
        assert result.passed is False
        assert "not found" in result.reason

    @pytest.mark.asyncio
    async def test_non_spec_artifact(self, db: Any) -> None:
        from anteroom.services import artifact_storage
        from anteroom.services.workflow_engine import get_gate_condition

        artifact_storage.create_artifact(db, "@ns/skill/x", "skill", "ns", "x", "content")
        fn = get_gate_condition("spec_requirements_approved")
        result = await fn({}, None, {"spec_fqn": "@ns/skill/x"})
        assert result.passed is False
        assert "not 'spec'" in result.reason

    @pytest.mark.asyncio
    async def test_missing_metadata_phases(self, db: Any) -> None:
        """Spec with empty metadata should fail gracefully."""
        from anteroom.services import artifact_storage
        from anteroom.services.workflow_engine import get_gate_condition

        artifact_storage.create_artifact(
            db,
            "@ns/spec/bare",
            "spec",
            "ns",
            "bare",
            "requirements: r\ndesign: d\ntasks:\n  - id: t1\n    summary: s\n",
            metadata={},
        )
        fn = get_gate_condition("spec_requirements_approved")
        result = await fn({}, None, {"spec_fqn": "@ns/spec/bare"})
        assert result.passed is False
        assert "'draft'" in result.reason


# ---------------------------------------------------------------------------
# GateResult backward compatibility in engine
# ---------------------------------------------------------------------------


class TestGateResultBackwardCompat:
    @pytest.mark.asyncio
    async def test_bool_true_still_works(self, db: Any) -> None:
        """Existing bool-returning gate conditions must still work."""
        from anteroom.services.workflow_engine import register_gate_condition

        async def always_pass(run: dict, step: Any, inputs: dict) -> bool:
            return True

        register_gate_condition("test_bool_pass", always_pass)

        from anteroom.services.workflow_engine import get_gate_condition

        fn = get_gate_condition("test_bool_pass")
        result = await fn({}, None, {})
        assert result is True

    @pytest.mark.asyncio
    async def test_bool_false_still_works(self, db: Any) -> None:
        from anteroom.services.workflow_engine import register_gate_condition

        async def always_fail(run: dict, step: Any, inputs: dict) -> bool:
            return False

        register_gate_condition("test_bool_fail", always_fail)

        from anteroom.services.workflow_engine import get_gate_condition

        fn = get_gate_condition("test_bool_fail")
        result = await fn({}, None, {})
        assert result is False
