"""HTTP relay for hook enforcement and event forwarding (runs in-process)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from runlayer_sdk.hook_transport import (
    API_KEY_HEADER_NAME,
    HOOK_RELAY_TARGETS,
    HookAPIClient,
)

from runlayer_cli.api import USER_AGENT
from runlayer_cli.config import load_config, normalize_url, save_config
from runlayer_cli.enrollment import (
    EnrollmentError,
    exchange_enrollment_key,
    write_enrollment_marker,
)
from runlayer_cli.hook.transcript_stream import (
    clear_transcript_stream_active,
    clear_transcript_stream_completed,
    is_transcript_stream_active,
    is_transcript_stream_recently_completed,
    resolve_transcript_path,
    transcript_start_offset,
)
from runlayer_cli.mdm_config import ManagedConfig, read_managed_config
from runlayer_cli.paths import get_runlayer_dir
from runlayer_cli.tls import http_client

_TRANSCRIPT_STREAM_CLIENTS = frozenset({"claude_code", "codex"})

_DEBUG_DIR = Path(tempfile.gettempdir())

TRANSCRIPT_STREAM_WORKER_SENTINEL = "__transcript_stream_worker__"

_ENROLLMENT_COOLDOWN_SECONDS = 60.0
_ENROLLMENT_ATTEMPT_FILENAME = ".enrollment-attempt"

# In-memory re-entry guard for `_try_lazy_enrollment`. The cooldown touch file
# is the cross-process guard, but it shares a failure domain with `save_config`
# (read-only fs, missing dir): if both writes fail, the post-success
# `forward_event` -> `_forward_post` -> `_load_credentials` chain would loop
# straight back here. This flag breaks the chain regardless of disk state.
_lazy_enrollment_in_progress = False


class RelayError(Exception):
    """Raised when the relay POST fails. ``exit_code``: 1 = no creds, 2 = HTTP/network."""

    def __init__(self, exit_code: int, detail: str = "", body: str = "") -> None:
        self.exit_code = exit_code
        self.detail = detail
        self.body = body
        super().__init__(detail)


def _load_credentials() -> tuple[str, str]:
    """Return (host, secret) or raise ``RelayError(1)`` (fail-closed)."""
    try:
        config = load_config()
        managed = read_managed_config()
        raw_host = config.default_host or managed.get("host")
        if not raw_host:
            raise RelayError(1, "no default_host")
        # MDM ``Host`` skips ``set_host_credentials`` normalization; strip
        # trailing slash so ``_post`` doesn't build double-slash URLs.
        host = normalize_url(raw_host)
        secret = config.get_secret_for_host(host)
        if secret:
            return host, secret
        secret = _try_lazy_enrollment(host, managed)
        if not secret:
            raise RelayError(1, "no secret for host")
    except RelayError:
        raise
    except Exception as e:
        raise RelayError(1, f"credential load failed: {e}") from e
    return host, secret


def _try_lazy_enrollment(host: str, managed: ManagedConfig) -> str | None:
    """Self-healing fallback (see cli/AGENTS.md); returns api_key or ``None``."""
    global _lazy_enrollment_in_progress
    if _lazy_enrollment_in_progress:
        return None
    _lazy_enrollment_in_progress = True
    try:
        return _try_lazy_enrollment_inner(host, managed)
    finally:
        _lazy_enrollment_in_progress = False


def _try_lazy_enrollment_inner(host: str, managed: ManagedConfig) -> str | None:
    enrollment_key = managed.get("enrollment_key")
    if not enrollment_key:
        return None
    if _enrollment_attempt_recently():
        return None
    _touch_enrollment_attempt()

    try:
        result = exchange_enrollment_key(
            host=host,
            enrollment_key=enrollment_key,
            username=managed.get("username"),
            device_name=managed.get("device_name"),
        )
    except EnrollmentError:
        return None

    config = load_config()
    config.set_host_credentials(host, result.api_key)
    try:
        save_config(config)
    except OSError:
        pass
    write_enrollment_marker(host)

    try:
        forward_event(
            client_name="aiwatch_hook",
            event_name="aiwatch.lazy_enrollment_fallback_hit",
            payload={
                "username": result.username,
                "device_name": result.device_name,
                "host": host,
            },
        )
    except Exception:
        pass

    return result.api_key


def _enrollment_attempt_path() -> Path:
    return get_runlayer_dir() / _ENROLLMENT_ATTEMPT_FILENAME


def _enrollment_attempt_recently() -> bool:
    path = _enrollment_attempt_path()
    try:
        mtime = path.stat().st_mtime
    except (FileNotFoundError, OSError):
        return False
    return (time.time() - mtime) < _ENROLLMENT_COOLDOWN_SECONDS


def _touch_enrollment_attempt() -> None:
    path = _enrollment_attempt_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        os.utime(path, None)
    except OSError:
        pass


def _post(
    host: str,
    secret: str,
    payload: str,
    *,
    target: str,
    timeout: int | None = None,
    debug: bool = False,
) -> str:
    spec = HOOK_RELAY_TARGETS[target]
    url = f"{host}{spec.endpoint}"
    client = HookAPIClient(
        host,
        headers={
            API_KEY_HEADER_NAME: secret,
            "User-Agent": USER_AGENT,
        },
        http_client_factory=http_client,
    )
    resp = None
    try:
        resp = client.post_target(target, payload, timeout=timeout)
        _maybe_debug(debug, target, url, payload, resp)
        if not resp.is_success:
            raise RelayError(2, f"HTTP {resp.status_code}", body=resp.text)
        return resp.text
    except RelayError:
        raise
    except Exception:
        _maybe_debug(debug, target, url, payload, resp)
        raise RelayError(2, "network error")


def _maybe_debug(debug: bool, target: str, url: str, payload: str, resp: Any) -> None:
    if not debug:
        return
    try:
        _write_debug(target, url, payload, resp)
    except Exception:
        pass


def _write_debug(target: str, url: str, request_body: str, resp: Any) -> None:
    try:
        ts = int(time.time())
        data = {
            "timestamp": ts,
            "url": url,
            "request_body_size": len(request_body) if request_body else 0,
            "response_status": resp.status_code if resp else None,
            "response_body_size": len(resp.text) if resp else None,
        }
        path = _DEBUG_DIR / f"runlayer-relay-{target}-{ts}.json"
        path.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


def enforce(payload: str, *, debug: bool = False) -> str:
    """Synchronous POST to enforce; raises ``RelayError(1)`` (creds) or ``RelayError(2)`` (network)."""
    host, secret = _load_credentials()
    return _post(
        host,
        secret,
        payload,
        target="enforce",
        debug=debug,
    )


def forward_event(
    client_name: str,
    event_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> None:
    """Best-effort synchronous in-process event POST; errors swallowed."""
    wrapper = json.dumps(
        {
            "client": client_name,
            "event_name": event_name,
            "payload": payload,
        }
    )
    _forward_post("event", wrapper, debug=debug)


def check_tool_lifecycle(
    target: str,
    client_name: str,
    event_name: str,
    tool_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> str:
    """Synchronous POST to /tool/pre or /tool/post. Returns response text."""
    wrapper = _tool_lifecycle_wrapper(
        target, client_name, event_name, tool_name, payload
    )
    host, secret = _load_credentials()
    return _post(
        host,
        secret,
        wrapper,
        target=target,
        debug=debug,
    )


def forward_tool_lifecycle(
    target: str,
    client_name: str,
    event_name: str,
    tool_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> None:
    """Best-effort synchronous in-process POST to /tool/pre or /tool/post; errors swallowed."""
    wrapper = _tool_lifecycle_wrapper(
        target, client_name, event_name, tool_name, payload
    )
    _forward_post(target, wrapper, debug=debug)


def _tool_lifecycle_wrapper(
    target: str,
    client_name: str,
    event_name: str,
    tool_name: str,
    payload: dict,
) -> str:
    if target not in ("tool-pre", "tool-post"):
        raise ValueError(f"Invalid tool lifecycle target: {target}")
    return json.dumps(
        {
            "client": client_name,
            "event_name": event_name,
            "tool_name": tool_name,
            "payload": payload,
        }
    )


def _wait_for_transcript_file(transcript_path: str) -> Path:
    p = Path(transcript_path)
    if p.is_file():
        return p
    for _ in range(5):
        time.sleep(0.1)
        if p.is_file():
            break
    return p


def forward_stop_event(
    client_name: str,
    event_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> None:
    """Forward a stop event, attaching transcript content if available."""
    if client_name in _TRANSCRIPT_STREAM_CLIENTS and (
        is_transcript_stream_active(payload)
        or is_transcript_stream_recently_completed(payload)
    ):
        forward_event(client_name, event_name, payload, debug=debug)
        return

    transcript_path = payload.get("transcript_path") or os.environ.get(
        "CURSOR_TRANSCRIPT_PATH", ""
    )
    if transcript_path.startswith("~"):
        transcript_path = str(Path.home()) + transcript_path[1:]

    transcript = ""
    if transcript_path:
        p = _wait_for_transcript_file(transcript_path)
        if p.is_file():
            try:
                data = p.read_bytes()
                transcript = data[-524288:].decode("utf-8", errors="replace")
            except OSError:
                pass

    if transcript:
        wrapper = json.dumps(
            {
                "client": client_name,
                "event_name": event_name,
                "payload": payload,
                "transcript": transcript,
            }
        )
        _forward_post("event", wrapper, timeout=10, debug=debug)
    else:
        forward_event(client_name, event_name, payload, debug=debug)


def start_transcript_stream(
    client_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> bool:
    """Start a detached transcript tailer for prompt turns with transcript JSONL."""
    if client_name not in _TRANSCRIPT_STREAM_CLIENTS:
        return False
    if resolve_transcript_path(payload) is None:
        return False
    completed_recently = is_transcript_stream_recently_completed(payload)
    if completed_recently:
        clear_transcript_stream_completed(payload)
    elif is_transcript_stream_active(payload):
        return True

    start_offset = transcript_start_offset(payload)
    wrapper = json.dumps(
        {
            "client": client_name,
            "payload": payload,
            "start_offset": start_offset,
        }
    )
    if getattr(sys, "frozen", False):
        args = [sys.executable, TRANSCRIPT_STREAM_WORKER_SENTINEL]
    else:
        args = [
            sys.executable,
            "-m",
            "runlayer_cli.hook._transcript_stream_worker",
        ]
    if debug:
        args.append("--debug")

    kwargs: dict[str, Any] = {
        "stdin": subprocess.PIPE,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "close_fds": True,
    }
    if sys.platform != "win32":
        kwargs["start_new_session"] = True
    else:
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008
        kwargs["creationflags"] = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP

    try:
        proc = subprocess.Popen(args, **kwargs)
        stdin = proc.stdin
        if stdin is not None:
            stdin.write(wrapper.encode("utf-8"))  # ty: ignore[no-matching-overload]
            stdin.close()
    except OSError:
        clear_transcript_stream_active(payload)
        return False
    return True


def _forward_post(
    target: str,
    wrapper: str,
    *,
    timeout: int | None = None,
    debug: bool = False,
) -> None:
    """Best-effort fire-and-forget POST; errors swallowed."""
    try:
        host, secret = _load_credentials()
        _post(
            host,
            secret,
            wrapper,
            target=target,
            timeout=timeout,
            debug=debug,
        )
    except Exception:
        pass
