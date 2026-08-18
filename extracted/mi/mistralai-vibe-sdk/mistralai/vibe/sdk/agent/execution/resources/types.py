"""Type contracts for execution-scoped resources."""

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Protocol, TypeVar, runtime_checkable

if TYPE_CHECKING:
    from mistralai.vibe.sdk.agent.execution.resources.scope import ResourcesScope


CompatibilityMetadata = Mapping[str, str | int | float | bool | None]
"""Serializable metadata refining a resource key."""

ResourceSharing = Literal["shared", "local"]
"""Whether a resource may be reused by child scopes (``shared``) or must be
acquired separately in each scope (``local``)."""

SHARED: ResourceSharing = "shared"
LOCAL: ResourceSharing = "local"

Finalizer = Callable[[], Awaitable[None]]
"""Async cleanup for an owned resource, run once during scope close."""

T_co = TypeVar("T_co", covariant=True)


@dataclass(frozen=True)
class AcquiredResource[T]:
    """The representation of an instantiated resource and an optional finalizer."""

    value: T
    """The instantiated resource handed back to callers."""

    finalizer: Finalizer | None = None
    """Async cleanup for the resource, or ``None`` when it needs no teardown."""


@dataclass(frozen=True)
class ResourceBinding[T]:
    """A resolved resource cached in a scope."""

    key: str
    """The resource key this binding was resolved under."""

    compatibility: CompatibilityMetadata
    """The metadata snapshot the resource was resolved with."""

    sharing: ResourceSharing
    """The sharing policy the resource was resolved under; a later request for the
    same key with a different policy is rejected rather than silently reused."""

    value: T
    """The resolved resource value."""

    finalizer: Finalizer | None
    """Async cleanup for an owned resource, or ``None`` when unowned or teardown-free."""

    owned: bool
    """Whether this scope acquired the resource itself (and must finalize it), as
    opposed to reusing a ``shared`` resource owned by a parent scope."""

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("ResourceBinding.key must be a non-empty string")


@runtime_checkable
class ResourceDefinition(Protocol[T_co]):
    """In-process recipe for acquiring one execution-scoped resource."""

    @property
    def key(self) -> str: ...

    @property
    def sharing(self) -> ResourceSharing: ...

    @property
    def compatibility(self) -> CompatibilityMetadata: ...

    async def acquire(self, scope: "ResourcesScope") -> AcquiredResource[T_co]: ...


__all__ = [
    "LOCAL",
    "SHARED",
    "AcquiredResource",
    "CompatibilityMetadata",
    "Finalizer",
    "ResourceBinding",
    "ResourceDefinition",
    "ResourceSharing",
]
