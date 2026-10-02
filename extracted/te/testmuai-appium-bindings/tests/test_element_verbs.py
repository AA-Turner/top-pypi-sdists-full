"""Element verbs: click, type, search, clear, select, scroll, scroll_until, drag."""
import pytest
import testmu_appium

from testmu_appium import _action_engine, _config
from testmu_appium._action_click import click
from testmu_appium._action_drag import drag
from testmu_appium._action_scroll import scroll
from testmu_appium._action_scroll_until import scroll_until, _perceive as _real_perceive
from testmu_appium._helpers.band import BAND_NUDGE_MAX_GESTURES
from testmu_appium._action_select import select
from testmu_appium._action_type import clear, search, type as type_
from testmu_appium._errors import (
    CoordinateFallbackUnavailable, ElementNotFound, PickerModeNotSupported,
)
from testmu_appium._heal import HealHit, HealNoMatch, HealUnresolved
from testmu_appium._step import step
from testmu_appium._vars import _variable_store

SELECTORS = [{"strategy": "view_id", "selector": "com.app:id/go", "score": 90}]
TARGET_SELECTORS = [
    {"strategy": "view_id", "selector": "com.app:id/drop", "score": 90}
]
BASIS = {"x_ratio": 0.5, "y_ratio": 0.5, "orientation": "portrait", "window": [1080, 2340]}


class _El:
    def __init__(self, rect=None, attributes=None, texts=None, element_id="el-1"):
        self.id = element_id
        self.rect = rect or {"x": 100, "y": 200, "width": 200, "height": 100}
        self.attributes = attributes or {}
        self.calls = []
        self._texts = list(texts) if texts else None

    def click(self):
        self.calls.append(("click",))

    def clear(self):
        self.calls.append(("clear",))

    def send_keys(self, text):
        self.calls.append(("send_keys", text))

    def get_attribute(self, name):
        if name == "text" and self._texts is not None:
            return self._texts.pop(0) if len(self._texts) > 1 else self._texts[0]
        return self.attributes.get(name)


class _Driver:
    def __init__(self, found=None, queue=None, window=(1080, 2340)):
        self.found = found or {}
        self.queue = list(queue) if queue is not None else None
        self.scripts = []
        self.find_calls = []
        self.keycodes = []
        self._window = window

    @property
    def page_source(self):
        # The screen fingerprint scroll_until's movement probe reads. It changes
        # with every scroll gesture, so a live list reads as "still moving" and the
        # search keeps going; a driver at its end (see _NoMoreContent) freezes it so
        # the loop takes its end-of-content branch.
        scrolls = sum(1 for name, _ in self.scripts if name == "mobile: scrollGesture")
        return f"<hierarchy scrolls='{scrolls}'/>"

    def get_window_size(self):
        return {"width": self._window[0], "height": self._window[1]}

    def find_elements(self, by, value):
        self.find_calls.append((by, value))
        # The scrollable-container lookup (R4) is not a target find. These fixtures
        # declare no auto-resolvable container, so it returns nothing and — crucially
        # for the positional queue — must not consume a queued target result.
        if "scrollable(true)" in str(value):
            return []
        if self.queue is not None:
            return self.queue.pop(0) if self.queue else []
        for needle, result in self.found.items():
            if needle in value:
                return result
        return []

    def execute_script(self, script, args=None):
        self.scripts.append((script, args))
        # scrollGesture returns "can scroll more"
        return script != "mobile: scrollGesture" or len(self.scripts) < 3

    def press_keycode(self, code):
        self.keycodes.append(code)


class _FakePerception:
    """What the scroll_until fake `_perceive` returns: one DESCRIPTOR whose identity
    is the driver's page_source fingerprint, so the container-scoped movement probe
    (`_container_signature`, which reads perception.descriptors — NOT the wire
    entries) sees content change exactly when that fingerprint does, with no real
    device tree or screenshot. Centred in the window so it lands inside any recorded
    container box."""

    def __init__(self, descriptors, screenshot_b64="shot"):
        self.descriptors = descriptors
        self.entries = [{"index": i} for i in descriptors]
        self.screenshot_b64 = screenshot_b64


def _fake_perceive(driver, *, screenshot):
    size = driver.get_window_size()
    w, h = size["width"], size["height"]
    descriptors = {1: {
        "resource_id": None, "text": driver.page_source, "content_desc": None,
        "bounds": (0, 0, w, h), "center": (w // 2, h // 2),
    }}
    return _FakePerception(descriptors, screenshot_b64=("shot" if screenshot else None))


@pytest.fixture(autouse=True)
def _fast(monkeypatch):
    monkeypatch.setattr(_action_engine, "_settle", lambda driver, deadline: None)
    monkeypatch.setattr(_action_engine.time, "sleep", lambda s: None)
    monkeypatch.setitem(_config._config, "platform", "android")
    # These suites are not about the find timeout; one strategy pass keeps a
    # deliberate miss instantaneous instead of polling for the real budget.
    monkeypatch.setitem(_config._config, "default_action_timeout_ms", 0)
    import testmu_appium._action_scroll_until as _su
    monkeypatch.setattr(_su, "_perceive", _fake_perceive)
    _variable_store.clear()
    yield
    _variable_store.clear()


def _found(element):
    return _Driver(found={"com.app:id/go": [element]})


class TestClick:
    def test_taps_the_element(self):
        el = _El()
        with step("s"):
            click(_found(el), selectors=SELECTORS, description="Go")
        assert el.calls == [("click",)]

    def test_timing_identifies_the_actual_click_command(self):
        el = _El()
        with testmu_appium.capture_action_timings() as timings:
            with step("s"):
                click(_found(el), selectors=SELECTORS, description="Go")

        [timing] = timings
        assert timing["counts"]["click_commands"] == 1
        assert "click" in timing["action_phases_ms"]

    def test_long_press_modifier_uses_the_long_click_gesture(self):
        el = _El()
        driver = _found(el)
        with step("s"):
            click(driver, selectors=SELECTORS, description="Go",
                  click_modifier={"kind": "long_press", "duration": "1.5"})
        assert driver.scripts == [
            ("mobile: longClickGesture", {"x": 200, "y": 250, "duration": 1500})
        ]
        assert el.calls == []

    def test_multi_click_modifier_taps_repeatedly(self, monkeypatch):
        monkeypatch.setattr("time.sleep", lambda s: None)
        el = _El()
        driver = _found(el)
        with step("s"):
            click(driver, selectors=SELECTORS, description="Go",
                  click_modifier={"kind": "multi_click", "frequency": 3, "gap": 0})
        assert [s[0] for s in driver.scripts] == ["mobile: clickGesture"] * 3

    def test_multi_click_of_one_degrades_to_a_plain_tap(self):
        el = _El()
        driver = _found(el)
        with step("s"):
            click(driver, selectors=SELECTORS, description="Go",
                  click_modifier={"kind": "multi_click", "frequency": 1})
        assert driver.scripts == []
        assert el.calls == [("click",)]

    def test_modifier_variables_resolve_at_execution_time(self):
        from testmu_appium._vars import set_var

        set_var("press_ms", "2")
        el = _El()
        driver = _found(el)
        with step("s"):
            click(driver, selectors=SELECTORS, description="Go",
                  click_modifier={"kind": "long_press", "duration": "{{press_ms}}"})
        assert driver.scripts[0][1]["duration"] == 2000

    def test_unknown_modifier_kind_raises(self):
        with pytest.raises(ValueError):
            with step("s"):
                click(_found(_El()), selectors=SELECTORS, click_modifier={"kind": "hover"})

    def test_unknown_recorded_gesture_raises(self):
        with pytest.raises(ValueError):
            with step("s"):
                click(_found(_El()), selectors=SELECTORS,
                      click_modifier={"gesture": "pinch"})

    def test_coordinate_fallback_taps_the_scaled_ratio(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))
        driver = _Driver(queue=[[]])
        with step("s"):
            click(driver, selectors=SELECTORS, description="Go", fallback_coordinates=BASIS)
        assert driver.scripts == [("mobile: clickGesture", {"x": 540, "y": 1170})]

    def test_coordinate_fallback_keeps_a_long_press_a_long_press(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))
        driver = _Driver(queue=[[]])
        with step("s"):
            click(driver, selectors=SELECTORS, description="Go", fallback_coordinates=BASIS,
                  click_modifier={"kind": "long_press", "duration": "1"})
        assert driver.scripts[0][0] == "mobile: longClickGesture"


class TestRecordedModifierVocabulary:
    """The generator and the AST carry the RECORDED modifier dict verbatim — keys
    `gesture`, `duration_ms`, `count`/`frequency`, `gap_ms`. The gesture primitives
    accept that spelling alongside the legacy web one (`kind`, `duration` in SECONDS,
    `gap`).

    The shapes below are the ones the cgf/AST corpora emit:
    `v4_appium_click_gesture_coordinate_basis` and the AST lowering tests.
    """

    def test_the_golden_long_press_shape_executes(self):
        """cgf golden: click_modifier={"gesture": "long_press", "duration_ms": 1500}."""
        el = _El()
        driver = _found(el)
        with step("Long-press the thread"):
            click(driver, selectors=SELECTORS, description="Long-press the thread",
                  click_modifier={"gesture": "long_press", "duration_ms": 1500})
        assert driver.scripts == [
            ("mobile: longClickGesture", {"x": 200, "y": 250, "duration": 1500})
        ]
        assert el.calls == []

    def test_recorded_milliseconds_are_not_re_scaled_as_seconds(self):
        """The legacy key is SECONDS and the recorded key is MILLISECONDS; reading
        1500 as 1500 seconds would press for 25 minutes."""
        driver = _found(_El())
        with step("s"):
            click(driver, selectors=SELECTORS,
                  click_modifier={"gesture": "long_press", "duration_ms": 1500})
        assert driver.scripts[0][1]["duration"] == 1500

    def test_a_recorded_gesture_without_a_duration_uses_the_default(self):
        driver = _found(_El())
        with step("s"):
            click(driver, selectors=SELECTORS, click_modifier={"gesture": "long_press"})
        assert driver.scripts[0][1]["duration"] == 800

    @pytest.mark.parametrize("recorded_ms,expected", [(0, 0), ("0", 0), (250, 250)])
    def test_an_explicit_recorded_duration_including_zero_is_honoured(
        self, recorded_ms, expected
    ):
        driver = _found(_El())
        with step("s"):
            click(driver, selectors=SELECTORS,
                  click_modifier={"gesture": "long_press", "duration_ms": recorded_ms})
        assert driver.scripts[0][1]["duration"] == expected

    def test_the_recorded_multi_click_count_key_taps_repeatedly(self, monkeypatch):
        """The AST lowering corpus emits {"gesture": "multi_click", "count": n}."""
        monkeypatch.setattr("time.sleep", lambda s: None)
        driver = _found(_El())
        with step("s"):
            click(driver, selectors=SELECTORS,
                  click_modifier={"gesture": "multi_click", "count": 3, "gap_ms": 50})
        assert [s[0] for s in driver.scripts] == ["mobile: clickGesture"] * 3

    def test_the_recorded_gap_is_milliseconds(self, monkeypatch):
        slept = []
        monkeypatch.setattr("time.sleep", lambda s: slept.append(s))
        with step("s"):
            click(_found(_El()), selectors=SELECTORS,
                  click_modifier={"gesture": "multi_click", "frequency": 3, "gap_ms": 250})
        assert slept == [0.25, 0.25]

    def test_the_legacy_gap_stays_seconds(self, monkeypatch):
        slept = []
        monkeypatch.setattr("time.sleep", lambda s: slept.append(s))
        with step("s"):
            click(_found(_El()), selectors=SELECTORS,
                  click_modifier={"kind": "multi_click", "frequency": 3, "gap": 0.25})
        assert slept == [0.25, 0.25]

    def test_a_recorded_count_of_one_still_degrades_to_a_plain_tap(self):
        el = _El()
        driver = _found(el)
        with step("s"):
            click(driver, selectors=SELECTORS,
                  click_modifier={"gesture": "multi_click", "count": 1})
        assert driver.scripts == []
        assert el.calls == [("click",)]

    def test_a_recorded_variable_token_resolves_before_normalization(self):
        from testmu_appium._vars import set_var

        set_var("press_ms", "1200")
        driver = _found(_El())
        with step("s"):
            click(driver, selectors=SELECTORS,
                  click_modifier={"gesture": "long_press", "duration_ms": "{{press_ms}}"})
        assert driver.scripts[0][1]["duration"] == 1200

    def test_the_coordinate_path_reads_the_recorded_vocabulary_too(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))
        driver = _Driver(queue=[[]])
        with step("s"):
            click(driver, selectors=SELECTORS, description="Go", fallback_coordinates=BASIS,
                  click_modifier={"gesture": "long_press", "duration_ms": 1500})
        assert driver.scripts == [
            ("mobile: longClickGesture", {"x": 540, "y": 1170, "duration": 1500})
        ]


class TestCoordinateRecordedClick:
    """The generator's coordinate-recorded shape, byte-for-byte from the cgf golden
    `v4_appium_click_coordinate_mode`: selectors=None plus a complete basis."""

    GOLDEN_BASIS = {
        "x_ratio": 0.8631, "y_ratio": 0.9012,
        "orientation": "portrait", "window": [1080, 2340],
    }

    @staticmethod
    def _misses(monkeypatch):
        """Heal answers authoritatively that the target is not on screen, which is
        the only thing that hands the action down to the recorded ratio."""
        monkeypatch.setattr(_action_engine, "autoheal",
                            lambda *a, **kw: HealNoMatch("not on this screen"))

    def test_the_golden_call_shape_executes(self, monkeypatch):
        self._misses(monkeypatch)
        driver = _Driver()
        with step("Tap the canvas at the recorded point"):
            click(
                driver,
                selectors=None,
                description="Tap the canvas at the recorded point",
                fallback_coordinates=self.GOLDEN_BASIS,
            )
        assert driver.scripts == [("mobile: clickGesture", {"x": 932, "y": 2108})]
        assert driver.find_calls == []

    def test_a_heal_hit_wins_over_the_recorded_point(self, monkeypatch):
        healed = _El()
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(element=healed, by="id", value="v", dom_index=3),
        )
        driver = _Driver()
        with step("Tap the canvas at the recorded point"):
            click(driver, selectors=None,
                  description="Tap the canvas at the recorded point",
                  fallback_coordinates=self.GOLDEN_BASIS)
        assert healed.calls == [("click",)]
        assert driver.scripts == [], "the remembered point is not owed once heal resolved it"

    def test_a_recorded_gesture_survives_the_selectorless_path(self, monkeypatch):
        self._misses(monkeypatch)
        driver = _Driver()
        with step("Long-press the canvas"):
            click(driver, selectors=None, description="Long-press",
                  fallback_coordinates=self.GOLDEN_BASIS,
                  click_modifier={"kind": "long_press", "duration": "1.5"})
        assert driver.scripts[0][0] == "mobile: longClickGesture"
        assert driver.scripts[0][1]["duration"] == 1500

    def test_an_orientation_mismatch_refuses_the_selectorless_click(self, monkeypatch):
        self._misses(monkeypatch)
        driver = _Driver()
        with pytest.raises(ElementNotFound) as exc:
            with step("s"):
                click(driver, selectors=None, description="Tap",
                      fallback_coordinates=dict(self.GOLDEN_BASIS, orientation="landscape"))
        assert isinstance(exc.value.__cause__, CoordinateFallbackUnavailable)
        assert driver.scripts == []

    def test_a_selectorless_click_without_a_basis_is_left_to_heal(self, monkeypatch):
        """No basis is no longer a generation error: the description names the
        target, so heal owns the click and only its authoritative miss ends it."""
        self._misses(monkeypatch)
        with pytest.raises(ElementNotFound):
            with step("s"):
                click(_Driver(), selectors=None, description="Tap")

    def test_a_verb_without_a_coordinate_runner_heals_instead_of_refusing(self, monkeypatch):
        """A blind tap is not a clear, so `clear` carries no coord_runner — but it is
        an element verb with a description, and heal returns an element rather than a
        point. `select` behaves the same; its engine-level cell lives in
        TestSelectorlessHeals, where the picker's own lookup is out of the way."""
        healed = _El()
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealHit(element=healed, by="id", value="v", dom_index=3),
        )
        with step("s"):
            clear(_Driver(), selectors=None, description="the coupon field",
                  fallback_coordinates=BASIS)
        assert healed.calls == [("click",), ("clear",)], "clear focuses, then clears"

    def test_scroll_until_without_selectors_or_condition_is_refused(self):
        """scroll_until never reaches the element engine — it owns its own lookup,
        so the heal ladder cannot re-ground it. Its stop is a recorded selector or
        a vision condition; a call carrying neither has nothing to search for."""
        with pytest.raises(ValueError):
            with step("s"):
                scroll_until(_Driver(), selectors=None, description="x",
                             fallback_coordinates=BASIS)

    def test_element_scroll_without_selectors_is_a_screen_scroll_not_an_error(self):
        """scroll() routes a selectorless call to the DRIVER-mode screen scroll before
        the element engine ever sees it — the one verb where selectorless is a
        different verb rather than a coordinate replay."""
        driver = _Driver()
        with step("s"):
            scroll(driver, selectors=None, kind="times", direction="down", value=1)
        assert [s[0] for s in driver.scripts] == ["mobile: scrollGesture"]


class TestUnresolvedHealActsAtItsCentre:
    """Heal named the element and the local re-find could not reach it.

    Android draws a dropdown's option rows in a child Pop-Up Window: the server
    selects them from the captured tree by dom_index, and no UiSelector reaches
    them, so the re-find returns zero however the lookup is compiled. The centre
    from that same parse is the one piece of evidence that survives — the recorded
    description resolved against the live screen, which is what `vision_runner`
    names. Measured on a device: with the list visibly open, `dumpsys window` shows
    two Pop-Up Windows and the main-window dump carries none of the rows.
    """

    #: bounds/centre as the perception parse retains them.
    DESCRIPTOR = {"center": (540, 700), "bounds": (100, 600, 980, 800)}

    @staticmethod
    def _unresolved(monkeypatch, descriptor=None, matched=0):
        monkeypatch.setattr(
            _action_engine, "autoheal",
            lambda *a, **kw: HealUnresolved(
                "healed lookup 'new UiSelector().resourceId(\"opt-2\")' matched "
                f"{matched} live elements, expected 1",
                descriptor=descriptor, matched=matched,
            ),
        )

    def test_click_acts_where_heal_said_the_element_was(self, monkeypatch):
        self._unresolved(monkeypatch, self.DESCRIPTOR)
        driver = _Driver()
        with step("Tap Alaska"):
            click(driver, selectors=None,
                  description='PRIMARY: Alaska state option; role=item')
        assert driver.scripts == [("mobile: clickGesture", {"x": 540, "y": 700})]

    def test_type_reaches_the_field_through_the_same_centre(self, monkeypatch):
        self._unresolved(monkeypatch, self.DESCRIPTOR)
        driver = _Driver()
        with step("Type into the overlay field"):
            type_(driver, selectors=None, description="the overlay field",
                  text="Alaska", clear_first=False)
        assert ("mobile: clickGesture", {"x": 540, "y": 700}) in driver.scripts

    def test_several_matches_are_ambiguity_not_unreachability(self, monkeypatch):
        """The centre already had its chance — disambiguate_by_centre weighed it
        against live geometry and declined. Tapping it anyway overrides that."""
        self._unresolved(monkeypatch, self.DESCRIPTOR, matched=3)
        driver = _Driver()
        with pytest.raises(ElementNotFound):
            with step("Tap Alaska"):
                click(driver, selectors=None, description="Alaska option")
        assert driver.scripts == []

    def test_a_descriptor_without_a_centre_still_raises(self, monkeypatch):
        self._unresolved(monkeypatch, {"resource_id": "opt-2"})
        driver = _Driver()
        with pytest.raises(ElementNotFound):
            with step("Tap Alaska"):
                click(driver, selectors=None, description="Alaska option")

    def test_no_descriptor_at_all_still_raises(self, monkeypatch):
        self._unresolved(monkeypatch, None)
        driver = _Driver()
        with pytest.raises(ElementNotFound):
            with step("Tap Alaska"):
                click(driver, selectors=None, description="Alaska option")

    def test_select_has_no_point_runner_and_still_raises(self, monkeypatch):
        """A point cannot express "open this picker and choose a row"."""
        self._unresolved(monkeypatch, self.DESCRIPTOR)
        driver = _Driver()
        with pytest.raises(ElementNotFound):
            with step("Choose Alaska"):
                select(driver, selectors=SELECTORS, label="Alaska",
                       description="the state picker")
        assert driver.scripts == []

    def test_the_recorded_ratio_is_not_what_gets_tapped(self, monkeypatch):
        """BASIS maps to the window centre (540, 1170); heal's own centre wins, and
        the recorded ratio stays behind an authoritative 404."""
        self._unresolved(monkeypatch, self.DESCRIPTOR)
        driver = _Driver()
        with step("Tap Alaska"):
            click(driver, selectors=None, description="Alaska option",
                  fallback_coordinates=BASIS)
        assert driver.scripts == [("mobile: clickGesture", {"x": 540, "y": 700})]


class TestVisionGroundedElementActions:
    @pytest.fixture(autouse=True)
    def _vision(self, monkeypatch):
        self.calls = []

        def resolve(driver, description, action_type):
            self.calls.append((description, action_type))
            return 400, 700

        monkeypatch.setattr(_action_engine, "get_vision_coordinates", resolve)

    @staticmethod
    def _with_active_element(driver, element):
        driver.switch_to = type("_Switch", (), {"active_element": element})()
        return driver

    def test_click_re_resolves_intent_without_selectors_or_ratios(self):
        driver = _Driver()
        with step("vision click"):
            click(
                driver, selectors=None, description="the unlabeled payment slider",
                grounded_by="vision",
            )
        assert self.calls == [("the unlabeled payment slider", "click")]
        assert driver.scripts == [
            ("mobile: clickGesture", {"x": 400, "y": 700})
        ]
        assert driver.find_calls == []

    def test_vision_double_click_performs_two_taps(self, monkeypatch):
        monkeypatch.setattr("time.sleep", lambda _seconds: None)
        driver = _Driver()
        with step("vision double"):
            click(
                driver, selectors=None, description="the thumbnail",
                grounded_by="vision",
                click_modifier={"gesture": "multi_click", "count": 2},
            )
        assert [script for script, _ in driver.scripts] == [
            "mobile: clickGesture", "mobile: clickGesture",
        ]

    def test_vision_long_press_preserves_duration(self):
        driver = _Driver()
        with step("vision hold"):
            click(
                driver, selectors=None, description="the answer control",
                grounded_by="vision",
                click_modifier={"gesture": "long_press", "duration_ms": 1200},
            )
        assert driver.scripts == [
            ("mobile: longClickGesture", {
                "x": 400, "y": 700, "duration": 1200,
            })
        ]

    def test_type_and_search_use_the_fresh_point(self):
        active = _El()
        driver = self._with_active_element(_Driver(), active)
        with step("vision type"):
            type_(
                driver, selectors=None, text="hello",
                description="the message field", grounded_by="vision",
            )
        with step("vision search"):
            search(
                driver, selectors=None, text="kane",
                description="the search field", grounded_by="vision",
            )
        assert self.calls == [
            ("the message field", "type"),
            ("the search field", "type"),
        ]
        assert [script for script, _ in driver.scripts] == [
            "mobile: clickGesture", "mobile: type",
            "mobile: clickGesture", "mobile: type",
        ]
        assert driver.keycodes

    def test_clear_is_vision_only_not_a_legacy_coordinate_fallback(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal",
                            lambda *a, **kw: HealNoMatch("not on this screen"))
        active = _El()
        driver = self._with_active_element(_Driver(), active)
        with step("vision clear"):
            clear(
                driver, selectors=None, description="the coupon field",
                grounded_by="vision",
            )
        assert active.calls == [("clear",)]
        # Without the vision mark the same call is an ordinary selectorless clear:
        # heal owns it, and clear has no coord_runner, so an authoritative miss ends
        # it rather than degrading into a blind tap at the recorded point.
        with pytest.raises(ElementNotFound):
            with step("legacy clear"):
                clear(
                    driver, selectors=None, description="the coupon field",
                    fallback_coordinates=BASIS,
                )


class TestTypeFamily:
    def test_type_focuses_clears_and_sends(self):
        """Focus precedes the clear: clearing is destructive, and an unfocused
        field is not necessarily the one the keys will reach."""
        el = _El()
        with step("s"):
            type_(_found(el), selectors=SELECTORS, text="hello", description="Field")
        assert el.calls == [("click",), ("clear",), ("send_keys", "hello")]

    def test_timing_splits_focus_clear_and_send_keys(self):
        el = _El()
        with testmu_appium.capture_action_timings() as timings:
            with step("s"):
                type_(_found(el), selectors=SELECTORS, text="hello")

        [timing] = timings
        assert timing["counts"]["focus_commands"] == 1
        assert timing["counts"]["clear_commands"] == 1
        assert timing["counts"]["send_keys_commands"] == 1
        assert {"focus", "clear", "send_keys"} <= timing[
            "action_phases_ms"
        ].keys()

    @pytest.mark.parametrize("flag", ["multiple_inputs", "manual_interaction_tag"])
    def test_clear_is_skipped_for_the_recorded_flags(self, flag):
        el = _El()
        with step("s"):
            type_(_found(el), selectors=SELECTORS, text="hello", **{flag: True})
        assert ("clear",) not in el.calls

    def test_type_resolves_variables(self):
        from testmu_appium._vars import set_var

        set_var("who", "world")
        el = _El()
        with step("s"):
            type_(_found(el), selectors=SELECTORS, text="hello {{who}}")
        assert ("send_keys", "hello world") in el.calls

    def test_search_submits_with_the_enter_key_event(self):
        el = _El()
        driver = _found(el)
        with step("s"):
            search(driver, selectors=SELECTORS, text="pizza")
        assert ("send_keys", "pizza") in el.calls
        assert driver.keycodes == [66]

    def test_search_does_not_send_a_newline(self):
        el = _El()
        with step("s"):
            search(_found(el), selectors=SELECTORS, text="pizza")
        assert all("\n" not in str(c[-1]) for c in el.calls if c[0] == "send_keys")

    def test_clear_focuses_then_clears(self):
        el = _El()
        with step("s"):
            clear(_found(el), selectors=SELECTORS)
        assert el.calls == [("click",), ("clear",)]

    def test_clear_has_no_coordinate_fallback(self, monkeypatch):
        monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))
        with pytest.raises(ElementNotFound):
            with step("s"):
                clear(_Driver(queue=[[]]), selectors=SELECTORS, fallback_coordinates=BASIS)


class TestSelect:
    def test_spinner_opens_then_taps_the_option(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        option = _El()
        driver = _Driver(queue=[[spinner], [option]])
        with step("s"):
            select(driver, selectors=SELECTORS, value="Delhi")
        assert spinner.calls == [("click",)]
        assert option.calls == [("click",)]
        assert 'text("Delhi")' in driver.find_calls[1][1]

    def test_spinner_option_must_be_unique(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        driver = _Driver(queue=[[spinner], [_El(), _El()]])
        with pytest.raises(ValueError):
            with step("s"):
                select(driver, selectors=SELECTORS, value="Delhi")

    def test_spinner_waits_for_the_options_list_to_render(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        option = _El()
        driver = _Driver(queue=[[spinner], [], [], [option]])
        with step("s"):
            select(driver, selectors=SELECTORS, value="Delhi")
        assert option.calls == [("click",)]
        assert len(driver.find_calls) == 4

    def test_spinner_index_waits_for_the_options_list_to_render(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        first, second = _El(), _El()
        driver = _Driver(queue=[[spinner], [], [first, second]])
        with step("s"):
            select(driver, selectors=SELECTORS, index=1)
        assert second.calls == [("click",)]

    def test_spinner_gives_up_when_options_never_render(self, monkeypatch):
        from testmu_appium._helpers import picker
        monkeypatch.setattr(picker, "_SPINNER_OPTIONS_SETTLE_S", 0.05)
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        driver = _Driver(queue=[[spinner]])
        with pytest.raises(ValueError) as exc:
            with step("s"):
                select(driver, selectors=SELECTORS, value="Delhi")
        assert "matched 0 entries" in str(exc.value)

    def test_spinner_ambiguity_is_answered_without_extra_polls(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        driver = _Driver(queue=[[spinner], [_El(), _El()]])
        with pytest.raises(ValueError):
            with step("s"):
                select(driver, selectors=SELECTORS, value="Delhi")
        assert len(driver.find_calls) == 2

    def test_number_picker_scrolls_to_the_value(self):
        picker = _El(attributes={"class": "android.widget.NumberPicker"},
                     texts=["5", "4", "3"])
        driver = _found(picker)
        with step("s"):
            select(driver, selectors=SELECTORS, value="3")
        assert [s[0] for s in driver.scripts] == ["mobile: scrollGesture"] * 2

    def test_number_picker_stops_when_it_makes_no_progress(self):
        picker = _El(attributes={"class": "android.widget.NumberPicker"}, texts=["5"])
        with pytest.raises(ValueError) as exc:
            with step("s"):
                select(_found(picker), selectors=SELECTORS, value="99")
        assert "did not reach" in str(exc.value)

    def test_number_picker_already_on_target_does_not_scroll(self):
        picker = _El(attributes={"class": "android.widget.NumberPicker"}, texts=["7"])
        driver = _found(picker)
        with step("s"):
            select(driver, selectors=SELECTORS, value="7")
        assert driver.scripts == []

    def test_spinner_index_is_scoped_to_the_picker_list_container(self):
        """`clickable(true)` over the whole screen also collects the toolbar, the FAB
        and everything behind the dialog, in an order nothing guarantees, so the
        positional lookup is scoped to the picker list."""
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        driver = _Driver(queue=[[spinner], [_El(), _El()]])
        with step("s"):
            select(driver, selectors=SELECTORS, index=1)
        lookup = driver.find_calls[1][1]
        assert "android:id/select_dialog_listview" in lookup
        assert "childSelector" in lookup
        assert "clickable(true)" in lookup

    def test_spinner_index_lookup_is_not_a_bare_screen_wide_clickable_scan(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        driver = _Driver(queue=[[spinner], [_El()]])
        with step("s"):
            select(driver, selectors=SELECTORS, index=0)
        assert driver.find_calls[1][1] != "new UiSelector().clickable(true)"

    @pytest.mark.parametrize("value,expected_x", [("50", 200), ("0.25", 150), ("100", 300)])
    def test_slider_drags_to_the_percentage(self, value, expected_x):
        slider = _El(attributes={"class": "android.widget.SeekBar"})
        driver = _found(slider)
        with step("s"):
            select(driver, selectors=SELECTORS, value=value)
        script, args = driver.scripts[0]
        assert script == "mobile: dragGesture"
        assert args["endX"] == expected_x

    def test_slider_drag_starts_at_the_left_edge_of_the_track(self):
        """The drag grabs the track at its left edge and moves right by the recorded
        proportion."""
        slider = _El(attributes={"class": "android.widget.SeekBar"})
        driver = _found(slider)
        with step("s"):
            select(driver, selectors=SELECTORS, value="50")
        args = driver.scripts[0][1]
        assert args["startX"] == 100      # rect x, not x + width // 2
        assert args["startY"] == args["endY"] == 250

    def test_a_fifty_percent_slider_target_is_not_a_no_op_drag(self):
        slider = _El(attributes={"class": "android.widget.SeekBar"})
        driver = _found(slider)
        with step("s"):
            select(driver, selectors=SELECTORS, value="50")
        args = driver.scripts[0][1]
        assert args["startX"] != args["endX"]

    @pytest.mark.parametrize("value,expected_x", [("0", 100), ("100", 300)])
    def test_slider_extremes_reach_the_track_ends(self, value, expected_x):
        slider = _El(attributes={"class": "android.widget.SeekBar"})
        driver = _found(slider)
        with step("s"):
            select(driver, selectors=SELECTORS, value=value)
        assert driver.scripts[0][1]["endX"] == expected_x

    def test_slider_requires_a_numeric_value(self):
        slider = _El(attributes={"class": "android.widget.SeekBar"})
        with pytest.raises(ValueError):
            with step("s"):
                select(_found(slider), selectors=SELECTORS, value="loud")

    @pytest.mark.parametrize("mode,widget", [
        ("wheel_column", "wheel-column"), ("dial", "clock-face dial"),
    ])
    def test_deferred_picker_modes_raise_naming_the_widget(self, mode, widget):
        with pytest.raises(PickerModeNotSupported) as exc:
            with step("s"):
                select(_found(_El()), selectors=SELECTORS, value="AM", mode=mode)
        assert widget in str(exc.value)
        assert exc.value.mode == mode

    def test_unknown_mode_raises(self):
        with pytest.raises(ValueError):
            with step("s"):
                select(_found(_El()), selectors=SELECTORS, value="x", mode="carousel")


class TestSelectTargetPrecedence:
    """value / label / index reach the mode that knows which of them applies.

    All three are carried through the entry point rather than collapsed into one
    string, because a spinner matches on the label and a wheel or slider on the value.
    """

    def _spinner(self, option=None):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        return _Driver(queue=[[spinner], [option or _El()]])

    def test_a_spinner_taps_the_option_carrying_the_recorded_label(self):
        driver = self._spinner()
        with step("s"):
            select(driver, selectors=SELECTORS, value="IN", label="India")
        assert 'text("India")' in driver.find_calls[1][1]
        assert "IN" not in driver.find_calls[1][1]

    def test_a_spinner_falls_back_to_the_value_when_no_label_was_recorded(self):
        driver = self._spinner()
        with step("s"):
            select(driver, selectors=SELECTORS, value="India")
        assert 'text("India")' in driver.find_calls[1][1]

    def test_a_spinner_uses_the_index_only_when_no_text_was_recorded(self):
        spinner = _El(attributes={"class": "android.widget.Spinner"})
        first, second = _El(), _El()
        driver = _Driver(queue=[[spinner], [first, second]])
        with step("s"):
            select(driver, selectors=SELECTORS, index=1)
        assert second.calls == [("click",)]

    def test_a_recorded_label_beats_a_recorded_index_on_a_spinner(self):
        """The cgf golden `v4_appium_clear_select` records label="India" AND index=3."""
        driver = self._spinner()
        with step("s"):
            select(driver, selectors=SELECTORS, label="India", index=3)
        assert 'text("India")' in driver.find_calls[1][1]

    def test_a_number_picker_targets_the_value_not_the_label(self):
        picker = _El(attributes={"class": "android.widget.NumberPicker"},
                     texts=["5", "4", "3"])
        driver = _found(picker)
        with step("s"):
            select(driver, selectors=SELECTORS, value="3", label="Three")
        assert [s[0] for s in driver.scripts] == ["mobile: scrollGesture"] * 2

    def test_a_number_picker_falls_back_to_the_label_when_no_value_was_recorded(self):
        picker = _El(attributes={"class": "android.widget.NumberPicker"}, texts=["7"])
        driver = _found(picker)
        with step("s"):
            select(driver, selectors=SELECTORS, label="7")
        assert driver.scripts == []

    def test_a_slider_reads_the_value_not_the_label(self):
        slider = _El(attributes={"class": "android.widget.SeekBar"})
        driver = _found(slider)
        with step("s"):
            select(driver, selectors=SELECTORS, value="25", label="a quarter")
        assert driver.scripts[0][1]["endX"] == 150

    @pytest.mark.parametrize("widget,cls", [
        ("NumberPicker", "android.widget.NumberPicker"),
        ("slider", "android.widget.SeekBar"),
    ])
    def test_an_index_only_target_stays_meaningless_for_a_value_widget(self, widget, cls):
        element = _El(attributes={"class": cls}, texts=["1"])
        with pytest.raises(ValueError) as exc:
            with step("s"):
                select(_found(element), selectors=SELECTORS, index=2)
        assert "index" in str(exc.value) and widget in str(exc.value)

    def test_variables_resolve_in_both_value_and_label(self):
        from testmu_appium._vars import set_var

        set_var("country", "India")
        driver = self._spinner()
        with step("s"):
            select(driver, selectors=SELECTORS, value="{{country}}",
                   label="{{country}}")
        assert 'text("India")' in driver.find_calls[1][1]


class TestScrollStopsAtTheEnd:
    """`mobile: scrollGesture` answers whether anything is left to scroll, and
    the count loop threw that answer away.

    A run scrolled a time list to its last entry and then gestured at it twice
    more, reporting ok each time — five "successful" scrolls, two of which moved
    nothing, on a container that had been pinned since the third.
    """

    def test_a_pinned_container_is_not_gestured_at_again(self):
        class _Pinned(_Driver):
            def execute_script(self, script, args=None):
                self.scripts.append((script, args))
                return False  # nothing left to scroll, from the first gesture

        driver = _Pinned()
        with step("s"):
            scroll(driver, kind="times", direction="down", value=5)
        assert len(driver.scripts) == 1, "kept scrolling a container at its end"

    def test_a_container_with_room_still_scrolls_the_full_count(self):
        class _Endless(_Driver):
            def execute_script(self, script, args=None):
                self.scripts.append((script, args))
                return True

        driver = _Endless()
        with step("s"):
            scroll(driver, kind="times", direction="down", value=3)
        assert len(driver.scripts) == 3

    def test_reaching_the_end_is_not_a_failed_action(self):
        """A list scrolled as far as it goes did what was asked. Only a gesture
        the driver refused is a failure, and scrollGesture reports "no more
        content" rather than "I could not act".

        Failure is raised, never returned: the executor derives success purely
        from whether the verb threw. So this asserts the verb completes — the
        return value carries "is there more", not "did it work", and a caller
        that read it as success would stop on a list it had merely finished.
        """
        class _Pinned(_Driver):
            def execute_script(self, script, args=None):
                self.scripts.append((script, args))
                return False

        driver = _Pinned()
        with step("s"):
            scroll(driver, kind="times", direction="down", value=5)

    def test_the_end_is_reported_as_no_more_content(self):
        """The other half of the same contract: arriving at the end is visible
        to the caller, which is what lets a loop stop instead of re-gesturing."""
        class _Pinned(_Driver):
            def execute_script(self, script, args=None):
                self.scripts.append((script, args))
                return False

        driver = _Pinned()
        with step("s"):
            assert scroll(driver, kind="times", direction="down", value=5) is False


class TestScroll:
    def test_screen_scroll_needs_no_selectors_but_asks_what_is_scrollable(self):
        """No recorded selector is ever resolved, so the find/heal path stays out
        of it. The gesture still has to know what a thumb at the screen centre
        would move, so it asks once per verb — not once per gesture — and this
        screen reports nothing scrollable, so the rectangle stands.
        """
        driver = _Driver()
        with step("s"):
            scroll(driver, kind="times", direction="down", value=2)
        assert len(driver.find_calls) == 1
        assert [s[0] for s in driver.scripts] == ["mobile: scrollGesture"] * 2

    def test_screen_scroll_insets_the_gesture_from_the_edges(self):
        driver = _Driver()
        with step("s"):
            scroll(driver, kind="times", direction="down", value=1)
        args = driver.scripts[0][1]
        assert args["left"] == 108 and args["top"] == 351
        assert args["width"] == 864 and args["height"] == 1638

    def test_element_scroll_addresses_the_element(self):
        """The element is named, not the rectangle it occupies — a rectangle only
        says where to swipe, which reaches nothing on a container that does not
        take a synthesized touch there."""
        el = _El(rect={"x": 0, "y": 300, "width": 1080, "height": 1200})
        driver = _found(el)
        with step("s"):
            scroll(driver, selectors=SELECTORS, kind="times", direction="down", value=1)
        args = driver.scripts[0][1]
        assert args["elementId"] == "el-1"
        assert "left" not in args

    @pytest.mark.parametrize("value,fraction", [(50, 0.5), (0.5, 0.5), (0.4, 0.4), (100, 1.0)])
    def test_percent_accepts_both_fraction_and_whole_percent(self, value, fraction):
        """A screen-level percent is a share of the 2340px screen, delivered
        through the inset rectangle (1638px tall, ~three quarters of it per
        gesture); 50 and 0.5 name the same share."""
        driver = _Driver()
        with step("s"):
            scroll(driver, kind="percent", direction="down", value=value)
        inset_height = 2340 - 2 * int(2340 * 0.15)
        expected = min(1.0, (fraction * 2340) / (0.75 * inset_height))
        assert driver.scripts[0][1]["percent"] == pytest.approx(expected)

    def test_pixels_convert_to_a_fraction_of_the_area(self):
        driver = _Driver()
        with step("s"):
            scroll(driver, kind="pixels", direction="down", value=819)
        assert driver.scripts[0][1]["percent"] == pytest.approx(0.667, abs=0.01)

    def test_edge_scroll_stops_when_the_gesture_reports_no_more(self):
        driver = _Driver()
        with step("s"):
            scroll(driver, kind="edge", direction="down")
        assert len(driver.scripts) < 30

    @pytest.mark.parametrize("kind,direction", [("warp", "down"), ("times", "sideways")])
    def test_unknown_kind_or_direction_raises(self, kind, direction):
        with pytest.raises(ValueError):
            with step("s"):
                scroll(_Driver(), kind=kind, direction=direction)


class TestScrollUntil:
    def _element_at(self, y):
        return _El(rect={"x": 0, "y": y, "width": 1080, "height": 100})

    def test_returns_immediately_when_the_target_is_already_in_band(self):
        el = self._element_at(800)          # cy 850, inside the band ~[694, 1646]
        driver = _found(el)
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS) is el
        assert driver.scripts == []

    def test_scrolls_until_the_target_reaches_the_band(self):
        offscreen = self._element_at(3000)
        onscreen = self._element_at(800)     # cy 850, inside the band
        driver = _Driver(queue=[[offscreen], [onscreen]])
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS) is onscreen
        assert len(driver.scripts) == 1

    def test_a_row_straddling_the_edge_is_returned_best_effort(self):
        """A row clipped by the bottom edge is out of band — its centre unreliable —
        so it is never accepted as placed, but it is on screen, so an exhausted
        search returns it best effort rather than raising (R17)."""
        el = self._element_at(2300)         # el_bottom 2400 >= viewport 2340: clipped
        driver = _Driver(queue=[[el]] * 6)
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS, max_scrolls=2) is el

    def test_a_straddling_row_passes_a_lower_threshold(self):
        el = self._element_at(2300)
        driver = _Driver(queue=[[el]] * 6)
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS, max_scrolls=2,
                                visibility_threshold=0.3) is el

    def test_gives_up_after_the_scroll_budget(self):
        driver = _Driver(queue=[[]] * 20)
        with pytest.raises(ElementNotFound) as exc:
            with step("s"):
                scroll_until(driver, selectors=SELECTORS, max_scrolls=3,
                             description="Row")
        assert "3 scroll" in str(exc.value)

    def test_container_scope_uses_the_container_rectangle(self):
        container = _El(rect={"x": 0, "y": 400, "width": 1080, "height": 1000})
        target = self._element_at(850)      # cy 900, inside the container's band
        driver = _Driver(queue=[[container], [target]])
        containers = [{"strategy": "view_id", "selector": "com.app:id/list", "score": 90}]
        with step("s"):
            scroll_until(driver, selectors=SELECTORS, container_selectors=containers)

    def test_a_target_outside_the_container_does_not_count_as_reached(self):
        """A container-scoped search checks visibility against the container clipped
        to the screen, so a row on screen but outside the container does not count as
        reached."""
        container = _El(rect={"x": 0, "y": 400, "width": 1080, "height": 400})
        outside = self._element_at(1200)   # on screen, well below the container
        containers = [{"strategy": "view_id", "selector": "com.app:id/list", "score": 90}]
        driver = _Driver(queue=[[container]] + [[outside]] * 8)
        with pytest.raises(ElementNotFound):
            with step("s"):
                scroll_until(driver, selectors=SELECTORS, container_selectors=containers,
                             max_scrolls=2)

    def test_a_target_inside_the_container_still_counts_as_reached(self):
        container = _El(rect={"x": 0, "y": 400, "width": 1080, "height": 400})
        inside = self._element_at(600)
        containers = [{"strategy": "view_id", "selector": "com.app:id/list", "score": 90}]
        driver = _Driver(queue=[[container], [inside]])
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS,
                                container_selectors=containers) is inside

    def test_a_container_scrolled_off_screen_makes_nothing_visible(self):
        """The container clipped to the screen is empty, so no row inside it can be
        reached — a lower threshold must not paper over that."""
        container = _El(rect={"x": 0, "y": 3000, "width": 1080, "height": 400})
        containers = [{"strategy": "view_id", "selector": "com.app:id/list", "score": 90}]
        driver = _Driver(queue=[[container]] + [[self._element_at(600)]] * 8)
        with pytest.raises(ElementNotFound):
            with step("s"):
                scroll_until(driver, selectors=SELECTORS, container_selectors=containers,
                             max_scrolls=2, visibility_threshold=0.1)

    def test_screen_scoped_visibility_still_uses_the_whole_screen(self):
        """Without a container the gesture area is inset from the screen edges; an
        element sitting inside that inset band is still visible."""
        in_the_inset_band = self._element_at(60)   # above the 15% vertical inset
        driver = _found(in_the_inset_band)
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS) is in_the_inset_band

    def test_a_missing_container_degrades_to_a_screen_search(self):
        """R5: a recorded container that is not on screen must not raise on its own.
        The search falls back to the screen and the target is still reachable —
        bringing the container on screen is a separate outer loop's concern."""
        target = self._element_at(800)     # cy 850, inside the screen band
        # The container query misses (empty), then the target is found on screen.
        driver = _Driver(queue=[[], [target]])
        containers = [{"strategy": "view_id", "selector": "com.app:id/list", "score": 90}]
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS,
                                container_selectors=containers) is target

    def test_an_on_screen_out_of_band_target_is_nudged_into_the_band(self):
        """Once the search brings the target on screen but out of band, the sized
        nudge finishes the placement: it scrolls the container and the target ends
        in band, rather than being returned out of band as best effort."""
        containers = [{"strategy": "view_id", "selector": "com.app:id/list", "score": 90}]
        container = _El(rect={"x": 0, "y": 400, "width": 1080, "height": 1000})
        out_of_band = self._element_at(1280)   # cy 1330, below the container band
        in_band_now = self._element_at(800)    # cy 850, inside it after one nudge
        # gesture_target → container; _placed → out_of_band; nudge re-finds
        # out_of_band (scrolls), then in_band_now (placed).
        driver = _Driver(queue=[[container], [out_of_band], [out_of_band], [in_band_now]])
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS,
                                container_selectors=containers) is in_band_now
        gestures = sum(1 for name, _ in driver.scripts if name == "mobile: scrollGesture")
        assert gestures >= 1, "the nudge must actually scroll the container"

    def test_the_nudge_returns_best_effort_when_it_cannot_reach_the_band(self):
        """A target that stays out of band under the nudge — a gesture moves it no
        further — is returned best effort, not raised, and the nudge stops rather
        than spending its whole budget (R17)."""
        containers = [{"strategy": "view_id", "selector": "com.app:id/list", "score": 90}]
        container = _El(rect={"x": 0, "y": 400, "width": 1080, "height": 1000})
        stuck = self._element_at(1280)          # cy 1330, out of band, never moves
        driver = _Driver(queue=[[container]] + [[stuck]] * 8)
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS,
                                container_selectors=containers) is stuck
        gestures = sum(1 for name, _ in driver.scripts if name == "mobile: scrollGesture")
        assert gestures <= BAND_NUDGE_MAX_GESTURES, "a nudge is bounded, never a search"

    def test_requires_selectors(self):
        with pytest.raises(ValueError):
            with step("s"):
                scroll_until(_Driver(), selectors=[])

    # --- vision-judged mode (a condition is present) ------------------------

    def _vision(self, monkeypatch, answers):
        """Patch the per-pass vision check to a scripted yes/no sequence (then a
        terminal False), so a test never reaches the real analyzer."""
        import testmu_appium._action_scroll_until as _su
        calls = {"n": 0}

        def _fake(driver, condition, perception=None):
            i = calls["n"]
            calls["n"] += 1
            return answers[i] if i < len(answers) else False

        monkeypatch.setattr(_su, "check_until_condition", _fake)
        return calls

    def test_a_met_condition_returns_without_scrolling(self, monkeypatch):
        self._vision(monkeypatch, [True])
        driver = _Driver()
        with step("s"):
            assert scroll_until(driver, condition="the Free plan is visible") is None
        assert driver.scripts == []

    def test_scrolls_until_the_condition_holds(self, monkeypatch):
        self._vision(monkeypatch, [False, False, True])
        driver = _Driver()
        with step("s"):
            assert scroll_until(driver, condition="the Free plan is visible") is None
        gestures = [s for s in driver.scripts if s[0] == "mobile: scrollGesture"]
        assert len(gestures) == 2

    def test_a_condition_needs_no_recorded_selector(self, monkeypatch):
        """The condition is the whole handle — the target may carry no ref (D8)."""
        self._vision(monkeypatch, [True])
        driver = _Driver()
        with step("s"):
            assert scroll_until(driver, condition="the banner reads Welcome") is None

    def test_a_condition_that_never_holds_raises_at_the_end_of_the_list(self, monkeypatch):
        self._vision(monkeypatch, [])   # every pass answers no
        driver = _NoMoreContent()       # nothing scrolls → the true end is reached at once
        with pytest.raises(ElementNotFound) as exc:
            with step("s"):
                scroll_until(driver, condition="the checkout button is visible",
                             max_scrolls=3)
        assert "end of the list" in str(exc.value)

    def test_a_condition_chunk_that_spends_its_budget_hands_off(self, monkeypatch):
        """A chunk that spends its budget with the list still moving returns (it did
        its share of the travel) rather than raising, so the next scroll_until op in a
        chained search continues from here. Only the true end raises."""
        self._vision(monkeypatch, [])   # never holds within this chunk
        driver = _Driver()              # base: content keeps moving on every scroll
        with step("s"):
            assert scroll_until(driver, condition="a far row is visible",
                                max_scrolls=3) is None
        gestures = [s for s in driver.scripts if s[0] == "mobile: scrollGesture"]
        assert len(gestures) == 3       # spent the budget, then handed off

    def test_a_condition_scrolls_the_recorded_container(self, monkeypatch):
        self._vision(monkeypatch, [False, True])
        container = _El(rect={"x": 0, "y": 400, "width": 1080, "height": 1000},
                        element_id="box")
        containers = [{"strategy": "view_id", "selector": "com.app:id/box", "score": 90}]
        driver = _Driver(found={"com.app:id/box": [container]})
        with step("s"):
            scroll_until(driver, condition="the row is visible",
                         container_selectors=containers)
        gestures = [s[1] for s in driver.scripts if s[0] == "mobile: scrollGesture"]
        assert gestures and all(a.get("elementId") == "box" for a in gestures)

    # --- R6: a target revealed by the final (end-of-content) gesture ---------

    def test_a_target_revealed_by_the_final_gesture_is_found(self):
        """R6 (geometric): the last gesture can scroll the target into view while
        reporting no more content; the loop must re-check before giving up."""
        offscreen = self._element_at(3000)
        onscreen = self._element_at(600)
        driver = _NoMoreContent(queue=[[offscreen], [onscreen]])
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS) is onscreen

    def test_a_condition_met_by_the_final_gesture_is_caught(self, monkeypatch):
        """R6 (vision): the terminal gesture reports no more content but may itself
        reveal the target, so the final screen is re-checked before giving up."""
        self._vision(monkeypatch, [False, True])   # unmet, then met after the last scroll
        driver = _NoMoreContent()
        with step("s"):
            assert scroll_until(driver, condition="the row is visible") is None
        gestures = [s for s in driver.scripts if s[0] == "mobile: scrollGesture"]
        assert len(gestures) == 1


class _NoMoreContent(_Driver):
    """Every scroll gesture moves nothing, so the loop takes its end-of-content
    branch on the first scroll. The screen fingerprint is frozen — the reliable
    end signal now that the loop no longer trusts the gesture's own canScrollMore."""

    page_source = "<hierarchy scrolls='end'/>"

    def execute_script(self, script, args=None):
        self.scripts.append((script, args))
        return script != "mobile: scrollGesture"


class TestDrag:
    def test_drags_between_the_scaled_coordinate_bases(self):
        driver = _Driver()
        source = dict(BASIS, x_ratio=0.1, y_ratio=0.2)
        target = dict(BASIS, x_ratio=0.9, y_ratio=0.8)
        with step("s"):
            drag(driver, source_coordinates=source, target_coordinates=target,
                 hold_duration_ms=500, move_duration_ms=1000)
        script, args = driver.scripts[0]
        assert script == "mobile: dragGesture"
        assert (args["startX"], args["startY"]) == (108, 468)
        assert (args["endX"], args["endY"]) == (972, 1872)
        assert args["holdDuration"] == 500 and args["moveDuration"] == 1000

    def test_durations_are_optional(self):
        driver = _Driver()
        with step("s"):
            drag(driver, source_coordinates=BASIS, target_coordinates=BASIS)
        args = driver.scripts[0][1]
        assert "holdDuration" not in args and "moveDuration" not in args

    def test_orientation_mismatch_refuses_the_drag(self):
        driver = _Driver(window=(2340, 1080))
        with pytest.raises(CoordinateFallbackUnavailable):
            with step("s"):
                drag(driver, source_coordinates=BASIS, target_coordinates=BASIS)

    def test_both_ends_are_required(self):
        with pytest.raises(ValueError):
            with step("s"):
                drag(_Driver(), source_coordinates=BASIS, target_coordinates=None)

    def test_never_finds_an_element(self):
        driver = _Driver()
        with step("s"):
            drag(driver, source_coordinates=BASIS, target_coordinates=BASIS)
        assert driver.find_calls == []


class TestDragGroundedByVision:
    """A drag authored by vision replays by vision.

    The mechanism that grounded the action is the mechanism that re-grounds it:
    a screen the tree never described has no selector to find, and routing such a
    recording through the tree would replay something authoring never did.
    """

    def _patch_vision(self, monkeypatch, result=(700, 900)):
        calls = []

        def _fake(driver, description, action_type="click"):
            calls.append(description)
            if isinstance(result, Exception):
                raise result
            if isinstance(result, dict):
                return result[description]
            return result

        monkeypatch.setattr(
            "testmu_appium._action_drag.get_vision_coordinates", _fake
        )
        return calls

    def test_a_named_destination_is_resolved_rather_than_travelled_towards(
        self, monkeypatch
    ):
        """A direction and a fraction can only approach a destination, never
        arrive at one: the distance is a guess about a place the recording never
        located. Naming the destination makes the end point a measurement.
        """
        calls = self._patch_vision(monkeypatch, result={
            "the green ball": (540, 2036),
            "Zone 3": (300, 800),
        })
        driver = _Driver()
        with step("s"):
            drag(driver, grounded_by="vision", source_description="the green ball",
                 target_description="Zone 3")
        assert calls == ["the green ball", "Zone 3"]
        script = driver.scripts[0][1]
        assert (script["startX"], script["startY"]) == (540, 2036)
        assert (script["endX"], script["endY"]) == (300, 800)

    def test_a_destination_needs_no_direction(self, monkeypatch):
        """Direction exists to point a displacement. A destination is a place."""
        self._patch_vision(monkeypatch, result={"a": (1, 2), "b": (3, 4)})
        driver = _Driver()
        with step("s"):
            drag(driver, grounded_by="vision", source_description="a",
                 target_description="b")
        assert driver.scripts

    def test_a_destination_and_a_displacement_together_are_refused(self, monkeypatch):
        """Two different end points, and no rule saying which wins. Silently
        preferring one drops an instruction the recording carried."""
        self._patch_vision(monkeypatch, result={"a": (1, 2), "b": (3, 4)})
        driver = _Driver()
        with pytest.raises(ValueError, match="direction"):
            with step("s"):
                drag(driver, grounded_by="vision", source_description="a",
                     target_description="b", direction="up")

    def test_a_destination_that_cannot_be_found_refuses(self, monkeypatch):
        """Half a resolved path is not a degraded drag — it is a drag to
        somewhere the recording never named."""
        def _fake(driver, description, action_type="click"):
            if description == "gone":
                raise RuntimeError("element not found")
            return (1, 2)

        monkeypatch.setattr(
            "testmu_appium._action_drag.get_vision_coordinates", _fake
        )
        driver = _Driver()
        with pytest.raises(RuntimeError):
            with step("s"):
                drag(driver, grounded_by="vision", source_description="here",
                     target_description="gone")
        assert driver.scripts == []

    def test_the_description_is_resolved_by_vision_not_the_tree(self, monkeypatch):
        calls = self._patch_vision(monkeypatch)
        driver = _Driver()
        with step("s"):
            drag(driver, grounded_by="vision", source_description="the Drag me chip",
                 direction="right")
        assert calls == ["the Drag me chip"]
        assert driver.find_calls == [], "went to the tree for a vision recording"
        assert driver.scripts[0][1]["startX"] == 700

    def test_selectors_are_ignored_when_vision_did_the_grounding(self, monkeypatch):
        """Stale selectors must not silently promote a vision recording to an
        element one — that is the drift provenance exists to prevent."""
        self._patch_vision(monkeypatch)
        driver = _found(_El())
        with step("s"):
            drag(driver, grounded_by="vision", selectors=SELECTORS,
                 source_description="the chip", direction="right")
        assert driver.find_calls == []

    def test_vision_failing_refuses_rather_than_replaying_a_ratio(self, monkeypatch):
        """D5 holds here too: the recorded ratio describes a screen this drag was
        never resolving against."""
        self._patch_vision(monkeypatch, result=RuntimeError("element not found"))
        driver = _Driver()
        with pytest.raises(RuntimeError):
            with step("s"):
                drag(driver, grounded_by="vision", source_description="gone",
                     direction="right", source_coordinates=BASIS,
                     target_coordinates=BASIS)
        assert driver.scripts == []

    def test_a_found_element_may_drag_to_a_vision_destination(self, monkeypatch):
        """Provenance is per ANCHOR, not per action.

        A source the tree resolved has selectors — the strongest handle there is
        — and the destination needing vision says nothing about it. Re-resolving
        the source visually would discard a locator that works.
        """
        calls = self._patch_vision(monkeypatch, result={"Zone 3": (300, 800)})
        driver = _found(_El())
        with step("s"):
            drag(driver, grounded_by="tree", selectors=SELECTORS,
                 target_description="Zone 3")
        assert driver.find_calls, "the source was not looked up in the tree"
        assert calls == ["Zone 3"], "vision resolved something other than the destination"
        script = driver.scripts[0][1]
        assert (script["endX"], script["endY"]) == (300, 800)

    def test_source_and_destination_can_both_replay_through_selectors(self):
        source = _El(
            rect={"x": 100, "y": 200, "width": 100, "height": 100},
            element_id="source",
        )
        target = _El(
            rect={"x": 700, "y": 900, "width": 200, "height": 200},
            element_id="target",
        )
        driver = _Driver(queue=[[source], [target]])
        with step("drag card"):
            drag(
                driver,
                selectors=SELECTORS,
                grounded_by="tree",
                source_description="the QA pass card",
                target_selectors=TARGET_SELECTORS,
                target_grounded_by="tree",
                target_description="the Done column",
            )
        assert driver.scripts == [
            ("mobile: dragGesture", {
                "startX": 150, "startY": 250,
                "endX": 800, "endY": 1000,
            })
        ]
        assert len(driver.find_calls) == 2

    def test_tree_destination_requires_selectors(self):
        with pytest.raises(ValueError, match="target_selectors"):
            drag(
                _Driver(),
                grounded_by="vision",
                source_description="the card",
                target_grounded_by="tree",
                target_description="the Done column",
            )

    def test_vision_destination_refuses_stale_target_selectors(self):
        with pytest.raises(ValueError, match="cannot carry target_selectors"):
            drag(
                _Driver(),
                grounded_by="vision",
                source_description="the card",
                target_grounded_by="vision",
                target_description="the Done column",
                target_selectors=TARGET_SELECTORS,
            )

    def test_an_element_drag_needs_an_end_point_of_some_kind(self, monkeypatch):
        driver = _found(_El())
        with pytest.raises(ValueError, match="direction"):
            with step("s"):
                drag(driver, grounded_by="tree", selectors=SELECTORS)

    def test_a_tree_recording_with_no_selectors_refuses_rather_than_degrading(self):
        """"Grounded by the tree" and no selectors is a contradiction.

        Falling through to the coordinate arm replays two remembered ratios for
        an action that was authored against a found element — a mis-aimed drag
        that moves something rather than missing, which is what D5 forbids.
        """
        driver = _Driver()
        with pytest.raises(ValueError, match="grounded_by"):
            with step("s"):
                drag(driver, grounded_by="tree", source_coordinates=BASIS,
                     target_coordinates=BASIS, direction="right")
        assert driver.scripts == []

    def test_a_tree_recording_still_goes_to_the_tree(self, monkeypatch):
        calls = self._patch_vision(monkeypatch)
        driver = _found(_El())
        with step("s"):
            drag(driver, grounded_by="tree", selectors=SELECTORS, direction="right")
        assert calls == [], "a tree recording must not call vision first"
        assert driver.find_calls


class TestDragOverAnElement:
    """Selectors make a drag an element verb: it finds the control, then measures
    the gesture against the screen in front of it rather than replaying a
    distance recorded on another one."""

    def test_a_direction_drag_starts_at_the_edge_the_slide_begins_from(self):
        """A direction drag IS slide-to-act, and a slide's thumb rests at the
        origin of its travel — the element's centre is empty rail there.
        Measured (sessions 20260805-*): every centre-started slide moved
        nothing; every start on the thumb confirmed. Half the cross-axis in
        from the edge, because a thumb is a circle about as wide as its track
        is tall."""
        el = _El(rect={"x": 100, "y": 200, "width": 200, "height": 100})
        driver = _found(el)
        with step("s"):
            drag(driver, selectors=SELECTORS, direction="right",
                 source_description="Slide to pay")
        script, args = driver.scripts[0]
        assert script == "mobile: dragGesture"
        assert (args["startX"], args["startY"]) == (150, 250)

    def test_a_leftward_slide_starts_at_the_right_edge(self):
        el = _El(rect={"x": 100, "y": 200, "width": 200, "height": 100})
        driver = _found(el)
        with step("s"):
            drag(driver, selectors=SELECTORS, direction="left")
        args = driver.scripts[0][1]
        assert (args["startX"], args["startY"]) == (250, 250)

    def test_a_vertical_slide_starts_at_its_origin_edge_too(self):
        el = _El(rect={"x": 100, "y": 200, "width": 200, "height": 60})
        driver = _found(el)
        with step("s"):
            drag(driver, selectors=SELECTORS, direction="up")
        args = driver.scripts[0][1]
        assert (args["startX"], args["startY"]) == (200, 200 + 60 - 30)

    def test_an_edge_start_stays_clear_of_the_screen_edge(self):
        """A start ON the screen edge is a system gesture (Android back), not
        a touch the app sees — same guard the end point has always had."""
        el = _El(rect={"x": 0, "y": 200, "width": 30, "height": 30})
        driver = _found(el)
        with step("s"):
            drag(driver, selectors=SELECTORS, direction="right")
        assert driver.scripts[0][1]["startX"] == 24

    def test_a_destination_drag_keeps_the_centre(self, monkeypatch):
        """Dragging the element SOMEWHERE moves the element itself, and its
        centre is the one point guaranteed inside it."""
        monkeypatch.setattr(
            "testmu_appium._action_drag.get_vision_coordinates",
            lambda driver, description, action_type="click": (700, 900))
        el = _El(rect={"x": 100, "y": 200, "width": 200, "height": 100})
        driver = _found(el)
        with step("s"):
            drag(driver, selectors=SELECTORS, target_description="zone 3")
        args = driver.scripts[0][1]
        assert (args["startX"], args["startY"]) == (200, 250)
        assert (args["endX"], args["endY"]) == (700, 900)

    def test_the_travel_is_measured_on_the_live_screen_not_the_recording(self):
        """Room to the edge, less the 24px inset that keeps a horizontal drag
        clear of the Android back gesture."""
        el = _El(rect={"x": 100, "y": 200, "width": 200, "height": 100})
        driver = _found(el)
        with step("s"):
            drag(driver, selectors=SELECTORS, direction="right")
        args = driver.scripts[0][1]
        assert args["endX"] == 1080 - 24
        assert args["endY"] == 250

    def test_a_fraction_shortens_the_travel(self):
        el = _El(rect={"x": 100, "y": 200, "width": 200, "height": 100})
        driver = _found(el)
        with step("s"):
            drag(driver, selectors=SELECTORS, direction="right", fraction=0.5)
        assert driver.scripts[0][1]["endX"] == 150 + (1080 - 24 - 150) // 2

    def test_an_unknown_direction_never_reaches_the_device(self):
        driver = _found(_El())
        with pytest.raises(ValueError):
            with step("s"):
                drag(driver, selectors=SELECTORS, direction="sideways")

    def test_a_drag_that_cannot_find_its_element_does_not_fall_back_to_ratios(self):
        """D5. A recorded position describes the layout that has just failed to
        produce the element, so it is least trustworthy exactly here — and a drag
        aimed at the wrong place moves something rather than missing."""
        driver = _Driver()
        with pytest.raises(ElementNotFound):
            with step("s"):
                drag(driver, selectors=SELECTORS, direction="right",
                     source_coordinates=BASIS, target_coordinates=BASIS)
        assert driver.scripts == []


class _ActiveElement:
    def __init__(self):
        self.cleared = 0

    def clear(self):
        self.cleared += 1


class _SwitchTo:
    def __init__(self, active_element):
        self.active_element = active_element


class _CoordDriver(_Driver):
    """A driver whose recorded strategies always miss, exposing an active element."""

    def __init__(self):
        super().__init__(queue=[[]])
        self.active = _ActiveElement()
        self.switch_to = _SwitchTo(self.active)


@pytest.fixture
def _exhausted(monkeypatch):
    monkeypatch.setattr(_action_engine, "autoheal", lambda *a, **kw: HealNoMatch("gone"))


class TestCoordinatePathHonoursClearFirst:
    """clear_first describes the FIELD ("this is a replace, not an append"), so it
    applies just as much when the field was reached by coordinates."""

    def test_type_clears_at_the_tapped_point_by_default(self, _exhausted):
        driver = _CoordDriver()
        with step("s"):
            type_(driver, selectors=SELECTORS, text="hi", fallback_coordinates=BASIS)
        assert driver.active.cleared == 1
        assert [s[0] for s in driver.scripts] == ["mobile: clickGesture", "mobile: type"]

    def test_type_skips_the_clear_when_clear_first_is_false(self, _exhausted):
        driver = _CoordDriver()
        with step("s"):
            type_(driver, selectors=SELECTORS, text="hi", clear_first=False,
                  fallback_coordinates=BASIS)
        assert driver.active.cleared == 0

    @pytest.mark.parametrize("flag", ["multiple_inputs", "manual_interaction_tag"])
    def test_the_sequence_flags_suppress_the_clear_here_too(self, _exhausted, flag):
        driver = _CoordDriver()
        with step("s"):
            type_(driver, selectors=SELECTORS, text="hi", clear_first=True,
                  fallback_coordinates=BASIS, **{flag: True})
        assert driver.active.cleared == 0

    def test_search_clears_at_the_tapped_point_too(self, _exhausted):
        driver = _CoordDriver()
        with step("s"):
            search(driver, selectors=SELECTORS, text="hi", fallback_coordinates=BASIS)
        assert driver.active.cleared == 1
        assert driver.keycodes == [66]

    def test_search_skips_the_clear_when_clear_first_is_false(self, _exhausted):
        driver = _CoordDriver()
        with step("s"):
            search(driver, selectors=SELECTORS, text="hi", clear_first=False,
                   fallback_coordinates=BASIS)
        assert driver.active.cleared == 0

    def test_the_clear_happens_before_the_text_is_typed(self, _exhausted):
        order = []
        driver = _CoordDriver()
        driver.active.clear = lambda: order.append("clear")
        original = driver.execute_script

        def _record(script, args=None):
            if script == "mobile: type":
                order.append("type")
            return original(script, args)

        driver.execute_script = _record
        with step("s"):
            type_(driver, selectors=SELECTORS, text="hi", fallback_coordinates=BASIS)
        assert order == ["clear", "type"]


class TestLongPressDurationZero:
    """A recorded duration of 0 is an explicit zero, not an unrecorded value falling
    back to the 800ms default."""

    @pytest.mark.parametrize("duration,expected", [
        ("0", 0), (0, 0), ("0.0", 0), ("1.5", 1500), (2, 2000),
    ])
    def test_an_explicit_duration_is_honoured_including_zero(self, duration, expected):
        driver = _found(_El())
        with step("s"):
            click(driver, selectors=SELECTORS,
                  click_modifier={"kind": "long_press", "duration": duration})
        assert driver.scripts[0][1]["duration"] == expected

    def test_an_absent_duration_still_uses_the_default(self):
        driver = _found(_El())
        with step("s"):
            click(driver, selectors=SELECTORS, click_modifier={"kind": "long_press"})
        assert driver.scripts[0][1]["duration"] == 800

    def test_an_explicit_none_duration_uses_the_default(self):
        driver = _found(_El())
        with step("s"):
            click(driver, selectors=SELECTORS,
                  click_modifier={"kind": "long_press", "duration": None})
        assert driver.scripts[0][1]["duration"] == 800

    @pytest.mark.parametrize("duration,expected", [("0", 0), (None, 800)])
    def test_the_coordinate_path_agrees(self, _exhausted, duration, expected):
        driver = _CoordDriver()
        with step("s"):
            click(driver, selectors=SELECTORS, fallback_coordinates=BASIS,
                  click_modifier={"kind": "long_press", "duration": duration})
        assert driver.scripts[0][1]["duration"] == expected


class TestScrollUntilFindBudget:
    """The loop runs max_scrolls + 1 times so the LAST scroll is followed by a check.
    Each call also resolves the scrollable under the centre once (R4 — one extra
    find), and the end-of-content branch re-checks the final screen exactly once
    (R6). Beyond those there is no wasted re-find."""

    class _EndlessScroll(_Driver):
        """Always reports "more to scroll", so the budget is what stops the loop."""

        def execute_script(self, script, args=None):
            self.scripts.append((script, args))
            return True

    class _Stuck(_Driver):
        """An unscrollable area: a gesture moves nothing, so the screen fingerprint
        never changes and the loop takes its end-of-content branch on the first
        scroll."""

        page_source = "<hierarchy stuck='1'/>"

        def execute_script(self, script, args=None):
            self.scripts.append((script, args))
            return False

    @staticmethod
    def _target_finds(driver):
        """The target lookups only — the one-off scrollable resolution excluded."""
        return [c for c in driver.find_calls if "scrollable(true)" not in c[1]]

    @pytest.mark.parametrize("max_scrolls", [0, 1, 3, 7])
    def test_the_find_count_is_exactly_the_loop_count(self, max_scrolls):
        driver = self._EndlessScroll(queue=[[] for _ in range(max_scrolls + 5)])
        with pytest.raises(ElementNotFound):
            with step("s"):
                scroll_until(driver, selectors=SELECTORS, max_scrolls=max_scrolls)
        # One check per loop turn; the endless scroll never takes the R6 branch.
        assert len(self._target_finds(driver)) == max_scrolls + 1

    def test_an_early_exit_on_an_unscrollable_area_re_checks_exactly_once(self):
        """R6: a gesture that reports the end may itself have revealed the target,
        so the final screen is re-checked once — the initial check plus that single
        re-check, and no more."""
        driver = self._Stuck(queue=[[], [], [], []])
        with pytest.raises(ElementNotFound):
            with step("s"):
                scroll_until(driver, selectors=SELECTORS, max_scrolls=5)
        assert len(self._target_finds(driver)) == 2

    def test_a_target_found_on_the_last_allowed_check_still_returns(self):
        el = _El(rect={"x": 0, "y": 0, "width": 1080, "height": 200})
        driver = _Driver(queue=[[], [], [el]])
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS, max_scrolls=2) is el

    class _EndsAfter(_Driver):
        """A finite list: its fingerprint changes for `moves` gestures, then freezes
        — the movement probe's end signal, independent of the gesture's own
        (unreliable) canScrollMore."""

        def __init__(self, moves, **kw):
            super().__init__(**kw)
            self._moves = moves

        @property
        def page_source(self):
            scrolls = sum(1 for name, _ in self.scripts
                          if name == "mobile: scrollGesture")
            return f"<hierarchy scrolls='{min(scrolls, self._moves)}'/>"

        def execute_script(self, script, args=None):
            self.scripts.append((script, args))
            return True  # canScrollMore lies "yes" forever; movement is the truth

    def _gestures(self, driver):
        return [s for s in driver.scripts if s[0] == "mobile: scrollGesture"]

    def test_the_loop_stops_when_the_screen_stops_moving(self):
        """A search stops at the true end — detected by the screen no longer moving —
        well before a large budget, even though canScrollMore never says stop."""
        driver = self._EndsAfter(moves=4, queue=[[] for _ in range(60)])
        with pytest.raises(ElementNotFound):
            with step("s"):
                scroll_until(driver, selectors=SELECTORS, max_scrolls=45)
        # Four gestures move the list, the fifth moves nothing -> stop. Far below 45.
        assert len(self._gestures(driver)) == 5

    def test_a_far_target_is_crossed_within_one_chunk(self):
        """One chunk reaches a target well past the old 20-gesture cap: a row that
        only appears after 25 gestures is found inside a single 30-gesture chunk."""
        el = _El(rect={"x": 0, "y": 800, "width": 1080, "height": 200})  # cy 900, in band
        driver = self._EndsAfter(moves=99, queue=[[] for _ in range(25)] + [[el]])
        with step("s"):
            assert scroll_until(driver, selectors=SELECTORS) is el
        assert len(self._gestures(driver)) == 25


class TestScrollUntilOnTheWebSurface:
    """`surface="web"` scrolls through the page instead of gesturing at the screen.

    The DOM knows where its elements are, so the bounded scroll-and-recheck loop —
    which exists because a native tree cannot say where an unrendered row will be —
    is replaced by one call. No device gesture is issued.
    """

    WEB_SELECTORS = [{"strategy": "css", "selector": "#searchIcon", "score": 90}]

    def _patch(self, monkeypatch, channel, calls=None):
        import testmu_appium._action_scroll_until as module
        monkeypatch.setattr(module._action_web, "visible_channel",
                            lambda package="": channel)
        if calls is not None:
            monkeypatch.setattr(module._action_web, "scroll_into_view",
                                lambda ch, css: calls.append(css) or "visible")

    def test_the_page_scrolls_and_the_device_is_never_gestured(self, monkeypatch):
        calls = []
        driver = _Driver()
        self._patch(monkeypatch, object(), calls)
        with step("s"):
            assert scroll_until(driver, selectors=self.WEB_SELECTORS,
                                surface="web") is None
        assert calls == ["#searchIcon"]
        assert driver.scripts == [], "a web scroll must not gesture at the screen"

    def test_a_target_the_page_does_not_have_is_not_found(self, monkeypatch):
        import testmu_appium._action_scroll_until as module
        self._patch(monkeypatch, object())
        monkeypatch.setattr(module._action_web, "scroll_into_view",
                            lambda ch, css: "missing")
        with pytest.raises(ElementNotFound):
            with step("s"):
                scroll_until(_Driver(), selectors=self.WEB_SELECTORS, surface="web")

    def test_a_failed_page_scroll_is_not_reported_as_success(self, monkeypatch):
        import testmu_appium._action_scroll_until as module

        self._patch(monkeypatch, object())
        monkeypatch.setattr(
            module._action_web, "scroll_into_view", lambda channel, css: None
        )
        with pytest.raises(ElementNotFound, match="failed while scrolling"):
            with step("s"):
                scroll_until(
                    _Driver(), selectors=self.WEB_SELECTORS, surface="web"
                )

    def test_a_missing_web_scroll_target_uses_the_normal_autoheal_tree(
            self, monkeypatch):
        import testmu_appium._action_scroll_until as module
        from testmu_appium._heal import WebHealHit

        descriptor = {
            "label": "Search", "tag": "BUTTON", "role": "button",
            "path": "", "dom_path": [{"kind": "element", "nodes": [0, 2]}],
            "editable": False,
        }
        self._patch(monkeypatch, object())
        monkeypatch.setattr(
            module._action_web, "scroll_into_view",
            lambda channel, css: "missing",
        )
        monkeypatch.setattr(
            module._action_web, "open_unplaced_surface",
            lambda channel: object(),
        )
        monkeypatch.setattr(
            module, "autoheal_web",
            lambda driver, surface, description, action_type, **kwargs:
                WebHealHit(descriptor, 4, "Search control"),
        )
        monkeypatch.setattr(
            module, "_scroll_healed_descriptor",
            lambda channel, chosen, deadline=None:
                "visible" if chosen is descriptor else None,
        )

        with step("Scroll Search") as recorded:
            assert scroll_until(
                _Driver(),
                selectors=self.WEB_SELECTORS,
                description="Search control",
                surface="web",
            ) is None
        assert recorded.is_autohealed is True

    def test_web_scroll_reacquires_the_visible_channel_after_heal(
            self, monkeypatch):
        from types import SimpleNamespace

        import testmu_appium._action_scroll_until as module
        from testmu_appium import _action_web
        from testmu_appium._heal import WebHealHit

        element = {
            "label": "Search", "tag": "BUTTON", "role": "",
            "path": "", "dom_path": [{"kind": "element", "nodes": [0, 2]}],
            "interactive": True, "editable": False, "disabled": False,
        }
        descriptor = _action_web.descriptor_for(element)
        before_heal, after_heal = object(), object()
        channels = [before_heal, after_heal]
        scrolled = []
        monkeypatch.setattr(
            module._action_web, "visible_channel",
            lambda package="": channels.pop(0),
        )
        monkeypatch.setattr(
            module._action_web, "open_unplaced_surface",
            lambda channel: SimpleNamespace(all_elements=[element]),
        )
        monkeypatch.setattr(
            module, "autoheal_web",
            lambda *args, **kwargs: WebHealHit(descriptor, 1),
        )
        monkeypatch.setattr(
            module._action_web, "scroll_descriptor",
            lambda channel, chosen: scrolled.append(channel) or "visible",
        )

        with step("Scroll Search"):
            assert module._heal_web_scroll(
                _Driver(), self.WEB_SELECTORS, "Search", ""
            ) == "visible"
        assert scrolled == [after_heal]

    def test_an_expired_cached_scroll_heal_does_not_recapture(
            self, monkeypatch):
        import testmu_appium._action_scroll_until as module

        class _Expired:
            @staticmethod
            def remaining_s():
                return 0.0

        monkeypatch.setattr(module, "_WebHealDeadline", _Expired)
        monkeypatch.setattr(module, "read_cache", lambda key: {"dom_path": []})
        monkeypatch.setattr(
            module, "_scroll_healed_descriptor",
            lambda driver, descriptor, deadline=None: None,
        )
        monkeypatch.setattr(
            module, "_fresh_unplaced_surface",
            lambda driver: pytest.fail(
                "an expired scroll must not start another CDP recapture"
            ),
        )
        with pytest.raises(ElementNotFound, match="deadline was exhausted"):
            module._heal_web_scroll(
                _Driver(), self.WEB_SELECTORS, "Search", ""
            )

    def test_an_expired_scroll_retry_does_not_recapture_again(
            self, monkeypatch):
        import testmu_appium._action_scroll_until as module
        from testmu_appium._heal import WebHealHit

        class _Deadline:
            expired = False

            def remaining_s(self):
                return 0.0 if self.expired else 1.0

        deadline = _Deadline()
        captures = []
        monkeypatch.setattr(module, "_WebHealDeadline", lambda: deadline)
        monkeypatch.setattr(module, "read_cache", lambda key: module.CACHE_ABSENT)
        monkeypatch.setattr(
            module, "_fresh_unplaced_surface",
            lambda driver: captures.append(True) or (object(), object()),
        )
        monkeypatch.setattr(
            module, "autoheal_web",
            lambda *args, **kwargs: WebHealHit({"dom_path": []}, 1),
        )

        def expire(*args, **kwargs):
            deadline.expired = True
            return None

        monkeypatch.setattr(module, "_scroll_healed_descriptor", expire)
        with pytest.raises(ElementNotFound):
            module._heal_web_scroll(
                _Driver(), self.WEB_SELECTORS, "Search", ""
            )
        assert captures == [True]

    def test_an_unreachable_page_is_not_found_rather_than_silently_skipped(
            self, monkeypatch):
        self._patch(monkeypatch, None)
        with pytest.raises(ElementNotFound):
            with step("s"):
                scroll_until(_Driver(), selectors=self.WEB_SELECTORS, surface="web")

    def test_a_web_scroll_without_a_css_strategy_is_producer_skew(self, monkeypatch):
        """Native strategies name nothing in a DOM, so this can only be a
        recorder that lost the surface an element was read through."""
        self._patch(monkeypatch, object())
        with pytest.raises(ValueError):
            with step("s"):
                scroll_until(_Driver(), selectors=SELECTORS, surface="web")

    def test_the_native_path_is_untouched_by_the_new_parameter(self):
        el = _El(rect={"x": 0, "y": 500, "width": 1080, "height": 100})
        with step("s"):
            assert scroll_until(_found(el), selectors=SELECTORS) is el


class TestClearOrderingAndFocus:
    """The focus-then-clear ordering, on every verb that clears before typing."""

    def test_search_focuses_before_it_clears_too(self):
        el = _El()
        driver = _found(el)
        with step("s"):
            search(driver, selectors=SELECTORS, text="pizza")
        assert el.calls[:2] == [("click",), ("clear",)]


class TestCoordinateClearNeedsAFocusedField:
    """`_clear_at_point` has no element handle — it clears whatever the tap focused.

    When the tap opened no text field there is nothing to clear, and the verb must
    say so. Swallowing it is wrong: the `mobile: type` that follows would type into
    the void and report success.
    """

    class _NoFocus:
        @property
        def active_element(self):
            from selenium.common.exceptions import NoSuchElementException

            raise NoSuchElementException("nothing is focused")

    def test_it_fails_naming_the_missing_field(self):
        from testmu_appium._action_type import _clear_at_point
        from testmu_appium._errors import ElementNotFound

        driver = _Driver()
        driver.switch_to = self._NoFocus()
        with pytest.raises(ElementNotFound) as exc:
            _clear_at_point(driver)
        assert "no text field" in str(exc.value).lower()

    def test_it_polls_rather_than_failing_on_the_first_read(self):
        """Focus can arrive a beat after the tap, so a single read is too eager."""
        from testmu_appium._action_type import _clear_at_point

        active = _El()

        class _LateFocus:
            def __init__(self):
                self.reads = 0

            @property
            def active_element(self):
                from selenium.common.exceptions import NoSuchElementException

                self.reads += 1
                if self.reads < 3:
                    raise NoSuchElementException("not focused yet")
                return active

        driver = _Driver()
        driver.switch_to = _LateFocus()
        _clear_at_point(driver)
        assert active.calls == [("clear",)]

    def test_a_focused_field_is_cleared_on_the_first_read(self):
        from testmu_appium._action_type import _clear_at_point

        active = _El()
        driver = _Driver()
        driver.switch_to = type("_S", (), {"active_element": active})()
        _clear_at_point(driver)
        assert active.calls == [("clear",)]


def test_container_signature_reads_descriptors_from_a_real_capture():
    """P1 regression: the movement signature reads perception.descriptors — which
    carry bounds/centre/identity — NOT the sanitized wire entries (index/role/name
    only, no geometry). With the old entries-based read it returned None for a
    container (every row filtered out) and hashed only the row COUNT without one, so
    a real scroll read as the end after one gesture. Built from real parse_tree /
    build_perception output, not a descriptor-shaped fake."""
    import testmu_appium._action_scroll_until as _su
    from testmu_appium.perception import parse_tree
    from testmu_appium._helpers._perception import build_perception, _DESCRIPTOR_KEYS

    def capture(row_y, clock):
        xml = (
            "<hierarchy rotation='0'>"
            "<node class='androidx.recyclerview.widget.RecyclerView' scrollable='true'"
            " resource-id='com.app:id/list' bounds='[0,200][1080,2100]'>"
            f"<node class='android.widget.TextView' resource-id='com.app:id/row'"
            f" text='Alpha' bounds='[0,{row_y}][1080,{row_y + 180}]'/>"
            "</node>"
            f"<node class='android.widget.TextView' text='{clock}' bounds='[0,0][240,150]'/>"
            "</hierarchy>"
        )
        return build_perception(parse_tree(xml, 1080, 2340), descriptor_keys=_DESCRIPTOR_KEYS)

    container = _El(rect={"x": 0, "y": 200, "width": 1080, "height": 1900})

    base = _su._container_signature(capture(300, "12:00"), container)
    scrolled = _su._container_signature(capture(500, "12:00"), container)   # the row moved
    ticked = _su._container_signature(capture(300, "12:01"), container)     # only the clock ticked

    assert base is not None       # descriptors carry bounds -> real rows (old code: None)
    assert base != scrolled       # the container's own row moving IS movement
    assert base == ticked         # a clock outside the container is NOT movement


def test_perceive_swallows_an_unparseable_tree_to_none():
    """P2 regression: a truncated mid-transition page source makes parse_tree raise
    ValueError; _perceive returns None (inconclusive) so the bounded search keeps
    going rather than aborting scroll_until. (`_real_perceive` is the pre-patch
    function; the autouse fixture swaps the module attribute for a fake.)"""
    class _BadDriver:
        page_source = "<hierarchy><node class='x' bounds='[0,0]"   # truncated
        def get_window_size(self):
            return {"width": 1080, "height": 2340}

    assert _real_perceive(_BadDriver(), screenshot=False) is None
