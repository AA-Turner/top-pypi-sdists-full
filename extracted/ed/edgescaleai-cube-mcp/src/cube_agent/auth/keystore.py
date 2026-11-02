"""Local API key storage for cube-agent."""

from __future__ import annotations

from cube_agent.config import CONFIG_DIR, KEY_FILE


def save_key(api_key: str) -> None:
    """Save API key to local config directory."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    KEY_FILE.write_text(api_key)
    KEY_FILE.chmod(0o600)


def delete_key() -> bool:
    """Delete stored API key. Returns True if a key was removed."""
    if KEY_FILE.exists():
        KEY_FILE.unlink()
        return True
    return False


def has_key() -> bool:
    """Check if an API key is stored."""
    return KEY_FILE.exists() and KEY_FILE.stat().st_size > 0
