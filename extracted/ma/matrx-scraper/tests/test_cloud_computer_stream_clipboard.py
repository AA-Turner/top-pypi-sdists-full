"""Copy, cut and paste cross between the person's computer and the Cloud Computer (2026-11-19).

The owner's shortcuts did nothing. Selkies 1.6.2's own page (read from the
pinned image) sends the person's clipboard only on window focus and writes the
machine's clipboard to theirs only if permission was already granted at page
load, and a Mac's Command key reached the Linux machine as Super. The page now
does the hand-off on the shortcut itself. This runs the real matrx-stream.js in
Node against stand-ins for Selkies' globals.
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
const scenario = JSON.parse(process.argv[3]);
const listeners = {};
const wire = [];          // everything that reached the machine, in order
const timers = [];
const el = () => ({ setAttribute() {}, addEventListener() {}, classList: { add() {} }, focus() {}, appendChild() {} });
const keyboard = { onkeydown: (k) => wire.push("kd," + k), onkeyup: (k) => wire.push("ku," + k), reset() {} };
let local = scenario.local;           // the person's clipboard
const written = [];
const clipboard = {
  readText: () => (scenario.denyRead ? Promise.reject(new Error("denied")) : Promise.resolve(local)),
  writeText: (t) => (scenario.denyWrite ? Promise.reject(new Error("denied")) : (written.push(t), Promise.resolve())),
};
const ctx = {
  URL, URLSearchParams, Promise, Error,
  navigator: { platform: scenario.platform, clipboard },
  stringToBase64: (t) => Buffer.from(t, "utf8").toString("base64"),
  location: { search: "" },
  document: {
    referrer: "", body: el(), documentElement: el(),
    createElement: el, getElementById: el, addEventListener() {},
  },
  webrtc: { input: { keyboard, detach_context() {}, attach_context() {} }, sendDataChannelMessage: (m) => wire.push(m) },
  signalling: {}, app: {},
  addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
  setTimeout(fn) { timers.push(fn); },
  focus() {},
};
ctx.window = ctx; ctx.parent = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], "utf8"), ctx);
ctx.webrtc.ondatachannelopen();
const k = ctx.webrtc.input.keyboard;
const settle = () => new Promise((r) => setImmediate(r));
async function run() {
  for (const step of scenario.steps) {
    if (step[0] === "down") k.onkeydown(step[1]);
    else if (step[0] === "up") k.onkeyup(step[1]);
    else if (step[0] === "blur") (listeners.blur || []).forEach((fn) => fn());
    else if (step[0] === "machine") ctx.webrtc.onclipboardcontent(step[1]);
    else if (step[0] === "rightclick") (listeners.pointerdown || []).forEach((fn) => fn({ button: 2 }));
    else if (step[0] === "timers") { await settle(); timers.splice(0).forEach((fn) => fn()); }
    await settle();
  }
  const posts = ctx.__matrxStreamPosts.filter((m) => m.state === "clipboard").map((m) => [m.way, m.ok]);
  process.stdout.write(JSON.stringify({ wire: wire.filter((m) => m !== "kr"), written, posts }));
}
run();
"""

CTRL, SHIFT, CMD = 0xFFE3, 0xFFE1, 0xFFE7
V, C, A = 0x76, 0x63, 0x61
HELLO = "aGVsbG8g4pyT"  # base64 of "hello ✓"


def _run(tmp_path, **scenario) -> dict:
    harness = tmp_path / "harness.js"
    harness.write_text(HARNESS, encoding="utf-8")
    scenario.setdefault("platform", "Win32")
    scenario.setdefault("local", "hello ✓")
    out = subprocess.run(
        ["node", str(harness), str(PAGE), json.dumps(scenario)],
        capture_output=True, text=True, check=True, timeout=30,
    ).stdout
    return json.loads(out)


pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")


def test_paste_sends_the_persons_clipboard_before_the_keys(tmp_path) -> None:
    log = _run(tmp_path, steps=[["down", CTRL], ["down", V], ["up", V], ["timers"], ["up", CTRL]])
    # The clipboard reaches the machine first, then V, while Control is still held.
    assert log["wire"] == [f"kd,{CTRL}", f"cw,{HELLO}", f"kd,{V}", f"ku,{V}", f"ku,{CTRL}"]
    assert log["posts"] == []


def test_paste_after_a_permission_prompt_resends_the_whole_chord(tmp_path) -> None:
    # The browser's prompt blurs the page, which releases every key: the page
    # presses Control+V itself once the clipboard is on the machine.
    log = _run(tmp_path, steps=[["down", CTRL], ["down", V], ["blur"], ["timers"]])
    assert log["wire"] == [f"kd,{CTRL}", f"cw,{HELLO}", f"kd,{CTRL}", f"kd,{V}", f"ku,{V}", f"ku,{CTRL}"]


def test_a_refused_clipboard_still_pastes_and_tells_the_app(tmp_path) -> None:
    log = _run(tmp_path, denyRead=True, steps=[["down", CTRL], ["down", V], ["up", V], ["timers"], ["up", CTRL]])
    # The keys still go (the machine pastes what it has); the app hears why.
    assert log["wire"] == [f"kd,{CTRL}", f"kd,{V}", f"ku,{V}", f"ku,{CTRL}"]
    assert log["posts"] == [["in", False]]


def test_copy_asks_the_machine_and_writes_what_comes_back(tmp_path) -> None:
    log = _run(tmp_path, steps=[["down", CTRL], ["down", C], ["up", C], ["up", CTRL], ["timers"], ["machine", "from the machine"]])
    assert log["wire"] == [f"kd,{CTRL}", f"kd,{C}", f"ku,{C}", f"ku,{CTRL}", "cr"]
    assert log["written"] == ["from the machine"]
    assert log["posts"] == []


def test_a_refused_write_tells_the_app_once(tmp_path) -> None:
    log = _run(tmp_path, denyWrite=True, steps=[["machine", "a"], ["machine", "b"]])
    assert log["written"] == []
    assert log["posts"] == [["out", False]]


def test_on_a_mac_command_is_the_machines_control(tmp_path) -> None:
    log = _run(tmp_path, platform="MacIntel", steps=[["down", CMD], ["down", A], ["up", A], ["up", CMD]])
    assert log["wire"] == [f"kd,{CTRL}", f"kd,{A}", f"ku,{A}", f"ku,{CTRL}"]
    # Command+V is a paste like any other.
    log = _run(tmp_path, platform="MacIntel", steps=[["down", CMD], ["down", V], ["up", V], ["timers"], ["up", CMD]])
    assert log["wire"] == [f"kd,{CTRL}", f"cw,{HELLO}", f"kd,{V}", f"ku,{V}", f"ku,{CTRL}"]


def test_off_a_mac_the_super_key_is_left_alone(tmp_path) -> None:
    log = _run(tmp_path, steps=[["down", 0xFFEB], ["up", 0xFFEB]])
    assert log["wire"] == [f"kd,{0xFFEB}", f"ku,{0xFFEB}"]


def test_a_plain_v_is_just_a_letter_and_shift_paste_keeps_shift(tmp_path) -> None:
    log = _run(tmp_path, steps=[["down", V], ["up", V]])
    assert log["wire"] == [f"kd,{V}", f"ku,{V}"]
    # Control+Shift+V (a terminal's paste) after a prompt: Shift is pressed again too.
    log = _run(tmp_path, steps=[["down", CTRL], ["down", SHIFT], ["down", 0x56], ["blur"], ["timers"]])
    assert log["wire"][-6:] == [f"kd,{CTRL}", f"kd,{SHIFT}", f"kd,{0x56}", f"ku,{0x56}", f"ku,{SHIFT}", f"ku,{CTRL}"]


def test_a_right_click_brings_the_machines_clipboard_up_to_date(tmp_path) -> None:
    log = _run(tmp_path, steps=[["rightclick"]])
    assert log["wire"] == [f"cw,{HELLO}"]
