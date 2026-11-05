"""The shim's signals, passed on to its command (`cli.signal`, D5).

The terminal signals the shim (it is the foreground job), never the command: the command runs in
the service's process tree. So each signal a terminal or a parent sends goes on to the command's
process group. A handler only notes the signal and wakes the shim's loop through a self-pipe
(`read_fd`); the loop sends `cli.signal` without waiting for its answer (`flush`), and reads the
answers off the connection when they come (`drain_answers`). Ctrl-Z stops the command (the
service sends SIGSTOP), then the shim itself; `fg` continues the shim, whose SIGCONT continues
the command.
"""

from __future__ import annotations

import collections
import contextlib
import os
import signal

from probe.foundation.service_api.service_api import Connection
from probe.foundation.service_api.wire import Method, encode, request

#: What the shim passes on (`commands.FORWARDED` on the service's side).
FORWARDED = ("SIGINT", "SIGTERM", "SIGHUP", "SIGWINCH", "SIGTSTP", "SIGCONT", "SIGQUIT")


class SignalForwarder:
    """While the command waits or runs: each FORWARDED signal goes to it as `cli.signal`."""

    def __init__(self, connection: Connection, command_id: str) -> None:
        self.connection = connection
        self.command_id = command_id
        self.read_fd, self._write_fd = os.pipe()
        os.set_blocking(self.read_fd, False)
        os.set_blocking(self._write_fd, False)
        self._noted: collections.deque[int] = collections.deque()
        self._previous: dict[int, object] = {}
        self.is_connected = True

    def __enter__(self) -> SignalForwarder:
        for name in FORWARDED:
            if hasattr(signal, name):
                number = int(getattr(signal, name))
                self._previous[number] = signal.signal(number, self._handle_signal)
        return self

    def __exit__(self, *exc: object) -> None:
        self.restore()
        for fd in (self.read_fd, self._write_fd):
            with contextlib.suppress(OSError):
                os.close(fd)

    def restore(self) -> None:
        """The handlers from before (the command ended, or the service went away)."""
        for number, previous in self._previous.items():
            with contextlib.suppress(Exception):
                signal.signal(number, previous)
        self._previous = {}

    def _handle_signal(self, number: int, _frame: object) -> None:
        self._noted.append(number)
        with contextlib.suppress(OSError):
            os.write(self._write_fd, b"\0")

    def flush(self) -> None:
        """Send every noted signal (the self-pipe woke the loop)."""
        with contextlib.suppress(OSError):
            while os.read(self.read_fd, 512):
                pass
        while self._noted:
            name = signal.Signals(self._noted.popleft()).name
            self.send_signal(name)
            if name == "SIGTSTP":
                # The command stopped; now this job stops too, as the shell expects. `fg` resumes it here.
                handler = signal.signal(signal.SIGTSTP, signal.SIG_DFL)
                os.kill(os.getpid(), signal.SIGTSTP)
                signal.signal(signal.SIGTSTP, handler)

    def send_signal(self, name: str) -> None:
        """`cli.signal`, written without waiting for its answer."""
        if not self.is_connected:
            return
        self.connection._next_id += 1  # noqa: SLF001 -- after `service.hello` and `cli.run`
        message = request(self.connection._next_id, Method.CLI_SIGNAL, {"command": self.command_id, "signal": name})  # noqa: SLF001
        try:
            self.connection.sock.sendall(encode(message))
        except OSError:
            self.is_connected = False

    def drain_answers(self) -> None:
        """The connection is readable: `cli.signal`'s answers (dropped), or its end."""
        try:
            if not self.connection.sock.recv(65536):
                self.is_connected = False
        except (BlockingIOError, InterruptedError):
            return
        except OSError:
            self.is_connected = False
