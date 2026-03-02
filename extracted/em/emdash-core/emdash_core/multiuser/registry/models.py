"""Data models for Team Registry.

The Team Registry stores team-level configuration:
- Rules: Prompt rules/guidelines applied to agent conversations
- Agents: Pre-configured agent configurations
- MCPs: MCP (Model Context Protocol) server configurations
- Skills: Custom capabilities/prompt templates

These are stored at the team level and synced to local storage.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class RegistryItemType(str, Enum):
    """Types of items in the registry."""
    RULE = "rule"
    AGENT = "agent"
    MCP = "mcp"
    SKILL = "skill"


@dataclass
class Rule:
    """A prompt rule/guideline for agent conversations.

    Rules are applied to agent system prompts to customize behavior.
    They can be enabled/disabled and have priority ordering.

    Attributes:
        rule_id: Unique identifier
        name: Human-readable name
        content: The rule text (prompt content)
        description: Optional description of what the rule does
        enabled: Whether the rule is active
        priority: Order of application (higher = applied first)
        tags: Optional tags for categorization
        created_at: Creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the rule
    """
    rule_id: str
    name: str
    content: str
    description: str = ""
    enabled: bool = True
    priority: int = 0
    tags: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    created_by: str = ""

    def __post_init__(self):
        if not self.rule_id:
            self.rule_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "content": self.content,
            "description": self.description,
            "enabled": self.enabled,
            "priority": self.priority,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Rule":
        return cls(
            rule_id=data.get("rule_id", ""),
            name=data.get("name", ""),
            content=data.get("content", ""),
            description=data.get("description", ""),
            enabled=data.get("enabled", True),
            priority=data.get("priority", 0),
            tags=data.get("tags", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            created_by=data.get("created_by", ""),
        )


@dataclass
class AgentConfig:
    """Configuration for a pre-defined agent.

    Agents can be configured with specific models, system prompts,
    tools, and settings. Team members can quickly start sessions
    with these pre-configured agents.

    Attributes:
        agent_id: Unique identifier
        name: Human-readable name
        description: What this agent is for
        model: LLM model identifier (e.g., "claude-3-opus")
        system_prompt: Custom system prompt
        tools: List of enabled tool names
        settings: Additional agent settings
        enabled: Whether this agent config is active
        created_at: Creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the config
    """
    agent_id: str
    name: str
    description: str = ""
    model: str = ""
    system_prompt: str = ""
    tools: list[str] = field(default_factory=list)
    settings: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    created_at: str = ""
    updated_at: str = ""
    created_by: str = ""

    def __post_init__(self):
        if not self.agent_id:
            self.agent_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "system_prompt": self.system_prompt,
            "tools": self.tools,
            "settings": self.settings,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentConfig":
        return cls(
            agent_id=data.get("agent_id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            model=data.get("model", ""),
            system_prompt=data.get("system_prompt", ""),
            tools=data.get("tools", []),
            settings=data.get("settings", {}),
            enabled=data.get("enabled", True),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            created_by=data.get("created_by", ""),
        )


@dataclass
class MCPConfig:
    """Configuration for an MCP (Model Context Protocol) server.

    MCP servers provide additional tools and capabilities to agents.
    This config stores how to launch and configure an MCP server.

    Attributes:
        mcp_id: Unique identifier
        name: Human-readable name
        description: What this MCP server provides
        command: Command to launch the server (e.g., "npx")
        args: Command arguments (e.g., ["-y", "@anthropic/mcp-server-fetch"])
        env: Environment variables for the server
        enabled: Whether this MCP is active
        auto_start: Whether to start automatically with sessions
        created_at: Creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the config
    """
    mcp_id: str
    name: str
    description: str = ""
    command: str = ""
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    enabled: bool = True
    auto_start: bool = False
    created_at: str = ""
    updated_at: str = ""
    created_by: str = ""

    def __post_init__(self):
        if not self.mcp_id:
            self.mcp_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

    def to_dict(self) -> dict[str, Any]:
        return {
            "mcp_id": self.mcp_id,
            "name": self.name,
            "description": self.description,
            "command": self.command,
            "args": self.args,
            "env": self.env,
            "enabled": self.enabled,
            "auto_start": self.auto_start,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MCPConfig":
        return cls(
            mcp_id=data.get("mcp_id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            command=data.get("command", ""),
            args=data.get("args", []),
            env=data.get("env", {}),
            enabled=data.get("enabled", True),
            auto_start=data.get("auto_start", False),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            created_by=data.get("created_by", ""),
        )


@dataclass
class Skill:
    """A custom skill/capability with prompt templates.

    Skills are reusable prompt templates that can be invoked
    with variables. They help standardize common operations.

    Attributes:
        skill_id: Unique identifier
        name: Human-readable name (used to invoke)
        description: What this skill does
        prompt_template: Template with {{variable}} placeholders
        variables: List of variable names used in template
        examples: Example usages with inputs/outputs
        tags: Optional tags for categorization
        enabled: Whether this skill is active
        created_at: Creation timestamp
        updated_at: Last update timestamp
        created_by: User ID who created the skill
    """
    skill_id: str
    name: str
    description: str = ""
    prompt_template: str = ""
    variables: list[str] = field(default_factory=list)
    examples: list[dict[str, Any]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    enabled: bool = True
    created_at: str = ""
    updated_at: str = ""
    created_by: str = ""

    def __post_init__(self):
        if not self.skill_id:
            self.skill_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
        # Auto-extract variables from template if not provided
        if not self.variables and self.prompt_template:
            import re
            self.variables = list(set(re.findall(r'\{\{(\w+)\}\}', self.prompt_template)))

    def render(self, **kwargs) -> str:
        """Render the prompt template with provided variables."""
        result = self.prompt_template
        for key, value in kwargs.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "prompt_template": self.prompt_template,
            "variables": self.variables,
            "examples": self.examples,
            "tags": self.tags,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "created_by": self.created_by,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Skill":
        return cls(
            skill_id=data.get("skill_id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            prompt_template=data.get("prompt_template", ""),
            variables=data.get("variables", []),
            examples=data.get("examples", []),
            tags=data.get("tags", []),
            enabled=data.get("enabled", True),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
            created_by=data.get("created_by", ""),
        )


@dataclass
class TeamRegistry:
    """The complete registry for a team.

    Contains all rules, agents, MCPs, and skills configured
    for the team. This is synced between Firebase and local storage.

    Attributes:
        team_id: Team this registry belongs to
        rules: List of prompt rules
        agents: List of agent configurations
        mcps: List of MCP server configurations
        skills: List of skills
        updated_at: Last update timestamp
        version: Registry version for sync conflict detection
    """
    team_id: str
    rules: list[Rule] = field(default_factory=list)
    agents: list[AgentConfig] = field(default_factory=list)
    mcps: list[MCPConfig] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)
    updated_at: str = ""
    version: int = 1

    def __post_init__(self):
        if not self.updated_at:
            self.updated_at = datetime.utcnow().isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "team_id": self.team_id,
            "rules": [r.to_dict() for r in self.rules],
            "agents": [a.to_dict() for a in self.agents],
            "mcps": [m.to_dict() for m in self.mcps],
            "skills": [s.to_dict() for s in self.skills],
            "updated_at": self.updated_at,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TeamRegistry":
        return cls(
            team_id=data.get("team_id", ""),
            rules=[Rule.from_dict(r) for r in data.get("rules", [])],
            agents=[AgentConfig.from_dict(a) for a in data.get("agents", [])],
            mcps=[MCPConfig.from_dict(m) for m in data.get("mcps", [])],
            skills=[Skill.from_dict(s) for s in data.get("skills", [])],
            updated_at=data.get("updated_at", ""),
            version=data.get("version", 1),
        )

    # ─────────────────────────────────────────────────────────────
    # Query methods
    # ─────────────────────────────────────────────────────────────

    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """Get a rule by ID."""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None

    def get_rule_by_name(self, name: str) -> Optional[Rule]:
        """Get a rule by name (case-insensitive)."""
        name_lower = name.lower()
        for rule in self.rules:
            if rule.name.lower() == name_lower:
                return rule
        return None

    def get_enabled_rules(self) -> list[Rule]:
        """Get all enabled rules, sorted by priority (descending)."""
        return sorted(
            [r for r in self.rules if r.enabled],
            key=lambda r: r.priority,
            reverse=True,
        )

    def get_agent(self, agent_id: str) -> Optional[AgentConfig]:
        """Get an agent config by ID."""
        for agent in self.agents:
            if agent.agent_id == agent_id:
                return agent
        return None

    def get_agent_by_name(self, name: str) -> Optional[AgentConfig]:
        """Get an agent config by name (case-insensitive)."""
        name_lower = name.lower()
        for agent in self.agents:
            if agent.name.lower() == name_lower:
                return agent
        return None

    def get_mcp(self, mcp_id: str) -> Optional[MCPConfig]:
        """Get an MCP config by ID."""
        for mcp in self.mcps:
            if mcp.mcp_id == mcp_id:
                return mcp
        return None

    def get_mcp_by_name(self, name: str) -> Optional[MCPConfig]:
        """Get an MCP config by name (case-insensitive)."""
        name_lower = name.lower()
        for mcp in self.mcps:
            if mcp.name.lower() == name_lower:
                return mcp
        return None

    def get_auto_start_mcps(self) -> list[MCPConfig]:
        """Get all MCPs configured to auto-start."""
        return [m for m in self.mcps if m.enabled and m.auto_start]

    def get_skill(self, skill_id: str) -> Optional[Skill]:
        """Get a skill by ID."""
        for skill in self.skills:
            if skill.skill_id == skill_id:
                return skill
        return None

    def get_skill_by_name(self, name: str) -> Optional[Skill]:
        """Get a skill by name (case-insensitive)."""
        name_lower = name.lower()
        for skill in self.skills:
            if skill.name.lower() == name_lower:
                return skill
        return None

    # ─────────────────────────────────────────────────────────────
    # Mutation methods
    # ─────────────────────────────────────────────────────────────

    def add_rule(self, rule: Rule) -> None:
        """Add a rule to the registry."""
        self.rules.append(rule)
        self._bump_version()

    def update_rule(self, rule: Rule) -> bool:
        """Update an existing rule."""
        for i, r in enumerate(self.rules):
            if r.rule_id == rule.rule_id:
                rule.updated_at = datetime.utcnow().isoformat()
                self.rules[i] = rule
                self._bump_version()
                return True
        return False

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by ID."""
        original_len = len(self.rules)
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
        if len(self.rules) < original_len:
            self._bump_version()
            return True
        return False

    def add_agent(self, agent: AgentConfig) -> None:
        """Add an agent config to the registry."""
        self.agents.append(agent)
        self._bump_version()

    def update_agent(self, agent: AgentConfig) -> bool:
        """Update an existing agent config."""
        for i, a in enumerate(self.agents):
            if a.agent_id == agent.agent_id:
                agent.updated_at = datetime.utcnow().isoformat()
                self.agents[i] = agent
                self._bump_version()
                return True
        return False

    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent config by ID."""
        original_len = len(self.agents)
        self.agents = [a for a in self.agents if a.agent_id != agent_id]
        if len(self.agents) < original_len:
            self._bump_version()
            return True
        return False

    def add_mcp(self, mcp: MCPConfig) -> None:
        """Add an MCP config to the registry."""
        self.mcps.append(mcp)
        self._bump_version()

    def update_mcp(self, mcp: MCPConfig) -> bool:
        """Update an existing MCP config."""
        for i, m in enumerate(self.mcps):
            if m.mcp_id == mcp.mcp_id:
                mcp.updated_at = datetime.utcnow().isoformat()
                self.mcps[i] = mcp
                self._bump_version()
                return True
        return False

    def remove_mcp(self, mcp_id: str) -> bool:
        """Remove an MCP config by ID."""
        original_len = len(self.mcps)
        self.mcps = [m for m in self.mcps if m.mcp_id != mcp_id]
        if len(self.mcps) < original_len:
            self._bump_version()
            return True
        return False

    def add_skill(self, skill: Skill) -> None:
        """Add a skill to the registry."""
        self.skills.append(skill)
        self._bump_version()

    def update_skill(self, skill: Skill) -> bool:
        """Update an existing skill."""
        for i, s in enumerate(self.skills):
            if s.skill_id == skill.skill_id:
                skill.updated_at = datetime.utcnow().isoformat()
                self.skills[i] = skill
                self._bump_version()
                return True
        return False

    def remove_skill(self, skill_id: str) -> bool:
        """Remove a skill by ID."""
        original_len = len(self.skills)
        self.skills = [s for s in self.skills if s.skill_id != skill_id]
        if len(self.skills) < original_len:
            self._bump_version()
            return True
        return False

    def _bump_version(self) -> None:
        """Increment version and update timestamp."""
        self.version += 1
        self.updated_at = datetime.utcnow().isoformat()
