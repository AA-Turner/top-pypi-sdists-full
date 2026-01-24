"""IATP client module for A2A integration with lazy loading."""

from typing import TYPE_CHECKING

# Type hints for IDEs and type checkers (not loaded at runtime)
if TYPE_CHECKING:
    from .a2a_client import UtilityAgencyTool, create_utility_agency_tools
    from .crewai_a2a_tools import A2AToolSchema

# Lazy imports to avoid loading CrewAI unless needed
_LAZY_IMPORTS = {
    "UtilityAgencyTool": ".a2a_client",
    "create_utility_agency_tools": ".a2a_client",
    "A2AToolSchema": ".crewai_a2a_tools",
}

__all__ = [
    "UtilityAgencyTool",
    "create_utility_agency_tools", 
    "A2AToolSchema",
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
