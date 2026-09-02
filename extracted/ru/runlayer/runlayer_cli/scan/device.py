"""Device identification utilities for MCP Watch."""

from __future__ import annotations

import os
import platform
import socket
import subprocess
import sys
import uuid
from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import islice
from pathlib import Path
from typing import TypedDict

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired

import structlog

from runlayer_cli import __version__, regex_safe
from runlayer_cli.paths import get_runlayer_dir
from runlayer_cli.scan.wsl_limits import (
    MAX_WSL_DISTROS,
    MAX_WSL_HOMES,
    MAX_WSL_HOME_PROBES,
)

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


@lru_cache(maxsize=1)
def _read_macos_ioplatform_device() -> dict[str, str]:
    """Parse IOPlatformExpertDevice key/values from one ioreg invocation.

    The hardware id (``IOPlatformUUID``) and the raw serial
    (``IOPlatformSerialNumber``) both live in the same
    ``ioreg -rd1 -c IOPlatformExpertDevice`` output, so probe the hardware once
    and cache the parsed values (matching the memoization the device-id path
    already relies on). Returns an empty dict on any failure.
    """
    values: dict[str, str] = {}
    try:
        result = subprocess.run(
            ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return values
    if result.returncode != 0:
        return values
    for line in result.stdout.splitlines():
        # Lines look like:  "IOPlatformUUID" = "ABCDEF12-...-1234567890"
        for key in ("IOPlatformUUID", "IOPlatformSerialNumber"):
            if key in line and key not in values:
                _, _, value = line.partition("=")
                value = value.strip().strip('"').strip()
                if value:
                    values[key] = value
    return values


def _get_macos_hardware_id() -> str | None:
    """Read the stable IOPlatformUUID on macOS via ioreg."""
    return _read_macos_ioplatform_device().get("IOPlatformUUID")


def _get_macos_serial_number() -> str | None:
    """Read the raw hardware serial (IOPlatformSerialNumber) on macOS via ioreg."""
    return _read_macos_ioplatform_device().get("IOPlatformSerialNumber")


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


def _get_windows_serial_number() -> str | None:
    """Read the BIOS serial number on Windows via PowerShell Get-CimInstance."""
    try:
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                "(Get-CimInstance -ClassName Win32_BIOS).SerialNumber",
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def _get_linux_hardware_id() -> str | None:
    """Read the systemd / D-Bus machine-id on Linux.

    ``RUNLAYER_MACHINE_ID_PATH`` overrides the first path checked. A container
    that scans a host's user homes can bind-mount the host machine-id anywhere
    (e.g. ``/host/etc/machine-id``) and point this at it, so the device id
    matches the host without mounting over the container's own
    ``/etc/machine-id``. (``RUNLAYER_DEVICE_ID`` still overrides outright — see
    ``get_or_create_device_id``.)
    """
    paths: list[Path] = []
    override = os.environ.get("RUNLAYER_MACHINE_ID_PATH")
    if override:
        paths.append(Path(override))
    paths += [Path("/etc/machine-id"), Path("/var/lib/dbus/machine-id")]
    for path in paths:
        try:
            value = path.read_text().strip()
        except OSError:
            continue
        if value:
            return value
    return None


def _get_linux_serial_number() -> str | None:
    """Read the DMI product serial on Linux (root-readable; else None)."""
    try:
        value = Path("/sys/class/dmi/id/product_serial").read_text().strip()
    except OSError:
        return None
    return value or None


@lru_cache(maxsize=1)
def _get_hardware_machine_id() -> str | None:
    """Resolve a stable per-machine hardware identifier as a UUID string.

    Derives a deterministic UUID from the platform's hardware machine id
    (macOS IOPlatformUUID, Windows MachineGuid, Linux machine-id), or returns
    None when none is available. The raw id is wrapped in a uuid5 so the wire
    value is a stable 36-char UUID and the raw serial never leaves the device.

    Memoized (the id is stable per machine) so repeated calls from hooks and
    scans don't re-probe hardware each time, matching the ``lru_cache`` pattern
    used by ``scan/clients.py``'s ``_is_windows_with_wsl`` / ``_wsl_homes``.
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


# SMBIOS/DMI placeholder serials that VMs, whiteboxes, and half-configured OEM
# images report instead of a real serial (the Linux ``product_serial`` and
# Windows ``Win32_BIOS.SerialNumber`` sources are especially prone to these).
# The backend coalesces the first non-empty serial into a permanent value it
# joins against MDM / asset inventories, so a placeholder that sticks would
# collide across many hosts and defeat the join — drop it before the serial
# leaves the device. Compared case-insensitively with surrounding / repeated
# whitespace collapsed; kept deliberately small so an unusual-but-real serial
# is never discarded.
_SERIAL_NUMBER_PLACEHOLDERS = frozenset(
    {
        "none",
        "not applicable",
        "not specified",
        "not available",
        "default string",
        "system serial number",
        "to be filled by o.e.m.",
        "to be filled by o.e.m",
    }
)


def _reject_placeholder_serial(value: str | None) -> str | None:
    """Return the serial, or None when it's blank or a known junk placeholder."""
    if value is None:
        return None
    normalized = " ".join(value.split()).lower()
    if not normalized or normalized in _SERIAL_NUMBER_PLACEHOLDERS:
        return None
    return value


@lru_cache(maxsize=1)
def _get_serial_number() -> str | None:
    """Resolve the device's raw hardware serial number, best-effort.

    Deliberately separate from ``device_id`` (a uuid5 hash): the raw serial is
    the key MDM / asset inventories join on, so it ships as its own nullable
    field. Returns None when unreadable (non-root Linux, missing tool, VM with
    no serial, etc.) or when the platform reports a known placeholder
    (``_reject_placeholder_serial``). Memoized like ``_get_hardware_machine_id``
    — stable per machine, so hooks and scans don't re-probe hardware on every
    call.
    """
    system = platform.system().lower()
    if system == "darwin":
        raw = _get_macos_serial_number()
    elif system == "windows":
        raw = _get_windows_serial_number()
    elif system == "linux":
        raw = _get_linux_serial_number()
    else:
        raw = None
    return _reject_placeholder_serial(raw)


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
    serial_number: str | None
    is_wsl: NotRequired[bool]


class DeviceContext(TypedDict):
    """Device identity attached to AI Watch check-in / submission payloads."""

    device_id: str
    hostname: str | None
    os: str | None
    os_version: str | None
    username: str | None
    org_device_id: str | None
    serial_number: str | None


class InstalledTool(TypedDict):
    name: str
    version: str | None


def get_installed_tools() -> list[InstalledTool]:
    """Return Runlayer agent/binary versions visible to this process."""
    return [
        {
            "name": "aiwatch",
            "version": __version__,
        }
    ]


def get_device_metadata() -> DeviceMetadata:
    """Collect device metadata for the scan payload."""
    system = platform.system().lower()
    os_name = {
        "darwin": "darwin",
        "windows": "windows",
        "linux": "linux",
    }.get(system, system)

    # RUNLAYER_HOSTNAME overrides the detected hostname for device attribution.
    # A K8s DaemonSet pod's hostname is the pod name, not the node; feeding the
    # node name in via the downward API (spec.nodeName) attributes scans to the
    # node the user homes actually live on.
    hostname = os.environ.get("RUNLAYER_HOSTNAME") or None
    if not hostname:
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
        serial_number=_get_serial_number(),
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


@dataclass(frozen=True)
class DiscoveredWSLDistro:
    """One WSL distribution installed on a Windows host.

    ``wsl_version`` is None when neither command output nor registry metadata
    supplies a version.
    """

    name: str
    wsl_version: int | None
    is_running: bool
    scanned: bool = False
    container_runtimes: tuple[str, ...] = ()

    def to_api_payload(
        self,
    ) -> dict[str, str | int | bool | None | list[str]]:
        return {
            "distro_name": self.name,
            "wsl_version": self.wsl_version,
            "is_running": self.is_running,
            "scanned": self.scanned,
            "container_runtimes": list(self.container_runtimes),
        }


@dataclass(frozen=True)
class WSLDistroInventory:
    """Best-effort WSL inventory plus whether the complete command parsed."""

    distros: tuple[DiscoveredWSLDistro, ...]
    success: bool


_WSL_VERBOSE_HEADER = ("NAME", "STATE", "VERSION")
_WSL_VERBOSE_ROW = regex_safe.compile(
    r"^\s*(?:\*\s*)?(?P<name>.+?)\s+(?P<state>\S+)\s+(?P<version>\d+)\s*$"
)
_WSL_EMPTY_MARKERS = (
    "no installed distributions",
    "no distributions installed",
)
_WSL_LXSS_REGISTRY_KEY = R"Software\Microsoft\Windows\CurrentVersion\Lxss"


@dataclass(frozen=True)
class WSLRegistryMetadata:
    version: int | None


def _read_wsl_registry_metadata() -> dict[str, WSLRegistryMetadata]:
    """Read locale-independent distro metadata from the current user's Lxss key."""
    registry = winreg
    if registry is None:
        return {}
    metadata: dict[str, WSLRegistryMetadata] = {}
    try:
        with registry.OpenKey(
            registry.HKEY_CURRENT_USER,
            _WSL_LXSS_REGISTRY_KEY,
        ) as lxss_key:
            subkey_count = registry.QueryInfoKey(lxss_key)[0]
            for index in range(subkey_count):
                try:
                    subkey_name = registry.EnumKey(lxss_key, index)
                    with registry.OpenKey(lxss_key, subkey_name) as distro_key:
                        name = registry.QueryValueEx(distro_key, "DistributionName")[0]
                        try:
                            version = registry.QueryValueEx(distro_key, "Version")[0]
                        except OSError:
                            version = None
                except OSError:
                    continue
                if not isinstance(name, str) or not name.strip():
                    continue
                metadata[name.strip().casefold()] = WSLRegistryMetadata(
                    version=version
                    if isinstance(version, int) and version > 0
                    else None,
                )
    except OSError:
        return {}
    return metadata


def _apply_wsl_registry_metadata(
    inventory: WSLDistroInventory,
) -> WSLDistroInventory:
    metadata = _read_wsl_registry_metadata()
    if not metadata:
        return inventory
    return WSLDistroInventory(
        distros=tuple(
            replace(
                distro,
                wsl_version=(
                    distro.wsl_version
                    if distro.wsl_version is not None
                    else metadata.get(
                        distro.name.casefold(),
                        WSLRegistryMetadata(None),
                    ).version
                ),
            )
            for distro in inventory.distros
        ),
        success=inventory.success,
    )


def _decode_wsl_output(stdout: object) -> str | None:
    """Decode wsl.exe console output, which is normally UTF-16LE."""
    if isinstance(stdout, str):
        return stdout.replace("\x00", "").lstrip("\ufeff")
    if not isinstance(stdout, (bytes, bytearray)):
        return None

    raw = bytes(stdout)
    if not raw:
        return ""
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else None
    if encoding is None:
        encoding = "utf-16-le" if b"\x00" in raw else "utf-8"
    try:
        decoded = raw.decode(encoding)
    except UnicodeDecodeError:
        return None
    return decoded.replace("\x00", "").lstrip("\ufeff")


def _parse_wsl_verbose_output(text: str) -> WSLDistroInventory:
    """Parse the NAME/STATE/VERSION table emitted by ``wsl --verbose``.

    Rows are parsed from the right so distribution names may contain spaces.
    Valid rows remain available for local diagnostics when another row is
    malformed, while ``success`` keeps an incomplete inventory out of both the
    upload and the discovery that :func:`list_wsl_distros` drives.
    """
    lines = [
        line.strip("\ufeff")
        for line in text.replace("\x00", "").splitlines()
        if line.strip("\ufeff").strip()
    ]
    if not lines:
        return WSLDistroInventory(distros=(), success=True)

    header_index = next(
        (
            index
            for index, line in enumerate(lines)
            if tuple(line.strip().split()) == _WSL_VERBOSE_HEADER
        ),
        None,
    )
    if header_index is None and any(
        marker in " ".join(lines).casefold() for marker in _WSL_EMPTY_MARKERS
    ):
        return WSLDistroInventory(distros=(), success=True)

    candidate_lines = lines[header_index + 1 :] if header_index is not None else lines
    parsed: list[DiscoveredWSLDistro] = []
    seen_names: set[str] = set()
    malformed = header_index is None
    over_cap = False
    for line in candidate_lines:
        match = _WSL_VERBOSE_ROW.fullmatch(line)
        if match is None:
            malformed = True
            continue
        name = match.group("name").strip()
        version = int(match.group("version"))
        if not name or version <= 0:
            malformed = True
            continue
        normalized_name = name.casefold()
        if normalized_name == "docker-desktop-data" or normalized_name in seen_names:
            continue
        if len(parsed) >= MAX_WSL_DISTROS:
            over_cap = True
            break
        seen_names.add(normalized_name)
        parsed.append(
            DiscoveredWSLDistro(
                name=name,
                wsl_version=version,
                is_running=match.group("state").casefold() == "running",
            )
        )
    return WSLDistroInventory(
        distros=tuple(parsed),
        success=not malformed and not over_cap,
    )


def _run_wsl_list(args: list[str]) -> str | None:
    """Run one ``wsl.exe --list`` variant and decode its output, or None."""
    try:
        environment = dict(os.environ)
        environment["WSL_UTF8"] = "1"
        result = subprocess.run(
            ["wsl.exe", "--list", *args],
            capture_output=True,
            timeout=10,
            env=environment,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return _decode_wsl_output(result.stdout)


def _quiet_fallback_inventory() -> WSLDistroInventory:
    """Locale-tolerant inventory from ``wsl --list --quiet`` name listings.

    ``wsl --list --verbose`` localizes its header and STATE column, so the
    strict verbose parse fails on non-English Windows (and localized Running
    states can be multi-word, which would corrupt the right-anchored name
    capture). Quiet mode prints bare distro names on every locale. Version is
    unknown here; the running set comes from ``--list --running --quiet``.
    A failed running query is retried once. Repeated failure retains the quiet
    names but leaves the inventory unsuccessful because running state is unknown.
    """
    text = _run_wsl_list(["--quiet"])
    if text is None:
        return WSLDistroInventory(distros=(), success=False)

    running_text = _run_wsl_list(["--running", "--quiet"])
    if running_text is None:
        running_text = _run_wsl_list(["--running", "--quiet"])
    running_list_succeeded = running_text is not None
    running_names = {
        line.strip().casefold()
        for line in (running_text or "").splitlines()
        if line.strip()
    }

    parsed: list[DiscoveredWSLDistro] = []
    seen_names: set[str] = set()
    over_cap = False
    for line in text.splitlines():
        name = line.strip()
        if not name:
            continue
        normalized_name = name.casefold()
        if normalized_name == "docker-desktop-data" or normalized_name in seen_names:
            continue
        if len(parsed) >= MAX_WSL_DISTROS:
            over_cap = True
            break
        seen_names.add(normalized_name)
        parsed.append(
            DiscoveredWSLDistro(
                name=name,
                wsl_version=None,
                is_running=normalized_name in running_names,
            )
        )
    return WSLDistroInventory(
        distros=tuple(parsed),
        success=running_list_succeeded and not over_cap,
    )


@lru_cache(maxsize=1)
def get_wsl_distro_inventory() -> WSLDistroInventory:
    """Collect installed WSL distributions from a Windows host once per process.

    WSL inventory is scoped to the calling Windows user. A SYSTEM all-users scan
    therefore sees a user's distros only when its child can run with that user's
    live token; stopped distros may also have unreachable UNC shares. Inventory
    does not imply process, hook, or CLI-binary discovery inside the WSL VM.

    The verbose table is authoritative when it parses (it carries version and
    running state), but its header and STATE column are localized. When the
    strict parse fails, :func:`_quiet_fallback_inventory` recovers names (and a
    best-effort running set) from the locale-stable quiet listings; only if
    that also fails does the incomplete verbose result stand, keeping any rows
    it did parse available for local diagnostics.
    """
    text = _run_wsl_list(["--verbose"])
    if text is None:
        verbose_inventory = WSLDistroInventory(distros=(), success=False)
    else:
        verbose_inventory = _parse_wsl_verbose_output(text)
    if verbose_inventory.success:
        return _apply_wsl_registry_metadata(verbose_inventory)

    quiet_inventory = _quiet_fallback_inventory()
    if quiet_inventory.success or quiet_inventory.distros:
        return _apply_wsl_registry_metadata(quiet_inventory)
    return _apply_wsl_registry_metadata(verbose_inventory)


def list_wsl_distros() -> list[str]:
    """List installed WSL distributions (Windows host only).

    Uses the shared inventory so WSL home expansion and first-class inventory
    collection do not launch duplicate subprocesses during one scan.

    An unsuccessful inventory (strict verbose parse failed and the quiet
    fallback also failed) yields nothing. Rows parsed before a malformed one
    stay on the inventory for local diagnostics, but they must not drive home
    expansion or WSL-scoped artifact attribution: the same scan withholds the
    inventory from upload, so the backend would have to synthesize distro rows
    (with a guessed running state) for artifacts it cannot corroborate.
    """
    inventory = get_wsl_distro_inventory()
    if not inventory.success:
        return []
    return [distro.name for distro in inventory.distros]


def get_wsl_user_homes(distro: str) -> list[Path]:
    """Resolve Linux user home directories inside a WSL distro from Windows.

    Lists ``\\\\wsl.localhost\\<distro>\\home\\*`` plus ``/root`` (falls back
    to the older ``\\\\wsl$`` share). To bound UNC enumeration, sorts only the
    capped listing prefix; selection is stable when the listing fits the cap.
    Returns each reachable home dir; tolerates missing and access-denied paths.
    """
    for unc_root in (Rf"\\wsl.localhost\{distro}", Rf"\\wsl$\{distro}"):
        homes: list[Path] = []
        root_home = Path(unc_root) / "root"
        try:
            if root_home.is_dir():
                homes.append(root_home)
        except OSError:
            pass
        home_base = Path(unc_root) / "home"
        try:
            if home_base.is_dir():
                probes_remaining = MAX_WSL_HOME_PROBES
                for entry in sorted(islice(home_base.iterdir(), MAX_WSL_HOME_PROBES)):
                    if len(homes) >= MAX_WSL_HOMES or probes_remaining <= 0:
                        break
                    probes_remaining -= 1
                    try:
                        is_directory = entry.is_dir()
                    except OSError:
                        continue
                    if is_directory:
                        homes.append(entry)
        except OSError:
            pass
        if homes:
            return homes
    return []


def get_wsl_distro_root(distro: str) -> Path | None:
    """Return the first reachable UNC root for a WSL distro."""
    for unc_root in (Rf"\\wsl.localhost\{distro}", Rf"\\wsl$\{distro}"):
        root = Path(unc_root)
        try:
            if root.is_dir():
                return root
        except OSError:
            continue
    return None


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
