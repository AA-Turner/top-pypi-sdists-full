"""Device identification utilities for MCP Watch."""

import os
import platform
import socket
import subprocess
import uuid
from pathlib import Path

import structlog

from runlayer_cli.paths import get_runlayer_dir

logger = structlog.get_logger(__name__)

DEVICE_ID_FILE = "device_id"

SYSTEM_USERNAMES = {"root", "_mbsetupuser", "loginwindow"}


def _get_device_id_path() -> Path:
    """Get the path to the device ID file."""
    return get_runlayer_dir() / DEVICE_ID_FILE


def get_or_create_device_id() -> str:
    """
    Get or create a stable device identifier.

    Priority:
    1. Environment variable RUNLAYER_DEVICE_ID
    2. Stored device ID in ~/.runlayer/device_id
    3. Generate and store a new UUID

    Returns:
        Stable device identifier string
    """
    # Check environment variable first
    env_device_id = os.environ.get("RUNLAYER_DEVICE_ID")
    if env_device_id:
        logger.debug(
            "Using device ID from environment", device_id_prefix=env_device_id[:8]
        )
        return env_device_id

    # Check stored device ID
    device_id_path = _get_device_id_path()
    if device_id_path.exists():
        try:
            device_id = device_id_path.read_text().strip()
            if device_id:
                logger.debug("Using stored device ID", device_id_prefix=device_id[:8])
                return device_id
        except IOError:
            pass

    # Generate new device ID
    device_id = str(uuid.uuid4())
    logger.info("Generated new device ID", device_id_prefix=device_id[:8])

    # Store for future use
    try:
        device_id_path.parent.mkdir(parents=True, exist_ok=True)
        device_id_path.write_text(device_id)
    except IOError as e:
        logger.warning("Failed to store device ID", error=str(e))

    return device_id


def get_device_metadata() -> dict[str, str | None]:
    """
    Collect device metadata for the scan payload.

    Returns:
        Dictionary with device metadata
    """
    system = platform.system().lower()
    # Normalize platform names
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

    return {
        "hostname": hostname,
        "os": os_name,
        "os_version": platform.release(),
        "username": username,
    }


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
