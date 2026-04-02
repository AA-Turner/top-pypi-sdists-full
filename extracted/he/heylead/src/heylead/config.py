"""HeyLead config management — ~/.heylead/config.json."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Optional

from . import constants

logger = logging.getLogger(__name__)


def _heylead_home() -> Path:
    """Return the HeyLead home directory (~/.heylead)."""
    return Path.home() / constants.HEYLEAD_DIR_NAME


def ensure_dirs() -> Path:
    """Create all required directories and return the home path."""
    home = _heylead_home()
    (home / constants.DB_DIR).mkdir(parents=True, exist_ok=True)
    (home / constants.AUTH_DIR).mkdir(parents=True, exist_ok=True)
    (home / constants.LOG_DIR).mkdir(parents=True, exist_ok=True)
    (home / constants.VOICE_MEMO_DIR).mkdir(parents=True, exist_ok=True)
    (home / constants.BACKUP_DIR).mkdir(parents=True, exist_ok=True)
    return home


def config_path() -> Path:
    return _heylead_home() / constants.CONFIG_FILE


def db_path() -> Path:
    return _heylead_home() / constants.DB_DIR / constants.DB_FILE


def cookie_path() -> Path:
    """Legacy — kept for cleanup of old installs."""
    return _heylead_home() / constants.AUTH_DIR / constants.COOKIE_FILE


def log_path() -> Path:
    return _heylead_home() / constants.LOG_DIR / constants.LOG_FILE


def json_log_path() -> Path:
    return _heylead_home() / constants.LOG_DIR / constants.LOG_FILE_JSON


# ──────────────────────────────────────────────
# Config read / write
# ──────────────────────────────────────────────

_DEFAULT_CONFIG: dict[str, Any] = {
    "llm_priority": constants.DEFAULT_LLM_PRIORITY,
    "api_keys": {
        "gemini": "",
        "claude": "",
        "openai": "",
        "serper": "",
        "hume": "",
    },
    "timezone": "",
    "working_hours": {
        "start": constants.DEFAULT_START_HOUR,
        "end": constants.DEFAULT_END_HOUR,
        "days": constants.DEFAULT_ACTIVE_DAYS,
    },
    "unipile_api_url": "",
    "unipile_api_key": "",
    "tier": constants.TIER_FREE,
    "telemetry": False,
    "scheduler_enabled": False,
    "scheduler_always_on": False,
    "gemini_model": constants.DEFAULT_GEMINI_MODEL,
    "claude_model": constants.DEFAULT_CLAUDE_MODEL,
    "openai_model": constants.DEFAULT_OPENAI_MODEL,
}


def load_config() -> dict[str, Any]:
    """Load config from disk, creating default if missing."""
    ensure_dirs()
    path = config_path()
    if path.exists():
        try:
            with open(path, "r") as f:
                data = json.load(f)
            # Merge defaults for any missing keys
            merged = {**_DEFAULT_CONFIG, **data}
            # Deep-merge nested dicts
            for key in ("api_keys", "working_hours"):
                if key in _DEFAULT_CONFIG:
                    merged[key] = {**_DEFAULT_CONFIG[key], **data.get(key, {})}
            # Migrate: upgrade to 24/7 autonomous bot (no working hours)
            wh = merged.get("working_hours", {})
            needs_save = False
            if wh.get("days") == [0, 1, 2, 3, 4]:
                wh["days"] = constants.DEFAULT_ACTIVE_DAYS
                needs_save = True
            if wh.get("start", 0) != 0 or wh.get("end", 24) != 24:
                wh["start"] = constants.DEFAULT_START_HOUR
                wh["end"] = constants.DEFAULT_END_HOUR
                needs_save = True
            if needs_save:
                merged["working_hours"] = wh
                save_config(merged)
                logger.info("Config migrated: working_hours upgraded to 24/7 autonomous")
            return merged
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Config file corrupt, using defaults: {e}")
            return dict(_DEFAULT_CONFIG)
    else:
        save_config(_DEFAULT_CONFIG)
        return dict(_DEFAULT_CONFIG)


def save_config(cfg: dict[str, Any]) -> None:
    """Persist config to disk."""
    ensure_dirs()
    path = config_path()
    with open(path, "w") as f:
        json.dump(cfg, f, indent=2)


def get_api_key(provider: str) -> str:
    """Return API key for a given LLM provider, or empty string."""
    cfg = load_config()
    return cfg.get("api_keys", {}).get(provider, "")


def set_api_key(provider: str, key: str) -> None:
    """Store an API key."""
    cfg = load_config()
    cfg.setdefault("api_keys", {})[provider] = key
    save_config(cfg)


def get_tier() -> str:
    """Return current tier ('free' or 'pro')."""
    cfg = load_config()
    return cfg.get("tier", constants.TIER_FREE)


def get_timezone() -> str:
    """Return configured timezone string, or empty."""
    cfg = load_config()
    return cfg.get("timezone", "")


def set_timezone(tz: str) -> None:
    cfg = load_config()
    cfg["timezone"] = tz
    save_config(cfg)


# ──────────────────────────────────────────────
# Unipile config helpers
# ──────────────────────────────────────────────

def get_unipile_config() -> tuple[str, str]:
    """Return (api_url, api_key) from config."""
    cfg = load_config()
    return cfg.get("unipile_api_url", ""), cfg.get("unipile_api_key", "")


def set_unipile_config(api_url: str, api_key: str) -> None:
    """Store Unipile credentials."""
    cfg = load_config()
    cfg["unipile_api_url"] = api_url.strip()
    cfg["unipile_api_key"] = api_key.strip()
    save_config(cfg)


# ──────────────────────────────────────────────
# Backend proxy config helpers
# ──────────────────────────────────────────────

def get_backend_config() -> tuple[str, str]:
    """Return (backend_url, jwt_token) from config.

    Defaults to the production backend URL if none is configured.
    Users only need to provide a JWT — the URL is automatic.
    """
    cfg = load_config()
    url = cfg.get("backend_url", "") or constants.DEFAULT_BACKEND_URL
    jwt_token = cfg.get("backend_jwt", "")
    return url, jwt_token


def set_backend_config(backend_url: str, jwt_token: str) -> None:
    """Store backend proxy credentials."""
    cfg = load_config()
    cfg["backend_url"] = backend_url.strip()
    cfg["backend_jwt"] = jwt_token.strip()
    save_config(cfg)


def is_backend_mode() -> bool:
    """Check if the MCP server should use the backend proxy."""
    url, jwt = get_backend_config()
    return bool(url and jwt)


def has_local_llm_key() -> bool:
    """Check if the user has any local LLM API key configured."""
    cfg = load_config()
    return any(v for v in cfg.get("api_keys", {}).values() if v)


# ──────────────────────────────────────────────
# ICP / Ingestion config helpers
# ──────────────────────────────────────────────

def embeddings_path() -> Path:
    """Return the embeddings cache directory (~/.heylead/embeddings/)."""
    return _heylead_home() / constants.EMBEDDINGS_DIR


def kb_path() -> Path:
    """Return the knowledge base directory (~/.heylead/knowledge-base/)."""
    return _heylead_home() / constants.KB_DIR


def get_firecrawl_api_key() -> str:
    """Return the Firecrawl API key from config, or empty string."""
    cfg = load_config()
    return cfg.get("firecrawl_api_key", "")


def get_serper_api_key() -> str:
    """Return the SERPER API key from config, or empty string."""
    cfg = load_config()
    return cfg.get("api_keys", {}).get("serper", "")


# ──────────────────────────────────────────────
# Scheduler config helpers
# ──────────────────────────────────────────────

def is_scheduler_enabled() -> bool:
    """Check if the autonomous scheduler is enabled."""
    return load_config().get("scheduler_enabled", False)


def set_scheduler_enabled(
    enabled: bool,
    *,
    caller: str = "unknown",
    reason: str = "",
) -> None:
    """Enable or disable the autonomous scheduler with attribution.

    Args:
        enabled: Whether to enable or disable.
        caller: Who triggered this change (e.g., "mcp_tool", "auto_campaign",
                "always_on_guard", "config_edit").
        reason: Human-readable reason for the change.
    """
    import time as _time

    cfg = load_config()
    was_enabled = cfg.get("scheduler_enabled", False)
    cfg["scheduler_enabled"] = enabled
    cfg["_last_scheduler_toggle"] = {
        "from": was_enabled,
        "to": enabled,
        "caller": caller,
        "reason": reason,
        "timestamp": int(_time.time()),
    }
    save_config(cfg)


def is_scheduler_always_on() -> bool:
    """Check if scheduler always-on mode is active."""
    return load_config().get("scheduler_always_on", False)


def set_scheduler_always_on(enabled: bool) -> None:
    """Enable or disable scheduler always-on mode."""
    cfg = load_config()
    cfg["scheduler_always_on"] = enabled
    save_config(cfg)


# ──────────────────────────────────────────────
# Hume AI / Voice Memo config helpers
# ──────────────────────────────────────────────

def get_hume_api_key() -> str:
    """Return Hume AI API key from config, or empty string."""
    cfg = load_config()
    return cfg.get("api_keys", {}).get("hume", "")


def set_hume_api_key(key: str) -> None:
    """Store Hume AI API key."""
    cfg = load_config()
    cfg.setdefault("api_keys", {})["hume"] = key
    save_config(cfg)


def is_voice_memo_enabled() -> bool:
    """Check if voice memos are configured (Hume API key or backend mode)."""
    if get_hume_api_key():
        return True
    if is_backend_mode():
        return True  # Backend proxies Hume calls
    return False


def voice_memo_dir() -> Path:
    """Return the voice memos directory (~/.heylead/voice_memos/)."""
    return _heylead_home() / constants.VOICE_MEMO_DIR


def backups_dir() -> Path:
    """Return the backups directory (~/.heylead/backups/)."""
    return _heylead_home() / constants.BACKUP_DIR
