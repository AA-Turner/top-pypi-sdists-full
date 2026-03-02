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
                "runtime": {"type": "docker"},
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
        """Load and validate config from JSON file."""
        path = Path(path).expanduser().resolve()
        with open(path) as f:
            # Support `${VAR}` and `$VAR` substitution in configs (docs guarantee this).
            # Dev mode relies on this for agent secrets like `${ANTHROPIC_API_KEY}`.
            config_text = os.path.expandvars(f.read())
        return cls.model_validate(json.loads(config_text))
