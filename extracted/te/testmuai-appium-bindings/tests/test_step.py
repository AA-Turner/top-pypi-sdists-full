"""step() lifecycle, on_failure routing and per-step heal state."""
import pytest

from testmu_appium import _step
from testmu_appium._step import (
    StepInfo, current_step, get_step_count, mark_autohealed, step,
)
from testmu_appium._test_state import (
    has_pending_failures, pending_failures_summary, reset_test_state,
)


class _SpyReporter:
    def __init__(self):
        self.events = []

    def begin_test(self, name): self.events.append(("begin_test", name))
    def pass_test(self): self.events.append(("pass_test",))
    def fail_test(self, error): self.events.append(("fail_test", str(error)))
    def begin_step(self, description, instruction_id=None):
        self.events.append(("begin_step", description, instruction_id))

    def end_step(self, description, ok, error=None, instruction_id=None,
                 is_autohealed=False, autoheal_source="", interacted_element=None):
        self.events.append(("end_step", description, ok, is_autohealed, autoheal_source))

    def warn_step(self, description, error):
        self.events.append(("warn_step", description, str(error)))

    def attach_screenshot(self, data): self.events.append(("attach_screenshot",))
    def set_driver(self, driver): pass


@pytest.fixture(autouse=True)
def spy(monkeypatch):
    r = _SpyReporter()
    monkeypatch.setattr(_step, "reporter", lambda: r)
    _step._reset_step_counter()
    reset_test_state()
    yield r
    reset_test_state()


def test_step_reports_begin_and_end(spy):
    with step("Tap Compose", instruction_id="op-1"):
        pass
    assert spy.events == [
        ("begin_step", "Tap Compose", "op-1"),
        ("end_step", "Tap Compose", True, False, ""),
    ]


def test_step_sets_the_context_var_inside_the_body():
    assert current_step() is None
    with step("Tap Compose") as info:
        assert isinstance(info, StepInfo)
        assert current_step() is info
    assert current_step() is None


def test_step_counter_increments_and_resets():
    with step("a"):
        pass
    with step("b"):
        pass
    assert get_step_count() == 2
    _step._reset_step_counter()
    assert get_step_count() == 0


def test_no_on_failure_reraises(spy):
    with pytest.raises(RuntimeError):
        with step("Tap Compose"):
            raise RuntimeError("boom")
    assert ("end_step", "Tap Compose", False, False, "") in spy.events
    assert not has_pending_failures()


def test_fail_continue_suppresses_and_marks_the_verdict(spy):
    with step("Tap Compose", on_failure="fail-continue"):
        raise RuntimeError("boom")
    assert has_pending_failures()
    assert "Tap Compose" in pending_failures_summary()
    assert ("end_step", "Tap Compose", False, False, "") in spy.events


def test_warn_continue_suppresses_without_touching_the_verdict(spy):
    with step("Tap Compose", on_failure="warn-continue"):
        raise RuntimeError("boom")
    assert not has_pending_failures()
    assert any(e[0] == "warn_step" for e in spy.events)


def test_unknown_on_failure_is_rejected_at_step_entry(spy):
    """Vocabulary is playwright's. An unknown value is rejected on the way IN, not on
    failure: a selenium-flavoured "continue" would otherwise look correct on every
    passing step and only swallow when something finally broke."""
    entered = False
    with pytest.raises(ValueError) as exc:
        with step("Tap Compose", on_failure="continue"):
            entered = True
    assert not entered
    assert "fail-continue" in str(exc.value)


def test_end_step_fires_before_the_context_var_is_reset(spy):
    """A reporter reading step state during end_step must still see it."""
    seen = {}

    def end_step(description, ok, error=None, instruction_id=None,
                 is_autohealed=False, autoheal_source="", interacted_element=None):
        seen["step"] = current_step()
        seen["is_autohealed"] = is_autohealed

    spy.end_step = end_step
    with step("Tap Compose"):
        mark_autohealed("v16-autoheal")
    assert seen["step"] is not None
    assert seen["is_autohealed"] is True


def test_mark_autohealed_carries_the_source_to_end_step(spy):
    with step("Tap Compose"):
        mark_autohealed("v16-autoheal")
    assert ("end_step", "Tap Compose", True, True, "v16-autoheal") in spy.events


def test_mark_autohealed_outside_a_step_is_a_no_op():
    mark_autohealed("v16-autoheal")


def test_each_step_gets_a_fresh_heal_cache():
    from testmu_appium._step import get_heal_cache

    assert get_heal_cache() is None
    with step("a"):
        first = get_heal_cache()
        first["k"] = "v"
    with step("b"):
        second = get_heal_cache()
        assert second is not first
        assert second == {}
    assert get_heal_cache() is None


def test_id_aliases_instruction_id(spy):
    with step("Tap Compose", id="op-9"):
        pass
    assert ("begin_step", "Tap Compose", "op-9") in spy.events


def test_interacted_element_is_forwarded_to_end_step(spy):
    from testmu_appium._step import record_interacted_element

    captured = {}

    def end_step(description, ok, error=None, instruction_id=None,
                 is_autohealed=False, autoheal_source="", interacted_element=None):
        captured["payload"] = interacted_element

    spy.end_step = end_step
    with step("Tap Compose"):
        record_interacted_element({"center": [1, 2]})
    assert captured["payload"] == {"center": [1, 2]}


class TestBaseExceptionIsStillAFailedStep:
    """A KeyboardInterrupt, SystemExit, GeneratorExit or pytest.fail() inside the body
    sets `error`, so the step is reported ok=False and then re-raised."""

    CASES = [KeyboardInterrupt, SystemExit, GeneratorExit]

    @pytest.mark.parametrize("exc", CASES)
    def test_a_base_exception_is_reported_as_a_failed_step(self, spy, exc):
        with pytest.raises(exc):
            with step("Tap Compose"):
                raise exc("interrupted")
        assert ("end_step", "Tap Compose", False, False, "") in spy.events

    @pytest.mark.parametrize("exc", CASES)
    def test_a_base_exception_always_propagates(self, spy, exc):
        with pytest.raises(exc):
            with step("Tap Compose"):
                raise exc("interrupted")

    @pytest.mark.parametrize("exc", CASES)
    @pytest.mark.parametrize("on_failure", ["fail-continue", "warn-continue"])
    def test_on_failure_never_swallows_a_base_exception(self, spy, exc, on_failure):
        """Swallowing a Ctrl-C on a fail-continue step makes the suite unstoppable."""
        with pytest.raises(exc):
            with step("Tap Compose", on_failure=on_failure):
                raise exc("interrupted")
        assert not has_pending_failures()

    @pytest.mark.parametrize("exc", CASES)
    def test_the_context_var_is_reset_after_a_base_exception(self, spy, exc):
        with pytest.raises(exc):
            with step("Tap Compose"):
                raise exc("interrupted")
        assert current_step() is None

    def test_a_pytest_failure_inside_a_step_is_a_failed_step(self, spy):
        """pytest.fail raises an OutcomeException, which is a BaseException."""
        with pytest.raises(BaseException):  # noqa: B017 — the class is pytest-internal
            with step("Tap Compose"):
                pytest.fail("assertion helper failed")
        assert ("end_step", "Tap Compose", False, False, "") in spy.events
