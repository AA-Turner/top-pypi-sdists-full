"""The Cloud Computer screen page reports its picture quality (2026-11-19).

A laggy screen said nothing: the page knew "connected" and nothing else, so
neither the person nor we could tell a slow network from a busy machine. While
connected and visible the page now posts raw numbers from its own video
connection every two seconds; the app judges them. This runs the real
matrx-stream.js in Node against stand-ins for Selkies' globals.
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
const el = () => ({ setAttribute() {}, addEventListener() {}, classList: { add() {} }, focus() {}, appendChild() {} });
const video = {
  videoWidth: 0, setAttribute() {}, focus() {}, addEventListener() {},
  requestVideoFrameCallback(fn) { frameCallbacks.push(fn); },
  getVideoPlaybackQuality() { return { totalVideoFrames: 0 }; },
};
const loader = { set innerHTML(v) {}, addEventListener() {}, classList: { add() {} } };
let stats = [];
const winListeners = {};
let now = 1000000;
const ctx = {
  URL, URLSearchParams, isFinite,
  Date: { now: () => now },
  location: { search: "" },
  document: {
    referrer: "", hidden: false, body: el(), documentElement: el(),
    createElement: () => loader, getElementById: () => video, addEventListener() {},
  },
  webrtc: {
    input: null, sendDataChannelMessage() {},
    peerConnection: { getStats: () => ({ then(fn) { fn(stats); return { catch() {} }; } }) },
  },
  signalling: {}, app: {},
  addEventListener(type, fn) { (winListeners[type] = winListeners[type] || []).push(fn); }, focus() {},
  setTimeout(fn) { timers.push(fn); },
};
ctx.window = ctx; ctx.parent = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], "utf8"), ctx);
const quality = () => ctx.__matrxStreamPosts.filter((m) => m.state === "quality").map((m) => m.quality);
function tick() { const due = timers.splice(0); due.forEach((fn) => fn()); }
function report(frames, lost, received, bytes, buffered, emitted, freezes, rtt, type) {
  stats = [
    { id: "in", type: "inbound-rtp", kind: "video", framesDecoded: frames, packetsLost: lost,
      packetsReceived: received, bytesReceived: bytes, jitterBufferDelay: buffered,
      jitterBufferEmittedCount: emitted, freezeCount: freezes },
    { id: "t", type: "transport", selectedCandidatePairId: "p" },
    { id: "p", type: "candidate-pair", currentRoundTripTime: rtt, localCandidateId: "l", remoteCandidateId: "r" },
    { id: "l", type: "local-candidate", candidateType: type },
    { id: "r", type: "remote-candidate", candidateType: "prflx" },
  ];
}
const log = {};
report(100, 0, 1000, 100000, 1.0, 100, 0, 0.05, "relay");
tick();
log.beforeConnected = quality().length;
ctx.webrtc.onconnectionstatechange("connected");
video.videoWidth = 1440; frameCallbacks.splice(0).forEach((fn) => fn());
tick();
log.firstSampleIsBaseline = quality().length;
now += 2000;
report(120, 10, 1190, 600000, 5.0, 120, 1, 0.4, "relay");
tick();
log.second = quality();
now += 1000; (winListeners.pointermove || []).forEach((fn) => fn());
now += 1000;
report(180, 10, 1390, 1100000, 5.0, 180, 1, 0.4, "relay");
tick();
log.thirdActive = quality()[1].active;
ctx.document.hidden = true;
now += 2000;
report(120, 10, 1190, 600000, 5.0, 120, 1, 0.4, "relay");
tick();
log.hiddenPosts = quality().length;
ctx.document.hidden = false;
now += 2000; tick();
log.afterHiddenIsBaseline = quality().length;
process.stdout.write(JSON.stringify(log));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_page_posts_raw_quality_numbers_only_while_connected_and_visible(tmp_path) -> None:
    harness = tmp_path / "harness.js"
    harness.write_text(HARNESS, encoding="utf-8")
    out = subprocess.run(
        ["node", str(harness), str(PAGE)], capture_output=True, text=True, check=True, timeout=30
    ).stdout
    log = json.loads(out)
    # No picture, no numbers.
    assert log["beforeConnected"] == 0
    # The first reading only sets the baseline: rates need two readings.
    assert log["firstSampleIsBaseline"] == 0
    # 20 frames in 2 s, 10 of 200 packets lost, 4 s buffered over 20 frames.
    assert log["second"] == [
        {"rttMs": 400, "fps": 10, "lossPct": 5, "delayMs": 200, "kbps": 2000, "freezes": 1, "active": False, "relay": True}
    ]
    # A hidden page decodes nothing: it stays silent, and the reading after it
    # is a fresh baseline, never a rate measured across the hidden time.
    # A press or move in the page during the sample marks it as driven.
    assert log["thirdActive"] is True
    assert log["hiddenPosts"] == 2
    assert log["afterHiddenIsBaseline"] == 2
