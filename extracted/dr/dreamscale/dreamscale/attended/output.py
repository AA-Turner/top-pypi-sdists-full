"""Minimal attended-task milestones with full diagnostic output retained on disk."""

from __future__ import annotations

import os
import re
import time
from contextlib import suppress
from pathlib import Path

from dreamscale.config import dreamscale_home
from dreamscale.terminal import make_progress_printer


def open_diagnostic_log(name: str, robot: str = "yam"):
    directory = dreamscale_home() / "logs" / robot
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name}-{time.time_ns()}-{os.getpid()}.log"
    return path, open(path, "x", encoding="utf-8", buffering=1, opener=_private_file)


def _private_file(path, flags):
    return os.open(path, flags, 0o600)


class ProgressPrinter:
    def __init__(self, *, verbose=False, log_path=None, console=None, clock=time.monotonic,
                 robot="yam"):
        self._printer = make_progress_printer(console=console, clock=clock)
        self._verbose = verbose
        self._executing = False
        self._compute_ready = False
        self._last = None
        self._muted = False
        self._log = None
        try:
            if log_path is None:
                self.log_path, self._log = open_diagnostic_log("cli", robot)
            else:
                self.log_path = Path(log_path)
                self._log = open(self.log_path, "a", encoding="utf-8", buffering=1,
                                               opener=_private_file)
        except OSError:
            self._log_unavailable()

    def _log_unavailable(self):
        self._verbose = True
        self._printer("Diagnostic log unavailable; showing full details.")

    @property
    def console(self):
        """The terminal, for output drawn directly (live agent turns); None once muted."""
        return None if self._muted else self._printer.console

    def log(self, message):
        """Keep a line in the diagnostic log without drawing it."""
        if self._log is not None:
            try:
                self._log.write(str(message) + "\n")
            except OSError:
                self._log_unavailable()
                with suppress(OSError):
                    self._log.close()
                self._log = None

    def __call__(self, message):
        message = str(message)
        self.log(message)
        if self._muted:
            return
        for line in message.splitlines():
            display = line if self._verbose else self._milestone(line)
            if not self._verbose and display == self._last == "Preparing task…":
                continue  # one milestone, however many steps report it
            if display is not None:
                self._last = display
                self._printer(display)

    def _milestone(self, line):
        if line.startswith("Starting compute"):
            # Each task starts its compute first, before anything moves.
            self._executing = self._compute_ready = False
            return "Starting compute…"
        if line.startswith(("Homing arms", "Homing arm…")):
            return "Homing…"
        if line.startswith("Homing ramp complete"):
            return "✓ Homed"
        if line.startswith("Checking the first prediction"):
            return "Checking the first prediction…"
        if line.startswith("Compute is ready"):
            if self._compute_ready:
                return None
            self._compute_ready = True
            return line
        if line == "Inference started.":
            return None
        if line == "Executing model actions.":
            return "Running · Ctrl+C to stop"
        if line.startswith("Executing with current observations"):
            self._executing = True
            return "Preparing task…"
        if line.startswith("Task stopped. Enter another instruction"):
            return "Stopped · arms holding"
        if line == "Disconnecting local hardware…":
            return "Disconnecting…"
        # Suppress only known routine details. Errors, warnings, hold failures
        # and unfamiliar future messages always reach the terminal.
        if line.startswith((
            "Confirm top/left/right camera views",
            "Confirm the side and wrist camera views",
            "Instruction: ",
            "Connected to session-scoped compute.",
            "Runtime selected: ",
            "Policy is ready for inference.",
            "Task ready.",
            "Initial prediction recorded: ",
            "Recording: ",
            "Recording saved: ",
            "Run failed: ",
            "  control: ", "  startup: ", "  dispatch: ", "  policy: ",
            "  data-plane RTT: ", "  worker: ", "  buffer: ", "  route: ",
            "Cloud task closed",
            "Prediction only: ",
            "Cartesian conversion: ",
            "Largest requested joint change from current pose: ",
            "Region latency check was unavailable; used deterministic fallback ",
            "Region latency check was partial; selected ",
        )):
            return None
        if re.match(
            r"^(Left|Right|Arm): (?:\w+ · |joints |measured-pose hold commanded\.$)", line,
        ):
            return None
        return line

    def mute(self):
        """Keep logging but stop drawing, e.g. once another program owns the terminal."""
        self._muted = True
        self._printer.close()

    def close(self):
        self._printer.close()
        if self._log is not None:
            self._log.close()
            self._log = None


# Pre-refactor name, kept for callers of the YAM modules.
YamProgressPrinter = ProgressPrinter
