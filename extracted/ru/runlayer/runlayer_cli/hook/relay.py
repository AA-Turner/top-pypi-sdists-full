"""HTTP relay for hook enforcement and event forwarding.

Shares the same endpoints and credential resolution as ``runlayer hooks relay``
but runs in-process (no subprocess needed).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT
from runlayer_cli.config import load_config
from runlayer_cli.hook.transcript_stream import (
    clear_transcript_stream_active,
    is_transcript_stream_active,
    resolve_transcript_path,
    transcript_start_offset,
)
from runlayer_cli.tls import http_client

_TARGETS: dict[str, tuple[str, int]] = {
    "enforce": ("/api/v1/hooks/cursor", 30),
    "event": ("/api/v1/hooks/events", 5),
    # Tool lifecycle endpoints — see backend/app/api/routes/hooks/tool.py.
    # These accept the same {client, event_name, tool_name, payload} wrapper
    # as /events but normalize into LocalToolPre/PostRequest for the scan
    # pipeline. Routing PreToolUse/PostToolUse data to /events instead would
    # silently downgrade local-tool scanning to plain audit forwarding.
    "tool-pre": ("/api/v1/hooks/tool/pre", 30),
    "tool-post": ("/api/v1/hooks/tool/post", 30),
}

_DEBUG_DIR = Path(tempfile.gettempdir())

# Sentinel argv[1] used when the frozen aiwatch-enforce binary re-spawns itself
# as a detached relay worker. The frozen bootloader doesn't understand `python
# -m`, so we route through the same entrypoint and dispatch on argv shape.
RELAY_WORKER_SENTINEL = "__relay_worker__"
TRANSCRIPT_STREAM_WORKER_SENTINEL = "__transcript_stream_worker__"


class RelayError(Exception):
    """Raised when the relay POST fails. ``exit_code`` mirrors the bash semantics:
    1 = credentials missing
    2 = HTTP / network error
    """

    def __init__(self, exit_code: int, detail: str = "") -> None:
        self.exit_code = exit_code
        self.detail = detail
        super().__init__(detail)


def _load_credentials() -> tuple[str, str]:
    """Return (host, secret) from config or raise RelayError(1).

    Any non-RelayError raised by ``load_config`` (corrupted YAML that parses
    to a non-dict, unreadable file with an unexpected OS error, etc.) or by
    the credential store (keyring backend raising outside ``KeyringError``)
    is converted to ``RelayError(1)`` so the hook fails closed (deny) instead
    of crashing with a non-zero exit. ``__main__`` only catches ``RelayError``
    around ``enforce()``; an unhandled exception would skip the deny shape and
    let some AI clients interpret a crashed hook as fail-open.
    """
    try:
        config = load_config()
        host = config.default_host
        if not host:
            raise RelayError(1, "no default_host")
        secret = config.get_secret_for_host(host)
        if not secret:
            raise RelayError(1, "no secret for host")
    except RelayError:
        raise
    except Exception as e:
        raise RelayError(1, f"credential load failed: {e}") from e
    return host, secret


def _post(
    host: str,
    secret: str,
    endpoint: str,
    payload: str,
    *,
    target: str,
    timeout: int,
    debug: bool = False,
) -> str:
    url = f"{host}{endpoint}"
    resp = None
    try:
        with http_client() as client:
            resp = client.post(
                url,
                content=payload,
                headers={
                    "Content-Type": "application/json",
                    API_KEY_HEADER_NAME: secret,
                    "User-Agent": USER_AGENT,
                },
                timeout=timeout,
            )
        if debug:
            _write_debug(target, url, payload, resp)
        if not resp.is_success:
            raise RelayError(2, f"HTTP {resp.status_code}")
        return resp.text
    except RelayError:
        raise
    except Exception:
        if debug:
            _write_debug(target, url, payload, resp)
        raise RelayError(2, "network error")


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
    """Synchronous POST to the enforce endpoint. Returns response text.

    Raises RelayError(1) for credential issues, RelayError(2) for network.
    """
    host, secret = _load_credentials()
    endpoint, default_timeout = _TARGETS["enforce"]
    return _post(
        host,
        secret,
        endpoint,
        payload,
        target="enforce",
        timeout=default_timeout,
        debug=debug,
    )


def forward_event(
    client_name: str,
    event_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> None:
    """Fire-and-forget event POST, run in a detached subprocess."""
    wrapper = json.dumps(
        {
            "client": client_name,
            "event_name": event_name,
            "payload": payload,
        }
    )
    _detached_relay("event", wrapper, debug=debug)


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
    endpoint, default_timeout = _TARGETS[target]
    return _post(
        host,
        secret,
        endpoint,
        wrapper,
        target=target,
        timeout=default_timeout,
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
    """Fire-and-forget POST to /tool/pre or /tool/post."""
    wrapper = _tool_lifecycle_wrapper(
        target, client_name, event_name, tool_name, payload
    )
    _detached_relay(target, wrapper, debug=debug)


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
    if client_name == "claude_code" and is_transcript_stream_active(payload):
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
        _detached_relay("event", wrapper, timeout=10, debug=debug)
    else:
        forward_event(client_name, event_name, payload, debug=debug)


def start_transcript_stream(
    client_name: str,
    payload: dict,
    *,
    debug: bool = False,
) -> bool:
    """Start a detached transcript tailer for Claude Code prompt turns."""
    if client_name != "claude_code":
        return False
    if resolve_transcript_path(payload) is None:
        return False
    if is_transcript_stream_active(payload):
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


def _detached_relay(
    target: str,
    wrapper: str,
    *,
    timeout: int | None = None,
    debug: bool = False,
) -> None:
    """Spawn a detached subprocess that POSTs the event payload.

    The hook process exits before the POST completes.
    """
    if getattr(sys, "frozen", False):
        args = [sys.executable, RELAY_WORKER_SENTINEL, target]
    else:
        args = [sys.executable, "-m", "runlayer_cli.hook._relay_worker", target]
    if timeout is not None:
        args.extend(["--timeout", str(timeout)])
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
        pass
