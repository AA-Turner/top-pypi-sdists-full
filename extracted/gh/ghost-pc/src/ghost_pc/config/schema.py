"""Persistent config model stored at ~/.ghost-pc/config.json."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

GHOST_HOME: Path = Path.home() / ".ghost-pc"
CONFIG_PATH: Path = GHOST_HOME / "config.json"


class GhostConfig(BaseModel):
    """User configuration persisted to disk."""

    # API
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3-flash-preview"
    gemini_computer_use_model: str = "gemini-3-flash-preview"

    # Model tier — "flash" (fast/cheap) or "pro" (premium reasoning)
    model_tier: str = "flash"

    # Browser automation — "vision" (Gemini CU only), "cdp" (Playwright CDP),
    # "browser-use" (hybrid DOM+Vision)
    browser_method: str = "vision"

    # Screen capture
    screen_fps: int = 10
    jpeg_quality: int = 70
    capture_width: int = 1280
    capture_height: int = 720

    # Streaming
    stream_port: int = 8443
    stream_mode: str = "mjpeg"

    # Security
    emergency_hotkey: str = "ctrl+alt+q"
    allowed_numbers: list[str] = Field(default_factory=list)
    max_messages_per_minute: int = 30

    # Paths (relative to GHOST_HOME unless absolute)
    credentials_dir: str = ""
    bridge_dir: str = ""

    # Confirmation (require user approval for sensitive actions)
    confirmation_enabled: bool = True
    confirmation_timeout: int = 120  # seconds

    # Notifications (proactive system alerts and reminders)
    notifications_enabled: bool = True
    notification_watch_dirs: list[str] = Field(default_factory=lambda: ["~/Downloads"])
    notification_rate_limit: int = 20  # max per day

    # Logging
    log_level: str = "INFO"

    # Installed optional extras (for doctor checks)
    installed_extras: list[str] = Field(default_factory=list)

    # State
    setup_completed: bool = False
    autostart_enabled: bool = False

    def get_bridge_dir(self) -> Path:
        """Return the bridge directory path (anchored to GHOST_HOME if relative)."""
        if self.bridge_dir:
            p = Path(self.bridge_dir)
            return p if p.is_absolute() else GHOST_HOME / p
        return GHOST_HOME / "bridge"

    def get_credentials_dir(self) -> Path:
        """Return the credentials directory path (anchored to GHOST_HOME if relative)."""
        if self.credentials_dir:
            p = Path(self.credentials_dir)
            return p if p.is_absolute() else GHOST_HOME / p
        return GHOST_HOME / "credentials"

    @classmethod
    def load(cls) -> GhostConfig:
        """Load config from disk, returning defaults if file is missing."""
        if not CONFIG_PATH.exists():
            logger.debug("No config file at %s, using defaults", CONFIG_PATH)
            return cls()
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return cls.model_validate(data)
        except (json.JSONDecodeError, Exception) as exc:
            logger.warning("Failed to load config from %s: %s — using defaults", CONFIG_PATH, exc)
            return cls()

    def save(self) -> None:
        """Write config to disk."""
        GHOST_HOME.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(
            self.model_dump_json(indent=2) + "\n",
            encoding="utf-8",
        )
        logger.info("Config saved to %s", CONFIG_PATH)
