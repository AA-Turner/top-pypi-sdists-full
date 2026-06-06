"""MDM enrollment-key exchange shared by ``runlayer credentials enroll`` and the hook lazy fallback."""

from __future__ import annotations

import getpass
import os
import socket
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple

import httpx

from runlayer_cli.api import USER_AGENT
from runlayer_cli.config import load_config, normalize_url, url_to_host_key
from runlayer_cli.mdm_config import read_managed_config
from runlayer_cli.tls import http_client

ENROLLMENT_ENDPOINT_PATH = "/api/v1/mdm/enroll"
ENROLLMENT_TIMEOUT_SECONDS = 60.0

# Marker file dropped on successful enrollment so the root/SYSTEM bootstrap gate
# can prove the console user enrolled without reading the per-user keychain.
# See ``hook_install.console_user.has_enrolled_credential_for_host``.
ENROLLMENT_MARKER_PREFIX = ".enrolled-"
_RUNLAYER_DIR_NAME = ".runlayer"

HOST_ENV_VAR = "RUNLAYER_HOST"
ENROLLMENT_KEY_ENV_VAR = "RUNLAYER_ENROLLMENT_API_KEY"

_USERNAME_ENV_VARS: tuple[str, ...] = (
    "ENROLLMENT_USERNAME",
    "RUNLAYER_ENROLLMENT_USERNAME",
)
_DEVICE_NAME_ENV_VARS: tuple[str, ...] = (
    "ENROLLMENT_DEVICE_NAME",
    "RUNLAYER_ENROLLMENT_DEVICE_NAME",
)


def resolve_host(explicit: str | None) -> str | None:
    """Host: explicit → ``RUNLAYER_HOST`` env → config ``default_host`` → MDM ``Host``."""
    if explicit:
        return normalize_url(explicit)
    env_host = os.environ.get(HOST_ENV_VAR)
    if env_host:
        return normalize_url(env_host)
    config = load_config()
    if config.default_host:
        return normalize_url(config.default_host)
    managed_host = read_managed_config().get("host")
    if managed_host:
        return normalize_url(managed_host)
    return None


def resolve_enrollment_key(explicit: str | None = None) -> str | None:
    """Enrollment key: explicit → ``RUNLAYER_ENROLLMENT_API_KEY`` env → MDM ``EnrollmentKey``."""
    if explicit:
        return explicit
    env_key = os.environ.get(ENROLLMENT_KEY_ENV_VAR)
    if env_key:
        return env_key
    return read_managed_config().get("enrollment_key")


def resolve_mdm_username(explicit: str | None = None) -> str | None:
    """MDM-side username override; OS fallback is applied later in ``resolve_enrollment_identity``."""
    return _resolve_mdm_field(explicit, _USERNAME_ENV_VARS, "username")


def resolve_mdm_device_name(explicit: str | None = None) -> str | None:
    """MDM-side device-name override; OS fallback is applied later in ``resolve_enrollment_identity``."""
    return _resolve_mdm_field(explicit, _DEVICE_NAME_ENV_VARS, "device_name")


def _resolve_mdm_field(
    explicit: str | None, env_vars: tuple[str, ...], mdm_key: str
) -> str | None:
    if explicit:
        return explicit
    for var in env_vars:
        env_value = os.environ.get(var)
        if env_value:
            return env_value
    return read_managed_config().get(mdm_key)


class EnrollmentError(Exception):
    """Raised when /api/v1/mdm/enroll fails. ``status_code`` is None for transport errors."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class EnrollmentResult(NamedTuple):
    """``exchange_enrollment_key`` return value.

    ``username`` / ``device_name`` are the values actually sent to the server
    (after env/OS fallback). Surfaced so callers like the lazy-enrollment
    fallback can echo them into observability events without re-resolving.
    """

    api_key: str
    username: str
    device_name: str


def resolve_enrollment_identity(
    username: str | None,
    device_name: str | None,
) -> tuple[str, str]:
    """Return ``(username, device_name)`` for ``MDMEnrollRequest``.

    Order: explicit/MDM input → ``ENROLLMENT_*`` env (and ``RUNLAYER_ENROLLMENT_*``
    aliases) → ``getpass.getuser()`` / ``socket.gethostname()``. Backend's
    ``MDMEnrollRequest`` requires both fields (test_enroll_missing_username → 422),
    so callers must never POST ``{}``. Returns empty strings only when every source
    failed; backend will then reject with 422 — surface that error rather than
    silently masking the misconfig.
    """
    return _resolve_field(username, _USERNAME_ENV_VARS, _os_username), _resolve_field(
        device_name, _DEVICE_NAME_ENV_VARS, _os_device_name
    )


def _resolve_field(
    value: str | None,
    env_vars: tuple[str, ...],
    os_default: Callable[[], str | None],
) -> str:
    if value:
        return value
    for env_var in env_vars:
        env_value = os.environ.get(env_var)
        if env_value:
            return env_value
    return os_default() or ""


def _os_username() -> str | None:
    try:
        return getpass.getuser() or None
    except Exception:
        return None


def _os_device_name() -> str | None:
    try:
        return socket.gethostname() or None
    except Exception:
        return None


def enrollment_marker_path(host: str, home: Path | None = None) -> Path:
    """Path to the per-host enrollment marker for *host* under *home* (defaults to ``Path.home()``).

    The marker is a 644 empty file at ``<home>/.runlayer/.enrolled-<host_key>``;
    presence proves the console user has enrolled. mtime carries the enrollment
    timestamp; no contents to parse.
    """
    base = home if home is not None else Path.home()
    return (
        base / _RUNLAYER_DIR_NAME / f"{ENROLLMENT_MARKER_PREFIX}{url_to_host_key(host)}"
    )


def write_enrollment_marker(host: str) -> None:
    """Best-effort touch of the per-host enrollment marker; swallows ``OSError``.

    Called by every enrollment success path (``aiwatch enroll``,
    ``aiwatch bootstrap``, ``runlayer credentials enroll``, hook lazy fallback)
    so the root/SYSTEM bootstrap gate can ``stat()`` it without touching the
    keychain. Idempotent; refreshes mtime on every call.
    """
    path = enrollment_marker_path(host)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        os.utime(path, None)
    except OSError:
        pass


def exchange_enrollment_key(
    *,
    host: str,
    enrollment_key: str,
    username: str | None,
    device_name: str | None,
) -> EnrollmentResult:
    """POST /api/v1/mdm/enroll → ``EnrollmentResult``. Raises ``EnrollmentError`` on failure.

    Sole owner of identity resolution: callers pass raw (possibly ``None``)
    values; this function applies the env/OS fallback via
    ``resolve_enrollment_identity`` before POSTing. Backend's
    ``MDMEnrollRequest`` requires both fields.
    """
    endpoint = f"{host.rstrip('/')}{ENROLLMENT_ENDPOINT_PATH}"
    resolved_username, resolved_device = resolve_enrollment_identity(
        username, device_name
    )
    body: dict[str, str] = {
        "username": resolved_username,
        "device_name": resolved_device,
    }

    try:
        with http_client(timeout=ENROLLMENT_TIMEOUT_SECONDS) as client:
            response = client.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {enrollment_key}",
                    "Content-Type": "application/json",
                    "User-Agent": USER_AGENT,
                },
                json=body,
            )
    except httpx.RequestError as exc:
        raise EnrollmentError(f"Failed to connect to {endpoint}: {exc}") from exc

    if response.status_code != 200:
        detail = ""
        try:
            payload = response.json()
            if isinstance(payload, dict):
                detail = str(payload.get("detail") or "")
        except (ValueError, TypeError):
            pass
        msg = f"enrollment failed (HTTP {response.status_code})"
        if detail:
            msg += f": {detail}"
        raise EnrollmentError(msg, status_code=response.status_code)

    try:
        api_key = response.json()["api_key"]
    except (KeyError, TypeError, ValueError) as exc:
        raise EnrollmentError(
            "enrollment response did not contain api_key",
            status_code=response.status_code,
        ) from exc

    if not isinstance(api_key, str) or not api_key:
        raise EnrollmentError(
            "enrollment response api_key is empty",
            status_code=response.status_code,
        )

    return EnrollmentResult(
        api_key=api_key,
        username=resolved_username,
        device_name=resolved_device,
    )
