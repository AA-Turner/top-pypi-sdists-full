"""Toolkit registry for sub-agents.

Provides specialized toolkits for different agent types.
Each toolkit contains a curated set of tools appropriate for the agent's purpose.

Custom agents from .emdash/agents/*.md are also supported and use the Explore toolkit
by default (unless they specify different tools in their frontmatter).

Simple two-layer model:
- Main agent can spawn Explore, Plan, Coder sub-agents
- Sub-agents cannot spawn further (they don't have the task tool)
"""

from pathlib import Path
from typing import TYPE_CHECKING, Dict, Optional

if TYPE_CHECKING:
    from .base import BaseToolkit

# Registry for easy extension - just add new toolkits here
# Imported lazily to avoid circular imports
TOOLKIT_REGISTRY: Dict[str, str] = {
    # Coding sub-agents (used by CodingMainAgent)
    "Explore": "emdash_core.agent.toolkits.explore:ExploreToolkit",
    "Plan": "emdash_core.agent.toolkits.plan:PlanToolkit",
    "Coder": "emdash_core.agent.toolkits.coder:CoderToolkit",

    # Coworker sub-agents (used by CoworkerAgent)
    "Researcher": "emdash_core.agent.toolkits.researcher:ResearcherToolkit",
    "GeneralPlanner": "emdash_core.agent.toolkits.general_planner:GeneralPlannerToolkit",
}


def _get_custom_agents(repo_root: Optional[Path] = None) -> dict:
    """Load custom agents from .emdash/agents/ directory.

    Args:
        repo_root: Repository root (defaults to cwd)

    Returns:
        Dict mapping agent name to CustomAgent
    """
    from ..agents import load_agents
    from ...utils.logger import log

    agents_dir = (repo_root or Path.cwd()) / ".emdash" / "agents"
    log.debug(f"Loading custom agents from: {agents_dir} (exists={agents_dir.exists()})")
    agents = load_agents(agents_dir)
    log.debug(f"Loaded custom agents: {list(agents.keys())}")
    return agents


def get_toolkit(
    subagent_type: str,
    repo_root: Path,
) -> "BaseToolkit":
    """Get toolkit for agent type.

    Args:
        subagent_type: Type of agent (e.g., "Explore", "Plan", "Coder", or custom agent name)
        repo_root: Root directory of the repository

    Returns:
        Toolkit instance

    Raises:
        ValueError: If agent type is not registered or found
    """
    # Check built-in agents first
    if subagent_type in TOOLKIT_REGISTRY:
        import importlib
        module_path, class_name = TOOLKIT_REGISTRY[subagent_type].rsplit(":", 1)
        module = importlib.import_module(module_path)
        toolkit_class = getattr(module, class_name)
        return toolkit_class(repo_root)

    # Check custom agents
    custom_agents = _get_custom_agents(repo_root)
    if subagent_type in custom_agents:
        # Custom agents use Explore toolkit by default (read-only, safe)
        # This gives them: glob, grep, read_file, list_files, semantic_search
        # Plus any MCP servers defined in the agent's frontmatter
        import importlib
        from ...utils.logger import log

        custom_agent = custom_agents[subagent_type]
        module_path, class_name = TOOLKIT_REGISTRY["Explore"].rsplit(":", 1)
        module = importlib.import_module(module_path)
        toolkit_class = getattr(module, class_name)

        # Pass MCP servers if defined
        mcp_servers = custom_agent.mcp_servers if custom_agent.mcp_servers else None
        if mcp_servers:
            log.info(f"Custom agent '{subagent_type}' has {len(mcp_servers)} MCP servers")

        return toolkit_class(repo_root, mcp_servers=mcp_servers)

    # Not found
    available = list_agent_types(repo_root)
    raise ValueError(
        f"Unknown agent type: {subagent_type}. Available: {available}"
    )


def list_agent_types(repo_root: Optional[Path] = None) -> list[str]:
    """List all available agent types (built-in + custom).

    Args:
        repo_root: Repository root for finding custom agents

    Returns:
        List of agent type names
    """
    # Start with built-in agents
    types = list(TOOLKIT_REGISTRY.keys())

    # Add custom agents
    custom_agents = _get_custom_agents(repo_root)
    for name in custom_agents.keys():
        if name not in types:
            types.append(name)

    return types


def get_agents_with_descriptions(repo_root: Optional[Path] = None) -> list[dict]:
    """Get all agents with their names and descriptions.

    Args:
        repo_root: Repository root for finding custom agents

    Returns:
        List of dicts with 'name' and 'description' keys
    """
    from ..prompts.subagents import BUILTIN_AGENTS

    agents = []

    # Built-in agents
    for name, description in BUILTIN_AGENTS.items():
        agents.append({"name": name, "description": description})

    # Custom agents
    custom_agents = _get_custom_agents(repo_root)
    for name, agent in custom_agents.items():
        agents.append({
            "name": name,
            "description": agent.description or "Custom agent"
        })

    return agents


def get_custom_agent(name: str, repo_root: Optional[Path] = None):
    """Get a specific custom agent by name.

    Args:
        name: Agent name
        repo_root: Repository root

    Returns:
        CustomAgent or None
    """
    custom_agents = _get_custom_agents(repo_root)
    return custom_agents.get(name)


__all__ = [
    "get_toolkit",
    "list_agent_types",
    "get_agents_with_descriptions",
    "get_custom_agent",
    "TOOLKIT_REGISTRY",
]
