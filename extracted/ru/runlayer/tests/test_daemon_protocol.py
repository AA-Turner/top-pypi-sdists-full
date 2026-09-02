"""Length-prefixed AI Watch daemon IPC contract."""

from __future__ import annotations

import io
import struct
from ctypes import wintypes

import pytest

from runlayer_cli.hook import daemon_protocol
from tests.daemon_frame_helpers import read_frame, write_frame


def _request(**overrides: object) -> dict[str, object]:
    request: dict[str, object] = {
        "version": "1.2.3",
        "argv": ["aiwatch", "--client", "cursor"],
        "cwd": "/workspace",
        "env": {"RUNLAYER_HOOK_CLIENT": "cursor"},
        "stdin": '{"hook_event_name":"PreToolUse"}',
    }
    request.update(overrides)
    return request


def test_frame_round_trip() -> None:
    stream = io.BytesIO()
    request = _request()

    write_frame(stream, request)
    stream.seek(0)

    assert read_frame(stream) == request
    assert daemon_protocol.parse_hook_request(request) == request


def test_write_frame_retries_partial_writes() -> None:
    class PartialWriter(io.BytesIO):
        def write(self, data: bytes) -> int:
            return super().write(data[:3])

    stream = PartialWriter()
    request = _request()

    write_frame(stream, request)
    stream.seek(0)

    assert read_frame(stream) == request


@pytest.mark.parametrize(
    "framed",
    [
        b"",
        b"\x00\x00",
        struct.pack(">I", 4) + b"{}",
        struct.pack(">I", 1) + b"\xff",
        struct.pack(">I", daemon_protocol.MAX_FRAME_BYTES + 1),
    ],
)
def test_read_frame_rejects_truncated_invalid_or_oversized_data(framed: bytes) -> None:
    with pytest.raises(daemon_protocol.FrameError):
        read_frame(io.BytesIO(framed))


@pytest.mark.parametrize(
    "prefix",
    [
        b"",
        b"\x00\x00\x00",
        b"\x00\x00\x00\x00\x00",
        struct.pack(">I", daemon_protocol.MAX_FRAME_BYTES + 1),
    ],
)
def test_frame_body_length_rejects_bad_prefix_or_oversized_body(
    prefix: bytes,
) -> None:
    with pytest.raises(daemon_protocol.FrameError):
        daemon_protocol.frame_body_length(prefix)


def test_frame_body_length_accepts_the_maximum_frame() -> None:
    largest = struct.pack(">I", daemon_protocol.MAX_FRAME_BYTES)

    assert daemon_protocol.frame_body_length(largest) == daemon_protocol.MAX_FRAME_BYTES


def test_encode_frame_rejects_oversized_payload() -> None:
    with pytest.raises(daemon_protocol.FrameError, match="maximum"):
        daemon_protocol.encode_frame("x" * daemon_protocol.MAX_FRAME_BYTES)


@pytest.mark.parametrize(
    "override",
    [
        {"version": ""},
        {"argv": "aiwatch"},
        {"cwd": ""},
        {"env": {"RUNLAYER_API_KEY": "secret"}},
        {"env": {"RUNLAYER_HOOK_CLIENT": 1}},
        {"stdin": b"{}"},
        {"extra": True},
        {"client_start_ms": 0},
        {"client_start_ms": -5},
        {"client_start_ms": True},
        {"client_start_ms": "1723500000123"},
        {"client_start_ms": 2**53},
    ],
)
def test_parse_hook_request_rejects_invalid_fields(
    override: dict[str, object],
) -> None:
    with pytest.raises(daemon_protocol.FrameError):
        daemon_protocol.parse_hook_request(_request(**override))


def test_parse_hook_request_round_trips_optional_client_start_ms() -> None:
    stamped = _request(client_start_ms=1723500000123)

    assert daemon_protocol.parse_hook_request(stamped) == stamped
    # Absence stays legal: older shims and thin clients never send the stamp.
    assert "client_start_ms" not in daemon_protocol.parse_hook_request(_request())


def test_parse_hook_response_accepts_result_and_restarting() -> None:
    assert daemon_protocol.parse_hook_response(
        {"stdout": "out", "stderr": "err", "exit_code": 2}
    ) == {"stdout": "out", "stderr": "err", "exit_code": 2}
    assert daemon_protocol.parse_hook_response({"status": "restarting"}) == {
        "status": "restarting"
    }


def test_health_frames_are_strict_and_versioned() -> None:
    request = {"op": "health", "version": "1.2.3"}
    response = {"status": "ok", "version": "1.2.3"}

    assert daemon_protocol.parse_health_request(request) == request
    assert daemon_protocol.parse_health_request(_request()) is None
    assert daemon_protocol.parse_health_response(response) == response


def test_health_response_accepts_restarting_daemon() -> None:
    response = {"status": "restarting"}

    assert daemon_protocol.parse_health_response(response) == response


@pytest.mark.parametrize(
    "frame",
    [
        {"op": "health"},
        {"op": "health", "version": ""},
        {"op": "health", "version": "1.2.3", "extra": True},
    ],
)
def test_parse_health_request_rejects_malformed_health_frame(frame: object) -> None:
    with pytest.raises(daemon_protocol.FrameError):
        daemon_protocol.parse_health_request(frame)


@pytest.mark.parametrize(
    "frame",
    [
        None,
        {"status": "ok"},
        {"status": "running", "version": "1.2.3"},
        {"status": "ok", "version": ""},
    ],
)
def test_parse_health_response_rejects_invalid_frame(frame: object) -> None:
    with pytest.raises(daemon_protocol.FrameError):
        daemon_protocol.parse_health_response(frame)


@pytest.mark.parametrize(
    "response",
    [
        None,
        {"status": "running"},
        {"stdout": "out", "stderr": "err", "exit_code": True},
        {"stdout": b"out", "stderr": "err", "exit_code": 0},
    ],
)
def test_parse_hook_response_rejects_invalid_fields(response: object) -> None:
    with pytest.raises(daemon_protocol.FrameError):
        daemon_protocol.parse_hook_response(response)


def test_request_environment_copies_only_allowlisted_values() -> None:
    environment = {
        "RUNLAYER_HOOK_CLIENT": "cursor",
        "RUNLAYER_FLOW_TRACE": "0",
        "QWEN_HOME": "/tmp/qwen",
        "GROK_HOME": "/tmp/grok",
        "GROK_HOOK_EVENT": "PreToolUse",
        "COPILOT_ADDITIONAL_MCP_CONFIG": "{}",
        "RUNLAYER_HOOK_GZIP": "0",
        # Carries the Devin host signal the double-fire guard reads.
        "DEVIN_PROJECT_DIR": "/repo",
        "RUNLAYER_API_KEY": "must-not-cross-ipc",
    }

    assert daemon_protocol.request_environment(environment) == {
        "RUNLAYER_HOOK_CLIENT": "cursor",
        "RUNLAYER_FLOW_TRACE": "0",
        "QWEN_HOME": "/tmp/qwen",
        "GROK_HOME": "/tmp/grok",
        "GROK_HOOK_EVENT": "PreToolUse",
        "COPILOT_ADDITIONAL_MCP_CONFIG": "{}",
        # The gzip kill switch crosses IPC so daemon-served hooks honor it.
        "RUNLAYER_HOOK_GZIP": "0",
        "DEVIN_PROJECT_DIR": "/repo",
    }


def test_daemon_endpoint_honors_test_override(monkeypatch, tmp_path) -> None:
    endpoint = tmp_path / "daemon.sock"
    monkeypatch.setenv(daemon_protocol.DAEMON_ENDPOINT_ENV, str(endpoint))

    assert daemon_protocol.daemon_endpoint() == str(endpoint)


def test_daemon_endpoint_rejects_unsupported_platform(monkeypatch) -> None:
    monkeypatch.delenv(daemon_protocol.DAEMON_ENDPOINT_ENV, raising=False)
    monkeypatch.setattr(daemon_protocol.sys, "platform", "linux")

    with pytest.raises(daemon_protocol.UnsupportedDaemonPlatform):
        daemon_protocol.daemon_endpoint()


def test_windows_daemon_endpoint_is_scoped_to_user_session(monkeypatch) -> None:
    monkeypatch.delenv(daemon_protocol.DAEMON_ENDPOINT_ENV, raising=False)
    monkeypatch.setattr(daemon_protocol.sys, "platform", "win32")
    monkeypatch.setattr(
        daemon_protocol,
        "current_windows_user_sid",
        lambda: "S-1-5-21-test",
    )
    monkeypatch.setattr(
        daemon_protocol,
        "current_windows_session_id",
        lambda: 7,
        raising=False,
    )

    session_seven = daemon_protocol.daemon_endpoint()
    monkeypatch.setattr(daemon_protocol, "current_windows_session_id", lambda: 8)

    assert session_seven == r"\\.\pipe\runlayer-aiwatch-S-1-5-21-test-7"
    assert daemon_protocol.daemon_endpoint() != session_seven


def test_current_windows_session_id_uses_current_process(monkeypatch) -> None:
    class FakeFunction:
        def __init__(self, implementation):
            self.implementation = implementation
            self.argtypes = None
            self.restype = None

        def __call__(self, *args):
            return self.implementation(*args)

    class FakeKernel32:
        def __init__(self) -> None:
            self.GetCurrentProcessId = FakeFunction(lambda: 1234)
            self.ProcessIdToSessionId = FakeFunction(self.process_id_to_session_id)

        @staticmethod
        def process_id_to_session_id(process_id, session_id_pointer) -> bool:
            assert process_id == 1234
            session_id = daemon_protocol.ctypes.cast(
                session_id_pointer,
                daemon_protocol.ctypes.POINTER(wintypes.DWORD),
            )
            session_id.contents.value = 7
            return True

    monkeypatch.setattr(daemon_protocol.sys, "platform", "win32")
    monkeypatch.setattr(daemon_protocol, "windows_dll", lambda _name: FakeKernel32())
    daemon_protocol.current_windows_session_id.cache_clear()
    try:
        assert daemon_protocol.current_windows_session_id() == 7
    finally:
        daemon_protocol.current_windows_session_id.cache_clear()


def test_daemon_endpoint_uses_macos_path_on_darwin(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv(daemon_protocol.DAEMON_ENDPOINT_ENV, raising=False)
    monkeypatch.setattr(daemon_protocol.sys, "platform", "darwin")
    monkeypatch.setattr(
        daemon_protocol.Path, "home", classmethod(lambda _cls: tmp_path)
    )

    assert daemon_protocol.daemon_endpoint() == str(
        tmp_path / "Library" / "Application Support" / "Runlayer" / "aiwatch.sock"
    )


def test_retry_kill_switch_in_hook_env_allowlist():
    """RUNLAYER_HOOK_RETRIES is read at send time in relay._post; without this
    allowlist entry the daemon path silently ignores the advertised kill
    switch (same failure class as the gzip switch)."""
    from runlayer_cli.hook.daemon_protocol import HOOK_ENV_ALLOWLIST

    assert "RUNLAYER_HOOK_RETRIES" in HOOK_ENV_ALLOWLIST
