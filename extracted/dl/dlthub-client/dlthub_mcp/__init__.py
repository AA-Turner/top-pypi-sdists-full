"""dltHub platform tools, contributed to dlt's MCP server.

The tools are plain callables over :mod:`dlthub_sdk`; the MCP runtime belongs to
whichever server registers them, so nothing here imports ``fastmcp``. dlt
broadcasts the requested feature names to every installed plugin, so installing
``dlthub-client`` is what makes these reachable::

    dlthub ai mcp run --stdio --features=+dlthub.jobs,+dlthub.logs

Import-light on purpose: the plugin hooks call the ``*_features`` functions
while the CLI parser is still being built, and the SDK must not be imported
until a tool actually runs.
"""

from __future__ import annotations

# Python internals
from typing import Optional, Set

# Other libraries
from dlt._workspace._plugins import McpFeatures

#: Feature names that turn each group on. The bare alias is accepted too, since
#: dlt's own features are unprefixed.
JOBS_FEATURE = "dlthub.jobs"
LOGS_FEATURE = "dlthub.logs"
CONFIG_FEATURE = "dlthub.config"
TELEMETRY_FEATURE = "dlthub.telemetry"

_JOBS_TOKENS = frozenset({JOBS_FEATURE, "jobs"})
_LOGS_TOKENS = frozenset({LOGS_FEATURE, "logs"})
_CONFIG_TOKENS = frozenset({CONFIG_FEATURE, "config"})
_TELEMETRY_TOKENS = frozenset({TELEMETRY_FEATURE, "telemetry"})


def jobs_features(requested: Set[str]) -> Optional[McpFeatures]:
    """Return the orientation, job and run tools when the caller asked for them.

    The orientation tools ride here rather than in a group of their own: dlt
    owns the bare alias ``workspace``, so a ``dlthub.workspace`` group would
    fire both hookimpls and register both tool sets.

    Args:
        requested: Feature names the MCP server is assembling.

    Returns:
        The feature, or ``None`` when it was not requested.
    """
    if not _JOBS_TOKENS & requested:
        return None
    # Current package
    from dlthub_mcp import jobs_tools, workspace_tools

    return McpFeatures(
        name=JOBS_FEATURE,
        tools=[*workspace_tools.__tools__, *jobs_tools.__tools__],
    )


def logs_features(requested: Set[str]) -> Optional[McpFeatures]:
    """Return the run log tools when the caller asked for them.

    Args:
        requested: Feature names the MCP server is assembling.

    Returns:
        The feature, or ``None`` when it was not requested.
    """
    if not _LOGS_TOKENS & requested:
        return None
    # Current package
    from dlthub_mcp import logs_tools

    return McpFeatures(name=LOGS_FEATURE, tools=list(logs_tools.__tools__))


def config_features(requested: Set[str]) -> Optional[McpFeatures]:
    """Return the variable and configuration tools when the caller asked for them.

    Args:
        requested: Feature names the MCP server is assembling.

    Returns:
        The feature, or ``None`` when it was not requested.
    """
    if not _CONFIG_TOKENS & requested:
        return None
    # Current package
    from dlthub_mcp import config_tools

    return McpFeatures(name=CONFIG_FEATURE, tools=list(config_tools.__tools__))


def telemetry_features(requested: Set[str]) -> Optional[McpFeatures]:
    """Return the telemetry tools when the caller asked for them.

    Args:
        requested: Feature names the MCP server is assembling.

    Returns:
        The feature, or ``None`` when it was not requested.
    """
    if not _TELEMETRY_TOKENS & requested:
        return None
    # Current package
    from dlthub_mcp import telemetry_tools

    return McpFeatures(name=TELEMETRY_FEATURE, tools=list(telemetry_tools.__tools__))


__all__ = [
    "CONFIG_FEATURE",
    "JOBS_FEATURE",
    "LOGS_FEATURE",
    "TELEMETRY_FEATURE",
    "McpFeatures",
    "config_features",
    "jobs_features",
    "logs_features",
    "telemetry_features",
]
