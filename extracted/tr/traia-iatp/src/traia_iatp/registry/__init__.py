"""IATP registry module for managing utility agents and MCP servers with lazy loading."""

from typing import TYPE_CHECKING

# Type hints for IDEs and type checkers (not loaded at runtime)
if TYPE_CHECKING:
    from .mongodb_registry import UtilityAgentRegistry, MCPServerRegistry
    from .iatp_search_api import (
        find_utility_agent, 
        list_utility_agents, 
        search_utility_agents,
        find_mcp_server,
        list_mcp_servers,
        search_mcp_servers,
        get_mcp_server
    )
    from .embeddings import get_embedding_service

# Lazy imports to avoid loading heavy dependencies (OpenAI, Cohere, etc.) unless needed
_LAZY_IMPORTS = {
    # Registry classes (write operations)
    "UtilityAgentRegistry": ".mongodb_registry",
    "MCPServerRegistry": ".mongodb_registry",
    # Search API functions (lightweight, no heavy deps)
    "find_utility_agent": ".iatp_search_api",
    "list_utility_agents": ".iatp_search_api",
    "search_utility_agents": ".iatp_search_api",
    "find_mcp_server": ".iatp_search_api",
    "list_mcp_servers": ".iatp_search_api",
    "search_mcp_servers": ".iatp_search_api",
    "get_mcp_server": ".iatp_search_api",
    # Embedding service (HEAVY - OpenAI/Cohere, only load if vector search is used)
    "get_embedding_service": ".embeddings",
}

__all__ = [
    "UtilityAgentRegistry",
    "MCPServerRegistry",
    "find_utility_agent",
    "list_utility_agents", 
    "search_utility_agents",
    "find_mcp_server",
    "list_mcp_servers",
    "search_mcp_servers", 
    "get_mcp_server",
    "get_embedding_service",
]


def __getattr__(name: str):
    """Lazy import mechanism to load modules only when accessed."""
    if name in _LAZY_IMPORTS:
        from importlib import import_module
        module_path = _LAZY_IMPORTS[name]
        module = import_module(module_path, package=__package__)
        attr = getattr(module, name)
        # Cache the imported attribute
        globals()[name] = attr
        return attr
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
