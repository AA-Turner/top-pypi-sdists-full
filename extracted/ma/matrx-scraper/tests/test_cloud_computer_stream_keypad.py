"""The Cloud Computer screen page types keypad digits (2026-10-17).

Keypad keys arrived on the machine as keypad keysyms (KP_1, or KP_End with the
client's NumLock off; a Mac keyboard has no NumLock) and Chrome typed nothing.
The page now sends the digit or operator keysym for every keypad key. This runs
the real matrx-stream.js in Node against stand-ins for Selkies' globals.
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
const listeners = {};
const sent = [];
const el = () => ({ setAttribute() {}, addEventListener() {}, classList: { add() {} }, focus() {}, appendChild() {} });
const keyboard = { onkeydown: (k) => sent.push(["kd", k]), onkeyup: (k) => sent.push(["ku", k]), reset() {} };
const ctx = {
  URL, URLSearchParams,
  location: { search: "" },
  document: {
    referrer: "", body: el(), documentElement: el(),
    createElement: el, getElementById: el, addEventListener() {},
  },
  webrtc: { input: { keyboard, detach_context() {}, attach_context() {} }, sendDataChannelMessage() {} },
  signalling: {}, app: {},
  addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
  focus() {},
};
ctx.window = ctx; ctx.parent = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], "utf8"), ctx);
ctx.webrtc.ondatachannelopen();
const k = ctx.webrtc.input.keyboard;
function press(code, keysym) {
  for (const fn of listeners.keydown || []) fn({ code });
  k.onkeydown(keysym);
  for (const fn of listeners.keyup || []) fn({ code });
  k.onkeyup(keysym);
}
press("Numpad1", 0xffb1);          // NumLock on: KP_1
press("Numpad2", 0xff99);          // NumLock off (Windows): KP_Down
press("NumpadAdd", 0xffab);
press("NumpadEnter", 0xff8d);
press("Digit5", 0x35);             // a row digit is untouched
press("", 0xff9c);                 // no code seen: KP_End falls back to "1"
press("End", 0xff57);              // the real End key stays End
process.stdout.write(JSON.stringify(sent));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_keypad_keys_always_type_their_digit(tmp_path) -> None:
    harness = tmp_path / "harness.js"
    harness.write_text(HARNESS, encoding="utf-8")
    out = subprocess.run(
        ["node", str(harness), str(PAGE)], capture_output=True, text=True, check=True, timeout=30
    ).stdout
    sent = json.loads(out)
    downs = [k for kind, k in sent if kind == "kd"]
    ups = [k for kind, k in sent if kind == "ku"]
    assert downs == [0x31, 0x32, 0x2B, 0xFF0D, 0x35, 0x31, 0xFF57]
    assert ups == downs


RESET_HARNESS = r"""
const vm = require("vm");
const fs = require("fs");
const listeners = {};
const sent = [];
const held = new Set();
const el = () => ({ setAttribute() {}, addEventListener() {}, classList: { add() {} }, focus() {}, appendChild() {} });
// Guacamole's reset() releases every key it still holds through onkeyup.
const keyboard = {
  onkeydown: (k) => sent.push(["kd", k]), onkeyup: (k) => sent.push(["ku", k]),
  reset() { for (const k of [...held]) { held.delete(k); this.onkeyup(k); } },
};
const ctx = {
  URL, URLSearchParams,
  location: { search: "" },
  document: { referrer: "", body: el(), documentElement: el(), createElement: el, getElementById: el, addEventListener() {} },
  webrtc: { input: { keyboard, detach_context() {}, attach_context() {} }, sendDataChannelMessage() {} },
  signalling: {}, app: {},
  addEventListener(type, fn) { (listeners[type] = listeners[type] || []).push(fn); },
  focus() {},
};
ctx.window = ctx; ctx.parent = ctx;
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(process.argv[2], "utf8"), ctx);
ctx.webrtc.ondatachannelopen();
const k = ctx.webrtc.input.keyboard;
function down(code, keysym) {
  for (const fn of listeners.keydown || []) fn({ code });
  held.add(keysym);
  k.onkeydown(keysym);
}
down("ShiftLeft", 0xffe1);   // a modifier held...
down("Numpad1", 0xffb1);     // ...and the last real key a keypad key
for (const fn of listeners.blur || []) fn({});  // focus leaves: releaseAll -> reset
process.stdout.write(JSON.stringify(sent));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node is not installed")
def test_reset_releases_each_key_as_it_was_sent(tmp_path) -> None:
    """A reset releases every held key with the keysym it was pressed as.

    Before: releaseAll cleared the pressed-keysym record before Guacamole's
    reset fired the key-ups, so a held Shift was released as the keypad digit
    of the last key event ("1"), and the real Shift was never let go."""
    harness = tmp_path / "reset.js"
    harness.write_text(RESET_HARNESS, encoding="utf-8")
    out = subprocess.run(
        ["node", str(harness), str(PAGE)], capture_output=True, text=True, check=True, timeout=30
    ).stdout
    ups = sorted(k for kind, k in json.loads(out) if kind == "ku")
    assert ups == sorted([0xFFE1, 0x31])
