"""Installed Runlayer build-variant identity for binary updates."""

from pathlib import Path
import sys

from runlayer_cli import regex_safe


_VARIANT_PATTERN = regex_safe.compile(r"glibc[0-9]+\.[0-9]+")
_CLI_VARIANT_MARKER_PATH = Path("/usr/lib/runlayer/variant")
_AIWATCH_VARIANT_MARKER_PATH = Path("/usr/lib/runlayer/aiwatch/variant")
# "desktop" shares the CLI marker path: cli and desktop are the same native
# /usr/lib/runlayer install slot (mirrors product.py's shared marker).
_VARIANT_MARKER_PATHS: dict[str, Path] = {
    "cli": _CLI_VARIANT_MARKER_PATH,
    "desktop": _CLI_VARIANT_MARKER_PATH,
    "ai-watch": _AIWATCH_VARIANT_MARKER_PATH,
}


def installed_variant(package: str) -> str | None:
    """Read the package-owned build-variant marker; absent means standard."""
    # Validate the package before the platform gate so a wiring bug fails on
    # every OS, not just Linux.
    marker_path = _VARIANT_MARKER_PATHS.get(package)
    if marker_path is None:
        raise ValueError(f"Unsupported binary package: {package!r}")
    if sys.platform != "linux":
        return None
    try:
        variant = marker_path.read_text(encoding="ascii").strip()
    except FileNotFoundError:
        return None
    except (OSError, UnicodeError) as exc:
        raise RuntimeError("Installed Runlayer variant marker is unreadable") from exc
    if _VARIANT_PATTERN.fullmatch(variant) is None:
        raise RuntimeError("Installed Runlayer variant marker is invalid")
    return variant
