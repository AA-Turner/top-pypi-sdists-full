# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Configuration management for muffuletta CLI."""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

CONFIG_DIR = Path.home() / ".geneva"
CONFIG_FILE = CONFIG_DIR / "config.json"


class Config(BaseModel):
    """muffuletta configuration."""

    db_uri: str | None = Field(None, description="Geneva database URI")
    namespace: str | None = Field(None, description="Default Kubernetes namespace")

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from file."""
        if not CONFIG_FILE.exists():
            return cls()

        try:
            data = json.loads(CONFIG_FILE.read_text())
            return cls.model_validate(data)
        except (json.JSONDecodeError, ValueError):
            return cls()

    def save(self) -> None:
        """Save configuration to file."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(self.model_dump(exclude_none=True), indent=2))

    def get(self, key: str) -> Any:
        """Get a configuration value."""
        return getattr(self, key, None)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Unknown configuration key: {key}")


def get_config() -> Config:
    """Get the current configuration."""
    return Config.load()


def get_db_uri() -> str | None:
    """Get the configured database URI."""
    return get_config().db_uri
