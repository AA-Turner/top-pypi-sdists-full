"""Tests for the AI Watch Chrome Native Messaging host."""

from __future__ import annotations

import io
import sys
from types import SimpleNamespace

from runlayer_cli import native_messaging as nm


def test_windows_standard_streams_use_binary_mode(monkeypatch):
    calls = []
    monkeypatch.setattr(nm.sys, "platform", "win32")
    monkeypatch.setattr(nm.os, "O_BINARY", 32768, raising=False)
    monkeypatch.setitem(
        sys.modules,
        "msvcrt",
        SimpleNamespace(setmode=lambda fd, mode: calls.append((fd, mode))),
    )
    monkeypatch.setattr(
        sys, "stdin", SimpleNamespace(fileno=lambda: 0, buffer=io.BytesIO())
    )
    monkeypatch.setattr(
        sys, "stdout", SimpleNamespace(fileno=lambda: 1, buffer=io.BytesIO())
    )
    assert nm.run_native_messaging_host() == 0
    assert calls == [(0, 32768), (1, 32768)]


def test_native_message_framing_roundtrip() -> None:
    stream = io.BytesIO()

    nm.write_message(stream, {"type": nm.REQUEST_IDENTITY, "version": 1})
    stream.seek(0)

    assert nm.read_message(stream) == {"type": nm.REQUEST_IDENTITY, "version": 1}


def test_identity_request_returns_os_identity(monkeypatch) -> None:
    monkeypatch.setattr(
        nm,
        "get_device_metadata",
        lambda: {
            "username": " alice ",
            "hostname": "ignored",
            "os": "darwin",
            "os_version": "x",
        },
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
        lambda: {
            "username": "alice",
            "hostname": "ignored",
            "os": "darwin",
            "os_version": "x",
        },
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
