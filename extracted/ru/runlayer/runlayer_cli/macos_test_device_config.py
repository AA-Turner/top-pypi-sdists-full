"""Local configuration for package-only Test Device installs."""

from __future__ import annotations

import json
import os
import platform
import plistlib
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import TypedDict, cast
from urllib.parse import urlsplit

from runlayer_cli.config import normalize_url
from runlayer_cli.mdm_config import (
    BACKEND_SYNC_OWNED_KEYS,
    CLI_PREF_DOMAIN,
    HOST_KEY,
    ORG_API_KEY_KEY,
    PREF_DOMAIN,
)

AIWATCH_LOCAL_CONFIG_PATH = Path("/Library/Preferences") / f"{PREF_DOMAIN}.plist"
CLI_LOCAL_CONFIG_PATH = Path("/Library/Preferences") / f"{CLI_PREF_DOMAIN}.plist"
LINUX_CONFIG_PATH = Path("/etc/runlayer/aiwatch/config.json")
LINUX_CREDENTIALS_PATH = Path("/etc/runlayer/aiwatch/credentials")
CLI_SCHEDULE_LABEL = "com.runlayer.cli.schedule"
LOCAL_CONFIG_FLUSH_TIMEOUT_SECONDS = 5.0
LOCAL_CONFIG_FLUSH_POLL_SECONDS = 0.05


class TestDeviceConfigError(RuntimeError):
    """A local Test Device configuration could not be written."""


class TestDeviceConfigResult(TypedDict):
    """Outcome from publishing local Test Device configuration."""

    host: str
    flushed: bool


def configure_aiwatch_test_device(
    host: str,
    org_api_key: str,
    *,
    path: Path = AIWATCH_LOCAL_CONFIG_PATH,
) -> TestDeviceConfigResult:
    """Write AI Watch credentials at lower precedence than Managed Preferences."""
    return _write_local_config(path, host=host, org_api_key=org_api_key)


def configure_cli_test_device(
    host: str,
    org_api_key: str,
    *,
    path: Path | None = None,
    credentials_path: Path | None = None,
) -> TestDeviceConfigResult:
    """Write package-local full-CLI credentials for the current platform."""
    system = platform.system()
    if system == "Darwin":
        return _write_local_config(
            path or CLI_LOCAL_CONFIG_PATH,
            host=host,
            org_api_key=org_api_key,
        )
    if system == "Linux":
        return _write_linux_config(
            path or LINUX_CONFIG_PATH,
            credentials_path=credentials_path or LINUX_CREDENTIALS_PATH,
            host=host,
            org_api_key=org_api_key,
        )
    raise TestDeviceConfigError(
        "package Test Device configuration is supported only on macOS and Linux"
    )


def kickstart_cli_schedule() -> bool:
    """Run the packaged CLI scheduler now for the current console user."""
    uid_result = subprocess.run(
        ["/usr/bin/stat", "-f", "%u", "/dev/console"],
        check=False,
        capture_output=True,
        text=True,
    )
    uid = uid_result.stdout.strip()
    if uid_result.returncode != 0 or not uid.isdigit() or uid == "0":
        return False

    result = subprocess.run(
        [
            "/bin/launchctl",
            "kickstart",
            "-k",
            f"gui/{uid}/{CLI_SCHEDULE_LABEL}",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def _write_local_config(
    path: Path,
    *,
    host: str,
    org_api_key: str,
) -> TestDeviceConfigResult:
    _require_macos_root()
    normalized_host = _validate_host(host)
    _validate_org_api_key(org_api_key)

    payload = _read_local_config(path)
    for policy_key in BACKEND_SYNC_OWNED_KEYS:
        payload.pop(policy_key, None)
    payload[HOST_KEY] = normalized_host
    payload[ORG_API_KEY_KEY] = org_api_key
    content = plistlib.dumps(payload, fmt=plistlib.FMT_XML, sort_keys=True)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        # cfprefsd may flush the backing plist later; root import supplies its metadata.
        subprocess.run(
            [
                "/usr/bin/defaults",
                "import",
                str(path.with_suffix("")),
                "-",
            ],
            input=content,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise TestDeviceConfigError(
            f"could not publish local preferences through cfprefsd: {path}"
        ) from exc
    flushed = _wait_for_local_config_flush(path, expected=payload)
    if not flushed:
        print(
            f"Warning: local preferences are still flushing to {path}; continuing.",
            file=sys.stderr,
        )

    return {"host": normalized_host, "flushed": flushed}


def _write_linux_config(
    path: Path,
    *,
    credentials_path: Path,
    host: str,
    org_api_key: str,
) -> TestDeviceConfigResult:
    _require_root()
    normalized_host = _validate_host(host)
    _validate_org_api_key(org_api_key)

    payload = _read_linux_config(path)
    for policy_key in BACKEND_SYNC_OWNED_KEYS:
        payload.pop(policy_key, None)
    payload.pop(ORG_API_KEY_KEY, None)
    payload[HOST_KEY] = normalized_host

    try:
        _atomic_write_text(
            path,
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            mode=0o644,
        )
        _atomic_write_text(
            credentials_path,
            f"RUNLAYER_API_KEY={shlex.quote(org_api_key)}\n",
            mode=0o600,
        )
    except OSError as exc:
        raise TestDeviceConfigError(
            "could not publish Linux Test Device configuration"
        ) from exc

    return {"host": normalized_host, "flushed": True}


def _read_linux_config(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, UnicodeError, ValueError) as exc:
        raise TestDeviceConfigError(
            f"existing Linux configuration is unreadable: {path}"
        ) from exc
    if not isinstance(payload, dict):
        raise TestDeviceConfigError(
            f"existing Linux configuration is not a dictionary: {path}"
        )
    return cast(dict[str, object], payload)


def _atomic_write_text(path: Path, content: str, *, mode: int) -> None:
    _ensure_public_directory(path.parent)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as temp_file:
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())
        os.chmod(temp_path, mode)
        os.replace(temp_path, path)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def _ensure_public_directory(directory: Path) -> None:
    missing: list[Path] = []
    candidate = directory
    while not candidate.exists():
        missing.append(candidate)
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent

    for candidate in reversed(missing):
        candidate.mkdir(exist_ok=True)
        os.chmod(candidate, 0o755)
    os.chmod(directory, 0o755)


def _wait_for_local_config_flush(
    path: Path,
    *,
    expected: dict[str, object],
) -> bool:
    # Immediate reconcile reads this plist from disk (read_managed_config), so
    # require the full imported payload — matching credentials alone would let
    # a stale disk copy that still carries stripped BACKEND_SYNC_OWNED_KEYS
    # (e.g. Sessions) pass and defer policy cleanup to the hourly bootstrap.
    deadline = time.monotonic() + LOCAL_CONFIG_FLUSH_TIMEOUT_SECONDS
    while True:
        try:
            with path.open("rb") as file:
                existing = plistlib.load(file)
        except (OSError, plistlib.InvalidFileException):
            existing = None
        if existing == expected:
            return True

        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return False
        time.sleep(min(LOCAL_CONFIG_FLUSH_POLL_SECONDS, remaining))


def _read_local_config(path: Path) -> dict[str, object]:
    try:
        result = subprocess.run(
            [
                "/usr/bin/defaults",
                "export",
                str(path.with_suffix("")),
                "-",
            ],
            check=False,
            capture_output=True,
        )
    except OSError as exc:
        raise TestDeviceConfigError(
            f"existing local preferences are unreadable: {path}"
        ) from exc

    if result.returncode != 0:
        if path.exists():
            raise TestDeviceConfigError(
                f"existing local preferences are unreadable: {path}"
            )
        return {}

    try:
        existing = plistlib.loads(result.stdout)
    except (TypeError, plistlib.InvalidFileException) as exc:
        raise TestDeviceConfigError(
            f"existing local preferences are unreadable: {path}"
        ) from exc
    if not isinstance(existing, dict):
        raise TestDeviceConfigError(
            f"existing local preferences are not a dictionary: {path}"
        )
    return existing


def _require_macos_root() -> None:
    if platform.system() != "Darwin":
        raise TestDeviceConfigError(
            "package Test Device configuration is supported only on macOS"
        )
    _require_root()


def _require_root() -> None:
    geteuid = getattr(os, "geteuid", None)
    if not callable(geteuid) or geteuid() != 0:
        raise TestDeviceConfigError(
            "package Test Device configuration requires root; rerun with sudo"
        )


def _validate_host(host: str) -> str:
    normalized_host = normalize_url(host.strip())
    parsed = urlsplit(normalized_host)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise TestDeviceConfigError("host must be an absolute HTTP(S) URL")
    return normalized_host


def _validate_org_api_key(org_api_key: str) -> None:
    if not org_api_key.startswith("rl_org_") or any(
        character.isspace() for character in org_api_key
    ):
        raise TestDeviceConfigError(
            "organization API key must be an rl_org_ key without whitespace"
        )
