"""Rules loader from .emdash/rules/*.md files.

Allows users to define custom rules and guidelines that are
injected into agent system prompts.

Rules are loaded from two locations (in order):
1. Global rules in ~/.emdash/rules/ (user's home directory)
2. Repo-local rules in .emdash/rules/ (can extend global rules)
"""

from pathlib import Path
from typing import Optional

from ..utils.logger import log


def _get_global_rules_dir() -> Path:
    """Get the global rules directory in user's home (~/.emdash/rules/)."""
    return Path.home() / ".emdash" / "rules"


def _load_rules_from_dir(rules_dir: Path, source: str = "local") -> list[str]:
    """Load rules from a specific directory.

    Args:
        rules_dir: Directory containing rule .md files
        source: Source type for logging ("global" or "local")

    Returns:
        List of rule content strings
    """
    rules_parts = []

    if not rules_dir.exists():
        return rules_parts

    # Load all .md files in order
    for md_file in sorted(rules_dir.glob("*.md")):
        try:
            content = md_file.read_text().strip()
            if content:
                rules_parts.append(content)
                log.debug(f"Loaded {source} rules from: {md_file.name}")
        except Exception as e:
            log.warning(f"Failed to load rules from {md_file}: {e}")

    return rules_parts


def load_rules(rules_dir: Optional[Path] = None) -> str:
    """Load rules from global and repo-local directories.

    Rules files are markdown that get concatenated and injected
    into the agent's system prompt.

    Rules are loaded from two locations (in order):
    1. Global rules in ~/.emdash/rules/ (user's home directory)
    2. Repo-local rules in .emdash/rules/ (extends global rules)

    Example rules file:

    ```markdown
    # Code Review Guidelines

    - Always check for security implications
    - Prefer composition over inheritance
    - Document all public APIs
    ```

    Args:
        rules_dir: Directory containing repo-local rule .md files.
                  Defaults to .emdash/rules/ in cwd.

    Returns:
        Combined rules as a string
    """
    if rules_dir is None:
        rules_dir = Path.cwd() / ".emdash" / "rules"

    all_rules_parts = []

    # First, load global rules from ~/.emdash/rules/
    global_dir = _get_global_rules_dir()
    global_rules = _load_rules_from_dir(global_dir, source="global")
    all_rules_parts.extend(global_rules)

    # Then, load repo-local rules (extends global)
    local_rules = _load_rules_from_dir(rules_dir, source="local")
    all_rules_parts.extend(local_rules)

    if all_rules_parts:
        combined = "\n\n---\n\n".join(all_rules_parts)
        log.info(
            f"Loaded {len(all_rules_parts)} rule files "
            f"({len(global_rules)} global, {len(local_rules)} local)"
        )
        return combined

    return ""


def get_rules_for_agent(
    agent_name: str,
    rules_dir: Optional[Path] = None,
) -> str:
    """Get rules specific to an agent.

    Looks for:
    1. Agent-specific rules in {rules_dir}/{agent_name}.md
    2. General rules in {rules_dir}/*.md

    Args:
        agent_name: Name of the agent
        rules_dir: Optional rules directory

    Returns:
        Combined rules string
    """
    if rules_dir is None:
        rules_dir = Path.cwd() / ".emdash" / "rules"

    parts = []

    # Load general rules first
    general_rules = load_rules(rules_dir)
    if general_rules:
        parts.append(general_rules)

    # Look for agent-specific rules
    agent_rules_file = rules_dir / f"{agent_name}.md"
    if agent_rules_file.exists():
        try:
            agent_rules = agent_rules_file.read_text().strip()
            if agent_rules:
                parts.append(f"# Agent-Specific Rules: {agent_name}\n\n{agent_rules}")
                log.debug(f"Loaded agent-specific rules for: {agent_name}")
        except Exception as e:
            log.warning(f"Failed to load agent rules: {e}")

    return "\n\n---\n\n".join(parts)


def format_rules_for_prompt(rules: str) -> str:
    """Format rules for inclusion in a system prompt.

    Args:
        rules: Raw rules content

    Returns:
        Formatted rules section
    """
    if not rules:
        return ""

    return f"""
## Project Guidelines

The following rules and guidelines should be followed:

{rules}

---
"""
