"""Best-effort standard-library AI Watch daemon client."""

from __future__ import annotations

import socket
import sys
import tempfile
import threading
import time
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from runlayer_cli import mdm_config
from runlayer_cli.hook import daemon_client, daemon_protocol
from tests.daemon_frame_helpers import read_frame, write_frame

pytestmark = pytest.mark.skipif(
    sys.platform == "win32",
    reason="Unix-socket client tests; Windows named pipe has a separate integration test",
)


@pytest.fixture
def endpoint() -> Iterator[Path]:
    # Darwin limits AF_UNIX paths to 103 bytes; pytest's tmp_path can exceed it.
    with tempfile.TemporaryDirectory(prefix="rl-aiwatch-", dir="/tmp") as directory:
        yield Path(directory) / "daemon.sock"


def _start_server(
    path: Path,
    handler: Callable[[object, object], None],
) -> tuple[threading.Thread, list[object]]:
    ready = threading.Event()
    received: list[object] = []

    def serve() -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
            listener.bind(str(path))
            listener.listen()
            ready.set()
            connection, _ = listener.accept()
            with connection, connection.makefile("rwb", buffering=0) as stream:
                request = read_frame(stream)
                received.append(request)
                handler(stream, request)

    thread = threading.Thread(target=serve)
    thread.start()
    assert ready.wait(timeout=5)
    return thread, received


def _enable_daemon(monkeypatch, endpoint: Path) -> None:
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)
    monkeypatch.setattr(daemon_client, "daemon_endpoint", lambda: str(endpoint))


def test_daemon_gate_requires_managed_org_key_and_backend_flag(monkeypatch) -> None:
    monkeypatch.setattr(
        mdm_config,
        "read_managed_config",
        lambda: {"org_api_key": "rl_org_test", "daemon_enabled": True},
    )
    assert daemon_client.daemon_is_enabled() is True

    monkeypatch.setattr(
        mdm_config,
        "read_managed_config",
        lambda: {"org_api_key": "rl_org_test", "daemon_enabled": False},
    )
    assert daemon_client.daemon_is_enabled() is False

    monkeypatch.setattr(
        mdm_config,
        "read_managed_config",
        lambda: {"daemon_enabled": True},
    )
    assert daemon_client.daemon_is_enabled() is False


def test_gate_off_does_not_attempt_connection(monkeypatch) -> None:
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: False)
    monkeypatch.setattr(
        daemon_client,
        "_send_unix_request",
        lambda *_args: (_ for _ in ()).throw(AssertionError("must not connect")),
    )

    assert daemon_client.try_daemon_hook("{}") is None


def test_unsupported_platform_falls_back_inline(monkeypatch) -> None:
    monkeypatch.setattr(daemon_client, "daemon_is_enabled", lambda: True)
    monkeypatch.delenv(daemon_protocol.DAEMON_ENDPOINT_ENV, raising=False)
    monkeypatch.setattr(daemon_protocol.sys, "platform", "linux")
    monkeypatch.setattr(
        daemon_client,
        "_send_unix_request",
        lambda *_args: (_ for _ in ()).throw(AssertionError("must not connect")),
    )

    assert daemon_client.try_daemon_hook("{}") is None


def test_gate_failure_falls_back_inline(monkeypatch) -> None:
    monkeypatch.setattr(
        daemon_client,
        "daemon_is_enabled",
        lambda: (_ for _ in ()).throw(RuntimeError("gate failed")),
    )

    assert daemon_client.try_daemon_hook("{}") is None


def test_successful_round_trip_returns_captured_hook_result(
    monkeypatch, endpoint
) -> None:
    _enable_daemon(monkeypatch, endpoint)
    monkeypatch.setattr(daemon_client.sys, "argv", ["aiwatch", "--client", "cursor"])
    monkeypatch.setenv("RUNLAYER_HOOK_CLIENT", "cursor")
    monkeypatch.setenv("RUNLAYER_API_KEY", "must-not-cross-ipc")

    thread, received = _start_server(
        endpoint,
        lambda stream, _request: write_frame(
            stream,
            {"stdout": '{"permission":"allow"}', "stderr": "", "exit_code": 0},
        ),
    )

    result = daemon_client.try_daemon_hook('{"hook_event_name":"PreToolUse"}')
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert result == {
        "stdout": '{"permission":"allow"}',
        "stderr": "",
        "exit_code": 0,
    }
    request = daemon_protocol.parse_hook_request(received[0])
    assert request["stdin"] == '{"hook_event_name":"PreToolUse"}'
    assert request["argv"] == ["aiwatch", "--client", "cursor"]
    assert request["env"] == {"RUNLAYER_HOOK_CLIENT": "cursor"}


def test_health_probe_returns_versioned_response_without_gate_check(endpoint) -> None:
    response = {
        "status": "ok",
        "version": daemon_protocol.protocol_version(),
    }
    thread, received = _start_server(
        endpoint,
        lambda stream, _request: write_frame(stream, response),
    )

    assert daemon_client.probe_daemon(str(endpoint)) == response
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert received == [
        {
            "op": "health",
            "version": daemon_protocol.protocol_version(),
        }
    ]


def test_health_probe_treats_malformed_response_as_unhealthy(endpoint) -> None:
    thread, _ = _start_server(
        endpoint,
        lambda stream, _request: write_frame(
            stream,
            {"status": "accepted"},
        ),
    )

    assert daemon_client.probe_daemon(str(endpoint)) is None
    thread.join(timeout=5)
    assert not thread.is_alive()


def test_missing_daemon_falls_back_inline(monkeypatch, endpoint) -> None:
    _enable_daemon(monkeypatch, endpoint)

    assert daemon_client.try_daemon_hook("{}") is None


def test_mid_response_crash_falls_back_inline(monkeypatch, endpoint) -> None:
    _enable_daemon(monkeypatch, endpoint)
    thread, _ = _start_server(endpoint, lambda _stream, _request: None)

    assert daemon_client.try_daemon_hook("{}") is None
    thread.join(timeout=5)
    assert not thread.is_alive()


def test_stalled_response_times_out_to_inline(monkeypatch, endpoint) -> None:
    _enable_daemon(monkeypatch, endpoint)
    monkeypatch.setattr(daemon_client, "RESPONSE_TIMEOUT_SECONDS", 0.05)
    release_server = threading.Event()
    thread, _ = _start_server(
        endpoint,
        lambda _stream, _request: release_server.wait(timeout=5),
    )

    started_at = time.monotonic()
    assert daemon_client.try_daemon_hook("{}") is None
    elapsed = time.monotonic() - started_at
    release_server.set()
    thread.join(timeout=5)

    assert elapsed < 1
    assert not thread.is_alive()


def test_accepted_hook_timeout_does_not_replay_inline(monkeypatch, endpoint) -> None:
    _enable_daemon(monkeypatch, endpoint)
    monkeypatch.setattr(daemon_client, "RESPONSE_TIMEOUT_SECONDS", 0.05)
    release_server = threading.Event()

    def accept_then_stall(stream, _request) -> None:
        write_frame(stream, {"status": "accepted"})
        assert stream.read(1) == daemon_protocol.REQUEST_ACCEPTED_ACK
        release_server.wait(timeout=5)

    thread, _ = _start_server(endpoint, accept_then_stall)

    result = daemon_client.try_daemon_hook("{}")
    release_server.set()
    thread.join(timeout=5)

    assert result == {
        "stdout": "",
        "stderr": "AI Watch daemon stopped before returning a hook result.\n",
        "exit_code": 2,
    }
    assert not thread.is_alive()


def test_failed_accept_ack_write_falls_back_inline(monkeypatch, endpoint) -> None:
    """A failed ACK write means the daemon never dispatched; replay stays safe."""
    _enable_daemon(monkeypatch, endpoint)
    real_send = daemon_client._send_unix_all

    def send_all_failing_ack(client, data, *, deadline) -> None:
        if data == daemon_protocol.REQUEST_ACCEPTED_ACK:
            raise OSError("ack write failed")
        real_send(client, data, deadline=deadline)

    monkeypatch.setattr(daemon_client, "_send_unix_all", send_all_failing_ack)
    dispatched = threading.Event()

    def accept_then_require_ack(stream, _request) -> None:
        write_frame(stream, {"status": "accepted"})
        # Mirror the daemon: hook dispatch happens only after the full ACK.
        if stream.read(1) == daemon_protocol.REQUEST_ACCEPTED_ACK:
            dispatched.set()

    thread, _ = _start_server(endpoint, accept_then_require_ack)

    result = daemon_client.try_daemon_hook("{}")
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert not dispatched.is_set()
    assert result is None


def test_slow_drip_response_cannot_reset_total_deadline(monkeypatch, endpoint) -> None:
    _enable_daemon(monkeypatch, endpoint)
    monkeypatch.setattr(daemon_client, "RESPONSE_TIMEOUT_SECONDS", 0.05)

    def drip_response(stream, _request) -> None:
        framed = daemon_protocol.encode_frame(
            {"stdout": "", "stderr": "", "exit_code": 0}
        )
        for byte in framed:
            try:
                stream.write(bytes([byte]))
                stream.flush()
            except OSError:
                break
            time.sleep(0.03)

    thread, _ = _start_server(endpoint, drip_response)

    started_at = time.monotonic()
    assert daemon_client.try_daemon_hook("{}") is None
    elapsed = time.monotonic() - started_at
    thread.join(timeout=5)

    assert elapsed < 0.2
    assert not thread.is_alive()


def test_restarting_response_falls_back_inline(monkeypatch, endpoint) -> None:
    _enable_daemon(monkeypatch, endpoint)
    thread, _ = _start_server(
        endpoint,
        lambda stream, _request: write_frame(stream, {"status": "restarting"}),
    )

    assert daemon_client.try_daemon_hook("{}") is None
    thread.join(timeout=5)
    assert not thread.is_alive()


def test_closed_before_acceptance_retries_legacy_frame_for_old_daemon(
    monkeypatch, endpoint
) -> None:
    """Old daemons strict-parse away client_start_ms and close silently.

    The retry must strip the stamp so the old daemon gets a parseable frame
    and its version-skew drain can trigger ("restarting"); the hook then
    falls back inline.
    """
    _enable_daemon(monkeypatch, endpoint)
    ready = threading.Event()
    received: list[dict[str, object]] = []

    def serve() -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
            listener.bind(str(endpoint))
            listener.listen()
            ready.set()
            # Strict old daemon: the unknown key fails parse, close silently.
            connection, _ = listener.accept()
            with connection, connection.makefile("rwb", buffering=0) as stream:
                received.append(read_frame(stream))
            # Retry: the legacy frame parses; version skew answers restarting.
            connection, _ = listener.accept()
            with connection, connection.makefile("rwb", buffering=0) as stream:
                received.append(read_frame(stream))
                write_frame(stream, {"status": "restarting"})

    thread = threading.Thread(target=serve)
    thread.start()
    assert ready.wait(timeout=5)

    result = daemon_client.try_daemon_hook("{}", client_start_ms=1723500000123)
    thread.join(timeout=5)

    assert not thread.is_alive()
    assert result is None
    assert len(received) == 2
    assert received[0]["client_start_ms"] == 1723500000123
    assert "client_start_ms" not in received[1]
    legacy = daemon_protocol.parse_hook_request(received[1])
    assert legacy["version"] == daemon_protocol.protocol_version()
    assert legacy["stdin"] == "{}"


def test_closed_before_acceptance_without_stamp_does_not_retry(
    monkeypatch, endpoint
) -> None:
    connects: list[int] = []

    def counting_send(endpoint_path, request, **kwargs):
        connects.append(1)
        raise daemon_client._DaemonClosedBeforeAcceptanceError()

    _enable_daemon(monkeypatch, endpoint)
    monkeypatch.setattr(daemon_client, "_send_unix_request", counting_send)

    assert daemon_client.try_daemon_hook("{}") is None
    assert len(connects) == 1


def test_stalled_response_with_start_stamp_does_not_retry(
    monkeypatch, endpoint
) -> None:
    """A timeout is not the old-daemon signature; retrying would double it."""
    _enable_daemon(monkeypatch, endpoint)
    monkeypatch.setattr(daemon_client, "RESPONSE_TIMEOUT_SECONDS", 0.05)
    release_server = threading.Event()
    thread, received = _start_server(
        endpoint,
        lambda _stream, _request: release_server.wait(timeout=5),
    )

    started_at = time.monotonic()
    assert daemon_client.try_daemon_hook("{}", client_start_ms=1723500000123) is None
    elapsed = time.monotonic() - started_at
    release_server.set()
    thread.join(timeout=5)

    assert elapsed < 1
    assert len(received) == 1
    assert not thread.is_alive()
