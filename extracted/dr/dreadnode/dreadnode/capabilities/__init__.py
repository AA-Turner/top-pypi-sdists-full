"""
Dreadnode capabilities.

Load capability directories that extend agent functionality with agents, tools,
skills, and MCP servers.
"""

from dreadnode.capabilities.capability import Capability, DiscoverResult
from dreadnode.capabilities.loader import (
    get_default_capabilities_dir,
    list_capabilities,
    load_capabilities,
    load_capabilities_from_search_paths,
    load_capability,
    merge_capabilities,
    resolve_search_paths,
)
from dreadnode.capabilities.sync import CapabilitySyncClient, SyncError, SyncResult
from dreadnode.capabilities.types import (
    AgentDef,
    AgentLinkDef,
    LoadFailure,
    LoadOptions,
    LoadResult,
    MCPServerDef,
)
from dreadnode.capabilities.worker import Worker
from dreadnode.packaging.manifest import CapabilityManifest

__all__ = [
    "AgentDef",
    "AgentLinkDef",
    "Capability",
    "CapabilityManifest",
    "CapabilitySyncClient",
    "DiscoverResult",
    "LoadFailure",
    "LoadOptions",
    "LoadResult",
    "MCPServerDef",
    "SyncError",
    "SyncResult",
    "Worker",
    "get_default_capabilities_dir",
    "list_capabilities",
    "load_capabilities",
    "load_capabilities_from_search_paths",
    "load_capability",
    "merge_capabilities",
    "resolve_search_paths",
]
