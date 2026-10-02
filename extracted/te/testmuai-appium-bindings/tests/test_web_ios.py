"""The iOS web provider: session lifetime, target ownership, and the envelope.

Each class here pins one way the single shared iwdp endpoint differs from
Android's per-app sockets — and one way pretending otherwise failed on a device.
"""
import json

import pytest

from testmu_appium import _config
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers import _web, _web_ios


@pytest.fixture(autouse=True)
def clean_state():
    _web_ios.reset()
    yield
    _web_ios.reset()


class TestTeardownReachesThisProvider:
    """The proxy child process, the port and the sticky unreachable verdict are
    session claims. Teardown lands in `_web.reset()` for every platform; before
    this it released only the Android forwards, and a second iOS session
    inherited the first one's proxy, target and verdict."""

    def test_web_reset_also_resets_the_ios_state(self):
        _web_ios._state.port = 32000
        _web_ios._state.unreachable = True
        _web_ios._state.remembered = "ws://old"
        _web_ios._state.foreground_pid = 1729
        _web.reset()
        assert _web_ios._state.port is None
        assert _web_ios._state.unreachable is False
        assert _web_ios._state.remembered == ""
        assert _web_ios._state.foreground_pid == 0


class TestTargetOwnership:
    """One proxy lists every inspectable page on the device — Safari's too.
    Ownership is the foreground app's pid, learned from the same
    `mobile: activeAppInfo` read that resolves the bundle id."""

    _TARGETS = [
        {"webSocketDebuggerUrl": "ws://a", "appId": "PID:1729", "title": "app"},
        {"webSocketDebuggerUrl": "ws://b", "appId": "PID:9999", "title": "safari"},
    ]

    def _serve(self, monkeypatch, targets):
        monkeypatch.setattr(_web_ios, "_json", lambda *_a, **_k: targets)

    def test_the_foreground_apps_pages_win(self, monkeypatch):
        self._serve(monkeypatch, self._TARGETS)
        _web_ios.note_foreground(1729)
        assert [t["title"] for t in _web_ios.list_targets(32000)] == ["app"]

    def test_no_learned_owner_keeps_the_old_behaviour(self, monkeypatch):
        self._serve(monkeypatch, self._TARGETS)
        assert len(_web_ios.list_targets(32000)) == 2

    def test_unattributable_targets_are_not_filtered(self, monkeypatch):
        """Entries with no parseable pid cannot be owned or disowned."""
        self._serve(monkeypatch, [
            {"webSocketDebuggerUrl": "ws://a", "title": "nameless"},
        ])
        _web_ios.note_foreground(1729)
        assert len(_web_ios.list_targets(32000)) == 1

    def test_an_owner_with_no_pages_gets_none_not_safaris(self, monkeypatch):
        self._serve(monkeypatch, [
            {"webSocketDebuggerUrl": "ws://b", "appId": "PID:9999"},
        ])
        _web_ios.note_foreground(1729)
        assert _web_ios.list_targets(32000) == []

    def test_a_changed_foreground_forgets_the_remembered_target(self):
        """The remembered page proved visible under the app that just LEFT."""
        _web_ios.note_foreground(1729)
        _web_ios._state.remembered = "ws://a"
        _web_ios.note_foreground(2222)
        assert _web_ios._state.remembered == ""

    def test_the_same_foreground_keeps_it(self):
        _web_ios.note_foreground(1729)
        _web_ios._state.remembered = "ws://a"
        _web_ios.note_foreground(1729)
        assert _web_ios._state.remembered == "ws://a"


class TestCloudSessionsDoNotSpawnALocalProxy:
    """A cloud session's device is not on this host's usbmux: an iwdp spawned
    here would read whatever LOCAL device is plugged in while gestures target
    the cloud one."""

    def test_reachable_is_false_on_a_cloud_run(self, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "cloud")
        transport = _web_ios.IwdpWebDebugTransport(udid="cloud-udid")
        assert transport.reachable() is False
        assert _web_ios._state.unreachable is True

    def test_a_local_run_still_reaches(self, monkeypatch):
        monkeypatch.setattr(_config, "run_target", "local")
        monkeypatch.setattr(_web_ios, "ensure_proxy", lambda *_a, **_k: 32000)
        assert _web_ios.IwdpWebDebugTransport().reachable() is True


class _ScriptedWire:
    """A websocket module whose connection announces a page target and answers
    Target-wrapped messages from a script of {inner method: inner result}."""

    def __init__(self, replies):
        self.replies = replies
        self.sent = []

    def create_connection(self, *args, **kwargs):
        wire = self

        class _Connection:
            def __init__(self):
                self.queue = [json.dumps({
                    "method": "Target.targetCreated",
                    "params": {"targetInfo": {"targetId": "page-1", "type": "page"}},
                })]

            def send(self, raw):
                message = json.loads(raw)
                assert message["method"] == "Target.sendMessageToTarget", (
                    f"raw RPC left the envelope: {message['method']}")
                wire.sent.append(message)
                inner = json.loads(message["params"]["message"])
                self.queue.append(json.dumps({
                    "method": "Target.dispatchMessageFromTarget",
                    "params": {"message": json.dumps({
                        "id": inner["id"],
                        "result": wire.replies[inner["method"]],
                    })},
                }))

            def recv(self):
                return self.queue.pop(0)

            def close(self):
                pass

        return _Connection()


class TestCallFunctionSpeaksTheEnvelope:
    """The inherited implementation sent raw `Runtime.evaluate` /
    `Runtime.callFunctionOn`, which this socket refuses — so every
    value-carrying storage verb failed on iOS while plain evaluate worked."""

    def test_both_rpcs_ride_inside_the_target_envelope(self):
        wire = _ScriptedWire({
            "Runtime.evaluate": {"result": {"objectId": "obj-7"}},
            "Runtime.callFunctionOn": {"result": {"value": "stored"}},
        })
        channel = _web_ios.IosChannel("ws://page", websocket_module=wire)
        value = channel.call_function("function(v){ return v }", ("stored",))
        assert value == "stored"
        inner = [json.loads(m["params"]["message"]) for m in wire.sent]
        assert [m["method"] for m in inner] == [
            "Runtime.evaluate", "Runtime.callFunctionOn"]
        call = inner[1]["params"]
        assert call["objectId"] == "obj-7"
        assert call["arguments"] == [{"value": "stored"}]

    def test_a_page_throw_is_an_error_not_a_value(self):
        wire = _ScriptedWire({
            "Runtime.evaluate": {"result": {"objectId": "obj-7"}},
            "Runtime.callFunctionOn": {
                "result": {}, "wasThrown": True,
            },
        })
        channel = _web_ios.IosChannel("ws://page", websocket_module=wire)
        with pytest.raises(RuntimeError):
            channel.call_function("function(){ throw 1 }")


class _RecordingIosChannel(_web_ios.IosChannel):
    """The real IosChannel with the WIRE stubbed: `call` records and answers
    from a script, `evaluate` records. What runs is the genuine WebKit cookie
    and history logic above the wire."""

    def __init__(self, *, cookies=None):
        self.cookie_jar = list(cookies or [])
        self.calls = []
        self.evaluations = []

    def call(self, method, params=None):
        self.calls.append((method, params))
        if method == "Page.getCookies":
            return {"cookies": self.cookie_jar}
        return {}

    def evaluate(self, expression, context_id=None):
        self.evaluations.append(expression)
        return None


class TestWebkitCookies:
    """The same verbs Chrome serves with Network/Storage methods, spoken in
    WebKit's own vocabulary — every route is the one Appium's remote debugger
    itself uses on this wire."""

    def test_reads_come_from_page_get_cookies(self):
        channel = _RecordingIosChannel(cookies=[{"name": "session"}])
        assert channel.get_cookies() == [{"name": "session"}]
        assert channel.calls == [("Page.getCookies", None)]

    def test_a_write_is_a_document_cookie_assignment(self):
        channel = _RecordingIosChannel()
        channel.set_cookies([{
            "name": "session", "value": "a b", "path": "/cart",
            "domain": "shop.example", "secure": True, "sameSite": "Lax",
        }])
        script = channel.evaluations[0]  # [1] is the verifying read-back
        assert script.startswith("document.cookie = ")
        assert "session=a%20b" in script
        assert "path=/cart" in script
        assert "domain=shop.example" in script
        assert "SameSite=Lax" in script
        assert "secure" in script

    def test_a_write_without_a_path_gets_safaris_default(self):
        """Safari does not reliably update a cookie without a path — the same
        defaulting the Appium driver applies."""
        channel = _RecordingIosChannel()
        channel.set_cookies([{"name": "k", "value": "v"}])
        assert "path=/" in channel.evaluations[0]

    def test_an_http_only_write_is_refused_not_silently_dropped(self):
        """No JavaScript can create an httpOnly cookie; writing one through
        document.cookie would claim success and never stick."""
        channel = _RecordingIosChannel()
        with pytest.raises(ValueError) as exc:
            channel.set_cookies([{"name": "sid", "value": "x", "httpOnly": True}])
        assert "httpOnly" in str(exc.value)
        assert channel.evaluations == []

    def test_a_delete_addresses_the_cookie_on_its_own_url(self):
        channel = _RecordingIosChannel()
        channel.delete_cookie({
            "name": "session", "domain": ".shop.example",
            "path": "/cart", "secure": True,
        })
        assert channel.calls == [("Page.deleteCookie", {
            "cookieName": "session", "url": "https://shop.example/cart",
        })]

    def test_clear_enumerates_and_deletes(self):
        """WebKit has no clearBrowserCookies counterpart."""
        channel = _RecordingIosChannel(cookies=[
            {"name": "a", "domain": "x.example", "path": "/"},
            {"name": "b", "domain": "x.example", "path": "/"},
        ])
        channel.clear_cookies()
        assert [m for m, _ in channel.calls] == [
            "Page.getCookies", "Page.deleteCookie", "Page.deleteCookie"]


class TestWebkitHistory:
    """WebKit has no getNavigationHistory to consult, so the PAGE is asked to
    move; at a boundary its own history.back() is a no-op, the same outcome
    Chrome's False describes."""

    def test_back_asks_the_page(self):
        channel = _RecordingIosChannel()
        assert channel.navigate_history(-1) is True
        assert channel.evaluations == ["history.back()"]

    def test_forward_asks_the_page(self):
        channel = _RecordingIosChannel()
        assert channel.navigate_history(1) is True
        assert channel.evaluations == ["history.forward()"]


class TestTheChannelsDeclareTheirProtocol:
    def test_the_ios_channel_is_not_raw_cdp(self):
        assert _web_ios.IosChannel.cdp_rpc is False

    def test_the_chrome_channel_is(self):
        assert getattr(_web.Channel, "cdp_rpc", True) is True


class TestTheProxyIsAlwaysOurOwn:
    """No adoption, ever: something already listening is either an unknown
    process (not ours to trust) or a dead session's orphan — and iOS orphans
    matter, because webinspectord serves ONE proxy per device. Ports come from
    the kernel, exactly as Android's `adb forward tcp:0` gets them, so
    parallel devices on one host never coordinate."""

    @pytest.fixture(autouse=True)
    def _no_real_processes(self, monkeypatch):
        self.killed = []
        self.spawned = []
        monkeypatch.setattr(
            _web_ios.shutil, "which", lambda _name: "/usr/local/bin/iwdp")
        def _record_kills(argv, **_kwargs):
            # ensure_proxy also shells out during simulator-socket discovery
            # (lsof/ps); only a pkill is a kill. stdout "" reads as no booted
            # simulators, keeping these tests on the device path.
            if argv[0] == "pkill":
                self.killed.append(argv)
            return type("R", (), {"returncode": 1, "stdout": ""})()

        monkeypatch.setattr(_web_ios.subprocess, "run", _record_kills)

        test = self

        class _Spawned:
            def __init__(self, argv, **_kwargs):
                test.spawned.append(argv)

            def poll(self):
                return None

            def terminate(self):
                pass

            def wait(self, timeout=None):
                return 0

        monkeypatch.setattr(_web_ios.subprocess, "Popen", _Spawned)
        monkeypatch.setattr(_web_ios, "_json", lambda *_a, **_k: [])
        monkeypatch.setattr(_web_ios, "_free_port", lambda: 45123)

    def test_the_port_is_kernel_assigned_and_returned(self):
        port = _web_ios.ensure_proxy("UDID-1")
        assert port == 45123
        assert _web_ios._state.port == 45123
        (argv,) = self.spawned
        assert argv == ["/usr/local/bin/iwdp", "-c", "UDID-1:45123"]

    def test_stale_proxies_for_this_device_are_killed_first(self):
        _web_ios.ensure_proxy("UDID-1")
        (kill_argv,) = self.killed
        assert kill_argv == ["pkill", "-f", "ios_webkit_debug_proxy.*UDID-1"]

    def test_nothing_is_ever_adopted(self, monkeypatch):
        """A listener already on some port is not probed, not trusted, not
        reused — the spawn happens regardless."""
        _web_ios.ensure_proxy("UDID-1")
        assert self.spawned, "a proxy must be spawned even if a port is busy"

    def test_idempotent_within_a_session(self):
        first = _web_ios.ensure_proxy("UDID-1")
        second = _web_ios.ensure_proxy("UDID-1")
        assert first == second
        assert len(self.spawned) == 1

    def test_an_explicit_port_is_honoured(self):
        assert _web_ios.ensure_proxy("UDID-1", port=40001) == 40001
        (argv,) = self.spawned
        assert argv[-1] == "UDID-1:40001"

    def test_a_lost_port_race_retries_on_a_fresh_port(self, monkeypatch):
        ports = iter([50001, 50002])
        monkeypatch.setattr(_web_ios, "_free_port", lambda: next(ports))
        test = self

        class _DiesOnce:
            deaths = [None]  # first spawn dies, second lives

            def __init__(self, argv, **_kwargs):
                test.spawned.append(argv)
                self._dead = bool(self.deaths)
                if self.deaths:
                    self.deaths.pop()

            def poll(self):
                return 1 if self._dead else None

            def terminate(self):
                pass

            def wait(self, timeout=None):
                return 0

        monkeypatch.setattr(_web_ios.subprocess, "Popen", _DiesOnce)
        answers = iter([Exception("not yet"), []])

        def _json(_port, *a, **k):
            answer = next(answers)
            if isinstance(answer, Exception):
                raise answer
            return answer

        monkeypatch.setattr(_web_ios, "_json", _json)
        assert _web_ios.ensure_proxy("UDID-1") == 50002
        assert [argv[-1] for argv in test.spawned] == [
            "UDID-1:50001", "UDID-1:50002"]


class TestPrepareWebSurface:
    """The host-facing warm-up: auteur calls this at session setup so the
    proxy's startup cost and its failure land there, not mid-run."""

    def test_ios_prepares_and_returns_the_port(self, monkeypatch):
        from testmu_appium import _config, perception

        monkeypatch.setitem(_config._config, "platform", "ios")
        monkeypatch.setitem(_config._config, "udid", "UDID-9")
        seen = {}

        def _ensure(udid, port):
            seen["udid"], seen["port"] = udid, port
            return 45999

        monkeypatch.setattr(_web_ios, "ensure_proxy", _ensure)
        assert perception.prepare_web_surface() == 45999
        assert seen == {"udid": "UDID-9", "port": None}

    def test_android_has_nothing_to_prewarm(self, monkeypatch):
        from testmu_appium import _config, perception

        monkeypatch.setitem(_config._config, "platform", "android")
        monkeypatch.setattr(
            _web_ios, "ensure_proxy",
            lambda *_a: pytest.fail("android must not touch the iOS proxy"))
        assert perception.prepare_web_surface() is None

    def test_an_explicit_udid_wins_over_the_configured_one(self, monkeypatch):
        from testmu_appium import _config, perception

        monkeypatch.setitem(_config._config, "platform", "ios")
        monkeypatch.setitem(_config._config, "udid", "configured")
        monkeypatch.setattr(
            _web_ios, "ensure_proxy", lambda udid, port: udid)
        assert perception.prepare_web_surface(udid="explicit") == "explicit"


class TestProxyTimeoutDoesNotLeak:
    """A proxy that spawns but never answers used to be left RUNNING —
    holding the device's single webinspectord slot — while the surface was
    marked unreachable for the rest of the session, with no retry."""

    def test_a_silent_spawn_is_torn_down_and_retried(self, monkeypatch):
        spawned = []

        class _Silent:
            def __init__(self, argv, **_kwargs):
                spawned.append(argv)
                self.terminated = False

            def poll(self):
                return None  # alive, never answering

            def terminate(self):
                self.terminated = True

            def wait(self, timeout=None):
                return 0

        monkeypatch.setattr(_web_ios.shutil, "which", lambda _n: "/bin/iwdp")
        monkeypatch.setattr(_web_ios.subprocess, "Popen", _Silent)
        monkeypatch.setattr(
            _web_ios.subprocess, "run",
            lambda *_a, **_k: type("R", (), {"returncode": 1})())
        monkeypatch.setattr(_web_ios, "_json",
                            lambda *_a, **_k: (_ for _ in ()).throw(
                                RuntimeError("not answering")))
        monkeypatch.setattr(_web_ios, "_free_port", lambda: 45000 + len(spawned))
        monkeypatch.setattr(_web_ios, "_PROXY_READY_TIMEOUT_S", 0.05)
        monkeypatch.setattr(_web_ios, "_PROXY_POLL_S", 0.01)

        with pytest.raises(RuntimeError) as exc:
            _web_ios.ensure_proxy("UDID-1")
        assert "did not answer" in str(exc.value)
        assert len(spawned) == _web_ios._SPAWN_ATTEMPTS, "every attempt used"
        assert _web_ios._state.process is None, "no child left behind"

    def test_a_proxy_that_died_mid_session_is_respawned(self, monkeypatch):
        class _Dead:
            def poll(self):
                return 1

        _web_ios._state.port = 45001
        _web_ios._state.process = _Dead()
        respawned = {}

        def _fresh(udid_arg):
            respawned["called"] = True
            return 45002

        monkeypatch.setattr(_web_ios.shutil, "which", lambda _n: "/bin/iwdp")
        monkeypatch.setattr(
            _web_ios.subprocess, "run",
            lambda *_a, **_k: type("R", (), {"returncode": 1})())

        class _Alive:
            def __init__(self, argv, **_kwargs):
                pass

            def poll(self):
                return None

            def terminate(self):
                pass

            def wait(self, timeout=None):
                return 0

        monkeypatch.setattr(_web_ios.subprocess, "Popen", _Alive)
        monkeypatch.setattr(_web_ios, "_json", lambda *_a, **_k: [])
        monkeypatch.setattr(_web_ios, "_free_port", lambda: 45002)
        assert _web_ios.ensure_proxy("UDID-1") == 45002


class TestCookieWritesAreReadBack:
    """document.cookie can silently refuse a write; 'set N cookie(s)' must be
    a fact, not a claim."""

    def test_a_refused_cookie_is_named_in_a_warning(self, caplog):
        import logging as _logging

        channel = _RecordingIosChannel()

        def evaluate(script, context_id=None):
            channel.evaluations.append(script)
            # writes answer nothing; the verifying read-back returns the jar
            # with only ONE of the two names actually kept
            return "" if script.startswith("document.cookie = ") else "kept=1"

        channel.evaluate = evaluate
        with caplog.at_level(_logging.WARNING, logger="testmu_appium"):
            channel.set_cookies([{"name": "kept", "value": "1"},
                                 {"name": "dropped", "value": "2"}])
        assert "['dropped']" in caplog.text, "only the refused name is reported"
