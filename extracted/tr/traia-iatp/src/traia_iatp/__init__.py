"""Traia IATP - Inter Agent Transfer Protocol package with lazy loading for performance."""

from typing import TYPE_CHECKING

# Read version from package metadata
def _get_version():
    """Read version from installed package metadata."""
    try:
        # Try importlib.metadata first (works for installed packages)
        from importlib.metadata import version
        return version("traia-iatp")
    except Exception:
        # Fallback: try reading from pyproject.toml (for development)
        try:
            import tomli
            from pathlib import Path
            pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
            with open(pyproject_path, "rb") as f:
                pyproject = tomli.load(f)
            return pyproject["project"]["version"]
        except Exception:
            # Last resort - return unknown instead of hardcoded old version
            return "unknown"

__version__ = _get_version()

# Type hints for IDEs and type checkers (not loaded at runtime)
if TYPE_CHECKING:
    from .core.models import UtilityAgent, MCPServer, AgentCard
    from .server.iatp_server_agent_generator import IATPServerAgentGenerator
    from .registry.mongodb_registry import UtilityAgentRegistry, MCPServerRegistry
    from .registry.iatp_search_api import find_utility_agent
    from .client.a2a_client import UtilityAgencyTool, create_utility_agency_tools
    from .utils.docker_utils import LocalDockerRunner, run_generated_agent_locally, use_run_local_docker_script
    from .d402 import (
        D402Config,
        D402PaymentInfo,
        D402ServicePrice,
        PaymentScheme,
        D402IATPClient,
        IATPSettlementFacilitator,
        require_payment,
    )
    from .client.d402_a2a_client import D402A2AClient, create_d402_a2a_client

# Lazy imports - these will only load when accessed
_LAZY_IMPORTS = {
    # Core models (lightweight)
    "UtilityAgent": ".core.models",
    "MCPServer": ".core.models",
    "AgentCard": ".core.models",
    # Server components
    "IATPServerAgentGenerator": ".server.iatp_server_agent_generator",
    # Registry (lightweight, no CrewAI dependency)
    "UtilityAgentRegistry": ".registry.mongodb_registry",
    "MCPServerRegistry": ".registry.mongodb_registry",
    "find_utility_agent": ".registry.iatp_search_api",
    # Client (HEAVY - imports CrewAI)
    "UtilityAgencyTool": ".client.a2a_client",
    "create_utility_agency_tools": ".client.a2a_client",
    # Docker utilities
    "LocalDockerRunner": ".utils.docker_utils",
    "run_generated_agent_locally": ".utils.docker_utils",
    "use_run_local_docker_script": ".utils.docker_utils",
    # D402 payment integration (HEAVY - imports CrewAI indirectly)
    "D402A2AClient": ".client.d402_a2a_client",
    "create_d402_a2a_client": ".client.d402_a2a_client",
}

# D402 imports need special handling as they come from a submodule
_D402_IMPORTS = [
    "D402Config",
    "D402PaymentInfo",
    "D402ServicePrice",
    "PaymentScheme",
    "D402IATPClient",
    "IATPSettlementFacilitator",
    "require_payment",
]

__all__ = [
    # Core models
    "UtilityAgent",
    "MCPServer", 
    "AgentCard",
    # Server components
    "IATPServerAgentGenerator",
    # Registry
    "UtilityAgentRegistry",
    "MCPServerRegistry",
    "find_utility_agent",
    # Client
    "UtilityAgencyTool",
    "create_utility_agency_tools",
    # Docker utilities
    "LocalDockerRunner",
    "run_generated_agent_locally",
    "use_run_local_docker_script",
    # D402 payment integration
    "D402Config",
    "D402PaymentInfo",
    "D402ServicePrice",
    "PaymentScheme",
    "D402IATPClient",
    "IATPSettlementFacilitator",
    "require_payment",
    "D402A2AClient",
    "create_d402_a2a_client",
]


def __getattr__(name: str):
    """Lazy import mechanism to load modules only when accessed."""
    # Handle regular lazy imports
    if name in _LAZY_IMPORTS:
        from importlib import import_module
        module_path = _LAZY_IMPORTS[name]
        module = import_module(module_path, package=__package__)
        attr = getattr(module, name)
        # Cache the imported attribute
        globals()[name] = attr
        return attr
    
    # Handle D402 imports
    if name in _D402_IMPORTS:
        from importlib import import_module
        d402_module = import_module(".d402", package=__package__)
        attr = getattr(d402_module, name)
        # Cache the imported attribute
        globals()[name] = attr
        return attr
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
