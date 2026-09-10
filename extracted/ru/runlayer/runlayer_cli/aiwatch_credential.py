"""Exchange the on-disk LLM routing credential for a short-lived gateway token.

Claude Code (``apiKeyHelper``) and Codex (``auth.command``) invoke it on start,
every four minutes, and after a 401. The helper caches the minted token in a
private file next to the credential and re-mints only when less than one client
refresh interval remains, so both clients share one live token per device
instead of about eight. The frozen ``aiwatch`` import closure must stay
stdlib-only plus ``runlayer_cli.mdm_config`` and ``runlayer_cli.__version__``.
"""

from __future__ import annotations

import contextlib
import errno
import hashlib
import http.client
import ipaddress
import json
import math
import os
import socket
import stat
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable, TypedDict, TypeGuard
from urllib.parse import urlsplit

from runlayer_cli import __version__
from runlayer_cli.mdm_config import read_managed_config

CREDENTIAL_SUBCOMMAND = "credential"
HELPER_CLIENTS = ("claude", "codex")
CREDENTIAL_RELATIVE_PATH = Path(".runlayer") / "aiwatch" / "llm-routing-credential"
DEVICE_TOKENS_PATH = "/api/v1/llm-gateway/device-tokens"
HELPER_TIMEOUT_SECONDS = 5.0
_MAX_RESPONSE_BYTES = 64 * 1024
# One token, bare or in a small JSON envelope; anything larger is not a file this tool wrote.
MAX_CREDENTIAL_BYTES = 4096
# Both routing writers configure the clients to call this helper on this cadence
# (Claude Code apiKeyHelper TTL, Codex auth refresh_interval_ms); the cache must
# hand out a token that outlives one full interval.
CLIENT_REFRESH_INTERVAL_SECONDS = 240
TOKEN_CACHE_FILENAME = "llm-routing-token"
_CREDENTIAL_OPEN_FLAGS = (
    os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
)
_RETRY_MIN_REMAINING_SECONDS = 0.5
_MIN_BUDGET_SECONDS = 0.1
HOST_ENV_VAR = "RUNLAYER_HOST"


class CredentialHelperError(Exception):
    """One-line, credential-free failure reason for stderr."""


class DeviceToken(TypedDict):
    token: str
    expires_in_seconds: float


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Following a redirect would re-send the bearer credential to another origin."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        return None


_OPENER = urllib.request.build_opener(_NoRedirect())


def credential_path(home: Path) -> Path:
    return home / CREDENTIAL_RELATIVE_PATH


def token_cache_path(credential: Path) -> Path:
    return credential.with_name(TOKEN_CACHE_FILENAME)


def is_single_token(value: str) -> bool:
    """One non-empty token without whitespace: the shape of a credential or token."""
    return bool(value) and not any(character.isspace() for character in value)


def _is_finite_number(value: object) -> TypeGuard[float]:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def _read_bounded(fd: int, limit: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while total <= limit:
        chunk = os.read(fd, limit + 1 - total)
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
    return b"".join(chunks)


def _read_private_file(
    path: Path,
    *,
    limit: int,
    label: str,
) -> bytes | None:
    """Read a bounded regular file without following symlinks.

    Returns None when absent. A pre-check gives a useful error while
    ``O_NOFOLLOW`` also refuses a symlink swapped in before the open.
    """
    if path.is_symlink():
        raise CredentialHelperError(f"{label} is a symlink: {path}")
    try:
        fd = os.open(path, _CREDENTIAL_OPEN_FLAGS)
    except FileNotFoundError:
        return None
    except OSError as exc:
        if exc.errno in (errno.ELOOP, errno.EMLINK):
            raise CredentialHelperError(f"{label} is a symlink: {path}") from exc
        raise CredentialHelperError(f"cannot read {label} at {path}") from exc
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise CredentialHelperError(f"{label} is not a regular file: {path}")
        data = _read_bounded(fd, limit)
    except OSError as exc:
        raise CredentialHelperError(f"cannot read {label} at {path}") from exc
    finally:
        os.close(fd)
    return data


def read_credential(path: Path) -> str | None:
    """Return the exchange credential, or None when absent, empty, or malformed.

    Opens with ``O_NOFOLLOW`` so a symlink swapped in after any pre-check is
    still refused, and reads at most ``MAX_CREDENTIAL_BYTES`` + 1.
    """
    data = _read_private_file(
        path,
        limit=MAX_CREDENTIAL_BYTES,
        label="LLM routing credential",
    )
    if data is None:
        return None
    if len(data) > MAX_CREDENTIAL_BYTES:
        return None
    try:
        content = data.decode("utf-8")
    except UnicodeDecodeError:
        return None

    credential = content.strip()
    return credential if is_single_token(credential) else None


def _credential_fingerprint(credential: str) -> str:
    return hashlib.sha256(credential.encode()).hexdigest()


def read_token_cache(path: Path, *, now: float, credential: str) -> str | None:
    """Cached token minted by *credential* with more than one refresh interval left, else None.

    The fingerprint binds the cache to the credential that minted it: a helper
    that read the old credential must not publish its token after a rotation.
    """
    try:
        data = _read_private_file(
            path,
            limit=MAX_CREDENTIAL_BYTES,
            label="LLM routing token cache",
        )
    except CredentialHelperError:
        return None
    if data is None:
        return None
    if len(data) > MAX_CREDENTIAL_BYTES:
        return None
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if not isinstance(payload, dict):
        return None

    token = payload.get("token")
    expires_at = payload.get("expires_at")
    if payload.get("credential_sha256") != _credential_fingerprint(credential):
        return None
    valid_expiry = (
        _is_finite_number(expires_at)
        and expires_at - now > CLIENT_REFRESH_INTERVAL_SECONDS
    )
    if not isinstance(token, str) or not is_single_token(token) or not valid_expiry:
        return None
    return token


def write_token_cache(
    path: Path, token: str, expires_at: float, *, credential: str
) -> None:
    payload = (
        json.dumps(
            {
                "token": token,
                "expires_at": int(expires_at),
                "credential_sha256": _credential_fingerprint(credential),
            }
        )
        + "\n"
    ).encode("utf-8")
    fd, temporary_path = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{TOKEN_CACHE_FILENAME}.",
        suffix=".tmp",
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
        # Replacing the path replaces an existing symlink instead of writing through it.
        os.replace(temporary_path, path)
    except OSError:
        with contextlib.suppress(OSError):
            os.unlink(temporary_path)
        raise


def _is_loopback_host(hostname: str) -> bool:
    if hostname.rstrip(".").lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(hostname).is_loopback
    except ValueError:
        return False


def resolve_exchange_host() -> str | None:
    """Resolve managed Host first, then ``RUNLAYER_HOST``, with HTTPS default.

    The exchange carries the durable device credential as a bearer, so a
    non-loopback ``http://`` host is refused (same rule as the routing
    writers' gateway URL check) instead of sending it in cleartext.
    """
    managed_host = read_managed_config().get("host")
    host = managed_host if isinstance(managed_host, str) else None
    if not host or not host.strip():
        host = os.environ.get(HOST_ENV_VAR)
    if not host:
        return None
    normalized = host.strip().rstrip("/")
    if not normalized:
        return None
    if "://" not in normalized:
        normalized = f"https://{normalized}"
    parsed = urlsplit(normalized)
    scheme = parsed.scheme.lower()
    hostname = parsed.hostname or ""
    if scheme == "http" and _is_loopback_host(hostname):
        return normalized
    if scheme != "https":
        raise CredentialHelperError("exchange host must use https")
    return normalized


def _http_error_message(
    error: urllib.error.HTTPError,
    credential: str,
) -> str:
    message = f"device token exchange failed: HTTP {error.code}"
    try:
        body = error.read(_MAX_RESPONSE_BYTES + 1)
        payload = json.loads(body)
    except (OSError, ValueError, TypeError):
        return message
    if len(body) > _MAX_RESPONSE_BYTES:
        return message
    if isinstance(payload, dict):
        detail = payload.get("detail")
        if isinstance(detail, str):
            collapsed = detail.replace("\r", " ").replace("\n", " ")
            if credential:
                collapsed = collapsed.replace(credential, "[redacted]")
            collapsed = collapsed[:200]
            message = f"{message} ({collapsed})"
    return message


def _device_token_from_body(body: bytes) -> DeviceToken:
    try:
        payload = json.loads(body)
    except (ValueError, TypeError) as exc:
        raise CredentialHelperError(
            "device token exchange returned an invalid token"
        ) from exc
    token = payload.get("token") if isinstance(payload, dict) else None
    expires_in_seconds = (
        payload.get("expires_in_seconds") if isinstance(payload, dict) else None
    )
    if not isinstance(token, str) or not is_single_token(token):
        raise CredentialHelperError("device token exchange returned an invalid token")
    if not _is_finite_number(expires_in_seconds) or expires_in_seconds <= 0:
        raise CredentialHelperError("device token exchange returned an invalid token")
    return {
        "token": token,
        "expires_in_seconds": float(expires_in_seconds),
    }


def request_device_token(
    host: str,
    credential: str,
    *,
    budget: float = HELPER_TIMEOUT_SECONDS,
    urlopen: Callable[..., Any] = _OPENER.open,
    monotonic: Callable[[], float] = time.monotonic,
) -> DeviceToken:
    """POST the credential exchange within *budget* seconds and return its token."""
    try:
        request = urllib.request.Request(
            host + DEVICE_TOKENS_PATH,
            data=b"{}",
            headers={
                "Authorization": f"Bearer {credential}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": f"runlayer-aiwatch/{__version__}",
            },
            method="POST",
        )
    except ValueError as exc:
        raise CredentialHelperError("device token exchange failed") from exc

    deadline = monotonic() + max(_MIN_BUDGET_SECONDS, budget)
    transport_errors = (
        urllib.error.URLError,
        socket.timeout,
        TimeoutError,
        OSError,
        http.client.HTTPException,
    )
    for attempt in range(2):
        timeout = max(0.1, deadline - monotonic())
        try:
            with urlopen(request, timeout=timeout) as response:
                body = response.read(_MAX_RESPONSE_BYTES + 1)
        except urllib.error.HTTPError as exc:
            raise CredentialHelperError(_http_error_message(exc, credential)) from exc
        except transport_errors as exc:
            remaining = deadline - monotonic()
            if attempt == 1 or remaining <= _RETRY_MIN_REMAINING_SECONDS:
                raise CredentialHelperError("device token exchange failed") from exc
            continue
        if len(body) > _MAX_RESPONSE_BYTES:
            raise CredentialHelperError(
                "device token exchange returned an oversized response"
            )
        return _device_token_from_body(body)
    raise CredentialHelperError("device token exchange failed")


def main(
    argv: list[str],
    *,
    prepare: Callable[[], None] | None = None,
    started_at: float | None = None,
    clock: Callable[[], float] = time.time,
) -> int:
    """Run ``aiwatch credential <claude|codex>``.

    ``prepare`` runs inside the failure handling (the entrypoint passes its
    truststore injection) so every failure stays one stderr line. ``started_at``
    (epoch seconds) anchors the budget at process start: Codex kills the helper
    ``timeout_ms`` after exec, so interpreter startup, truststore injection and
    config reads all count against the same five seconds.
    """
    if len(argv) != 1 or argv[0] not in HELPER_CLIENTS:
        sys.stderr.write(
            "aiwatch credential: usage: aiwatch credential <claude|codex>\n"
        )
        return 1

    client = argv[0]
    try:
        now = clock()
        if prepare is not None:
            prepare()
        path = credential_path(Path.home())
        credential = read_credential(path)
        if credential is None:
            raise CredentialHelperError(f"no LLM routing credential at {path}")
        cache = token_cache_path(path)
        cached = read_token_cache(cache, now=now, credential=credential)
        if cached is not None:
            token = cached
        else:
            host = resolve_exchange_host()
            if host is None:
                raise CredentialHelperError("no Runlayer host configured")
            budget = HELPER_TIMEOUT_SECONDS
            if started_at is not None:
                # Re-read the clock: prepare() and the file reads above count
                # against the same window the client kills the helper after.
                budget -= max(0.0, clock() - started_at)
            minted = request_device_token(host, credential, budget=budget)
            token = minted["token"]
            try:
                # Helper start precedes server issue time, keeping local expiry lower.
                write_token_cache(
                    cache,
                    minted["token"],
                    now + minted["expires_in_seconds"],
                    credential=credential,
                )
            except OSError as exc:
                sys.stderr.write(
                    f"aiwatch credential {client}: cannot write LLM routing "
                    f"token cache at {cache} ({type(exc).__name__})\n"
                )
    except CredentialHelperError as exc:
        sys.stderr.write(f"aiwatch credential {client}: {exc}\n")
        return 1
    except Exception as exc:
        sys.stderr.write(
            f"aiwatch credential {client}: credential helper failed "
            f"({type(exc).__name__})\n"
        )
        return 1

    sys.stdout.write(token)
    sys.stdout.flush()
    return 0
