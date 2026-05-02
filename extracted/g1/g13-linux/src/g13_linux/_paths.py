"""Centralized path resolution for the g13_linux package.

Detects whether we're running from a source checkout (dev mode) or
an installed package and provides consistent paths for configs,
profiles, macros, and static assets.
"""

from __future__ import annotations

from pathlib import Path

# Package directory: src/g13_linux/
_PACKAGE_DIR: Path = Path(__file__).parent

# Source root: two levels up from package dir (src/g13_linux/ -> src/ -> project root)
_SOURCE_ROOT: Path = _PACKAGE_DIR.parent.parent

# User config directory for installed (non-dev) mode
_USER_CONFIG_DIR: Path = Path.home() / ".config" / "g13-linux"


def _is_source_checkout() -> bool:
    """Check if we're running from a source checkout.

    Returns True if both configs/ and pyproject.toml exist at the
    computed source root, indicating a development environment.
    """
    return (_SOURCE_ROOT / "configs").is_dir() and (_SOURCE_ROOT / "pyproject.toml").is_file()


def get_configs_dir() -> Path:
    """Get the configs directory.

    Returns source root configs/ in dev, ~/.config/g13-linux/ when installed.
    """
    if _is_source_checkout():
        return _SOURCE_ROOT / "configs"
    return _USER_CONFIG_DIR


def get_profiles_dir() -> Path:
    """Get the profiles directory (configs/profiles/)."""
    return get_configs_dir() / "profiles"


def get_macros_dir() -> Path:
    """Get the macros directory (configs/macros/)."""
    return get_configs_dir() / "macros"


def get_app_profiles_path() -> Path:
    """Get the app_profiles.json path (configs/app_profiles.json)."""
    return get_configs_dir() / "app_profiles.json"


def get_static_dir() -> Path:
    """Get the web GUI static files directory (gui-web/dist/ in dev)."""
    return _SOURCE_ROOT / "gui-web" / "dist"
