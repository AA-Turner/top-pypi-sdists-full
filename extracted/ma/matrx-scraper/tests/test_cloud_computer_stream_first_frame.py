"""The Cloud Computer screen page says "connected" only with a picture on screen (2026-10-17).

Live, the page posted "connected" when the video peer's ICE connected, the app
dropped its "Connecting..." cover, and the person saw this page's own black
loader until the first frame arrived (FIX-FIRST-FRAME-2026-10-17). "connected"
now waits for a frame decoded after the connection, on first connect and on
every reconnect. This runs the real matrx-stream.js in Node against stand-ins
for Selkies' globals and the video element.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

PAGE = Path(__file__).resolve().parents[1] / "docker" / "cloud-computer" / "stream-client" / "matrx-stream.js"

HARNESS = r"""
const vm = require("vm");
const fs = require("fs");
const timers = [];
const frameCallbacks = [];
const videoListeners = {};
let frames = 0;
const el = () => ({ setAttribute() {}, addEventListener() {}, classList: { add() {} }, focus() {}, appendChild() {} });
const video = {
  videoWidth: 0,
  setAttribute() {}, focus() {},
  addEventListener(type, fn) { (videoListeners[type] = videoListeners[type] || []).push(fn); },
  requestVideoFrameCallback(fn) { frameCallbacks.push(fn); },
  getVideoPlaybackQuality() { return { totalVideoFrames: frames }; },
};
const loaderClasses = [];
const loader = { set innerHTML(v) {}, addEventListener() {}, classList: { add(c) { loaderClasses.push(c); } } };
const ctx = {
  URL, URLSearchParams,
  location: { search: "" },
  document: {
    referrer: "", body: el(), documentElement: el(),
    createElement: () => loader, getElementById: () => video, addEventListener() {},
  },
  webrtc: { input: null, sendDataChannelMessage() {} },
  signalling: {}, app: {},
  addEventListener() {}, focus() {},
  setTimeout(fn) { timers.push(fn); },
};
ctx.window = ctx; ctx.parent = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], "utf8"), ctx);
const states = () => ctx.__matrxStreamPosts.map((m) => m.state);
function tick() { const due = timers.splice(0); due.forEach((fn) => fn()); }
function present() { frames += 1; video.videoWidth = 1440; frameCallbacks.splice(0).forEach((fn) => fn()); }
function decodeOnly() { frames += 1; video.videoWidth = 1440; }
const log = {};
ctx.webrtc.onconnectionstatechange("connecting");
ctx.webrtc.onconnectionstatechange("connected");
tick(); tick();
log.peerUpNoFrame = states();
present();
log.afterFirstFrame = states();
log.loaderHidden = loaderClasses.includes("matrx-hidden");
ctx.webrtc.onconnectionstatechange("disconnected");
ctx.webrtc.onconnectionstatechange("connected");
tick();
log.reconnectedNoNewFrame = states();
decodeOnly(); tick();
(videoListeners.loadeddata || []).forEach((fn) => fn());
(videoListeners.playing || []).forEach((fn) => fn());
log.visibleDecodeOnly = states();
ctx.document.hidden = true;
decodeOnly(); tick();
log.afterReconnectFrame = states();
process.stdout.write(JSON.stringify(log));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_connected_waits_for_a_frame_on_connect_and_reconnect(tmp_path) -> None:
    harness = tmp_path / "harness.js"
    harness.write_text(HARNESS, encoding="utf-8")
    out = subprocess.run(
        ["node", str(harness), str(PAGE)], capture_output=True, text=True, check=True, timeout=30
    ).stdout
    log = json.loads(out)
    # The peer is up but no frame yet: the app must keep its own cover.
    assert log["peerUpNoFrame"] == ["connecting"]
    # The first presented frame is the moment the app may reveal the stream.
    assert log["afterFirstFrame"] == ["connecting", "connected"]
    assert log["loaderHidden"] is True
    # A reconnect keeps "reconnecting" until a frame arrives after it.
    assert log["reconnectedNoNewFrame"] == ["connecting", "connected", "reconnecting"]
    # On a VISIBLE page a decoded frame that was never presented is no picture
    # (2026-10-18: in the app's pane the cover dropped onto an unpainted frame;
    # the review saw it black for 8-25 s). Only a presented frame counts there.
    assert log["visibleDecodeOnly"] == ["connecting", "connected", "reconnecting"]
    # A hidden page presents nothing, so there the decoded counter is the signal.
    assert log["afterReconnectFrame"] == ["connecting", "connected", "reconnecting", "connected"]
