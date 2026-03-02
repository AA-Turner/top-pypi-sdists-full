"""Team Registry module.

Provides team-level storage for:
- Rules: Prompt rules/guidelines for agent conversations
- Agents: Pre-configured agent configurations
- MCPs: MCP (Model Context Protocol) server configurations
- Skills: Custom capabilities/prompt templates
"""

from .manager import RegistryManager
from .models import (
    AgentConfig,
    MCPConfig,
    RegistryItemType,
    Rule,
    Skill,
    TeamRegistry,
)

__all__ = [
    "AgentConfig",
    "MCPConfig",
    "RegistryItemType",
    "RegistryManager",
    "Rule",
    "Skill",
    "TeamRegistry",
]
