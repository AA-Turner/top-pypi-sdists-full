"""Tests for spec portfolio dashboard (#1016)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

from anteroom.services.spec_dashboard import _derive_overall_status, get_spec_dashboard

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_artifact(
    fqn: str,
    *,
    req: str = "draft",
    des: str = "draft",
    tasks: str = "draft",
    namespace: str = "ns",
    source: str = "local",
    updated_at: str = "2026-01-01T00:00:00",
    content: str = "mode: feature\nrequirements: r\ndesign: d\ntasks: []",
) -> dict[str, Any]:
    return {
        "id": f"art-{fqn}",
        "fqn": fqn,
        "type": "spec",
        "namespace": namespace,
        "name": fqn.split("/")[-1] if "/" in fqn else fqn,
        "content": content,
        "source": source,
        "metadata": {
            "phases": {
                "requirements": {"status": req, "approved_at": None, "approved_by": None},
                "design": {"status": des, "approved_at": None, "approved_by": None},
                "tasks": {"status": tasks, "approved_at": None, "approved_by": None},
            }
        },
        "updated_at": updated_at,
        "created_at": updated_at,
    }


_NO_RUNS: dict[str, int] = {"total": 0, "completed": 0, "failed": 0, "running": 0, "blocked": 0}


def _dashboard(
    artifacts: list[dict[str, Any]],
    run_counts: dict[str, int] | None = None,
    stale_reason: str | None = None,
    **kwargs: Any,
) -> Any:
    with (
        patch(
            "anteroom.services.spec_dashboard.artifact_storage.list_artifacts",
            return_value=artifacts,
        ),
        patch(
            "anteroom.services.spec_dashboard.workflow_storage.count_runs_by_spec",
            return_value=run_counts or _NO_RUNS,
        ),
        patch(
            "anteroom.services.spec_dashboard.derive_stale_reason",
            return_value=stale_reason,
        ),
    ):
        return get_spec_dashboard(MagicMock(), **kwargs)


# ---------------------------------------------------------------------------
# Tests — _derive_overall_status
# ---------------------------------------------------------------------------


class TestDeriveOverallStatus:
    def test_blocked_highest_priority(self) -> None:
        assert (
            _derive_overall_status(
                {"requirements": "approved", "design": "approved", "tasks": "approved"},
                {"blocked": 1},
            )
            == "blocked"
        )

    def test_stale_over_draft(self) -> None:
        assert (
            _derive_overall_status(
                {"requirements": "stale", "design": "draft", "tasks": "draft"},
                _NO_RUNS,
            )
            == "stale"
        )

    def test_all_draft(self) -> None:
        assert (
            _derive_overall_status(
                {"requirements": "draft", "design": "draft", "tasks": "draft"},
                _NO_RUNS,
            )
            == "draft"
        )

    def test_all_approved(self) -> None:
        assert (
            _derive_overall_status(
                {"requirements": "approved", "design": "approved", "tasks": "approved"},
                _NO_RUNS,
            )
            == "all_approved"
        )

    def test_in_progress(self) -> None:
        assert (
            _derive_overall_status(
                {"requirements": "approved", "design": "draft", "tasks": "draft"},
                _NO_RUNS,
            )
            == "in_progress"
        )

    def test_blocked_over_stale(self) -> None:
        assert (
            _derive_overall_status(
                {"requirements": "stale", "design": "draft", "tasks": "draft"},
                {"blocked": 2},
            )
            == "blocked"
        )


# ---------------------------------------------------------------------------
# Tests — get_spec_dashboard
# ---------------------------------------------------------------------------


class TestGetSpecDashboard:
    def test_empty_dashboard(self) -> None:
        result = _dashboard([])
        assert result.totals.total_specs == 0
        assert result.specs == []

    def test_single_spec_all_draft(self) -> None:
        art = _make_artifact("@ns/spec/foo")
        result = _dashboard([art])
        assert len(result.specs) == 1
        assert result.specs[0].overall_status == "draft"
        assert result.totals.draft == 1

    def test_single_spec_all_approved(self) -> None:
        art = _make_artifact("@ns/spec/foo", req="approved", des="approved", tasks="approved")
        result = _dashboard([art])
        assert result.specs[0].overall_status == "all_approved"
        assert result.totals.all_approved == 1

    def test_stale_spec_status(self) -> None:
        art = _make_artifact("@ns/spec/foo", req="approved", des="stale", tasks="draft")
        result = _dashboard([art], stale_reason="design changed after approval")
        assert result.specs[0].overall_status == "stale"
        assert result.specs[0].stale_reasons["design"] == "design changed after approval"
        assert result.totals.stale == 1

    def test_blocked_spec_status(self) -> None:
        art = _make_artifact("@ns/spec/foo", req="approved", des="approved", tasks="approved")
        result = _dashboard(
            [art],
            run_counts={"total": 3, "completed": 1, "failed": 0, "running": 0, "blocked": 1},
        )
        assert result.specs[0].overall_status == "blocked"
        assert result.totals.blocked == 1

    def test_in_progress_status(self) -> None:
        art = _make_artifact("@ns/spec/foo", req="approved", des="draft", tasks="draft")
        result = _dashboard([art])
        assert result.specs[0].overall_status == "in_progress"
        assert result.totals.in_progress == 1

    def test_filter_by_status(self) -> None:
        arts = [
            _make_artifact("@ns/spec/a", req="approved", des="approved", tasks="approved"),
            _make_artifact("@ns/spec/b"),  # all draft
        ]
        result = _dashboard(arts, status="draft")
        assert len(result.specs) == 1
        assert result.specs[0].fqn == "@ns/spec/b"
        assert result.filters_applied["status"] == "draft"

    def test_filter_by_namespace(self) -> None:
        arts = [
            _make_artifact("@team/spec/a", namespace="team"),
            _make_artifact("@other/spec/b", namespace="other"),
        ]
        result = _dashboard(arts, namespace="team")
        assert len(result.specs) == 1
        assert result.specs[0].fqn == "@team/spec/a"

    def test_filter_by_has_runs_true(self) -> None:
        arts = [_make_artifact("@ns/spec/a")]
        result = _dashboard(
            arts,
            run_counts={"total": 2, "completed": 1, "failed": 0, "running": 0, "blocked": 0},
            has_runs=True,
        )
        assert len(result.specs) == 1

    def test_filter_by_has_runs_false(self) -> None:
        arts = [_make_artifact("@ns/spec/a")]
        result = _dashboard(
            arts,
            run_counts={"total": 2, "completed": 1, "failed": 0, "running": 0, "blocked": 0},
            has_runs=False,
        )
        assert len(result.specs) == 0

    def test_run_summary_aggregation(self) -> None:
        art = _make_artifact("@ns/spec/a")
        counts = {"total": 5, "completed": 3, "failed": 1, "running": 1, "blocked": 0}
        result = _dashboard([art], run_counts=counts)
        rs = result.specs[0].run_summary
        assert rs.total == 5
        assert rs.completed == 3
        assert rs.failed == 1
        assert rs.running == 1

    def test_dashboard_totals(self) -> None:
        arts = [
            _make_artifact("@ns/spec/a", req="approved", des="approved", tasks="approved"),
            _make_artifact("@ns/spec/b"),  # all draft
            _make_artifact("@ns/spec/c", req="approved", des="stale", tasks="draft"),
        ]
        result = _dashboard(arts)
        assert result.totals.total_specs == 3
        assert result.totals.all_approved == 1
        assert result.totals.draft == 1
        assert result.totals.stale == 1

    def test_to_dict_serialization(self) -> None:
        art = _make_artifact("@ns/spec/a")
        result = _dashboard([art])
        d = result.to_dict()
        assert "specs" in d
        assert "totals" in d
        assert "filters_applied" in d
        assert len(d["specs"]) == 1
        spec_dict = d["specs"][0]
        assert spec_dict["fqn"] == "@ns/spec/a"
        assert "run_summary" in spec_dict

    def test_bugfix_mode_detection(self) -> None:
        art = _make_artifact(
            "@ns/spec/a",
            content="mode: bugfix\nrequirements: r\ndesign: d\ntasks: []",
        )
        result = _dashboard([art])
        assert result.specs[0].mode == "bugfix"

    def test_no_runs_returns_zero_summary(self) -> None:
        art = _make_artifact("@ns/spec/a")
        result = _dashboard([art])
        rs = result.specs[0].run_summary
        assert rs.total == 0
        assert rs.completed == 0

    def test_filter_by_phase_and_phase_status(self) -> None:
        arts = [
            _make_artifact("@ns/spec/a", req="approved", des="draft", tasks="draft"),
            _make_artifact("@ns/spec/b", req="draft", des="draft", tasks="draft"),
        ]
        result = _dashboard(arts, phase="requirements", phase_status="approved")
        assert len(result.specs) == 1
        assert result.specs[0].fqn == "@ns/spec/a"
        assert result.filters_applied["phase"] == "requirements"
        assert result.filters_applied["phase_status"] == "approved"

    def test_filter_by_phase_status_no_match(self) -> None:
        arts = [_make_artifact("@ns/spec/a", req="draft", des="draft", tasks="draft")]
        result = _dashboard(arts, phase="requirements", phase_status="approved")
        assert len(result.specs) == 0

    def test_filter_by_invalid_phase_excludes_all(self) -> None:
        arts = [_make_artifact("@ns/spec/a")]
        result = _dashboard(arts, phase="nonexistent", phase_status="draft")
        assert len(result.specs) == 0
