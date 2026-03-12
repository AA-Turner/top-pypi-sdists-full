"""Configuration models for `plato chronos test`."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator

from plato.cli.chronos.config import WorldConfig, _expand_vars_recursive
from plato.worlds.config import DevConfig, SessionConfig


class TestPhaseConfig(BaseModel):
    """One test phase command executed on the VM."""

    name: str = Field(description="Phase name (for logs and filtering)")
    command: str = Field(description="Shell command to execute on the VM")
    junit_path: str | None = Field(
        default=None,
        description="Optional remote junit XML path to fetch after phase",
    )


class TestRunnerConfig(BaseModel):
    """Settings for running tests in a synced world VM."""

    workdir: str = Field(default="/world", description="VM working directory")
    env: dict[str, str] = Field(
        default_factory=dict,
        description="Extra environment variables to export before test commands",
    )
    pass_env: list[str] = Field(
        default_factory=list,
        description="Host env variable names to forward when present",
    )
    phases: list[TestPhaseConfig] = Field(
        default_factory=lambda: [
            TestPhaseConfig(
                name="integration",
                command="uv run pytest tests/integration -vv -s",
                junit_path="/tmp/pytest-integration.xml",
            ),
        ],
        description="Ordered test phases",
    )

    @model_validator(mode="after")
    def _validate_phases(self) -> TestRunnerConfig:
        if not self.phases:
            raise ValueError("test.phases must include at least one phase")

        seen: set[str] = set()
        for phase in self.phases:
            phase_name = phase.name.strip().lower()
            if not phase_name:
                raise ValueError("test phase name must be non-empty")
            if phase_name in seen:
                raise ValueError(f"duplicate test phase name: {phase.name}")
            seen.add(phase_name)
        return self


class TestConfig(BaseModel):
    """Standalone config for `plato chronos test`."""

    tags: list[str] = Field(default_factory=list)
    world: WorldConfig
    dev: DevConfig = Field(default_factory=DevConfig)
    session: SessionConfig = Field(default_factory=SessionConfig)
    test: TestRunnerConfig = Field(default_factory=TestRunnerConfig)

    model_config = {"extra": "allow"}

    @classmethod
    def from_file(cls, path: str | Path) -> TestConfig:
        """Load and validate a `chronos test` JSON config file."""
        path = Path(path).expanduser().resolve()

        from dotenv import load_dotenv

        env_path = path.parent / ".env"
        if env_path.exists():
            load_dotenv(env_path, override=True)

        with open(path) as f:
            raw = f.read()

        data: dict[str, Any] = json.loads(raw)
        _expand_vars_recursive(data)

        # Allow single-purpose files with top-level world/dev/session/test only.
        # Strip `dev` config from launch payloads if someone reuses this file.
        data.pop("allow_prerelease", None)
        return cls.model_validate(data)


TestPhaseConfig.__test__ = False
TestRunnerConfig.__test__ = False
TestConfig.__test__ = False


__all__ = [
    "TestConfig",
    "TestPhaseConfig",
    "TestRunnerConfig",
]
