"""Immutable atomic training checkpoint identities."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from labqoat.references.resource_id import ResourceId
from labqoat.references.sha256 import Sha256

ArtifactT = TypeVar("ArtifactT", covariant=True)


@dataclass(frozen=True, slots=True, kw_only=True)
class CheckpointRef(Generic[ArtifactT]):
    """A completed training step and its immutable captured checkpoint manifest digest."""

    id: ResourceId
    run_id: ResourceId
    step: int
    manifest_sha256: Sha256

    def __post_init__(self) -> None:
        """Reject negative or noninteger checkpoint steps without boolean coercion."""
        if type(self.step) is not int or self.step < 0:
            raise ValueError("Checkpoint step must be a nonnegative integer")
