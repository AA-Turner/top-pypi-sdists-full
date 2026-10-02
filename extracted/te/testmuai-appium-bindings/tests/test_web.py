"""The web surface: socket discovery and the CSS-to-device conversion.

Both are pure given their inputs, and both are where the investigation lost the
most time — socket names vary by more than the two obvious forms, and three
end-to-end taps missed while the content origin was assumed rather than derived.
"""
import json

import pytest

from testmu_appium import _config
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers import _web

# /proc/net/unix as the device actually prints it, including the Stetho socket a
# fixed two-name lookup would have missed.
PROC_NET_UNIX = """\
Num       RefCount Protocol Flags    Type St Inode Path
0000000000000000: 00000002 00000000 00010000 0001 01 123456 @chrome_devtools_remote
0000000000000000: 00000002 00000000 00010000 0001 01 123457 @webview_devtools_remote_16685
0000000000000000: 00000002 00000000 00010000 0001 01 123458 @stetho_com.google.android.apps.messaging_devtools_remote
0000000000000000: 00000002 00000000 00010000 0001 01 123459 /dev/socket/logdw
0000000000000000: 00000003 00000000 00000000 0001 03 123460 @android:something_else
"""


class TestSocketDiscovery:
    def test_it_finds_every_devtools_socket_not_just_the_two_obvious_ones(self):
        names = {s.name for s in _web.discover_sockets(PROC_NET_UNIX)}
        assert names == {
            "chrome_devtools_remote",
            "webview_devtools_remote_16685",
            "stetho_com.google.android.apps.messaging_devtools_remote",
        }

    def test_non_devtools_sockets_are_ignored(self):
        names = {s.name for s in _web.discover_sockets(PROC_NET_UNIX)}
        assert not any("logdw" in n or "something_else" in n for n in names)

    def test_a_webview_socket_carries_the_pid_that_owns_it(self):
        socket = next(s for s in _web.discover_sockets(PROC_NET_UNIX)
                      if s.name.startswith("webview_"))
        assert socket.pid == 16685
        assert socket.kind == "webview"

    def test_the_browser_socket_has_no_pid(self):
        socket = next(s for s in _web.discover_sockets(PROC_NET_UNIX)
                      if s.name == "chrome_devtools_remote")
        assert socket.pid is None
        assert socket.kind == "browser"

    def test_an_unrecognised_devtools_socket_is_kept_but_marked(self):
        """Stetho is a different debug bridge. Keeping it visible beats a silent
        drop; the caller decides whether it can speak the protocol."""
        socket = next(s for s in _web.discover_sockets(PROC_NET_UNIX)
                      if s.name.startswith("stetho_"))
        assert socket.kind == "other"
        assert socket.pid is None

    def test_a_socket_is_matched_to_its_app_by_pid(self):
        sockets = _web.discover_sockets(PROC_NET_UNIX)
        assert _web.socket_for_pid(sockets, 16685).name == "webview_devtools_remote_16685"
        assert _web.socket_for_pid(sockets, 99999) is None

    def test_empty_input_yields_nothing_rather_than_raising(self):
        assert _web.discover_sockets("") == []


class TestOriginCalibration:
    """The content origin is derived from an element visible on both surfaces.

    Assuming it from the WebView node's bounds produced three missed taps; the
    derived value landed. Numbers below are the measured ones.
    """

    def test_the_origin_is_solved_from_a_marker_seen_on_both_surfaces(self):
        # marker at CSS (0,0); the OS reported it at [0,252,600,372]
        origin = _web.derive_origin(css=(0, 0), native_bounds=(0, 252, 600, 372),
                                    dpr=3, scale=1.0)
        assert origin == (0, 252)

    def test_a_marker_away_from_the_css_origin_still_solves(self):
        origin = _web.derive_origin(css=(10, 20), native_bounds=(30, 312, 630, 432),
                                    dpr=3, scale=1.0)
        assert origin == (0, 252)

    def test_zoom_is_carried_into_the_solution(self):
        # factor = 3 * 0.4787 = 1.4361, so a marker at CSS (100,100) under an
        # origin of (0,84) is reported by the OS at (144, 228).
        origin = _web.derive_origin(css=(100, 100), native_bounds=(144, 228, 200, 300),
                                    dpr=3, scale=0.4787)
        assert origin == (0, 84)

    def test_a_degenerate_viewport_refuses_rather_than_solving(self):
        with pytest.raises(ValueError):
            _web.derive_origin(css=(0, 0), native_bounds=(0, 0, 10, 10),
                               dpr=3, scale=0)


class TestCssToDevice:
    def test_the_conversion_matches_what_the_os_reported(self):
        """Measured: CSS centre (494.74, 61.33), dpr 3, scale 0.4787, origin (0,84)
        -> the OS put that element's centre at (710, 171)."""
        point = _web.to_device(494.74, 61.33, origin=(0, 84), dpr=3, scale=0.4787)
        assert abs(point[0] - 710) <= 1
        assert abs(point[1] - 171) <= 1

    def test_scale_is_not_optional(self):
        """Dropping it is worth ~700px on a zoomed page — the v1 bug."""
        unscaled = _web.to_device(494.74, 61.33, origin=(0, 84), dpr=3, scale=1.0)
        scaled = _web.to_device(494.74, 61.33, origin=(0, 84), dpr=3, scale=0.4787)
        assert unscaled[0] - scaled[0] > 700

    def test_panning_offsets_are_subtracted_before_scaling(self):
        point = _web.to_device(200, 300, origin=(0, 0), dpr=2, scale=1.0,
                               offset_left=50, offset_top=100)
        assert point == (300, 400)

    @pytest.mark.parametrize("dpr,scale", [(0, 1.0), (3, 0)])
    def test_a_degenerate_viewport_refuses_rather_than_returning_a_point(self, dpr, scale):
        with pytest.raises(ValueError):
            _web.to_device(10, 10, origin=(0, 0), dpr=dpr, scale=scale)


class TestTheUnitTheOsReportsIn:
    """What one CSS pixel is worth, per platform.

    Android's accessibility tree is in device PIXELS, so a CSS pixel is `dpr` of
    them. iOS's is in POINTS, and a CSS pixel IS a point — `dpr` there describes
    the backing store, which no coordinate on either side is expressed in.

    Getting this wrong does not shift the page by a constant, which is what makes
    it dangerous: every element solves a DIFFERENT origin, calibration finds no
    majority, and the surface is dropped as unplaceable. The web reader then
    looks absent rather than wrong, on every screen, silently.
    """

    #: (css_point, native_top_left) pairs read off a Google page on a real iPhone
    #: at dpr 2 — "Main menu", "ALL", "Notifications", "Google apps", the Google
    #: wordmark, "Search with AI". The page's true origin is (5, 141), which is
    #: also the WebView node's own box: independent corroboration.
    IOS_SAMPLES = [
        ((0, 0), (5, 141)), ((72, 0), (85, 157)), ((203, 0), (208, 141)),
        ((255, 4), (260, 145)), ((122, 108), (127, 249)), ((237, 185), (242, 326)),
    ]

    def _origins(self, monkeypatch, platform):
        monkeypatch.setitem(_config._config, "platform", platform)
        return [_web.derive_origin(css=css, native_bounds=(b[0], b[1], 0, 0),
                                   dpr=2, scale=1.0)
                for css, b in self.IOS_SAMPLES]

    def test_ios_solves_one_origin_from_every_sample(self, monkeypatch):
        origins = self._origins(monkeypatch, "ios")
        xs = {o[0] for o in origins}
        assert max(xs) - min(xs) <= 8, f"samples disagree: {origins}"

    def test_android_would_not_agree_on_the_same_numbers(self, monkeypatch):
        """The same page read as device pixels scatters — this is the measured
        failure the iOS row exists to prevent, kept as the contrast."""
        origins = self._origins(monkeypatch, "android")
        xs = {o[0] for o in origins}
        assert max(xs) - min(xs) > 8

    def test_ios_ignores_dpr_and_android_does_not(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "ios")
        assert _web.to_device(100, 100, origin=(0, 0), dpr=2, scale=1.0) == (100, 100)
        monkeypatch.setitem(_config._config, "platform", "android")
        assert _web.to_device(100, 100, origin=(0, 0), dpr=2, scale=1.0) == (200, 200)

    def test_zoom_still_counts_on_ios(self, monkeypatch):
        """Only `dpr` is dropped. A pinch-zoomed page still scales."""
        monkeypatch.setitem(_config._config, "platform", "ios")
        assert _web.to_device(100, 100, origin=(0, 0), dpr=2, scale=2.0) == (200, 200)

    def test_a_platform_with_no_row_refuses_rather_than_guessing(self, monkeypatch):
        monkeypatch.setitem(_config._config, "platform", "tizen")
        with pytest.raises(UnsupportedOnPlatform):
            _web.to_device(10, 10, origin=(0, 0), dpr=2, scale=1.0)


class TestConversionSelfCheck:
    """A converted rect is checked against the native bounds it came from.
    Disagreement means the conversion is wrong, and a wrong tap is worse than none.
    """

    def test_agreement_within_tolerance_passes(self):
        assert _web.agrees((710, 171), (700, 160, 720, 182), tolerance=8)

    def test_a_point_far_from_the_native_box_is_rejected(self):
        assert not _web.agrees((1484, 268), (700, 160, 720, 182), tolerance=8)

    def test_the_tolerance_is_applied_around_the_box_not_its_centre(self):
        assert _web.agrees((695, 165), (700, 160, 720, 182), tolerance=8)
        assert not _web.agrees((680, 165), (700, 160, 720, 182), tolerance=8)


class TestPiercingWalk:
    """The walk script is a contract with the page: what it must reach, and what
    it must not return. Its behaviour was measured across seven DOM-complexity
    modes; these pin the clauses that made those results possible."""

    def test_it_descends_open_shadow_roots(self):
        assert "shadowRoot" in _web.WALK_JS

    def test_it_descends_same_origin_frames(self):
        assert "contentDocument" in _web.WALK_JS

    def test_a_blocked_frame_is_counted_rather_than_swallowed(self):
        """A cross-origin frame throws on contentDocument. Silently skipping it
        would report a partial page as a whole one."""
        assert "blocked" in _web.WALK_JS

    def test_it_is_depth_bounded(self):
        assert str(_web.MAX_WALK_DEPTH) in _web.WALK_JS

    def test_it_reports_geometry_for_conversion(self):
        for field in ("getBoundingClientRect", "devicePixelRatio", "visualViewport"):
            assert field in _web.WALK_JS

    def test_it_records_which_attribute_a_label_came_from(self):
        """The clause travels with the value; matching a content-desc label with
        .text() resolves nothing, which is how the native child_text failed."""
        assert "aria-label" in _web.WALK_JS

    def test_informational_rows_use_only_their_own_text(self):
        assert "ownText(el)" in _web.WALK_JS
        assert "interactive ? el.innerText : ownText(el)" in _web.WALK_JS

    def test_simple_controls_suppress_duplicate_descendant_text(self):
        assert (
            "isInteractive(parent) && !isCompoundInteractive(parent)"
            in _web.WALK_JS
        )

    def test_compound_controls_keep_individual_descendant_fields(self):
        assert "const isCompoundInteractive = (el)" in _web.WALK_JS
        assert "split(/\\n+/)" in _web.WALK_JS
        assert "new Set(lines).size > 1" in _web.WALK_JS

    def test_hidden_content_is_rejected_without_using_the_viewport(self):
        for clause in (
                "checkVisibility({checkOpacity: true, checkVisibilityCSS: true})",
                "ariaHiddenOrInert", "insideActiveModal", "clippedOut"):
            assert clause in _web.WALK_JS

    def test_hidden_cross_origin_frames_are_not_recovered(self):
        assert "else if (visible)" in _web.WALK_JS


class TestElementFiltering:
    ELEMENTS = [
        {"tag": "A", "label": "Docs", "css": "#docs", "w": 100, "h": 20,
         "x": 10, "y": 10, "interactive": True},
        {"tag": "IFRAME", "label": "", "css": "#ads", "w": 300, "h": 250,
         "x": -29325, "y": -29255, "interactive": True},
        {"tag": "DIV", "label": "hidden", "css": "#h", "w": 0, "h": 0,
         "x": 0, "y": 0, "interactive": True},
        {"tag": "SCRIPT", "label": "// queue window.location.href",
         "css": "script", "w": 50, "h": 10, "x": 5, "y": 5, "interactive": False},
    ]

    def test_offscreen_elements_are_dropped(self):
        """Measured: a hidden ad iframe sat at (-29325, -29255) and was merged as
        though tappable."""
        kept = _web.usable(self.ELEMENTS, viewport=(1080, 2400))
        assert not any(e["css"] == "#ads" for e in kept)

    def test_offscreen_elements_are_read_when_no_viewport_is_requested(self):
        kept = _web.usable(self.ELEMENTS)
        assert [e["css"] for e in kept] == ["#docs", "#ads"]

    def test_the_walks_hidden_verdict_is_honoured(self):
        kept = _web.usable([
            {**self.ELEMENTS[0], "visible": True},
            {**self.ELEMENTS[0], "css": "#hidden", "visible": False},
        ])
        assert [e["css"] for e in kept] == ["#docs"]

    def test_zero_sized_elements_are_dropped(self):
        kept = _web.usable(self.ELEMENTS, viewport=(1080, 2400))
        assert not any(e["css"] == "#h" for e in kept)

    def test_script_and_style_text_is_not_an_element(self):
        """CDP's innerText picks up script bodies; the a11y projection does not."""
        kept = _web.usable(self.ELEMENTS, viewport=(1080, 2400))
        assert not any(e["tag"] == "SCRIPT" for e in kept)

    def test_a_real_link_survives(self):
        kept = _web.usable(self.ELEMENTS, viewport=(1080, 2400))
        assert [e["css"] for e in kept] == ["#docs"]


class _FakeConnection:
    def __init__(self, replies, sent):
        self._replies, self._sent = replies, sent
    def send(self, payload):
        self._sent.append(json.loads(payload))
    def recv(self):
        message = self._sent[-1]
        result = self._replies.get(message["method"], {})
        if isinstance(result, Exception):
            return json.dumps({"id": message["id"], "error": {"message": str(result)}})
        return json.dumps({"id": message["id"], "result": result})
    def close(self):
        pass


class _FakeWebsocket:
    def __init__(self, replies):
        self.replies, self.sent, self.kwargs = replies, [], []
    def create_connection(self, url, **kw):
        self.kwargs.append(kw)
        return _FakeConnection(self.replies, self.sent)


class TestChannel:
    def test_the_origin_header_is_suppressed(self):
        """Chrome 150 answers 403 to a devtools WebSocket carrying a browser
        Origin, so it must be absent rather than plausible."""
        ws = _FakeWebsocket({"Runtime.evaluate": {"result": {"value": "1"}}})
        _web.Channel("ws://x", websocket_module=ws).evaluate("1")
        assert ws.kwargs[0]["suppress_origin"] is True

    def test_local_debug_transport_publishes_the_cloud_ready_contract(self):
        capabilities = _web.debug_transport().capabilities()
        assert capabilities == {
            "contract_version": 1,
            "provider": "local-adb",
            "cdp_rpc": True,
            "session_bound": False,
        }

    def test_a_protocol_error_raises_rather_than_reading_as_empty(self):
        ws = _FakeWebsocket({"Runtime.evaluate": RuntimeError("boom")})
        with pytest.raises(RuntimeError):
            _web.Channel("ws://x", websocket_module=ws).evaluate("1")

    def test_page_function_uses_one_connection_and_structured_arguments(self):
        ws = _FakeWebsocket({
            "Runtime.evaluate": {"result": {"objectId": "window-1"}},
            "Runtime.callFunctionOn": {"result": {"value": None}},
        })
        value = {"hostile": "'; globalThis.pwned = true; //"}

        _web.Channel("ws://x", websocket_module=ws).call_function(
            "function(value) { this.localStorage.setItem('k', value.hostile); }",
            (value,),
        )

        assert len(ws.kwargs) == 1
        assert ws.sent == [
            {
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "globalThis",
                    "returnByValue": False,
                },
            },
            {
                "id": 2,
                "method": "Runtime.callFunctionOn",
                "params": {
                    "functionDeclaration": (
                        "function(value) { "
                        "this.localStorage.setItem('k', value.hostile); }"
                    ),
                    "objectId": "window-1",
                    "arguments": [{"value": value}],
                    "returnByValue": True,
                    "awaitPromise": True,
                },
            },
        ]

    def test_read_page_returns_an_empty_page_rather_than_raising(self):
        ws = _FakeWebsocket({"Runtime.evaluate": {"result": {"value": None}}})
        page = _web.Channel("ws://x", websocket_module=ws).read_page()
        assert page["elements"] == []

    def test_a_thrown_page_script_is_reported_rather_than_read_as_empty(self, caplog):
        """A crashed walk and an empty page return the same None. Only the log
        separates them, and without it the whole surface disappears silently."""
        ws = _FakeWebsocket({"Runtime.evaluate": {
            "result": {"type": "undefined"},
            "exceptionDetails": {"exception": {
                "description": "TypeError: x.trim is not a function\n  at walk"}},
        }})

        with caplog.at_level("WARNING", logger="testmu_appium"):
            page = _web.Channel("ws://x", websocket_module=ws).read_page()

        assert page["elements"] == []
        assert "TypeError: x.trim is not a function" in caplog.text
        assert "at walk" not in caplog.text, "one line, not the whole stack"

    def test_a_label_survives_an_element_whose_value_is_a_number(self):
        """`progress`, `meter` and a numbered list item report a NUMBER from
        `.value`. The walk runs in the page, so this asserts the source coerces;
        the behaviour itself is verified on a device."""
        label_expression = _web.WALK_JS.split("const label =", 1)[1].split(";", 1)[0]

        assert label_expression.strip().startswith("String(")
        assert ".trim()" in label_expression

    def test_an_editable_field_is_named_without_sending_its_typed_value(self):
        label_expression = _web.WALK_JS.split(
            "const label =", 1
        )[1].split(";", 1)[0]
        assert "getAttribute('placeholder')" in label_expression
        assert "fieldLabel" in label_expression
        assert "isEditable(el) ? '' : el.value" in label_expression

    def test_only_writable_text_inputs_are_type_candidates(self):
        """Readonly fields and native controls such as checkbox/file inputs cannot
        accept the coordinate type runner's IME text."""
        assert "editableInputTypes.has" in _web.WALK_JS
        assert "el.readOnly === true" in _web.WALK_JS
        assert "getAttribute('aria-readonly') === 'true'" in _web.WALK_JS
        assert "'checkbox'" not in _web.WALK_JS.split(
            "const editableInputTypes", 1
        )[1].split("]);", 1)[0]
        assert "input_type:" in _web.WALK_JS

    TREE = {"frameTree": {
        "frame": {"id": "ROOT", "url": "https://example.com/"},
        "childFrames": [
            {"frame": {"id": "F1", "url": "https://www.wikipedia.org/"}},
            {"frame": {"id": "F2", "url": "https://example.com/inner"},
             "childFrames": [{"frame": {"id": "F3", "url": "https://other.test/"}}]},
        ]}}

    def test_only_the_frames_the_walk_could_not_enter_are_listed(self):
        """The frame tree lists every frame, including the ones the walk already
        descended. Reading one of those again puts each of its elements in the
        pool twice, which the cardinality-1 rule then reads as ambiguity."""
        ws = _FakeWebsocket({"Page.getFrameTree": self.TREE})
        frames = _web.Channel("ws://x", websocket_module=ws).unreachable_frames(
            {"blockedUrls": ["https://www.wikipedia.org/", "https://other.test/"]})
        assert [f[0] for f in frames] == ["F1", "F3"]

    def test_a_walk_that_entered_everything_asks_for_no_frame_tree(self):
        ws = _FakeWebsocket({"Page.getFrameTree": self.TREE})
        assert _web.Channel("ws://x", websocket_module=ws).unreachable_frames(
            {"blockedUrls": []}) == []
        assert ws.sent == []

    def test_a_frame_is_read_through_its_own_execution_context(self):
        """This is what recovers a cross-origin frame: 379 elements were read
        this way where the JS walk saw none."""
        ws = _FakeWebsocket({
            "Page.createIsolatedWorld": {"executionContextId": 42},
            "Runtime.evaluate": {"result": {"value":
                                            '{"elements":[{"tag":"A","x":1,"y":2}]}'}},
            "DOM.getFrameOwner": {"backendNodeId": 7},
            "DOM.getBoxModel": {"model": {"content": [0, 0, 0, 0, 0, 0, 0, 0]}},
        })
        page = _web.Channel("ws://x", websocket_module=ws).read_frame("F1")
        assert page["elements"] == [
            {"tag": "A", "x": 1, "y": 2, "path": "", "frame_id": "F1"}
        ]
        assert ws.sent[1]["params"]["contextId"] == 42

    def test_a_cross_origin_frame_owner_can_be_scrolled_before_its_contents(self):
        ws = _FakeWebsocket({
            "DOM.getFrameOwner": {"backendNodeId": 7},
            "DOM.scrollIntoViewIfNeeded": {},
        })
        channel = _web.Channel("ws://x", websocket_module=ws)
        assert channel.scroll_frame_into_view("F1") is True
        assert [message["method"] for message in ws.sent] == [
            "DOM.getFrameOwner", "DOM.scrollIntoViewIfNeeded"
        ]

    def test_a_frames_elements_are_moved_to_where_the_frame_sits(self):
        """Rects inside a frame are measured against the FRAME's viewport, so a
        frame halfway down the page would otherwise report its contents as
        though they were at the top of the screen."""
        ws = _FakeWebsocket({
            "Page.createIsolatedWorld": {"executionContextId": 42},
            "Runtime.evaluate": {"result": {"value":
                                            '{"elements":[{"tag":"A","x":10,"y":20}]}'}},
            "DOM.getFrameOwner": {"backendNodeId": 7},
            "DOM.getBoxModel": {"model": {"content": [30, 400, 0, 0, 0, 0, 0, 0]}},
        })
        page = _web.Channel("ws://x", websocket_module=ws).read_frame("F1")
        assert (page["elements"][0]["x"], page["elements"][0]["y"]) == (40, 420)

    def test_a_frame_that_cannot_be_located_is_dropped_rather_than_placed(self):
        """Its contents would otherwise land on the top document: a control 400 px
        down the page reported as though it were at the top of the screen."""
        ws = _FakeWebsocket({
            "Page.createIsolatedWorld": {"executionContextId": 42},
            "Runtime.evaluate": {"result": {"value":
                                            '{"elements":[{"tag":"A","x":10,"y":20}]}'}},
            "DOM.getFrameOwner": {},
        })
        assert _web.Channel("ws://x", websocket_module=ws).read_frame("F1") is None

    def test_a_frame_whose_owner_has_no_box_is_dropped_too(self):
        ws = _FakeWebsocket({
            "Page.createIsolatedWorld": {"executionContextId": 42},
            "Runtime.evaluate": {"result": {"value":
                                            '{"elements":[{"tag":"A","x":10,"y":20}]}'}},
            "DOM.getFrameOwner": {"backendNodeId": 7},
            "DOM.getBoxModel": {"model": {}},
        })
        assert _web.Channel("ws://x", websocket_module=ws).read_frame("F1") is None

    def test_a_frame_with_no_context_yields_none_rather_than_a_bare_page(self):
        ws = _FakeWebsocket({"Page.createIsolatedWorld": {}})
        assert _web.Channel("ws://x", websocket_module=ws).read_frame("F1") is None

    def test_closed_roots_are_read_with_pierce(self):
        ws = _FakeWebsocket({"DOM.getDocument": {"root": {"nodeName": "#document"}}})
        _web.Channel("ws://x", websocket_module=ws).pierce_closed_roots()
        assert ws.sent[-1]["params"]["pierce"] is True


class TestDeviceAttachment:
    """Reaching the socket: one forward per socket, released at teardown."""

    #: `ps -A` as an Android device prints it — USER, PID, PPID, VSZ, RSS, WCHAN,
    #: ADDR, S(TAT), NAME — measured on device alongside `pidof`. NAME is always
    #: the last column; PID is always the second.
    PS_A_HEADER = "USER      PID   PPID  VSZ   RSS   WCHAN PC  S NAME"

    def setup_method(self):
        _web._forwards.clear()
        _web._unreachable = False
        _web.remember_target("")

    def test_a_socket_is_forwarded_once_per_session(self, monkeypatch):
        calls = []
        monkeypatch.setattr(_web, "_adb", lambda *a, **kw: calls.append(a) or "41234")
        socket = _web.Socket("chrome_devtools_remote", None, "browser")
        assert _web.forward(socket) == 41234
        assert _web.forward(socket) == 41234
        assert len(calls) == 1

    def test_teardown_removes_exactly_the_forwards_this_session_made(self, monkeypatch):
        removed = []

        def adb(*args, **kwargs):
            if args[0] == "forward" and args[1] == "--remove":
                removed.append(args[2])
                return ""
            return "41234"

        monkeypatch.setattr(_web, "_adb", adb)
        _web.forward(_web.Socket("chrome_devtools_remote", None, "browser"))
        _web.reset()
        assert removed == ["tcp:41234"]
        assert _web._forwards == {}

    def test_a_teardown_that_cannot_reach_the_device_still_clears_its_state(
            self, monkeypatch):
        """Teardown runs on the failure paths too, where the device may already
        be gone; it must not raise over the verdict the session is reporting."""
        monkeypatch.setattr(_web, "_adb", lambda *a, **kw: "41234")
        _web.forward(_web.Socket("chrome_devtools_remote", None, "browser"))
        _web.remember_target("ws://x")

        def dead(*args, **kwargs):
            raise RuntimeError("device offline")

        monkeypatch.setattr(_web, "_adb", dead)
        _web.reset()
        assert _web._forwards == {}
        assert _web.remembered_target() == ""

    def test_remembered_targets_are_isolated_by_foreground_package(self):
        _web.remember_target("ws://stable", "com.android.chrome")
        _web.remember_target("ws://beta", "com.chrome.beta")

        assert _web.remembered_target("com.android.chrome") == "ws://stable"
        assert _web.remembered_target("com.chrome.beta") == "ws://beta"
        assert _web.remembered_target("com.chrome.canary") == ""

        _web.remember_target("", "com.android.chrome")
        assert _web.remembered_target("com.android.chrome") == ""
        assert _web.remembered_target("com.chrome.beta") == "ws://beta"

    def test_a_cloud_session_is_never_reachable(self, monkeypatch):
        monkeypatch.setattr(_web._config, "run_target", "cloud")
        assert _web.reachable() is False

    def test_a_device_found_unreachable_is_not_probed_again(self, monkeypatch):
        monkeypatch.setattr(_web._config, "run_target", "local")
        assert _web.reachable() is True
        _web.mark_unreachable(RuntimeError("no sockets"))
        assert _web.reachable() is False

    def test_every_process_a_package_runs_under_is_returned(self, monkeypatch):
        """An app commonly runs several processes and the WebView need not live in
        the first; taking one would filter its own app's socket out."""
        monkeypatch.setattr(_web._config, "get", lambda key, default=None: None)
        monkeypatch.setattr(_web.subprocess, "run", lambda cmd, **kw: _Completed(
            f"{self.PS_A_HEADER}\n"
            "u0_a1     100   1     1     1     0     0    S com.example.app\n"
            "u0_a1     200   100   1     1     0     0    S com.example.app:child\n"
            "u0_a1     300   100   1     1     0     0    S com.example.app:other\n"
        ))
        assert _web.pids_of("com.example.app") == {100, 200, 300}

    def test_a_child_process_hosting_the_webview_is_included(self, monkeypatch):
        """Measured on device: `pidof com.android.chrome` returns only 12188,
        while the WebView it hosts in `android:process=":privileged_process0"`
        runs as 12241 — a pid `pidof` never reports, and a socket named for it
        would be filtered out as though it belonged to another app entirely."""
        monkeypatch.setattr(_web._config, "get", lambda key, default=None: None)
        monkeypatch.setattr(_web.subprocess, "run", lambda cmd, **kw: _Completed(
            f"{self.PS_A_HEADER}\n"
            "u0_a123   12188 123   1     1     0     0    S com.android.chrome\n"
            "u0_a123   12241 12188 1     1     0     0    S "
            "com.android.chrome:privileged_process0\n"
        ))
        assert _web.pids_of("com.android.chrome") == {12188, 12241}

    def test_a_package_that_merely_prefixes_another_is_not_matched(self, monkeypatch):
        """`com.app.other` is a distinct app; `com.app` must not absorb its pid."""
        monkeypatch.setattr(_web._config, "get", lambda key, default=None: None)
        monkeypatch.setattr(_web.subprocess, "run", lambda cmd, **kw: _Completed(
            f"{self.PS_A_HEADER}\n"
            "u0_a1     100   1     1     1     0     0    S com.app.other\n"
        ))
        assert _web.pids_of("com.app") is None

    def test_a_package_that_is_not_running_has_no_pids(self, monkeypatch):
        """`ps -A` succeeds and simply does not list the package — unlike
        `pidof`, which signals absence with a non-zero exit code."""
        monkeypatch.setattr(_web._config, "get", lambda key, default=None: None)
        monkeypatch.setattr(_web.subprocess, "run", lambda cmd, **kw: _Completed(
            f"{self.PS_A_HEADER}\n"
            "u0_a2     900   1     1     1     0     0    S com.other.app\n"
        ))
        assert _web.pids_of("com.example.app") is None

    def test_a_failed_ps_command_is_non_fatal(self, monkeypatch):
        monkeypatch.setattr(_web._config, "get", lambda key, default=None: None)
        monkeypatch.setattr(_web.subprocess, "run",
                            lambda cmd, **kw: _Completed("", "error: device offline", 1))
        assert _web.pids_of("com.example.app") is None

    def test_the_no_socket_diagnostic_fires_once_and_reset_rearms_it(self, caplog):
        """A build with webview debugging disabled publishes nothing to fail
        against; the diagnostic that says so must not repeat every action, and
        must be able to fire again in a session that starts over."""
        with caplog.at_level("INFO", logger="testmu_appium"):
            _web.mark_no_socket("com.example.app")
            _web.mark_no_socket("com.example.app")
        assert caplog.text.count("com.example.app publishes no devtools socket") == 1

        _web.reset()

        with caplog.at_level("INFO", logger="testmu_appium"):
            _web.mark_no_socket("com.example.app")
        assert caplog.text.count("com.example.app publishes no devtools socket") == 2

    def test_the_configured_device_is_the_one_adb_talks_to(self, monkeypatch):
        """A host with two devices attached answers `adb shell` with an error
        rather than a guess, so the serial is always named."""
        seen = []
        monkeypatch.setattr(_web._config, "get",
                            lambda key, default=None: "R5CT30" if key == "udid" else default)
        monkeypatch.setattr(_web.subprocess, "run",
                            lambda cmd, **kw: seen.append(cmd) or _Completed("41234"))
        _web._adb("forward", "tcp:0", "localabstract:x")
        assert seen[0][:3] == ["adb", "-s", "R5CT30"]

    def test_a_failed_adb_command_raises_rather_than_returning_empty(self, monkeypatch):
        monkeypatch.setattr(_web._config, "get", lambda key, default=None: None)
        monkeypatch.setattr(_web.subprocess, "run",
                            lambda cmd, **kw: _Completed("", "error: device offline", 1))
        with pytest.raises(RuntimeError, match="device offline"):
            _web._adb("shell", "cat", "/proc/net/unix")


class _Completed:
    def __init__(self, stdout, stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


class TestPanning:
    """`visualViewport.offsetLeft/Top` is part of the model, not of the conversion
    alone. Solving without it and converting with it subtracts it twice, and every
    calibration sample shifts by the same amount so the agreement check cannot see
    it."""

    def test_an_origin_solved_under_panning_converts_back_to_where_it_came_from(self):
        native = (300, 900, 400, 960)
        css = (120.0, 300.0)
        origin = _web.derive_origin(css, native, dpr=3, scale=2,
                                    offset_left=50, offset_top=20)
        assert _web.to_device(css[0], css[1], origin=origin, dpr=3, scale=2,
                              offset_left=50, offset_top=20) == (native[0], native[1])

    def test_an_unpanned_page_is_unaffected(self):
        native = (300, 900, 400, 960)
        origin = _web.derive_origin((10.0, 20.0), native, dpr=3, scale=1)
        assert origin == _web.derive_origin((10.0, 20.0), native, dpr=3, scale=1,
                                            offset_left=0, offset_top=0)


class TestFramePaths:
    """The frame path is the tie-breaker for one selector naming one element per
    frame, so two frames must not share a path."""

    def test_sibling_frames_and_shadow_roots_are_told_apart(self):
        """Both segments carry the container's index, so two frames under one
        parent no longer produce the same path. The walk runs in the page, so what
        is pinned here is the expression; the behaviour is verified on device."""
        assert "const index = frames++" in _web.WALK_JS
        assert "path + '>f' + index" in _web.WALK_JS
        assert "path + '>s' + (shadowRoots++)" in _web.WALK_JS

    def test_a_recovered_frames_elements_are_labelled_with_that_frame(self):
        """The walk inside a recovered frame starts at the root, so without a
        prefix its elements claim to be in the top document — the one place they
        are certainly not."""
        ws = _FakeWebsocket({
            "Page.createIsolatedWorld": {"executionContextId": 42},
            "Runtime.evaluate": {"result": {"value":
                                            '{"elements":[{"tag":"A","x":0,"y":0}]}'}},
            "DOM.getFrameOwner": {"backendNodeId": 7},
            "DOM.getBoxModel": {"model": {"content": [0, 0, 0, 0, 0, 0, 0, 0]}},
        })
        page = _web.Channel("ws://x", websocket_module=ws).read_frame("F1", ">x2")
        assert page["elements"][0]["path"] == ">x2"

    def test_a_frame_already_recovered_is_not_offered_again(self):
        tree = {"frameTree": {
            "frame": {"id": "ROOT", "url": "https://example.com/"},
            "childFrames": [{"frame": {"id": "F1", "url": "https://other.test/"}}]}}
        ws = _FakeWebsocket({"Page.getFrameTree": tree})
        channel = _web.Channel("ws://x", websocket_module=ws)
        page = {"blockedUrls": ["https://other.test/"]}
        assert channel.unreachable_frames(page) != []
        assert channel.unreachable_frames(page, seen={"https://other.test/"}) == []


class TestTransformedFrames:
    """Frame geometry composes by translation, which is only right while the frame
    is drawn at its own scale."""

    def test_the_walk_compares_the_frames_box_against_its_own_viewport(self):
        assert "doc.documentElement.clientWidth" in _web.WALK_JS
        assert "Math.abs(outer - inner) > 4" in _web.WALK_JS
        assert "transformed++" in _web.WALK_JS

    def test_a_transformed_frame_is_counted_rather_than_walked(self):
        """Counted so the count can be logged: silently dropping a frame's
        contents reads as a page that has none."""
        assert "transformedFrames: transformed" in _web.WALK_JS
