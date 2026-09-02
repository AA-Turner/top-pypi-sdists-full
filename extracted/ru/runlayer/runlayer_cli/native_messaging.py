"""Chrome Native Messaging host for the AI Watch browser extension."""

from __future__ import annotations

import json
import platform
import socket
import struct
import subprocess
import sys
from typing import Any, BinaryIO, TextIO, TypedDict, cast

from runlayer_cli.scan.device import get_device_metadata

HOST_NAME = "com.runlayer.aiwatch"
REQUEST_IDENTITY = "identity.get"
PROTOCOL_VERSION = 1
MAX_MESSAGE_BYTES = 1024 * 1024


class NativeIdentity(TypedDict):
    username: str | None
    deviceName: str | None


class NativeIdentityResponse(TypedDict):
    ok: bool
    version: int
    identity: NativeIdentity


class NativeErrorResponse(TypedDict):
    ok: bool
    version: int
    error: str


def _clean_string(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _macos_computer_name() -> str | None:
    try:
        result = subprocess.run(
            ["scutil", "--get", "ComputerName"],
            capture_output=True,
            text=True,
            timeout=2,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return _clean_string(result.stdout)


def _device_name() -> str | None:
    if platform.system().lower() == "darwin":
        macos_name = _macos_computer_name()
        if macos_name:
            return macos_name
    try:
        return _clean_string(socket.gethostname())
    except Exception:
        return None


def get_native_identity() -> NativeIdentity:
    metadata = get_device_metadata()
    return {
        "username": _clean_string(metadata.get("username")),
        "deviceName": _device_name(),
    }


def _identity_response() -> NativeIdentityResponse:
    return {
        "ok": True,
        "version": PROTOCOL_VERSION,
        "identity": get_native_identity(),
    }


def _error_response(error: str) -> NativeErrorResponse:
    return {"ok": False, "version": PROTOCOL_VERSION, "error": error}


def handle_message(message: object) -> NativeIdentityResponse | NativeErrorResponse:
    if not isinstance(message, dict):
        return _error_response("invalid_message")
    payload = cast(dict[str, Any], message)
    if payload.get("type") != REQUEST_IDENTITY:
        return _error_response("unsupported_type")
    return _identity_response()


def read_message(stream: BinaryIO) -> object | None:
    raw_length = stream.read(4)
    if raw_length == b"":
        return None
    if len(raw_length) != 4:
        raise ValueError("truncated_length")
    message_length = struct.unpack("<I", raw_length)[0]
    if message_length > MAX_MESSAGE_BYTES:
        raise ValueError("message_too_large")
    raw_message = stream.read(message_length)
    if len(raw_message) != message_length:
        raise ValueError("truncated_message")
    return json.loads(raw_message.decode("utf-8"))


def write_message(stream: BinaryIO, message: object) -> None:
    payload = json.dumps(message, separators=(",", ":")).encode("utf-8")
    stream.write(struct.pack("<I", len(payload)))
    stream.write(payload)
    stream.flush()


def run_native_messaging_host(
    stdin: BinaryIO | None = None,
    stdout: BinaryIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    input_stream = stdin or sys.stdin.buffer
    output_stream = stdout or sys.stdout.buffer
    error_stream = stderr or sys.stderr

    while True:
        try:
            message = read_message(input_stream)
        except Exception as exc:
            print(f"{HOST_NAME}: failed to read message: {exc}", file=error_stream)
            return 1
        if message is None:
            return 0
        try:
            response: dict[str, Any] | NativeIdentityResponse | NativeErrorResponse = (
                handle_message(message)
            )
        except Exception as exc:
            print(f"{HOST_NAME}: failed to handle message: {exc}", file=error_stream)
            response = _error_response("internal_error")
        write_message(output_stream, response)
