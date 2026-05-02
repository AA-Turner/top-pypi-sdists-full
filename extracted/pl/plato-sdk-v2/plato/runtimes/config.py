"""Runtime configuration models and resolver.

Configs are discriminated on the ``type`` field so a single JSON/dict
can be deserialized into the right config, and ``create_runtime`` turns
any config into a running ``Runtime`` instance.

``VMRuntimeConfig`` mirrors the backend's ``WorldRuntimeConfig`` shape
(``runtime.vm.{cpus,memory,disk,timeout}`` under a ``type`` discriminator)
so the same JSON drives both ``LaunchJobRequest`` and a local ``VMRuntime``.

Example JSON::

    {"type": "vm", "image": "383806609161.dkr.ecr...", "vm": {"cpus": 4, "memory": 8192}}
    {"type": "apple", "image": "ubuntu:latest", "cpus": 4, "memory": "4G"}
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from plato.chronos.models import VMResources as _GeneratedVMResources
from plato.chronos.models import WorldRuntimeConfig as _WorldRuntimeConfig


class VMResources(_GeneratedVMResources):
    """Strict local override of the generated ``VMResources``.

    The generated model declares each field as ``int | None`` with a non-None
    default — an OpenAPI-spec artifact. Narrow the types so callers can use
    ``vm.cpus`` directly without static-checker noise about ``None``.
    """

    cpus: int = 2
    memory: int = 4096
    disk: int = 10240
    timeout: int = 7200


class VMRuntimeConfig(_WorldRuntimeConfig):
    """Local SDK runtime config for a Plato VM.

    Subclass of the generated ``WorldRuntimeConfig``: same nested
    ``vm: VMResources`` shape the backend's ``/launch`` endpoint accepts,
    plus a client-only ``image`` field. ``image`` is set separately in the
    launch path (resolved from ``world_schema.image`` server-side) and is
    populated for local ``VMRuntime`` use.
    """

    type: Literal["vm"] = "vm"
    vm: VMResources = Field(default_factory=VMResources)
    image: str = ""


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
