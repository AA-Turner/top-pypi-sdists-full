"""Local resident arm owners: leaving a CLI never means releasing torque.

Only an attended client attach starts native control. The resident process owns
ProcessArm and its watchdog; CLI lifetime is deliberately not that watchdog's
lifetime. A private Unix socket and per-client CAN lock allow exclusive reuse.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import socket
import stat
import subprocess
import sys
import tempfile
import time
import traceback
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .yam_config import ArmConfig
from .yam_native import ArmState, ProcessArm, YamHardwareError

_PROTOCOL = 2  # Hold accepts finite encoder range excursions; commands stay bounded.
_RELEASE_PROTOCOL = 1  # Keep explicit torque release compatible with existing owners.


def _directory():
    path = Path(tempfile.gettempdir()) / f"dreamscale-yam-hold-{os.getuid()}"
    path.mkdir(mode=0o700, exist_ok=True)
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise YamHardwareError("YAM controller directory must be a private, owned directory.")
    return path


def _paths(config):
    key = hashlib.sha256(config.can_interface.encode()).hexdigest()[:16]
    root = _directory()
    return root / f"{key}.sock", root / f"{key}.client", root / f"{key}.server"


def _status_path(config):
    """Where the resident owner says whether it holds the arm and since when (read by the CLI
    without connecting: an owner from before this file re-commands its hold whenever any
    connection ends, so asking it would not be read-only)."""
    return _paths(config)[0].with_suffix(".status")


def _write_status(config, *, holding, unattended_since=None):
    """Best effort: a status that can't be written never stops the arm holding."""
    path = _status_path(config)
    temporary = path.with_suffix(".status.tmp")
    try:
        temporary.write_text(
            json.dumps(
                {
                    "pid": os.getpid(),
                    "holding": holding,
                    "unattended_since": unattended_since,
                }
            )
        )
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    except OSError:
        pass


def _lock(path):
    import fcntl

    fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BaseException:
        os.close(fd)
        raise YamHardwareError("This arm already has an active controller client.") from None
    return fd


def _send(stream, value):
    stream.write(json.dumps(value, allow_nan=False).encode() + b"\n")
    stream.flush()


def _read(stream):
    line = stream.readline(65537)
    if not line:
        raise EOFError
    if len(line) > 65536 or not line.endswith(b"\n"):
        raise YamHardwareError("Invalid local controller message.")
    return json.loads(line)


def _hold(arm):
    state = arm.snapshot().validate()
    target = state.position.copy()
    limits = arm.limits
    target = np.clip(target, limits[:, 0], limits[:, 1])
    applied = arm.command(target)
    if not np.array_equal(applied, target):
        raise YamHardwareError("Native controller changed hold target; hold unconfirmed.")
    arm.snapshot().validate()


@contextlib.contextmanager
def _client_stream(connection):
    """The connection's buffered stream, closed without failing the owner.

    A client that hangs up before reading its reply leaves that reply unsent in
    the buffer; closing re-flushes it and raises BrokenPipeError. Letting that
    escape ended serve() while the native controller kept the arm energized
    with nothing able to reach or release it.
    """
    stream = connection.makefile("rwb")
    try:
        yield stream
    finally:
        try:
            stream.close()  # also closes the underlying socket file when flush fails
        except OSError:
            pass


def serve(config, *, arm_factory=ProcessArm):
    """Run until explicit release. Client EOF parks in measured-pose hold."""
    import signal

    signal.signal(signal.SIGINT, signal.SIG_IGN)
    path, _, lock_path = _paths(config)
    owner = _lock(lock_path)
    listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    arm = None
    released = False
    try:
        path.unlink(missing_ok=True)  # server lock proves no other live owner
        listener.bind(str(path))
        os.chmod(path, 0o600)
        listener.listen(4)
        while not released:
            connection, _ = listener.accept()
            attached = False
            held = False
            with connection, _client_stream(connection) as stream:
                try:
                    while True:
                        request = _read(stream)
                        method = request.get("method")
                        protocols = (
                            {_PROTOCOL, _RELEASE_PROTOCOL} if method == "release" else {_PROTOCOL}
                        )
                        if request.get("protocol") not in protocols or request.get(
                            "config"
                        ) != asdict(config):
                            raise YamHardwareError(
                                "Resident arm configuration/protocol mismatch. Support the arms, "
                                "run dreamscale robots yam release, then start again."
                            )
                        if method == "release":
                            if arm is not None:
                                if getattr(arm, "closed", False):
                                    raise YamHardwareError(
                                        "Native controller stopped; torque release unconfirmed."
                                    )
                                arm.close()  # ONLY explicit release requests torque-off
                                arm = None
                            released = True
                            _status_path(config).unlink(missing_ok=True)  # before the reply
                            _send(stream, {"ok": True, "value": None})
                            break
                        if method == "attach":
                            if arm is None:
                                arm = arm_factory(config)
                            _hold(arm)
                            attached = True
                            _write_status(config, holding=True)  # driven: not unattended
                            value = arm.limits.tolist()
                        elif not attached:
                            raise YamHardwareError("Attach before using the arm controller.")
                        elif method == "snapshot":
                            state = arm.snapshot()
                            value = dict(
                                position=state.position.tolist(),
                                velocity=state.velocity.tolist(),
                                timestamp=state.timestamp,
                                healthy=state.healthy,
                            )
                        elif method == "command":
                            target = np.asarray(request["target"], dtype=float)
                            if target.shape != (7,) or not np.isfinite(target).all():
                                raise YamHardwareError("Expected seven finite local arm targets.")
                            if ((target < arm.limits[:, 0]) | (target > arm.limits[:, 1])).any():
                                raise YamHardwareError("Local arm target exceeds native bounds.")
                            value = arm.command(target).tolist()
                        elif method == "detach":
                            _hold(arm)
                            held = True
                            # Before the reply: the client may ask straight after.
                            _write_status(config, holding=True, unattended_since=time.time())
                            _send(stream, {"ok": True, "value": None})
                            break
                        else:
                            raise YamHardwareError("Unknown local arm controller request.")
                        _send(stream, {"ok": True, "value": value})
                except EOFError:
                    pass
                except Exception as exc:
                    try:
                        _send(stream, {"ok": False, "error": str(exc)})
                    except (OSError, ValueError):
                        pass
                finally:
                    if arm is not None and not held:
                        confirmed = False
                        try:
                            _hold(arm)
                            confirmed = True
                        except Exception as exc:
                            print(f"Arm hold UNCONFIRMED: {exc}", file=sys.stderr, flush=True)
                        if attached:  # the client went without detaching
                            _write_status(config, holding=confirmed, unattended_since=time.time())
                    # Never call arm.close() simply because a client ended.
    finally:
        listener.close()
        path.unlink(missing_ok=True)
        _status_path(config).unlink(missing_ok=True)
        os.close(owner)


def _start(config):
    from .yam_output import open_diagnostic_log

    _, log = open_diagnostic_log(f"hold-{config.can_interface}")
    try:
        return subprocess.Popen(
            [sys.executable, "-m", __name__, json.dumps(asdict(config))],
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=log,
            start_new_session=True,
            close_fds=True,
        )
    finally:
        log.close()


class PersistentArm:
    """CLI lease on a resident controller; close holds and relinquishes the lease."""

    holds_after_close = True

    def __init__(self, config, *, launcher=_start, startup_timeout_s=50.0):
        self.config = config
        self.closed = False
        self.hold_confirmed = False
        self.torque_released = False
        self.connection = self.stream = None
        path, client_lock, _ = _paths(config)
        self.owner = _lock(client_lock)
        launched = False
        deadline = time.monotonic() + startup_timeout_s
        try:
            while True:
                connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                try:
                    connection.connect(str(path))
                    break
                except (FileNotFoundError, ConnectionRefusedError):
                    connection.close()
                    if not launched:
                        launcher(config)
                        launched = True
                    if time.monotonic() >= deadline:
                        raise YamHardwareError(
                            "Resident arm controller did not start; hold unconfirmed."
                        ) from None
                    time.sleep(0.05)
            self.connection = connection
            self.stream = connection.makefile("rwb")
            self.limits = np.asarray(self._request("attach", timeout=startup_timeout_s))
            from .yam_native import _validate_limits

            _validate_limits(self.limits)
        except BaseException:
            self._disconnect()
            raise

    def _disconnect(self):
        self.closed = True
        try:
            if self.connection is not None:
                try:
                    self.connection.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
            if self.stream is not None:
                self.stream.close()
        finally:
            try:
                if self.connection is not None:
                    self.connection.close()
            finally:
                if self.owner is not None:
                    os.close(self.owner)
                    self.owner = None

    def _request(self, method, *, timeout=2.0, **values):
        if self.closed:
            raise YamHardwareError("Arm client is closed; resident hold may still be active.")
        self.connection.settimeout(timeout)
        try:
            _send(
                self.stream,
                dict(protocol=_PROTOCOL, config=asdict(self.config), method=method, **values),
            )
            reply = _read(self.stream)
            if not reply["ok"]:
                raise YamHardwareError(reply["error"])
            return reply["value"]
        except (OSError, EOFError) as exc:
            self._disconnect()
            raise YamHardwareError("Local controller connection failed; hold unconfirmed.") from exc
        except BaseException:
            # EOF makes the resident owner attempt a measured hold, not torque-off.
            self._disconnect()
            raise

    def snapshot(self):
        state = self._request("snapshot")
        return ArmState(
            np.asarray(state["position"]),
            np.asarray(state["velocity"]),
            state["timestamp"],
            state["healthy"],
        )

    def command(self, target):
        return np.asarray(self._request("command", target=np.asarray(target).tolist()))

    def close(self):
        if self.closed:
            if not self.hold_confirmed and not self.torque_released:
                raise YamHardwareError("Local controller disconnected; hold unconfirmed.")
            return
        try:
            self._request("detach")
            self.hold_confirmed = True
        finally:
            self._disconnect()

    def release(self):
        """Release torque while retaining this client's exclusive arm lease."""
        try:
            self._request("release", timeout=5.0)
            self.torque_released = True
            self.holds_after_close = False
        finally:
            self._disconnect()


def _release(config):
    path, _, _ = _paths(config)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(5)
        try:
            connection.connect(str(path))
        except (FileNotFoundError, ConnectionRefusedError):
            return False
        with connection.makefile("rwb") as stream:
            _send(stream, dict(protocol=_RELEASE_PROTOCOL, config=asdict(config), method="release"))
            response = _read(stream)
            if not response["ok"]:
                raise YamHardwareError(response["error"])
            return True


def hold_status(config, *, now=time.time, alive=None):
    """Whether this arm's resident owner holds it unattended, and for how long:
    {holding, unattended_s}, or None (no owner, a driven arm, or an owner from before the
    status file). Reads a file; never connects, so it never touches the arm."""
    try:
        state = json.loads(_status_path(config).read_text())
        pid = int(state["pid"])
        since = state.get("unattended_since")
        if not (alive or _alive)(pid) or since is None:
            return None
        return {
            "holding": state.get("holding") is True,
            "unattended_s": max(0.0, now() - float(since)),
        }
    except (OSError, ValueError, TypeError, KeyError):
        return None


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


# While compute starts, the operator hears about arms holding with nobody driving them: first
# after this long, then this often (a long hold under load heats the motors).
HOLD_NOTICE_AFTER_S = 20.0
HOLD_NOTICE_EVERY_S = 120.0


def _held_for(seconds: float) -> str:
    return f"{int(seconds)} s" if seconds < 60 else f"{int(seconds // 60)} min"


async def watch_resident_holds(
    configs,
    print_fn,
    *,
    status=hold_status,
    sleep=None,
    first_after_s=HOLD_NOTICE_AFTER_S,
    every_s=HOLD_NOTICE_EVERY_S,
):
    """Until cancelled (compute is ready): tell the operator when arms an earlier run left
    holding are still held, for how long, and how to support and release them. Never moves or
    releases anything itself (releasing drops the arms), and never connects to the arms."""
    import asyncio

    from dreamscale.embodiments import YAM

    sleep = sleep or asyncio.sleep
    await sleep(first_after_s)
    told = False
    while True:
        held = {}
        for side, config in configs.items():
            state = status(config)
            if state and state.get("holding"):
                held[side] = float(state.get("unattended_s") or 0.0)
        if held:
            longest = _held_for(max(held.values()))
            sides = " and ".join(side.title() for side in held)
            several = len(held) > 1
            print_fn(
                f"{sides} {'arms are' if several else 'arm is'} holding the pose the last run "
                f"left ({longest} so far) while compute starts. If "
                f"{'they carry' if several else 'it carries'} a load, support "
                f"{'them' if several else 'it'} and run `{YAM.release_command}` in another "
                "terminal: a long hold under load heats the motors."
                if not told
                else f"Still starting compute; {sides.lower()} "
                f"{'arms have' if several else 'arm has'} held for {longest}."
            )
            told = True
        await sleep(every_s)


def release_controllers(configs):
    """Explicit torque release; acquire ALL leases before changing either arm.

    An active run prevents any release. Missing resident controllers are reported
    separately: absence cannot confirm the physical motor state.
    """
    owners = []
    results = {}
    try:
        for config in configs.values():
            owners.append(_lock(_paths(config)[1]))
        for side, config in configs.items():
            try:
                results[side] = "released" if _release(config) else "no resident controller"
            except Exception as exc:
                results[side] = f"release UNCONFIRMED: {exc}"
        return results
    finally:
        for owner in owners:
            os.close(owner)


def release_yam(config_path, *, input_fn=input, print_fn=print, discover_can=None):
    from .yam_can import discover_can_interfaces, resolve_arms
    from .yam_config import load_config

    config = resolve_arms(
        load_config(config_path).validate(complete=True),
        discover_can=discover_can or discover_can_interfaces,
    )
    print_fn("Support the arms. This releases motor torque.")
    try:
        while input_fn("Enter to release · Ctrl+C to cancel: ").strip():
            pass
    except (EOFError, KeyboardInterrupt):
        return
    results = release_controllers(config.arms)
    for side, result in results.items():
        print_fn(f"{side.title()}: {result}.")
    if any("UNCONFIRMED" in result for result in results.values()):
        raise YamHardwareError("Torque release unconfirmed; check the hardware E-stop.")


if __name__ == "__main__":
    try:
        serve(ArmConfig(**json.loads(sys.argv[1])))
    except BaseException:
        # An owner that can no longer serve must not linger: interpreter exit
        # would wait on the native controller (a non-daemon child), leaving the
        # arm driven but unreachable for release. Exit now; the controller sees
        # its parent die and stops, as on any other owner death.
        traceback.print_exc()
        sys.stderr.flush()
        os._exit(1)
