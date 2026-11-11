"""The program a command asks its shim to start (`probe exec`'s, T42): the shim's own child.

The one thing the shim runs itself, because joining is impossible: the user's program belongs
where they launched `probe exec` (their terminal's process group, cgroup, Slurm allocation, GPUs).
Everything around it (the run, its log, its outputs, its close) stays in the service's command,
which asks over the launcher channel (`probe.sdk.run.launch.program` has the wire) and is told
the program's pid and, later, its exit status.
"""

from __future__ import annotations

import contextlib
import json
import os
import signal
import socket
import subprocess

from probe.foundation.service_api.env import SERVICE_OWNED_ENV

#: While the program outlives the service: these reach it from the terminal already (its own
#: process group is the shim's), the rest are passed on.
TERMINAL_SIGNALS = ("SIGINT", "SIGQUIT", "SIGTSTP")
PASSED_ON = ("SIGTERM", "SIGHUP")


class ProgramLauncher:
    """The shim's end of its command's launcher channel: one program at a time."""

    def __init__(self, channel: socket.socket, held: socket.socket) -> None:
        self.channel = channel
        #: Our copy of the command's end while it is in flight (alone there, macOS may collect it):
        #: let go at the command's first message, else a reply to a command gone blocks for good.
        self.held: socket.socket | None = held
        self.program: subprocess.Popen | None = None
        self._buffer = b""
        self._fds: list[int] = []
        self.is_open = True

    def receive(self) -> None:
        """What the command sent: a program to start, or a signal for it."""
        try:
            data, fds, _flags, _addr = socket.recv_fds(self.channel, 65536, 2)
        except OSError:
            data, fds = b"", []
        self._fds.extend(fds)
        if not data:
            self.is_open = False
            self._close_fds()
            return
        self._close_held()  # the command wrote this: its end has arrived
        self._buffer += data
        while b"\n" in self._buffer:
            line, self._buffer = self._buffer.split(b"\n", 1)
            with contextlib.suppress(ValueError):
                message = json.loads(line.decode("utf-8"))
                if isinstance(message, dict) and "argv" in message:
                    self._start(message)
                elif isinstance(message, dict) and isinstance(message.get("signal"), int) and self.program:
                    with contextlib.suppress(OSError):
                        self.program.send_signal(message["signal"])

    def wait_alone(self) -> int:
        """The service went away while the program runs (H5): wait for it here, passing
        SIGTERM and SIGHUP on; its exit status as a shell reports it (128 + N for a signal)."""
        program = self.program
        if program is None:
            return 70
        for name in TERMINAL_SIGNALS:
            with contextlib.suppress(Exception):
                signal.signal(getattr(signal, name), signal.SIG_IGN)
        for name in PASSED_ON:
            with contextlib.suppress(Exception):
                signal.signal(getattr(signal, name), lambda number, _frame: program.send_signal(number))
        code = program.wait()
        return 128 - code if code < 0 else code

    def report_exit(self) -> None:
        """The program ended: its status goes to the command."""
        if self.program is None or self.program.poll() is None:
            return
        self._send({"exit": self.program.returncode})
        self.program = None

    def _start(self, request: dict) -> None:
        named = request.get("fds") or []
        streams = dict(zip(named, self._fds))
        env = request.get("env")
        if isinstance(env, dict):
            # What the service set on its command (M6) would name that command, not this program.
            env = {name: value for name, value in env.items() if name not in SERVICE_OWNED_ENV}
        try:
            self.program = subprocess.Popen(  # noqa: S603 -- the person's own program, as `probe exec` was given it
                [str(a) for a in request["argv"]], cwd=request.get("cwd") or None,
                env={str(k): str(v) for k, v in env.items()} if isinstance(env, dict) else None,
                stdout=streams.get("stdout"), stderr=streams.get("stderr"),
            )
        except (OSError, ValueError, TypeError) as exc:
            self._send({"error": f"could not run {request['argv'][0]!r}: {exc}"})
        else:
            self._send({"pid": self.program.pid})
        finally:
            self._close_fds()

    def close(self) -> None:
        """The command ended: the channel goes, with our copy of its end if still held."""
        self.channel.close()
        self._close_held()

    def _close_held(self) -> None:
        if self.held is not None:
            self.held.close()
            self.held = None

    def _send(self, message: dict) -> None:
        with contextlib.suppress(OSError):
            self.channel.sendall(json.dumps(message).encode("utf-8") + b"\n")

    def _close_fds(self) -> None:
        while self._fds:
            with contextlib.suppress(OSError):
                os.close(self._fds.pop())
