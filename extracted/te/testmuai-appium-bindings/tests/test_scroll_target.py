"""What a scroll gesture is aimed at: an element, or a rectangle.

`mobile: scrollGesture` takes either an `elementId` or a bounding rectangle, and
they do not mean the same thing. An elementId scrolls that scrollable; a
rectangle only says where to swipe, which reaches nothing when the container does
not respond to a synthesized touch at those coordinates.

So the payload shape IS the contract, and these tests assert it directly rather
than only that a scrollGesture was issued.
"""
import pytest

from testmu_appium import _action_engine, _config
from testmu_appium._action_scroll import scroll
from testmu_appium._action_scroll_until import scroll_until
from testmu_appium._errors import ElementNotFound
from testmu_appium._step import step

SELECTORS = [{"strategy": "view_id", "selector": "com.app:id/list", "score": 90}]
CONTAINER = [{"strategy": "view_id", "selector": "com.app:id/box", "score": 90}]


class _El:
    def __init__(self, element_id="el-1", rect=None):
        self.id = element_id
        self.rect = rect or {"x": 0, "y": 600, "width": 1080, "height": 1500}

    def get_attribute(self, name):
        return None


class _Driver:
    page_source = "<hierarchy rotation='0'/>"

    def __init__(self, found=None, can_scroll=True, window=(1080, 2340)):
        self.found = found or {}
        self.scripts = []
        self._window = window
        self._can_scroll = can_scroll

    def get_window_size(self):
        return {"width": self._window[0], "height": self._window[1]}

    def find_elements(self, by, value):
        for needle, result in self.found.items():
            if needle in value:
                return result
        return []

    def execute_script(self, script, args=None):
        self.scripts.append((script, args))
        return self._can_scroll


@pytest.fixture(autouse=True)
def _fast(monkeypatch):
    monkeypatch.setattr(_action_engine, "_settle", lambda driver, deadline: None)
    monkeypatch.setattr(_action_engine.time, "sleep", lambda s: None)
    monkeypatch.setitem(_config._config, "platform", "android")


def _gestures(driver):
    return [args for name, args in driver.scripts if name == "mobile: scrollGesture"]


# --- scroll -----------------------------------------------------------------

def test_an_element_scroll_addresses_the_element():
    """The resolved element is what gets scrolled, not the rectangle it occupies."""
    driver = _Driver(found={"com.app:id/list": [_El()]})
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert args["elementId"] == "el-1"
    assert "left" not in args and "top" not in args


def test_a_screen_scroll_still_addresses_a_rectangle():
    """With no element AND no scrollable on screen, there is nothing to address
    but the screen itself."""
    driver = _Driver()
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert "elementId" not in args
    assert {"left", "top", "width", "height"} <= set(args)


# --- screen scroll: naming the container ------------------------------------
#
# A screen scroll has no selectors, but the screen still has exactly one thing a
# thumb at its centre would move. The inset rectangle is not that thing: on a
# layout with a sticky header the rectangle's leading edge lands ABOVE the
# scrollable, so an upward gesture is delivered to the header, moves nothing, and
# the driver truthfully answers "no more content" — indistinguishable from a real
# end of list. Naming the container is what makes the two distinguishable.

def test_a_screen_scroll_addresses_the_scrollable_under_the_centre():
    container = _El("list", {"x": 0, "y": 600, "width": 1080, "height": 1500})
    driver = _Driver(found={"scrollable(true)": [container]})
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert args["elementId"] == "list"
    assert "left" not in args


def test_the_innermost_scrollable_containing_the_centre_wins():
    """A nested list is what a thumb over it scrolls, not the page holding it."""
    page = _El("page", {"x": 0, "y": 0, "width": 1080, "height": 2340})
    inner = _El("inner", {"x": 0, "y": 900, "width": 1080, "height": 600})
    driver = _Driver(found={"scrollable(true)": [page, inner]})
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert args["elementId"] == "inner"


def test_a_scrollable_that_misses_the_centre_is_not_addressed():
    """Off to one side it is not what a centre gesture would reach, so the
    rectangle remains the honest answer."""
    aside = _El("aside", {"x": 0, "y": 0, "width": 200, "height": 200})
    driver = _Driver(found={"scrollable(true)": [aside]})
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert "elementId" not in args
    assert {"left", "top", "width", "height"} <= set(args)


def test_a_named_container_still_travels_a_screens_worth():
    """The caller asked to scroll the SCREEN; naming the container is only how
    that was carried out, so the distance must not shrink to the container
    stride. A stride is a fraction OF THE BOX being dragged, so covering the
    same ground inside a smaller box needs a larger fraction.

    0.8 of the 1638px gesture area, expressed against a 1500px container.
    """
    container = _El("list", {"x": 0, "y": 600, "width": 1080, "height": 1500})
    driver = _Driver(found={"scrollable(true)": [container]})
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert args["percent"] == pytest.approx(0.8 * 1638 / 1500)


def test_a_short_container_is_dragged_no_further_than_itself():
    """A gesture cannot drag a container past its own span, so a screen's worth
    inside a short list clamps rather than asking for the impossible."""
    container = _El("list", {"x": 0, "y": 1000, "width": 1080, "height": 400})
    driver = _Driver(found={"scrollable(true)": [container]})
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert args["percent"] == 1.0


def test_a_horizontal_screen_scroll_measures_against_the_width():
    """Sideways the reach is the gesture area's WIDTH (864), not its height —
    a rail as tall as it is wide would otherwise be handed a vertical stride."""
    container = _El("rail", {"x": 0, "y": 900, "width": 900, "height": 600})
    driver = _Driver(found={"scrollable(true)": [container]})
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="right", value=1)

    (args,) = _gestures(driver)
    assert args["percent"] == pytest.approx(0.8 * 864 / 900)


def test_an_explicitly_scoped_scroll_keeps_the_container_stride():
    """Asking for THIS container is a different request from asking for the
    screen, and it keeps the shorter stride that leaves more overlap."""
    driver = _Driver(found={"com.app:id/list": [_El()]})
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert args["percent"] == 0.6


def test_an_unreadable_scrollable_query_falls_back_to_the_rectangle():
    """Resolution is an improvement on the gesture, never a new way to fail it."""
    class _Angry(_Driver):
        def find_elements(self, by, value):
            raise RuntimeError("uiautomator unavailable")

    driver = _Angry()
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert {"left", "top", "width", "height"} <= set(args)


@pytest.mark.parametrize("kind,value", [
    ("times", 1), ("percent", 50), ("pixels", 300), ("edge", None),
])
def test_every_scroll_kind_addresses_the_element(kind, value):
    driver = _Driver(found={"com.app:id/list": [_El()]}, can_scroll=False)
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind=kind, direction="down", value=value)

    for args in _gestures(driver):
        assert args["elementId"] == "el-1"
        assert "left" not in args


def test_a_pixel_scroll_measures_against_the_elements_own_height():
    """750px against the element's 1500 is measured against the ~three quarters
    of it a full gesture actually travels, not the raw span — and not the
    screen's."""
    driver = _Driver(found={"com.app:id/list": [_El()]})
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind="pixels", direction="down", value=750)

    (args,) = _gestures(driver)
    assert args["percent"] == pytest.approx(750 / (0.75 * 1500))


def test_a_long_pixel_scroll_issues_gestures_until_the_distance_is_covered():
    """3000px over a 1500px element is two full gestures and a remainder, not
    one clamped gesture that silently drops the rest of the distance."""
    driver = _Driver(found={"com.app:id/list": [_El()]})
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind="pixels", direction="down", value=3000)

    percents = [args["percent"] for args in _gestures(driver)]
    assert percents == pytest.approx([1.0, 1.0, 750 / 1125])


def test_a_long_pixel_scroll_stops_at_the_end_of_content():
    driver = _Driver(found={"com.app:id/list": [_El()]}, can_scroll=False)
    with step("s"):
        answer = scroll(driver, selectors=SELECTORS, kind="pixels",
                        direction="down", value=3000)

    assert len(_gestures(driver)) == 1
    assert answer is False


def test_a_pixel_scroll_that_cannot_cover_its_distance_gives_up():
    """A distance far past the content is a bounded give-up, not a spin."""
    driver = _Driver(found={"com.app:id/list": [_El()]}, can_scroll=True)
    with step("s"):
        answer = scroll(driver, selectors=SELECTORS, kind="pixels",
                        direction="down", value=10**7)

    assert len(_gestures(driver)) == 30
    assert answer is True


def test_a_percent_over_one_hundred_issues_multiple_gestures():
    """250% of the area cannot land in one gesture: it is two full gestures and a
    half, not one clamped gesture that silently drops the rest."""
    driver = _Driver(found={"com.app:id/list": [_El()]})
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind="percent", direction="down", value=250)

    percents = [args["percent"] for args in _gestures(driver)]
    assert percents == pytest.approx([1.0, 1.0, 0.5])


def test_a_percent_over_one_hundred_stops_at_the_end_of_content():
    """A percent past the end is a bounded give-up: the first full gesture reports
    no more content and the remainder is not chased."""
    driver = _Driver(found={"com.app:id/list": [_El()]}, can_scroll=False)
    with step("s"):
        answer = scroll(driver, selectors=SELECTORS, kind="percent",
                        direction="down", value=250)

    assert len(_gestures(driver)) == 1
    assert answer is False


def test_a_times_scroll_stops_when_the_element_reports_no_more_content():
    """The gesture's own answer is what ends the loop, so it must be the element's."""
    driver = _Driver(found={"com.app:id/list": [_El()]}, can_scroll=False)
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind="times", direction="down", value=5)

    assert len(_gestures(driver)) == 1


# --- how far one step goes --------------------------------------------------

def test_one_step_inside_an_element_leaves_most_of_the_view_behind():
    """0.6 of a container travels roughly 45% of it, so the next perception
    overlaps the last by about half."""
    driver = _Driver(found={"com.app:id/list": [_El()]})
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert args["percent"] == 0.6


def test_one_step_over_the_screen_keeps_the_longer_stride():
    """The screen path covers a taller area than any container inside it."""
    driver = _Driver()
    with step("s"):
        scroll(driver, selectors=None, kind="times", direction="down", value=1)

    (args,) = _gestures(driver)
    assert args["percent"] == 0.8


@pytest.mark.parametrize("selectors", [SELECTORS, None])
def test_running_to_an_edge_uses_the_longer_stride(selectors):
    """Reaching an end wants distance; there is no view to overlap with."""
    driver = _Driver(found={"com.app:id/list": [_El()]}, can_scroll=False)
    with step("s"):
        scroll(driver, selectors=selectors, kind="edge", direction="down", value=None)

    for args in _gestures(driver):
        assert args["percent"] == 0.8


# --- what a scroll answers --------------------------------------------------
#
# `scrollGesture` answers whether content remains in that direction, and that
# answer is the only thing separating "this container is at its end" from "keep
# going". Throwing it away costs a caller its exit condition: an until-loop with
# nothing else to go on spends its whole retry budget, and every retry it spends
# after the end pays for a gesture, a tree read and a model call that cannot
# change anything.

def test_a_scroll_that_can_continue_says_so():
    driver = _Driver(found={"com.app:id/list": [_El()]}, can_scroll=True)
    with step("s"):
        answer = scroll(driver, selectors=SELECTORS, kind="times",
                        direction="down", value=1)
    assert answer is True


def test_a_scroll_at_the_end_says_there_is_no_more():
    driver = _Driver(found={"com.app:id/list": [_El()]}, can_scroll=False)
    with step("s"):
        answer = scroll(driver, selectors=SELECTORS, kind="times",
                        direction="down", value=1)
    assert answer is False


def test_a_screen_scroll_answers_the_same_question():
    container = _El("list", {"x": 0, "y": 600, "width": 1080, "height": 1500})
    driver = _Driver(found={"scrollable(true)": [container]}, can_scroll=False)
    with step("s"):
        answer = scroll(driver, selectors=None, kind="times",
                        direction="down", value=1)
    assert answer is False


def test_an_edge_scroll_that_hit_its_budget_still_reports_more():
    """Thirty gestures without reaching an end is a bounded give-up, not an end."""
    driver = _Driver(can_scroll=True)
    with step("s"):
        answer = scroll(driver, selectors=None, kind="edge",
                        direction="down", value=None)
    assert answer is True


def test_an_edge_scroll_that_arrived_reports_no_more():
    driver = _Driver(can_scroll=False)
    with step("s"):
        answer = scroll(driver, selectors=None, kind="edge",
                        direction="down", value=None)
    assert answer is False


# --- what ends an edge scroll -----------------------------------------------
#
# The gesture's own answer cannot end an edge scroll by itself: iOS has no
# gesture that reports "more to scroll" (its adapter answers True forever), and
# Android's answer lies both ways. The movement probe is the judge — a gesture
# that moved nothing is the end — and the gesture's claim is honoured only while
# the probe cannot rule (the blank-tree tests above).

class _FiniteList(_Driver):
    """A finite page: one real row shifts down the tree for `moves` gestures,
    then freezes — the movement probe's end signal, independent of the gesture's
    own (unreliable) canScrollMore. A clock OUTSIDE the inset gesture area ticks
    with every gesture, so an unscoped probe would read it as endless movement."""

    def __init__(self, moves, **kw):
        super().__init__(**kw)
        self._moves = moves

    @property
    def page_source(self):
        scrolls = sum(1 for name, _ in self.scripts
                      if name == "mobile: scrollGesture")
        y = 400 + 120 * min(scrolls, self._moves)
        return (
            "<hierarchy rotation='0'>"
            f"<node class='android.widget.TextView' resource-id='com.app:id/row'"
            f" text='Alpha' bounds='[0,{y}][1080,{y + 180}]'/>"
            f"<node class='android.widget.TextView' text='12:{scrolls:02d}'"
            f" bounds='[0,0][240,150]'/>"
            "</hierarchy>"
        )


def test_an_edge_scroll_stops_when_the_screen_stops_moving():
    """The iOS shape: the gesture claims "more" forever, so the probe is the only
    exit. Three gestures move the row, the fourth moves nothing -> the end, far
    below the 30-gesture budget the old loop always burned."""
    driver = _FiniteList(moves=3, can_scroll=True)
    with step("s"):
        answer = scroll(driver, selectors=None, kind="edge",
                        direction="down", value=None)
    assert answer is False
    assert len(_gestures(driver)) == 4


def test_an_edge_scroll_does_not_trust_a_lying_no_more():
    """The Android shape: canScrollMore claims the end while the page plainly
    still moves (Compose LazyColumn; a gesture landed on a sticky header). A
    claim refuted by the gesture's own effect is not an exit — the scroll runs
    to the true end instead of stopping one screen in."""
    driver = _FiniteList(moves=3, can_scroll=False)
    with step("s"):
        answer = scroll(driver, selectors=None, kind="edge",
                        direction="down", value=None)
    assert answer is False
    assert len(_gestures(driver)) == 4


def test_a_ticking_clock_outside_the_gesture_area_is_not_movement():
    """The screen-level probe is scoped to the inset gesture rectangle, so the
    status bar's clock ticking with every gesture cannot keep an ended page
    reading as "still moving"."""
    driver = _FiniteList(moves=0, can_scroll=True)
    with step("s"):
        answer = scroll(driver, selectors=None, kind="edge",
                        direction="down", value=None)
    assert answer is False
    assert len(_gestures(driver)) == 1


# --- scroll_until -----------------------------------------------------------

def test_a_container_scoped_scroll_until_scrolls_the_container():
    offscreen = _El("target", {"x": 0, "y": 5000, "width": 100, "height": 50})
    container = _El("box", {"x": 0, "y": 600, "width": 1080, "height": 1200})
    driver = _Driver(found={"com.app:id/list": [offscreen],
                            "com.app:id/box": [container]}, can_scroll=False)
    with pytest.raises(Exception):
        with step("s"):
            scroll_until(driver, selectors=SELECTORS, container_selectors=CONTAINER,
                         max_scrolls=1)

    gestures = _gestures(driver)
    assert gestures, "expected at least one scroll gesture"
    assert all(a["elementId"] == "box" for a in gestures)


def test_a_screen_scoped_scroll_until_scrolls_the_screen_rectangle():
    offscreen = _El("target", {"x": 0, "y": 5000, "width": 100, "height": 50})
    driver = _Driver(found={"com.app:id/list": [offscreen]}, can_scroll=False)
    with pytest.raises(Exception):
        with step("s"):
            scroll_until(driver, selectors=SELECTORS, max_scrolls=1)

    for args in _gestures(driver):
        assert "elementId" not in args
        assert {"left", "top", "width", "height"} <= set(args)


# --- scroll_until: the band stop test + best-effort exhaustion (R14/R17) -----
# Window is 1080x2340, so the band centre range is roughly y in [694, 1646].

def test_scroll_until_returns_an_element_inside_the_band():
    el = _El(rect={"x": 0, "y": 800, "width": 1080, "height": 200})   # cy=900, in band
    driver = _Driver(found={"com.app:id/list": [el]})
    assert scroll_until(driver, selectors=SELECTORS, description="row") is el
    assert _gestures(driver) == []          # placed on the first check, no scroll


def test_scroll_until_treats_edge_coincident_bounds_as_not_placed():
    # Clipped at the top edge: the centre reads mid-screen but the bounds are
    # unreliable, so it is not accepted as placed — the search scrolls first.
    clipped = _El(rect={"x": 0, "y": 0, "width": 1080, "height": 1200})
    driver = _Driver(found={"com.app:id/list": [clipped]})
    result = scroll_until(driver, selectors=SELECTORS, description="row")
    assert _gestures(driver), "a clipped box must not count as placed"
    assert result is clipped                # ...then returned best effort (R17)


def test_scroll_until_returns_a_found_but_unplaced_element_best_effort():
    # On screen but below the band, and content that will not move: the verb
    # returns the element rather than raising (R17 — a structurally-stuck row).
    low = _El(rect={"x": 0, "y": 2100, "width": 1080, "height": 200})   # cy=2200
    driver = _Driver(found={"com.app:id/list": [low]})
    assert scroll_until(driver, selectors=SELECTORS, description="row",
                        max_scrolls=3) is low


def test_scroll_until_raises_only_when_the_target_is_never_found():
    driver = _Driver(found={})              # the selector never resolves
    with pytest.raises(ElementNotFound):
        scroll_until(driver, selectors=SELECTORS, description="row")


# --- a screen-level percent is a share of the screen ------------------------


def test_a_screen_percent_scroll_measures_against_the_screen_height():
    """45% of a 2340px screen is 1053px. Delivered through the container under
    the centre (1500px tall, ~1125px of travel per full gesture), that is one
    gesture of 1053/1125 — not a 0.45 gesture that moves ~45% of the container
    at three-quarter travel."""
    container = _El("list", {"x": 0, "y": 600, "width": 1080, "height": 1500})
    driver = _Driver(found={"scrollable(true)": [container]})
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=45)

    (args,) = _gestures(driver)
    assert args["elementId"] == "list"
    assert args["percent"] == pytest.approx((0.45 * 2340) / (0.75 * 1500))


def test_a_screen_percent_larger_than_the_container_spans_gestures():
    """100% of the screen (2340px) through a 1500px container is two full
    gestures and a remainder, the same delivery a pixel distance gets."""
    container = _El("list", {"x": 0, "y": 600, "width": 1080, "height": 1500})
    driver = _Driver(found={"scrollable(true)": [container]})
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=100)

    percents = [args["percent"] for args in _gestures(driver)]
    assert percents == pytest.approx([1.0, 1.0, (2340 - 2 * 1125) / 1125])


def test_a_horizontal_screen_percent_measures_against_the_screen_width():
    container = _El("row", {"x": 0, "y": 600, "width": 1080, "height": 1500})
    driver = _Driver(found={"scrollable(true)": [container]})
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="right", value=50)

    (args,) = _gestures(driver)
    assert args["percent"] == pytest.approx((0.5 * 1080) / (0.75 * 1080))


def test_a_screen_percent_without_a_container_still_measures_against_the_screen():
    """With nothing scrollable under the centre the gesture falls back to the
    inset rectangle, and the distance is still a share of the full screen."""
    driver = _Driver(found={})
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=45)

    (args,) = _gestures(driver)
    assert "left" in args and "elementId" not in args
    inset_height = 2340 - 2 * int(2340 * 0.15)
    assert args["percent"] == pytest.approx((0.45 * 2340) / (0.75 * inset_height))


def test_an_element_scoped_percent_keeps_the_elements_own_meaning():
    """Naming the container keeps percent as a share of that container: one
    0.45 gesture, unchanged."""
    driver = _Driver(found={"com.app:id/list": [_El()]})
    with step("s"):
        scroll(driver, selectors=SELECTORS, kind="percent", direction="down", value=45)

    (args,) = _gestures(driver)
    assert args["percent"] == pytest.approx(0.45)


# --- iOS: the drag travels the asked distance -------------------------------


class _IOSDriver:
    """Records the W3C pointer batches an iOS scroll is delivered as."""

    page_source = "<AppiumAUT/>"

    def __init__(self, found=None, window=(400, 1000)):
        self._found = found or {}
        self._window = window
        self.actions = []
        self.scripts = []

    def get_window_size(self):
        return {"width": self._window[0], "height": self._window[1]}

    def find_elements(self, by, value):
        return self._found.get(value, [])

    def execute_script(self, script, args=None):
        self.scripts.append((script, args))
        return True

    def execute(self, command, params=None):
        self.actions.append((command, params))
        return {"value": None}

    def drags(self):
        """Signed vertical travel of each W3C pointer batch, in points."""
        out = []
        for _, params in self.actions:
            moves = [a for d in params["actions"] for a in d["actions"]
                     if a["type"] == "pointerMove"]
            out.append(moves[-1]["y"] - moves[0]["y"])
        return out


@pytest.fixture
def ios(monkeypatch):
    monkeypatch.setitem(_config._config, "platform", "ios")


def test_ios_screen_percent_drags_the_asked_share_of_the_screen(ios):
    """45% of a 1000pt screen is a 450pt drag. The finger travels 0.90 of the
    box it swipes, and the distance is divided by THAT — not by scrollGesture's
    0.75 — so it is not stretched to 540pt."""
    driver = _IOSDriver()
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=45)

    assert driver.scripts == []
    assert driver.drags() == pytest.approx([-450], abs=1)


def test_ios_pixel_scroll_drags_the_asked_distance(ios):
    driver = _IOSDriver()
    with step("s"):
        scroll(driver, selectors=None, kind="pixels", direction="down", value=450)

    assert driver.drags() == pytest.approx([-450], abs=1)


def test_ios_screen_percent_through_a_container_still_travels_the_screen_share(ios, monkeypatch):
    """45% of a 2340pt screen is 1053pt, delivered as a drag over the 1500pt
    container under the centre: one 1053pt drag."""
    from testmu_appium import _action_scroll
    container = _El("list", {"x": 0, "y": 600, "width": 1080, "height": 1500})
    monkeypatch.setattr(_action_scroll, "scrollable_containers", lambda driver: [container])
    driver = _IOSDriver(window=(1080, 2340))
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=45)

    assert driver.drags() == pytest.approx([-1053], abs=1)


class _FixedSurface(_Driver):
    """A scrollable whose tree never changes while it scrolls — a multiline
    EditText exposing its full text, a custom surface exposing only its
    container. The driver's canScrollMore is the only movement signal."""

    page_source = (
        "<hierarchy rotation='0'>"
        "<node class='android.widget.EditText' resource-id='com.app:id/notes'"
        " scrollable='true' text='forty lines, viewport fixed'"
        " bounds='[0,600][1080,1600]'/>"
        "</hierarchy>"
    )

    def __init__(self, answers):
        super().__init__(found={}, can_scroll=True)
        self._answers = list(answers)
        self._surface = _El("notes", {"x": 0, "y": 600, "width": 1080, "height": 1000})

    def find_elements(self, by, value):
        return [self._surface] if "scrollable" in value else []

    def execute_script(self, script, args=None):
        self.scripts.append((script, args))
        if script == "mobile: scrollGesture":
            return self._answers.pop(0) if self._answers else False
        return True


def test_a_surface_with_no_observable_content_defers_to_the_driver():
    """The scrolled surface's own row is fixed by definition, so it is no
    evidence either way. With nothing else inside the box the probe is
    inconclusive and the driver's canScrollMore decides — the loop must not
    stop one gesture in on a surface that reports more content."""
    driver = _FixedSurface(answers=[True, True, True, False])
    with step("s"):
        answer = scroll(driver, selectors=None, kind="edge",
                        direction="down", value=None)
    assert answer is False
    assert len(_gestures(driver)) == 4


# --- a selector-less scroll aimed at a recorded point --------------------------
#
# A control nothing can name (a NumberPicker with no id or text) is recorded by
# its coordinate basis. The screen scroll then aims at the container under THAT
# point, not under the screen centre, and drags from the point itself when the
# device reports no container there.

_DRUM_BASIS = {"x_ratio": 0.5, "y_ratio": 0.5667, "orientation": "portrait",
               "window": [1080, 2340]}


class _PointDriver(_Driver):
    """Records W3C pointer batches beside scripts, for the drag path."""

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.actions = []

    def execute(self, command, params=None):
        self.actions.append((command, params))
        return {"value": None}

    def drags(self):
        out = []
        for _, params in self.actions:
            moves = [a for d in params["actions"] for a in d["actions"]
                     if a["type"] == "pointerMove"]
            out.append(((moves[0]["x"], moves[0]["y"]), (moves[-1]["x"], moves[-1]["y"])))
        return out


def test_a_recorded_point_picks_the_container_under_it_not_the_centre():
    """The page list holds the screen centre; the drum sits lower, where the
    author scrolled. The basis aims the gesture at the drum."""
    page = _El("page", {"x": 0, "y": 0, "width": 1080, "height": 2340})
    drum = _El("drum", {"x": 72, "y": 1079, "width": 936, "height": 495})
    driver = _PointDriver(found={"scrollable(true)": [page, drum]}, window=(1080, 2340))
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=70,
               fallback_coordinates=_DRUM_BASIS)

    (args,) = _gestures(driver)
    assert args["elementId"] == "drum"
    assert driver.actions == []


def test_no_container_under_the_point_drags_from_the_point():
    """The device flags nothing scrollable at the point (a NumberPicker on some
    builds). The finger lands on the point and drags the asked share of the
    screen upward for a downward scroll — no screen-rectangle swipe."""
    driver = _PointDriver(found={}, window=(1080, 2340))
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=70,
               fallback_coordinates=_DRUM_BASIS)

    assert _gestures(driver) == []
    ((sx, sy), (ex, ey)),  = driver.drags()
    assert (sx, sy) == (540, 1326)
    assert ex == 540 and ey < sy
    # One drag is capped at 15% of the inset screen: 0.15 * 1638 = 245px, not
    # the asked 70% — a screen-sized fling spins a drum past the target row.
    assert sy - ey == 245
    # ...and slow enough to be tracked rather than flung: 245px at 0.4px/ms.
    (_, params), = driver.actions
    moves = [a for d in params["actions"] for a in d["actions"] if a["type"] == "pointerMove"]
    assert moves[-1]["duration"] == 612


def test_a_point_outside_the_inset_never_drags_against_the_direction():
    """y_ratio 0.05 lands in the status-bar strip, above the inset top (351 on
    a 2340 screen). The start clamps into the inset like the endpoints do, so a
    downward scroll moves the finger up or not at all — unclamped, the end
    (351) would sit BELOW the start (117) and the drag would scroll backwards."""
    driver = _PointDriver(found={}, window=(1080, 2340))
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=70,
               fallback_coordinates={**_DRUM_BASIS, "y_ratio": 0.05})

    ((sx, sy), (_ex, ey)), = driver.drags()
    assert (sx, sy) == (540, 351)
    assert ey <= sy


def test_a_pixel_scroll_covers_the_asked_distance_in_capped_drags():
    """1000px asked; one drag is capped at 245px (15% of the inset span), so
    the ask is delivered as five drags summing to the distance — not one capped
    drag with the remaining 755px booked as covered and never attempted."""
    driver = _PointDriver(found={}, window=(1080, 2340))
    with step("s"):
        scroll(driver, selectors=None, kind="pixels", direction="down", value=1000,
               fallback_coordinates=_DRUM_BASIS)

    drags = driver.drags()
    assert len(drags) == 5
    total = sum(start[1] - end[1] for start, end in drags)
    assert 990 <= total <= 1000


def test_a_point_from_the_other_orientation_falls_back_to_the_centre():
    """A landscape recording on a portrait screen would land somewhere else, so
    the basis is refused and the scroll aims the way it always has."""
    page = _El("page", {"x": 0, "y": 0, "width": 1080, "height": 2340})
    driver = _PointDriver(found={"scrollable(true)": [page]}, window=(1080, 2340))
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=70,
               fallback_coordinates={**_DRUM_BASIS, "orientation": "landscape"})

    (args,) = _gestures(driver)
    assert args["elementId"] == "page"
    assert driver.actions == []


def test_without_a_basis_the_screen_scroll_is_unchanged():
    page = _El("page", {"x": 0, "y": 0, "width": 1080, "height": 2340})
    driver = _PointDriver(found={"scrollable(true)": [page]}, window=(1080, 2340))
    with step("s"):
        scroll(driver, selectors=None, kind="percent", direction="down", value=70)

    (args,) = _gestures(driver)
    assert args["elementId"] == "page"
