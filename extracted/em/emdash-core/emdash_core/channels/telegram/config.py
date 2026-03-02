"""Telegram configuration management.

Handles storage and retrieval of Telegram bot configuration including
bot token, authorized chat IDs, and user preferences.
"""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


# Config file location
CONFIG_DIR = Path.home() / ".emdash"
CONFIG_FILE = CONFIG_DIR / "telegram.json"


@dataclass
class TelegramSettings:
    """User settings for Telegram integration."""

    # How to display streaming responses: "edit" updates a single message,
    # "append" sends new messages for each update
    streaming_mode: str = "edit"

    # Minimum interval between message edits (ms) to avoid rate limits
    update_interval_ms: int = 500

    # Whether to show agent thinking/reasoning
    show_thinking: bool = False

    # Whether to show tool calls and results
    show_tool_calls: bool = False

    # Use compact formatting for responses
    compact_mode: bool = False

    # Enable live status panel — aggregates tool calls and progress
    # into a single continuously-edited message so users can see what
    # the LLM is doing in real time.  The show_thinking and
    # show_tool_calls flags above still control whether thinking and
    # tool events appear in the panel.
    show_status_panel: bool = True

    # Maximum message length before splitting (Telegram limit is 4096)
    max_message_length: int = 4000


@dataclass
class TelegramState:
    """Runtime state for Telegram integration."""

    # Whether the integration is enabled
    enabled: bool = False

    # Last successful connection timestamp (ISO format)
    last_connected: str | None = None

    # Last update_id processed (for long-polling offset)
    last_update_id: int = 0

    # Bot username (cached from verify_token / getMe)
    bot_username: str | None = None


@dataclass
class TelegramConfig:
    """Complete Telegram configuration."""

    # Bot token from @BotFather
    bot_token: str | None = None

    # List of authorized chat IDs that can interact with the bot
    authorized_chats: list[int] = field(default_factory=list)

    # User settings
    settings: TelegramSettings = field(default_factory=TelegramSettings)

    # Runtime state
    state: TelegramState = field(default_factory=TelegramState)

    def is_configured(self) -> bool:
        """Check if the bot token is configured."""
        return bool(self.bot_token)

    def is_chat_authorized(self, chat_id: int) -> bool:
        """Check if a chat ID is authorized to use the bot."""
        # If no chats are configured, allow all (during setup)
        if not self.authorized_chats:
            return True
        return chat_id in self.authorized_chats

    def add_authorized_chat(self, chat_id: int) -> None:
        """Add a chat ID to the authorized list."""
        if chat_id not in self.authorized_chats:
            self.authorized_chats.append(chat_id)

    def remove_authorized_chat(self, chat_id: int) -> None:
        """Remove a chat ID from the authorized list."""
        if chat_id in self.authorized_chats:
            self.authorized_chats.remove(chat_id)

    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary for JSON serialization."""
        return {
            "bot_token": self.bot_token,
            "authorized_chats": self.authorized_chats,
            "settings": asdict(self.settings),
            "state": asdict(self.state),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TelegramConfig":
        """Create config from dictionary."""
        settings_data = data.get("settings", {})
        state_data = data.get("state", {})

        return cls(
            bot_token=data.get("bot_token"),
            authorized_chats=data.get("authorized_chats", []),
            settings=TelegramSettings(**settings_data),
            state=TelegramState(**state_data),
        )


def get_config() -> TelegramConfig:
    """Load Telegram configuration from disk.

    Returns:
        TelegramConfig instance (empty config if file doesn't exist)
    """
    if not CONFIG_FILE.exists():
        return TelegramConfig()

    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
        return TelegramConfig.from_dict(data)
    except (json.JSONDecodeError, KeyError, TypeError):
        # Return empty config if file is corrupted
        return TelegramConfig()


def save_config(config: TelegramConfig) -> None:
    """Save Telegram configuration to disk.

    Args:
        config: TelegramConfig instance to save
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        json.dump(config.to_dict(), f, indent=2)


def delete_config() -> bool:
    """Delete the Telegram configuration file.

    Returns:
        True if file was deleted, False if it didn't exist
    """
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        return True
    return False
