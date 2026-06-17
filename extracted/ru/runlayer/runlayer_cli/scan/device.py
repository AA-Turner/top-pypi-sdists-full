"""Device identification utilities for MCP Watch."""

from __future__ import annotations

import os
import platform
import socket
import subprocess
import sys
import uuid
from pathlib import Path
from typing import TypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired

import structlog

from runlayer_cli.paths import get_runlayer_dir

if sys.platform == "win32":
    import winreg
else:
    winreg = None  # type: ignore[assignment]

logger = structlog.get_logger(__name__)

DEVICE_ID_FILE = "device_id"

# Stable namespace for deriving a device UUID from a raw hardware identifier.
# Keeps the wire format a 36-char UUID and avoids transmitting the raw serial.
DEVICE_ID_NAMESPACE = uuid.uuid5(uuid.NAMESPACE_DNS, "device-id.aiwatch.runlayer.com")

SYSTEM_USERNAMES = {"root", "_mbsetupuser", "loginwindow"}


def _get_device_id_path() -> Path:
    """Get the path to the device ID file."""
    return get_runlayer_dir() / DEVICE_ID_FILE


def _get_macos_hardware_id() -> str | None:
    """Read the stable IOPlatformUUID on macOS via ioreg."""
    try:
        result = subprocess.run(
            ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    for line in result.stdout.splitlines():
        if "IOPlatformUUID" in line:
            # Line looks like:  "IOPlatformUUID" = "ABCDEF12-...-1234567890"
            _, _, value = line.partition("=")
            value = value.strip().strip('"').strip()
            if value:
                return value
    return None


def _get_windows_hardware_id() -> str | None:
    """Read the stable MachineGuid from the Windows registry."""
    if winreg is None:
        return None
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            R"SOFTWARE\Microsoft\Cryptography",
            0,
            winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
        ) as key:
            value, _ = winreg.QueryValueEx(key, "MachineGuid")
    except OSError:
        return None
    value = str(value).strip()
    return value or None


def _get_linux_hardware_id() -> str | None:
    """Read the systemd / D-Bus machine-id on Linux."""
    for path in (Path("/etc/machine-id"), Path("/var/lib/dbus/machine-id")):
        try:
            value = path.read_text().strip()
        except OSError:
            continue
        if value:
            return value
    return None


def _get_hardware_machine_id() -> str | None:
    """Resolve a stable per-machine hardware identifier as a UUID string.

    Derives a deterministic UUID from the platform's hardware machine id
    (macOS IOPlatformUUID, Windows MachineGuid, Linux machine-id), or returns
    None when none is available. The raw id is wrapped in a uuid5 so the wire
    value is a stable 36-char UUID and the raw serial never leaves the device.
    """
    system = platform.system().lower()
    if system == "darwin":
        raw = _get_macos_hardware_id()
    elif system == "windows":
        raw = _get_windows_hardware_id()
    elif system == "linux":
        raw = _get_linux_hardware_id()
    else:
        raw = None

    if not raw:
        return None
    return str(uuid.uuid5(DEVICE_ID_NAMESPACE, raw))


def get_or_create_device_id() -> str:
    """
    Get or create a stable device identifier.

    Priority:
    1. Environment variable RUNLAYER_DEVICE_ID
    2. Hardware machine id (stable per physical device, shared across users)
    3. Stored device ID in ~/.runlayer/device_id
    4. Generate and store a new UUID

    Returns:
        Stable device identifier string
    """
    # 1. Explicit override (env var / --device-id flag).
    env_device_id = os.environ.get("RUNLAYER_DEVICE_ID")
    if env_device_id:
        logger.debug(
            "Using device ID from environment", device_id_prefix=env_device_id[:8]
        )
        return env_device_id

    # 2. Hardware machine id. Preferred over the stored file so every user on a
    # shared machine — and re-runs after a failed file write — map to one
    # physical device instead of minting a new device_id each time (which
    # inflated the per-config device count on the MDM cards).
    hardware_id = _get_hardware_machine_id()
    if hardware_id:
        logger.debug("Using hardware device ID", device_id_prefix=hardware_id[:8])
        return hardware_id

    # 3. Stored device ID (fallback for hosts without a readable hardware id).
    device_id_path = _get_device_id_path()
    if device_id_path.exists():
        try:
            device_id = device_id_path.read_text().strip()
            if device_id:
                logger.debug("Using stored device ID", device_id_prefix=device_id[:8])
                return device_id
        except IOError:
            pass

    # 4. Generate new device ID.
    device_id = str(uuid.uuid4())
    logger.info("Generated new device ID", device_id_prefix=device_id[:8])

    # Store for future use.
    try:
        device_id_path.parent.mkdir(parents=True, exist_ok=True)
        device_id_path.write_text(device_id)
    except IOError as e:
        logger.warning("Failed to store device ID", error=str(e))

    return device_id


class DeviceMetadata(TypedDict):
    hostname: str | None
    os: str | None
    os_version: str | None
    username: str | None
    is_wsl: NotRequired[bool]


def get_device_metadata() -> DeviceMetadata:
    """Collect device metadata for the scan payload."""
    system = platform.system().lower()
    os_name = {
        "darwin": "darwin",
        "windows": "windows",
        "linux": "linux",
    }.get(system, system)

    hostname = None
    try:
        hostname = socket.gethostname()
    except Exception:
        pass

    username = None
    try:
        username = os.getlogin()
    except Exception:
        username = os.environ.get("USER") or os.environ.get("USERNAME")

    if (not username or username in SYSTEM_USERNAMES) and system == "darwin":
        username = _get_macos_console_user() or username

    metadata = DeviceMetadata(
        hostname=hostname,
        os=os_name,
        os_version=platform.release(),
        username=username,
    )

    if system == "linux" and detect_wsl():
        metadata["is_wsl"] = True

    return metadata


def detect_wsl() -> bool:
    """Detect whether the current environment is Windows Subsystem for Linux."""
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        content = Path("/proc/version").read_text()
        if "microsoft" in content.lower():
            return True
    except OSError:
        pass
    return False


def list_wsl_distros() -> list[str]:
    """List installed WSL distributions (Windows host only).

    Runs ``wsl.exe --list --quiet``; output is UTF-16LE with NUL bytes and may
    include a BOM. Returns an empty list on any failure or timeout.
    """
    try:
        result = subprocess.run(
            ["wsl.exe", "--list", "--quiet"],
            capture_output=True,
            timeout=10,
        )
    except Exception:
        return []

    if result.returncode != 0:
        return []

    try:
        text = result.stdout.decode("utf-16-le")
    except (UnicodeDecodeError, AttributeError):
        text = result.stdout.decode("utf-8", errors="ignore")

    distros: list[str] = []
    for raw in text.replace("\x00", "").splitlines():
        name = raw.strip().lstrip("\ufeff").strip()
        if name and name.lower() != "docker-desktop-data":
            distros.append(name)
    return distros


def get_wsl_user_homes(distro: str) -> list[Path]:
    """Resolve Linux user home directories inside a WSL distro from Windows.

    Lists ``\\\\wsl.localhost\\<distro>\\home\\*`` (falls back to the older
    ``\\\\wsl$\\<distro>\\home``). Returns each user home dir; tolerates a
    missing/unreachable UNC root.
    """
    homes: list[Path] = []
    for unc_root in (Rf"\\wsl.localhost\{distro}", Rf"\\wsl$\{distro}"):
        home_base = Path(unc_root) / "home"
        try:
            if not home_base.is_dir():
                continue
            for entry in sorted(home_base.iterdir()):
                if entry.is_dir():
                    homes.append(entry)
        except OSError:
            continue
        if homes:
            break
    return homes


def _get_macos_console_user() -> str | None:
    """Get the logged-in console user on macOS via stat /dev/console."""
    try:
        result = subprocess.run(
            ["stat", "-f", "%Su", "/dev/console"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        user = result.stdout.strip()
        if user and user not in SYSTEM_USERNAMES:
            return user
    except Exception:
        pass
    return None
