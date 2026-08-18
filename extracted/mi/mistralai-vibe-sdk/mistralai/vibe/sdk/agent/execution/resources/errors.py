"""Failure contracts for execution-scoped resources."""

from mistralai.vibe.sdk.agent.execution.resources.types import (
    CompatibilityMetadata,
    ResourceSharing,
)


class ResourceKeyConflictError(RuntimeError):
    """Raised when a resource key is requested with incompatible metadata."""

    def __init__(
        self,
        *,
        key: str,
        existing: CompatibilityMetadata,
        requested: CompatibilityMetadata,
    ) -> None:
        self.key = key
        self.existing = existing
        self.requested = requested
        super().__init__(
            f"resource key {key!r} already resolved with incompatible metadata "
            f"(existing={dict(existing)!r}, requested={dict(requested)!r})"
        )


class ResourceSharingConflictError(RuntimeError):
    """Raised when a resource key is requested with a different sharing policy."""

    def __init__(
        self,
        *,
        key: str,
        existing: ResourceSharing,
        requested: ResourceSharing,
    ) -> None:
        self.key = key
        self.existing = existing
        self.requested = requested
        super().__init__(
            f"resource key {key!r} already resolved with sharing {existing!r} "
            f"but requested {requested!r}"
        )


class ScopeClosedError(RuntimeError):
    """Raised when a resource is requested from a scope that is closing or closed."""

    def __init__(self, *, key: str | None = None) -> None:
        self.key = key
        detail = f" for key {key!r}" if key is not None else ""
        super().__init__(f"resources scope is closed{detail}")


class NoCurrentScopeError(RuntimeError):
    """Raised when the current execution scope is requested outside a binding."""

    def __init__(self) -> None:
        super().__init__(
            "no current execution scope is bound; wrap the call in bind_execution_scope(...)"
        )


__all__ = [
    "NoCurrentScopeError",
    "ResourceKeyConflictError",
    "ResourceSharingConflictError",
    "ScopeClosedError",
]
