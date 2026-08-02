"""Resolve the Claude notification icon to a filesystem path for desktop-notifier.

The official Claude logo ships as ``assets/claude.svg`` in the package. Since the
package may live inside a zip, we extract it once to a stable path so the detached
notification worker can read it after the hook process has exited.
"""

import importlib.resources

from ..config import assistant_data_dir

ICON_CACHE = assistant_data_dir("claude") / "assets" / "claude-icon.svg"
_FALLBACK = "dialog-information"


def icon_path() -> str:
    """Path to the Claude icon, or a themed fallback name if the asset is unavailable."""
    if ICON_CACHE.exists():
        return str(ICON_CACHE)
    try:
        data = importlib.resources.files("pysae_ai_tools.usage").joinpath("assets", "claude.svg").read_bytes()
        ICON_CACHE.parent.mkdir(parents=True, exist_ok=True)
        ICON_CACHE.write_bytes(data)
        return str(ICON_CACHE)
    except (OSError, ModuleNotFoundError, FileNotFoundError):
        return _FALLBACK
