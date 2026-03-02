"""Main agent system prompt.

The primary prompt for the orchestrating agent that manages sub-agents
and handles complex multi-step tasks.
"""

from .workflow import (
    EXPLORATION_DECISION_RULES,
    WORKFLOW_PATTERNS,
    EXPLORATION_STRATEGY,
    OUTPUT_GUIDELINES,
    PARALLEL_EXECUTION,
    TASK_GUIDANCE,
    VERIFICATION_AND_CRITIQUE,
    ACTION_NOT_ANNOUNCEMENT,
    COMPLETE_IMPLEMENTATION,
    BROWSER_HANDOFF_GUIDELINES,
)
from .plan_mode import PLAN_MODE_PROMPT as _PLAN_MODE_INSTRUCTIONS

# Base system prompt template with placeholder for tools
_BASE_PROMPT = """You are a code exploration and implementation assistant. You orchestrate focused sub-agents for exploration while maintaining the high-level view.

{tools_section}
"""

# Code mode system prompt - the default orchestrator prompt
# EXPLORATION_DECISION_RULES comes first as the core decision framework
_CODE_MODE_PROMPT = _BASE_PROMPT + EXPLORATION_DECISION_RULES + WORKFLOW_PATTERNS + PARALLEL_EXECUTION + EXPLORATION_STRATEGY + TASK_GUIDANCE + ACTION_NOT_ANNOUNCEMENT + VERIFICATION_AND_CRITIQUE + OUTPUT_GUIDELINES + COMPLETE_IMPLEMENTATION + BROWSER_HANDOFF_GUIDELINES

# Legacy alias
BASE_SYSTEM_PROMPT = _CODE_MODE_PROMPT

# Mode-specific prompts
CODE_MODE_PROMPT = _CODE_MODE_PROMPT
PLAN_MODE_PROMPT = _CODE_MODE_PROMPT + "\n\n" + _PLAN_MODE_INSTRUCTIONS


def build_system_prompt(toolkit) -> str:
    """Build the complete system prompt with dynamic tool descriptions.

    Selects the appropriate base prompt depending on whether the toolkit
    is in plan mode (read-only exploration + planning workflow) or code
    mode (full implementation capabilities).

    Args:
        toolkit: The agent toolkit with registered tools

    Returns:
        Complete system prompt string
    """
    tools_section = build_tools_section(toolkit)
    agents_section = build_agents_section(toolkit)
    skills_section = build_skills_section()
    rules_section = build_rules_section()
    session_section = build_session_context_section(toolkit)

    # Select base prompt based on mode
    plan_mode = getattr(toolkit, 'plan_mode', False)
    base = PLAN_MODE_PROMPT if plan_mode else _CODE_MODE_PROMPT

    # Build prompt - task guidance is provided by emdash-tasks MCP server
    prompt = base.format(
        tools_section=tools_section,
    )

    # Add session context section first (repo, branch, status)
    if session_section:
        prompt += "\n" + session_section

    # Add agents section so main agent knows what agents are available
    if agents_section:
        prompt += "\n" + agents_section

    # Add rules section if there are rules defined
    if rules_section:
        prompt += "\n" + rules_section

    # Add skills section if there are skills available
    if skills_section:
        prompt += "\n" + skills_section

    return prompt


def build_session_context_section(toolkit) -> str:
    """Build the session context section with repo, branch, and git status.

    Args:
        toolkit: The agent toolkit (to access repo_root)

    Returns:
        Formatted string with session context, or empty string if not in a git repo
    """
    from ...utils.git import (
        get_repo_name,
        get_current_branch,
        get_git_status_summary,
    )

    repo_root = getattr(toolkit, '_repo_root', None)
    if not repo_root:
        return ""

    repo_name = get_repo_name(repo_root)
    branch = get_current_branch(repo_root)
    status = get_git_status_summary(repo_root)

    # Only include if we have at least some git info
    if not any([repo_name, branch, status]):
        return ""

    lines = [
        "## Session Context",
        "",
    ]

    if repo_name:
        lines.append(f"- **Repository**: {repo_name}")
    if branch:
        lines.append(f"- **Branch**: {branch}")
    if status:
        lines.append(f"- **Git Status**: {status}")

    lines.append(f"- **Working Directory**: {repo_root}")
    lines.append("")

    return "\n".join(lines)


def build_rules_section() -> str:
    """Build the rules section of the system prompt.

    Loads rules from .emdash/rules/*.md files.

    Returns:
        Formatted string with project rules, or empty string if none
    """
    from ..rules import load_rules, format_rules_for_prompt

    rules = load_rules()
    return format_rules_for_prompt(rules)


def build_skills_section() -> str:
    """Build the skills section of the system prompt.

    Returns:
        Formatted string with available skills, or empty string if none
    """
    from ..skills import SkillRegistry

    registry = SkillRegistry.get_instance()
    return registry.get_skills_for_prompt()


def build_agents_section(toolkit) -> str:
    """Build the agents section describing available sub-agents.

    Args:
        toolkit: The agent toolkit (to access repo_root)

    Returns:
        Formatted string with agent descriptions, or empty string if none
    """
    from ..toolkits import get_agents_with_descriptions

    repo_root = getattr(toolkit, '_repo_root', None)
    agents = get_agents_with_descriptions(repo_root)

    if not agents:
        return ""

    lines = [
        "## Available Agents",
        "",
        "Use the `task` tool to delegate work to these specialized agents:",
        "",
    ]

    for agent in agents:
        lines.append(f"- **{agent['name']}**: {agent['description']}")

    return "\n".join(lines)


def build_tools_section(toolkit) -> str:
    """Build the tools section of the system prompt from registered tools.

    Args:
        toolkit: The agent toolkit with registered tools

    Returns:
        Formatted string with tool descriptions grouped by category
    """
    from ..tools.base import ToolCategory

    # Group tools by category
    tools_by_category: dict[str, list[tuple[str, str]]] = {}

    for tool in toolkit._tools.values():
        # Get category name
        if hasattr(tool, 'category'):
            category = tool.category.value if isinstance(tool.category, ToolCategory) else str(tool.category)
        else:
            category = "other"

        # Get tool name and description
        name = tool.name
        description = tool.description

        # Clean up description - take first sentence or first 150 chars
        if description:
            # Remove [server_name] prefix if present (from MCP tools)
            if description.startswith("["):
                description = description.split("]", 1)[-1].strip()
            # Take first sentence
            first_sentence = description.split(".")[0] + "."
            if len(first_sentence) > 150:
                first_sentence = description[:147] + "..."
            description = first_sentence
        else:
            description = "No description available."

        if category not in tools_by_category:
            tools_by_category[category] = []
        tools_by_category[category].append((name, description))

    # Build formatted section
    lines = ["## Available Tools\n"]

    # Define category display order and titles
    category_titles = {
        "search": "Search & Discovery",
        "traversal": "Graph Traversal",
        "analytics": "Analytics",
        "planning": "Planning",
        "history": "History",
        "other": "Other Tools",
    }

    # Sort categories by predefined order
    category_order = ["search", "traversal", "analytics", "planning", "history", "other"]
    sorted_categories = sorted(
        tools_by_category.keys(),
        key=lambda c: category_order.index(c) if c in category_order else 999
    )

    for category in sorted_categories:
        tools = tools_by_category[category]
        title = category_titles.get(category, category.title())

        lines.append(f"### {title}")
        for name, desc in sorted(tools):
            lines.append(f"- **{name}**: {desc}")
        lines.append("")

    return "\n".join(lines)
