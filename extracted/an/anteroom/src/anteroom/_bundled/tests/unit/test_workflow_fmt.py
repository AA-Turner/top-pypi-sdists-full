"""Tests for shared workflow monitoring formatters."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from anteroom.cli.workflow_fmt import (
    STATUS_ICONS,
    format_duration_ms,
    format_duration_s,
    format_elapsed,
    render_diagnosis,
    render_run_header,
    render_step_line,
    status_color,
    status_icon,
)
from anteroom.services.workflow_diagnosis import Diagnosis, DiagnosisEvidence


class TestFormatDurationMs:
    def test_none(self) -> None:
        assert format_duration_ms(None) == "—"

    def test_zero(self) -> None:
        assert format_duration_ms(0) == "< 1s"

    def test_sub_second(self) -> None:
        assert format_duration_ms(500) == "< 1s"

    def test_one_second(self) -> None:
        assert format_duration_ms(1000) == "1s"

    def test_seconds_only(self) -> None:
        assert format_duration_ms(45_000) == "45s"

    def test_minutes_and_seconds(self) -> None:
        assert format_duration_ms(312_000) == "5m 12s"

    def test_exact_minutes(self) -> None:
        assert format_duration_ms(300_000) == "5m"

    def test_one_hour(self) -> None:
        assert format_duration_ms(3_600_000) == "1h"

    def test_hours_and_minutes(self) -> None:
        assert format_duration_ms(3_780_000) == "1h 3m"

    def test_large_duration(self) -> None:
        assert format_duration_ms(7_200_000) == "2h"


class TestFormatDurationS:
    def test_none(self) -> None:
        assert format_duration_s(None) == "—"

    def test_float_sub_second(self) -> None:
        assert format_duration_s(0.5) == "< 1s"

    def test_59_seconds(self) -> None:
        assert format_duration_s(59) == "59s"

    def test_60_seconds(self) -> None:
        assert format_duration_s(60) == "1m"

    def test_90_seconds(self) -> None:
        assert format_duration_s(90) == "1m 30s"


class TestFormatElapsed:
    def test_none(self) -> None:
        assert format_elapsed(None) == "—"

    def test_empty_string(self) -> None:
        assert format_elapsed("") == "—"

    def test_invalid_timestamp(self) -> None:
        assert format_elapsed("not-a-date") == "—"

    def test_recent_timestamp(self) -> None:
        now = datetime.now(timezone.utc)
        recent = (now - timedelta(seconds=65)).isoformat()
        result = format_elapsed(recent)
        assert "m" in result  # should be ~1m 5s

    def test_z_suffix(self) -> None:
        now = datetime.now(timezone.utc)
        ts = (now - timedelta(seconds=30)).isoformat().replace("+00:00", "Z")
        result = format_elapsed(ts)
        assert "s" in result


class TestStatusIcon:
    def test_known_statuses(self) -> None:
        for status in STATUS_ICONS:
            icon = status_icon(status)
            assert icon  # non-empty
            assert icon == STATUS_ICONS[status]

    def test_unknown_status(self) -> None:
        icon = status_icon("something_unknown")
        assert icon  # should return fallback

    @patch.dict("os.environ", {"NO_COLOR": "1"})
    def test_no_color_ascii_fallback(self) -> None:
        # Reimport to pick up env change
        import importlib

        import anteroom.cli.workflow_fmt as mod

        importlib.reload(mod)
        try:
            icon = mod.status_icon("completed")
            assert icon == "[OK]"
        finally:
            # Restore
            import os

            os.environ.pop("NO_COLOR", None)
            importlib.reload(mod)


class TestStatusColor:
    def test_known_statuses(self) -> None:
        assert status_color("completed") == "green"
        assert status_color("failed") == "red"
        assert status_color("running") == "cyan"
        assert status_color("pending") == "dim"

    def test_unknown_status(self) -> None:
        assert status_color("unknown") == "white"


class TestRenderStepLine:
    def test_completed_step(self) -> None:
        step = {
            "step_id": "prepare_issue",
            "status": "completed",
            "result_status": "success",
            "step_type": "runner",
            "runner_type": "shell",
            "duration_ms": 3200,
        }
        line = render_step_line(step)
        assert "✅" in line
        assert "prepare_issue" in line
        assert "3.2s" in line or "3s" in line
        assert "shell" in line

    def test_running_step(self) -> None:
        step = {
            "step_id": "draft_plan_r1",
            "status": "running",
            "result_status": None,
            "step_type": "runner",
            "runner_type": "python_script",
            "duration_ms": 154_000,
        }
        line = render_step_line(step)
        assert "●" in line
        assert "draft_plan_r1" in line
        assert "python_script" in line

    def test_pending_step(self) -> None:
        step = {
            "step_id": "review_plan_r1",
            "status": "pending",
            "step_type": "runner",
            "runner_type": "python_script",
        }
        line = render_step_line(step)
        assert "○" in line
        assert "review_plan_r1" in line

    def test_skipped_step(self) -> None:
        step = {
            "step_id": "review_plan_r1",
            "status": "skipped",
            "result_status": "skipped",
            "step_type": "runner",
            "runner_type": "python_script",
        }
        line = render_step_line(step)
        assert "⏭" in line
        assert "(skipped)" in line

    def test_failed_step(self) -> None:
        step = {
            "step_id": "draft_plan_r1",
            "status": "failed",
            "result_status": "failed",
            "step_type": "runner",
            "runner_type": "python_script",
            "duration_ms": 5000,
        }
        line = render_step_line(step)
        assert "❌" in line

    def test_cached_annotation(self) -> None:
        step = {
            "step_id": "llm_step",
            "status": "completed",
            "result_status": "success",
            "step_type": "llm",
            "duration_ms": 100,
            "result_artifacts": {"cache_hit": True},
        }
        line = render_step_line(step)
        assert "(cached)" in line

    def test_fallback_annotation(self) -> None:
        step = {
            "step_id": "llm_step",
            "status": "completed",
            "result_status": "success",
            "step_type": "llm",
            "duration_ms": 2000,
            "result_artifacts": {"fallback_used": True, "model": "gpt-4o-mini"},
        }
        line = render_step_line(step)
        assert "(fallback: gpt-4o-mini)" in line


class TestRenderDiagnosis:
    def test_multiline_evidence_is_indented_and_labeled(self) -> None:
        diagnosis = Diagnosis(
            category="runner_failure",
            what="Step prepare_issue failed",
            why="The step tried to write under `.git/...` in a linked worktree.",
            evidence=[
                DiagnosisEvidence(
                    source="exception",
                    content=(
                        "NotADirectoryError: [Errno 20] Not a directory\n"
                        "while creating /repo/.git/anteroom-workflows/issue-1092"
                    ),
                    location="prepare_issue",
                )
            ],
            next_actions=["Run from the main checkout."],
        )
        rendered = render_diagnosis(diagnosis)
        assert "exception (prepare_issue)" in rendered
        assert "NotADirectoryError" in rendered
        assert "while creating /repo/.git/anteroom-workflows/issue-1092" in rendered

    def test_indent(self) -> None:
        step = {
            "step_id": "nested_step",
            "status": "completed",
            "result_status": "success",
            "step_type": "runner",
            "duration_ms": 1000,
        }
        line = render_step_line(step, indent=1)
        assert line.startswith("  ")

    def test_compensation_annotation(self) -> None:
        step = {
            "step_id": "rollback_deploy",
            "status": "completed",
            "result_status": "success",
            "step_type": "runner",
            "duration_ms": 500,
            "is_compensation": True,
        }
        line = render_step_line(step)
        assert "(compensation)" in line


class TestRenderRunHeader:
    def test_running_run(self) -> None:
        now = datetime.now(timezone.utc)
        run = {
            "id": "20b3119a-5d73-4135-aaa4-b4f618ca0b49",
            "workflow_id": "local_claude_codex_issue_delivery",
            "status": "running",
            "started_at": (now - timedelta(seconds=312)).isoformat(),
        }
        header = render_run_header(run, step_count=3, total_steps=8)
        assert "local_claude_codex_issue_delivery" in header
        assert "●" in header
        assert "running" in header
        assert "20b3119a" in header
        assert "Steps: 3/8" in header

    def test_completed_run(self) -> None:
        start = datetime(2026, 3, 22, 10, 0, 0, tzinfo=timezone.utc)
        end = datetime(2026, 3, 22, 10, 12, 45, tzinfo=timezone.utc)
        run = {
            "id": "abc12345-xxxx",
            "workflow_id": "test_workflow",
            "status": "completed",
            "started_at": start.isoformat(),
            "completed_at": end.isoformat(),
        }
        header = render_run_header(run)
        assert "✅" in header
        assert "12m 45s" in header

    def test_no_timing(self) -> None:
        run = {
            "id": "abc12345-xxxx",
            "workflow_id": "test_workflow",
            "status": "pending",
        }
        header = render_run_header(run)
        assert "○" in header
        assert "—" in header


class TestRenderStepLineLoopEndReason:
    """Tests for loop_end_reason annotations in render_step_line (#1125, #1130)."""

    def test_until_met_annotation(self) -> None:
        step = {
            "step_id": "repair_loop",
            "status": "completed",
            "result_status": "success",
            "step_type": "loop",
            "duration_ms": 5000,
            "result_artifacts": {"loop_end_reason": "until_met"},
        }
        line = render_step_line(step)
        assert "(until met)" in line

    def test_until_not_met_annotation(self) -> None:
        step = {
            "step_id": "repair_loop",
            "status": "failed",
            "result_status": "failed",
            "step_type": "loop",
            "duration_ms": 15000,
            "result_artifacts": {"loop_end_reason": "until_not_met"},
        }
        line = render_step_line(step)
        assert "(until not met)" in line

    def test_break_when_annotation(self) -> None:
        step = {
            "step_id": "repair_loop",
            "status": "completed",
            "result_status": "success",
            "step_type": "loop",
            "duration_ms": 3000,
            "result_artifacts": {"loop_end_reason": "break_when"},
        }
        line = render_step_line(step)
        assert "(break condition)" in line

    def test_exhausted_annotation(self) -> None:
        step = {
            "step_id": "repair_loop",
            "status": "completed",
            "result_status": "success",
            "step_type": "loop",
            "duration_ms": 10000,
            "result_artifacts": {"loop_end_reason": "exhausted"},
        }
        line = render_step_line(step)
        assert "(exhausted)" in line

    def test_no_progress_annotation(self) -> None:
        step = {
            "step_id": "repair_loop",
            "status": "failed",
            "result_status": "failed",
            "step_type": "loop",
            "duration_ms": 8000,
            "result_artifacts": {"loop_end_reason": "no_progress"},
        }
        line = render_step_line(step)
        assert "(no progress)" in line

    def test_all_succeeded_no_annotation(self) -> None:
        step = {
            "step_id": "repair_loop",
            "status": "completed",
            "result_status": "success",
            "step_type": "loop",
            "duration_ms": 2000,
            "result_artifacts": {"loop_end_reason": "all_succeeded"},
        }
        line = render_step_line(step)
        assert "(until" not in line
        assert "(break" not in line
        assert "(exhausted)" not in line

    def test_no_artifacts_no_annotation(self) -> None:
        step = {
            "step_id": "repair_loop",
            "status": "completed",
            "result_status": "success",
            "step_type": "loop",
            "duration_ms": 2000,
        }
        line = render_step_line(step)
        assert "(until" not in line
        assert "(break" not in line
        assert "(exhausted)" not in line


class TestRenderStepLineOutputs:
    """Tests for structured output annotations in render_step_line (#1131)."""

    def test_outputs_annotation_single(self) -> None:
        step = {
            "step_id": "generate",
            "status": "completed",
            "result_status": "success",
            "step_type": "runner",
            "duration_ms": 3000,
            "result_outputs": {"exit_code": "0"},
        }
        line = render_step_line(step)
        assert "[1 output]" in line

    def test_outputs_annotation_multiple(self) -> None:
        step = {
            "step_id": "generate",
            "status": "completed",
            "result_status": "success",
            "step_type": "runner",
            "duration_ms": 3000,
            "result_outputs": {"exit_code": "0", "report_path": "/tmp/report.json"},
        }
        line = render_step_line(step)
        assert "[2 outputs]" in line

    def test_no_outputs_no_annotation(self) -> None:
        step = {
            "step_id": "generate",
            "status": "completed",
            "result_status": "success",
            "step_type": "runner",
            "duration_ms": 3000,
        }
        line = render_step_line(step)
        assert "output" not in line.lower()

    def test_empty_outputs_no_annotation(self) -> None:
        step = {
            "step_id": "generate",
            "status": "completed",
            "result_status": "success",
            "step_type": "runner",
            "duration_ms": 3000,
            "result_outputs": {},
        }
        line = render_step_line(step)
        assert "output" not in line.lower()


class TestRenderStepLineEmit:
    """Tests for emit step rendering (#1150)."""

    def test_emit_step_shows_emit_runner(self) -> None:
        step = {
            "step_id": "notify",
            "step_type": "emit",
            "status": "completed",
            "result_status": "success",
            "duration_ms": 0,
        }
        line = render_step_line(step)
        assert "emit" in line

    def test_emit_step_without_runner_type(self) -> None:
        step = {
            "step_id": "msg",
            "step_type": "emit",
            "runner_type": None,
            "status": "completed",
            "result_status": "success",
        }
        line = render_step_line(step)
        assert "emit" in line
