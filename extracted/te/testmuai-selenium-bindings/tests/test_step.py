"""Test step context manager."""
from unittest.mock import patch

import pytest
from testmu_selenium._step import step, _current_step, StepInfo


def test_step_context_manager_basic():
    with step("My step"):
        pass


def test_step_records_description():
    with step("My step description") as s:
        assert s.description == "My step description"


def test_step_propagates_exception():
    with pytest.raises(ValueError):
        with step("My step"):
            raise ValueError("oops")


def test_step_on_failure_continue_suppresses(caplog):
    """If on_failure='continue', exception is logged but not re-raised."""
    with step("My step", on_failure="continue"):
        raise ValueError("oops")
    # Should NOT raise — caller continues


def test_step_timeout_records():
    """Timeout is best-effort; just verify timeout_ms is stored."""
    with step("My step", timeout_ms=5000) as s:
        assert s.timeout_ms == 5000


def test_step_nested_steps_track_current():
    """Inside a step, _current_step ContextVar should hold its description."""
    assert _current_step.get(None) is None
    with step("Outer"):
        assert _current_step.get(None) is not None
        assert _current_step.get().description == "Outer"


class TestStepEndPayload:
    def test_end_logs_status_passed(self, caplog):
        with caplog.at_level("INFO"):
            with step("Open page"):
                pass
        assert "end name='Open page' status=passed auto_heal=False" in caplog.text

    def test_end_logs_status_failed_on_raise(self, caplog):
        with caplog.at_level("INFO"):
            with pytest.raises(ValueError):
                with step("Click thing"):
                    raise ValueError("boom")
        assert "end name='Click thing' status=failed auto_heal=False" in caplog.text

    def test_end_logs_status_failed_on_continue(self, caplog):
        with caplog.at_level("INFO"):
            with step("Soft step", on_failure="continue"):
                raise ValueError("boom")
        assert "end name='Soft step' status=failed auto_heal=False" in caplog.text

    def test_auto_heal_flag_reflected_in_end_log(self, caplog):
        with caplog.at_level("INFO"):
            with step("Healed step") as info:
                info.auto_heal = True
        assert "auto_heal=True" in caplog.text

    def test_stepinfo_auto_heal_defaults_false(self):
        assert StepInfo(description="x").auto_heal is False


# ---------------------------------------------------------------------------
# The end hook must say WHY a failed step failed
#
# HPS maps a step to its commands and shows the per-step failure disposition;
# without failure_condition the exported run loses that. The wire vocabulary is
# the runtime's FailureCondition enum, which each binding names differently.
# ---------------------------------------------------------------------------

class TestFailureConditionOnEndHook:
    def _end_payload(self, emit):
        return [c.args[1] for c in emit.call_args_list
                if c.args[0] == "lambda-testCase-end"][0]

    def test_passing_step_sends_no_failure_condition(self):
        from testmu_selenium._step import step
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with step("ok step"):
                pass
        assert "failure_condition" not in self._end_payload(emit)

    def test_failing_step_defaults_to_fail_test_immediately(self):
        from testmu_selenium._step import step
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with pytest.raises(RuntimeError):
                with step("boom"):
                    raise RuntimeError("boom")
        assert self._end_payload(emit)["failure_condition"] == "FAIL_TEST_IMMEDIATELY"

    def test_continue_maps_to_fail_but_continue(self):
        from testmu_selenium._step import step
        with patch("testmu_selenium._step._emit_step_hook") as emit:
            with step("soft", on_failure="continue"):
                raise RuntimeError("boom")
        payload = self._end_payload(emit)
        assert payload["status"] == "failed"
        assert payload["failure_condition"] == "FAIL_BUT_CONTINUE_EXECUTING"

    @pytest.mark.parametrize("token,expected", [
        ("fail", "FAIL_TEST_IMMEDIATELY"),
        ("continue", "FAIL_BUT_CONTINUE_EXECUTING"),
        ("fail-continue", "FAIL_BUT_CONTINUE_EXECUTING"),
        ("warn-continue", "WARN_BUT_CONTINUE_EXECUTING"),
        ("FAIL", "FAIL_TEST_IMMEDIATELY"),
        ("unknown", ""),
        ("", ""),
        (None, ""),
    ])
    def test_wire_vocabulary_mapping(self, token, expected):
        from testmu_selenium._step import _wire_failure_condition
        assert _wire_failure_condition(token) == expected
