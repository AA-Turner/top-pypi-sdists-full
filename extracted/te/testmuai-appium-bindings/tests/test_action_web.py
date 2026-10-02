"""Acting on web content: locate over the debug channel, act with Appium."""
import pytest

from testmu_appium import _action_web
from testmu_appium._errors import ElementNotFound
from testmu_appium._helpers import _web, _web_ios

PAGE = {"dpr": 3, "scale": 1.0, "offsetLeft": 0, "offsetTop": 0,
        "viewportWidth": 360, "viewportHeight": 800, "blockedUrls": [],
        "elements": [
            {"tag": "BUTTON", "label": "Pay now", "css": "#pay", "path": "",
             "dom_path": [{"kind": "element", "nodes": [0, 1]}],
             "interactive": True, "editable": False, "states": [],
             "x": 10, "y": 20, "w": 100, "h": 40},
            {"tag": "A", "label": "Terms", "css": "a", "path": "",
             "dom_path": [{"kind": "element", "nodes": [0, 2]}],
             "interactive": True, "editable": False, "states": [],
             "x": 10, "y": 80, "w": 60, "h": 20},
            {"tag": "A", "label": "Privacy", "css": "a", "path": "",
             "dom_path": [{"kind": "element", "nodes": [0, 3]}],
             "interactive": True, "editable": False, "states": [],
             "x": 90, "y": 80, "w": 60, "h": 20},
            {"tag": "DIV", "label": "hidden", "css": "#ghost", "path": "",
             "dom_path": [{"kind": "element", "nodes": [0, 4]}],
             "interactive": True, "editable": False, "states": [],
             "x": -9000, "y": -9000, "w": 50, "h": 50},
        ]}


class _Channel:
    def __init__(self, page=None, frames=(), frame_pages=None, visible=True):
        self._page = page or PAGE
        self._frames = list(frames)
        self._frame_pages = frame_pages or {}
        self._visible = visible
        self.read_frames = []

    def is_visible(self):
        return self._visible

    def read_page(self):
        return self._page

    def unreachable_frames(self, page, seen=()):
        return [f for f in self._frames if f[1] not in set(seen)]

    def read_frame(self, frame_id, path=""):
        self.read_frames.append(frame_id)
        page = self._frame_pages.get(frame_id)
        if page is None:
            return None
        return {**page, "elements": [{**e, "path": path + e.get("path", "")}
                                     for e in page.get("elements", [])]}


def _native(label, bounds):
    return {"text": label, "content_desc": "", "name": label, "bounds": bounds}


#: The device's view of PAGE's first two elements, at origin (0, 250), dpr 3.
NATIVE = [
    _native("Pay now", (30, 310, 330, 430)),
    _native("Terms", (30, 490, 210, 550)),
]


def _elements(channel=None):
    _, found, _ = _action_web.read_all(channel or _Channel())
    return found


class TestReadAll:
    def test_offscreen_elements_are_read_but_not_actionable(self):
        all_elements, viewport_elements, _ = _action_web.read_all(_Channel())
        assert any(e["css"] == "#ghost" for e in all_elements)
        assert all(e["css"] != "#ghost" for e in viewport_elements)

    def test_elements_in_an_unreachable_frame_are_included(self):
        channel = _Channel(
            frames=[("F1", "https://other.test/")],
            frame_pages={"F1": {"elements": [
                {"tag": "INPUT", "label": "Card", "css": "#card", "path": ">f",
                 "x": 5, "y": 5, "w": 200, "h": 30}]}})
        assert any(e["css"] == "#card" for e in _elements(channel))
        assert channel.read_frames == ["F1"]

    def test_a_frame_that_cannot_be_read_does_not_abort_the_read(self):
        channel = _Channel(frames=[("F1", "https://other.test/")], frame_pages={})
        assert any(e["css"] == "#pay" for e in _elements(channel))

    def test_a_recovery_that_RAISES_does_not_take_the_page_with_it(self):
        """Recovery is enrichment: the page is already walked when it starts.

        A channel whose protocol has no frame vocabulary at all raises here —
        iOS answers `-32601 'Page.getFrameTree' was not found` — and discarding
        23 already-read elements to report none is strictly worse than reporting
        them without the frames the walk was blocked from anyway.
        """
        class _Hostile(_Channel):
            def unreachable_frames(self, page, seen=()):
                raise RuntimeError("Page.getFrameTree: method was not found")

        assert any(e["css"] == "#pay" for e in _elements(_Hostile()))


class TestTheTwoDebuggersAreNotOneProtocol:
    """`Page.getFrameTree` and `Page.createIsolatedWorld` are Chrome-only.

    A WebKit target answers `-32601 method was not found`. Before this, every
    capture of any page carrying a cross-origin iframe paid that round trip
    twice and lost the whole surface with it.
    """

    class _Loud:
        """A wire that fails the test if anything speaks to it."""

        def create_connection(self, *args, **kwargs):
            raise AssertionError("the iOS channel opened a socket to ask a "
                                 "question its protocol cannot answer")

    def _channel(self):
        return _web_ios.IosChannel("ws://unused", websocket_module=self._Loud())

    def test_the_ios_channel_recovers_no_frames(self):
        assert self._channel().unreachable_frames({"blockedUrls": ["https://x/"]}) == []

    def test_and_does_not_go_to_the_wire_to_say_so(self):
        """Cheap matters: this ran on every capture, twice."""
        self._channel().unreachable_frames({"blockedUrls": ["https://x/"]}, seen=())

    def test_the_android_channel_still_asks(self):
        """The Chrome path is unchanged — it is the one where these methods exist."""
        assert _web.Channel.unreachable_frames is not _web_ios.IosChannel.unreachable_frames


class TestLocate:
    def test_a_unique_css_selector_resolves(self):
        found = _action_web.locate(_elements(), [{"strategy": "css", "selector": "#pay"}])
        assert found["label"] == "Pay now"


class TestPreparedTarget:
    class _Probe:
        def __init__(self, state):
            self.state = state
            self.expressions = []

        def evaluate(self, expression):
            self.expressions.append(expression)
            return self.state

    @staticmethod
    def _state(element, **changes):
        page = PAGE
        values = {
            "visibility": "visible",
            "scroll_x": page.get("scrollX", 0),
            "scroll_y": page.get("scrollY", 0),
            "dpr": page["dpr"],
            "scale": page["scale"],
            "offset_left": page["offsetLeft"],
            "offset_top": page["offsetTop"],
            "viewport_width": page["viewportWidth"],
            "viewport_height": page["viewportHeight"],
            "visual_width": page["viewportWidth"],
            "visual_height": page["viewportHeight"],
            "x": element["x"], "y": element["y"],
            "w": element["w"], "h": element["h"],
            "disabled": element.get("disabled", False),
            "tag": element["tag"], "label": element["label"],
        }
        values.update(changes)
        return list(values.values())

    def test_same_top_document_target_and_viewport_are_reused(self):
        element = PAGE["elements"][1]  # generic css 'a', exact dom_path
        probe = self._Probe(self._state(element))
        surface = _action_web.Surface(
            probe, [element], [element], PAGE, (0, 250), {}
        )
        assert _action_web.prepared_target_is_current(surface, element) is True
        assert element["dom_path"][0]["nodes"] == [0, 2]
        assert "querySelectorAll" not in probe.expressions[0]

    @pytest.mark.parametrize("change", [
        {"x": 30}, {"scroll_y": 20}, {"scale": 2},
        {"visibility": "hidden"}, {"disabled": True}, {"label": "Other"},
    ])
    def test_target_or_viewport_drift_falls_back(self, change):
        element = PAGE["elements"][0]
        surface = _action_web.Surface(
            self._Probe(self._state(element, **change)),
            [element], [element], PAGE, (0, 250), {},
        )
        assert _action_web.prepared_target_is_current(surface, element) is False

    def test_frame_target_falls_back_without_a_probe(self):
        element = {**PAGE["elements"][0], "path": ">f0"}
        probe = self._Probe(self._state(element))
        surface = _action_web.Surface(
            probe, [element], [element], PAGE, (0, 250), {}
        )
        assert _action_web.prepared_target_is_current(surface, element) is False
        assert probe.expressions == []


class TestWebPerception:
    class _Driver:
        def get_window_size(self):
            return {"width": 1080, "height": 2340}

        def get_screenshot_as_png(self):
            return b"\x89PNG"

    def test_dom_rows_use_the_canonical_generated_tree_shape(self):
        surface = _action_web.open_surface(_Channel(), NATIVE)
        perception = _action_web.capture_perception(
            self._Driver(), surface, "click"
        )
        assert perception.entries
        assert set(perception.entries[0]) == {
            "index", "role", "name", "states", "position_hint"
        }
        assert perception.entries[0]["name"] == "Pay now"
        assert "dom_path" not in perception.entries[0]
        assert perception.descriptors[1]["dom_path"]
        assert perception.screenshot_b64

    def test_type_candidates_are_limited_to_editable_dom_rows(self):
        page = {
            **PAGE,
            "elements": [
                *PAGE["elements"],
                {
                    "tag": "INPUT", "label": "Email", "css": "#email", "path": ">f0",
                    "dom_path": [{"kind": "element", "nodes": [0, 5]}],
                    "interactive": True, "editable": True, "states": [],
                    "x": 10, "y": 140, "w": 200, "h": 40,
                },
            ],
        }
        surface = _action_web.open_surface(_Channel(page), NATIVE)
        perception = _action_web.capture_perception(
            self._Driver(), surface, "type"
        )
        assert [entry["name"] for entry in perception.entries] == ["Email"]
        assert perception.entries[0]["states"] == ["in-frame"]

    def test_readonly_and_non_text_inputs_are_not_type_candidates(self):
        controls = [
            {
                "tag": "INPUT", "label": "Account", "css": "#readonly",
                "path": "", "dom_path": [{"kind": "element", "nodes": [0, 5]}],
                "interactive": True, "editable": False, "input_type": "text",
                "states": ["readonly"], "x": 10, "y": 140, "w": 200, "h": 40,
            },
            {
                "tag": "INPUT", "label": "Remember", "css": "#remember",
                "path": "", "dom_path": [{"kind": "element", "nodes": [0, 6]}],
                "interactive": True, "editable": False, "input_type": "checkbox",
                "states": [], "x": 10, "y": 190, "w": 40, "h": 40,
            },
        ]
        surface = _action_web.open_unplaced_surface(
            _Channel({**PAGE, "elements": controls})
        )
        perception = _action_web.capture_perception(
            self._Driver(), surface, "type"
        )
        assert perception.entries == []

    def test_a_healed_input_descriptor_keeps_its_input_type(self):
        text = {
            "tag": "INPUT", "label": "Code", "css": "#code", "path": "",
            "dom_path": [{"kind": "element", "nodes": [0, 5]}],
            "interactive": True, "editable": True, "input_type": "text",
        }
        descriptor = _action_web.descriptor_for(text)
        assert descriptor["input_type"] == "text"
        assert _action_web.resolve_descriptor(
            [{**text, "input_type": "password"}], descriptor
        ) is None

    def test_web_select_is_not_offered_until_it_has_a_replay_runner(self):
        select = {
            "tag": "SELECT", "label": "Country", "css": "#country", "path": "",
            "dom_path": [{"kind": "element", "nodes": [0, 6]}],
            "interactive": True, "editable": False, "states": [],
            "x": 10, "y": 200, "w": 200, "h": 40,
        }
        surface = _action_web.open_surface(
            _Channel({**PAGE, "elements": [*PAGE["elements"], select]}),
            NATIVE,
        )
        perception = _action_web.capture_perception(
            self._Driver(), surface, "click"
        )
        assert "Country" not in [entry["name"] for entry in perception.entries]


class TestLocateContinued:
    def test_an_ambiguous_selector_is_skipped_like_a_miss(self):
        """Two links both serialise to `a`. Acting on the first would be a
        confident wrong click."""
        assert _action_web.locate(
            _elements(), [{"strategy": "css", "selector": "a"}]) is None

    def test_a_later_selector_is_tried_when_the_first_is_ambiguous(self):
        found = _action_web.locate(_elements(), [
            {"strategy": "css", "selector": "a"},
            {"strategy": "text", "selector": "Privacy"},
        ])
        assert found["label"] == "Privacy"

    def test_a_label_selector_resolves_where_css_cannot(self):
        """Most web elements carry no id — 14 of 19 on a real page — so labels
        do the work the css strategy cannot."""
        found = _action_web.locate(
            _elements(), [{"strategy": "text", "selector": "Terms"}])
        assert found["css"] == "a"

    def test_type_does_not_accept_a_same_named_non_editable_label(self):
        password_label = {
            "tag": "LABEL", "label": "Password", "css": "label", "path": "",
            "dom_path": [{"kind": "element", "nodes": [0, 8]}],
            "interactive": True, "editable": False, "states": [],
            "x": 10, "y": 300, "w": 120, "h": 30,
        }
        assert _action_web.locate(
            [password_label],
            [
                {"strategy": "css", "selector": "#password"},
                {"strategy": "text", "selector": "Password"},
            ],
            action_type="type",
        ) is None

    def test_nothing_matching_yields_none(self):
        assert _action_web.locate(
            _elements(), [{"strategy": "css", "selector": "#absent"}]) is None

    def test_a_frame_path_separates_the_same_selector_in_two_frames(self):
        elements = [
            {"label": "Pay", "css": "#pay", "path": "", "x": 0, "y": 0, "w": 1, "h": 1},
            {"label": "Pay", "css": "#pay", "path": ">f", "x": 0, "y": 9, "w": 1, "h": 1},
        ]
        found = _action_web.locate(
            elements, [{"strategy": "css", "selector": "#pay"}], frame_path=">f")
        assert found["y"] == 9

    def test_a_frame_path_that_matches_nothing_does_not_lose_the_element(self):
        """A page that has since gained or lost a frame gives the same element a
        different path; the selector still resolving is what matters."""
        found = _action_web.locate(
            _elements(), [{"strategy": "css", "selector": "#pay"}], frame_path=">s>f")
        assert found["label"] == "Pay now"

    def test_replay_does_not_accept_a_unique_match_from_the_wrong_frame(self):
        only_other_frame = [{
            "label": "Pay", "css": "#pay", "path": ">f1",
            "x": 0, "y": 0, "w": 1, "h": 1,
        }]
        assert _action_web.locate(
            only_other_frame,
            [{"strategy": "css", "selector": "#pay"}],
            frame_path=">f0",
            strict_path=True,
        ) is None

    def test_replay_treats_empty_frame_path_as_strict_top_document_identity(self):
        only_frame = [{
            "label": "Pay", "css": "#pay", "path": ">f0",
            "x": 0, "y": 0, "w": 1, "h": 1,
        }]
        assert _action_web.locate(
            only_frame,
            [{"strategy": "css", "selector": "#pay"}],
            frame_path="",
            strict_path=True,
        ) is None


class TestHealedDescriptor:
    def test_frame_identity_is_strict_even_when_local_paths_are_identical(self):
        route = [{"kind": "element", "nodes": [0, 1]}]
        elements = [
            {
                "tag": "BUTTON", "label": "Pay", "role": "", "path": ">f0",
                "dom_path": route, "interactive": True, "editable": False,
            },
            {
                "tag": "BUTTON", "label": "Pay", "role": "", "path": ">f1",
                "dom_path": route, "interactive": True, "editable": False,
            },
        ]
        descriptor = _action_web.descriptor_for(elements[1])
        assert _action_web.resolve_descriptor(elements, descriptor) is elements[1]

    def test_a_changed_structural_path_is_unresolved(self):
        element = PAGE["elements"][0]
        descriptor = _action_web.descriptor_for(element)
        moved = {
            **element,
            "dom_path": [{"kind": "element", "nodes": [0, 9]}],
        }
        assert _action_web.resolve_descriptor([moved], descriptor) is None

    def test_an_element_that_became_disabled_is_unresolved(self):
        element = {**PAGE["elements"][0], "disabled": False}
        descriptor = _action_web.descriptor_for(element)
        disabled = {
            **element, "disabled": True, "states": ["disabled"],
        }
        assert _action_web.resolve_descriptor([disabled], descriptor) is None


class TestCalibration:
    def test_the_origin_is_solved_from_elements_both_surfaces_describe(self):
        samples = _action_web.calibration_samples(_elements(), NATIVE)
        origin, _ = _action_web.calibrate(samples, dpr=3, scale=1)
        assert origin == (0, 250)

    def test_one_sample_is_not_enough_to_calibrate(self):
        """A single sample cannot be cross-checked, and single samples were seen
        to disagree by 59 px where the tree described a different box."""
        samples = _action_web.calibration_samples(_elements(), NATIVE[:1])
        origin, _ = _action_web.calibrate(samples, dpr=3, scale=1)
        assert origin is None

    def test_a_disagreeing_sample_is_discarded_rather_than_averaged(self):
        native = [*NATIVE, _native("Privacy", (30, 9000, 210, 9060))]
        samples = _action_web.calibration_samples(_elements(), native)
        origin, agreeing = _action_web.calibrate(samples, dpr=3, scale=1)
        assert origin == (0, 250)
        assert [label for label, _ in agreeing] == ["Pay now", "Terms"]

    def test_a_label_naming_two_native_elements_is_not_a_sample(self):
        native = [*NATIVE, _native("Terms", (0, 0, 10, 10))]
        samples = _action_web.calibration_samples(_elements(), native)
        assert [s[0] for s in samples] == ["Pay now"]

    def test_a_label_naming_two_web_elements_is_not_a_sample(self):
        """Both links serialise the same label in this page; neither identifies
        the element the tree was describing."""
        samples = _action_web.calibration_samples(
            _elements(), [_native("Terms", (0, 0, 10, 10)),
                          _native("Privacy", (0, 0, 10, 10))])
        assert all(s[0] != "a" for s in samples)


class TestOpenSurface:
    def test_a_calibrated_page_becomes_a_surface(self):
        surface = _action_web.open_surface(_Channel(), NATIVE)
        assert surface.origin == (0, 250)
        assert set(surface.twins) == {"Pay now", "Terms"}

    def test_offscreen_duplicates_do_not_make_calibration_ambiguous(self):
        duplicate = {
            **PAGE["elements"][0], "css": "#pay-later", "y": 1200,
        }
        surface = _action_web.open_surface(
            _Channel({**PAGE, "elements": [*PAGE["elements"], duplicate]}), NATIVE)
        assert surface.origin == (0, 250)
        assert len(surface.all_elements) == len(PAGE["elements"]) + 1
        assert duplicate not in surface.elements

    def test_a_page_that_shares_nothing_with_the_device_is_not_the_one_on_screen(self):
        """Every open tab publishes a debug target and none says which is
        visible; sharing content with the accessibility tree is what does."""
        assert _action_web.open_surface(_Channel(), [_native("Other app", (0, 0, 5, 5))]) is None


class TestASingleSampleCorroboratedByTheContainer:
    """A screen can share almost nothing with the page and still be placeable.

    Two samples are required because a lone one cannot be cross-checked. The
    accessibility tree carries a second opinion that needs no second element —
    the WebView node's own top-left. Measured on a Google suggestions screen: 41
    native rows, 33 of them keyboard keys, ONE shared label, solving (5, 141) —
    byte-identical to the WebView's box. The page was discarded and everything on
    it became unreachable.
    """

    #: Only "Pay now" is shared; "Terms" is not on the device's tree.
    ONE_SHARED = [_native("Pay now", (30, 310, 330, 430))]

    def _webview(self, bounds):
        return {"text": "", "content_desc": "", "name": "", "role": "webview",
                "cls": "XCUIElementTypeWebView", "bounds": bounds}

    def test_one_sample_alone_is_still_refused(self):
        """Unchanged: without corroboration a lone sample is not enough."""
        assert _action_web.open_surface(_Channel(), self.ONE_SHARED) is None

    def test_one_sample_the_webview_box_agrees_with_is_accepted(self):
        native = [*self.ONE_SHARED, self._webview((0, 250, 414, 900))]
        surface = _action_web.open_surface(_Channel(), native)
        assert surface is not None
        assert surface.origin == (0, 250)

    def test_a_browser_drawing_chrome_inside_its_webview_is_still_refused(self):
        """The case the corroboration protects. Safari's WebView node spans the
        whole screen while the page starts below the toolbar, so the box leads
        the content — and a confident wrong origin is worse than none."""
        native = [*self.ONE_SHARED, self._webview((0, 0, 414, 900))]
        assert _action_web.open_surface(_Channel(), native) is None

    def test_the_origin_comes_from_the_measured_sample_not_the_box(self):
        """The box only corroborates. The sample was measured against real
        content, so it is the more precise of the two."""
        native = [*self.ONE_SHARED, self._webview((8, 258, 414, 900))]
        surface = _action_web.open_surface(_Channel(), native)
        assert surface is not None and surface.origin == (0, 250)

    def test_two_agreeing_samples_never_consult_the_container(self):
        surface = _action_web.open_surface(_Channel(), NATIVE)
        assert surface.origin == (0, 250)
        assert set(surface.twins) == {"Pay now", "Terms"}


class TestDevicePoint:
    def test_the_centre_is_converted_through_the_viewport(self):
        element = PAGE["elements"][0]
        assert _action_web.device_point(element, PAGE, origin=(0, 84)) == (180, 204)

    def test_zoom_is_honoured(self):
        element = PAGE["elements"][0]
        zoomed = {**PAGE, "scale": 0.5}
        assert _action_web.device_point(element, zoomed, origin=(0, 84)) == (90, 144)


class TestVerifiedPoint:
    ELEMENT = PAGE["elements"][0]

    def test_a_point_agreeing_with_the_device_is_returned(self):
        point = _action_web.verified_point(
            self.ELEMENT, PAGE, origin=(0, 84), native_bounds=(150, 180, 220, 240))
        assert point == (180, 204)

    def test_a_disagreeing_conversion_refuses_rather_than_tapping(self):
        """The failure mode this exists for: a wrong conversion yields a
        perfectly plausible point somewhere else on the screen."""
        with pytest.raises(ElementNotFound):
            _action_web.verified_point(
                self.ELEMENT, PAGE, origin=(0, 84), native_bounds=(900, 900, 950, 950))

    def test_without_native_bounds_the_point_is_returned_unchecked(self):
        """Not every web element is projected into the accessibility tree, so the
        check applies where it can and does not block where it cannot."""
        assert _action_web.verified_point(self.ELEMENT, PAGE, origin=(0, 84)) == (180, 204)

    def test_a_located_element_is_checked_against_its_own_twin(self):
        surface = _action_web.open_surface(_Channel(), NATIVE)
        element = _action_web.locate(
            surface.elements, [{"strategy": "css", "selector": "#pay"}])
        assert _action_web.point_for(surface, element) == (180, 370)

    def test_the_telemetry_box_is_the_whole_element(self):
        surface = _action_web.open_surface(_Channel(), NATIVE)
        element = _action_web.locate(
            surface.elements, [{"strategy": "css", "selector": "#pay"}])
        assert _action_web.device_bounds(surface, element) == (30, 310, 330, 430)


class _Silent(_Channel):
    """A surface with no page-visibility support: it cannot answer, which is not
    the same as answering "no"."""

    def is_visible(self):
        raise RuntimeError("visibilityState unavailable")


class _Dead:
    """A target whose socket is published but no longer answers — an app's WebView
    that has gone away. It fails when spoken to, not when it is opened."""

    def is_visible(self):
        raise TimeoutError("Connection timed out")

    def read_page(self):
        raise TimeoutError("Connection timed out")


class TestOwnsSocket:
    """Whether a socket could belong to the app currently in the foreground."""

    WEBVIEW = _web.Socket("webview_devtools_remote_200", 200, "webview")
    BROWSER = _web.Socket("chrome_devtools_remote", None, "browser")
    OTHER = _web.Socket("stetho_com.example_devtools_remote", None, "other")

    def test_a_webview_socket_matches_its_owning_pid(self):
        assert _action_web._owns_socket(self.WEBVIEW, {100, 200}, "com.example.app")

    def test_a_webview_socket_is_ruled_out_by_pid_mismatch(self):
        assert not _action_web._owns_socket(self.WEBVIEW, {100}, "com.example.app")

    def test_a_webview_socket_is_kept_when_no_package_context_is_known(self):
        assert _action_web._owns_socket(self.WEBVIEW, None, "")

    def test_the_browser_socket_is_owned_by_a_recognised_browser_package(self):
        assert _action_web._owns_socket(self.BROWSER, {100}, "com.android.chrome")

    def test_the_browser_socket_is_not_owned_by_a_native_app(self):
        assert not _action_web._owns_socket(self.BROWSER, {100}, "com.example.app")

    def test_the_browser_socket_is_kept_when_no_package_context_is_known(self):
        assert _action_web._owns_socket(self.BROWSER, None, "")

    def test_an_unrecognised_socket_never_belongs_to_anything(self):
        assert not _action_web._owns_socket(self.OTHER, None, "")
        assert not _action_web._owns_socket(self.OTHER, {100}, "com.example.app")


class _ProbeTransport:
    """Small package-aware provider double for the visibility-only API."""

    def __init__(self, *, sockets=(), targets=(), channels=None, reachable=True):
        self._sockets = sockets if isinstance(sockets, BaseException) else list(sockets)
        self._targets = list(targets)
        self._channels = channels or {}
        self._reachable = reachable
        self.memory = {}
        self.socket_reads = 0
        self.channel_reads = []
        self.dead = []
        self.unreachable = []

    def reachable(self):
        return self._reachable

    def remembered_target(self):
        return ""

    def remembered_target_for(self, package):
        return self.memory.get(package, "")

    def remember_target(self, target_id):
        pass

    def remember_target_for(self, package, target_id):
        if target_id:
            self.memory[package] = target_id
        else:
            self.memory.pop(package, None)

    def channel(self, target_id):
        self.channel_reads.append(target_id)
        value = self._channels[target_id]
        if isinstance(value, BaseException):
            raise value
        return value

    def sockets(self):
        self.socket_reads += 1
        if isinstance(self._sockets, BaseException):
            raise self._sockets
        return self._sockets

    def is_dead(self, socket):
        return False

    def forward(self, socket):
        return 9222

    def list_targets(self, endpoint):
        return self._targets

    def mark_dead(self, socket, cause):
        self.dead.append((socket, cause))

    def mark_unreachable(self, cause):
        self.unreachable.append(cause)


class TestProbeVisibleWebTarget:
    BROWSER = _web.Socket("chrome_devtools_remote", None, "browser")
    TARGET = {"webSocketDebuggerUrl": "ws://visible", "url": "https://one.test"}

    def test_a_visible_target_is_returned_and_remembered_for_its_package(self):
        transport = _ProbeTransport(
            sockets=[self.BROWSER], targets=[self.TARGET],
            channels={"ws://visible": _Channel(visible=True)})

        result = _action_web.probe_visible_web_target(
            "com.android.chrome", transport)

        assert result == _action_web.VisibleWebTarget(
            True, "ws://visible", "com.android.chrome",
            "discovered-target-visible")
        assert transport.memory == {"com.android.chrome": "ws://visible"}

    def test_a_remembered_target_is_reverified_without_rescanning(self):
        transport = _ProbeTransport(
            sockets=AssertionError("sockets were rescanned"),
            channels={"ws://remembered": _Channel(visible=True)})
        transport.memory["com.android.chrome"] = "ws://remembered"

        result = _action_web.probe_visible_web_target(
            "com.android.chrome", transport)

        assert result.present is True
        assert result.target_id == "ws://remembered"
        assert result.reason == "remembered-target-visible"
        assert transport.socket_reads == 0

    def test_remembered_targets_are_owned_by_package(self):
        transport = _ProbeTransport(
            sockets=[self.BROWSER], targets=[self.TARGET],
            channels={"ws://visible": _Channel(visible=True),
                      "ws://chrome": _Channel(visible=True)})
        transport.memory["com.android.chrome"] = "ws://chrome"

        result = _action_web.probe_visible_web_target(
            "com.chrome.beta", transport)

        assert result.target_id == "ws://visible"
        assert transport.channel_reads == ["ws://visible"]
        assert transport.memory == {
            "com.android.chrome": "ws://chrome",
            "com.chrome.beta": "ws://visible",
        }

    def test_a_hidden_target_is_not_present_and_no_negative_is_cached(self):
        transport = _ProbeTransport(
            sockets=[self.BROWSER], targets=[self.TARGET],
            channels={"ws://visible": _Channel(visible=False)})

        first = _action_web.probe_visible_web_target(
            "com.android.chrome", transport)
        second = _action_web.probe_visible_web_target(
            "com.android.chrome", transport)

        assert first.present is second.present is False
        assert first.reason == second.reason == "no-visible-target"
        assert transport.memory == {}
        assert transport.socket_reads == 2

    def test_no_browser_socket_is_an_uncached_capture_result(self):
        transport = _ProbeTransport(sockets=[])

        result = _action_web.probe_visible_web_target(
            "com.android.chrome", transport)

        assert result == _action_web.VisibleWebTarget(
            False, None, "com.android.chrome", "no-browser-socket")
        assert transport.memory == {}

    def test_a_target_that_raises_does_not_hide_a_later_visible_target(self):
        targets = [
            {"webSocketDebuggerUrl": "ws://dead"},
            {"webSocketDebuggerUrl": "ws://visible"},
        ]
        transport = _ProbeTransport(
            sockets=[self.BROWSER], targets=targets,
            channels={"ws://dead": RuntimeError("target closed"),
                      "ws://visible": _Channel(visible=True)})

        result = _action_web.probe_visible_web_target(
            "com.android.chrome", transport)

        assert result.present is True
        assert result.target_id == "ws://visible"
        assert transport.channel_reads == ["ws://dead", "ws://visible"]

    def test_socket_enumeration_failure_is_a_false_observation_not_a_cache(self):
        transport = _ProbeTransport(sockets=RuntimeError("adb offline"))

        result = _action_web.probe_visible_web_target(
            "com.android.chrome", transport)

        assert result.reason == "socket-enumeration-failed"
        assert result.present is False
        assert len(transport.unreachable) == 1
        assert transport.memory == {}

    def test_non_chrome_packages_do_not_touch_the_transport(self):
        transport = _ProbeTransport(
            sockets=AssertionError("transport should not be used"))

        result = _action_web.probe_visible_web_target(
            "com.example.app", transport)

        assert result.reason == "unsupported-package"
        assert result.present is False
        assert transport.socket_reads == 0


class TestChoosingTheSurface:
    """Which of the device's debug targets is the page on screen."""

    def setup_method(self):
        _web._forwards.clear()
        _web._dead.clear()
        _web._unreachable = False
        _web._no_socket_reported = False
        _web.remember_target("")

    def test_a_cloud_session_does_not_reach_for_adb(self, monkeypatch):
        """adb runs on the host running the test; a cloud device's host is
        somebody else's machine."""
        monkeypatch.setattr(_web._config, "run_target", "cloud")
        monkeypatch.setattr(_web, "sockets", lambda: pytest.fail("adb was called"))
        assert _action_web.open_web_surface(NATIVE) is None

    def test_the_page_sharing_most_with_the_device_wins(self, monkeypatch):
        """The fallback, for surfaces that cannot answer the visibility question
        at all. A page that answers `hidden` is a different thing entirely."""
        other = {**PAGE, "elements": [
            {"tag": "A", "label": "Pay now", "css": "#pay", "path": "",
             "x": 10, "y": 20, "w": 100, "h": 40}]}
        channels = {"ws://a": _Silent(other), "ws://b": _Silent()}
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": "ws://a", "url": "https://one.test/"},
            {"webSocketDebuggerUrl": "ws://b", "url": "https://two.test/"}])
        monkeypatch.setattr(_web, "pids_of", lambda package: None)
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: channels[url])

        surface = _action_web.open_web_surface(NATIVE)
        assert set(surface.twins) == {"Pay now", "Terms"}
        assert _web.remembered_target() == "ws://b"

    def test_the_last_winner_is_tried_before_rescanning_every_tab(self, monkeypatch):
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets", lambda: pytest.fail("rescanned"))
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: _Channel())
        _web.remember_target("ws://b")
        assert _action_web.open_web_surface(NATIVE) is not None

    def test_a_remembered_target_that_no_longer_calibrates_is_rescanned(self, monkeypatch):
        scanned = []
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: _Channel())
        monkeypatch.setattr(_web, "sockets", lambda: scanned.append(1) or [])
        _web.remember_target("ws://stale")
        assert _action_web.open_web_surface([_native("Other", (0, 0, 5, 5))]) is None
        assert scanned == [1]

    def test_an_unreachable_device_is_recorded_once_rather_than_retried(self, monkeypatch):
        calls = []

        def explode():
            calls.append(1)
            raise RuntimeError("adb: device offline")

        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets", explode)
        assert _action_web.open_web_surface(NATIVE) is None
        assert _action_web.open_web_surface(NATIVE) is None
        assert calls == [1]

    def test_a_target_that_does_not_answer_does_not_decide_for_the_others(
            self, monkeypatch):
        """A device carries sockets for other apps and for WebViews that have gone
        away; one of those hanging must not disable the web surface for the run."""
        def channel(url, **kwargs):
            return _Dead() if url == "ws://dead" else _Channel()

        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets", lambda: [
            _web.Socket("webview_devtools_remote_16685", 16685, "webview"),
            _web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": "ws://dead", "url": "https://stale.test/"}]
            if port == 9222 and not _web.is_dead(
                _web.Socket("webview_devtools_remote_16685", 16685, "webview"))
            else [{"webSocketDebuggerUrl": "ws://live", "url": "https://live.test/"}])
        monkeypatch.setattr(_web, "Channel", channel)

        assert _action_web.open_web_surface(NATIVE) is not None
        assert _web.reachable() is True

    def test_a_socket_that_never_answers_is_written_off_for_the_session(
            self, monkeypatch):
        """It costs the first action two probes — one asking for the visible page,
        one comparing content — and every action after that nothing."""
        attempts = []

        def channel(url, **kwargs):
            attempts.append(url)
            return _Dead()

        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("webview_devtools_remote_1", 1, "webview")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": "ws://dead", "url": "https://stale.test/"}])
        monkeypatch.setattr(_web, "Channel", channel)

        assert _action_web.open_web_surface(NATIVE) is None
        first = len(attempts)
        assert _action_web.open_web_surface(NATIVE) is None
        assert len(attempts) == first

    def test_a_decisive_share_stops_the_scan(self, monkeypatch):
        """Chrome freezes background tabs, so every target left unread is a
        connection timeout saved."""
        read = []

        def channel(url, **kwargs):
            read.append(url)
            return _Channel()

        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": f"ws://{n}", "url": f"https://{n}.test/"}
            for n in range(6)])
        monkeypatch.setattr(_web, "Channel", channel)

        native = [_native(f"Shared {n}", (30, 310 + n * 60, 330, 360 + n * 60))
                  for n in range(4)]
        page = {**PAGE, "elements": [
            {"tag": "A", "label": f"Shared {n}", "css": f"#s{n}", "path": "",
             "x": 10, "y": 20 + n * 20, "w": 100, "h": 16} for n in range(4)]}
        monkeypatch.setattr(_web, "Channel",
                            lambda url, **kw: read.append(url) or _Channel(page))

        assert _action_web.open_web_surface(native) is not None
        assert read == ["ws://0"]

    def test_the_page_that_says_it_is_visible_wins(self, monkeypatch):
        """Five tabs of the same site all calibrate identically; only one of them
        is on screen, and comparing content against the device cannot say which."""
        same = {**PAGE}
        channels = {"ws://bg1": _Channel(same, visible=False),
                    "ws://bg2": _Channel(same, visible=False),
                    "ws://fg": _Channel(same, visible=True)}
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "pids_of", lambda package: None)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": url, "url": f"https://same.test/{url[-3:]}"}
            for url in ("ws://bg1", "ws://bg2", "ws://fg")])
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: channels[url])

        assert _action_web.open_web_surface(NATIVE) is not None
        assert _web.remembered_target() == "ws://fg"

    def test_a_page_that_claims_nothing_still_calibrates_its_way_in(self, monkeypatch):
        """Not every surface implements page visibility; the content comparison is
        the fallback, not the other way round."""
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "pids_of", lambda package: None)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": "ws://only", "url": "https://only.test/"}])
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: _Silent())

        assert _action_web.open_web_surface(NATIVE) is not None

    def test_a_remembered_target_that_went_to_the_background_is_dropped(self, monkeypatch):
        """The app switched away; the tab still calibrates, and is still wrong."""
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets", lambda: [])
        monkeypatch.setattr(_web, "pids_of", lambda package: None)
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: _Channel(visible=False))
        _web.remember_target("ws://was-visible")
        assert _action_web.open_web_surface(NATIVE) is None

    def test_the_visible_page_failing_to_place_does_not_send_us_round_the_device(
            self, monkeypatch):
        """A WebView that projects too little into the accessibility tree cannot
        be placed (§5.2). It is still the page on screen, so no other target is
        worth a connection timeout."""
        read = []

        def channel(url, **kwargs):
            read.append(url)
            return _Channel(visible=(url == "ws://fg"))

        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "pids_of", lambda package: None)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": url, "url": f"https://{url[-2:]}.test/"}
            for url in ("ws://fg", "ws://bg1", "ws://bg2")])
        monkeypatch.setattr(_web, "Channel", channel)

        # Nothing the page shows appears in this device tree, so it cannot be placed.
        assert _action_web.open_web_surface([_native("Elsewhere", (0, 0, 5, 5))]) is None
        assert read == ["ws://fg"]

    def test_a_page_that_said_it_is_hidden_never_wins_on_content(self, monkeypatch):
        """The content pass exists for surfaces that CANNOT answer. A background
        tab that answered plainly must not be re-admitted by it — its DOM
        coordinates would be applied to the foreground screen."""
        channels = {"ws://fg": _Silent(),          # cannot answer, shares nothing
                    "ws://bg": _Channel(visible=False)}   # answers: not on screen
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "pids_of", lambda package: None)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": "ws://fg", "url": "https://fg.test/"},
            {"webSocketDebuggerUrl": "ws://bg", "url": "https://bg.test/"}])
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: channels[url])

        # ws://fg cannot be placed against this tree and ws://bg could be — but
        # ws://bg has said it is not the page on screen.
        assert _action_web.open_web_surface([_native("Nothing", (0, 0, 5, 5))]) is None

    def test_a_target_that_answers_and_then_fails_does_not_kill_its_socket(
            self, monkeypatch):
        """A page navigating mid-read is transient. Writing the browser's socket
        off for the session would take the web surface away for the whole run."""
        class _FailsAfterAnswering(_Channel):
            def read_page(self):
                raise RuntimeError("Inspected target navigated or closed")

        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "pids_of", lambda package: None)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": "ws://fg", "url": "https://fg.test/"}])
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: _FailsAfterAnswering())

        assert _action_web.open_web_surface(NATIVE) is None
        assert not _web.is_dead(_web.Socket("chrome_devtools_remote", None, "browser"))

    def test_a_socket_belonging_to_any_of_the_apps_processes_is_kept(self, monkeypatch):
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("webview_devtools_remote_200", 200,
                                                 "webview")])
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "pids_of", lambda package: {100, 200})
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": "ws://wv", "url": "https://app.test/"}])
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: _Channel())

        assert _action_web.open_web_surface(NATIVE, "com.example.app") is not None

    def test_the_browser_socket_is_not_probed_for_a_non_browser_foreground_app(
            self, monkeypatch):
        """A native app cannot own `chrome_devtools_remote`; probing it anyway
        produced a stray timeout and a misleading "did not answer" log for every
        session whose app simply has webview debugging turned off."""
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "pids_of", lambda package: {100})
        monkeypatch.setattr(_web, "forward",
                            lambda socket: pytest.fail("browser socket was probed"))
        monkeypatch.setattr(_web, "list_targets",
                            lambda port: pytest.fail("browser socket was probed"))

        assert _action_web.open_web_surface(NATIVE, "com.example.app") is None

    def test_the_browser_socket_is_still_probed_when_the_browser_itself_is_foreground(
            self, monkeypatch):
        """The one case a bare pid check cannot tell apart from a native app:
        Chrome driven directly still needs its own devtools socket scanned."""
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "pids_of", lambda package: {100, 200})
        monkeypatch.setattr(_web, "forward", lambda socket: 9222)
        monkeypatch.setattr(_web, "list_targets", lambda port: [
            {"webSocketDebuggerUrl": "ws://x", "url": "https://example.test/"}])
        monkeypatch.setattr(_web, "Channel", lambda url, **kw: _Channel())

        assert _action_web.open_web_surface(NATIVE, "com.android.chrome") is not None

    def test_the_channel_scan_skips_the_browser_socket_for_a_native_app_too(
            self, monkeypatch, caplog):
        """`visible_channel` is the re-locate path healing and scroll_until read
        the page through, and it decides socket ownership for itself."""
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "pids_of", lambda package: {100})
        monkeypatch.setattr(_web, "forward",
                            lambda socket: pytest.fail("browser socket was probed"))
        monkeypatch.setattr(_web, "list_targets",
                            lambda port: pytest.fail("browser socket was probed"))

        with caplog.at_level("INFO", logger="testmu_appium"):
            assert _action_web.visible_channel("com.example.app") is None

        assert "com.example.app publishes no devtools socket" in caplog.text

    def test_a_foreground_app_with_no_devtools_socket_is_reported_once(
            self, monkeypatch, caplog):
        """The true cause was a build with webview debugging disabled, not a
        transport fault — the diagnostic must name that, and only once."""
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "pids_of", lambda package: {100})

        with caplog.at_level("INFO", logger="testmu_appium"):
            assert _action_web.open_web_surface(NATIVE, "com.example.app") is None
            assert _action_web.open_web_surface(NATIVE, "com.example.app") is None

        assert caplog.text.count(
            "com.example.app publishes no devtools socket") == 1

    def test_reset_rearms_the_no_socket_diagnostic(self, monkeypatch, caplog):
        monkeypatch.setattr(_web._config, "run_target", "local")
        monkeypatch.setattr(_web, "sockets",
                            lambda: [_web.Socket("chrome_devtools_remote", None, "browser")])
        monkeypatch.setattr(_web, "pids_of", lambda package: {100})

        with caplog.at_level("INFO", logger="testmu_appium"):
            assert _action_web.open_web_surface(NATIVE, "com.example.app") is None
            _web.reset()
            assert _action_web.open_web_surface(NATIVE, "com.example.app") is None

        assert caplog.text.count(
            "com.example.app publishes no devtools socket") == 2


class TestPartiallyVisibleElements:
    """An element half off an edge is still actable — at the middle of the part
    that is on screen. Its full-rectangle centre can be off the screen entirely."""

    PAGE = {"dpr": 3, "scale": 1.0, "offsetLeft": 0, "offsetTop": 0,
            "viewportWidth": 360, "viewportHeight": 800,
            "visualWidth": 360, "visualHeight": 800, "blockedUrls": []}

    def test_an_element_off_the_left_edge_is_tapped_where_it_can_be_seen(self):
        element = {"x": -90, "y": 100, "w": 100, "h": 40}
        assert _action_web.device_point(element, self.PAGE, origin=(0, 0)) == (15, 360)

    def test_a_fully_visible_element_is_still_tapped_at_its_centre(self):
        element = {"x": 10, "y": 100, "w": 100, "h": 40}
        assert _action_web.device_point(element, self.PAGE, origin=(0, 0)) == (180, 360)

    def test_a_zoomed_page_filters_against_what_is_on_the_screen(self):
        """The visual viewport is a window onto the layout viewport; an element
        inside the page but outside that window is not on the screen."""
        panned = {**self.PAGE, "scale": 2.0, "offsetLeft": 180, "offsetTop": 0,
                  "visualWidth": 180, "visualHeight": 400}
        elements = [{"tag": "A", "x": 0, "y": 10, "w": 60, "h": 20},      # panned past
                    {"tag": "A", "x": 200, "y": 10, "w": 60, "h": 20}]    # on screen
        kept = _web.usable(elements, panned)
        assert [e["x"] for e in kept] == [200]


class TestNestedFrameRecovery:
    """A cross-origin frame can itself contain one. Reading only the top
    document's blocked list loses everything below the first boundary."""

    class _Nested:
        def __init__(self):
            self.read = []

        def read_page(self):
            return {"dpr": 3, "scale": 1.0, "viewportWidth": 360, "viewportHeight": 800,
                    "blockedUrls": ["https://outer.test/"], "elements": []}

        def unreachable_frames(self, page, seen=()):
            return [(url.strip("/").split("/")[-1], url)
                    for url in page.get("blockedUrls", []) if url not in set(seen)]

        def read_frame(self, frame_id, path=""):
            self.read.append(frame_id)
            if frame_id == "outer.test":
                return {"blockedUrls": ["https://inner.test/"], "elements": [
                    {"tag": "A", "label": "Outer", "css": "#outer", "path": path,
                     "x": 10, "y": 10, "w": 50, "h": 20}]}
            return {"blockedUrls": [], "elements": [
                {"tag": "INPUT", "label": "Inner", "css": "#inner", "path": path,
                 "x": 20, "y": 20, "w": 50, "h": 20}]}

    def test_a_frame_inside_a_recovered_frame_is_recovered_too(self):
        channel = self._Nested()
        elements, _, _ = _action_web.read_all(channel)
        assert [e["css"] for e in elements] == ["#outer", "#inner"]
        assert channel.read == ["outer.test", "inner.test"]

    def test_each_recovered_frame_labels_its_own_elements(self):
        elements, _, _ = _action_web.read_all(self._Nested())
        assert [e["path"] for e in elements] == [">x0", ">x0>x0"]


class TestPageInMotion:
    """A page that scrolls between the native read and the DOM read shifts EVERY
    calibration sample by the same amount, so they still agree — on an origin
    wrong by however far it moved. The agreement check cannot see it."""

    class _Scrolling(_Channel):
        def __init__(self, walked_at, now):
            super().__init__({**PAGE, "scrollX": 0, "scrollY": walked_at})
            self._now = now

        def scroll_position(self):
            return (0, self._now)

    def test_a_page_that_moved_while_it_was_read_is_not_placed(self):
        assert _action_web.open_surface(self._Scrolling(0, 40), NATIVE) is None

    def test_a_still_page_is_placed_as_before(self):
        assert _action_web.open_surface(self._Scrolling(120, 120), NATIVE) is not None

    def test_sub_pixel_drift_is_not_motion(self):
        """Rounding is not scrolling."""
        assert _action_web.open_surface(self._Scrolling(120, 120.5), NATIVE) is not None

    def test_a_surface_that_cannot_report_its_scroll_is_not_assumed_to_be_moving(self):
        class _Silent(_Channel):
            def scroll_position(self):
                raise RuntimeError("no scroll position")

        assert _action_web.open_surface(_Silent(), NATIVE) is not None


class TestScrollIntoView:
    """A web element is scrolled by the page, not by a gesture.

    The DOM places its own elements, so one evaluate moves the target and reports
    whether it landed in the viewport. No origin is solved: scrolling needs the
    page, not the page's position on the device.
    """

    class _Scroller:
        def __init__(self, verdict="visible"):
            self.verdict = verdict
            self.evaluated = []

        def evaluate(self, expression, context_id=None):
            self.evaluated.append(expression)
            return self.verdict

        def evaluate_in_frame(self, frame_id, expression):
            self.evaluated.append((frame_id, expression))
            return self.verdict

        def scroll_frame_into_view(self, frame_id):
            self.evaluated.append(("owner", frame_id))
            return True

    def test_the_recorded_css_strategy_is_the_one_used(self):
        assert _action_web.css_of([
            {"strategy": "text", "selector": "Search"},
            {"strategy": "css", "selector": "#searchIcon"},
        ]) == "#searchIcon"

    def test_a_target_with_no_css_strategy_is_not_a_web_target(self):
        assert _action_web.css_of(
            [{"strategy": "accessibility_id", "selector": "Search"}]) is None
        assert _action_web.css_of([]) is None
        assert _action_web.css_of(None) is None

    def test_the_selector_reaches_the_page_as_a_string_literal(self):
        """A selector carrying a quote must not end the JS string it sits in."""
        channel = self._Scroller()
        _action_web.scroll_into_view(channel, "a[href='/wiki/Appium']")
        sent = channel.evaluated[0]
        assert '"a[href=\'/wiki/Appium\']"' in sent
        assert "scrollIntoView" in sent

    @pytest.mark.parametrize("verdict", ["visible", "moved", "missing"])
    def test_the_page_verdict_is_returned_unchanged(self, verdict):
        """`moved` is a real outcome: a sticky header can hold an element partly
        out of view after a correct scroll, and that is not a failure to find it."""
        assert _action_web.scroll_into_view(self._Scroller(verdict), "#a") == verdict

    def test_a_healed_shadow_descriptor_is_scrolled_by_structural_identity(self):
        channel = self._Scroller()
        descriptor = {
            "dom_path": [
                {"kind": "shadow", "nodes": [0, 1]},
                {"kind": "element", "nodes": [0, 2]},
            ],
        }
        assert _action_web.scroll_descriptor(channel, descriptor) == "visible"
        sent = channel.evaluated[0]
        assert "shadowRoot" in sent
        assert '"kind": "shadow"' in sent

    def test_a_cross_origin_descriptor_uses_a_fresh_frame_context(self):
        channel = self._Scroller()
        descriptor = {
            "frame_id": "FRAME-7",
            "dom_path": [{"kind": "element", "nodes": [0, 3]}],
        }
        assert _action_web.scroll_descriptor(channel, descriptor) == "visible"
        assert channel.evaluated[0] == ("owner", "FRAME-7")
        frame_id, sent = channel.evaluated[1]
        assert frame_id == "FRAME-7"
        assert "scrollIntoView" in sent
