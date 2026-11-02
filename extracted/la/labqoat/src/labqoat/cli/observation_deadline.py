"""CLI-owned wall-clock observation deadline independent of HTTP and execution timeouts."""

import math
import signal
import re
from contextlib import contextmanager
from collections.abc import Iterator
from time import monotonic
from types import FrameType

import click

from labqoat.cli.output.cli_failure import CliFailure


class ObservationDeadline:
    """Interrupt blocking observation on the CLI thread and restore the previous signal state."""

    def __init__(self, seconds: float | None, resource_id: str | None = None) -> None:
        """Retain only local observation policy; never change server-side deadlines."""
        self.seconds = seconds
        self.resource_id = resource_id
        if seconds is not None and (not math.isfinite(seconds) or seconds <= 0):
            raise click.UsageError("--wait-timeout must be a positive finite number.")

    @staticmethod
    def option() -> click.Option:
        """Add an optional observer timeout without a default execution deadline."""
        return click.Option(
            ["--timeout", "--wait-timeout", "wait_timeout"],
            type=str,
            help="Disconnect observation after a duration such as 30s or 2m; accepted work continues.",
            callback=ObservationDeadline.validate,
        )

    @staticmethod
    def validate(_ctx: click.Context, _param: click.Parameter, value: float | str | None) -> float | None:
        """Reject invalid timeout values during parsing, before any remote mutation."""
        seconds = ObservationDeadline.parse(value)
        ObservationDeadline(seconds)
        return seconds

    @staticmethod
    def parse(value: float | str | None) -> float | None:
        """Accept explicit seconds, minutes and hours without changing HTTP timeout policy."""
        if not isinstance(value, str):
            return value
        match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)([smh]?)", value)
        if match is None:
            raise click.BadParameter("Expected positive seconds or a duration such as 30s or 2m.")
        return float(match[1]) * {"": 1, "s": 1, "m": 60, "h": 3600}[match[2]]

    @classmethod
    def current(cls, resource_id: str | None = None) -> "ObservationDeadline":
        """Read the leaf or authored launch group's local option."""
        context = click.get_current_context()
        value = context.params.get("wait_timeout")
        if value is None and context.parent is not None:
            value = context.parent.params.get("wait_timeout")
        return cls(value, resource_id)

    def expired(self, _signal: int, _frame: FrameType | None) -> None:
        """Raise a distinct local timeout after preserving the reconnectable identity."""
        raise CliFailure("Observation timed out. Accepted work continues.", 3, resource_id=self.resource_id)

    @contextmanager
    def watching(self) -> Iterator[None]:
        """Unwind response/client contexts on expiry, Ctrl-C, and ordinary completion."""
        if self.seconds is None:
            yield
            return
        previous = signal.getsignal(signal.SIGALRM)
        started = monotonic()
        signal.signal(signal.SIGALRM, self.expired)
        timer = signal.setitimer(signal.ITIMER_REAL, self.seconds)
        try:
            yield
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)
            if timer[0] > 0:
                signal.setitimer(signal.ITIMER_REAL, max(0.000001, timer[0] - (monotonic() - started)), timer[1])
