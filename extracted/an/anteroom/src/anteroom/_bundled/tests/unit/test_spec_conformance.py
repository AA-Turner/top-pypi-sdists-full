"""Tests for spec conformance checks (#1017)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

from anteroom.services.spec_conformance import (
    ConformanceSeverity,
    run_conformance_check,
)
from anteroom.services.spec_schema import SpecContent, SpecTask

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SPEC_YAML = (
    'requirements: "req"\ndesign: "des"\ntasks:\n  - id: t1\n    summary: task one\n  - id: t2\n    summary: task two\n'
)

_SPEC = SpecContent(
    requirements="req",
    design="des",
    tasks=[
        SpecTask(id="t1", summary="task one"),
        SpecTask(id="t2", summary="task two"),
    ],
)

_SINGLE_TASK_YAML = 'requirements: "req"\ndesign: "des"\ntasks:\n  - id: t1\n    summary: task one\n'

_SINGLE_TASK_SPEC = SpecContent(
    requirements="req",
    design="des",
    tasks=[SpecTask(id="t1", summary="task one")],
)


def _make_art(
    fqn: str = "ns/spec/test",
    phases: dict[str, Any] | None = None,
    content: str = _SPEC_YAML,
    **kwargs: Any,
) -> dict[str, Any]:
    default_phases: dict[str, Any] = {
        "requirements": {"status": "approved", "approved_at": "2026-01-01T00:00:00", "approved_by": None},
        "design": {"status": "approved", "approved_at": "2026-01-01T00:00:00", "approved_by": None},
        "tasks": {"status": "approved", "approved_at": "2026-01-01T00:00:00", "approved_by": None},
    }
    if phases:
        default_phases.update(phases)
    return {
        "id": "art-1",
        "fqn": fqn,
        "type": "spec",
        "content": content,
        "metadata": {"phases": default_phases},
        "updated_at": "2026-01-01T00:00:00",
        **kwargs,
    }


def _make_run(
    task_id: str = "t1",
    status: str = "completed",
    completed_at: str = "2026-06-01T00:00:00",
    run_id: str = "run-1",
    **kwargs: Any,
) -> dict[str, Any]:
    return {"id": run_id, "task_id": task_id, "status": status, "completed_at": completed_at, **kwargs}


# Patch targets — these are imported locally inside run_conformance_check,
# so we patch them at their source modules.
_P_GET_SPEC = "anteroom.services.spec_service.get_spec"
_P_VERSIONS = "anteroom.services.artifact_storage.list_artifact_versions"
_P_RUNS = "anteroom.services.workflow_storage.list_runs_by_spec"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestSpecNotFound:
    def test_spec_not_found(self) -> None:
        db = MagicMock()
        with patch(_P_GET_SPEC, return_value=None):
            result = run_conformance_check(db, "ns/spec/missing")
        assert result is None


class TestTaskCoverage:
    def test_empty_spec_no_runs(self) -> None:
        art = _make_art()
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=[]),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        coverage = [f for f in result.findings if f.category == "task_coverage"]
        assert len(coverage) == 2
        assert all(f.severity == ConformanceSeverity.ERROR for f in coverage)
        assert coverage[0].task_id == "t1"
        assert coverage[1].task_id == "t2"
        assert coverage[0].details == {"completed_runs": 0}

    def test_all_tasks_covered(self) -> None:
        art = _make_art()
        runs = [
            _make_run(task_id="t1", run_id="r1"),
            _make_run(task_id="t2", run_id="r2"),
        ]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        coverage = [f for f in result.findings if f.category == "task_coverage"]
        assert all(f.severity == ConformanceSeverity.INFO for f in coverage)
        assert result.conformant is True

    def test_partial_coverage(self) -> None:
        art = _make_art()
        runs = [_make_run(task_id="t1", run_id="r1")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        coverage = [f for f in result.findings if f.category == "task_coverage"]
        t1 = [f for f in coverage if f.task_id == "t1"]
        t2 = [f for f in coverage if f.task_id == "t2"]
        assert t1[0].severity == ConformanceSeverity.INFO
        assert t1[0].details == {"completed_runs": 1}
        assert t2[0].severity == ConformanceSeverity.ERROR
        assert t2[0].details == {"completed_runs": 0}


class TestRunHealth:
    def test_failed_run_produces_error(self) -> None:
        art = _make_art(content=_SINGLE_TASK_YAML)
        runs = [_make_run(task_id="t1", status="failed", run_id="r-fail")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SINGLE_TASK_SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        health = [f for f in result.findings if f.category == "run_health"]
        assert len(health) == 1
        assert health[0].severity == ConformanceSeverity.ERROR
        assert "r-fail" in health[0].message
        assert health[0].details["status"] == "failed"

    def test_blocked_run_produces_info(self) -> None:
        """Blocked runs are resumable wait states, not failures — INFO not WARNING."""
        art = _make_art(content=_SINGLE_TASK_YAML)
        runs = [_make_run(task_id="t1", status="blocked", run_id="r-block")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SINGLE_TASK_SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        health = [f for f in result.findings if f.category == "run_health"]
        assert len(health) == 1
        assert health[0].severity == ConformanceSeverity.INFO
        assert health[0].details["status"] == "blocked"

    def test_cancelled_run_produces_warning(self) -> None:
        art = _make_art(content=_SINGLE_TASK_YAML)
        runs = [_make_run(task_id="t1", status="cancelled", run_id="r-cancel")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SINGLE_TASK_SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        health = [f for f in result.findings if f.category == "run_health"]
        assert len(health) == 1
        assert health[0].severity == ConformanceSeverity.WARNING
        assert health[0].details["status"] == "cancelled"


class TestPhaseStatus:
    def test_stale_phase_produces_warning(self) -> None:
        art = _make_art(
            phases={
                "design": {"status": "stale", "approved_at": "2026-01-01T00:00:00", "approved_by": None},
            }
        )
        runs = [_make_run(task_id="t1", run_id="r1"), _make_run(task_id="t2", run_id="r2")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        phase_findings = [f for f in result.findings if f.category == "phase_status"]
        assert len(phase_findings) == 1
        assert phase_findings[0].severity == ConformanceSeverity.WARNING
        assert phase_findings[0].details["phase"] == "design"
        assert phase_findings[0].details["status"] == "stale"

    def test_draft_phase_produces_info(self) -> None:
        art = _make_art(
            phases={
                "requirements": {"status": "draft", "approved_at": None, "approved_by": None},
            }
        )
        runs = [_make_run(task_id="t1", run_id="r1"), _make_run(task_id="t2", run_id="r2")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        phase_findings = [f for f in result.findings if f.category == "phase_status"]
        assert len(phase_findings) == 1
        assert phase_findings[0].severity == ConformanceSeverity.INFO
        assert phase_findings[0].details["phase"] == "requirements"

    def test_all_approved_no_phase_findings(self) -> None:
        art = _make_art()
        runs = [_make_run(task_id="t1", run_id="r1"), _make_run(task_id="t2", run_id="r2")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        phase_findings = [f for f in result.findings if f.category == "phase_status"]
        assert len(phase_findings) == 0


class TestTemporalValidity:
    def test_temporal_run_before_approval(self) -> None:
        art = _make_art(
            phases={
                "tasks": {"status": "approved", "approved_at": "2026-07-01T00:00:00", "approved_by": None},
            }
        )
        runs = [_make_run(task_id="t1", completed_at="2026-06-01T00:00:00", run_id="r-early")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SINGLE_TASK_SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        temporal = [f for f in result.findings if f.category == "temporal"]
        assert len(temporal) == 1
        assert temporal[0].severity == ConformanceSeverity.WARNING
        assert "r-early" in temporal[0].message
        assert temporal[0].details["run_completed"] == "2026-06-01T00:00:00"
        assert temporal[0].details["tasks_approved"] == "2026-07-01T00:00:00"

    def test_temporal_run_after_approval(self) -> None:
        art = _make_art()
        runs = [_make_run(task_id="t1", completed_at="2026-06-01T00:00:00", run_id="r1")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SINGLE_TASK_SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        temporal = [f for f in result.findings if f.category == "temporal"]
        assert len(temporal) == 0

    def test_temporal_no_approval_yet(self) -> None:
        art = _make_art(
            phases={
                "tasks": {"status": "draft", "approved_at": None, "approved_by": None},
            }
        )
        runs = [_make_run(task_id="t1", run_id="r1")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SINGLE_TASK_SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        temporal = [f for f in result.findings if f.category == "temporal"]
        assert len(temporal) == 1
        assert temporal[0].severity == ConformanceSeverity.INFO
        assert "not yet approved" in temporal[0].message


class TestConformanceProperty:
    def test_conformant_true(self) -> None:
        art = _make_art()
        runs = [
            _make_run(task_id="t1", run_id="r1"),
            _make_run(task_id="t2", run_id="r2"),
        ]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        assert result.conformant is True

    def test_conformant_false(self) -> None:
        art = _make_art()
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 1}]),
            patch(_P_RUNS, return_value=[]),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        assert result.conformant is False
        errors = [f for f in result.findings if f.severity == ConformanceSeverity.ERROR]
        assert len(errors) >= 1


class TestSerialization:
    def test_to_dict_serialization(self) -> None:
        art = _make_art()
        runs = [_make_run(task_id="t1", run_id="r1")]
        db = MagicMock()
        with (
            patch(_P_GET_SPEC, return_value=(art, _SPEC)),
            patch(_P_VERSIONS, return_value=[{"version": 2}]),
            patch(_P_RUNS, return_value=runs),
        ):
            result = run_conformance_check(db, "ns/spec/test")

        assert result is not None
        d = result.to_dict()
        assert d["spec_fqn"] == "ns/spec/test"
        assert d["spec_version"] == 2
        assert isinstance(d["checked_at"], str)
        assert isinstance(d["conformant"], bool)
        assert isinstance(d["findings"], list)
        for f in d["findings"]:
            assert "severity" in f
            assert "category" in f
            assert "message" in f
            assert "task_id" in f
            assert "details" in f
            assert f["severity"] in ("error", "warning", "info")
