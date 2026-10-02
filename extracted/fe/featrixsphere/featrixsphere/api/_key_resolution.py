#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Shared API key / config resolution.

Single source of truth for both featrixsphere and featrixevents --
featrixevents/_key_resolution.py is a symlink to this file (featrixevents
is a deliberately standalone package with no import dependency on
featrixsphere, so the file is duplicated at the filesystem level via the
symlink rather than imported across the package boundary; edit this file
only, the symlink keeps featrixevents in sync automatically).

Checks (in order of precedence):
  1. FEATRIX_API_KEY / FEATRIX_BASE_URL environment variables
  2. ~/.featrix (if it's a file)
  3. ~/.featrix/identity.env (if ~/.featrix is a directory)
  4. ~/.featrix/config (if ~/.featrix is a directory)
  5. ~/.featrix_default_key
  6. FEATRIX_KEY_FILE env var, default /etc/.featrix_key (raw key text,
     same file beagle's admin-ui backend reads -- see
     admin-ui/backend/config.py)

Supports two file formats:
  1. JSON: {"api_key": "fx_...", "base_url": "https://..."}
  2. Env-style: api_key=fx_... / FEATRIX_API_KEY=fx_...

/etc/.featrix_key is a third format: the raw key with no key= prefix at all.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

_CONFIG_PATHS = [
    Path.home() / ".featrix",
    Path.home() / ".featrix" / "identity.env",
    Path.home() / ".featrix" / "config",
    Path.home() / ".featrix_default_key",
]


def _read_config_file(path: Path) -> Optional[Dict[str, str]]:
    """Try to read a config file. Returns parsed dict or None."""
    if not path.is_file():
        return None
    try:
        content = path.read_text().strip()
        if not content:
            return None

        # Try JSON format first
        if content.startswith('{'):
            return json.loads(content)

        # Parse env-style format: key=value
        file_config = {}
        for line in content.splitlines():
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                value = value.strip()
                # Strip surrounding quotes (single or double)
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                file_config[key.strip().lower()] = value
        return file_config

    except Exception as e:
        logger.debug(f"Failed to read config from {path}: {e}")
        return None


def load_config() -> Dict[str, str]:
    """Load config from environment variables and config files.

    Checks (in order of precedence):
    1. FEATRIX_API_KEY / FEATRIX_BASE_URL environment variables
    2. ~/.featrix (if it's a file)
    3. ~/.featrix/identity.env (if ~/.featrix is a directory)
    4. ~/.featrix/config (if ~/.featrix is a directory)
    5. ~/.featrix_default_key

    Supports two file formats:
    1. JSON: {"api_key": "sk_live_...", "base_url": "https://..."}
    2. Env-style: api_key=sk_live_...

    Returns:
        Dict with 'api_key' and optionally 'base_url'.
    """
    config = {}

    # Check environment variables first (highest precedence)
    env_key = os.getenv("FEATRIX_API_KEY")
    if env_key:
        config["api_key"] = env_key

    env_url = os.getenv("FEATRIX_BASE_URL")
    if env_url:
        config["base_url"] = env_url

    # Then check config files (env vars take precedence)
    for path in _CONFIG_PATHS:
        file_config = _read_config_file(path)
        if file_config is None:
            continue

        # Support both "api_key" and "featrix_api_key" in config file
        if "api_key" not in config:
            if "api_key" in file_config:
                config["api_key"] = file_config["api_key"]
            elif "featrix_api_key" in file_config:
                config["api_key"] = file_config["featrix_api_key"]
        if "base_url" not in config:
            if "base_url" in file_config:
                config["base_url"] = file_config["base_url"]
            elif "featrix_base_url" in file_config:
                config["base_url"] = file_config["featrix_base_url"]

        # Stop once we've found what we need
        if "api_key" in config:
            break

    # Last resort: system-wide key file (raw key text, no key= prefix).
    # Present on boxes that don't have a per-user ~/.featrix (compute nodes
    # running as root, beagle) -- same file admin-ui/backend/config.py reads.
    if "api_key" not in config:
        etc_key_path = Path(os.getenv("FEATRIX_KEY_FILE", "/etc/.featrix_key"))
        if etc_key_path.is_file():
            try:
                raw_key = etc_key_path.read_text().strip()
                if raw_key:
                    config["api_key"] = raw_key
            except Exception as e:
                logger.debug(f"Failed to read config from {etc_key_path}: {e}")

    return config


def get_api_key() -> Optional[str]:
    """Convenience wrapper: resolve just the API key, or None if not found."""
    return load_config().get("api_key")


# Where the Featrix Internal key is provisioned. Linux nodes: the raw key in
# /etc/.featrix_key (root-owned). Mac nodes: the node user's
# ~/.featrix-mac-secrets, the one file holding every Mac node secret (same
# KEY=VALUE file as the DO Spaces credentials -- see
# lib.featrix.platform_utils.MacHost.spaces_keyfile); the services run as that
# user and macOS's /etc needs sudo to provision. FEATRIX_KEY_FILE (raw key
# text) overrides both.
_LINUX_INTERNAL_KEY_FILE = "/etc/.featrix_key"
_MAC_SECRETS_FILE_NAME = ".featrix-mac-secrets"
MAC_INTERNAL_KEY_VAR = "FEATRIX_INTERNAL_API_KEY"


def _mac_secrets_path() -> Path:
    return Path.home() / _MAC_SECRETS_FILE_NAME


def internal_key_location() -> str:
    """Human-readable location get_internal_api_key() reads on this host."""
    override = os.getenv("FEATRIX_KEY_FILE")
    if override:
        return override
    if sys.platform == "darwin":
        return f"{MAC_INTERNAL_KEY_VAR}= in {_mac_secrets_path()}"
    return _LINUX_INTERNAL_KEY_FILE


def get_internal_api_key() -> Optional[str]:
    """Resolve the Featrix Internal org's API key.

    Deliberately bypasses the FEATRIX_API_KEY / ~/.featrix precedence chain
    in load_config() -- those are per-environment and may hold a customer's
    key (e.g. a customer job's process env). The internal key lives at one
    fixed, known location provisioned on every node (internal_key_location():
    /etc/.featrix_key on Linux, FEATRIX_INTERNAL_API_KEY= in
    ~/.featrix-mac-secrets on a Mac, or the FEATRIX_KEY_FILE override).
    Training that is explicitly Featrix's own must read from there directly,
    not fall through an ambient chain that could resolve to someone else's key.
    """
    override = os.getenv("FEATRIX_KEY_FILE")
    if not override and sys.platform == "darwin":
        secrets = _read_config_file(_mac_secrets_path()) or {}
        return (secrets.get(MAC_INTERNAL_KEY_VAR.lower()) or "").strip() or None
    key_path = Path(override or _LINUX_INTERNAL_KEY_FILE)
    if not key_path.is_file():
        return None
    try:
        return key_path.read_text().strip() or None
    except Exception as e:
        logger.debug(f"Failed to read internal key from {key_path}: {e}")
        return None
