"""Spec artifact phase gate conditions for the workflow engine.

Registers three gate conditions that check whether a spec artifact's
requirements, design, or tasks phase is approved.  Gate conditions
read ``spec_fqn`` from top-level workflow inputs.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

from .spec_schema import SpecPhaseStatus, get_phase_status
from .workflow_engine import GateResult, register_gate_condition

logger = logging.getLogger(__name__)


def register_spec_gates(db: ThreadSafeConnection) -> None:
    """Register all spec phase gate conditions.

    Uses a closure over *db* so gate condition functions can read
    artifact metadata without requiring DB access via the run dict.
    """
    register_gate_condition(
        "spec_requirements_approved",
        _make_phase_gate(db, "requirements"),
    )
    register_gate_condition(
        "spec_design_approved",
        _make_phase_gate(db, "design"),
    )
    register_gate_condition(
        "spec_tasks_approved",
        _make_phase_gate(db, "tasks"),
    )
    logger.debug("Registered spec phase gate conditions")


def _make_phase_gate(db: ThreadSafeConnection, phase: str) -> Any:
    """Return an async gate condition function that checks a spec phase status."""

    async def _check(run: dict[str, Any], step_def: Any, inputs: dict[str, Any]) -> GateResult:
        spec_fqn = inputs.get("spec_fqn")
        if not spec_fqn:
            return GateResult(passed=False, reason="No 'spec_fqn' in workflow inputs")

        from . import artifact_storage

        art = artifact_storage.get_artifact_by_fqn(db, spec_fqn)
        if art is None:
            return GateResult(passed=False, reason=f"Spec artifact '{spec_fqn}' not found")

        if art["type"] != "spec":
            return GateResult(passed=False, reason=f"Artifact '{spec_fqn}' is type '{art['type']}', not 'spec'")

        # Derive attachment context from the workflow run, then inputs
        _gate_space_id = run.get("space_id") or inputs.get("space_id")
        _gate_project_path: str | None = None
        if _gate_space_id:
            try:
                from .space_storage import get_space_local_dirs

                _local_dirs = get_space_local_dirs(db, _gate_space_id)
                if _local_dirs:
                    _gate_project_path = _local_dirs[0]
            except Exception:
                pass
        if not _gate_project_path:
            _gate_project_path = inputs.get("project_path")

        # Check if artifact is from a detached pack
        if not artifact_storage.is_artifact_attached(
            db, art["id"], space_id=_gate_space_id, project_path=_gate_project_path
        ):
            return GateResult(passed=False, reason=f"Spec '{spec_fqn}' is from a detached pack")

        metadata = art.get("metadata", {})
        try:
            status = get_phase_status(metadata, phase)
        except ValueError:
            return GateResult(passed=False, reason=f"Invalid phase '{phase}' on spec '{spec_fqn}'")

        if status == SpecPhaseStatus.APPROVED:
            return GateResult(passed=True)

        return GateResult(
            passed=False,
            reason=f"Phase '{phase}' is '{status.value}' for {spec_fqn}",
        )

    return _check
