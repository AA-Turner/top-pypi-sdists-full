"""Standard-library IPC contract shared by AI Watch hook clients and daemon."""

from __future__ import annotations

import ctypes
import json
import os
import struct
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal, TypedDict, cast

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired

FRAME_PREFIX_SIZE = 4
MAX_FRAME_BYTES = 16 * 1024 * 1024
CONNECT_TIMEOUT_SECONDS = 0.2
RESPONSE_TIMEOUT_SECONDS = 60.0
HEALTH_TIMEOUT_SECONDS = 1.0
DAEMON_ENDPOINT_ENV = "RUNLAYER_AIWATCH_DAEMON_SOCKET"
# Carries the Go shim's start stamp to its exec-fallback child, which has no
# IPC frame to read `client_start_ms` from. Mirrored by
# clientStartEnvironmentName in aiwatch-hook-shim/internal/shim/request.go.
CLIENT_START_ENV = "RUNLAYER_HOOK_CLIENT_START_MS"
# Both handshake phases currently use ASCII ACK, but they are separate protocol
# tokens: readers must match the constant for their phase, not the byte value.
WINDOWS_RESPONSE_ACK = b"\x06"
REQUEST_ACCEPTED_ACK = b"\x06"

HOOK_ENV_ALLOWLIST = frozenset(
    {
        "APPDATA",
        "CLINE_DIR",
        "COPILOT_ADDITIONAL_MCP_CONFIG",
        "COPILOT_HOME",
        "CURSOR_TRANSCRIPT_PATH",
        "CURSOR_VERSION",
        "DEVIN_PROJECT_DIR",
        "GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG",
        "GROK_HOME",
        "GROK_HOOK_EVENT",
        "HOOK_EVENT_NAME",
        "PROGRAMFILES",
        "QWEN_HOME",
        "RUNLAYER_GITHUB_COPILOT_CLI_ADDITIONAL_MCP_CONFIG",
        "RUNLAYER_FLOW_TRACE",
        "RUNLAYER_HOOK_CLIENT",
        "RUNLAYER_HOOK_DEBUG",
        # Gzip kill switch must reach daemon-served hooks: the daemon's own
        # environment lacks the invoking client's override, and hook_io.getenv
        # reads the forwarded request env first.
        "RUNLAYER_HOOK_GZIP",
        # Retry kill switch: read at send time in relay._post; must ride the
        # request env or daemon-served hooks silently keep the default retries.
        "RUNLAYER_HOOK_RETRIES",
        "USERPROFILE",
    }
)


class FrameError(ValueError):
    """Raised when an IPC frame is malformed or exceeds the protocol limit."""


class UnsupportedDaemonPlatform(OSError):
    """Raised when this platform has no daemon endpoint.

    Hooks ship on macOS and Windows only; the Linux distribution is Detect-only
    but still reads managed config, so a rollout gate flipped on there must fail
    closed to inline dispatch instead of binding a macOS-shaped socket path.
    """


class HookRequest(TypedDict):
    """One hook invocation sent to the daemon.

    ``client_start_ms`` is the only optional field: the epoch-ms stamp the
    client captured at process start, threaded through so the daemon-side flow
    summary can report startup overhead. Older daemons strict-parse the exact
    legacy field set and close on the unknown key, so clients retry once with
    the stamp stripped when a daemon closes before acceptance — the legacy
    frame parses and the daemon's version-skew drain still triggers.
    """

    version: str
    argv: list[str]
    cwd: str
    env: dict[str, str]
    stdin: str
    client_start_ms: NotRequired[int]


class HookResult(TypedDict):
    """Captured hook process result."""

    stdout: str
    stderr: str
    exit_code: int


class RestartingResponse(TypedDict):
    """Version-skew response instructing the caller to run inline."""

    status: Literal["restarting"]


HookResponse = HookResult | RestartingResponse


class HealthRequest(TypedDict):
    """Side-effect-free daemon liveness probe."""

    op: Literal["health"]
    version: str


class HealthResponse(TypedDict):
    """Daemon liveness response carrying the serving binary version."""

    status: Literal["ok"]
    version: str


def protocol_version() -> str:
    """Return the binary version used to detect daemon/client skew."""
    from runlayer_cli import __version__  # noqa: PLC0415 - keep module top stdlib-only

    return __version__


def daemon_endpoint() -> str:
    """Return this user's Unix socket path or Windows named-pipe name."""
    override = os.environ.get(DAEMON_ENDPOINT_ENV)
    if override:
        return override
    if sys.platform == "win32":
        return (
            rf"\\.\pipe\runlayer-aiwatch-{current_windows_user_sid()}-"
            f"{current_windows_session_id()}"
        )
    if sys.platform != "darwin":
        raise UnsupportedDaemonPlatform(
            f"AI Watch hook daemon is not supported on {sys.platform}"
        )
    return daemon_endpoint_for_home(Path.home())


def daemon_endpoint_for_home(home: Path) -> str:
    """Return the macOS socket path for a specific user home.

    For privileged callers (root reconcile/status) probing the console user's
    daemon; ignores the env override on purpose.
    """
    return str(home / "Library" / "Application Support" / "Runlayer" / "aiwatch.sock")


def request_environment(environment: dict[str, str] | None = None) -> dict[str, str]:
    """Copy only hook-relevant variables into an IPC request."""
    source = os.environ if environment is None else environment
    return {name: source[name] for name in HOOK_ENV_ALLOWLIST if name in source}


def encode_frame(payload: object) -> bytes:
    """Serialize one length-prefixed JSON frame."""
    try:
        body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode(
            "utf-8"
        )
    except (TypeError, ValueError, UnicodeError) as exc:
        raise FrameError("frame is not JSON serializable") from exc
    if len(body) > MAX_FRAME_BYTES:
        raise FrameError("frame exceeds maximum size")
    return struct.pack(">I", len(body)) + body


def decode_frame(body: bytes) -> object:
    """Decode one JSON frame body after its length prefix was removed."""
    if len(body) > MAX_FRAME_BYTES:
        raise FrameError("frame exceeds maximum size")
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise FrameError("frame is not valid UTF-8 JSON") from exc


def frame_body_length(prefix: bytes) -> int:
    """Parse a frame's length prefix and enforce the frame-bomb limit.

    Every transport reads bytes differently (deadline socket, overlapped pipe
    handle, anyio stream) but must apply this one size check identically.
    """
    if len(prefix) != FRAME_PREFIX_SIZE:
        raise FrameError("frame prefix is incomplete")
    (length,) = struct.unpack(">I", prefix)
    if length > MAX_FRAME_BYTES:
        raise FrameError("frame exceeds maximum size")
    return length


def parse_hook_request(payload: object) -> HookRequest:
    """Validate an untrusted request before installing its hook context."""
    if not isinstance(payload, dict):
        raise FrameError("request must be an object")
    request = cast(dict[object, object], payload)
    if set(request) - {"client_start_ms"} != {"version", "argv", "cwd", "env", "stdin"}:
        raise FrameError("request fields do not match protocol")

    version = request["version"]
    argv = request["argv"]
    cwd = request["cwd"]
    environment = request["env"]
    stdin = request["stdin"]
    if not isinstance(version, str) or not version or len(version) > 128:
        raise FrameError("invalid request version")
    if (
        not isinstance(argv, list)
        or len(argv) > 128
        or not all(isinstance(arg, str) for arg in argv)
    ):
        raise FrameError("invalid request argv")
    if not isinstance(cwd, str) or not cwd or len(cwd) > 32_768:
        raise FrameError("invalid request cwd")
    if not isinstance(environment, dict):
        raise FrameError("invalid request environment")
    if not all(
        isinstance(key, str) and key in HOOK_ENV_ALLOWLIST and isinstance(value, str)
        for key, value in environment.items()
    ):
        raise FrameError("request environment contains unsupported values")
    if not isinstance(stdin, str):
        raise FrameError("invalid request stdin")

    parsed: HookRequest = {
        "version": version,
        "argv": cast(list[str], argv),
        "cwd": cwd,
        "env": cast(dict[str, str], environment),
        "stdin": stdin,
    }
    if "client_start_ms" in request:
        client_start_ms = request["client_start_ms"]
        # bool is an int subclass; 2**53 bounds the stamp at JSON-safe integer
        # range (epoch ms fits with millennia to spare).
        if (
            type(client_start_ms) is not int
            or client_start_ms <= 0
            or client_start_ms >= 2**53
        ):
            raise FrameError("invalid request client_start_ms")
        parsed["client_start_ms"] = client_start_ms
    return parsed


def parse_health_request(payload: object) -> HealthRequest | None:
    """Parse a health frame, or return ``None`` when it is another frame type."""
    if not isinstance(payload, dict):
        return None
    request = cast(dict[object, object], payload)
    if request.get("op") != "health":
        return None
    if set(request) != {"op", "version"}:
        raise FrameError("health request fields do not match protocol")
    version = request["version"]
    if not isinstance(version, str) or not version or len(version) > 128:
        raise FrameError("invalid health request version")
    return {"op": "health", "version": version}


def parse_health_response(
    payload: object,
) -> HealthResponse | RestartingResponse:
    """Validate a health response before trusting its state or version."""
    if not isinstance(payload, dict):
        raise FrameError("health response fields do not match protocol")
    response = cast(dict[object, object], payload)
    if response == {"status": "restarting"}:
        return {"status": "restarting"}
    if set(response) != {"status", "version"}:
        raise FrameError("health response fields do not match protocol")
    status = response["status"]
    version = response["version"]
    if status != "ok":
        raise FrameError("invalid health response status")
    if not isinstance(version, str) or not version or len(version) > 128:
        raise FrameError("invalid health response version")
    return {"status": "ok", "version": version}


def parse_hook_response(payload: object) -> HookResponse:
    """Validate a daemon response before writing it to hook process streams."""
    if not isinstance(payload, dict):
        raise FrameError("response must be an object")
    response = cast(dict[object, object], payload)
    if response == {"status": "restarting"}:
        return {"status": "restarting"}
    if set(response) != {"stdout", "stderr", "exit_code"}:
        raise FrameError("response fields do not match protocol")
    stdout = response["stdout"]
    stderr = response["stderr"]
    exit_code = response["exit_code"]
    if not isinstance(stdout, str) or not isinstance(stderr, str):
        raise FrameError("invalid response output")
    if type(exit_code) is not int:
        raise FrameError("invalid response exit code")
    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
    }


@lru_cache(maxsize=1)
def current_windows_session_id() -> int:
    """Resolve the current process's WTS session ID without pywin32."""
    if sys.platform != "win32":
        raise OSError("Windows session ID requested on a non-Windows platform")

    from ctypes import wintypes  # noqa: PLC0415 - unavailable API off Windows

    kernel32 = windows_dll("kernel32")
    kernel32.GetCurrentProcessId.argtypes = ()
    kernel32.GetCurrentProcessId.restype = wintypes.DWORD
    kernel32.ProcessIdToSessionId.argtypes = (
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    kernel32.ProcessIdToSessionId.restype = wintypes.BOOL

    session_id = wintypes.DWORD()
    process_id = kernel32.GetCurrentProcessId()
    if not kernel32.ProcessIdToSessionId(process_id, ctypes.byref(session_id)):
        raise windows_error()
    return int(session_id.value)


@lru_cache(maxsize=1)
def current_windows_user_sid() -> str:
    """Resolve the current process token's user SID without pywin32."""
    if sys.platform != "win32":
        raise OSError("Windows user SID requested on a non-Windows platform")

    from ctypes import wintypes  # noqa: PLC0415 - unavailable API off Windows

    token_query = 0x0008
    token_user = 1
    token = wintypes.HANDLE()
    kernel32 = windows_dll("kernel32")
    advapi32 = windows_dll("advapi32")

    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    advapi32.OpenProcessToken.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.HANDLE),
    )
    advapi32.OpenProcessToken.restype = wintypes.BOOL
    advapi32.GetTokenInformation.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
    )
    advapi32.GetTokenInformation.restype = wintypes.BOOL
    advapi32.ConvertSidToStringSidW.argtypes = (
        wintypes.LPVOID,
        ctypes.POINTER(wintypes.LPWSTR),
    )
    advapi32.ConvertSidToStringSidW.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
    kernel32.LocalFree.argtypes = (wintypes.HLOCAL,)
    kernel32.LocalFree.restype = wintypes.HLOCAL

    if not advapi32.OpenProcessToken(
        kernel32.GetCurrentProcess(), token_query, ctypes.byref(token)
    ):
        raise windows_error()

    try:
        required = wintypes.DWORD()
        advapi32.GetTokenInformation(
            token,
            token_user,
            None,
            0,
            ctypes.byref(required),
        )
        if required.value == 0:
            raise windows_error()
        buffer = ctypes.create_string_buffer(required.value)
        if not advapi32.GetTokenInformation(
            token,
            token_user,
            buffer,
            required,
            ctypes.byref(required),
        ):
            raise windows_error()

        sid_pointer = ctypes.cast(
            buffer, ctypes.POINTER(ctypes.c_void_p)
        ).contents.value
        sid_string = wintypes.LPWSTR()
        if not advapi32.ConvertSidToStringSidW(
            sid_pointer,
            ctypes.byref(sid_string),
        ):
            raise windows_error()
        try:
            if not sid_string.value:
                raise OSError("current Windows user SID is empty")
            return sid_string.value
        finally:
            kernel32.LocalFree(ctypes.cast(sid_string, ctypes.c_void_p))
    finally:
        kernel32.CloseHandle(token)


class Overlapped(ctypes.Structure):
    """OVERLAPPED for ctypes I/O, kept wintypes-free so the module top stays portable."""

    _fields_ = [
        ("Internal", ctypes.c_size_t),
        ("InternalHigh", ctypes.c_size_t),
        ("Offset", ctypes.c_uint32),
        ("OffsetHigh", ctypes.c_uint32),
        ("hEvent", ctypes.c_void_p),
    ]


def windows_dll(name: str) -> Any:
    return ctypes.WinDLL(name, use_last_error=True)  # ty: ignore[unresolved-attribute]


def last_windows_error() -> int:
    return int(
        ctypes.get_last_error()  # ty: ignore[unresolved-attribute]
    )


def windows_error(code: int | None = None) -> OSError:
    if code is None:
        code = last_windows_error()
    return ctypes.WinError(code)  # ty: ignore[unresolved-attribute]
