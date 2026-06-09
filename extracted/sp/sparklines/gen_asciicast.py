#! /usr/bin/env python3

# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///

"""Generate an asciinema v3 .cast file from a YAML spec.

Usage:  python gen_asciicast.py spec.yaml [output.cast]

If output is omitted it falls back to the spec's `output` key,
then to the input filename with a .cast extension.

Each command is run in its own PTY via ``shell -c cmd``.  Before the first
command the shell is started once in interactive mode to capture its real
prompt string; that prompt is then replayed before every command, so the
recording looks like a genuine session in the configured shell.

Example:
    # demo.yaml
    cols: 100
    rows: 30
    shell: nu          # bash, zsh, nu, fish, ... (default: bash)
    type_delay: 0.04
    type_variance: 0.7
    pause_after_cmd: 1.0
    steps:
    - marker: "Hello"
    - cmd: "echo 'Hello, world!'"

Security and Robustness Notes:
    - Commands from the YAML spec are executed in a PTY. Only use trusted YAML files.
    - A 5-minute timeout prevents runaway commands from hanging indefinitely.
    - Shell is resolved via ``shutil.which`` with fallback to $SHELL or /bin/sh.
    - Input validation ensures cols/rows are positive integers and delays are non-negative.
    - Empty YAML files produce a clear error message rather than failing silently.
"""

import fcntl
import json
import os
import pty
import random
import re
import select
import shutil
import struct
import sys
import termios
import time

import yaml

# Terminal sequences that switch or clear the screen — strip these from
# captured output so they don't disrupt the recording's visual continuity.
_SCREEN_OPS = re.compile(
    r"\x1b\[\?1049[hl]"  # alternate screen buffer on/off
    r"|\x1b\[\?47[hl]"  # alternate screen (older form)
    r"|\x1b\[\d*;\d*H\x1b\[\d*J"  # cursor-to-position + erase (nu prompt setup)
    r"|\x1b\[H\x1b\[\d*J"  # cursor home + erase
    r"|\x1b\[\d*J"  # erase display (0=to end, 1=to start, 2=all, 3=scrollback)
)


def random_typing_delay(type_delay: float, type_variance: float) -> float:
    """Return a randomised per-character delay (seconds).

    Args:
        type_delay: Base delay between keystrokes in seconds.
        type_variance: Variance factor (0-1) for randomizing delays.

    Returns:
        A delay value in seconds, minimum 0.005s.
    """
    jitter = (random.random() * 2 - 1) * type_variance
    return max(type_delay * (1 + jitter), 0.005)


def _capture_prompt(shell: str) -> str:
    """Return the shell's prompt string (colours preserved, no cursor ops).

    Runs the shell in non-interactive mode to evaluate its prompt command and
    return just the visible text.  This avoids the cursor-positioning and
    screen-clearing sequences that interactive prompts emit.

    Falls back to ``"$ "`` if the shell or its prompt command can't be queried.
    """
    import subprocess

    shell_path = shutil.which(shell)
    if not shell_path:
        return "$ "

    # Shell-specific one-liners that print the prompt text without side-effects.
    cmds: dict[str, str] = {
        "nu": 'print --no-newline $"(do $env.PROMPT_COMMAND)> "',
        "zsh": r'print -n "${(%%)PS1}"',
        "fish": "fish_prompt",
    }

    cmd = cmds.get(shell)
    if cmd:
        try:
            r = subprocess.run(
                [shell_path, "-c", cmd],
                capture_output=True,
                timeout=10,
            )
            if r.returncode == 0:
                raw = r.stdout.decode("utf-8", errors="replace").rstrip("\n")
                # Strip any remaining cursor-movement / OSC sequences that
                # slipped through (keep SGR colour codes).
                raw = re.sub(r"\x1b\[\d*;\d*[Hf]", "", raw)  # absolute position
                raw = re.sub(r"\x1b\[\d*[ABCDEFGST]", "", raw)  # relative movement
                raw = re.sub(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)", "", raw)  # OSC
                raw = re.sub(r"\x1b[78]", "", raw)  # save/restore cursor
                raw = re.sub(r"\x1b\[\?\d+[hl]", "", raw)  # private modes
                if raw:
                    return raw
        except Exception:
            pass

    return "$ "


def run_in_pty(
    cmd: str, rows: int, cols: int, shell: str = "bash", timeout: float = 300.0
) -> tuple[list[tuple[float, str]], float]:
    """Execute *cmd* in a pty and return (chunks, elapsed).

    Args:
        cmd: Shell command to execute.
        rows: Terminal height in rows.
        cols: Terminal width in columns.
        shell: Shell to use (e.g. 'bash', 'zsh', 'nu'). Resolved via shutil.which.
        timeout: Maximum execution time in seconds (default: 300.0 = 5 minutes).

    Returns:
        A tuple of (chunks, elapsed) where chunks is a list of
        (relative_seconds, text) pairs.
    """
    chunks: list[tuple[float, str]] = []
    pid, fd = pty.fork()

    if pid == 0:
        # ── child ──
        winsize = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(1, termios.TIOCSWINSZ, winsize)
        os.environ["TERM"] = "xterm-256color"
        shell_path = shutil.which(shell) or os.environ.get("SHELL", "/bin/sh")
        shell_name = os.path.basename(shell_path)
        os.execlp(shell_path, shell_name, "-c", cmd)

    # ── parent ──
    start = time.monotonic()
    alive = True
    timed_out = False
    while alive:
        elapsed = time.monotonic() - start
        if elapsed > timeout:
            timed_out = True
            break
        rlist, _, _ = select.select([fd], [], [], 1.0)
        if rlist:
            try:
                data = os.read(fd, 4096)
                if not data:
                    break
                chunks.append(
                    (time.monotonic() - start, data.decode("utf-8", errors="replace"))
                )
            except OSError:
                break
        else:
            try:
                rpid, _ = os.waitpid(pid, os.WNOHANG)
            except ChildProcessError:
                break
            if rpid != 0:
                while True:
                    elapsed = time.monotonic() - start
                    if elapsed > timeout:
                        timed_out = True
                        break
                    rlist, _, _ = select.select([fd], [], [], 0.1)
                    if not rlist:
                        break
                    try:
                        data = os.read(fd, 4096)
                        if not data:
                            break
                        chunks.append(
                            (
                                time.monotonic() - start,
                                data.decode("utf-8", errors="replace"),
                            )
                        )
                    except OSError:
                        break
                alive = False

    elapsed = time.monotonic() - start
    os.close(fd)
    if timed_out:
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except (ProcessLookupError, ChildProcessError):
            pass
        print(
            f"Warning: command timed out after {timeout}s: {cmd[:50]}...",
            file=sys.stderr,
        )
    else:
        try:
            os.waitpid(pid, 0)
        except ChildProcessError:
            pass
    return chunks, elapsed


def generate(spec_path: str, output_override: str | None = None) -> None:
    """Parse a YAML spec file and generate an asciinema v3 .cast file.

    Args:
        spec_path: Path to the YAML specification file.
        output_override: Optional output path for the .cast file. If omitted,
            falls back to the spec's ``output`` key, then to the input filename
            with a .cast extension.

    The YAML spec supports the following keys:
        cols: Terminal width in columns (default: 80, must be positive integer)
        rows: Terminal height in rows (default: 24, must be positive integer)
        type_delay: Base delay between keystrokes in seconds (default: 0.04)
        type_variance: Random variance factor for typing delays (default: 0.6)
        pause_after_cmd: Pause after command completes in seconds (default: 1.0)
        shell: Shell to run commands with, e.g. 'bash', 'zsh', 'nu' (default: 'bash')
        prompt: Override the prompt string (default: auto-captured from the shell)
        output: Output file path (optional)
        steps: List of steps, each being a dict with 'cmd', 'marker', or 'poster'

    Raises:
        SystemExit: If the spec file is empty, has invalid values, or contains
            no cmd entries in steps.
    """
    with open(spec_path) as f:
        spec = yaml.safe_load(f)

    if spec is None:
        sys.exit(f"Error: {spec_path} is empty or contains only comments")

    # ── Resolve settings ──────────────────────────────────────────
    cols = spec.get("cols", 80)
    rows = spec.get("rows", 24)
    type_delay = spec.get("type_delay", 0.04)
    type_variance = spec.get("type_variance", 0.6)
    pause_after_cmd = spec.get("pause_after_cmd", 1.0)
    shell = spec.get("shell", "bash")
    prompt_override = spec.get("prompt")
    steps = spec.get("steps", [])

    # ── Validate inputs ───────────────────────────────────────────
    if not isinstance(cols, int) or cols <= 0:
        sys.exit(f"Error: cols must be a positive integer, got {cols!r}")
    if not isinstance(rows, int) or rows <= 0:
        sys.exit(f"Error: rows must be a positive integer, got {rows!r}")
    if not isinstance(type_delay, (int, float)) or type_delay < 0:
        sys.exit(f"Error: type_delay must be a non-negative number, got {type_delay!r}")
    if not isinstance(type_variance, (int, float)) or type_variance < 0:
        sys.exit(
            f"Error: type_variance must be a non-negative number, got {type_variance!r}"
        )
    if not isinstance(pause_after_cmd, (int, float)) or pause_after_cmd < 0:
        sys.exit(
            f"Error: pause_after_cmd must be a non-negative number, got {pause_after_cmd!r}"
        )

    if output_override:
        output = output_override
    elif spec.get("output"):
        output = spec["output"]
    else:
        base, _ = os.path.splitext(spec_path)
        output = base + ".cast"

    if not any(isinstance(s, dict) and "cmd" in s for s in steps):
        sys.exit("Error: steps must contain at least one cmd entry")

    # ── Capture the shell's real prompt ───────────────────────────
    if prompt_override is not None:
        prompt = prompt_override
    else:
        prompt = _capture_prompt(shell)

    # ── Build cast events (absolute timestamps internally) ────────
    events = []
    t = 0.0
    poster_time = None

    for step in steps:
        if isinstance(step, dict) and "cmd" in step:
            cmd = step["cmd"] or ""
            events.append([t, "o", prompt])

            for ch in cmd.rstrip("\n"):
                t += random_typing_delay(type_delay, type_variance)
                events.append([t, "o", "\r\n" if ch == "\n" else ch])

            t += 0.3
            events.append([t, "o", "\r\n"])

            if cmd:
                chunks, elapsed = run_in_pty(cmd, rows, cols, shell=shell)
                for rel_t, data in chunks:
                    data = _SCREEN_OPS.sub("", data)
                    if data:
                        events.append([t + rel_t, "o", data])
                t += elapsed + pause_after_cmd
            else:
                pass

        elif isinstance(step, dict) and "marker" in step:
            events.append([t, "m", step["marker"]])

        elif step == "poster" or (isinstance(step, dict) and "poster" in step):
            poster_time = round(t, 6)

    events.append([t, "o", prompt + "\r\n"])

    # ── Convert to asciicast v3 deltas (time since previous event) ─
    delta_events = []
    prev_t = 0.0
    for abs_t, etype, data in events:
        delta = abs_t - prev_t
        delta_events.append([round(max(delta, 0.0), 6), etype, data])
        prev_t = abs_t

    # ── Write the .cast file ──────────────────────────────────────
    header = {
        "version": 3,
        "term": {"cols": cols, "rows": rows, "type": "xterm-256color"},
        "timestamp": int(time.time()),
        "env": {"SHELL": os.environ.get("SHELL", "/bin/bash")},
    }
    if poster_time is not None:
        header["poster_time"] = poster_time

    with open(output, "w") as f:
        f.write(json.dumps(header) + "\n")
        for ev in delta_events:
            f.write(json.dumps(ev) + "\n")

    # ── Summary ───────────────────────────────────────────────────
    markers = sum(1 for s in steps if isinstance(s, dict) and "marker" in s)
    size = os.path.getsize(output)
    print(f"Cast file: {output} ({size:,} bytes)")
    print(f"Duration:  {t:.1f}s")
    print(f"Events:    {len(delta_events)}")
    print(f"Markers:   {markers}")
    if poster_time is not None:
        print(f"Poster:    {poster_time}s")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} spec.yaml [output.cast]")
    generate(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
