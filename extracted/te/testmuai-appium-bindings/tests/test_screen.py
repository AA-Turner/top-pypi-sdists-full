"""Reading the screen size off a driver that may not serve the standard route.

The behaviour under test is a fallback chain, and the two things that make it
worth having are invisible in a "does it return a number" test: that it prefers
the SPEC route over a driver extension, and that it stops re-probing a route the
session has already refused.
"""
import pytest

from testmu_appium._helpers import _screen


class _Driver:
    """A driver that serves exactly the routes it was told to.

    Every route records that it was called, so a test can assert on what was NOT
    asked as well as what was.
    """

    def __init__(self, *, w3c=None, screen_info=None, source=None, session="s1"):
        self._w3c = w3c
        self._screen_info = screen_info
        self._source = source
        self.session_id = session
        self.calls = []

    def get_window_size(self):
        self.calls.append("w3c")
        if self._w3c is None:
            raise RuntimeError("Unhandled endpoint: /session/x/window/rect")
        return self._w3c

    def execute_script(self, script, *args):
        self.calls.append(script)
        if script != "mobile: deviceScreenInfo" or self._screen_info is None:
            raise RuntimeError("Unhandled endpoint: /wda/screen")
        return self._screen_info

    @property
    def page_source(self):
        self.calls.append("source")
        if self._source is None:
            raise RuntimeError("no source")
        return self._source


#: What `mobile: deviceScreenInfo` actually returns, captured from a device.
SCREEN_INFO = {
    "statusBarSize": {"width": 414, "height": 48},
    "scale": 2,
    "screenSize": {"width": 414, "height": 896},
}

SOURCE = (
    '<XCUIElementTypeApplication type="XCUIElementTypeApplication" '
    'x="0" y="0" width="414" height="896"/>'
)


@pytest.fixture(autouse=True)
def _forget():
    _screen.reset()
    yield
    _screen.reset()


class TestTheOrderIsThePlatforms:
    """iOS on a 9.x driver CANNOT answer the spec route — asking it first was
    a guaranteed failed round trip plus a warning at every session start.
    Android CANNOT answer the extension (`deviceScreenInfo` is XCUITest's).
    Each platform asks in the order it can actually answer."""

    def test_ios_never_pays_the_dead_spec_call(self, monkeypatch):
        from testmu_appium import _config

        monkeypatch.setitem(_config._config, "platform", "ios")
        driver = _Driver(w3c={"width": 414, "height": 896},
                         screen_info=SCREEN_INFO)
        assert _screen.window_size(driver) == (414, 896)
        assert driver.calls == ["mobile: deviceScreenInfo"], (
            "the spec route must not be probed when the extension answers")

    def test_ios_still_reaches_the_spec_route_as_backup(self, monkeypatch):
        from testmu_appium import _config

        monkeypatch.setitem(_config._config, "platform", "ios")
        driver = _Driver(w3c={"width": 400, "height": 800})
        assert _screen.window_size(driver) == (400, 800)
        assert driver.calls == ["mobile: deviceScreenInfo", "w3c"]

    def test_android_still_asks_the_spec_route_first(self):
        driver = _Driver(w3c={"width": 1080, "height": 2400},
                         screen_info=SCREEN_INFO)
        assert _screen.window_size(driver) == (1080, 2400)
        assert driver.calls == ["w3c"]

    def test_an_explicit_platform_beats_an_unconfigured_default(self):
        """The FIRST read of a run happens at session open, before anything
        has called configure(platform=...) — the configured platform is still
        the default (android) at that moment, which re-asked the dead spec
        route on every iOS session start. A caller that knows its platform
        says so and gets that platform's order."""
        driver = _Driver(w3c={"width": 414, "height": 896},
                         screen_info=SCREEN_INFO)
        assert _screen.window_size(driver, platform="ios") == (414, 896)
        assert driver.calls == ["mobile: deviceScreenInfo"]


class TestWhichRouteIsUsed:
    def test_the_standard_route_wins_when_the_driver_serves_it(self):
        """A driver implementing the spec must never be routed around — the
        extension exists to cover its absence, not to replace it."""
        driver = _Driver(w3c={"width": 390, "height": 844}, screen_info=SCREEN_INFO)
        assert _screen.window_size(driver) == (390, 844)
        assert driver.calls == ["w3c"]

    def test_the_driver_extension_covers_a_missing_standard_route(self):
        """xcuitest-driver 9.x asks WDA for /window/rect, which WDA has never
        implemented. /wda/screen answers on the same agent."""
        driver = _Driver(screen_info=SCREEN_INFO, source=SOURCE)
        assert _screen.window_size(driver) == (414, 896)
        assert "mobile: deviceScreenInfo" in driver.calls
        assert "source" not in driver.calls, "the document should not be fetched"

    def test_the_document_is_the_last_resort(self):
        driver = _Driver(source=SOURCE)
        assert _screen.window_size(driver) == (414, 896)
        assert driver.calls[-1] == "source"

    def test_losing_every_route_says_what_was_tried(self):
        driver = _Driver()
        with pytest.raises(RuntimeError) as exc:
            _screen.window_size(driver)
        for route in ("w3c", "screen_info", "page_source"):
            assert route in str(exc.value)


class TestTheScaleIsNotApplied:
    def test_points_are_returned_not_pixels(self):
        """`scale: 2` is points-to-pixels. iOS is points end to end — Appium taps
        in points and the element tree is in points — so multiplying here would
        double every coordinate on a 2x device."""
        driver = _Driver(screen_info=SCREEN_INFO)
        assert _screen.window_size(driver) == (414, 896)


class TestTheChoiceIsRemembered:
    def test_a_refused_route_is_not_probed_twice(self):
        """Without this every consumer pays a failing round trip before falling
        back — on every scroll, every vision lookup, every capture."""
        driver = _Driver(screen_info=SCREEN_INFO)
        _screen.window_size(driver)
        driver.calls.clear()
        _screen.window_size(driver)
        assert driver.calls == ["mobile: deviceScreenInfo"]

    def test_a_different_session_probes_afresh(self):
        """The limitation belongs to the driver behind a session, so a later
        session on a newer one must not inherit this one's verdict."""
        old = _Driver(screen_info=SCREEN_INFO, session="old")
        _screen.window_size(old)
        new = _Driver(w3c={"width": 390, "height": 844},
                      screen_info=SCREEN_INFO, session="new")
        assert _screen.window_size(new) == (390, 844)
        assert new.calls == ["w3c"]


class TestFailuresKeepTheirEvidence:
    """This helper runs inside every capture, so it is often the FIRST place a
    dying session is observed. The runner classifies a dead session by message
    substrings ("invalid session id", "socket hang up"); a bare exception type
    name carries none of them, and swallowing the message here defeated the
    auto-reconnect built on those markers."""

    class _DyingDriver(_Driver):
        def get_window_size(self):
            raise RuntimeError("A session is either terminated or not started "
                               "(invalid session id)")

        def execute_script(self, script, *args):
            raise RuntimeError("socket hang up")

        @property
        def page_source(self):
            raise RuntimeError("could not proxy command to the remote server")

    def test_the_original_messages_survive_the_reraise(self):
        with pytest.raises(RuntimeError) as exc:
            _screen.window_size(self._DyingDriver())
        message = str(exc.value)
        assert "invalid session id" in message
        assert "socket hang up" in message
        assert "could not proxy command to the remote server" in message


class TestTheDocumentReaderIsNeverPinned:
    """The document wins only when both cheap routes failed — and a TRANSIENT
    failure would otherwise pin a whole-tree fetch onto every remaining size
    read of the session. The cheap routes are re-offered on the next call."""

    def test_a_transient_w3c_failure_does_not_pin_page_source(self):
        driver = _Driver(source=SOURCE, session="flaky")
        assert _screen.window_size(driver) == (414, 896)  # both cheap routes down

        recovered = _Driver(w3c={"width": 414, "height": 896}, session="flaky")
        assert _screen.window_size(recovered) == (414, 896)
        assert recovered.calls == ["w3c"], "the cheap route is offered again"

    def test_the_cheap_extension_is_still_pinned(self):
        driver = _Driver(screen_info=SCREEN_INFO)
        _screen.window_size(driver)
        driver.calls.clear()
        _screen.window_size(driver)
        assert driver.calls == ["mobile: deviceScreenInfo"]


class TestZeroSizedNodesDoNotAnswer:
    """A mid-transition capture can put a zero-sized node first in document
    order; answering (0, 0) would poison every ratio computed against it —
    and the pin would keep it for the session."""

    _ZERO_FIRST = (
        '<AppiumAUT>'
        '<XCUIElementTypeOther width="0" height="0">'
        '<XCUIElementTypeApplication x="0" y="0" width="414" height="896"/>'
        '</XCUIElementTypeOther>'
        '</AppiumAUT>'
    )

    def test_the_first_non_zero_node_answers(self):
        driver = _Driver(source=self._ZERO_FIRST)
        assert _screen.window_size(driver) == (414, 896)

    def test_a_document_with_no_non_zero_node_refuses(self):
        driver = _Driver(source='<AppiumAUT><a width="0" height="0"/></AppiumAUT>')
        with pytest.raises(RuntimeError) as exc:
            _screen.window_size(driver)
        assert "non-zero" in str(exc.value)
