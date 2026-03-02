"""Runtime configuration for Plato agents and worlds.

Defines execution environments (Docker containers or Firecracker VMs)
and resource allocation for VMs.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from plato.chronos.models import VMResources as VMResources  # noqa: F401


class DockerRuntimeConfig(BaseModel):
    """Docker runtime configuration."""

    type: Literal["docker"] = "docker"


class VMRuntimeConfig(BaseModel):
    """VM runtime configuration with resource allocation."""

    type: Literal["vm"] = "vm"
    vm: VMResources = Field(default_factory=VMResources)


# Discriminated union for runtime config
RuntimeConfig = Annotated[DockerRuntimeConfig | VMRuntimeConfig, Field(discriminator="type")]

# Runtime environment type
Runtime = Literal["docker", "vm"]
