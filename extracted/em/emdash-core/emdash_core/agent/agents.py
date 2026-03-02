"""Custom agent loader from .emdash/agents/*.md files.

Allows users to define custom agent configurations with
specialized system prompts and tool selections.

Example agent file:
```markdown
---
description: GitHub integration agent
model: minimax
tools: [grep, glob, read_file]
mcp_servers:
  github:
    command: github-mcp-server
    args: []
    env:
      GITHUB_TOKEN: ${GITHUB_TOKEN}
    enabled: true
  filesystem:
    command: npx
    args: [-y, "@anthropic/mcp-server-filesystem", "/tmp"]
    enabled: false  # Disabled - won't be started
---

# System Prompt

You are a GitHub integration specialist...
```
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
import re

import yaml

from ..utils.logger import log


@dataclass
class AgentMCPServerConfig:
    """MCP server configuration for a custom agent.

    Attributes:
        name: Server name (key in mcp_servers dict)
        command: Command to run the server
        args: Arguments to pass to the command
        env: Environment variables (supports ${VAR} syntax)
        enabled: Whether this server is enabled (default: True)
        timeout: Timeout in seconds for tool calls
    """
    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    enabled: bool = True
    timeout: int = 30

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> "AgentMCPServerConfig":
        """Create from dictionary parsed from YAML."""
        return cls(
            name=name,
            command=data.get("command", ""),
            args=data.get("args", []),
            env=data.get("env", {}),
            enabled=data.get("enabled", True),
            timeout=data.get("timeout", 30),
        )


@dataclass
class CustomAgent:
    """A custom agent configuration loaded from markdown.

    Attributes:
        name: Agent name (from filename)
        description: Brief description
        model: Model to use for this agent (optional, uses default if not set)
        system_prompt: Custom system prompt
        tools: List of tools to enable
        mcp_servers: MCP server configurations for this agent
        rules: List of rule names to apply (references .emdash/rules/)
        skills: List of skill names to enable (references .emdash/skills/)
        verifiers: List of verifier names to use (references .emdash/verifiers.json)
        examples: Example interactions
        file_path: Source file path
    """

    name: str
    description: str = ""
    model: Optional[str] = None
    system_prompt: str = ""
    tools: list[str] = field(default_factory=list)
    mcp_servers: list[AgentMCPServerConfig] = field(default_factory=list)
    rules: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    verifiers: list[str] = field(default_factory=list)
    examples: list[dict] = field(default_factory=list)
    file_path: Optional[Path] = None


def load_agents(
    agents_dir: Optional[Path] = None,
) -> dict[str, CustomAgent]:
    """Load custom agents from .emdash/agents/ directory.

    Agent files are markdown with frontmatter-style metadata:

    ```markdown
    ---
    description: Security analysis agent
    tools: [semantic_search, get_callers, get_impact_analysis]
    ---

    # System Prompt

    You are a security-focused code analyst...

    # Examples

    ## Example 1
    User: Find SQL injection vulnerabilities
    Agent: I'll search for database query patterns...
    ```

    Args:
        agents_dir: Directory containing agent .md files.
                   Defaults to .emdash/agents/ in cwd.

    Returns:
        Dict mapping agent name to CustomAgent
    """
    if agents_dir is None:
        agents_dir = Path.cwd() / ".emdash" / "agents"

    if not agents_dir.exists():
        return {}

    agents = {}

    for md_file in agents_dir.glob("*.md"):
        try:
            agent = _parse_agent_file(md_file)
            if agent:
                agents[agent.name] = agent
                log.debug(f"Loaded custom agent: {agent.name}")
        except Exception as e:
            log.warning(f"Failed to load agent from {md_file}: {e}")

    if agents:
        log.info(f"Loaded {len(agents)} custom agents")

    return agents


def _parse_agent_file(file_path: Path) -> Optional[CustomAgent]:
    """Parse a single agent markdown file.

    Args:
        file_path: Path to the .md file

    Returns:
        CustomAgent or None if parsing fails
    """
    content = file_path.read_text()

    # Extract frontmatter
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = _parse_frontmatter(parts[1])
            body = parts[2].strip()

    # Extract system prompt (content before # Examples)
    system_prompt = body
    examples = []

    if "# Examples" in body:
        prompt_part, examples_part = body.split("# Examples", 1)
        system_prompt = prompt_part.strip()
        examples = _parse_examples(examples_part)

    # Remove "# System Prompt" header if present
    if system_prompt.startswith("# System Prompt"):
        system_prompt = system_prompt[len("# System Prompt") :].strip()

    # Parse MCP servers from frontmatter
    mcp_servers = []
    mcp_servers_data = frontmatter.get("mcp_servers", {})
    if isinstance(mcp_servers_data, dict):
        for server_name, server_config in mcp_servers_data.items():
            if isinstance(server_config, dict):
                mcp_servers.append(
                    AgentMCPServerConfig.from_dict(server_name, server_config)
                )

    return CustomAgent(
        name=file_path.stem,
        description=frontmatter.get("description", ""),
        model=frontmatter.get("model"),
        system_prompt=system_prompt,
        tools=frontmatter.get("tools", []),
        mcp_servers=mcp_servers,
        rules=frontmatter.get("rules", []),
        skills=frontmatter.get("skills", []),
        verifiers=frontmatter.get("verifiers", []),
        examples=examples,
        file_path=file_path,
    )


def _parse_frontmatter(frontmatter_str: str) -> dict:
    """Parse YAML frontmatter.

    Uses PyYAML for proper nested structure parsing.

    Args:
        frontmatter_str: Frontmatter string (YAML format)

    Returns:
        Dict of parsed values
    """
    try:
        result = yaml.safe_load(frontmatter_str)
        return result if isinstance(result, dict) else {}
    except yaml.YAMLError as e:
        log.warning(f"Failed to parse frontmatter as YAML: {e}")
        return {}


def _parse_examples(examples_str: str) -> list[dict]:
    """Parse example interactions from markdown.

    Args:
        examples_str: Examples section content

    Returns:
        List of example dicts with user/agent keys
    """
    examples = []

    # Split by ## Example headers
    example_blocks = re.split(r"##\s+Example\s*\d*", examples_str)

    for block in example_blocks:
        if not block.strip():
            continue

        example = {"user": "", "agent": ""}

        # Find User: and Agent: sections
        user_match = re.search(r"User:\s*(.+?)(?=Agent:|$)", block, re.DOTALL)
        agent_match = re.search(r"Agent:\s*(.+?)(?=User:|$)", block, re.DOTALL)

        if user_match:
            example["user"] = user_match.group(1).strip()
        if agent_match:
            example["agent"] = agent_match.group(1).strip()

        if example["user"] or example["agent"]:
            examples.append(example)

    return examples


def get_agent(name: str, agents_dir: Optional[Path] = None) -> Optional[CustomAgent]:
    """Get a specific custom agent by name.

    Args:
        name: Agent name (filename without .md)
        agents_dir: Optional agents directory

    Returns:
        CustomAgent or None if not found
    """
    agents = load_agents(agents_dir)
    return agents.get(name)


def list_agents(agents_dir: Optional[Path] = None) -> list[str]:
    """List available custom agent names.

    Args:
        agents_dir: Optional agents directory

    Returns:
        List of agent names
    """
    agents = load_agents(agents_dir)
    return list(agents.keys())
