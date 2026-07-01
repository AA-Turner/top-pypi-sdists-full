"""Dead-window-handle recovery in _run_action (V3 export self-close case).

Bug
---
A page opens a popup in a new tab and closes it via JS ``window.close()``.
Selenium stays bound to the now-dead popup handle — it does NOT auto-follow the
browser's visual focus to the opener — so the next element action raises
``NoSuchWindowException: no such window``. That exception is not in
``_DEFAULT_RECOVERABLE``, so it propagates and the test dies.

V3 exported standalone tests delegate every element op (click/type/search/hover/
clear) to this engine via ``_run_action``, so they hit exactly this. The host
runtime heals it in its own executor before code runs; standalone exports have no
such pre-step, so the heal must live here.

Fix
---
``_heal_stale_window`` re-points the driver to a surviving window before SmartWait
and findElement, mirroring the host runtime's heal and V2 ``is_dom_loaded``
(switch to ``window_handles[0]`` for ANY surviving count).
"""
from unittest.mock import MagicMock, patch

from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException

from testmu_selenium._action_engine import _ActionSpec, _run_action, _heal_stale_window


PRIMARY = [{"selector": "#a", "isXPath": False}]
_DEAD = object()  # sentinel: current_window_handle raises (closed handle)


def _spec(runner):
    return _ActionSpec(runner=runner, recoverable_exceptions=(NoSuchElementException,))


class _FakeDriver:
    """Sync Selenium-driver stand-in.

    ``current_window_handle`` raises ``NoSuchWindowException`` when ``current`` is
    ``_DEAD`` (the self-closed popup); ``window_handles`` stays readable even then
    (Selenium queries the browser, not the dead window). ``switch_to.window``
    revives the current handle.
    """

    def __init__(self, *, current, handles):
        self._current = current
        self._handles = list(handles)
        self.switch_to = MagicMock(name="switch_to")
        self.switch_to.window.side_effect = lambda h: setattr(self, "_current", h)

    @property
    def window_handles(self):
        return list(self._handles)

    @property
    def current_window_handle(self):
        if self._current is _DEAD:
            raise NoSuchWindowException("no such window: target window already closed")
        return self._current


class TestHealStaleWindow:

    def test_dead_handle_one_survivor_switches(self):
        """Reported case: opener + popup, popup self-closes -> 1 survivor."""
        d = _FakeDriver(current=_DEAD, handles=["win-opener"])
        _heal_stale_window(d)
        d.switch_to.window.assert_called_once_with("win-opener")

    def test_dead_handle_multiple_survivors_switches_to_most_recent(self):
        """Current handle dead, 2 survivors -> switch to the most-recently-opened
        (window_handles[-1]), the popup the test just opened and is acting on, NOT
        window_handles[0] (the opener)."""
        d = _FakeDriver(current=_DEAD, handles=["win-a", "win-b"])
        _heal_stale_window(d)
        d.switch_to.window.assert_called_once_with("win-b")

    def test_live_handle_is_noop(self):
        """Current handle alive and a member of window_handles -> no switch."""
        d = _FakeDriver(current="win-a", handles=["win-a", "win-b"])
        _heal_stale_window(d)
        d.switch_to.window.assert_not_called()

    def test_current_handle_absent_without_exception_is_noop(self):
        """Regression: a live popup's current handle can be transiently absent from
        the window_handles snapshot without being dead. Do NOT steal focus unless
        Selenium reports the current handle as genuinely dead (raises) — else a
        click meant for the open popup yanks the browser to the wrong tab."""
        d = _FakeDriver(current="win-popup", handles=["win-opener"])
        _heal_stale_window(d)
        d.switch_to.window.assert_not_called()

    def test_dead_handle_no_survivors_is_noop(self):
        """No surviving windows -> nothing to switch to (don't fabricate a target)."""
        d = _FakeDriver(current=_DEAD, handles=[])
        _heal_stale_window(d)
        d.switch_to.window.assert_not_called()


class TestWindowHealWiring:

    def test_heal_runs_before_smart_wait_and_find(self):
        """_run_action must heal the window BEFORE SmartWait (which executes JS and
        would itself throw on a dead handle) and before findElement."""
        driver = MagicMock(name="driver")
        el = MagicMock(name="element")
        runner = MagicMock(return_value="OK")
        spec = _spec(runner)
        order = []
        sw_instance = MagicMock(name="SmartWait-inst")
        sw_instance.smart_wait.side_effect = lambda **k: order.append("smart_wait")

        def _find(*a, **k):
            order.append("find")
            return el

        with patch("testmu_selenium._action_engine.findElement", side_effect=_find), \
             patch("testmu_selenium._action_engine.SmartWait", return_value=sw_instance), \
             patch("testmu_selenium._action_engine._heal_stale_window",
                   side_effect=lambda d: order.append("heal")) as m_heal:
            assert _run_action(driver, spec, PRIMARY) == "OK"

        m_heal.assert_called_once_with(driver)
        assert order == ["heal", "smart_wait", "find"]
