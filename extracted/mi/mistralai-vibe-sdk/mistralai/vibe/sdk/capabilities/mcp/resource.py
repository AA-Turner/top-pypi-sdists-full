"""Execution-scoped resource definition for MCP server connections."""

from dataclasses import dataclass

from mistralai.vibe.sdk.agent.execution.resources.scope import ResourcesScope
from mistralai.vibe.sdk.agent.execution.resources.types import (
    SHARED,
    AcquiredResource,
    CompatibilityMetadata,
    ResourceSharing,
)
from mistralai.vibe.sdk.capabilities.mcp.config import McpConfigBase
from mistralai.vibe.sdk.capabilities.mcp.port import McpPort

__all__ = [
    "McpResourceDefinition",
]


@dataclass(frozen=True)
class McpResourceDefinition:
    """Acquire and share one MCP server connection within an execution scope."""

    config: McpConfigBase

    @property
    def key(self) -> str:
        return self.config.server_key

    @property
    def sharing(self) -> ResourceSharing:
        return SHARED

    @property
    def compatibility(self) -> CompatibilityMetadata:
        # The key already encodes the full config, no extra metadata is needed.
        return {}

    async def acquire(self, scope: ResourcesScope) -> AcquiredResource[McpPort]:
        adapter = self.config.create_adapter()

        await adapter.setup()

        return AcquiredResource(value=adapter, finalizer=adapter.teardown)
