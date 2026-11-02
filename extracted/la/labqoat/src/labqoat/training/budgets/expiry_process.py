"""Independent grant expiry process unaffected by a training interpreter's GIL or API calls."""

import math
import os
import select
import signal
import sys
import time
from typing import BinaryIO


class ExpiryProcess:
    """Terminate only the captured parent-owned isolated process group at its monotonic deadline."""

    @classmethod
    def run(cls, parent: int, deadline: float, channel: BinaryIO, replies: BinaryIO) -> None:
        """Acknowledge each armed deadline; disconnection or invalid renewal fails closed."""
        try:
            cls._validate(parent, deadline)
            while True:
                replies.write(b"armed\n")
                replies.flush()
                if not select.select([channel], [], [], max(0.0, deadline - time.monotonic()))[0]:
                    break
                command = channel.readline(128)
                if command == b"stop\n":
                    return
                renewal = float(command)
                cls._validate(parent, renewal)
                if time.monotonic() >= deadline or renewal <= deadline:
                    break
                deadline = renewal
        except (OSError, ValueError):
            pass
        cls._terminate(parent)

    @staticmethod
    def _validate(parent: int, deadline: float) -> None:
        """Limit supervisor authority to its still-live isolated parent and bounded future grants."""
        if parent <= 1 or os.getppid() != parent or os.getpgid(parent) != parent:
            raise ValueError("Fit supervision requires a parent-owned isolated process group")
        remaining = deadline - time.monotonic()
        if not math.isfinite(deadline) or not 0 < remaining <= 60:
            raise ValueError("Fit expiry must be bounded and in the future")

    @staticmethod
    def _terminate(parent: int) -> None:
        """Parent identity checks prevent targeting a recycled PID after the original invocation exits."""
        if parent > 1 and os.getppid() == parent:
            try:
                if os.getpgid(parent) == parent:
                    os.killpg(parent, signal.SIGKILL)
            except ProcessLookupError:
                pass

    @classmethod
    def main(cls) -> None:
        """Run only as the explicitly spawned expiry helper, with no network or credential access."""
        cls.run(int(sys.argv[1]), float(sys.argv[2]), sys.stdin.buffer, sys.stdout.buffer)
