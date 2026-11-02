"""Terminal-safe public summaries, motion descriptions and transient progress."""

import json
import re
import time
import unicodedata
from contextlib import contextmanager, suppress

from rich.console import Console
from rich.padding import Padding
from rich.text import Text

# Strip terminal commands before constructing literal Rich Text. C1 forms and
# unterminated OSC strings must not become terminal output either.
ANSI = re.compile(
    r"(?:\x1b\[|\x9b)[0-?]*[ -/]*[@-~]"
    r"|(?:\x1b\]|\x9d)[^\x07\x1b\x9c]*(?:\x07|\x1b\\|\x9c|$)"
)


def clean(value, limit=None):
    value = ANSI.sub("", str(value))
    value = "".join(
        " " if c.isspace() else c
        for c in value
        if c.isspace() or not unicodedata.category(c).startswith("C")
    )
    value = " ".join(value.split())
    if limit is not None and len(value) > limit:
        return value[: max(0, limit - 1)].rstrip() + "…"
    return value


def elapsed(seconds):
    minutes, seconds = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{seconds:02d}"


def summary_lines(message):
    """Plain callback output leaves wrapping to its consumer; retain all text."""
    message = clean(message)
    return ["  " + message] if message else []


def action_lines(adapter, call, observation):
    formatter = getattr(adapter, "describe_action", None)
    try:
        lines = formatter(call, observation) if formatter else None
    except Exception:
        lines = None
    # An empty description intentionally omits unchanged command components.
    if lines is None:
        lines = [
            f"{call.name} → {json.dumps(call.arguments, ensure_ascii=False, separators=(',', ':'))}"
        ]
    return ["  " + clean(line) for line in lines]


class _ThinkingLine:
    def __init__(self, turn, started, clock):
        self.turn, self.started, self.clock = turn, started, clock

    def __rich_console__(self, console, options):
        yield Text(f"Turn {self.turn} · {elapsed(self.clock() - self.started)}")


class AgentDisplay:
    """Rich output for the default terminal; plain strings for SDK callbacks."""

    def __init__(self, print_fn=print, *, console=None, clock=time.monotonic):
        self._print = print_fn
        self._clock = clock
        self._started = clock()
        self._fixed_console = console
        if console is None and print_fn is print:
            with suppress(Exception):
                self._fixed_console = Console(highlight=False)
        self._status = None

    @property
    def _console(self):
        # The CLI's printer lends its terminal (clearing its own live status) and keeps
        # the diagnostic log; anything else gets plain strings.
        if self._fixed_console is not None:
            return self._fixed_console
        try:
            return getattr(self._print, "console", None)
        except Exception:
            return None

    def _write(self, message, *, style="", indent=False):
        # Output errors must never interrupt a robot's stop/recovery path.
        with suppress(Exception):
            message = clean(message)
            if not message:
                return
            line = ("  " if indent else "") + message
            console = self._console
            if console is None:
                self._print(line)
                return
            log = getattr(self._print, "log", None)
            if log is not None:
                log(line)
            text = Text(message, style=style)
            console.print(Padding(text, (0, 0, 0, 2), expand=False) if indent else text)

    def info(self, message):
        self._write(message)

    def summary(self, message):
        # This is the provider's public summary only, never private reasoning.
        self._write(message, style="dim grey62", indent=True)

    def motion(self, message):
        self._write(message, style="cyan", indent=True)

    def warning(self, message):
        self._write(message, style="yellow")

    @contextmanager
    def thinking(self, turn):
        self.close()
        console = self._console
        interactive = console is not None and console.is_interactive
        if interactive:
            try:
                self._status = console.status(
                    _ThinkingLine(turn, self._started, self._clock),
                    spinner="line",
                    spinner_style="bold cyan",
                    refresh_per_second=12.5,
                )
                self._status.start()
            except Exception:
                self.close()
        else:
            self.info(f"Turn {turn} · {elapsed(self._clock() - self._started)}")
        try:
            yield
        finally:
            self.close()
        if interactive:
            self.info(f"Turn {turn} · {elapsed(self._clock() - self._started)}")

    def close(self):
        status, self._status = self._status, None
        if status is not None:
            with suppress(Exception):
                status.stop()
