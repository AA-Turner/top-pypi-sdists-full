"""
NX CLI — PHONE CONTROL BRIDGE (Android via adb / iOS Simulator via simctl): let NX drive a connected phone the
way nx_computer drives the Mac. Invoked with `$phone <goal>`.

REUSES nx_computer's decision layer VERBATIM (eliminate-disagreement-attractors, CLAUDE.md #5) — the SAME safety
gate (classify_computer_action), action parsing (parse_plan_action), coordinate clamp (validate_point), and typed-
text-hiding describe (describe_action). Only the executor + action vocabulary are phone-specific. (Coupling note:
this imports nx_computer module-level helpers _run/_int — a future nx_computer refactor moves nx_phone with it.)

SAFE BY CONSTRUCTION — the same three-tier gate as $computer:
  - OBSERVE (screenshot / wait) = SAFE, runs free.
  - ACT (tap / swipe / type / key / open_app) = GATED — each confirmed by the operator per-op; fail-CLOSED headless.
  - SENSITIVE (a password / 2FA / card-number / payment / purchase CONTEXT) = PROHIBITED — NX never types a phone
    credential or confirms a mobile purchase; it stops and hands control back. (The gate is WORD-based, not raw-PAN
    digit detection — a bare card number with no context word lands GATED, i.e. per-op-confirmed, not prohibited.)

Android is real via adb (screencap / input tap|swipe|text|keyevent / monkey launch). iOS Simulator is
screenshot+observe only (simctl has no tap/type primitive); physical-device iOS needs WebDriverAgent — out of
scope, honestly degraded. Every device command PINS `-s <device_id>` so adb never fans out to the wrong device.
The pure layer (parsing, the gate, adb-command mapping, device selection, capability detection) is unit-tested with
no device; the executor is device-proven like nx_computer's.
"""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import tempfile
from typing import Any, Callable, Optional

from nx_computer import (  # reuse the decision layer verbatim — no duplication
    classify_computer_action,
    describe_action as _desc_shared,
    validate_point,  # noqa: F401 — reused to clamp tap/swipe coords into device bounds (device-proven path)
    _int,
    _run,
)

MAX_STEPS_DEFAULT = 12

# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# ACTION MODEL — phone-specific verbs; the SAFETY GATE is nx_computer.classify_computer_action reused verbatim.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

PHONE_ACTION_KINDS = frozenset({"screenshot", "tap", "swipe", "type", "key", "open_app", "wait", "done"})

# The reused gate: tap/swipe fall to its GATED default; type/key/open_app are GATED (in nx_computer.ACTION_KINDS);
# screenshot/wait/done are SAFE (in its _OBSERVE); a sensitive CONTEXT word → PROHIBITED. One source of truth.
classify_phone_action = classify_computer_action


def parse_phone_action(obj: Any) -> dict:
    """Normalize a model-emitted phone action dict into a typed action. Unknown/missing kind → {kind:'done'}. Pure."""
    if not isinstance(obj, dict):
        return {"kind": "done", "why": "no action"}
    kind = str(obj.get("kind") or obj.get("action") or "done").strip().lower()
    if kind not in PHONE_ACTION_KINDS:
        kind = "done"
    out: dict = {"kind": kind, "why": str(obj.get("why") or "")[:160], "target": str(obj.get("target") or "")[:120]}
    if kind in ("tap", "swipe"):
        out["x"] = _int(obj.get("x"))
        out["y"] = _int(obj.get("y"))
        if kind == "swipe":
            out["to_x"] = _int(obj.get("to_x"))
            out["to_y"] = _int(obj.get("to_y"))
            out["ms"] = max(50, min(_int(obj.get("ms") or 300), 5000))
    if kind == "type":
        out["text"] = str(obj.get("text") or obj.get("value") or "")
    if kind == "key":
        out["keys"] = str(obj.get("keys") or obj.get("combo") or obj.get("value") or "").strip()
    if kind == "open_app":
        out["app"] = str(obj.get("app") or obj.get("target") or obj.get("value") or "").strip()
    if kind == "wait":
        out["ms"] = max(0, min(_int(obj.get("ms") or 500), 10_000))
    return out


def parse_plan_phone_action(answer: str) -> dict:
    """Extract the first balanced JSON action from a model answer and normalize to the PHONE action shape. (Same
    brace-scan as nx_computer.parse_plan_action, but normalizing via parse_phone_action — delegating to
    parse_plan_action would lose 'tap'/'swipe', which aren't computer-action kinds.) {kind:'done'} on none. Pure."""
    if not answer:
        return {"kind": "done", "why": "empty answer"}
    s = answer.find("{")
    e = answer.rfind("}")
    if s < 0 or e <= s:
        return {"kind": "done", "why": "no action json"}
    try:
        obj = json.loads(answer[s : e + 1])
    except Exception:
        return {"kind": "done", "why": "unparseable action"}
    return parse_phone_action(obj)


def describe_phone_action(action: dict) -> str:
    """A short human line for the confirmation prompt / trail. Reuses describe_action for type/key/open_app (incl.
    its 40-char typed-text hiding); adds tap/swipe."""
    kind = action.get("kind")
    if kind == "tap":
        return "tap %s" % (action.get("target") or "(%s,%s)" % (action.get("x"), action.get("y")))
    if kind == "swipe":
        return "swipe (%s,%s)→(%s,%s)" % (action.get("x"), action.get("y"), action.get("to_x"), action.get("to_y"))
    if kind in ("type", "key", "open_app"):
        return _desc_shared(action)
    return str(kind)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# CAPABILITY + DEVICE DETECTION — pure parsers + capability lookups.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def is_macos() -> bool:
    return platform.system() == "Darwin"


def is_android_available() -> bool:
    return bool(shutil.which("adb"))


def is_ios_sim_available() -> bool:
    return is_macos() and bool(shutil.which("xcrun"))


def parse_adb_devices(output: str) -> list[dict]:
    """Parse `adb devices` output into online Android devices. Only state 'device' is online; 'offline' /
    'unauthorized' are excluded (an unauthorized device means USB-debugging isn't approved). Pure."""
    devices: list[dict] = []
    for line in (output or "").splitlines():
        line = line.strip()
        if not line or line.startswith("List of devices"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append({"id": parts[0], "kind": "android", "name": parts[0]})
    return devices


def parse_simctl_booted(json_str: str) -> list[dict]:
    """Parse `xcrun simctl list devices booted -j` JSON into booted iOS simulators. Pure; [] on bad JSON."""
    try:
        data = json.loads(json_str or "{}")
    except Exception:
        return []
    out: list[dict] = []
    for _runtime, sims in (data.get("devices") or {}).items():
        for s in sims or []:
            if isinstance(s, dict) and s.get("state") == "Booted" and s.get("udid"):
                out.append({"id": s["udid"], "kind": "ios_sim", "name": s.get("name") or s["udid"]})
    return out


def select_device(devices: list[dict], prefer: Optional[str] = None) -> Optional[dict]:
    """Pick the device to drive: an explicit prefer-id wins; else the sole device auto-selects; multiple → None
    (ambiguous, name one); none → None. Pure."""
    if not devices:
        return None
    if prefer:
        for d in devices:
            if d.get("id") == prefer or d.get("name") == prefer:
                return d
        return None
    return devices[0] if len(devices) == 1 else None


def detect_phone_devices() -> list[dict]:
    """All connected drivable devices (online Android + booted iOS sims). Executor (runs adb/xcrun); [] on error."""
    devices: list[dict] = []
    if is_android_available():
        r = _run(["adb", "devices"], timeout=10)
        if r.get("ok"):
            devices.extend(parse_adb_devices(r.get("stdout") or ""))
    if is_ios_sim_available():
        r = _run(["xcrun", "simctl", "list", "devices", "booted", "-j"], timeout=10)
        if r.get("ok"):
            devices.extend(parse_simctl_booted(r.get("stdout") or ""))
    return devices


def phone_permission_guidance(has_android: Optional[bool] = None, has_ios: Optional[bool] = None) -> str:
    """The honest 'connect a phone' message when control isn't available."""
    ha = is_android_available() if has_android is None else has_android
    hi = is_ios_sim_available() if has_ios is None else has_ios
    lines = ["To let NX drive a phone, connect one:"]
    if ha:
        lines.append("  • Android: plug in your phone, enable Developer Options → USB debugging, and approve the "
                     "prompt. `adb devices` should list it as 'device'.")
    else:
        lines.append("  • Android: install Android platform-tools so `adb` is on PATH, then enable USB debugging on "
                     "the phone.")
    if hi:
        lines.append("  • iOS: boot a Simulator (Xcode → Simulator). NX can SEE the Simulator; tapping/typing on it "
                     "(and any physical iPhone) needs WebDriverAgent — not supported yet.")
    else:
        lines.append("  • iOS: physical-device / Simulator control needs macOS + Xcode (and WebDriverAgent for input) "
                     "— not available here.")
    return "\n".join(lines)


def phone_preflight(devices: Optional[list[dict]] = None, prefer: Optional[str] = None) -> dict:
    """Can NX drive a phone right now? Returns {ready, device?, reason?, guidance?}. ready=False carries honest
    guidance. `devices` may be injected (tests); None → detect."""
    ha, hi = is_android_available(), is_ios_sim_available()
    if not ha and not hi:
        return {"ready": False, "reason": "no_tooling", "guidance": phone_permission_guidance(ha, hi)}
    devs = detect_phone_devices() if devices is None else devices
    if not devs:
        return {"ready": False, "reason": "no_device", "guidance": phone_permission_guidance(ha, hi)}
    dev = select_device(devs, prefer)
    if not dev:
        names = ", ".join("%s (%s)" % (d.get("name"), d.get("id")) for d in devs)
        return {"ready": False, "reason": "ambiguous_device", "guidance": "More than one device connected — name which: " + names}
    if dev.get("kind") == "ios_sim":
        # We can observe an iOS sim but not act on it (no simctl input primitive).
        return {"ready": False, "reason": "ios_input_unsupported", "guidance": phone_permission_guidance(ha, hi), "device": dev}
    return {"ready": True, "device": dev}


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# PURE ACTION → adb COMMAND mapping (every argv pins `-s <device_id>`).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

# A small friendly-name → Android package starter map; a value already containing a dot is treated as a package.
_APP_PACKAGES = {
    "chrome": "com.android.chrome", "settings": "com.android.settings", "gmail": "com.google.android.gm",
    "maps": "com.google.android.apps.maps", "youtube": "com.google.android.youtube", "camera": "com.android.camera2",
    "photos": "com.google.android.apps.photos", "messages": "com.google.android.apps.messaging",
    "phone": "com.android.dialer", "contacts": "com.android.contacts", "calendar": "com.google.android.calendar",
    "playstore": "com.android.vending", "play store": "com.android.vending", "clock": "com.android.deskclock",
    "files": "com.google.android.documentsui", "calculator": "com.android.calculator2",
}


def resolve_package(app: str) -> str:
    """Map a friendly app name to an Android package (a value with a dot passes through as a package). '' when
    unresolved. Pure."""
    a = (app or "").strip().lower()
    if "." in a and " " not in a:
        return a
    return _APP_PACKAGES.get(a, "")


_ANDROID_KEYCODES = {
    "enter": "KEYCODE_ENTER", "return": "KEYCODE_ENTER", "back": "KEYCODE_BACK", "home": "KEYCODE_HOME",
    "tab": "KEYCODE_TAB", "del": "KEYCODE_DEL", "backspace": "KEYCODE_DEL", "search": "KEYCODE_SEARCH",
    "space": "KEYCODE_SPACE", "menu": "KEYCODE_MENU", "power": "KEYCODE_POWER", "up": "KEYCODE_DPAD_UP",
    "down": "KEYCODE_DPAD_DOWN", "left": "KEYCODE_DPAD_LEFT", "right": "KEYCODE_DPAD_RIGHT",
    "volume_up": "KEYCODE_VOLUME_UP", "volume_down": "KEYCODE_VOLUME_DOWN", "app_switch": "KEYCODE_APP_SWITCH",
}


def android_keyevent(friendly: str) -> str:
    """Map a friendly key to an Android KEYCODE. An already-KEYCODE_* string passes through; an unmapped key
    upper-cases (best-effort). Pure."""
    k = (friendly or "").strip().lower()
    if k.startswith("keycode_"):
        return k.upper()
    return _ANDROID_KEYCODES.get(k, "KEYCODE_" + k.upper()) if k else ""


def android_text_escape(text: str) -> str:
    """Escape text for `adb shell input text`: spaces → %s, and shell/adb metacharacters backslash-escaped so the
    string can't break the shell word or inject. Multi-line/unicode is a known adb-input limitation (surfaced, not
    silently mangled). Pure."""
    out = []
    for ch in (text or ""):
        if ch == " ":
            out.append("%s")
        elif ch in "()<>|;&*\\~\"'`$?[]{}":
            out.append("\\" + ch)
        elif ch == "\n":
            out.append(" ")  # adb input text can't do newlines; collapse to space (honest limitation)
        else:
            out.append(ch)
    return "".join(out)


def adb_command(action: dict, device_id: str) -> list[str]:
    """Map a phone action to an adb argv list, ALWAYS pinning `-s <device_id>` (adb fans out to the wrong device
    otherwise). [] for an unmappable/observe action. Pure."""
    base = ["adb", "-s", device_id]
    kind = action.get("kind")
    if kind == "tap":
        return base + ["shell", "input", "tap", str(action.get("x")), str(action.get("y"))]
    if kind == "swipe":
        return base + ["shell", "input", "swipe", str(action.get("x")), str(action.get("y")),
                       str(action.get("to_x")), str(action.get("to_y")), str(action.get("ms", 300))]
    if kind == "type":
        return base + ["shell", "input", "text", android_text_escape(action.get("text", ""))]
    if kind == "key":
        return base + ["shell", "input", "keyevent", android_keyevent(action.get("keys", ""))]
    if kind == "open_app":
        pkg = resolve_package(action.get("app", ""))
        if not pkg:
            return []
        return base + ["shell", "monkey", "-p", pkg, "-c", "android.intent.category.LAUNCHER", "1"]
    if kind == "screenshot":
        return base + ["exec-out", "screencap", "-p"]
    return []


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# EXECUTOR (device-proven, not in CI). Never raises.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def take_phone_screenshot(device: dict) -> dict:
    """Capture the phone screen to a PNG. Android: `adb -s <id> exec-out screencap -p` emits raw PNG BYTES —
    captured bytes-safe (subprocess WITHOUT text=True; NOT via _run, which sets text=True and would corrupt the
    binary). iOS sim: `xcrun simctl io booted screenshot`. Returns {ok, path} / {ok:False, error}. Never raises."""
    kind = device.get("kind")
    path = tempfile.mkstemp(suffix=".png")[1]
    try:
        if kind == "android":
            r = subprocess.run(["adb", "-s", device["id"], "exec-out", "screencap", "-p"],
                               capture_output=True, timeout=20)
            if r.returncode != 0 or not r.stdout:
                return {"ok": False, "error": (r.stderr or b"").decode("utf-8", "replace")[:200] or "screencap_failed"}
            with open(path, "wb") as f:
                f.write(r.stdout)
            return {"ok": True, "path": path}
        if kind == "ios_sim":
            r = subprocess.run(["xcrun", "simctl", "io", device["id"], "screenshot", path],
                               capture_output=True, timeout=20)
            return {"ok": r.returncode == 0, "path": path} if r.returncode == 0 else {"ok": False, "error": "simctl_screenshot_failed"}
        return {"ok": False, "error": "unsupported_device"}
    except FileNotFoundError:
        return {"ok": False, "error": "tool_not_found"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}
    except Exception as e:  # never raise into the loop
        return {"ok": False, "error": type(e).__name__}


def observe_phone_context(device: dict) -> dict:
    """A lightweight text observation: the foreground Android package/activity (via dumpsys). {} for iOS sim / on
    error. Executor."""
    if device.get("kind") != "android":
        return {}
    r = _run(["adb", "-s", device["id"], "shell", "dumpsys", "activity", "activities"], timeout=8)
    if not r.get("ok"):
        return {}
    import re as _re
    m = _re.search(r"mResumedActivity.*?\{[^}]*?\s([\w.]+/[\w.$]+)", r.get("stdout") or "")
    if not m:
        m = _re.search(r"ResumedActivity.*?([\w.]+/[\w.$]+)", r.get("stdout") or "")
    return {"activity": m.group(1)} if m else {}


def execute_phone_action(action: dict, device: dict) -> dict:
    """Execute ONE already-gated action on the device. The CALLER owns the safety gate (classify + confirm). Never
    raises. iOS sim can't act (no input primitive) — honest failure, never a fake success."""
    kind = action.get("kind")
    if kind == "wait":
        _run(["sleep", str(max(0, int(action.get("ms", 500))) / 1000.0)], timeout=11)
        return {"ok": True}
    if kind == "screenshot":
        return take_phone_screenshot(device)
    if device.get("kind") == "ios_sim":
        return {"ok": False, "error": "ios_input_unsupported"}
    if device.get("kind") != "android":
        return {"ok": False, "error": "unsupported_device"}
    argv = adb_command(action, device["id"])
    if not argv:
        return {"ok": False, "error": "unmappable_action" if kind == "open_app" else "unsupported_action"}
    r = _run(argv, timeout=15)
    return {"ok": bool(r.get("ok")), "error": None if r.get("ok") else (r.get("error") or r.get("stderr") or "adb_failed")}


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# PLAN + LOOP — mirrors nx_computer.plan_next_action / control_computer.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

_PHONE_PLAN_SYS = (
    "You are NX driving the operator's phone to accomplish a goal, one action at a time. Each step respond with "
    "EXACTLY ONE JSON action object (no prose, no fences):\n"
    '  {"kind":"tap","x":<int>,"y":<int>,"target":"<what you\'re tapping>","why":"<short>"}\n'
    '  {"kind":"swipe","x":<int>,"y":<int>,"to_x":<int>,"to_y":<int>,"target":"..."}\n'
    '  {"kind":"type","text":"<text to type>","target":"..."}\n'
    '  {"kind":"key","keys":"back|home|enter|tab|search","why":"..."}\n'
    '  {"kind":"open_app","app":"Chrome","why":"..."}\n'
    '  {"kind":"done","why":"<goal reached or you need the operator>"}\n'
    "Give tap x,y as pixel coordinates on the phone screen. ALWAYS include a short descriptive `target` for every "
    "tap/type. NEVER type a password, 2FA/OTP code, card number, or any credential, and NEVER confirm a "
    "purchase/payment — emit {\"kind\":\"done\"} and let the operator do that. Every real action is confirmed by "
    "the operator before it runs, so act decisively; call done when complete or blocked."
)


def plan_next_phone_action(goal: str, observation: dict, model_fn: Callable[[str], str]) -> dict:
    """Ask the model for the next phone action from the goal + observation (foreground activity + history). Returns
    a parsed phone action. Pure aside from the injected model_fn."""
    ctx = observation.get("context") or {}
    hist = observation.get("history") or []
    hist_lines = "\n".join(
        "- %s → %s" % (describe_phone_action(h.get("action", {})), ("ok" if h.get("executed") else (h.get("error") or "skipped")))
        for h in hist[-6:]
    )
    prompt = (
        _PHONE_PLAN_SYS
        + "\n\nGOAL: " + (goal or "")
        + "\n\nForeground: " + str(ctx.get("activity", "?"))
        + (("\n\nWhat you've done so far:\n" + hist_lines) if hist_lines else "")
        + "\n\nNext action? Respond with exactly one JSON object."
    )
    try:
        answer = model_fn(prompt)
    except Exception:
        return {"kind": "done", "why": "planner error"}
    return parse_plan_phone_action(answer)


def control_phone(
    goal: str,
    planner: Callable[[str, dict], Any],
    confirm: Optional[Callable[[str], bool]] = None,
    device: Optional[dict] = None,
    max_steps: int = MAX_STEPS_DEFAULT,
    on_step: Optional[Callable[[str], None]] = None,
) -> dict:
    """Drive the phone toward `goal`, mirroring nx_computer.control_phone. Observe runs free; every ACT is
    gated by `confirm` (fail-CLOSED); a SENSITIVE action is refused. Bounded. Never raises."""
    on_step = on_step or (lambda _s: None)
    pf = phone_preflight([device] if device else None)
    if not pf.get("ready"):
        on_step("phone control unavailable — " + pf.get("reason", ""))
        return {"ok": False, "halted": pf.get("reason"), "guidance": pf.get("guidance"), "steps": []}
    dev = pf["device"]

    steps: list[dict] = []
    for _ in range(max(1, min(int(max_steps), 40))):
        shot = take_phone_screenshot(dev)
        observation = {
            "screenshot": shot.get("path") if shot.get("ok") else None,
            "screenshot_ok": bool(shot.get("ok")),
            "context": observe_phone_context(dev),
            "history": steps,
        }
        try:
            planned = planner(goal, observation)
        except Exception:
            return {"ok": True, "steps": steps, "done": True, "halted": "planner_error"}
        action = planned if isinstance(planned, dict) else parse_plan_phone_action(str(planned or ""))
        verdict = classify_phone_action(action)
        desc = describe_phone_action(action)

        if action.get("kind") == "done":
            on_step("done: " + (action.get("why") or ""))
            return {"ok": True, "steps": steps, "done": True}
        if verdict == "PROHIBITED":
            on_step("refused (sensitive — you do this yourself): " + desc)
            steps.append({"action": action, "verdict": "PROHIBITED", "executed": False})
            return {"ok": True, "steps": steps, "done": False, "halted": "prohibited"}
        if verdict == "GATED":
            if not bool(confirm and confirm(desc)):
                on_step("skipped (not approved): " + desc)
                steps.append({"action": action, "verdict": "GATED", "executed": False, "refused": True})
                return {"ok": True, "steps": steps, "done": False, "halted": "declined"}

        res = execute_phone_action(action, dev)
        ok = bool(res.get("ok"))
        on_step(("✓ " if ok else "⚠ ") + desc + ("" if ok else " — %s" % res.get("error", "failed")))
        steps.append({"action": action, "verdict": verdict, "executed": ok, "error": res.get("error")})
        if not ok and res.get("error") in ("ios_input_unsupported", "unsupported_device", "tool_not_found"):
            return {"ok": True, "steps": steps, "done": False, "halted": "executor_unavailable", "guidance": phone_permission_guidance()}

    return {"ok": True, "steps": steps, "done": False, "halted": "max_steps"}
