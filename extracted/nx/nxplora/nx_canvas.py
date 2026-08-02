"""
nx_canvas.py — NX Execution Canvas
Shows live task progress like Codex.
Query bar collapses, work panel appears, approve/reject gate at end.
"""

import sys
import time
import threading
import os

# prompt_toolkit is optional; if unavailable or stdin is not a TTY we fall back to plain input.
try:
    from prompt_toolkit import Application
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.layout import Layout, Window, FormattedTextControl
    from prompt_toolkit.formatted_text import ANSI
    _HAVE_PROMPT_TOOLKIT = True
except Exception:  # pragma: no cover
    _HAVE_PROMPT_TOOLKIT = False

GOLD   = "\033[38;2;200;164;74m"
GOLDD  = "\033[38;2;196;162;88m"
GOLDK  = "\033[38;2;150;130;70m"
WHITE  = "\033[38;2;224;221;212m"
DIM    = "\033[38;2;146;140;122m"
DIMR   = "\033[38;2;132;126;110m"
GREEN  = "\033[38;2;80;200;100m"
RED    = "\033[38;2;220;80;70m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


class NXCanvas:
    """
    Live execution canvas.
    Shows task steps as they happen.
    Ends with approve/reject gate.
    """

    def __init__(self, task: str):
        self.task = task
        self.steps = []
        self.start_time = time.time()
        self._lock = threading.Lock()
        self._closed = False
        self._lines_drawn = 0

    def _elapsed(self) -> str:
        return f"{int(time.time() - self.start_time)}s"

    def open(self):
        """Draw the canvas header."""
        try:
            cols = os.get_terminal_size().columns
        except Exception:
            cols = 80
        w = min(cols, 96)

        print(f"\n{GOLDK}{'─' * w}{RESET}")
        print(
            f"  {GOLD}✦{RESET}  "
            f"{WHITE}{self.task}{RESET}"
        )
        print(f"{GOLDK}{'─' * w}{RESET}\n")

    def step(self, label: str, status: str = "working"):
        """Add a step to the canvas."""
        with self._lock:
            self.steps.append({
                "label": label,
                "status": status,
                "time": self._elapsed(),
            })
            self._redraw_steps()

    def complete_step(self, label: str, result: str = "done"):
        """Mark a step as complete."""
        with self._lock:
            for s in self.steps:
                if s["label"] == label:
                    s["status"] = result
                    break
            self._redraw_steps()

    def update_step(self, label: str, status: str = "working"):
        """Update an existing step or add it if not found."""
        with self._lock:
            for s in self.steps:
                if s["label"] == label:
                    s["status"] = status
                    s["time"] = self._elapsed()
                    self._redraw_steps()
                    return
            self.steps.append({
                "label": label,
                "status": status,
                "time": self._elapsed(),
            })
            self._redraw_steps()

    def request_approval(self, prompt: str) -> bool:
        """Thread-safe approval prompt."""
        with self._lock:
            self._lines_drawn = 0
            print(f"\n  {GOLD}?{RESET}  {WHITE}{prompt}{RESET}  [a/r] > ", end="")
        try:
            response = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False
        return response in ("a", "approve", "y", "yes")

    def _redraw_steps(self):
        """Redraw all steps in place."""
        if self._closed:
            return
        lines = len(self.steps)
        if self._lines_drawn > 0:
            sys.stdout.write(f"\033[{self._lines_drawn}A")
        total = max(lines, self._lines_drawn)
        for _ in range(total):
            sys.stdout.write("\033[2K")
            sys.stdout.write("\033[B")
        if total > 0:
            sys.stdout.write(f"\033[{total}A")
        for step in self.steps:
            status = step["status"]
            time_str = step["time"]
            if status == "done":
                icon = f"{GREEN}✓{RESET}"
            elif status == "working":
                icon = f"{GOLD}·{RESET}"
            elif status == "error":
                icon = f"{RED}✗{RESET}"
            else:
                icon = f"{DIM}·{RESET}"
            label = step["label"]
            sys.stdout.write(
                f"  {icon}  "
                f"{WHITE}{label:<40}{RESET}"
                f"  {DIMR}{time_str}{RESET}\n"
            )
        sys.stdout.flush()
        self._lines_drawn = lines

    def output(self, text: str):
        """Show output text below steps."""
        print(f"\n  {WHITE}{text}{RESET}")

    def close(self, final_status: str = "done"):
        """Close the canvas — subtle single-line status. On plain success we print
        NOTHING: the per-action lines (and any approval line) already show the outcome,
        so a trailing green ✓ is redundant. Only error/interrupt get a marker."""
        if self._closed:
            return
        self._closed = True
        if final_status == "done":
            return
        elapsed = self._elapsed()
        icon = f"{RED}✗{RESET}" if final_status == "error" else f"{GOLD}·{RESET}"
        print(f"\n  {icon}  {DIM}{elapsed}{RESET}\n")


def approve_gate(
    summary: str,
    changes: list[dict] = None,
    allow_approve_all: bool = True,
) -> tuple[bool, str]:
    """
    Show approve/reject gate after NX completes a task.
    Returns (approved: bool, reason: str)

    In an interactive terminal this uses arrow keys (↑/↓) + Enter.
    In non-TTY environments (tests, pipes) it falls back to text input.

    allow_approve_all=False removes the 'Approve all (this session)' option entirely
    (menu AND the 'AA' text fallback) — used for DESTRUCTIVE integration ops (delete /
    money / send), which are ALWAYS per-op by policy: there is no blanket authority to
    offer, so it must not even appear as a choice a tired operator can click.

    changes = [
        {"type": "edit", "file": "nx_cli.py", "description": "Fixed /world handler"},
        {"type": "api", "service": "shopify", "description": "Updated 23 products"},
    ]
    """
    try:
        cols = os.get_terminal_size().columns
    except Exception:
        cols = 80
    w = min(cols, 96)

    options = [
        ("approve", "Approve"),
        ("approve_all", "Approve all (this session)"),
        ("reject", "Reject"),
        ("reject_reason", "Reject with reason"),
    ]
    if not allow_approve_all:
        options = [o for o in options if o[0] != "approve_all"]

    def _render_text(selected: int, plain: bool = False) -> str:
        lines = [f"\n{GOLD}{'─' * w}{RESET}"]
        lines.append(f"\n  {WHITE}{summary}{RESET}\n")
        if changes:
            for change in changes:
                ctype = change.get("type", "change")
                desc = change.get("description", "")
                file = change.get("file", change.get("service", ""))
                icon = "📝" if ctype == "edit" else "🔗"
                lines.append(f"  {DIM}{icon}  {file:<30}  {desc}{RESET}")
            lines.append("")
        if plain:
            # Typed-input gate: NUMBER shortcuts, never "↑↓ Select / Enter Confirm"
            # (that misled the operator into pressing Enter on nothing → empty → blocked).
            lines.append(f"  {DIM}Type a number and press Enter{RESET}")
            lines.append("")
            for i, (_key, label) in enumerate(options):
                lines.append(f"  {GOLD}{i + 1}{RESET}  {label}")
        else:
            lines.append(f"  {DIM}↑↓ or a number  ·  Enter to confirm{RESET}")
            lines.append("")
            for i, (_key, label) in enumerate(options):
                marker = f"{GOLD}›{RESET}" if i == selected else " "
                color = WHITE if i == selected else ""
                reset = RESET if i == selected else ""
                lines.append(f"  {marker} {GOLD}{i + 1}{RESET} {color}{label}{reset}")
        lines.append(f"\n{GOLD}{'─' * w}{RESET}\n")
        return "\n".join(lines)

    def _fallback_input() -> tuple[bool, str]:
        """Plain LINE-input gate for embedded/browser terminals where the arrow-key app
        can't read keys. Shows NUMBER shortcuts (1/2/3/4) matching the menu, and — critically
        — a bare Enter RE-PROMPTS instead of counting as a reject. (The old gate printed
        "↑↓ Select / Enter Confirm" then read a typed line, so a habitual Enter returned ""
        and blocked the run though the operator meant to approve.)"""
        print(_render_text(0, plain=True))
        # Number → option key by position (auto-handles allow_approve_all removing one).
        # Letters kept as forgiving aliases; numbers are what the menu shows.
        _by_num = {str(i + 1): key for i, (key, _lbl) in enumerate(options)}
        _valid = {key for key, _lbl in options}
        _alias = {"a": "approve", "approve": "approve", "y": "approve", "yes": "approve",
                  "aa": "approve_all",
                  "r": "reject", "reject": "reject", "n": "reject", "no": "reject",
                  "rr": "reject_reason"}
        n = len(options)
        # Bounded reads: empty line re-prompts; EOF/^C fails closed; a valid number/alias
        # decides. Only an explicit approve token ever returns True.
        for _attempt in range(8):
            try:
                response = input(f"  {GOLD}›{RESET}  ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                return False, "cancelled"
            if response == "":
                print(f"  {DIM}Type a number 1-{n} and press Enter (1 = approve).{RESET}")
                continue
            choice = _by_num.get(response) or _alias.get(response)
            if choice not in _valid:
                print(f"  {DIM}Unrecognized — type a number 1-{n}.{RESET}")
                continue
            if choice == "approve":
                print(f"\n  {GREEN}✦ Approved{RESET}\n")
                return True, ""
            if choice == "approve_all":
                print(f"\n  {GREEN}✦ Approved — all changes auto-approved this session{RESET}\n")
                return True, "session_approve_all"
            if choice == "reject":
                print(f"\n  {RED}✦ Rejected{RESET}\n")
                return False, ""
            if choice == "reject_reason":
                try:
                    reason = input(f"  {GOLD}Reason › {RESET}").strip()
                except (KeyboardInterrupt, EOFError):
                    reason = ""
                print(f"\n  {RED}✦ Rejected{RESET}  {DIM}{reason}{RESET}\n")
                return False, reason
        return False, ""   # too many invalid entries → fail closed

    # Use the arrow-key prompt_toolkit dialog whenever we have a real TTY — INCLUDING VS
    # Code integrated terminals and Codespaces, which are full xterm.js terminals that DO
    # support raw-key input (vim/htop work there), so the operator gets ↑↓ + Enter (and 1-4).
    # We no longer force those to the typed gate — that denied working terminals the arrow
    # keys. The two safety nets below still catch a genuinely un-drivable terminal without
    # ever silently blocking: app.run() raising → _fallback_input(); app.run() returning an
    # unrecognized/None result → _fallback_input(). Plain gate only when there's no TTY, no
    # prompt_toolkit, or the operator sets NX_APPROVE_GATE_FALLBACK=1.
    try:
        _clean_tty = sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        _clean_tty = False
    if (not _HAVE_PROMPT_TOOLKIT or os.environ.get("NX_APPROVE_GATE_FALLBACK")
            or not _clean_tty):
        return _fallback_input()

    selected = 0

    def _render_ansi():
        return ANSI(_render_text(selected))

    kb = KeyBindings()

    @kb.add("up")
    def _up(event):
        nonlocal selected
        selected = (selected - 1) % len(options)
        event.app.invalidate()

    @kb.add("down")
    def _down(event):
        nonlocal selected
        selected = (selected + 1) % len(options)
        event.app.invalidate()

    @kb.add("enter")
    def _enter(event):
        event.app.exit(result=options[selected][0])

    @kb.add("c-c")
    @kb.add("c-d")
    def _cancel(event):
        event.app.exit(result="cancel")

    # Number keys 1-N pick that option immediately — matches the numbered menu and the
    # plain gate, and is faster than arrow+Enter.
    def _make_num_pick(idx):
        def _pick(event):
            event.app.exit(result=options[idx][0])
        return _pick
    for _oi in range(len(options)):
        kb.add(str(_oi + 1))(_make_num_pick(_oi))

    control = FormattedTextControl(text=_render_ansi)
    layout = Layout(Window(control))
    app = Application(
        layout=layout,
        key_bindings=kb,
        full_screen=False,
        mouse_support=False,
        erase_when_done=True,
    )

    try:
        result = app.run()
    except Exception:
        return _fallback_input()

    if result == "cancel":
        print(f"\n  {RED}✦ Cancelled{RESET}\n")
        return False, "cancelled"
    if result == "approve":
        print(f"\n  {GREEN}✦ Approved{RESET}\n")
        return True, ""
    if result == "approve_all":
        print(f"\n  {GREEN}✦ Approved — all changes auto-approved this session{RESET}\n")
        return True, "session_approve_all"
    if result == "reject":
        print(f"\n  {RED}✦ Rejected{RESET}\n")
        return False, ""
    if result == "reject_reason":
        try:
            reason = input(f"  {GOLD}Reason › {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            reason = ""
        print(f"\n  {RED}✦ Rejected{RESET}  {DIM}{reason}{RESET}\n")
        return False, reason

    # Unknown / None result: the arrow-key app rendered but returned no recognized
    # choice. Some embedded/browser terminals (Codespaces, the VS Code web terminal)
    # don't reliably deliver keys to a raw-mode prompt_toolkit app, so app.run() comes
    # back None even after the operator pressed Enter on "Approve". NEVER silently treat
    # that as blocked — that IS the bug (operator approved, run said "not approved by
    # operator"). Fall back to the plain line-input gate so the approval registers.
    return _fallback_input()


def arrow_pick(title, options, subtitle="↑↓ to move  ·  Enter to select"):
    """A reusable VERTICAL ↑/↓ + Enter menu (number keys work too). `options` = [(key, label), …]; returns the chosen
    key, or None on cancel. Real TTY → arrow keys; non-TTY / no prompt_toolkit → a typed-number fallback. Mirrors
    approve_gate's proven prompt_toolkit path (drives VS Code / Codespaces terminals too). Never raises."""
    n = len(options)
    if n == 0:
        return None

    def _render(selected, plain=False):
        lines = ["", f"  {GOLD}{title}{RESET}"]
        if not plain and subtitle:
            lines.append(f"  {DIM}{subtitle}{RESET}")
        lines.append("")
        if plain:
            lines.append(f"  {DIM}Type a number and press Enter{RESET}")
            lines.append("")
            for i, (_k, lbl) in enumerate(options):
                lines.append(f"  {GOLD}{i + 1}{RESET}  {lbl}")
        else:
            for i, (_k, lbl) in enumerate(options):
                marker = f"{GOLD}❯{RESET}" if i == selected else " "
                body = f"{WHITE}{lbl}{RESET}" if i == selected else f"{DIM}{lbl}{RESET}"
                lines.append(f"  {marker} {body}")
        lines.append("")
        return "\n".join(lines)

    def _fallback():
        print(_render(0, plain=True))
        by_num = {str(i + 1): k for i, (k, _l) in enumerate(options)}
        for _ in range(6):
            try:
                r = input(f"  {GOLD}❯{RESET} ").strip()
            except (EOFError, KeyboardInterrupt):
                return None
            if r in by_num:
                return by_num[r]
            print(f"  {DIM}Type a number 1-{n}.{RESET}")
        return None

    try:
        _clean_tty = sys.stdin.isatty() and sys.stdout.isatty()
    except Exception:
        _clean_tty = False
    if not _HAVE_PROMPT_TOOLKIT or os.environ.get("NX_APPROVE_GATE_FALLBACK") or not _clean_tty:
        return _fallback()

    _sel = [0]

    def _render_ansi():
        return ANSI(_render(_sel[0]))

    kb = KeyBindings()

    @kb.add("up")
    def _u(event):
        _sel[0] = (_sel[0] - 1) % n
        event.app.invalidate()

    @kb.add("down")
    def _d(event):
        _sel[0] = (_sel[0] + 1) % n
        event.app.invalidate()

    @kb.add("enter")
    def _en(event):
        event.app.exit(result=options[_sel[0]][0])

    @kb.add("c-c")
    @kb.add("c-d")
    def _cx(event):
        event.app.exit(result="__cancel__")

    def _mk(idx):
        def _p(event):
            event.app.exit(result=options[idx][0])
        return _p
    for _i in range(n):
        kb.add(str(_i + 1))(_mk(_i))

    control = FormattedTextControl(text=_render_ansi)
    app = Application(layout=Layout(Window(control)), key_bindings=kb, full_screen=False,
                      mouse_support=False, erase_when_done=True)
    try:
        result = app.run()
    except Exception:
        return _fallback()
    if result == "__cancel__":
        return None
    if result is None:  # a broken embedded terminal returned nothing — re-prompt via the typed fallback, never fail silently
        return _fallback()
    return result


import re
import shlex


def extract_bash_blocks(text: str) -> list[str]:
    """Pull all ```bash ... ``` blocks out of a model response."""
    return re.findall(r"```bash\s*(.*?)```", text, re.DOTALL)


def run_canvas_loop(
    task: str,
    model_response: str,
    canvas,
    auto_approve: bool = False,
) -> dict:
    """
    Parse model response for bash blocks.
    Show approve gate before running anything.
    Execute approved blocks via subprocess.
    Return {executed: [...], skipped: [...], output: str}
    """
    import subprocess

    blocks = extract_bash_blocks(model_response)
    if not blocks:
        return {"executed": [], "skipped": [], "output": ""}

    def _step(msg):
        if canvas is not None:
            try:
                canvas.step(msg)
            except Exception:
                pass

    results = []

    for i, block in enumerate(blocks):
        cmd = block.strip()
        if not cmd:
            continue

        _step(f"$ {cmd[:80]}{'...' if len(cmd) > 80 else ''}")

        if not auto_approve:
            approved, reason = approve_gate(cmd)
        else:
            approved, reason = True, ""

        if approved:
            if reason == "session_approve_all":
                auto_approve = True
            try:
                # Run in the user's actual cwd. Falls back to $HOME only if
                # cwd is unreadable (rare). Never silently runs in the NX
                # install directory — that surprised users with destructive ops.
                try:
                    run_cwd = os.getcwd()
                except OSError:
                    run_cwd = os.path.expanduser("~")
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=run_cwd,
                )
                output = (result.stdout + result.stderr).strip()
                _step(f"✓ {output[:120] if output else 'done'}")
                results.append({"cmd": cmd, "output": output, "ok": True})
            except subprocess.TimeoutExpired:
                _step("✗ timed out")
                results.append({"cmd": cmd, "output": "timeout", "ok": False})
            except Exception as e:
                _step(f"✗ {e}")
                results.append({"cmd": cmd, "output": str(e), "ok": False})
        elif reason:
            results.append({"cmd": cmd, "output": f"rejected: {reason}", "ok": False})
        else:
            results.append({"cmd": cmd, "output": "rejected", "ok": False})

    executed = [r for r in results if r["ok"]]
    skipped = [r for r in results if not r["ok"]]
    full_output = "\n".join(r["output"] for r in executed)

    return {"executed": executed, "skipped": skipped, "output": full_output}
