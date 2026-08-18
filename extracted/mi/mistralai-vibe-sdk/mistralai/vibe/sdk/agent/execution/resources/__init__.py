"""Execution-scoped resources."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "LOCAL",
    "SHARED",
    "AcquiredResource",
    "CompatibilityMetadata",
    "Finalizer",
    "NoCurrentScopeError",
    "ResourceDefinition",
    "ResourceDescriptor",
    "ResourceKeyConflictError",
    "ResourceRegistry",
    "ResourceSharing",
    "ResourceSharingConflictError",
    "ResourcesScope",
    "ScopeClosedError",
    "bind_execution_scope",
    "current_execution_scope",
    "spawn_child_scope",
    "stop_execution_scope",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.agent.execution.resources.context import (
        bind_execution_scope,
        current_execution_scope,
        spawn_child_scope,
        stop_execution_scope,
    )
    from mistralai.vibe.sdk.agent.execution.resources.errors import (
        NoCurrentScopeError,
        ResourceKeyConflictError,
        ResourceSharingConflictError,
        ScopeClosedError,
    )
    from mistralai.vibe.sdk.agent.execution.resources.registry import (
        ResourceDescriptor,
        ResourceRegistry,
    )
    from mistralai.vibe.sdk.agent.execution.resources.scope import ResourcesScope
    from mistralai.vibe.sdk.agent.execution.resources.types import (
        LOCAL,
        SHARED,
        AcquiredResource,
        CompatibilityMetadata,
        Finalizer,
        ResourceDefinition,
        ResourceSharing,
    )

_LAZY_EXPORTS = {
    "AcquiredResource": "mistralai.vibe.sdk.agent.execution.resources.types",
    "CompatibilityMetadata": "mistralai.vibe.sdk.agent.execution.resources.types",
    "Finalizer": "mistralai.vibe.sdk.agent.execution.resources.types",
    "LOCAL": "mistralai.vibe.sdk.agent.execution.resources.types",
    "NoCurrentScopeError": "mistralai.vibe.sdk.agent.execution.resources.errors",
    "ResourceDefinition": "mistralai.vibe.sdk.agent.execution.resources.types",
    "ResourceDescriptor": "mistralai.vibe.sdk.agent.execution.resources.registry",
    "ResourceKeyConflictError": "mistralai.vibe.sdk.agent.execution.resources.errors",
    "ResourceRegistry": "mistralai.vibe.sdk.agent.execution.resources.registry",
    "ResourceSharingConflictError": "mistralai.vibe.sdk.agent.execution.resources.errors",
    "ResourceSharing": "mistralai.vibe.sdk.agent.execution.resources.types",
    "ResourcesScope": "mistralai.vibe.sdk.agent.execution.resources.scope",
    "SHARED": "mistralai.vibe.sdk.agent.execution.resources.types",
    "ScopeClosedError": "mistralai.vibe.sdk.agent.execution.resources.errors",
    "bind_execution_scope": "mistralai.vibe.sdk.agent.execution.resources.context",
    "current_execution_scope": "mistralai.vibe.sdk.agent.execution.resources.context",
    "spawn_child_scope": "mistralai.vibe.sdk.agent.execution.resources.context",
    "stop_execution_scope": "mistralai.vibe.sdk.agent.execution.resources.context",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
