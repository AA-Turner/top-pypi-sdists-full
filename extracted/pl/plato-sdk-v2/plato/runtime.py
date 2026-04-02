"""Runtime configuration for Plato agents and worlds."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from plato.chronos.models import VMResources as VMResources  # noqa: F401


class VMRuntimeConfig(BaseModel):
    """VM runtime configuration with resource allocation."""

    type: Literal["vm"] = "vm"
    vm: VMResources = Field(default_factory=VMResources)


RuntimeConfig = VMRuntimeConfig
Runtime = Literal["vm"]
