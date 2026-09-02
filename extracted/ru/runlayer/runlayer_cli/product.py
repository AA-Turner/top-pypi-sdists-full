"""Installed Runlayer product identity for binary updates."""

from pathlib import Path
import sys
from typing import Literal


InstalledPackage = Literal["cli", "desktop"]

if sys.platform == "win32":
    _PRODUCT_MARKER_PATH = Path(r"C:\Program Files\Runlayer\CLI\product")
elif sys.platform == "darwin":
    _PRODUCT_MARKER_PATH = Path("/usr/local/lib/runlayer/product")
else:
    _PRODUCT_MARKER_PATH = Path("/usr/lib/runlayer/product")
PRODUCT_DISPLAY_NAMES: dict[InstalledPackage, str] = {
    "cli": "Runlayer CLI",
    "desktop": "Runlayer",
}


def installed_package() -> InstalledPackage:
    """Read the package-owned marker; legacy installs without one are CLI."""
    try:
        package = _PRODUCT_MARKER_PATH.read_text(encoding="ascii").strip()
    except FileNotFoundError:
        return "cli"
    except (OSError, UnicodeError) as exc:
        raise RuntimeError("Installed Runlayer product marker is unreadable") from exc
    if package == "cli":
        return "cli"
    if package == "desktop":
        return "desktop"
    raise RuntimeError("Installed Runlayer product marker is invalid")


def package_display_name(package: InstalledPackage) -> str:
    return PRODUCT_DISPLAY_NAMES[package]
