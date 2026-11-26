"""Shared pieces of the air-gap link: framing, pairing, auth, target profile."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import platform
import re
import secrets
import struct
import sys
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = 1
DEFAULT_PORT = 8765
MAX_FRAME = 1 << 20  # control frames only; wheels are streamed raw
CHUNK = 1 << 16
TOKEN_PREFIX = "pm1-"

_TAG_RE = re.compile(r"^[A-Za-z0-9_.]{1,64}$")
_ENV_KEYS = {
    "implementation_name",
    "implementation_version",
    "os_name",
    "platform_machine",
    "platform_release",
    "platform_system",
    "platform_version",
    "python_full_version",
    "platform_python_implementation",
    "python_version",
    "sys_platform",
}


class AirgapError(Exception):
    """Base error of the air-gap link."""


class ProtocolError(AirgapError):
    """Malformed or unexpected data on the wire."""


class AuthError(AirgapError):
    """The peer failed authentication or certificate pinning."""


# --------------------------------------------------------------------------- files
def config_dir() -> Path:
    root = os.environ.get("PIPMASTER_HOME")
    path = Path(root) if root else Path.home() / ".pipmaster" / "airgap"
    path.mkdir(parents=True, exist_ok=True)
    _chmod(path, 0o700)
    return path


def _chmod(path: Path, mode: int) -> None:
    try:
        os.chmod(path, mode)
    except OSError:
        pass  # best effort: Windows ACLs differ


def write_private(path: Path, data: bytes) -> None:
    """Write a secret file readable by the owner only (best effort on Windows)."""
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "wb") as fh:
        fh.write(data)
    _chmod(path, 0o600)


# ------------------------------------------------------------------------- framing
def send_frame(sock: Any, obj: dict[str, Any]) -> None:
    data = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    if len(data) > MAX_FRAME:
        raise ProtocolError("frame too large")
    sock.sendall(struct.pack(">I", len(data)) + data)


def recv_exact(sock: Any, size: int) -> bytes:
    buf = bytearray()
    while len(buf) < size:
        chunk = sock.recv(min(size - len(buf), CHUNK))
        if not chunk:
            raise ProtocolError("connection closed")
        buf += chunk
    return bytes(buf)


def recv_frame(sock: Any) -> dict[str, Any]:
    (size,) = struct.unpack(">I", recv_exact(sock, 4))
    if size > MAX_FRAME:
        raise ProtocolError("frame too large")
    try:
        obj = json.loads(recv_exact(sock, size).decode("utf-8"))
    except ValueError as exc:
        raise ProtocolError("invalid frame") from exc
    if not isinstance(obj, dict):
        raise ProtocolError("frame is not an object")
    return obj


# ------------------------------------------------------------------------- pairing
def b64e(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def b64d(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def make_token(
    fingerprint: str,
    secret: bytes,
    host: str | None = None,
    port: int = DEFAULT_PORT,
) -> str:
    raw = json.dumps(
        {
            "v": PROTOCOL_VERSION,
            "fp": fingerprint,
            "key": b64e(secret),
            "host": host,
            "port": port,
        },
        separators=(",", ":"),
    )
    return TOKEN_PREFIX + b64e(raw.encode("utf-8"))


def parse_token(token: str) -> dict[str, Any]:
    token = token.strip()
    if not token.startswith(TOKEN_PREFIX):
        raise AirgapError("not a pipmaster pairing token")
    try:
        data = json.loads(b64d(token[len(TOKEN_PREFIX) :]))
        fp = str(data["fp"]).lower()
        key = b64d(data["key"])
        port = int(data.get("port") or DEFAULT_PORT)
    except (ValueError, KeyError, TypeError) as exc:
        raise AirgapError("malformed pairing token") from exc
    if len(fp) != 64 or len(key) < 32:
        raise AirgapError("malformed pairing token")
    return {"fp": fp, "key": key, "host": data.get("host"), "port": port}


# ---------------------------------------------------------------------------- auth
def _mac(key: bytes, tag: bytes, first: bytes, second: bytes) -> bytes:
    return hmac.new(key, tag + first + second, hashlib.sha256).digest()


def server_auth(sock: Any, key: bytes) -> bool:
    """Challenge-response with the paired secret. Returns False on any failure."""
    server_nonce = secrets.token_bytes(32)
    send_frame(
        sock,
        {
            "hello": "pipmaster-airgap",
            "v": PROTOCOL_VERSION,
            "nonce": server_nonce.hex(),
        },
    )
    try:
        msg = recv_frame(sock)
        client_nonce = bytes.fromhex(msg["nonce"])
        mac = bytes.fromhex(msg["mac"])
    except (KeyError, ValueError, TypeError, ProtocolError):
        return False
    if len(client_nonce) != 32 or not hmac.compare_digest(
        mac, _mac(key, b"C", server_nonce, client_nonce)
    ):
        send_frame(sock, {"ok": False, "error": "authentication failed"})
        return False
    send_frame(
        sock, {"ok": True, "mac": _mac(key, b"S", client_nonce, server_nonce).hex()}
    )
    return True


def client_auth(sock: Any, key: bytes) -> None:
    try:
        hello = recv_frame(sock)
        if (
            hello.get("hello") != "pipmaster-airgap"
            or hello.get("v") != PROTOCOL_VERSION
        ):
            raise ProtocolError("unexpected relay greeting")
        server_nonce = bytes.fromhex(hello["nonce"])
        client_nonce = secrets.token_bytes(32)
        send_frame(
            sock,
            {
                "nonce": client_nonce.hex(),
                "mac": _mac(key, b"C", server_nonce, client_nonce).hex(),
            },
        )
        reply = recv_frame(sock)
        if not reply.get("ok"):
            raise AuthError("relay rejected our credentials")
        proof = bytes.fromhex(reply["mac"])
    except (KeyError, ValueError, TypeError) as exc:
        raise ProtocolError("malformed handshake") from exc
    if not hmac.compare_digest(proof, _mac(key, b"S", client_nonce, server_nonce)):
        raise AuthError("relay failed to prove knowledge of the shared secret")


# -------------------------------------------------------------------------- profile
def collect_profile() -> dict[str, Any]:
    """Describe THIS interpreter so the relay can fetch wheels that fit it."""
    from packaging import markers, tags

    platforms: list = []
    abis: list = []
    for tag in tags.sys_tags():
        if tag.platform not in platforms:
            platforms.append(tag.platform)
        if tag.abi not in abis:
            abis.append(tag.abi)
    return {
        "os": platform.system(),
        "machine": platform.machine(),
        "python": [sys.version_info[0], sys.version_info[1]],
        "implementation": tags.interpreter_name(),
        "platforms": platforms,
        "abis": abis,
        "env": dict(markers.default_environment()),
    }


def validate_profile(raw: Any) -> dict[str, Any]:
    """Relay side: never trust the profile, it ends up on a pip command line."""
    try:
        major, minor = int(raw["python"][0]), int(raw["python"][1])
        impl = str(raw["implementation"])
        platforms = [str(x) for x in raw["platforms"]]
        abis = [str(x) for x in raw["abis"]]
        env = {str(k): str(v)[:200] for k, v in raw["env"].items() if k in _ENV_KEYS}
    except (KeyError, TypeError, ValueError, AttributeError, IndexError) as exc:
        raise ProtocolError("invalid target profile") from exc
    if not (2 <= major <= 9 and 0 <= minor <= 99):
        raise ProtocolError("invalid python version")
    if not (
        _TAG_RE.match(impl)
        and 1 <= len(platforms) <= 300
        and 1 <= len(abis) <= 60
        and all(_TAG_RE.match(t) for t in platforms + abis)
    ):
        raise ProtocolError("invalid platform or ABI tags")
    return {
        "python": [major, minor],
        "implementation": impl,
        "platforms": platforms,
        "abis": abis,
        "env": env,
    }