"""Coordinate gesture primitives, per platform.

Two things here are invisible in a passing test and wrong on a device: the
direction convention (a scroll DOWN is a finger moving UP) and iOS measuring every
gesture duration in seconds where Android measures milliseconds. Both are pinned.
"""
import pytest

from testmu_appium import _config
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers import gesture


class _Focus:
    """The element a tap left focused. Text verbs address it, never a locator."""

    def __init__(self, sink):
        self._sink = sink

    def send_keys(self, text):
        self._sink.append(str(text))


class _SwitchTo:
    def __init__(self, sink):
        self.active_element = _Focus(sink)


class _RecordingDriver:
    """Captures the three ways a verb can reach the device.

    `execute` is the W3C actions channel — ActionBuilder.perform() lands there,
    which is how a real touch is issued on a WebDriverAgent that does not serve
    `mobile: tap`.
    """

    def __init__(self):
        self.scripts = []
        self.actions = []
        self.typed = []
        self.switch_to = _SwitchTo(self.typed)

    def execute_script(self, name, args=None):
        self.scripts.append((name, args))
        return True

    def execute(self, command, params=None):
        self.actions.append((command, params))
        return {"value": None}

    @property
    def last(self):
        return self.scripts[-1]

    def keys_sent(self):
        """The string spelled out by keyDown events in the W3C action batches."""
        out = []
        for _, params in self.actions:
            for device in (params or {}).get("actions", []):
                if device.get("type") != "key":
                    continue
                for action in device.get("actions", []):
                    if action.get("type") == "keyDown":
                        out.append(action.get("value", ""))
        return "".join(out)

    def touch_points(self):
        """(x, y) of every pointerMove in the last W3C action batch."""
        out = []
        for _, params in self.actions:
            for device in (params or {}).get("actions", []):
                for action in device.get("actions", []):
                    if action.get("type") == "pointerMove":
                        out.append((action.get("x"), action.get("y")))
        return out


@pytest.fixture
def ios(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "ios")
    return _RecordingDriver()


@pytest.fixture
def android(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "android")
    return _RecordingDriver()


class TestTap:
    def test_ios_taps_with_a_real_pointer_not_a_script(self, ios):
        """`mobile: tap` is not served by every WebDriverAgent build, and a
        synthesized gesture is documented not to focus a web input. A W3C pointer
        is the same primitive everywhere."""
        gesture.tap(ios, 100, 200)
        assert ios.scripts == []
        assert ios.touch_points() == [(100, 200)]

    def test_android_is_unchanged(self, android):
        gesture.tap(android, 100, 200)
        assert android.last == ("mobile: clickGesture", {"x": 100, "y": 200})


class TestTypeText:
    def test_ios_types_at_the_session_not_at_an_element(self, ios):
        """The distinction this verb lives or dies by.

        `switch_to.active_element` only knows NATIVE focus. With the caret inside
        a WKWebView it raises NoSuchElementException while the page happily
        reports its focused textarea, so the text ends up in the nearest native
        field instead — the caret visibly jumps out of the page mid-type.

        W3C key actions name no element, so they follow the OS's keystroke
        routing — the same place the on-screen keyboard is typing, whichever
        surface that is.
        """
        gesture.type_text(ios, "8.8.8.8")
        assert ios.keys_sent() == "8.8.8.8"
        assert ios.typed == [], "no element may be addressed"
        assert ios.scripts == [], "not a driver extension either"

    def test_android_is_unchanged(self, android):
        gesture.type_text(android, "8.8.8.8")
        assert android.last == ("mobile: type", {"text": "8.8.8.8"})


class TestLongPress:
    def test_ios_converts_milliseconds_to_seconds(self, ios):
        """The single most common way to get an iOS gesture wrong: handing it a
        millisecond count produces a gesture minutes long."""
        gesture.long_press(ios, 10, 20, duration_ms=800)
        assert ios.last == ("mobile: touchAndHold", {"x": 10, "y": 20, "duration": 0.8})

    def test_android_keeps_milliseconds(self, android):
        gesture.long_press(android, 10, 20, duration_ms=800)
        assert android.last[1]["duration"] == 800


def _last_batch_points(driver):
    """(x, y) of the pointerMoves in the LAST W3C batch — start, then end."""
    _, params = driver.actions[-1]
    return [(a.get("x"), a.get("y"))
            for device in (params or {}).get("actions", [])
            for a in device.get("actions", [])
            if a.get("type") == "pointerMove"]


class TestScrollDirection:
    """`direction="down"` means SCROLL DOWN — reveal what is below — which the
    finger performs by moving UP. The sign is the whole test."""

    AREA = (0, 0, 400, 1000)

    def _points(self, driver):
        start, end = _last_batch_points(driver)
        return start, end

    def test_scrolling_down_moves_the_finger_up(self, ios):
        gesture.scroll_area(ios, *self.AREA, "down", 0.8)
        (_, from_y), (_, to_y) = self._points(ios)
        assert from_y > to_y

    def test_scrolling_up_moves_the_finger_down(self, ios):
        gesture.scroll_area(ios, *self.AREA, "up", 0.8)
        (_, from_y), (_, to_y) = self._points(ios)
        assert from_y < to_y

    def test_scrolling_right_moves_the_finger_left(self, ios):
        gesture.scroll_area(ios, *self.AREA, "right", 0.8)
        (from_x, _), (to_x, _) = self._points(ios)
        assert from_x > to_x

    def test_scrolling_left_moves_the_finger_right(self, ios):
        gesture.scroll_area(ios, *self.AREA, "left", 0.8)
        (from_x, _), (to_x, _) = self._points(ios)
        assert from_x < to_x

    def test_a_full_percent_swipe_stays_off_the_edges(self, ios):
        """A gesture starting on the very edge lands in the system's own edge-swipe
        zones — back navigation, notification centre — and never reaches the app."""
        gesture.scroll_area(ios, 0, 0, 400, 1000, "down", 1.0)
        (_, from_y), (_, to_y) = self._points(ios)
        assert 0 < to_y < from_y < 1000

    def test_a_smaller_percent_travels_less(self, ios):
        gesture.scroll_area(ios, *self.AREA, "down", 0.2)
        (_, small_from), (_, small_to) = self._points(ios)
        gesture.scroll_area(ios, *self.AREA, "down", 0.9)
        (_, big_from), (_, big_to) = self._points(ios)
        assert (small_from - small_to) < (big_from - big_to)


class TestScrollExhaustion:
    def test_ios_always_reports_more_may_remain(self, ios):
        """XCUITest cannot answer "could anything still scroll?".

        scroll_until treats False as "the list ended" and stops, so a wrong False
        abandons a search one scroll in. A wrong True only spends the caller's
        remaining budget. The bounded loop is what guarantees termination on iOS.
        """
        assert gesture.scroll_area(ios, 0, 0, 400, 1000, "down", 0.8) is True

    def test_ios_scrolls_an_element_over_its_own_box(self, ios):
        class _El:
            rect = {"x": 0, "y": 500, "width": 400, "height": 400}

        assert gesture.scroll_element(ios, _El(), "down", 0.8) is True
        (_, from_y), (_, to_y) = _last_batch_points(ios)
        # Inside the element, not the screen: percent stays meaningful.
        assert 500 <= to_y < from_y <= 900


class TestAndroidScrollSpeed:
    """`mobile: scrollGesture` swipes at 1500 dp/s unless told otherwise, and a
    swipe that fast flings a stock Android list past the asked distance on some
    runs. Every Android scroll therefore names a slow speed: 200 dp/s, scaled
    to px/s by the session's pixel ratio."""

    class _El:
        id = "list-1"
        rect = {"x": 0, "y": 1464, "width": 1080, "height": 690}

    def test_element_scroll_names_a_speed_scaled_by_the_pixel_ratio(self, android):
        android.capabilities = {"pixelRatio": "3"}
        gesture.scroll_element(android, self._El(), "down", 0.7)
        name, args = android.last
        assert name == "mobile: scrollGesture"
        assert args["elementId"] == "list-1"
        assert args["percent"] == 0.7
        assert args["speed"] == 600

    def test_area_scroll_names_the_same_speed(self, android):
        android.capabilities = {"pixelRatio": 2.625}
        gesture.scroll_area(android, 108, 351, 864, 1638, "down", 0.8)
        _, args = android.last
        assert args["speed"] == 525

    def test_an_unknown_pixel_ratio_assumes_a_low_density(self, android):
        """No pixel ratio on the session: scale by 2, the low end of phone
        densities. Underestimating density makes the finger slower, never faster."""
        gesture.scroll_element(android, self._El(), "down", 0.7)
        assert android.last[1]["speed"] == 400

    def test_an_unreadable_pixel_ratio_assumes_a_low_density(self, android):
        android.capabilities = {"pixelRatio": "n/a"}
        gesture.scroll_element(android, self._El(), "down", 0.7)
        assert android.last[1]["speed"] == 400


class TestScrollTouchIsNotALongPress:
    """The measured failure this pins: `dragFromToForDuration`'s duration is
    the press-HOLD before the move, floored at 0.5s — exactly iOS's long-press
    threshold — so every scroll long-pressed whatever sat under its start
    point. With the keyboard open that was a letter key, whose accent popup
    commits the letter on release: "rohith" became "rohithg" mid-scroll, and a
    later scroll opened a text field's copy/share callout."""

    def _last_batch(self, driver):
        _, params = driver.actions[-1]
        return [a for device in (params or {}).get("actions", [])
                for a in device.get("actions", [])]

    def test_a_scroll_is_a_w3c_drag_not_a_drag_script(self, ios):
        gesture.scroll_area(ios, 0, 0, 400, 1000, "down", 0.8)
        assert ios.scripts == [], "no mobile: script may carry a scroll"
        assert len(ios.actions) == 1

    def test_the_touch_settles_below_the_long_press_threshold(self, ios):
        gesture.scroll_area(ios, 0, 0, 400, 1000, "down", 0.8)
        pauses = [a["duration"] for a in self._last_batch(ios)
                  if a["type"] == "pause"]
        assert pauses and all(p < 500 for p in pauses), pauses

    def test_the_move_is_slow_enough_to_drag_not_flick(self, ios):
        """A flick's momentum travel depends on velocity physics no recording
        can replay; only a drag keeps the recorded distance exact."""
        gesture.scroll_area(ios, 0, 0, 400, 1000, "down", 0.8)
        moves = [a for a in self._last_batch(ios) if a["type"] == "pointerMove"]
        assert moves[0]["duration"] == 0, "positioning hover is instant"
        assert moves[-1]["duration"] >= 400, "the on-glass move must be slow"

    def test_the_drag_verb_keeps_its_hold(self, ios):
        """Drag-and-drop WANTS the press-hold — it is the pickup. It survived
        the move off `dragFromToForDuration`; it is a pause now, not that
        command's only duration."""
        gesture.drag_gesture(ios, (10, 20), (30, 40))
        assert ios.scripts == []
        pauses = [a["duration"] for a in self._last_batch(ios)
                  if a["type"] == "pause"]
        assert pauses == [500], "the pickup, before the travel"


class TestDrag:
    def test_ios_holds_for_the_recorded_pickup_before_moving(self, ios):
        """The pickup decides whether a long-press-then-drag is recognised, so a
        recording that states one gets exactly that, before the travel."""
        gesture.drag_gesture(ios, (1, 2), (3, 4), hold_duration_ms=600)
        _, params = ios.actions[-1]
        batch = [a for device in (params or {}).get("actions", [])
                 for a in device.get("actions", [])]
        assert [a["type"] for a in batch[:3]] == [
            "pointerMove", "pointerDown", "pause"]
        assert batch[2]["duration"] == 600

    def test_android_keeps_both_durations(self, android):
        gesture.drag_gesture(android, (1, 2), (3, 4), hold_duration_ms=600,
                             move_duration_ms=250)
        assert android.last[1]["holdDuration"] == 600
        assert android.last[1]["moveDuration"] == 250


class TestDragHoldsAtItsDestination:
    """A slide-and-hold control watches the thumb STAY past its threshold and
    reads a release on arrival as an abandon, however far it travelled. Neither
    platform's drag script can express that — `dragFromToForDuration` has one
    duration and it is the pickup, `dragGesture` releases when the travel ends —
    so both compose the gesture instead. Measured on the toggles fixture, where
    the hold slider reported `released-early` and confirmed nothing on both
    platforms while the two plain sliders reached 100."""

    def _batch(self, driver):
        _, params = driver.actions[-1]
        return [a for device in (params or {}).get("actions", [])
                for a in device.get("actions", [])]

    def _batch_after_drag(self, driver, **kwargs):
        gesture.drag_gesture(driver, (1, 2), (3, 4), **kwargs)
        return self._batch(driver)

    @pytest.mark.parametrize("platform", ["ios", "android"])
    def test_the_finger_stays_down_for_the_whole_dwell(self, request, platform):
        driver = request.getfixturevalue(platform)
        gesture.drag_gesture(driver, (1, 2), (3, 4),
                             hold_at_destination_ms=1200)
        assert driver.scripts == [], "a hold cannot ride a mobile: script"
        batch = self._batch(driver)
        assert batch[-1]["type"] == "pointerUp"
        # However the dwell is spent, it is spent BEFORE the lift and it lasts
        # as long as the caller asked.
        travel = next(i for i, a in enumerate(batch)
                      if a["type"] == "pointerMove" and a["duration"] > 0)
        held = sum(a["duration"] for a in batch[travel + 1:]
                   if a["type"] == "pause")
        assert held == 1200, batch

    def test_android_holds_still(self, android):
        """Nothing asks Android for more: a still hold confirms there, measured
        on the fixture (`slide-hold-state` went to `held`)."""
        gesture.drag_gesture(android, (1, 2), (3, 4),
                             hold_at_destination_ms=1200)
        batch = self._batch(android)
        assert [a["type"] for a in batch[-2:]] == ["pause", "pointerUp"]
        assert batch[-2]["duration"] == 1200

    def test_ios_wakes_the_control_once_before_it_lifts(self, ios):
        """iOS needs a movement event to notice the dwell elapsed, so the dwell
        is spent still and one 1px move delivers that event just before the
        lift. Held still instead, the fixture abandons every time — measured
        with the drag composed and with it scripted."""
        gesture.drag_gesture(ios, (10, 20), (300, 20),
                             hold_at_destination_ms=600)
        batch = self._batch(ios)
        assert [a["type"] for a in batch[-3:]] == [
            "pause", "pointerMove", "pointerUp"]
        assert batch[-3]["duration"] == 600, "the whole dwell, spent still"
        wake = batch[-2]
        assert wake["duration"] == 0 and wake["y"] == 20
        assert wake["x"] == 301, "1px off the destination"

    def test_the_travel_is_honoured_when_the_caller_times_it(self, ios):
        gesture.drag_gesture(ios, (1, 2), (3, 4), move_duration_ms=900,
                             hold_at_destination_ms=300)
        moves = [a for a in self._batch(ios) if a["type"] == "pointerMove"]
        assert moves[0]["duration"] == 0, "positioning hover is instant"
        travel = [a for a in moves if a["duration"] > 0]
        assert [a["duration"] for a in travel] == [900], "one timed travel"

    def test_the_pickup_still_comes_first(self, ios):
        """Both pauses can be asked for at once; they are different moments."""
        batch = self._batch_after_drag(ios, hold_duration_ms=700,
                                       hold_at_destination_ms=1200)
        pauses = [a["duration"] for a in batch if a["type"] == "pause"]
        travel = next(i for i, a in enumerate(batch)
                      if a["type"] == "pointerMove" and a["duration"] > 0)
        assert pauses[0] == 700, "the pickup, before the move"
        assert sum(a["duration"] for a in batch[travel + 1:]
                   if a["type"] == "pause") == 1200

    def test_android_keeps_its_script_for_a_plain_drag(self, android):
        """Nothing there needs composing: `dragGesture` travels and releases,
        which is the whole of a drag with no dwell."""
        gesture.drag_gesture(android, (1, 2), (3, 4))
        assert android.last[0] == "mobile: dragGesture"

    def test_ios_composes_even_without_a_dwell(self, ios):
        """`dragFromToForDuration` is gone from this verb: it floors the pickup
        at 0.5s and opens with an overture of XCTest's own, visible on screen and
        belonging to no recording."""
        gesture.drag_gesture(ios, (1, 2), (3, 4))
        assert ios.scripts == []
        assert len(ios.actions) == 1


class _FakeElement:
    """An element as the click runner sees it: a type, children, a click sink."""

    def __init__(self, tag_name, nested=()):
        self.tag_name = tag_name
        self._nested = list(nested)
        self.clicked = False
        self.queried = False

    def find_elements(self, by, value):
        self.queried = True
        return self._nested

    def click(self):
        self.clicked = True


class TestClickTarget:
    """SwiftUI's Toggle is ONE switch element spanning label + capsule; its
    center — where element.click() lands — is the label, which ignores taps.
    The tappable capsule is a nested non-accessible switch child. Proven on
    device (chaos-enabled): parent click left value 0, child click flipped it."""

    def test_an_ios_switch_click_is_redirected_to_its_nested_switch(self, ios):
        capsule = _FakeElement("XCUIElementTypeSwitch")
        row = _FakeElement("XCUIElementTypeSwitch", nested=[capsule])
        assert gesture.click_target(ios, row) is capsule

    def test_an_ios_switch_with_no_nested_child_is_clicked_as_found(self, ios):
        """A bare capsule-sized switch: its own center IS the control."""
        bare = _FakeElement("XCUIElementTypeSwitch")
        assert gesture.click_target(ios, bare) is bare

    def test_ios_elements_that_are_not_switches_are_never_queried(self, ios):
        """The redirect must not reroute a click on a row that merely CONTAINS
        a switch — clicking such a row can mean opening it, not toggling."""
        button = _FakeElement("XCUIElementTypeButton",
                              nested=[_FakeElement("XCUIElementTypeSwitch")])
        assert gesture.click_target(ios, button) is button
        assert button.queried is False

    def test_android_is_unchanged(self, android):
        switch = _FakeElement("android.widget.Switch",
                              nested=[_FakeElement("android.widget.Switch")])
        assert gesture.click_target(android, switch) is switch
        assert switch.queried is False


def test_an_unshipped_platform_is_refused_by_name(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "tizen")
    with pytest.raises(UnsupportedOnPlatform) as exc:
        gesture.tap(_RecordingDriver(), 1, 2)
    assert "coordinate tap" in str(exc.value)


class TestDragPickup:
    """`mobile: dragFromToForDuration` floored its one duration at 0.5s, so a
    recording that stated a shorter pickup silently got 0.5s. Composed, the
    pickup is a pause like any other and the floor was the command's, not the
    platform's."""

    def _pauses(self, driver):
        _, params = driver.actions[-1]
        return [a["duration"] for device in (params or {}).get("actions", [])
                for a in device.get("actions", []) if a["type"] == "pause"]

    def test_an_unstated_pickup_keeps_the_half_second_it_always_had(self, ios):
        """A recording made under the old command replays as the same gesture."""
        gesture.drag_gesture(ios, (10, 20), (30, 40))
        assert self._pauses(ios) == [500]

    def test_a_pickup_under_the_old_floor_is_now_honoured(self, ios):
        gesture.drag_gesture(ios, (1, 2), (3, 4), hold_duration_ms=200)
        assert self._pauses(ios) == [200]

    def test_a_stated_pickup_is_kept(self, ios):
        gesture.drag_gesture(ios, (1, 2), (3, 4), hold_duration_ms=600)
        assert self._pauses(ios) == [600]


class TestComposedDragTravel:
    """`move_duration_ms` is the travel time. The Android script always took it
    as `moveDuration`; on iOS it was inexpressible until the composed path
    existed — `dragFromToForDuration` has one duration and it is the pickup —
    so it was silently dropped there. Composed, both platforms honour it."""

    def _travel(self, driver):
        _, params = driver.actions[-1]
        moves = [a for device in (params or {}).get("actions", [])
                 for a in device.get("actions", [])
                 if a["type"] == "pointerMove" and a["duration"] > 0]
        assert len(moves) == 1, f"expected one timed travel, got {moves}"
        return moves[0]["duration"]

    def test_ios_travel_defaults_when_the_caller_does_not_say(self, ios):
        gesture.drag_gesture(ios, (1, 2), (3, 4))
        assert self._travel(ios) == 600

    def test_ios_honours_a_stated_travel(self, ios):
        """The point of the parameter: a control that rejects a fast swipe can
        finally be given a slow one on iOS."""
        gesture.drag_gesture(ios, (1, 2), (3, 4), move_duration_ms=1500)
        assert self._travel(ios) == 1500

    def test_a_faster_than_default_travel_is_honoured_too(self, ios):
        """These controls settle where the finger is released and carry no
        momentum, so a quick travel lands in the same place — it is not the
        scroll path, whose velocity decides how far the content coasts."""
        gesture.drag_gesture(ios, (1, 2), (3, 4), move_duration_ms=200)
        assert self._travel(ios) == 200

    @pytest.mark.parametrize("stated", [0, 1, -5])
    def test_a_degenerate_travel_is_floored(self, ios, stated):
        """At zero the finger teleports: the driver interpolates the move into
        intermediate events, and a control reading continuous updates can miss
        the drag entirely."""
        gesture.drag_gesture(ios, (1, 2), (3, 4), move_duration_ms=stated)
        assert self._travel(ios) == 50

    def test_android_honours_it_on_the_composed_path(self, android):
        gesture.drag_gesture(android, (1, 2), (3, 4),
                             move_duration_ms=1500, hold_at_destination_ms=300)
        assert self._travel(android) == 1500

    def test_android_still_hands_it_to_the_script(self, android):
        """No dwell means no composed drag, and the script takes it directly."""
        gesture.drag_gesture(android, (1, 2), (3, 4), move_duration_ms=1500)
        name, args = android.last
        assert name == "mobile: dragGesture"
        assert args["moveDuration"] == 1500


class TestComposedDragPicksUpOnBothPlatforms:
    """`dragGesture` presses before it travels whether or not a hold is named.
    Composing has to be told to, or a control that arms on a long press — a
    reorderable row, an app icon — is never picked up, and only the drags
    carrying a dwell would break."""

    def _first_pause(self, driver):
        _, params = driver.actions[-1]
        pauses = [a["duration"] for device in (params or {}).get("actions", [])
                  for a in device.get("actions", []) if a["type"] == "pause"]
        return pauses[0] if pauses else None

    def test_android_composed_drag_presses_before_it_travels(self, android):
        gesture.drag_gesture(android, (1, 2), (3, 4), hold_at_destination_ms=300)
        assert self._first_pause(android) == 500

    def test_a_stated_pickup_still_wins_on_android(self, android):
        gesture.drag_gesture(android, (1, 2), (3, 4),
                             hold_duration_ms=800, hold_at_destination_ms=300)
        assert self._first_pause(android) == 800

    def test_both_platforms_use_the_same_default(self, ios, android):
        gesture.drag_gesture(ios, (1, 2), (3, 4), hold_at_destination_ms=300)
        ios_pickup = self._first_pause(ios)
        gesture.drag_gesture(android, (1, 2), (3, 4), hold_at_destination_ms=300)
        assert self._first_pause(android) == ios_pickup
