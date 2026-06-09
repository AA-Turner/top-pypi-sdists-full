#! /usr/bin/env python3

# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///

"""Generate an asciinema v3 .cast file from a YAML spec.

Usage:  python gen_asciicast.py spec.yaml [output.cast]

If output is omitted it falls back to the spec's `output` key,
then to the input filename with a .cast extension.

Example:
    # demo.yaml
    cols: 100
    rows: 30
    type_delay: 0.04
    type_variance: 0.7
    pause_after_cmd: 1.0
    steps:
    - marker: "Hello"
    - cmd: "echo 'Hello, world!'"

    - marker: "Yahoo chart"
    - cmd: "# Printing stock charts"
    - cmd: "termseries yahoo tsla aapl"

    - marker: "Yahoo chart, indexed"
    - cmd: "termseries --mode indexed yahoo --period 1y tsla aapl"

Security and Robustness Notes:
    - Commands from the YAML spec are executed in a PTY. Only use trusted YAML files.
    - A 5-minute timeout prevents runaway commands from hanging indefinitely.
    - Shell is resolved via `shutil.which("bash")` with fallback to $SHELL or /bin/sh.
    - Input validation ensures cols/rows are positive integers and delays are non-negative.
    - Empty YAML files produce a clear error message rather than failing silently.
"""

import fcntl
import json
import os
import pty
import random
import select
import shutil
import struct
import sys
import termios
import time

import yaml


def random_typing_delay(type_delay: float, type_variance: float) -> float:
    """Return a randomised per-character delay (seconds).

    Args:
        type_delay: Base delay between keystrokes in seconds.
        type_variance: Variance factor (0-1) for randomizing delays.
            A value of 0.6 means delays vary by up to ±60%.

    Returns:
        A delay value in seconds, minimum 0.005s.
    """
    jitter = (random.random() * 2 - 1) * type_variance
    return max(type_delay * (1 + jitter), 0.005)


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
            Commands exceeding this limit are killed with SIGKILL.

    Returns:
        A tuple of (chunks, elapsed) where:
            - chunks: List of (relative_seconds, text) tuples capturing output
            - elapsed: Total execution time in seconds

    Note:
        Each chunk captures real terminal output including ANSI codes
        and \\r\\n translation. If the command times out, a warning is
        printed to stderr but partial output is still returned.
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
            os.kill(pid, 9)  # SIGKILL
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
            falls back to the spec's `output` key, then to the input filename
            with a .cast extension.

    The YAML spec supports the following keys:
        cols: Terminal width in columns (default: 80, must be positive integer)
        rows: Terminal height in rows (default: 24, must be positive integer)
        type_delay: Base delay between keystrokes in seconds (default: 0.04)
        type_variance: Random variance factor for typing delays (default: 0.6)
        pause_after_cmd: Pause after command completes in seconds (default: 1.0)
        shell: Shell to run commands with, e.g. 'bash', 'zsh', 'nu' (default: 'bash')
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

    # ── Build cast events (absolute timestamps internally) ────────
    events = []
    t = 0.0
    poster_time = None

    for step in steps:
        if isinstance(step, dict) and "cmd" in step:
            cmd = step["cmd"] or ""
            events.append([t, "o", "$ "])

            for ch in cmd:
                t += random_typing_delay(type_delay, type_variance)
                events.append([t, "o", ch])

            t += 0.3
            events.append([t, "o", "\r\n"])

            if cmd:
                chunks, elapsed = run_in_pty(cmd, rows, cols, shell=shell)
                for rel_t, data in chunks:
                    events.append([t + rel_t, "o", data])
                t += elapsed + pause_after_cmd
            else:
                pass

        elif isinstance(step, dict) and "marker" in step:
            events.append([t, "m", step["marker"]])

        elif step == "poster" or (isinstance(step, dict) and "poster" in step):
            poster_time = round(t, 6)

    events.append([t, "o", "$ \r\n"])

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
