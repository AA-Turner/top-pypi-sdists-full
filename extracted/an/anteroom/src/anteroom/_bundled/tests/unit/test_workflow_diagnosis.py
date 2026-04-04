"""Tests for workflow diagnosis engine (#1103)."""

from __future__ import annotations

from anteroom.services.workflow_diagnosis import diagnose, recovery_actions_for_run


def _run(status: str = "failed", stop_reason: str = "", **extra: object) -> dict:
    return {"id": "abc12345-xxxx", "status": status, "stop_reason": stop_reason, **extra}


def _step(step_id: str, status: str = "completed", result_status: str = "success", **extra: object) -> dict:
    return {"step_id": step_id, "status": status, "result_status": result_status, **extra}


class TestStepFailure:
    def test_basic_step_failure(self) -> None:
        run = _run(stop_reason="step_failed:draft_plan_r1")
        steps = [
            _step("prepare_issue"),
            _step("draft_plan_r1", status="failed", result_status="failed", result_summary="Command failed: claude -C"),
        ]
        dx = diagnose(run, steps, [])
        assert dx.category == "runner_failure"
        assert "draft_plan_r1" in dx.what
        assert "claude" in dx.why.lower() or "Command failed" in dx.why
        assert dx.confidence == "high"
        assert any("resume" in a for a in dx.next_actions)

    def test_step_failure_with_findings(self) -> None:
        run = _run(stop_reason="step_failed:checks")
        steps = [
            _step(
                "checks",
                status="failed",
                result_status="failed",
                result_summary="Exit code 1",
                result_findings=[{"type": "stderr", "content": "ruff found 3 errors"}],
            ),
        ]
        dx = diagnose(run, steps, [])
        assert dx.category == "runner_failure"
        assert any("ruff" in e.content for e in dx.evidence)

    def test_traceback_extracts_real_exception_and_frame(self) -> None:
        run = _run(stop_reason="step_failed:prepare_issue")
        summary = """Traceback (most recent call last):
  File "/repo/scripts/local_cli_issue_flow.py", line 663, in <module>
    raise SystemExit(main())
  File "/repo/scripts/local_cli_issue_flow.py", line 98, in save_state
    path.parent.mkdir(parents=True, exist_ok=True)
NotADirectoryError: [Errno 20] Not a directory: '/repo/.git/anteroom-workflows/issue-1092'
"""
        steps = [
            _step(
                "prepare_issue",
                status="failed",
                result_status="failed",
                result_summary=summary,
            ),
        ]
        dx = diagnose(run, steps, [])
        assert dx.category == "runner_failure"
        assert "linked git worktree" in dx.why.lower()
        assert any(ev.source == "exception" and "NotADirectoryError" in ev.content for ev in dx.evidence)
        assert any(ev.source == "traceback_frame" and "save_state" in ev.content for ev in dx.evidence)
        assert any("git rev-parse --git-dir" in action for action in dx.next_actions)

    def test_uses_raw_output_excerpt_when_summary_is_generic(self) -> None:
        run = _run(stop_reason="step_failed:prepare_issue")
        steps = [
            _step(
                "prepare_issue",
                status="failed",
                result_status="failed",
                result_summary="Exit code 1",
                _diagnosis_output_excerpt=(
                    "Traceback (most recent call last):\n"
                    '  File "/repo/script.py", line 10, in <module>\n'
                    "    main()\n"
                    "FileNotFoundError: [Errno 2] No such file or directory: '/tmp/missing'\n"
                ),
            ),
        ]
        dx = diagnose(run, steps, [])
        assert "FileNotFoundError" in dx.why
        assert any(ev.source == "raw_output" for ev in dx.evidence) or any(
            ev.source == "exception" for ev in dx.evidence
        )

    def test_command_failed_summary_surfaces_nested_detail(self) -> None:
        run = _run(stop_reason="step_failed:checks")
        steps = [
            _step(
                "checks",
                status="failed",
                result_status="failed",
                result_summary="Command failed: ruff check src/ tests/\nRuff found 3 errors",
            ),
        ]
        dx = diagnose(run, steps, [])
        assert dx.category == "runner_failure"
        assert dx.why == "Ruff found 3 errors"
        assert any(ev.source == "command" and "ruff check" in ev.content for ev in dx.evidence)

    def test_step_not_found(self) -> None:
        run = _run(stop_reason="step_failed:missing_step")
        dx = diagnose(run, [], [])
        assert dx.category == "runner_failure"
        assert "missing_step" in dx.what


class TestGateBlock:
    def test_blocked_at_gate(self) -> None:
        run = _run(status="blocked", stop_reason="blocked_plan_not_approved", current_step_id="gate_plan_approved")
        steps = [
            _step(
                "gate_plan_approved",
                status="completed",
                result_status="blocked",
                result_summary="blocked_plan_not_approved",
            ),
        ]
        dx = diagnose(run, steps, [])
        assert dx.category == "gate_block"
        assert "gate_plan_approved" in dx.what
        assert "plan not approved" in dx.why.lower()
        assert any("gate" in a.lower() or "condition" in a.lower() for a in dx.next_actions)

    def test_blocked_at_explicit(self) -> None:
        run = _run(status="blocked", stop_reason="blocked_at:gate_ready")
        dx = diagnose(run, [], [])
        assert dx.category == "gate_block"
        assert "gate_ready" in dx.what

    def test_gate_block_suggests_resume_and_cancel(self) -> None:
        """Gate block diagnosis suggests both resume and cancel (#1141)."""
        run = _run(status="blocked", stop_reason="blocked_at:gate_ready")
        dx = diagnose(run, [], [])
        assert any("resume" in a for a in dx.next_actions)
        assert any("cancel" in a for a in dx.next_actions)


class TestBudget:
    def test_budget_exceeded(self) -> None:
        run = _run(
            stop_reason="budget_exceeded:tokens", budget={"max_tokens": 10000}, budget_usage={"total_tokens": 10500}
        )
        dx = diagnose(run, [], [])
        assert dx.category == "budget"
        assert "tokens" in dx.what
        assert any("repair" in a for a in dx.next_actions)


class TestCancel:
    def test_cancel_requested(self) -> None:
        run = _run(status="cancelled", stop_reason="cancel_requested")
        dx = diagnose(run, [], [])
        assert dx.category == "cancel"
        assert "cancelled" in dx.what.lower()

    def test_cancelled_status_no_reason(self) -> None:
        run = _run(status="cancelled", stop_reason="")
        dx = diagnose(run, [], [])
        assert dx.category == "cancel"


class TestApproval:
    def test_denied(self) -> None:
        run = _run(stop_reason="approval_denied: not ready")
        dx = diagnose(run, [], [])
        assert dx.category == "approval"
        assert "denied" in dx.what.lower()

    def test_expired(self) -> None:
        run = _run(stop_reason="approval_expired")
        dx = diagnose(run, [], [])
        assert dx.category == "approval"
        assert "expired" in dx.what.lower()


class TestEngineError:
    def test_unhandled_exception(self) -> None:
        run = _run(stop_reason="unhandled_exception", current_step_id="some_step")
        steps = [_step("some_step", status="failed", result_status="failed", result_summary="KeyError: 'foo'")]
        dx = diagnose(run, steps, [])
        assert dx.category == "engine_error"
        assert "exception" in dx.what.lower()

    def test_process_interrupted(self) -> None:
        run = _run(stop_reason="process_interrupted")
        dx = diagnose(run, [], [])
        assert dx.category == "engine_error"
        assert "interrupted" in dx.what.lower()


class TestConcurrency:
    def test_target_locked(self) -> None:
        run = _run(stop_reason="target_locked")
        dx = diagnose(run, [], [])
        assert dx.category == "concurrency"


class TestHumanGate:
    def test_timeout(self) -> None:
        run = _run(stop_reason="human_timeout")
        dx = diagnose(run, [], [])
        assert dx.category == "human_gate"

    def test_decision_expired(self) -> None:
        run = _run(stop_reason="human_decision_expired")
        dx = diagnose(run, [], [])
        assert dx.category == "human_gate"

    def test_operator_stopped(self) -> None:
        run = _run(stop_reason="operator_stopped")
        dx = diagnose(run, [], [])
        assert dx.category == "human_gate"


class TestCompensation:
    def test_compensation_failed(self) -> None:
        run = _run(stop_reason="compensation_failed:rollback_a,rollback_b")
        dx = diagnose(run, [], [])
        assert dx.category == "compensation"
        assert "rollback_a" in dx.what


class TestUnknown:
    def test_empty_stop_reason(self) -> None:
        run = _run(status="failed", stop_reason="")
        dx = diagnose(run, [], [])
        assert dx.category == "unknown"
        assert dx.confidence == "low"

    def test_unrecognized_reason(self) -> None:
        run = _run(stop_reason="something_new_and_unexpected")
        dx = diagnose(run, [], [])
        assert dx.category == "unknown"
        assert dx.confidence == "low"


class TestLoopUntilNotMet:
    """Tests for loop_until_not_met diagnosis category (#1125)."""

    def test_loop_until_not_met_diagnosis(self) -> None:
        run = _run(stop_reason="step_failed:repair_loop")
        steps = [
            _step(
                "repair_loop",
                status="failed",
                result_status="failed",
                result_summary="Loop exhausted 5 rounds without meeting until condition",
                result_artifacts={"loop_end_reason": "until_not_met"},
            ),
        ]
        dx = diagnose(run, steps, [])
        assert dx.category == "loop_until_not_met"
        assert "repair_loop" in dx.what
        assert dx.confidence == "high"
        assert any("max_rounds" in a for a in dx.next_actions)

    def test_loop_no_progress_diagnosis(self) -> None:
        run = _run(stop_reason="step_failed:repair_loop")
        steps = [
            _step(
                "repair_loop",
                status="failed",
                result_status="failed",
                result_summary="Loop stopped: no progress after 3 consecutive rounds with same failure",
                result_artifacts={"loop_end_reason": "no_progress"},
            ),
        ]
        dx = diagnose(run, steps, [])
        assert dx.category == "loop_no_progress"
        assert "repair_loop" in dx.what
        assert dx.confidence == "high"
        assert any("root cause" in a for a in dx.next_actions)

    def test_regular_step_failure_not_misdiagnosed_as_loop(self) -> None:
        run = _run(stop_reason="step_failed:deploy")
        steps = [
            _step(
                "deploy",
                status="failed",
                result_status="failed",
                result_summary="Command failed: deploy.sh",
            ),
        ]
        dx = diagnose(run, steps, [])
        assert dx.category == "runner_failure"
        assert dx.category != "loop_until_not_met"


class TestRecoveryActions:
    """Tests for recovery_actions_for_run (#1153)."""

    def test_recovery_actions_waiting_for_approval(self) -> None:
        run = _run(status="waiting_for_approval", stop_reason="")
        actions = recovery_actions_for_run(run, [], [])
        assert len(actions) == 2
        assert "approve" in actions[0].lower()
        assert "deny" in actions[1].lower()

    def test_recovery_actions_waiting_for_input(self) -> None:
        run = _run(status="waiting_for_input", stop_reason="")
        actions = recovery_actions_for_run(run, [], [])
        assert len(actions) == 1
        assert "respond" in actions[0].lower()

    def test_recovery_actions_completed_returns_empty(self) -> None:
        run = _run(status="completed", stop_reason="")
        actions = recovery_actions_for_run(run, [], [])
        assert actions == []

    def test_recovery_actions_running_returns_empty(self) -> None:
        run = _run(status="running", stop_reason="")
        actions = recovery_actions_for_run(run, [], [])
        assert actions == []

    def test_recovery_actions_failed_delegates_to_diagnose(self) -> None:
        run = _run(status="failed", stop_reason="step_failed:build")
        steps = [
            _step("build", status="failed", result_status="failed", result_summary="exit code 1"),
        ]
        actions = recovery_actions_for_run(run, steps, [])
        assert len(actions) > 0
        assert any("resume" in a.lower() for a in actions)

    def test_recovery_actions_blocked_includes_resume_and_cancel(self) -> None:
        run = _run(status="blocked", stop_reason="blocked_at:gate_check")
        steps = [_step("gate_check", status="completed", result_status="blocked")]
        actions = recovery_actions_for_run(run, steps, [])
        assert any("resume" in a.lower() for a in actions)
        assert any("cancel" in a.lower() for a in actions)


# ---------------------------------------------------------------------------
# Stale heartbeat reclaimed (#1257)
# ---------------------------------------------------------------------------


class TestStaleRecoveryDiagnosis:
    def test_stale_heartbeat_reclaimed(self) -> None:
        run = _run(status="failed", stop_reason="stale_heartbeat_reclaimed")
        dx = diagnose(run, [], [])
        assert dx.category == "stale_recovery"
        assert "heartbeat" in dx.what.lower()
        assert "died" in dx.why.lower() or "interrupted" in dx.why.lower()
        assert any("resume" in a for a in dx.next_actions)
        assert any("status" in a for a in dx.next_actions)

    def test_stale_heartbeat_reclaimed_during_compensation(self) -> None:
        run = _run(status="paused", stop_reason="stale_heartbeat_reclaimed_during_compensation")
        dx = diagnose(run, [], [])
        assert dx.category == "stale_recovery"
        assert "compensation" in dx.why.lower() or "rollback" in dx.why.lower()
        assert any("resume" in a for a in dx.next_actions)
