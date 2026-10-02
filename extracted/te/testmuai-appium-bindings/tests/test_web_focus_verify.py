"""The focus check between a web type's tap and its keys.

Pins the failure this exists for: a page that redraws on focus (Google's
search box swapping in its suggestions overlay) can steal the tap's click for
whatever now occupies the point. Measured on a device: the click landed on a
trending row, NAVIGATED, six keystrokes went to a page that no longer existed,
and the verb reported success three runs straight.
"""
import pytest

from testmu_appium import _config
from testmu_appium._action_type import _verify_web_focus, _type_coord_runner
from testmu_appium._errors import ElementBlocked


class _Driver:
    def __init__(self):
        self.taps = []


@pytest.fixture(autouse=True)
def _w3c_tap(monkeypatch):
    monkeypatch.setattr("testmu_appium._action_type.tap",
                        lambda driver, x, y: driver.taps.append((x, y)))
    monkeypatch.setattr("testmu_appium._action_type.type_text",
                        lambda driver, text: None)
    monkeypatch.setattr("testmu_appium._action_type._FOCUS_POLL_BUDGET_S", 0.05)
    monkeypatch.setattr("testmu_appium._action_type._FOCUS_POLL_INTERVAL_S", 0.01)


def _ctx(states, href="https://www.google.com/"):
    """A ctx whose probe answers from a script, then repeats its last answer."""
    queue = list(states)

    def probe():
        return queue.pop(0) if len(queue) > 1 else queue[0]

    return {"web_focus_state": probe, "web_href_before": href,
            "description": "the search box", "clear_first": False,
            "text": "testmu"}


class TestVerifyWebFocus:
    def test_an_editable_holding_focus_lets_the_keys_through(self):
        driver = _Driver()
        _verify_web_focus(driver, 157, 348, _ctx(
            [{"href": "https://www.google.com/", "editable": True}]))
        assert driver.taps == []

    def test_the_overlays_replacement_field_is_the_correct_field(self):
        """Focus on a DIFFERENT editable node than the one located is the
        GOOD case — the redraw swapped in its own textarea."""
        driver = _Driver()
        _verify_web_focus(driver, 157, 348, _ctx([
            {"href": "https://www.google.com/", "editable": False},
            {"href": "https://www.google.com/", "editable": True},
        ]))
        assert driver.taps == []

    def test_a_navigating_tap_raises_naming_both_locations(self):
        """The measured Google failure: the click landed on a trending row."""
        driver = _Driver()
        with pytest.raises(ElementBlocked) as exc:
            _verify_web_focus(driver, 157, 348, _ctx([
                {"href": "https://www.google.com/search?q=zepto+pre+ipo",
                 "editable": False},
            ]))
        message = str(exc.value)
        assert "navigated" in message
        assert "google.com/" in message and "zepto" in message
        assert "nothing was typed" in message

    def test_no_focus_gets_one_more_tap_then_raises(self):
        driver = _Driver()
        with pytest.raises(ElementBlocked) as exc:
            _verify_web_focus(driver, 157, 348, _ctx(
                [{"href": "https://www.google.com/", "editable": False}]))
        assert driver.taps == [(157, 348)], "exactly one re-tap"
        assert "nowhere to go" in str(exc.value)

    def test_the_retap_can_succeed(self):
        driver = _Driver()
        states = [{"href": "https://www.google.com/", "editable": False}]

        real_tap = driver.taps.append

        def tap_and_focus(x, y):
            real_tap((x, y))
            states.append({"href": "https://www.google.com/", "editable": True})

        ctx = _ctx([])
        queue = states

        def probe():
            return queue[-1]

        ctx["web_focus_state"] = probe
        import testmu_appium._action_type as module
        original = module.tap
        module.tap = lambda driver_, x, y: tap_and_focus(x, y)
        try:
            _verify_web_focus(driver, 10, 20, ctx)
        finally:
            module.tap = original
        assert driver.taps == [(10, 20)]

    def test_a_page_that_cannot_answer_stands_down(self):
        """None from the probe is 'no verification available', not a verdict —
        a channel hiccup must not fail a type that would have worked."""
        driver = _Driver()
        ctx = _ctx([])
        ctx["web_focus_state"] = lambda: None
        _verify_web_focus(driver, 1, 2, ctx)
        assert driver.taps == []

    def test_a_native_type_has_no_probe_and_is_untouched(self):
        driver = _Driver()
        _verify_web_focus(driver, 1, 2, {"description": "native field"})
        assert driver.taps == []


class TestTheRunnerRunsTheCheckBetweenTapAndKeys:
    def test_keys_are_never_sent_after_a_navigating_tap(self, monkeypatch):
        typed = []
        monkeypatch.setattr("testmu_appium._action_type.type_text",
                            lambda driver, text: typed.append(text))
        driver = _Driver()
        ctx = _ctx([
            {"href": "https://elsewhere.example/", "editable": False},
        ])
        with pytest.raises(ElementBlocked):
            _type_coord_runner(driver, 157, 348, ctx)
        assert typed == []


class TestPrefocusMovesTheTap:
    """The preventive half: focus through the page BEFORE tapping, so a
    redraw-on-focus fires with no click in flight, and the tap lands on the
    field at its post-redraw position. Probe-proven twice on the device."""

    def test_the_tap_moves_to_the_prefocused_point(self, monkeypatch):
        driver = _Driver()
        ctx = _ctx([{"href": "https://www.google.com/", "editable": True}])
        ctx["web_prefocus"] = lambda: (183, 169)
        _type_coord_runner(driver, 157, 348, ctx)
        assert driver.taps == [(183, 169)], "tap follows the field's new home"

    def test_a_declined_prefocus_keeps_the_located_point(self, monkeypatch):
        driver = _Driver()
        ctx = _ctx([{"href": "https://www.google.com/", "editable": True}])
        ctx["web_prefocus"] = lambda: None
        _type_coord_runner(driver, 157, 348, ctx)
        assert driver.taps == [(157, 348)]

    def test_native_types_have_no_prefocus_and_tap_as_before(self, monkeypatch):
        driver = _Driver()
        _type_coord_runner(driver, 10, 20, {"description": "native",
                                            "clear_first": False, "text": "x"})
        assert driver.taps == [(10, 20)]


class TestPrefocusPoint:
    """prefocus_point: page focus, settle, read the focused field's new rect,
    convert with the surface's own calibration."""

    class _Surface:
        def __init__(self, answers):
            self.page = {"dpr": 2, "scale": 1, "offsetLeft": 0, "offsetTop": 0,
                         "viewportWidth": 400, "viewportHeight": 800}
            self.origin = (5, 141)
            self.channel = self
            self._answers = list(answers)

        def evaluate(self, script):
            return self._answers.pop(0)

    def test_the_probe_sequence_returns_the_device_point(self, monkeypatch):
        from testmu_appium import _action_web

        monkeypatch.setitem(_config._config, "platform", "ios")
        monkeypatch.setattr(_action_web, "_PREFOCUS_SETTLE_S", 0)
        surface = self._Surface([True, '{"x": 178, "y": 28}'])
        element = {"css_path": "#tsf textarea", "editable": True}
        point = _action_web.prefocus_point(surface, element)
        # iOS factor = scale (1): device = origin + css — the probe's own numbers
        assert point == (183, 169)

    def test_a_page_that_refuses_script_focus_declines(self, monkeypatch):
        from testmu_appium import _action_web

        monkeypatch.setattr(_action_web, "_PREFOCUS_SETTLE_S", 0)
        surface = self._Surface([False])
        assert _action_web.prefocus_point(
            surface, {"css_path": "#q", "editable": True}) is None

    def test_a_framed_element_declines(self):
        from testmu_appium import _action_web

        surface = self._Surface([])
        assert _action_web.prefocus_point(
            surface, {"css_path": "#q", "path": ">x0"}) is None

    def test_a_field_that_settled_below_the_viewport_declines(self, monkeypatch):
        """The docstring's promise, previously unkept: off-screen means
        DECLINE, not a confident tap at a point the screen does not have."""
        from testmu_appium import _action_web

        monkeypatch.setattr(_action_web, "_PREFOCUS_SETTLE_S", 0)
        surface = self._Surface([True, '{"x": 200, "y": 900}'])  # viewport is 800 tall
        assert _action_web.prefocus_point(
            surface, {"css_path": "#q"}) is None

    def test_a_field_that_settled_offscreen_declines(self, monkeypatch):
        from testmu_appium import _action_web

        monkeypatch.setattr(_action_web, "_PREFOCUS_SETTLE_S", 0)
        surface = self._Surface([True, '{"x": -400, "y": 28}'])
        assert _action_web.prefocus_point(
            surface, {"css_path": "#q"}) is None

    def test_a_channel_error_declines_rather_than_failing_the_type(self):
        from testmu_appium import _action_web

        class _Broken(self._Surface):
            def evaluate(self, script):
                raise RuntimeError("socket closed")

        assert _action_web.prefocus_point(
            _Broken([]), {"css_path": "#q"}) is None


class TestFragmentChangesAreNotNavigation:
    """Google's box appends `#sbfbu=…` to the address the moment it gains
    focus — the SAME page noting its state. Reading that as 'the tap
    navigated' failed a healthy type on any cold page."""

    def test_a_fragment_change_lets_the_keys_through(self):
        driver = _Driver()
        ctx = _ctx(
            [{"href": "https://www.google.com/#sbfbu=1&pi=", "editable": True}],
            href="https://www.google.com/")
        _verify_web_focus(driver, 157, 348, ctx)
        assert driver.taps == []

    def test_a_real_navigation_still_raises(self):
        driver = _Driver()
        with pytest.raises(ElementBlocked):
            _verify_web_focus(driver, 157, 348, _ctx(
                [{"href": "https://www.google.com/search?q=zepto",
                  "editable": False}],
                href="https://www.google.com/"))
