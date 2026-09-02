"""Tests for the AI Watch Chrome Native Messaging host."""

from __future__ import annotations

import io

from runlayer_cli import native_messaging as nm


def test_native_message_framing_roundtrip() -> None:
    stream = io.BytesIO()

    nm.write_message(stream, {"type": nm.REQUEST_IDENTITY, "version": 1})
    stream.seek(0)

    assert nm.read_message(stream) == {"type": nm.REQUEST_IDENTITY, "version": 1}


def test_identity_request_returns_os_identity(monkeypatch) -> None:
    monkeypatch.setattr(
        nm,
        "get_device_metadata",
        lambda: {"username": " alice ", "hostname": "ignored", "os": "darwin", "os_version": "x"},
    )
    monkeypatch.setattr(nm, "_device_name", lambda: "Alice Mac")

    response = nm.handle_message({"type": nm.REQUEST_IDENTITY})

    assert response == {
        "ok": True,
        "version": nm.PROTOCOL_VERSION,
        "identity": {
            "username": "alice",
            "deviceName": "Alice Mac",
        },
    }


def test_unsupported_message_returns_error() -> None:
    response = nm.handle_message({"type": "secrets.get"})

    assert response == {
        "ok": False,
        "version": nm.PROTOCOL_VERSION,
        "error": "unsupported_type",
    }


def test_native_host_reads_request_and_writes_response(monkeypatch) -> None:
    monkeypatch.setattr(
        nm,
        "get_device_metadata",
        lambda: {"username": "alice", "hostname": "ignored", "os": "darwin", "os_version": "x"},
    )
    monkeypatch.setattr(nm, "_device_name", lambda: "Alice Mac")
    stdin = io.BytesIO()
    stdout = io.BytesIO()
    stderr = io.StringIO()
    nm.write_message(stdin, {"type": nm.REQUEST_IDENTITY})
    stdin.seek(0)

    exit_code = nm.run_native_messaging_host(stdin=stdin, stdout=stdout, stderr=stderr)

    assert exit_code == 0
    assert stderr.getvalue() == ""
    stdout.seek(0)
    assert nm.read_message(stdout) == {
        "ok": True,
        "version": nm.PROTOCOL_VERSION,
        "identity": {
            "username": "alice",
            "deviceName": "Alice Mac",
        },
    }
