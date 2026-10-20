"""The screen page keeps its picture when its signalling socket drops (2026-10-17).

A release drains the aidream gateway task that carries the page's Selkies
signalling socket. Upstream's page answered the close with ``webrtc.reset()``:
it closed the live peer connection and started over behind "Reconnecting...".
While the peer is still connected the page now only re-opens signalling as a
resume (the machine's hub puts it back in its session); upstream's reset still
runs when the hub refuses, the peer is down, or the page closed signalling on
purpose. The page also keeps its own two-minute stream cookie fresh so the
re-opened socket is admitted. This runs the real matrx-stream.js in Node
against stand-ins for Selkies' globals.
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
const fetches = [];
let fetchReply = { ok: true, json: () => Promise.resolve({ refresh_in_seconds: 20 }) };
const el = () => ({ setAttribute() {}, addEventListener() {}, classList: { add() {} }, focus() {}, appendChild() {} });
const video = { videoWidth: 1440, setAttribute() {}, focus() {}, addEventListener() {},
  getVideoPlaybackQuality() { return { totalVideoFrames: 1 }; } };
function makeSignalling(log, name) {
  const sig = { connects: 0, sockets: [] };
  sig.connect = function () {
    this.connects += 1;
    const listeners = {};
    this._ws_conn = { addEventListener(t, fn) { (listeners[t] = listeners[t] || []).push(fn); } };
    this._ws_conn.emit = (t, e) => (listeners[t] || []).forEach((fn) => fn(e));
    this.sockets.push(this._ws_conn);
  };
  sig.disconnect = function () { log.push(name + ".disconnect"); };
  return sig;
}
const log = [];
const signalling = makeSignalling(log, "signalling");
const audio_signalling = makeSignalling(log, "audio_signalling");
const webrtc = { input: null, sendDataChannelMessage() {}, peerConnection: { connectionState: "connected" } };
const audio_webrtc = { peerConnection: { connectionState: "new" }, reset() { log.push("audio_webrtc.reset"); } };
signalling.ondisconnect = () => log.push("upstream video reset");
audio_signalling.ondisconnect = () => { log.push("upstream audio reset"); signalling.disconnect(); };
const ctx = {
  URL, URLSearchParams, Promise, Number,
  location: { search: "" },
  document: { referrer: "", body: el(), documentElement: el(),
    createElement: () => ({ set innerHTML(v) {}, addEventListener() {}, classList: { add() {} } }),
    getElementById: () => video, addEventListener() {} },
  webrtc, signalling, audio_signalling, audio_webrtc, app: {},
  addEventListener() {}, focus() {},
  setTimeout(fn, ms) { timers.push([fn, ms]); },
  fetch(url, opts) { fetches.push([url, opts.method, opts.credentials]); return Promise.resolve(fetchReply); },
};
ctx.window = ctx; ctx.parent = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], "utf8"), ctx);
const states = () => ctx.__matrxStreamPosts.map((m) => m.state);
const out = {};
(async () => {
  await new Promise((r) => setImmediate(r));
  out.cookie_fetch = fetches[0];
  out.cookie_timer_ms = timers.length ? timers[timers.length - 1][1] : null;
  // The picture is up.
  ctx.webrtc.onconnectionstatechange("connected");
  const before = states().slice();
  // 1. The gateway task drains: the socket closes while the peer is connected.
  signalling.ondisconnect();
  out.resume = { connects: signalling.connects, resume_flag: signalling.matrx_resume,
    log: log.slice(), new_states: states().slice(before.length) };
  // 2. The hub had nothing to resume: it says so, then closes.
  signalling._ws_conn.emit("message", { data: "ERROR matrx-no-session" });
  signalling.ondisconnect();
  out.refused = { log: log.slice(), resume_flag: signalling.matrx_resume, last_state: states().slice(-1)[0] };
  // 3. Selkies' own "reload" closes signalling on purpose: upstream reset.
  log.length = 0; signalling.connect();
  signalling.disconnect(); signalling.ondisconnect();
  out.deliberate = log.slice();
  // 4. The peer itself is down: upstream reset.
  log.length = 0; signalling.connect(); webrtc.peerConnection.connectionState = "failed";
  signalling.ondisconnect();
  out.peer_down = log.slice();
  // 5. A lost audio link resets audio only, never the picture.
  log.length = 0; audio_signalling.ondisconnect();
  out.audio = log.slice();
  out.resumes = ctx.__matrxSignallingResumes.length;
  console.log(JSON.stringify(out));
})();
"""


@pytest.fixture(scope="module")
def run():
    if shutil.which("node") is None:
        pytest.skip("node is not installed")
    harness = Path(__file__).with_name("_signalling_resume_harness.js")
    harness.write_text(HARNESS)
    try:
        done = subprocess.run(["node", str(harness), str(PAGE)], capture_output=True, text=True, timeout=30)
    finally:
        harness.unlink()
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout.strip().splitlines()[-1])


def test_a_dropped_socket_with_a_live_picture_only_reopens_signalling(run):
    assert run["resume"]["connects"] == 1
    assert run["resume"]["resume_flag"] is True
    assert "upstream video reset" not in run["resume"]["log"]
    assert run["resume"]["new_states"] == [], "no Reconnecting cover while the picture is live"
    assert run["resumes"] == 1


def test_a_refused_resume_falls_back_to_upstreams_reset(run):
    assert run["refused"]["log"] == ["upstream video reset"]
    assert run["refused"]["resume_flag"] is False
    assert run["refused"]["last_state"] == "reconnecting"


def test_a_deliberate_close_and_a_dead_peer_still_reset(run):
    assert run["deliberate"] == ["signalling.disconnect", "upstream video reset"]
    assert run["peer_down"] == ["upstream video reset"]


def test_a_lost_audio_link_never_restarts_the_picture(run):
    assert run["audio"] == ["audio_webrtc.reset"]


def test_the_frame_keeps_its_own_stream_cookie_fresh(run):
    assert run["cookie_fetch"] == ["matrx-cookie", "POST", "same-origin"]
    assert run["cookie_timer_ms"] == 20000
