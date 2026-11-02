"""cube-agent configuration."""

from __future__ import annotations

import os
from pathlib import Path

# Default cube-cloud endpoint
DEFAULT_CLOUD_URL = "https://cube.edgescaleai-cube.com"

# Config directory
CONFIG_DIR = Path(os.environ.get("CUBE_AGENT_CONFIG_DIR", "~/.cube-agent")).expanduser()
CONFIG_FILE = CONFIG_DIR / "config.toml"
KEY_FILE = CONFIG_DIR / "api_key"


def get_cloud_url() -> str:
    """Return the cube-cloud URL from env or default."""
    return os.environ.get("CUBE_CLOUD_URL", DEFAULT_CLOUD_URL)


def get_api_key() -> str | None:
    """Return the API key from env, key file, or None."""
    key = os.environ.get("CUBE_API_KEY")
    if key:
        return key

    if KEY_FILE.exists():
        return KEY_FILE.read_text().strip()

    return None
