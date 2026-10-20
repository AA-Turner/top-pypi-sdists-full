"""A reopened Cloud Computer session uses the newest TURN credentials (2026-10-17).

Selkies 1.6.2 builds each session's webrtcbin from ``app.turn_servers``, which
it reads once at start. Its RTC-file callback (``mon_rtc_config``) only pokes the
webrtcbin that is running at that moment, so a warm machine opened every later
session with the TURN credentials it started with. Those expire after 120 s:
close the Computer, wait two minutes, open it again, and the machine offers no
relay route (live, machine 681bba: relay candidates only while the startup
credentials were under 120 s old; the two later sessions never opened a data
channel). Each rewrite during a session also ``add-turn-server``-ed one more
entry into the live agent until libnice refused more than 8.

This runs the upstream callback and upstream's pipeline TURN setup verbatim,
then the callback through the patcher's real edit, against a recording
webrtcbin.
"""
from __future__ import annotations

import importlib.util
import logging
from pathlib import Path
from types import SimpleNamespace

PATCHER = Path(__file__).resolve().parents[1] / "docker" / "cloud-computer" / "patch-selkies-web.py"

# Selkies 1.6.2 gstwebrtc_app.py GSTWebRTCApp.build_webrtc_pipeline, the STUN/TURN
# lines, verbatim (one level of indentation removed).
UPSTREAM_PIPELINE_TURN = """\
    if self.stun_servers:
        logger.info("updating STUN server")
        self.webrtcbin.set_property("stun-server", self.stun_servers[0])

    # Add TURN server
    if self.turn_servers:
        for i, turn_server in enumerate(self.turn_servers):
            logger.info("updating TURN server")
            if i == 0:
                self.webrtcbin.set_property("turn-server", turn_server)
            else:
                self.webrtcbin.emit("add-turn-server", turn_server)
"""

STARTUP = ["turn://old:expired@relay:3478", "turn://old:expired@relay:443"]


def _fresh(n: int) -> list[str]:
    return [f"turn://u{n}:c{n}@relay:3478", f"turn://u{n}:c{n}@relay:443"]


class Webrtcbin:
    """Records TURN entries the way libnice holds them: one set per agent."""

    def __init__(self) -> None:
        self.primary: str | None = None
        self.added: list[str] = []

    def set_property(self, name: str, value: str) -> None:
        if name == "turn-server":
            self.primary = value

    def emit(self, signal: str, value: str) -> None:
        assert signal == "add-turn-server"
        self.added.append(value)

    @property
    def turn_servers(self) -> list[str]:
        return ([self.primary] if self.primary else []) + self.added


def _patcher():
    spec = importlib.util.spec_from_file_location("patch_selkies_web", PATCHER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _callback(fragment: str, app, audio_app, server):
    namespace: dict = {}
    source = "def build(app, audio_app, server, logger):\n" + fragment + "    return mon_rtc_config\n"
    exec(compile(source, "selkies_main_fragment", "exec"), namespace)
    return namespace["build"](app, audio_app, server, logging.getLogger("selkies-fragment"))


def _start_pipeline(app) -> None:
    """Upstream's per-session webrtcbin build, verbatim TURN setup."""
    app.webrtcbin = Webrtcbin()
    namespace: dict = {}
    source = "def setup(self, logger):\n" + UPSTREAM_PIPELINE_TURN
    exec(compile(source, "selkies_pipeline_fragment", "exec"), namespace)
    namespace["setup"](app, logging.getLogger("selkies-fragment"))


def _scenario(fragment: str):
    """Warm machine: one session with heartbeats, close, then a reopen after a new ticket."""
    app = SimpleNamespace(stun_servers=["stun://s:3478"], turn_servers=list(STARTUP), webrtcbin=None)
    audio_app = SimpleNamespace(stun_servers=["stun://s:3478"], turn_servers=list(STARTUP), webrtcbin=None)
    server = SimpleNamespace(rtc=None, set_rtc_config=lambda rtc: setattr(server, "rtc", rtc))
    mon = _callback(fragment, app, audio_app, server)

    mon(["stun://s:3478"], _fresh(1), "rtc-1")  # first open writes a fresh relay
    _start_pipeline(app)
    first_session = app.webrtcbin
    for n in range(2, 14):  # heartbeats rewrite the file during the session
        mon(["stun://s:3478"], _fresh(n), f"rtc-{n}")
    app.webrtcbin = None  # the viewer closes; upstream stop_pipeline drops the webrtcbin

    mon(["stun://s:3478"], _fresh(99), "rtc-99")  # reopen: the claim writes a fresh relay
    _start_pipeline(app)
    _start_pipeline(audio_app)
    return first_session, app.webrtcbin, audio_app.webrtcbin, server


def test_upstream_reopen_uses_startup_credentials_and_piles_up_turn_servers() -> None:
    """The harness sees both defects in the upstream callback."""
    first, reopened, audio, server = _scenario(_patcher().UPSTREAM_MON_RTC_CONFIG)
    assert reopened.turn_servers == STARTUP  # expired credentials: no relay route
    assert audio.turn_servers == STARTUP
    assert len(first.turn_servers) > 8  # libnice: "more than 8 turn servers per component"
    assert server.rtc == "rtc-99"


def test_patched_reopen_uses_newest_credentials_and_never_appends() -> None:
    patcher = _patcher()
    old, new = patcher.UPSTREAM_MON_RTC_CONFIG, patcher.MATRX_MON_RTC_CONFIG
    assert (old, new) in patcher.PACKAGE_EDITS["__main__.py"]
    patched = patcher.patch_text("__main__.py", old, [(old, new)])
    first, reopened, audio, server = _scenario(patched)
    assert reopened.turn_servers == _fresh(99)
    assert audio.turn_servers == _fresh(99)
    assert first.turn_servers == _fresh(1)  # the live session's agent is never appended to
    assert server.rtc == "rtc-99"  # the viewer's /turn answer still follows the file
