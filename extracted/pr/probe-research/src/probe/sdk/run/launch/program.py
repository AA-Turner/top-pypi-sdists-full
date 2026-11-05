"""Start the program a run wraps: here, or by the `probe` shim when this command runs in the service (T42).

A `probe exec` runs as a child of the Probe service (`cli.run`), but its program must start where
the person launched `probe exec`: their terminal, cgroup, Slurm allocation, GPUs. So the shim
stays a minimal waiting parent: the command hands it the program over the launcher channel
(LAUNCHER_FD_ENV, set by the service on every command), and `ShimProcess` stands in for the
`subprocess.Popen` it would have been. Wire, one program at a time:

    command -> shim   {"argv", "cwd", "env", "fds": ["stdout", "stderr"]}\\n  + those fds (SCM_RIGHTS)
    shim -> command   {"pid": N}\\n  (or {"error": "..."}\\n), later {"exit": returncode}\\n
    command -> shim   {"signal": N}\\n
"""

from __future__ import annotations

import contextlib
import json
import os
import select
import socket
import subprocess
import time

from ....foundation.service_api.env import SERVICE_OWNED_ENV

#: The fd of this command's launcher channel to its shim (set by the service, never the caller).
LAUNCHER_FD_ENV = "PROBE_LAUNCHER_FD"


def get_program_env(env: dict | None) -> dict:
    """The program's environment: `env` (else this process's), less what the service set on this
    command (`env.SERVICE_OWNED_ENV`, M6): the program, the shim's own child, finds its caller
    as its parent anyway."""
    source = os.environ if env is None else env
    return {name: value for name, value in source.items() if name not in SERVICE_OWNED_ENV}


def start_program(argv: list[str], *, cwd: str | None = None, env: dict | None = None, stdout=None,
                  stderr=None) -> subprocess.Popen | ShimProcess:
    """`subprocess.Popen(argv, ...)`, by the shim when this command has one (its stdin is the shim's)."""
    channel = _get_channel()
    env = get_program_env(env)
    if channel is None:
        return subprocess.Popen(argv, cwd=cwd, env=env, stdout=stdout, stderr=stderr)  # noqa: S603 -- the run's own program
    return ShimProcess(channel, argv, cwd=cwd, env=env, stdout=stdout, stderr=stderr)


def run_program(argv: list[str], *, cwd: str | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    """`subprocess.run(argv, cwd=..., env=..., check=False)`, through `start_program`: on Ctrl-C the
    program gets a moment to end on its own (it took the same Ctrl-C), then is killed."""
    channel = _get_channel()
    env = get_program_env(env)
    if channel is None:
        return subprocess.run(argv, cwd=cwd, env=env, check=False)  # noqa: S603 -- the run's own program
    process = ShimProcess(channel, argv, cwd=cwd, env=env)
    try:
        return subprocess.CompletedProcess(argv, process.wait())
    except KeyboardInterrupt:
        with contextlib.suppress(subprocess.TimeoutExpired):
            process.wait(timeout=0.25)
        process.kill()
        process.wait()
        raise


def _get_channel() -> socket.socket | None:
    raw = os.environ.get(LAUNCHER_FD_ENV, "")
    if not raw.isdigit():
        return None
    try:
        channel = socket.socket(fileno=os.dup(int(raw)))
    except OSError:
        return None
    if channel.family != socket.AF_UNIX:
        channel.close()
        return None
    return channel


class ShimProcess:
    """A program the shim started (its own child): what `subprocess.Popen` offers of one."""

    def __init__(self, channel: socket.socket, argv: list[str], *, cwd: str | None, env: dict | None,
                 stdout=None, stderr=None) -> None:
        self.args = list(argv)
        self.channel = channel
        self.returncode: int | None = None
        self._buffer = b""
        named, fds = [], []
        for name, stream in (("stdout", stdout), ("stderr", stderr)):
            if stream is not None:
                named.append(name)
                fds.append(stream if isinstance(stream, int) else stream.fileno())
        request = {"argv": self.args, "cwd": os.path.abspath(cwd) if cwd else os.getcwd(),
                   "env": dict(os.environ if env is None else env), "fds": named}
        data = json.dumps(request).encode("utf-8") + b"\n"
        sent = socket.send_fds(channel, [data[:65536]], fds) if fds else channel.send(data[:65536])
        if sent < len(data):
            channel.sendall(data[sent:])
        answer = self._read(None)
        if answer is None or not isinstance(answer.get("pid"), int):
            channel.close()
            raise OSError((answer or {}).get("error") or "the probe shim did not start the program")
        self.pid = answer["pid"]

    def _read(self, timeout: float | None) -> dict | None:
        deadline = None if timeout is None else time.monotonic() + timeout
        while b"\n" not in self._buffer:
            left = None if deadline is None else max(0.0, deadline - time.monotonic())
            ready, _, _ = select.select([self.channel], [], [], left)
            if not ready:
                raise subprocess.TimeoutExpired(self.args, timeout)
            chunk = self.channel.recv(65536)
            if not chunk:
                return None
            self._buffer += chunk
        line, self._buffer = self._buffer.split(b"\n", 1)
        message = json.loads(line.decode("utf-8"))
        return message if isinstance(message, dict) else None

    def poll(self) -> int | None:
        if self.returncode is None:
            with contextlib.suppress(subprocess.TimeoutExpired):
                self.wait(timeout=0)
        return self.returncode

    def wait(self, timeout: float | None = None) -> int:
        while self.returncode is None:
            message = self._read(timeout)
            if message is None:
                self.returncode = -9  # the shim is gone, and its program with it: as a kill
            elif isinstance(message.get("exit"), int):
                self.returncode = message["exit"]
        return self.returncode

    def send_signal(self, number: int) -> None:
        if self.returncode is None:
            with contextlib.suppress(OSError):
                self.channel.sendall(json.dumps({"signal": int(number)}).encode("utf-8") + b"\n")

    def kill(self) -> None:
        import signal

        self.send_signal(signal.SIGKILL)

    def __enter__(self) -> ShimProcess:
        return self

    def __exit__(self, *exc: object) -> None:
        with contextlib.suppress(Exception):
            self.wait()
        self.channel.close()
