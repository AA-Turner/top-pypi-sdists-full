from __future__ import annotations

import atexit
import json
import os
import secrets
import select
import socket
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, BinaryIO, Callable, cast

from .config import load_config
from .core import Enabled, enable

PROTOCOL_VERSION = 1
MAX_MESSAGE_BYTES = 64 * 1024
PERMISSION_HELP_URL = (
    "https://docs.python.org/3.14/howto/remote_debugging.html#permission-requirements"
)


class AttachError(RuntimeError):
    pass


@dataclass
class AttachResult:
    trace_id: str
    db_path: Path


@dataclass
class _AttachedSession:
    connection: socket.socket
    enabled: Enabled
    token: str
    stopped: bool = False
    stop_lock: threading.Lock = field(default_factory=threading.Lock)


_session_lock = threading.Lock()
_active_session: _AttachedSession | None = None


def _send_message(connection: socket.socket, message: dict[str, Any]) -> None:
    payload = json.dumps(message, sort_keys=True).encode() + b"\n"
    connection.sendall(payload)


def _open_reader(connection: socket.socket) -> BinaryIO:
    # select() watches the socket, so the reader must not prefetch a later
    # protocol message into a separate userspace buffer.
    return cast(BinaryIO, connection.makefile("rb", buffering=0))


def _read_message(reader: BinaryIO) -> dict[str, Any]:
    payload = reader.readline(MAX_MESSAGE_BYTES + 1)
    if not payload:
        raise AttachError("The target process closed the attach connection.")
    if len(payload) > MAX_MESSAGE_BYTES:
        raise AttachError("The target process sent an oversized response.")
    try:
        message = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise AttachError("The target process sent an invalid response.") from exc
    if not isinstance(message, dict):
        raise AttachError("The target process sent an invalid response.")
    return message


def _read_message_with_timeout(
    connection: socket.socket,
    reader: BinaryIO,
    *,
    timeout: float,
    timeout_message: str,
) -> dict[str, Any]:
    previous_timeout = connection.gettimeout()
    connection.settimeout(timeout)
    try:
        return _read_message(reader)
    except (socket.timeout, TimeoutError) as exc:
        raise AttachError(timeout_message) from exc
    finally:
        connection.settimeout(previous_timeout)


def _stop_session(session: _AttachedSession, *, reply: bool) -> None:
    global _active_session

    with session.stop_lock:
        if session.stopped:
            return
        session.stopped = True

        with _session_lock:
            if _active_session is session:
                _active_session = None

        try:
            session.enabled._deactivate(None, None, None)
        except Exception as exc:
            message = {
                "event": "error",
                "protocol": PROTOCOL_VERSION,
                "token": session.token,
                "error": f"{type(exc).__name__}: {exc}",
            }
        else:
            assert session.enabled.trace_id is not None
            message = {
                "event": "stopped",
                "protocol": PROTOCOL_VERSION,
                "token": session.token,
                "trace_id": session.enabled.trace_id,
                "db_path": str(session.enabled._active_db_path),
            }

        if reply:
            try:
                _send_message(session.connection, message)
            except OSError:
                # The controller may already be gone; saving has completed.
                pass
        try:
            session.connection.close()
        except OSError:
            # Best-effort cleanup during target shutdown.
            pass


def _control_session(session: _AttachedSession) -> None:
    try:
        reader = _open_reader(session.connection)
        with reader:
            message = _read_message(reader)
    except (AttachError, OSError):
        _stop_session(session, reply=False)
        return

    if message.get("protocol") != PROTOCOL_VERSION:
        _stop_session(session, reply=False)
        return
    if not _tokens_match(message.get("token"), session.token):
        _stop_session(session, reply=False)
        return
    if message.get("command") != "stop":
        try:
            _send_message(
                session.connection,
                {
                    "event": "error",
                    "protocol": PROTOCOL_VERSION,
                    "token": session.token,
                    "error": "Unknown attach command.",
                },
            )
        except OSError:
            # The error response is best-effort; session shutdown still follows.
            pass
        _stop_session(session, reply=False)
        return

    _stop_session(session, reply=True)


def _load_attach_config(payload_path: str | None) -> dict[str, Any]:
    config = dict(load_config())
    if payload_path is None:
        return config

    filters = dict(config.get("filters", {}))
    ignore_frames = list(filters.get("ignore_frames", []))
    ignore_frames.extend((os.path.normpath(__file__), payload_path))
    filters["ignore_frames"] = ignore_frames
    config["filters"] = filters
    return config


def start_attached_session(
    connection: socket.socket,
    token: str,
    name: str | None,
    payload_path: str | None = None,
) -> dict[str, Any]:
    global _active_session

    config = _load_attach_config(payload_path)
    if not config.get("use_monitoring", True):
        raise RuntimeError(
            "kolo attach requires the sys.monitoring backend; remove "
            "`use_monitoring = false` from the target's Kolo config."
        )

    with _session_lock:
        if _active_session is not None:
            raise RuntimeError("Kolo is already attached to this process.")

        enabled = enable(
            config,
            name=name,
            source="kolo attach",
            _save_in_thread=False,
        )
        assert isinstance(enabled, Enabled)
        if not enabled._activate():
            raise RuntimeError(
                "Kolo could not attach because another profiler is already active."
            )
        if enabled.trace_id is None:
            enabled._deactivate(None, None, None)
            raise RuntimeError("Kolo started tracing without creating a trace ID.")

        session = _AttachedSession(connection, enabled, token)
        _active_session = session

    try:
        control_thread = threading.Thread(
            target=_control_session,
            args=(session,),
            name="kolo-attach-control",
            daemon=True,
        )
        control_thread.start()
    except BaseException:
        _stop_session(session, reply=False)
        raise

    return {
        "event": "started",
        "protocol": PROTOCOL_VERSION,
        "token": token,
        "trace_id": enabled.trace_id,
        "db_path": str(enabled._active_db_path),
    }


@atexit.register
def _cleanup_attached_session() -> None:
    with _session_lock:
        session = _active_session
    if session is not None:
        _stop_session(session, reply=True)


def _payload_source(host: str, port: int, token: str, name: str | None) -> str:
    return f"""\
def _kolo_attach():
    import json
    import os
    import socket
    import sys

    payload_path = sys._getframe().f_code.co_filename
    try:
        os.unlink(payload_path)
    except OSError:
        pass

    try:
        connection = socket.create_connection(({host!r}, {port!r}))
    except OSError:
        return

    try:
        from kolo._attach import _send_message, start_attached_session

        message = start_attached_session(
            connection, {token!r}, {name!r}, payload_path
        )
        _send_message(connection, message)
    except BaseException as error:
        payload = json.dumps({{
            "event": "error",
            "protocol": {PROTOCOL_VERSION},
            "token": {token!r},
            "error": f"{{type(error).__name__}}: {{error}}",
        }}, sort_keys=True).encode() + b"\\n"
        try:
            connection.sendall(payload)
        finally:
            connection.close()


_kolo_attach()
del _kolo_attach
"""


def _write_payload(source: str, *, owner: tuple[int, int] | None) -> Path:
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", prefix="kolo-attach-", suffix=".py", delete=False
    ) as payload:
        payload.write(source)
        payload_path = Path(payload.name)
    try:
        if owner is not None:
            os.chown(payload_path, *owner)
            payload_path.chmod(0o600)
    except BaseException:
        try:
            payload_path.unlink()
        except OSError:
            # Best-effort cleanup must not replace the original ownership error.
            pass
        raise
    return payload_path


def _controller_is_elevated() -> bool:
    get_effective_uid = getattr(os, "geteuid", None)
    return get_effective_uid is not None and get_effective_uid() == 0


def _target_process_owner(pid: int) -> tuple[int, int] | None:
    if not _controller_is_elevated():
        return None

    try:
        status = (Path("/proc") / str(pid) / "status").read_text(encoding="ascii")
    except FileNotFoundError:
        try:
            completed = subprocess.run(
                ("/bin/ps", "-o", "uid=", "-o", "gid=", "-p", str(pid)),
                check=True,
                capture_output=True,
                encoding="ascii",
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            raise ProcessLookupError(pid) from exc

        fields = completed.stdout.split()
        if len(fields) != 2:
            raise ProcessLookupError(pid)
        try:
            return int(fields[0]), int(fields[1])
        except ValueError as exc:
            raise ProcessLookupError(pid) from exc
    else:
        try:
            uid_fields = next(
                line.split() for line in status.splitlines() if line.startswith("Uid:")
            )
            gid_fields = next(
                line.split() for line in status.splitlines() if line.startswith("Gid:")
            )
            return int(uid_fields[2]), int(gid_fields[2])
        except (IndexError, StopIteration, ValueError) as exc:
            raise ProcessLookupError(pid) from exc


def _tokens_match(candidate: Any, token: str) -> bool:
    if not isinstance(candidate, str):
        return False
    return secrets.compare_digest(candidate.encode(), token.encode())


def _validate_message(message: dict[str, Any], token: str) -> None:
    if message.get("protocol") != PROTOCOL_VERSION:
        raise AttachError("The target process uses an incompatible attach protocol.")
    if not _tokens_match(message.get("token"), token):
        raise AttachError("The target process returned an invalid attach token.")
    if message.get("event") == "error":
        raise AttachError(str(message.get("error", "Unknown target error.")))


def _wait_for_duration_or_target(
    connection: socket.socket,
    reader: BinaryIO,
    duration: float | None,
) -> dict[str, Any] | None:
    deadline = None if duration is None else time.monotonic() + duration
    while True:
        if deadline is None:
            timeout = 0.5
        else:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None
            timeout = min(remaining, 0.5)

        readable, _, _ = select.select([connection], [], [], timeout)
        if readable:
            return _read_message_with_timeout(
                connection,
                reader,
                timeout=timeout,
                timeout_message=(
                    "Timed out waiting for the target process to send a complete "
                    "attach message."
                ),
            )


def _wait_for_message(
    connection: socket.socket,
    reader: BinaryIO,
    *,
    timeout: float,
    timeout_message: str,
) -> dict[str, Any]:
    readable, _, _ = select.select([connection], [], [], timeout)
    if not readable:
        raise AttachError(timeout_message)
    return _read_message_with_timeout(
        connection,
        reader,
        timeout=timeout,
        timeout_message=timeout_message,
    )


def attach_process(
    pid: int,
    *,
    duration: float | None,
    name: str | None,
    timeout: float,
    remote_exec: Callable[[int, str], None],
    output: Callable[[str], None],
) -> AttachResult:
    token = secrets.token_urlsafe(32)
    server = socket.create_server(("127.0.0.1", 0), backlog=1)
    payload_path: Path | None = None
    payload_dispatched = False

    try:
        host, port = server.getsockname()
        payload_path = _write_payload(
            _payload_source(host, port, token, name),
            owner=_target_process_owner(pid),
        )
        remote_exec(pid, os.fspath(payload_path))
        payload_dispatched = True

        server.settimeout(timeout)
        try:
            connection, _ = server.accept()
        except socket.timeout as exc:
            raise AttachError(
                f"Timed out after {timeout:g} seconds waiting for process {pid} "
                "to run the attach script. The process may be blocked in native "
                "code or have remote debugging disabled."
            ) from exc
        with connection:
            reader = _open_reader(connection)
            with reader:
                started = _wait_for_message(
                    connection,
                    reader,
                    timeout=timeout,
                    timeout_message=(
                        f"Timed out after {timeout:g} seconds waiting for process "
                        f"{pid} to start tracing."
                    ),
                )
                _validate_message(started, token)
                if started.get("event") != "started":
                    raise AttachError("The target process did not start tracing.")

                trace_id = str(started["trace_id"])
                output(f"Attached to process {pid}. Trace ID: {trace_id}")
                if duration is None:
                    output("Tracing until interrupted. Press Ctrl-C to stop and save.")
                else:
                    output(f"Tracing for {duration:g} seconds.")

                try:
                    stopped = _wait_for_duration_or_target(connection, reader, duration)
                except KeyboardInterrupt:
                    stopped = None

                if stopped is None:
                    _send_message(
                        connection,
                        {
                            "command": "stop",
                            "protocol": PROTOCOL_VERSION,
                            "token": token,
                        },
                    )
                    stopped = _wait_for_message(
                        connection,
                        reader,
                        timeout=timeout,
                        timeout_message=(
                            f"Timed out after {timeout:g} seconds waiting for process "
                            f"{pid} to save the trace."
                        ),
                    )

                _validate_message(stopped, token)
                if stopped.get("event") != "stopped":
                    raise AttachError("The target process did not save the trace.")

                result = AttachResult(
                    trace_id=str(stopped["trace_id"]),
                    db_path=Path(stopped["db_path"]),
                )
                output(f"Trace saved: {result.trace_id}")
                output(f"Kolo store: {result.db_path.parent.parent}")
                output(
                    f"View it with `kolo cat {result.trace_id}` from "
                    f"{result.db_path.parent.parent.parent}, or set KOLO_PATH to "
                    "that directory."
                )
                return result
    finally:
        server.close()
        if payload_path is not None and not payload_dispatched:
            try:
                payload_path.unlink()
            except OSError:
                # The target may still hold the script open on Windows. Temporary
                # file cleanup must not mask the attach result or original error.
                pass
