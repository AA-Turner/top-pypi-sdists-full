"""The `probe` command, as its console script runs it: plumbing to the Probe service (service-only T7).

    package     argv, cwd, the whole environment, and fds 0-2 (the terminal, or pipes)
    ensure      a service that answers, started when none does (`start.ensure`)
    cli.run     the service answers a door; the shim connects and waits for its turn (told
                what for: `waiting`, printed after a second), then passes its fds when asked
                (`ready`), forwards its signals (`signals.SignalForwarder`), and waits
    exit        with the command's status: re-raising the signal that ended it, so a shell
                loop stops on Ctrl-C; or `ShimExit` (69 no service, 70 service lost, 75 updating)

A command the service never started (it stopped, or restarts after a `probe service stop`) is
asked of the next service, once. A service older than this shim still runs the command (its
host loads the files on disk) and restarts once nothing runs; only one from before `cli.run`
is replaced here (D15).

It does nothing else: no CLI import, no work of its own (the rule of service-only D1). Stdlib only;
`foundation/service_api` is the one client it uses. The program a command asks for (`probe exec`'s)
is the one thing it starts itself, as a minimal waiting parent (`launches.py`, T42).
"""

from __future__ import annotations

import contextlib
import errno
import hashlib
import json
import os
import select
import signal
import socket
import sys
import time

from probe.foundation.service_api import paths, start
from probe.foundation.service_api.service_api import Connection, ServiceError
from probe.foundation.service_api.vocabularies import Client, CommandStdio, RefusedReason, ShimExit
from probe.foundation.service_api.wire import API_VERSION, ErrorCode, Method, encode, request

#: How long the shim waits for a service it started (a cold start is ~0.3 s; P3 budgets 1 s).
START_WAIT_S = 10.0
#: `service.hello` and `cli.run`'s answer (the door, at once): past it the service is stuck.
ANSWER_TIMEOUT_S = 10.0
#: How long an older service (from before `cli.run`) gets to stop before ours starts (D15).
REPLACE_WAIT_S = 10.0
#: How long a stopping service gets to exit before its command is asked of the next one.
RESTART_WAIT_S = 30.0
#: A command still waiting for its turn after this long says what for, once.
WAITING_NOTICE_S = 1.0
#: The signals that end a shell's job: a command that died of one ends the shim the same way.
REPEATED_DEATHS = ("SIGINT", "SIGTERM", "SIGHUP", "SIGQUIT", "SIGPIPE")
#: Another copy's own service roots (D13): `<machine root>/copies/<hash of its sys.prefix>`.
COPY_KEY_LEN = 12
#: What a person reads when no service can be reached (D4, T39).
REINSTALL_HINT = "reinstall: https://research.prbe.ai/install"
LIFEBOAT_HINT = "repair it with:  /bin/sh {lifeboat} cli    (or " + REINSTALL_HINT + ")"
#: An uninstall that stopped halfway keeps every other `probe` off: these two finish it.
HALFWAY_UNINSTALL = ("an uninstall of Probe stopped halfway; run `probe repair` to finish it and set Probe up "
                     "again, or `probe uninstall` to finish removing it")
#: The end a command that never started carries: asked of the next service once.
NOT_STARTED = "not_started"
NO_HOST = "no_host"


#: A sandbox that may not write the drop folder: what fixes it, never a reinstall link.
SANDBOX_CLOSED = (
    "this sandbox cannot reach the Probe service (it may not write {folder}).\n"
    "  Run `probe wizard` once from your own terminal: it lets your coding agent's sandbox reach Probe.\n"
    "  Or run this command outside the sandbox."
)
#: No service took a sandboxed request (none running, none the OS starts): a sandbox never starts one.
SANDBOX_NO_SERVICE = (
    "the Probe service is not running, and a sandboxed command cannot start it.\n"
    "  Run any `probe` command from your own terminal (it starts the service), then try again."
)


class ShimError(Exception):
    """The shim could not hand the command over: what to print, and its exit status."""

    def __init__(self, message: str, status: int = ShimExit.UNAVAILABLE) -> None:
        super().__init__(message)
        self.status = int(status)


class RetryError(Exception):
    """The service will not run it now but the next one will (it stops or restarts)."""

    def __init__(self, message: str, service_pid: int | None) -> None:
        super().__init__(message)
        self.service_pid = service_pid


def run_command(argv: list[str], version: str) -> int:
    """Run `probe <argv>` in the Probe service; this process's exit status."""
    try:
        choose_service_root(version)
        try:
            return _run_handed_over_twice(argv, version)
        except FencedShim:
            return _run_fenced(argv, version)
    except ShimError as exc:
        print(f"probe: {exc}", file=sys.stderr)
        return exc.status
    except OSError as exc:
        # A folder it could not make (a read-only home), a socket it could not open: never a traceback.
        print(f"probe: could not reach the Probe service ({exc}).\n{_get_hints()}", file=sys.stderr)
        return ShimExit.UNAVAILABLE
    except KeyboardInterrupt:
        # Ctrl-C before its signals went to the command (starting the service, handing it over).
        return 128 + signal.SIGINT


def _run_handed_over_twice(argv: list[str], version: str) -> int:
    """The command handed over with this process's fds (a retry once when the service restarted)."""
    for attempt in range(2):
        try:
            door, connection, command_id, service_pid = _hand_over(argv, version)
        except RetryError as exc:
            if attempt == 0:
                _wait_for_restart(exc.service_pid)
                continue
            raise ShimError(str(exc)) from None
        end, status = _run_handed_over(door, connection, command_id)
        if status is not None:
            return status
        if (end or {}).get("reason") == NOT_STARTED and attempt == 0:
            _wait_for_restart(service_pid)
            continue
        return _finish(end)
    raise ShimError("the Probe service restarted twice before this command started")


def _run_fenced(argv: list[str], version: str) -> int:
    """A sandboxed agent's `probe` (D30): asked through the drop folder (`transports`, Q1 = A), its
    output captured into the answer and printed here (no fds cross a folder, so no terminal: the
    service serves a fenced caller only commands that read or ask). Exit 2 when it is refused."""
    from probe.foundation.service_api import transports

    # The answer comes when the command ends (`probe ask --wait` may take minutes): one wait for it.
    with _explain_closed_sandbox():
        channel = transports.connect(FENCED_ANSWER_WAIT_S, client=Client.CLI, client_version=version)
    parameters = {"argv": list(argv), "argv0": sys.argv[0] if sys.argv else "probe", "cwd": _get_cwd(),
                  "env": dict(os.environ), "stdio": CommandStdio.CAPTURE, "stdin": ""}
    try:
        with _explain_closed_sandbox():  # the request file is written here
            answer = channel.call(Method.CLI_RUN, parameters)
    except ServiceError as exc:
        print(f"probe: {exc.message if hasattr(exc, 'message') else exc}", file=sys.stderr)
        return 2 if (getattr(exc, "data", None) or {}).get("reason") == RefusedReason.SANDBOXED else ShimExit.UNAVAILABLE
    finally:
        channel.close()
    sys.stdout.write(answer.get("stdout") or "")
    sys.stderr.write(answer.get("stderr") or "")
    return _finish(answer)


@contextlib.contextmanager
def _explain_closed_sandbox():
    """A sandbox that may not write the drop folder (an agent set up before its entry existed,
    0.406.0), or no service took the request: what fixes it, never a reinstall link."""
    try:
        yield
    except ConnectionRefusedError:
        raise ShimError(SANDBOX_NO_SERVICE) from None
    except OSError as exc:
        if exc.errno not in (errno.EROFS, errno.EACCES, errno.EPERM):
            raise
        raise ShimError(SANDBOX_CLOSED.format(folder=paths.get_drop_dir())) from None


def choose_service_root(version: str) -> None:
    """A `probe` from another copy than the machine's install (a checkout, a project venv) runs a
    service of its own, on its own code, under its own root (D13): that service records no
    session and serves only this copy's shims. The machine's install is runtime.json's."""
    if os.environ.get(paths.SERVICE_ROOT_ENV):
        return  # named already: a copy's own command runs `probe` again, or a read-only home's root
    recorded = start.runtime_python()
    if recorded is None or is_same_install(recorded):
        return
    digest = hashlib.sha256(os.fsencode(os.path.realpath(sys.prefix))).hexdigest()[:COPY_KEY_LEN]
    os.environ[paths.SERVICE_ROOT_ENV] = str(paths.root_dir() / paths.COPIES_DIRNAME / digest)
    paths.private_dir(paths.root_dir())
    start.write_runtime(sys.executable, version)


def is_same_install(python: str) -> bool:
    """Is `python` (the machine's recorded CLI interpreter) this interpreter, or one of its
    environment? The path as run, never resolved: two venvs' `bin/python` are links to one
    base interpreter. A framework build (Homebrew's) runs from a `bin/` outside its
    `sys.prefix`, so the interpreter's own path counts too."""
    try:
        if os.path.abspath(python) == os.path.abspath(sys.executable):
            return True
        theirs = os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(python))))
        return theirs == os.path.realpath(sys.prefix)
    except OSError:
        return False


def _hand_over(argv: list[str], version: str) -> tuple[socket.socket, Connection, str, int | None]:
    """`cli.run` answered and the door connected: the door (its turn, then the exit status come
    there), the connection (signals go there), the command's id and the service's pid. One
    more try when the service went away before it answered (a restart onto an update)."""
    parameters = {
        "argv": list(argv), "argv0": sys.argv[0] if sys.argv else "probe", "cwd": _get_cwd(),
        "env": dict(os.environ), "stdio": CommandStdio.FDS,
    }
    nofile = _get_open_files_limit()
    if nofile is not None:
        parameters["nofile"] = nofile  # the command gets this process's limit back
    for attempt in range(2):
        connection = _connect(version, is_finishing_uninstall=start.get_command_word(argv) in start.FINISHING_COMMANDS)
        try:
            hello, answer = _call_pipelined(connection, version, parameters)
        except ServiceError as exc:
            connection.close()
            reason = exc.data.get("reason") if isinstance(exc.data, dict) else None
            if exc.code == ErrorCode.UNKNOWN_METHOD and attempt == 0:
                _replace_older_service(version)  # a service from before `cli.run` (D15)
                continue
            if reason == RefusedReason.CALLER_GONE:  # the service is stopping: the next one runs it
                raise RetryError(exc.message, getattr(exc, "service_pid", None)) from None
            if reason == RefusedReason.UNINSTALLING:
                raise ShimError(exc.message) from None
            if reason == RefusedReason.SANDBOXED:  # D30: the same exit as through the drop folder
                raise ShimError(exc.message, status=2) from None
            raise ShimError(f"the Probe service refused this command: {exc.message}") from None
        except TimeoutError:
            connection.close()
            raise ShimError(f"the Probe service did not answer within {ANSWER_TIMEOUT_S:.0f} s: it may be stuck.\n"
                            f"{_get_hints()}") from None
        except OSError:
            connection.close()
            if attempt == 0:
                continue
            raise ShimError("the Probe service closed the connection before it took this command",
                            ShimExit.SERVICE_LOST) from None
        try:
            door = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            door.settimeout(5.0)
            door.connect(answer["socket"])
            door.settimeout(None)
            pid = hello.get("pid")
            return door, connection, str(answer["command"]), pid if isinstance(pid, int) else None
        except (OSError, KeyError, TypeError) as exc:
            connection.close()
            raise ShimError(f"could not pass this terminal to the Probe service: {exc}") from None
    raise ShimError("the Probe service could not be reached")


#: How long a sandboxed agent's command, asked through the drop folder, may take to answer.
FENCED_ANSWER_WAIT_S = 1800.0


class FencedShim(Exception):
    """A sandbox refused this process the service's socket (EPERM / EACCES): it asks through the
    drop folder instead (`_run_fenced`)."""


def _connect(version: str, *, is_finishing_uninstall: bool = False) -> Connection:
    """A connection to this machine's service, starting one when none answers (for `probe
    uninstall` / `probe repair` after an uninstall stopped halfway too: they finish it).
    FencedShim when a sandbox refuses the socket: never a spawn from inside a fence (D19)."""
    try:
        return Connection.open(2.0)
    except PermissionError as exc:
        if exc.errno in (errno.EPERM, errno.EACCES):
            raise FencedShim from None
    except OSError:
        pass
    outcome = _ensure(version, is_finishing_uninstall=is_finishing_uninstall)
    try:
        return Connection.open(2.0)
    except OSError as exc:
        raise ShimError(
            f"the Probe service is not running and did not start ({outcome}: {_explain(outcome, exc)}).\n{_get_hints()}"
        ) from None


def _ensure(version: str, *, is_finishing_uninstall: bool = False) -> str:
    """`ensure`, waiting for the service to answer.
    # SEAM (service-only L1, T37): `ensure(min_version=version)` replaces an older service.
    """
    if start.runtime_python() is None and start.uninstall_barrier() is None:
        # No install recorded (a pip install, a checkout): this interpreter is the CLI's.
        start.write_runtime(sys.executable, version)
    return start.ensure(wait=START_WAIT_S, is_finishing_uninstall=is_finishing_uninstall)


def _explain(outcome: str, exc: OSError) -> str:
    if outcome == start.Ensured.UNINSTALLING and start.is_uninstall_orphaned():
        return HALFWAY_UNINSTALL
    reasons = {
        start.Ensured.UNINSTALLING: start.UNINSTALLING_MESSAGE,
        start.Ensured.BACKOFF: "it failed to start 3 times in the last minute",
        start.Ensured.UNAVAILABLE: "no Python to start it with",
    }
    return reasons.get(outcome, f"no answer: {exc}")


def _get_hints() -> str:
    """Where the service's log is, and how to repair it (the lifeboat only when it is there)."""
    try:
        log = str(paths.log_path())
    except OSError:
        log = "?"
    lifeboat = paths.state_dir() / "lifeboat" / "lifeboat.sh"
    fix = LIFEBOAT_HINT.format(lifeboat=lifeboat) if lifeboat.is_file() else REINSTALL_HINT
    return f"  log: {log}\n  {fix}"


def _replace_older_service(version: str) -> None:
    """The version floor (D15), for a service from before `cli.run` only: it stops, ours starts.
    # SEAM (service-only L1, T37): becomes `ensure(min_version=version)`.
    """
    try:
        with Connection.open(2.0) as connection:
            connection.hello(Client.CLI, version)
            connection.call(Method.STOP)
    except ServiceError as exc:
        raise ShimError(f"an older Probe service runs here and will not stop now ({exc.message}); "
                        "try again in a moment", ShimExit.UPDATING) from None
    except OSError:
        return
    _wait_until_gone()
    _ensure(version)


def _wait_for_restart(service_pid: int | None) -> None:
    """The service stops (or restarts): until its process is gone (it holds its lock until
    then, and `ensure` would wait on it), at most RESTART_WAIT_S."""
    deadline = time.monotonic() + RESTART_WAIT_S
    while service_pid is not None and time.monotonic() < deadline:
        try:
            os.kill(service_pid, 0)
        except ProcessLookupError:
            return
        except OSError:
            break
        time.sleep(0.05)
    _wait_until_gone()


def _wait_until_gone() -> None:
    deadline = time.monotonic() + REPLACE_WAIT_S
    while time.monotonic() < deadline:
        try:
            Connection.open(0.5).close()
        except OSError:
            return
        time.sleep(0.05)


def _call_pipelined(connection: Connection, version: str, parameters: dict) -> tuple[dict, dict]:
    """`service.hello` and `cli.run` in one write; both answers (ServiceError for an error)."""
    hello = {"client": Client.CLI, "client_version": version, "api": API_VERSION}
    connection.sock.settimeout(ANSWER_TIMEOUT_S)
    connection.sock.sendall(encode(request(1, Method.HELLO, hello)) + encode(request(2, Method.CLI_RUN, parameters)))
    connection._next_id = 2  # noqa: SLF001 -- the next call (a signal) numbers after these
    answers: dict = {}
    while len(answers) < 2:
        message = connection._read_message()  # noqa: SLF001
        if message.get("id") not in (1, 2):
            continue
        if "error" in message:
            error = message["error"] or {}
            failure = ServiceError(int(error.get("code", 0)), str(error.get("message", "")), error.get("data"))
            pid = answers.get(1, {}).get("pid")
            failure.service_pid = pid if isinstance(pid, int) else None  # whose restart to wait out
            raise failure
        answers[message["id"]] = message.get("result") or {}
    return answers[1], answers[2]


def _run_handed_over(door: socket.socket, connection: Connection, command_id: str) -> tuple[dict | None, int | None]:
    """Wait for the command's turn, pass the fds, wait for its end. `(end, None)`, or
    `(None, status)` when a program it started outlived the service (H5)."""
    from probe.foundation.cli_shim.launches import ProgramLauncher
    from probe.foundation.cli_shim.signals import SignalForwarder

    launcher = None
    try:
        with SignalForwarder(connection, command_id) as forwarder:
            first = _wait_for_turn(door, forwarder)
            if first is not None:
                return first, None
            launcher = ProgramLauncher(_send_fds(door))
            end = _wait_for_end(door, launcher, forwarder)
            if end is None and launcher.program is not None and launcher.program.poll() is None:
                forwarder.restore()
                print("probe: the Probe service stopped while running this command; "
                      "waiting for the program it started", file=sys.stderr)
                return None, launcher.wait_alone()
            return end, None
    finally:
        door.close()
        if launcher is not None:
            launcher.channel.close()
        connection.close()


def _wait_for_turn(door: socket.socket, forwarder) -> dict | None:
    """Until the service asks for the fds (None), or the command ended before it started (its
    end). What it waits for is printed once it has waited WAITING_NOTICE_S."""
    since = time.monotonic()
    waiting_for: str | None = None
    is_told = False
    buffer = b""
    while True:
        timeout = None
        if waiting_for is not None and not is_told:
            timeout = max(0.0, since + WAITING_NOTICE_S - time.monotonic())
        ready, _, _ = _select([door, forwarder.read_fd, forwarder.connection.sock], timeout)
        if forwarder.read_fd in ready:
            forwarder.flush()
        if forwarder.connection.sock in ready:
            forwarder.drain_answers()
        if waiting_for is not None and not is_told and time.monotonic() - since >= WAITING_NOTICE_S:
            print(f"probe: waiting for {waiting_for}...", file=sys.stderr)
            is_told = True
        if door not in ready:
            continue
        chunk = _read_chunk(door)
        if not chunk:
            return {"exit": None}
        buffer += chunk
        while b"\n" in buffer:
            line, buffer = buffer.split(b"\n", 1)
            message = _parse(line)
            if message.get("ready"):
                return None
            if "exit" in message:
                return message
            if isinstance(message.get("waiting"), str):
                waiting_for = message["waiting"]


def _send_fds(door: socket.socket) -> socket.socket:
    """Pass fds 0-2 (a closed one as /dev/null) and the command's end of its launcher channel;
    this shim's end of the channel."""
    launcher, theirs = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM)
    stdio, opened = [], []
    for fd in (0, 1, 2):
        try:
            os.fstat(fd)
            stdio.append(fd)
        except OSError:
            null = os.open(os.devnull, os.O_RDWR)
            opened.append(null)
            stdio.append(null)
    try:
        socket.send_fds(door, [b"F"], [*stdio, theirs.fileno()])
    finally:
        theirs.close()
        for fd in opened:
            os.close(fd)
    return launcher


def _wait_for_end(door: socket.socket, launcher, forwarder) -> dict | None:
    """The command's end, as the service sends it through the door (None when it went away);
    meanwhile the programs it asks for are started and their ends reported."""
    buffer = b""
    while b"\n" not in buffer:
        watched = [door, forwarder.read_fd, forwarder.connection.sock] + ([launcher.channel] if launcher.is_open else [])
        ready, _, _ = _select(watched, 0.1 if launcher.program else None)
        if forwarder.read_fd in ready:
            forwarder.flush()
        if forwarder.connection.sock in ready:
            forwarder.drain_answers()
        if launcher.channel in ready:
            launcher.receive()
        launcher.report_exit()
        if door not in ready:
            continue
        chunk = _read_chunk(door)
        if not chunk:
            return None
        buffer += chunk
    end = _parse(buffer.split(b"\n", 1)[0])
    return end or None


def _select(watched: list, timeout: float | None) -> tuple[list, list, list]:
    """`select` over what is still open (a closed socket's fileno is -1; an int is an fd)."""
    try:
        return select.select([w for w in watched if _is_open(w)], [], [], timeout)
    except InterruptedError:
        return [], [], []


def _is_open(watched) -> bool:
    if isinstance(watched, int):
        return watched >= 0
    try:
        return watched.fileno() >= 0
    except (OSError, ValueError):
        return False


def _read_chunk(door: socket.socket) -> bytes:
    try:
        return door.recv(4096)
    except OSError:
        return b""


def _parse(line: bytes) -> dict:
    try:
        message = json.loads(line.decode("utf-8"))
    except ValueError:
        return {}
    return message if isinstance(message, dict) else {}


def _finish(end: dict | None) -> int:
    if end is None or end.get("exit") is None:
        why = (end or {}).get("message") or "the Probe service stopped while running this command"
        print(f"probe: {why}", file=sys.stderr)
        return ShimExit.SERVICE_LOST
    if end.get("reason") == NO_HOST:
        print(f"probe: {end.get('message') or 'the Probe service could not start this command'}\n{_get_hints()}",
              file=sys.stderr)
        return ShimExit.UNAVAILABLE
    if end.get("message"):
        print(f"probe: {end['message']}", file=sys.stderr)
    number = end.get("signal")
    if isinstance(number, int):
        names = {int(getattr(signal, name)) for name in REPEATED_DEATHS if hasattr(signal, name)}
        if number in names:
            sys.stdout.flush()
            signal.signal(number, signal.SIG_DFL)
            os.kill(os.getpid(), number)
    return int(end["exit"])


def _get_open_files_limit() -> int | None:
    try:
        import resource

        soft, _hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    except (ImportError, OSError, ValueError):
        return None
    return None if soft == resource.RLIM_INFINITY else int(soft)


def _get_cwd() -> str:
    try:
        return os.getcwd()
    except OSError:
        return os.environ.get("PWD") or os.environ.get("HOME") or "/"
