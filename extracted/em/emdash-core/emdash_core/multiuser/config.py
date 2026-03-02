"""Configuration for multiuser sessions.

This module handles configuration for the multiuser system including
provider selection, feature flags, and environment variable parsing.

Environment Variables:
    EMDASH_MULTIUSER_ENABLED: Enable multiuser features (true/false, default: false)
    EMDASH_MULTIUSER_PROVIDER: Provider to use (local/firebase, default: local)

    For Firebase provider:
        FIREBASE_PROJECT_ID: Firebase project ID
        FIREBASE_DATABASE_URL: Realtime Database URL
        FIREBASE_CREDENTIALS_PATH: Path to service account JSON
        FIREBASE_API_KEY: Web API key (alternative to service account)

Example Setup:
    # Enable multiuser with local provider (single machine)
    export EMDASH_MULTIUSER_ENABLED=true
    export EMDASH_MULTIUSER_PROVIDER=local

    # Enable multiuser with Firebase (multi-machine)
    export EMDASH_MULTIUSER_ENABLED=true
    export EMDASH_MULTIUSER_PROVIDER=firebase
    export FIREBASE_PROJECT_ID=my-project-123
    export FIREBASE_DATABASE_URL=https://my-project-123-default-rtdb.firebaseio.com
    export FIREBASE_CREDENTIALS_PATH=/path/to/service-account.json
"""

import logging
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

log = logging.getLogger(__name__)


class SyncProviderType(str, Enum):
    """Available sync provider types."""

    LOCAL = "local"  # File-based, single machine
    FIREBASE = "firebase"  # Firebase Realtime Database


@dataclass
class FirebaseConfig:
    """Firebase-specific configuration."""

    project_id: Optional[str] = None
    database_url: Optional[str] = None
    credentials_path: Optional[str] = None
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "FirebaseConfig":
        """Load Firebase config from environment variables."""
        return cls(
            project_id=os.environ.get("FIREBASE_PROJECT_ID"),
            database_url=os.environ.get("FIREBASE_DATABASE_URL"),
            credentials_path=os.environ.get("FIREBASE_CREDENTIALS_PATH"),
            api_key=os.environ.get("FIREBASE_API_KEY"),
        )

    def is_valid(self) -> bool:
        """Check if config has minimum required values."""
        return bool(self.database_url)

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if not self.database_url:
            errors.append("FIREBASE_DATABASE_URL is required")

        if not self.credentials_path and not self.api_key:
            errors.append("Either FIREBASE_CREDENTIALS_PATH or FIREBASE_API_KEY is required")

        if self.credentials_path and not Path(self.credentials_path).exists():
            errors.append(f"Credentials file not found: {self.credentials_path}")

        return errors


@dataclass
class MultiuserConfig:
    """Configuration for multiuser features."""

    # Feature flag
    enabled: bool = False

    # Provider selection
    provider: SyncProviderType = SyncProviderType.LOCAL

    # Storage root for local provider
    storage_root: Path = field(default_factory=lambda: Path.home() / ".emdash" / "multiuser")

    # Firebase config (only used when provider=firebase)
    firebase: FirebaseConfig = field(default_factory=FirebaseConfig)

    # Heartbeat interval in seconds
    heartbeat_interval: int = 30

    # Session timeout in seconds (mark offline after this)
    session_timeout: int = 120

    # Default team ID (sessions created with multiuser enabled will auto-join this team)
    default_team_id: Optional[str] = None

    # Auto-share: automatically share new sessions with the default team
    auto_share_to_team: bool = False

    @classmethod
    def from_env(cls) -> "MultiuserConfig":
        """Load configuration from environment variables."""
        enabled = os.environ.get("EMDASH_MULTIUSER_ENABLED", "").lower() in ("true", "1", "yes")

        provider_str = os.environ.get("EMDASH_MULTIUSER_PROVIDER", "local").lower()
        try:
            provider = SyncProviderType(provider_str)
        except ValueError:
            log.warning(f"Unknown provider '{provider_str}', using local")
            provider = SyncProviderType.LOCAL

        storage_root = Path(
            os.environ.get("EMDASH_MULTIUSER_STORAGE", str(Path.home() / ".emdash" / "multiuser"))
        )

        heartbeat_interval = int(os.environ.get("EMDASH_MULTIUSER_HEARTBEAT", "30"))
        session_timeout = int(os.environ.get("EMDASH_MULTIUSER_TIMEOUT", "120"))

        # Team configuration
        default_team_id = os.environ.get("EMDASH_TEAM_ID") or None
        auto_share_to_team = os.environ.get("EMDASH_AUTO_SHARE_TO_TEAM", "").lower() in ("true", "1", "yes")

        return cls(
            enabled=enabled,
            provider=provider,
            storage_root=storage_root,
            firebase=FirebaseConfig.from_env(),
            heartbeat_interval=heartbeat_interval,
            session_timeout=session_timeout,
            default_team_id=default_team_id,
            auto_share_to_team=auto_share_to_team,
        )

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if self.provider == SyncProviderType.FIREBASE:
            errors.extend(self.firebase.validate())

        return errors

    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return len(self.validate()) == 0


# Global config instance (lazily loaded)
_config: Optional[MultiuserConfig] = None


def get_multiuser_config() -> MultiuserConfig:
    """Get the global multiuser configuration.

    Loads from environment variables on first call.
    """
    global _config
    if _config is None:
        _config = MultiuserConfig.from_env()
        log.debug(f"Loaded multiuser config: enabled={_config.enabled}, provider={_config.provider}")
    return _config


def set_multiuser_config(config: MultiuserConfig) -> None:
    """Set the global multiuser configuration."""
    global _config
    _config = config


def is_multiuser_enabled() -> bool:
    """Check if multiuser features are enabled."""
    return get_multiuser_config().enabled


def get_provider_type() -> SyncProviderType:
    """Get the configured provider type."""
    return get_multiuser_config().provider


def print_config_help():
    """Print help for configuring multiuser."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    MULTIUSER CONFIGURATION                       ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  To enable multiuser features, set these environment variables:  ║
║                                                                  ║
║  ┌─────────────────────────────────────────────────────────────┐ ║
║  │ BASIC (Local Provider - Single Machine)                     │ ║
║  │                                                             │ ║
║  │   export EMDASH_MULTIUSER_ENABLED=true                      │ ║
║  │   export EMDASH_MULTIUSER_PROVIDER=local                    │ ║
║  │                                                             │ ║
║  └─────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  ┌─────────────────────────────────────────────────────────────┐ ║
║  │ FIREBASE (Multi-Machine Real-Time Sync)                     │ ║
║  │                                                             │ ║
║  │   export EMDASH_MULTIUSER_ENABLED=true                      │ ║
║  │   export EMDASH_MULTIUSER_PROVIDER=firebase                 │ ║
║  │   export FIREBASE_PROJECT_ID=your-project-id                │ ║
║  │   export FIREBASE_DATABASE_URL=https://your-project.firebaseio.com │
║  │                                                             │ ║
║  │   # Authentication (choose one):                            │ ║
║  │   export FIREBASE_CREDENTIALS_PATH=/path/to/service.json    │ ║
║  │   # OR                                                      │ ║
║  │   export FIREBASE_API_KEY=your-api-key                      │ ║
║  │                                                             │ ║
║  └─────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  Firebase Setup:                                                 ║
║  1. Go to https://console.firebase.google.com                    ║
║  2. Create a project (or use existing)                           ║
║  3. Enable Realtime Database                                     ║
║  4. For service account: Project Settings > Service Accounts     ║
║     > Generate new private key                                   ║
║  5. For API key: Project Settings > General > Web API Key        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
