"""The descriptor-to-definition boundary for execution resources.

A `ResourceDescriptor` is the serializable pointer persisted in
task configs and durable records, a `ResourceRegistry` resolves it to an
in-process `ResourceDefinition`.
"""

from typing import Protocol, runtime_checkable

from pydantic import BaseModel

from mistralai.vibe.sdk.agent.execution.resources.types import ResourceDefinition


class ResourceDescriptor(BaseModel):
    """Serializable pointer to a resource definition."""

    type: str  # Discriminator for concrete descriptors.


@runtime_checkable
class ResourceRegistry(Protocol):
    """Resolves a serializable descriptor into an in-process definition."""

    def resolve(self, descriptor: ResourceDescriptor) -> ResourceDefinition[object]: ...


__all__ = ["ResourceDescriptor", "ResourceRegistry"]
