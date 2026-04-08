"""Runtime configuration models and resolver.

Configs are discriminated on the ``type`` field so a single JSON/dict
can be deserialized into the right config, and ``create_runtime`` turns
any config into a running ``Runtime`` instance.

Example JSON::

    {"type": "vm", "image": "383806609161.dkr.ecr...", "cpus": 4, "memory": 8192}
    {"type": "apple", "image": "ubuntu:latest", "cpus": 4, "memory": "4G"}
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field


class VMRuntimeConfig(BaseModel):
    """Config for Plato VM runtime."""

    type: Literal["vm"] = "vm"
    image: str = ""
    cpus: int = 2
    memory: int = 4096
    disk: int = 10240
    timeout: int = 7200
    heartbeat_timeout: int | None = None


class AppleRuntimeConfig(BaseModel):
    """Config for Apple Virtualization.framework container runtime."""

    type: Literal["apple"] = "apple"
    image: str = "ubuntu:latest"
    cpus: int = 4
    memory: str = "4G"
    server_url: str


RuntimeConfig = Annotated[
    VMRuntimeConfig | AppleRuntimeConfig,
    Field(discriminator="type"),
]
