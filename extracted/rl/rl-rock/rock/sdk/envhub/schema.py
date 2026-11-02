"""
EnvHub data model definitions.
"""

from dataclasses import dataclass, field
from typing import Any

from rock import env_vars


@dataclass
class EnvHubClientConfig:
    """EnvHub configuration class."""

    base_url: str = env_vars.ROCK_ENVHUB_BASE_URL


@dataclass
class RockEnvInfo:
    """Environment information data class."""

    env_name: str
    image: str
    owner: str = ""
    create_at: str = ""
    update_at: str = ""
    description: str = ""
    tags: list[str] = field(default_factory=list)
    extra_spec: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert environment object to dictionary."""
        return {
            "env_name": self.env_name,
            "image": self.image,
            "owner": self.owner,
            "create_at": self.create_at,
            "update_at": self.update_at,
            "description": self.description,
            "tags": self.tags,
            "extra_spec": self.extra_spec,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RockEnvInfo":
        """Create environment object from dictionary."""
        return cls(**data)
