"""@testmu_appium.test — announces the test body; run() owns the verdict.

Every assertion here counts emissions rather than testing membership, because the
behaviour under test is "exactly one verdict", not "at least one".
"""
import pytest

from testmu_appium import _decorator
from testmu_appium._step import step
from testmu_appium._test_state import has_pending_failures, reset_test_state


class _SpyReporter:
    def __init__(self):
        self.events = []

    def set_driver(self, driver): pass
    def begin_test(self, name): self.events.append(("begin_test", name))
    def pass_test(self): self.events.append(("pass_test",))
    def fail_test(self, error): self.events.append(("fail_test", str(error)))
    def begin_step(self, description, instruction_id=None): pass

    def end_step(self, description, ok, error=None, instruction_id=None,
                 is_autohealed=False, autoheal_source="", interacted_element=None):
        pass

    def warn_step(self, description, error): pass
    def attach_screenshot(self, data): pass

    def counts(self, name):
        return sum(1 for e in self.events if e[0] == name)


@pytest.fixture(autouse=True)
def spy(monkeypatch):
    r = _SpyReporter()
    monkeypatch.setattr(_decorator, "reporter", lambda: r)
    import testmu_appium._step as step_mod
    monkeypatch.setattr(step_mod, "reporter", lambda: r)
    reset_test_state()
    yield r
    reset_test_state()


def test_marks_the_function(spy):
    @_decorator.test
    def body(driver):
        pass

    assert body._testmu_test is True
    assert body.__name__ == "body"


def test_the_body_result_is_returned(spy):
    @_decorator.test
    def body(driver):
        return "result"

    assert body(None) == "result"


def test_the_test_is_announced_exactly_once(spy):
    @_decorator.test
    def body(driver):
        pass

    body(None)
    assert spy.counts("begin_test") == 1
    assert spy.events[0] == ("begin_test", "body")


class TestTheDecoratorEmitsNoVerdict:
    """run() is the single verdict owner: a decorated body invoked through run() —
    the shape codegen emits — produces exactly one verdict."""

    def test_a_passing_body_emits_no_verdict(self, spy):
        @_decorator.test
        def body(driver):
            pass

        body(None)
        assert spy.counts("pass_test") == 0
        assert spy.counts("fail_test") == 0

    def test_a_raising_body_emits_no_verdict_and_still_reraises(self, spy):
        @_decorator.test
        def body(driver):
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError):
            body(None)
        assert spy.counts("fail_test") == 0
        assert spy.counts("pass_test") == 0

    def test_pending_fail_continue_failures_emit_no_verdict_either(self, spy):
        @_decorator.test
        def body(driver):
            with step("Tap Go", on_failure="fail-continue"):
                raise RuntimeError("swallowed")

        body(None)
        assert spy.counts("fail_test") == 0
        assert spy.counts("pass_test") == 0

    def test_the_pending_failure_is_still_recorded_for_run_to_find(self, spy):
        """The decorator stops REPORTING the verdict, not accumulating it."""

        @_decorator.test
        def body(driver):
            with step("Tap Go", on_failure="fail-continue"):
                raise RuntimeError("swallowed")

        body(None)
        assert has_pending_failures()
