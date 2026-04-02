"""Chronos configuration - uses the shared config models from worlds/config.py."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from plato.runtime import VMRuntimeConfig

# Import world-specific config models
from plato.worlds.config import DevConfig, SessionConfig


def _expand_vars_recursive(obj: Any) -> None:
    """Walk a parsed JSON structure and expand ${VAR} references in string values."""
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            val = obj[key]
            if isinstance(val, str):
                obj[key] = os.path.expandvars(val)
            else:
                _expand_vars_recursive(val)
    elif isinstance(obj, list):
        for i, val in enumerate(obj):
            if isinstance(val, str):
                obj[i] = os.path.expandvars(val)
            else:
                _expand_vars_recursive(val)


class WorldConfig(BaseModel):
    """World package, runtime, and config.

    Package should include version using colon separator (e.g., "plato-world-name:0.1.0").
    Image is fetched from the world's schema.json on PyPI.

    Example:
        {
            "package": "plato-world-structured-execution:0.0.0.dev4",
            "runtime": {"type": "vm", "vm": {"cpus": 2, "memory": 4096}},
            "config": {"sim_name": "...", "steps": [...]}
        }
    """

    package: str  # Package name with optional version (e.g., plato-world-name:0.1.0)
    world_name: str | None = None  # World name for multi-world packages
    image: str = ""  # Direct image URL override — skips registry lookup when set
    runtime: VMRuntimeConfig = Field(default_factory=VMRuntimeConfig)
    config: dict[str, Any] = Field(default_factory=dict)


class Config(BaseModel):
    """Chronos job configuration.

    World config is nested under world.config.
    Agent configs are at the top level with their own runtime settings.

    Example:
        {
            "world": {
                "package": "structured-execution",
                "image": "...",
                "runtime": {"type": "vm", "vm": {"cpus": 2, "memory": 4096}},
                "config": {"sim_name": "...", "steps": [...]}
            },
            "dev": {"world": "./worlds/my-world"},
            "skill_runner": {
                "image": "...",
                "runtime": {"type": "vm", "vm": {"cpus": 2, "memory": 4096}},
                "config": {...}
            }
        }
    """

    tags: list[str] = Field(default_factory=list)
    world: WorldConfig
    dev: DevConfig = Field(default_factory=DevConfig)
    session: SessionConfig = Field(default_factory=SessionConfig)

    model_config = {"extra": "allow"}

    @classmethod
    def from_file(cls, path: str | Path) -> Config:
        """Load and validate config from JSON file.

        Automatically loads a .env file co-located with the config file before
        performing variable substitution.
        """
        path = Path(path).expanduser().resolve()

        # Load .env file next to the config (if any) so ${VAR} substitution works
        from dotenv import load_dotenv

        env_path = path.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path, override=True)

        with open(path) as f:
            raw = f.read()

        # Support `${VAR}` and `$VAR` substitution in configs (docs guarantee this).
        # Dev mode relies on this for agent secrets like `${ANTHROPIC_API_KEY}`.
        #
        # When the substituted value contains JSON (e.g. OAuth creds), raw
        # expansion would break the surrounding JSON because of unescaped
        # quotes.  We parse the raw JSON first, then walk string values and
        # expand vars there — keeping the result valid JSON.
        data = json.loads(raw)
        _expand_vars_recursive(data)
        return cls.model_validate(data)
