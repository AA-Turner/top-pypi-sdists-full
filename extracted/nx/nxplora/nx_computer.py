"""
NX CLI — COMPUTER USE (control_computer): let NX drive the LOCAL desktop — click, type, open apps, read the
screen — the way Codex Computer Use / Claude computer-use does, but for NX. NX runs ON the operator's machine, so
this is REAL local control (not a sandbox hand-off).

SAFE BY CONSTRUCTION — the same three-tier gate as /browse (nx_browse.classify_browse_action):
  - OBSERVE (screenshot / move / scroll / wait) = SAFE, runs free — no outward effect, fully reversible.
  - ACT (click / type / key / drag / open_app) = GATED — each is confirmed per-op by the operator (or under an
    explicit scoped "approve-all" session), exactly like a destructive tool call. Fails CLOSED headless.
  - SENSITIVE (typing into a password/credential field, a payment/purchase confirmation) = PROHIBITED — NX never
    types a credential or confirms a charge on the operator's behalf; it stops and hands control back.

The pure decision layer here (action parsing, the safety gate, coordinate bounds, permission guidance, plan
parsing) is unit-tested with no GUI. The EXECUTOR (screencapture / cliclick / osascript) + the screenshot→plan→act
loop are capability-detected + proven on the operator's Mac (like nx_browse's Playwright path — not exercised in
CI, real on device). On a machine without the tools / permissions, every entry point degrades to an honest
"grant Accessibility + Screen Recording" / "install cliclick" message — it never fakes an action.
"""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
from typing import Any, Callable, Optional


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# ACTION MODEL — the typed shape the model emits each step (mirrors nx_browse's action shape).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

# Every action the operator's computer can be driven with. `done` ends the loop.
ACTION_KINDS = frozenset({
    "screenshot", "move", "scroll", "wait",            # OBSERVE (safe)
    "click", "double_click", "right_click", "drag", "type", "key", "open_app",  # ACT (gated)
    "done",
})

# Observe actions have no outward effect — they run without a per-op gate.
_OBSERVE = frozenset({"screenshot", "move", "scroll", "wait", "done"})

# Signals in an action's target/why/value that mark it SENSITIVE → PROHIBITED (never auto-performed).
_SENSITIVE_RE = re.compile(
    r"\b(password|passcode|passphrase|credential|secret\s*key|2fa|otp|one.?time.?code|"
    r"card\s*number|cvv|cvc|security\s*code|payment|purchase|buy\s*now|place\s*order|checkout|confirm\s*(charge|payment|order)|"
    r"wire\s*transfer|social\s*security|ssn|seed\s*phrase|private\s*key)\b",
    re.I,
)


def parse_computer_action(obj: Any) -> dict:
    """Normalize a model-emitted action dict into a typed action. Unknown/missing kind → {kind:'done'} (safe stop).
    Coordinates coerce to int; text/target/why coerce to str. Pure."""
    if not isinstance(obj, dict):
        return {"kind": "done", "why": "no action"}
    kind = str(obj.get("kind") or obj.get("action") or "done").strip().lower()
    if kind not in ACTION_KINDS:
        kind = "done"
    out: dict = {
        "kind": kind,
        "why": str(obj.get("why") or "")[:160],
    }
    if kind in ("click", "double_click", "right_click", "move", "drag"):
        out["x"] = _int(obj.get("x"))
        out["y"] = _int(obj.get("y"))
        if kind == "drag":
            out["to_x"] = _int(obj.get("to_x"))
            out["to_y"] = _int(obj.get("to_y"))
    if kind == "type":
        out["text"] = str(obj.get("text") or obj.get("value") or "")
    if kind == "key":
        out["keys"] = str(obj.get("keys") or obj.get("combo") or obj.get("value") or "").strip()
    if kind == "scroll":
        out["dx"] = _int(obj.get("dx"))
        out["dy"] = _int(obj.get("dy"))
    if kind == "open_app":
        out["app"] = str(obj.get("app") or obj.get("target") or obj.get("value") or "").strip()
    if kind == "wait":
        out["ms"] = max(0, min(_int(obj.get("ms") or 500), 10_000))
    out["target"] = str(obj.get("target") or "")[:120]
    return out


def parse_plan_action(answer: str) -> dict:
    """Extract the first balanced JSON action object out of a model answer (tolerant of stray prose). Falls back to
    {kind:'done'} when there's no parseable action. Pure."""
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
    return parse_computer_action(obj)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# SAFETY GATE — observe = SAFE, act = GATED, credential/payment = PROHIBITED (mirrors nx_browse).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def classify_computer_action(action: dict) -> str:
    """Return 'SAFE' | 'GATED' | 'PROHIBITED' for an action. A SENSITIVE target (password/payment/etc.) is
    PROHIBITED regardless of kind — NX never types a credential or confirms a charge. Observe actions are SAFE;
    every real action is GATED (per-op operator confirmation). Pure."""
    kind = str(action.get("kind") or "done")
    haystack = " ".join(str(action.get(k) or "") for k in ("target", "why", "text", "app"))
    if _SENSITIVE_RE.search(haystack):
        return "PROHIBITED"
    if kind in _OBSERVE:
        return "SAFE"
    if kind in ACTION_KINDS:
        return "GATED"
    return "GATED"  # unknown → gate (never free-run something unclassified)


def describe_action(action: dict) -> str:
    """A short human line for the confirmation prompt / trail — never includes typed secret text verbatim beyond a
    short preview (and typing is gated anyway)."""
    kind = action.get("kind")
    if kind in ("click", "double_click", "right_click", "move"):
        t = action.get("target") or f"({action.get('x')},{action.get('y')})"
        return f"{kind.replace('_', ' ')} {t}".strip()
    if kind == "drag":
        return f"drag ({action.get('x')},{action.get('y')})→({action.get('to_x')},{action.get('to_y')})"
    if kind == "type":
        preview = (action.get("text") or "")[:40]
        return f'type "{preview}{"…" if len(action.get("text") or "") > 40 else ""}"'
    if kind == "key":
        return f"press {action.get('keys')}"
    if kind == "open_app":
        return f"open {action.get('app')}"
    if kind == "scroll":
        return f"scroll ({action.get('dx')},{action.get('dy')})"
    return str(kind)


def validate_point(x: Any, y: Any, screen_w: int, screen_h: int) -> Optional[tuple[int, int]]:
    """Clamp a click point to the screen bounds; None when the coords aren't finite numbers. Pure — guards a
    fat-fingered model coordinate from clicking off-screen or at a negative offset."""
    xi, yi = _int(x, None), _int(y, None)
    if xi is None or yi is None:
        return None
    return (max(0, min(xi, max(0, screen_w - 1))), max(0, min(yi, max(0, screen_h - 1))))


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# CAPABILITY + PERMISSION PREFLIGHT (macOS) — detect the executor + guide the Accessibility / Screen Recording grants.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def is_macos() -> bool:
    return platform.system() == "Darwin"


def _pynput_available() -> bool:
    """pynput ships WITH nx (a pip dependency) — precise mouse/keyboard control with NO Homebrew. Soft-imported so a
    lean/headless install still boots."""
    try:
        import pynput  # noqa: F401
        return True
    except Exception:
        return False


def detect_executor() -> dict:
    """Which local-control backend is available, best first. `pynput` (bundled pip dep) gives precise click/type with
    no Homebrew; `cliclick` (brew) is honored if the operator has it; `osascript` (System Events) is the always-
    present macOS fallback; `screencapture` for screenshots. Returns {os, screenshot, click, backend}."""
    mac = is_macos()
    has_pynput = _pynput_available()
    has_cliclick = bool(shutil.which("cliclick"))
    has_osascript = bool(shutil.which("osascript"))
    has_screencap = bool(shutil.which("screencapture"))
    backend = ("pynput" if has_pynput else
               ("cliclick" if has_cliclick else ("osascript" if has_osascript else None)))
    return {
        "os": platform.system(),
        "screenshot": has_screencap,
        "click": bool(backend),
        "backend": backend,
        "macos": mac,
    }


def permission_guidance(cap: Optional[dict] = None) -> str:
    """The honest 'grant these' message when control isn't available yet — the exact macOS grants a computer-use
    agent needs (Accessibility to click/type, Screen Recording to see the screen), plus the optional cliclick
    install for precise control. Mirrors what the operator sees in System Settings."""
    cap = cap or detect_executor()
    if not cap.get("macos"):
        return ("Computer control currently supports macOS. (Detected OS: %s.) Run NX on a Mac to let it drive the "
                "desktop." % cap.get("os"))
    lines = ["To let NX control your Mac, grant it these once in System Settings → Privacy & Security:"]
    lines.append("  • Accessibility — so NX can click, type, and move windows (System Settings → Privacy & Security → Accessibility).")
    lines.append("  • Screen & System Audio Recording — so NX can see the screen it's acting on (same panel → Screen Recording).")
    if not cap.get("backend"):
        lines.append("  • Precise control ships WITH NX (pynput) — if it's somehow missing, reinstall nxplora "
                     "(or `brew install cliclick` as an alternative). AppleScript System Events is the last-resort fallback.")
    lines.append("Add your terminal / NX to each list and toggle it on, then try again.")
    return "\n".join(lines)


# ── one-click remediation: pop macOS's OWN grant dialog + open the exact pane (no scavenger hunt) ──────────────
# Apple forbids an app from granting itself these permissions — but it DOES let us (1) provoke the system's own
# native dialog (the popup WITH an "Open System Settings" button) by attempting the guarded action, and (2) deep-
# link straight to the exact Privacy pane so granting is a single toggle. cliclick can't ride in a wheel (it's a
# Homebrew binary), but we can run the one command for the operator.

PRIVACY_PANE_URLS = {
    "accessibility":    "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility",
    "screen_recording": "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture",
}


def open_privacy_pane(which: str) -> dict:
    """`open` the EXACT System Settings → Privacy pane (accessibility | screen_recording) so the grant is one click,
    not a hunt. Returns {ok, which, url}. macOS-only; honest no-op elsewhere. Never raises."""
    url = PRIVACY_PANE_URLS.get(which)
    if not url or not is_macos():
        return {"ok": False, "which": which, "error": "unsupported"}
    r = _run(["open", url], timeout=8)
    return {"ok": bool(r.get("ok")), "which": which, "url": url}


def trigger_permission_prompts() -> dict:
    """Provoke macOS's OWN native permission dialogs (the popups WITH an 'Open System Settings' button): a real
    screencapture attempt makes macOS prompt for Screen Recording; a System-Events no-op makes it prompt for
    Accessibility ('… wants to control this computer'). Returns which were attempted. macOS-only; never raises."""
    out = {"screen_recording": False, "accessibility": False}
    if not is_macos():
        return out
    if shutil.which("screencapture"):
        import tempfile, os as _os
        _p = _os.path.join(tempfile.gettempdir(), "nx_perm_probe.png")
        _run(["screencapture", "-x", _p], timeout=8)
        try:
            _os.remove(_p)
        except Exception:
            pass
        out["screen_recording"] = True
    if shutil.which("osascript"):
        _run(["osascript", "-e", 'tell application "System Events" to return name of first process'], timeout=8)
        out["accessibility"] = True
    return out


def brew_available() -> bool:
    return bool(shutil.which("brew"))


def accessibility_granted() -> Optional[bool]:
    """Is the Accessibility grant actually ON (not just the binary present)? True/False when we can tell, None when
    unknown. Probes with a System-Events call macOS BLOCKS without the grant ('not allowed assistive access') — the
    same call also surfaces macOS's native grant prompt the first time. macOS-only; never raises."""
    if not is_macos() or not shutil.which("osascript"):
        return None
    r = _run(["osascript", "-e", 'tell application "System Events" to return name of first process'], timeout=8)
    if r.get("ok"):
        return True
    err = (str(r.get("stderr") or "") + str(r.get("error") or "")).lower()
    if "not allowed" in err or "assistive access" in err or "-1719" in err or "1002" in err:
        return False
    return None  # a different failure — don't false-negative the operator into a needless grant dance


def install_cliclick(run: bool = False) -> dict:
    """The one-command precise-click install. run=False returns the command to show; run=True executes
    `brew install cliclick`. Returns {ok, cmd, installed, already?, error?, hint?}. Homebrew-gated; never raises."""
    cmd = ["brew", "install", "cliclick"]
    if shutil.which("cliclick"):
        return {"ok": True, "cmd": cmd, "installed": True, "already": True}
    if not brew_available():
        return {"ok": False, "cmd": cmd, "installed": False, "error": "no_brew",
                "hint": "Install Homebrew first (https://brew.sh), then `brew install cliclick`."}
    if not run:
        return {"ok": True, "cmd": cmd, "installed": False}
    _run(cmd, timeout=180)
    ok = bool(shutil.which("cliclick"))
    return {"ok": ok, "cmd": cmd, "installed": ok, "error": None if ok else "brew_install_failed"}


def remediate_permissions(cap: Optional[dict] = None, do_open: bool = True, do_prompt: bool = True) -> dict:
    """Turn the scavenger hunt into one click when control isn't ready: fire macOS's own grant prompts AND open the
    exact Privacy panes, so the operator just flips a toggle. Returns {opened, prompted, needs, cliclick, message}.
    Side-effectful (opens Settings + provokes dialogs) but never interactive/raises — the caller runs any cliclick Y/n."""
    cap = cap or detect_executor()
    res = {"opened": [], "prompted": {}, "needs": [], "cliclick": None, "message": ""}
    if not cap.get("macos"):
        res["message"] = permission_guidance(cap)
        return res
    if not cap.get("screenshot"):
        res["needs"].append("screen_recording")
    res["needs"].append("accessibility")
    if do_prompt:
        res["prompted"] = trigger_permission_prompts()
    if do_open:
        for which in ("accessibility", "screen_recording"):
            if open_privacy_pane(which).get("ok"):
                res["opened"].append(which)
    if not cap.get("backend"):
        res["cliclick"] = install_cliclick(run=False)
    res["message"] = ("I opened the exact Privacy panes and macOS should show a grant prompt — switch NX (your "
                      "terminal) ON for Accessibility + Screen Recording, then try again.")
    return res


def preflight(cap: Optional[dict] = None) -> dict:
    """Can NX drive the desktop right now? Returns {ready, reason?, guidance?}. ready=False carries the guidance so
    the tool surfaces an honest 'grant these permissions' instead of silently failing or faking an action."""
    cap = cap or detect_executor()
    if not cap.get("macos"):
        return {"ready": False, "reason": "unsupported_os", "guidance": permission_guidance(cap)}
    if not cap.get("screenshot"):
        return {"ready": False, "reason": "no_screencapture", "guidance": permission_guidance(cap)}
    if not cap.get("click"):
        return {"ready": False, "reason": "no_click_backend", "guidance": permission_guidance(cap)}
    return {"ready": True}


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# EXECUTOR (macOS) — capability-detected; device-proven. Each returns {ok, error?}. Never raises.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def _run(cmd: list[str], timeout: float = 15.0) -> dict:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"ok": r.returncode == 0, "stdout": r.stdout, "stderr": r.stderr, "returncode": r.returncode}
    except FileNotFoundError:
        return {"ok": False, "error": "tool_not_found: " + (cmd[0] if cmd else "")}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}
    except Exception as e:  # never raise into the loop
        return {"ok": False, "error": type(e).__name__}


def take_screenshot(path: Optional[str] = None) -> dict:
    """Capture the screen to a PNG (screencapture -x = no shutter sound, whole screen). Returns {ok, path} or
    {ok:False, error}. A permission-denied capture yields a black image — the loop's planner will see nothing and
    the operator is guided to grant Screen Recording."""
    if not shutil.which("screencapture"):
        return {"ok": False, "error": "no_screencapture"}
    p = path or os.path.join(tempfile.gettempdir(), "nx-screen.png")
    r = _run(["screencapture", "-x", p])
    return {"ok": r.get("ok") and os.path.exists(p), "path": p} if r.get("ok") else {"ok": False, "error": r.get("error") or r.get("stderr") or "capture_failed"}


def execute_action(action: dict, backend: Optional[str] = None) -> dict:
    """Execute ONE already-gated action via the detected backend. The CALLER is responsible for the safety gate
    (classify + confirm) — this only runs. Never raises; returns {ok, error?}. macOS-only backends."""
    cap = detect_executor()
    backend = backend or cap.get("backend")
    kind = action.get("kind")
    if kind in _OBSERVE and kind != "screenshot":
        if kind == "wait":
            _run(["sleep", str(max(0, int(action.get("ms", 500))) / 1000.0)], timeout=11)
        return {"ok": True}
    if kind == "screenshot":
        return take_screenshot()
    if not backend:
        return {"ok": False, "error": "no_backend"}
    if backend == "pynput":
        return _execute_pynput(action)
    if backend == "cliclick":
        return _execute_cliclick(action)
    if backend == "osascript":
        return _execute_osascript(action)
    return {"ok": False, "error": "no_backend"}


def _execute_pynput(action: dict) -> dict:
    """Precise mouse/keyboard control via pynput — the BUNDLED (pip) backend, so there's no Homebrew step. Same
    macOS CGEvent path as cliclick, so it needs the Accessibility grant identically; a denied grant surfaces as an
    error the loop guides on. Never raises."""
    try:
        from pynput.mouse import Controller as _Mouse, Button as _Button
        from pynput.keyboard import Controller as _Kbd
    except Exception as e:
        return {"ok": False, "error": "pynput_import: " + type(e).__name__}
    kind = action.get("kind")
    try:
        if kind in ("click", "double_click", "right_click", "move", "drag"):
            m = _Mouse()
            x, y = int(action.get("x", 0)), int(action.get("y", 0))
            m.position = (x, y)
            if kind == "click":
                m.click(_Button.left, 1)
            elif kind == "double_click":
                m.click(_Button.left, 2)
            elif kind == "right_click":
                m.click(_Button.right, 1)
            elif kind == "drag":
                m.press(_Button.left)
                m.position = (int(action.get("to_x", x)), int(action.get("to_y", y)))
                m.release(_Button.left)
            return {"ok": True}
        if kind == "scroll":
            m = _Mouse()
            if action.get("x") is not None and action.get("y") is not None:
                m.position = (int(action["x"]), int(action["y"]))
            m.scroll(int(action.get("dx", 0)), int(action.get("dy", action.get("amount", -3))))
            return {"ok": True}
        if kind == "type":
            _Kbd().type(action.get("text", ""))
            return {"ok": True}
        if kind == "key":
            return _execute_pynput_key(action.get("keys", ""))
        if kind == "open_app":
            return _run(["open", "-a", action.get("app", "")])
        return {"ok": False, "error": "unsupported_action"}
    except Exception as e:
        return {"ok": False, "error": "pynput_exec: " + type(e).__name__}


def _execute_pynput_key(keys: str) -> dict:
    """A friendly key / combo ('enter', 'cmd+c', 'shift+tab') → pynput key presses (modifiers held around the key).
    Unmapped single chars are typed as-is. Never raises."""
    try:
        from pynput.keyboard import Controller as _Kbd, Key as _Key
    except Exception as e:
        return {"ok": False, "error": "pynput_import: " + type(e).__name__}
    special = {
        "enter": _Key.enter, "return": _Key.enter, "tab": _Key.tab, "esc": _Key.esc, "escape": _Key.esc,
        "space": _Key.space, "delete": _Key.delete, "backspace": _Key.backspace, "up": _Key.up, "down": _Key.down,
        "left": _Key.left, "right": _Key.right, "home": _Key.home, "end": _Key.end,
        "cmd": _Key.cmd, "command": _Key.cmd, "ctrl": _Key.ctrl, "control": _Key.ctrl,
        "alt": _Key.alt, "option": _Key.alt, "shift": _Key.shift,
    }
    parts = [p.strip().lower() for p in str(keys or "").replace("-", "+").split("+") if p.strip()]
    if not parts:
        return {"ok": False, "error": "unmapped_key"}
    mods = [p for p in parts if p in ("cmd", "command", "ctrl", "control", "alt", "option", "shift")]
    rest = [p for p in parts if p not in mods]
    k = _Kbd()
    try:
        held = [special[m] for m in mods]
        for h in held:
            k.press(h)
        for p in rest:
            r = special.get(p, p)  # a single char stays a char
            k.press(r)
            k.release(r)
        for h in reversed(held):
            k.release(h)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": "pynput_key: " + type(e).__name__}


def _execute_cliclick(action: dict) -> dict:
    kind = action.get("kind")
    x, y = action.get("x"), action.get("y")
    if kind == "click":
        return _run(["cliclick", f"c:{x},{y}"])
    if kind == "double_click":
        return _run(["cliclick", f"dc:{x},{y}"])
    if kind == "right_click":
        return _run(["cliclick", f"rc:{x},{y}"])
    if kind == "move":
        return _run(["cliclick", f"m:{x},{y}"])
    if kind == "drag":
        return _run(["cliclick", f"dd:{x},{y}", f"du:{action.get('to_x')},{action.get('to_y')}"])
    if kind == "type":
        return _run(["cliclick", "-w", "20", f"t:{action.get('text', '')}"])
    if kind == "key":
        return _run(["cliclick", f"kp:{_cliclick_key(action.get('keys', ''))}"])
    if kind == "open_app":
        return _run(["open", "-a", action.get("app", "")])
    if kind == "scroll":
        # cliclick has no native scroll; fall back to osascript for scroll.
        return _execute_osascript(action)
    return {"ok": False, "error": "unsupported_action"}


def _execute_osascript(action: dict) -> dict:
    """AppleScript System Events fallback. Requires Accessibility permission; a denied call returns an 'assistive
    access' error that preflight/guidance explains."""
    kind = action.get("kind")
    if kind == "open_app":
        return _run(["open", "-a", action.get("app", "")])
    if kind == "type":
        text = (action.get("text") or "").replace("\\", "\\\\").replace('"', '\\"')
        return _run(["osascript", "-e", f'tell application "System Events" to keystroke "{text}"'])
    if kind == "key":
        combo = _osascript_keystroke(action.get("keys", ""))
        if not combo:
            return {"ok": False, "error": "unmapped_key"}
        return _run(["osascript", "-e", f'tell application "System Events" to {combo}'])
    if kind in ("click", "double_click", "right_click", "move", "drag"):
        # System Events can't click at arbitrary coords without extra tooling; guide toward cliclick.
        return {"ok": False, "error": "click_needs_cliclick"}
    if kind == "scroll":
        return {"ok": False, "error": "scroll_needs_cliclick"}
    return {"ok": False, "error": "unsupported_action"}


def _cliclick_key(keys: str) -> str:
    """Map a friendly key/combo to a cliclick key name (best-effort; returns the input lowercased if unmapped)."""
    k = (keys or "").strip().lower()
    return {"enter": "return", "return": "return", "esc": "esc", "escape": "esc", "tab": "tab",
            "space": "space", "delete": "delete", "backspace": "delete", "up": "arrow-up",
            "down": "arrow-down", "left": "arrow-left", "right": "arrow-right"}.get(k, k)


def _osascript_keystroke(keys: str) -> str:
    """Map a friendly key/combo to an AppleScript System Events statement. Supports simple keys + cmd/opt/ctrl/shift
    modifiers (e.g. 'cmd+s'). Empty when unmappable."""
    k = (keys or "").strip().lower()
    special = {"enter": "return", "return": "return", "tab": "tab", "space": "space", "esc": "key code 53",
               "escape": "key code 53", "up": "key code 126", "down": "key code 125", "left": "key code 123",
               "right": "key code 124", "delete": "key code 51", "backspace": "key code 51"}
    if k in special:
        v = special[k]
        return v if v.startswith("key code") else f"keystroke {v}"
    m = re.match(r"^(cmd|command|opt|option|ctrl|control|shift)\+(.+)$", k)
    if m:
        mod = {"cmd": "command", "command": "command", "opt": "option", "option": "option",
               "ctrl": "control", "control": "control", "shift": "shift"}[m.group(1)]
        base = m.group(2).strip()
        if len(base) == 1:
            return f'keystroke "{base}" using {mod} down'
    return ""


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# OBSERVE + PLAN — a text observation of the screen (frontmost app/window) the text-model planner reasons over.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def observe_context() -> dict:
    """A lightweight TEXT observation for a text-model planner: the frontmost app + its front-window title (macOS,
    via osascript). {} on non-mac or on error. Cheap grounding — the model knows WHERE it is acting even without
    vision. (A screenshot is still captured so the operator watches + a future vision model can use it.)"""
    if not is_macos() or not shutil.which("osascript"):
        return {}
    script = (
        'tell application "System Events" to set frontApp to name of first application process whose frontmost is true\n'
        'set winTitle to ""\n'
        'try\n'
        '  tell application "System Events" to tell process frontApp to set winTitle to name of front window\n'
        'end try\n'
        'return frontApp & "\\n" & winTitle'
    )
    r = _run(["osascript", "-e", script], timeout=5)
    if not r.get("ok"):
        return {}
    parts = (r.get("stdout") or "").strip().split("\n", 1)
    return {"app": (parts[0].strip() if parts else ""), "window": (parts[1].strip() if len(parts) > 1 else "")}


_PLAN_SYS = (
    "You are NX driving the operator's Mac to accomplish a goal, one action at a time. Each step you get the "
    "current screen context and respond with EXACTLY ONE JSON action object (no prose, no fences):\n"
    '  {"kind":"click","x":<int>,"y":<int>,"target":"<what you\'re clicking>","why":"<short>"}\n'
    '  {"kind":"double_click"|"right_click"|"move","x":<int>,"y":<int>,"target":"..."}\n'
    '  {"kind":"type","text":"<text to type into the focused field>","target":"..."}\n'
    '  {"kind":"key","keys":"cmd+s|enter|tab|esc|...","why":"..."}\n'
    '  {"kind":"open_app","app":"Safari","why":"..."}\n'
    '  {"kind":"scroll","dx":0,"dy":-300}\n'
    '  {"kind":"done","why":"<goal reached or you need the operator>"}\n'
    "Rules: prefer open_app + keyboard (type / key) over clicking exact pixels when you can't see coordinates. "
    "NEVER type a password, 2FA code, card number, or any credential, and NEVER confirm a purchase/payment — emit "
    "{\"kind\":\"done\"} and let the operator do that themselves. Every real action is confirmed by the operator "
    "before it runs, so act decisively toward the goal; call done when it's complete or you're blocked."
)


def plan_next_action(goal: str, observation: dict, model_fn: Callable[[str], str]) -> dict:
    """Build the planning prompt from the goal + observation (frontmost app/window + recent history) and ask the
    model for the next action JSON via `model_fn` (the caller's one-shot completion). Returns a parsed action.
    Pure aside from the injected model_fn call. Mirrors nx_browse.plan_next_action."""
    ctx = observation.get("context") or {}
    hist = observation.get("history") or []
    hist_lines = "\n".join(
        "- %s → %s" % (describe_action(h.get("action", {})), ("ok" if h.get("executed") else (h.get("error") or "skipped")))
        for h in hist[-6:]
    )
    screen = "app=%s window=%s%s" % (ctx.get("app", "?"), ctx.get("window", ""), "" if observation.get("screenshot_ok") else " (no screenshot — grant Screen Recording)")
    prompt = (
        _PLAN_SYS
        + "\n\nGOAL: " + (goal or "")
        + "\n\nScreen now: " + screen
        + (("\n\nWhat you've done so far:\n" + hist_lines) if hist_lines else "")
        + "\n\nNext action? Respond with exactly one JSON object."
    )
    try:
        answer = model_fn(prompt)
    except Exception:
        return {"kind": "done", "why": "planner error"}
    return parse_plan_action(answer)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# VISION PLANNING — feed the SCREENSHOT to a vision model for pixel-accurate clicking (degrades to text planning).
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def png_dimensions(path: str) -> Optional[tuple[int, int]]:
    """Parse a PNG's pixel (width, height) from its IHDR chunk — 8-byte signature + big-endian uint32 width[16:20] /
    height[20:24]. None on a non-PNG / short read / any error. Pure + dependency-free (no Pillow — NX ships none).
    Used to map screenshot-pixel coords (Retina = 2x) to logical click points."""
    try:
        with open(path, "rb") as f:
            head = f.read(24)
    except Exception:
        return None
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w = int.from_bytes(head[16:20], "big")
    h = int.from_bytes(head[20:24], "big")
    return (w, h) if w > 0 and h > 0 else None


def encode_image_data_uri(path: str, mime: str = "image/png") -> Optional[str]:
    """base64 a file into a data: URI (data:image/png;base64,<b64>) for a chat-completions image_url part. None on a
    falsy / missing / unreadable path. Never raises."""
    if not path:
        return None
    try:
        import base64
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return "data:%s;base64,%s" % (mime, b64)
    except Exception:
        return None


_VISION_PLAN_SYS = (
    "You are NX driving the operator's Mac to accomplish a goal, one action at a time. You are shown a SCREENSHOT of "
    "the current screen. Respond with EXACTLY ONE JSON action object (no prose, no fences):\n"
    '  {"kind":"click","x":<int>,"y":<int>,"target":"<what you\'re clicking>","why":"<short>"}\n'
    '  {"kind":"double_click"|"right_click"|"move","x":<int>,"y":<int>,"target":"..."}\n'
    '  {"kind":"drag","x":<int>,"y":<int>,"to_x":<int>,"to_y":<int>,"target":"..."}\n'
    '  {"kind":"type","text":"<text to type into the focused field>","target":"..."}\n'
    '  {"kind":"key","keys":"cmd+s|enter|tab|esc|...","why":"..."}\n'
    '  {"kind":"open_app","app":"Safari","why":"..."}\n'
    '  {"kind":"scroll","dx":0,"dy":-300}\n'
    '  {"kind":"done","why":"<goal reached or you need the operator>"}\n'
    "Give x,y as PIXEL coordinates in the screenshot's own coordinate space (top-left origin). ALWAYS include a "
    "short descriptive `target` for every click/type (e.g. \"the blue Save button\", \"the search field\") — this is "
    "required. NEVER type a password, 2FA code, card number, or any credential, and NEVER click a purchase/payment "
    "confirmation — emit {\"kind\":\"done\"} and let the operator do that. Every real action is confirmed by the "
    "operator before it runs, so act decisively; call done when the goal is complete or you're blocked."
)


def build_vision_messages(goal: str, observation: dict, image_data_uri: str) -> list:
    """Build the chat-completions MULTIMODAL message list (a text part + an image_url part) the vision model plans
    over. Pure — the exact shape stream_chat passes through untouched. Mirrors plan_next_action's text shaping."""
    ctx = observation.get("context") or {}
    hist = observation.get("history") or []
    hist_lines = "\n".join(
        "- %s → %s" % (describe_action(h.get("action", {})), ("ok" if h.get("executed") else (h.get("error") or "skipped")))
        for h in hist[-6:]
    )
    text = (
        "GOAL: " + (goal or "")
        + "\n\nScreen: app=%s window=%s" % (ctx.get("app", "?"), ctx.get("window", ""))
        + (("\n\nWhat you've done so far:\n" + hist_lines) if hist_lines else "")
        + "\n\nLook at the screenshot and give the next action as one JSON object."
    )
    return [
        {"role": "system", "content": _VISION_PLAN_SYS},
        {"role": "user", "content": [
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": image_data_uri}},
        ]},
    ]


def scale_point(x: Any, y: Any, shot_w: Any, shot_h: Any, screen_w: Any, screen_h: Any) -> tuple[Any, Any]:
    """Map a screenshot-pixel coordinate to a LOGICAL click point (Retina screenshots are 2x the logical points
    cliclick uses). (round(x*screen_w/shot_w), round(y*screen_h/shot_h)) when all dims are positive; IDENTITY
    degrade when any dim is missing / zero / non-numeric (validate_point clamps downstream). Pure."""
    xi, yi = _int(x, None), _int(y, None)
    sw, sh = _int(shot_w, None), _int(shot_h, None)
    lw, lh = _int(screen_w, None), _int(screen_h, None)
    if xi is None or yi is None:
        return (x, y)
    if not (sw and sh and lw and lh):
        return (xi, yi)
    return (round(xi * lw / sw), round(yi * lh / sh))


def plan_next_action_vision(
    goal: str,
    observation: dict,
    vision_model_fn: Optional[Callable[[list], str]],
    text_model_fn: Optional[Callable[[str], str]] = None,
) -> dict:
    """Plan the next action from the SCREENSHOT via a vision model, scaling its pixel coords to logical click points.
    DEGRADES to the existing text planner (plan_next_action) whenever vision isn't usable: no vision_model_fn, no
    screenshot, the image won't encode, an empty vision reply, or the vision call raises. Returns a parsed action.
    Never fakes a click — a degrade just plans from the text observation instead."""
    text_fn = text_model_fn or (lambda _p: "")
    shot = observation.get("screenshot")
    data_uri = encode_image_data_uri(shot) if shot else None
    if not vision_model_fn or not data_uri:
        return plan_next_action(goal, observation, text_fn)
    try:
        answer = vision_model_fn(build_vision_messages(goal, observation, data_uri))
    except Exception:
        return plan_next_action(goal, observation, text_fn)
    if not (answer or "").strip():
        return plan_next_action(goal, observation, text_fn)  # empty vision reply → text planner (avoid a premature done)
    action = parse_plan_action(answer)
    # Scale + clamp the coordinates from screenshot-pixel space into logical click points.
    dims = png_dimensions(shot) or (None, None)
    screen = observation.get("screen_size") or (None, None)
    for xk, yk in (("x", "y"), ("to_x", "to_y")):
        if xk in action and yk in action:
            sx, sy = scale_point(action[xk], action[yk], dims[0], dims[1], screen[0], screen[1])
            clamped = validate_point(sx, sy, _int(screen[0], 100000) or 100000, _int(screen[1], 100000) or 100000)
            if clamped is not None:
                action[xk], action[yk] = clamped
    return action


def logical_screen_size() -> Optional[tuple[int, int]]:
    """The LOGICAL screen size (points, not Retina pixels) via osascript Finder desktop bounds. None off-mac or on
    error. Device-proven like observe_context (not CI-exercised). Feeds scale_point so a 2x screenshot coordinate
    maps to the right click point."""
    if not is_macos() or not shutil.which("osascript"):
        return None
    r = _run(["osascript", "-e", 'tell application "Finder" to get bounds of window of desktop'], timeout=5)
    if not r.get("ok"):
        return None
    nums = re.findall(r"-?\d+", r.get("stdout") or "")
    if len(nums) < 4:
        return None
    return (int(nums[2]), int(nums[3]))  # bounds = {x1,y1,x2,y2}; width=x2, height=y2 (desktop origin 0,0)


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# THE LOOP — screenshot → plan → (gate) → act → observe, bounded. Mirrors nx_browse.browse_task.
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

MAX_STEPS_DEFAULT = 12


def control_computer(
    goal: str,
    planner: Callable[[str, dict], str],
    confirm: Optional[Callable[[str], bool]] = None,
    max_steps: int = MAX_STEPS_DEFAULT,
    on_step: Optional[Callable[[str], None]] = None,
) -> dict:
    """Drive the desktop toward `goal`. `planner(goal, observation)` returns the model's next-action answer (the
    caller wires the NX model). `confirm(description)` gates every ACT action (returns True to proceed) — fails
    CLOSED (no confirm ⇒ act refused). Observe actions run free; PROHIBITED actions are refused outright. Bounded by
    max_steps. Returns {ok, steps:[...], done, halted?}. Never raises.

    The executor is device-proven; on a machine without permissions/tools, preflight short-circuits with honest
    guidance instead of faking anything."""
    on_step = on_step or (lambda _s: None)
    pf = preflight()
    if not pf.get("ready"):
        on_step("computer control unavailable — " + pf.get("reason", ""))
        return {"ok": False, "halted": pf.get("reason"), "guidance": pf.get("guidance"), "steps": []}

    steps: list[dict] = []
    for _ in range(max(1, min(int(max_steps), 40))):
        shot = take_screenshot()
        observation = {
            "screenshot": shot.get("path") if shot.get("ok") else None,
            "screenshot_ok": bool(shot.get("ok")),
            "context": observe_context(),
            "history": steps,
            "screen_size": logical_screen_size(),  # logical points, so a vision planner can scale Retina pixel coords
        }
        try:
            planned = planner(goal, observation)
        except Exception:
            return {"ok": True, "steps": steps, "done": True, "halted": "planner_error"}
        # The planner may return a parsed action dict (plan_next_action) OR a raw model-answer string — accept both.
        action = planned if isinstance(planned, dict) else parse_plan_action(str(planned or ""))
        verdict = classify_computer_action(action)
        desc = describe_action(action)

        if action.get("kind") == "done":
            on_step("done: " + (action.get("why") or ""))
            return {"ok": True, "steps": steps, "done": True}

        if verdict == "PROHIBITED":
            on_step(f"refused (sensitive — you do this yourself): {desc}")
            steps.append({"action": action, "verdict": "PROHIBITED", "executed": False})
            return {"ok": True, "steps": steps, "done": False, "halted": "prohibited"}

        if verdict == "GATED":
            approved = bool(confirm and confirm(desc))
            if not approved:
                on_step(f"skipped (not approved): {desc}")
                steps.append({"action": action, "verdict": "GATED", "executed": False, "refused": True})
                return {"ok": True, "steps": steps, "done": False, "halted": "declined"}

        res = execute_action(action)
        ok = bool(res.get("ok"))
        on_step(("✓ " if ok else "⚠ ") + desc + ("" if ok else f" — {res.get('error', 'failed')}"))
        steps.append({"action": action, "verdict": verdict, "executed": ok, "error": res.get("error")})
        if not ok and res.get("error") in ("no_backend", "click_needs_cliclick"):
            return {"ok": True, "steps": steps, "done": False, "halted": "executor_unavailable", "guidance": permission_guidance()}

    return {"ok": True, "steps": steps, "done": False, "halted": "max_steps"}


# ───────────────────────────────────────────────────────────────────────────────────────────────────────────
# helpers
# ───────────────────────────────────────────────────────────────────────────────────────────────────────────

def _int(v: Any, default: Any = 0) -> Any:
    try:
        return int(v)
    except (TypeError, ValueError):
        return default
