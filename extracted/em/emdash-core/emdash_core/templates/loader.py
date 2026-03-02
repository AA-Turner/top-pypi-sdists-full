"""Template loader with 3-tier priority: project -> user -> defaults."""

import os
from pathlib import Path
from typing import Optional, Tuple

# Template names and their corresponding files
TEMPLATE_NAMES = {
    "spec": "spec.md.template",
    "tasks": "tasks.md.template",
    "project": "project.md.template",
    "focus": "focus.md.template",
    "pr-review": "pr-review.md.template",
    "reviewer": "reviewer.md.template",
    "agent-builder": "agent-builder.md.template",
}

# Directory name for templates
EMDASH_RULES_DIR = ".emdash-rules"


def get_defaults_dir() -> Path:
    """Get the path to the bundled defaults directory."""
    return Path(__file__).parent / "defaults"


def get_project_rules_dir() -> Optional[Path]:
    """Get the project-local .emdash-rules directory if it exists."""
    cwd = Path.cwd()
    rules_dir = cwd / EMDASH_RULES_DIR
    return rules_dir if rules_dir.is_dir() else None


def get_user_rules_dir() -> Optional[Path]:
    """Get the user-wide ~/.emdash-rules directory if it exists."""
    home = Path.home()
    rules_dir = home / EMDASH_RULES_DIR
    return rules_dir if rules_dir.is_dir() else None


def get_template_path(name: str) -> Tuple[Path, str]:
    """Get the path to a template and its source tier.

    Args:
        name: Template name ("spec", "tasks", or "project")

    Returns:
        Tuple of (path, tier) where tier is "project", "user", or "default"

    Raises:
        ValueError: If template name is invalid
    """
    if name not in TEMPLATE_NAMES:
        raise ValueError(f"Invalid template name: {name}. Must be one of: {list(TEMPLATE_NAMES.keys())}")

    filename = TEMPLATE_NAMES[name]

    # Priority 1: Project-local .emdash-rules/
    project_dir = get_project_rules_dir()
    if project_dir:
        project_path = project_dir / filename
        if project_path.is_file():
            return project_path, "project"

    # Priority 2: User-wide ~/.emdash-rules/
    user_dir = get_user_rules_dir()
    if user_dir:
        user_path = user_dir / filename
        if user_path.is_file():
            return user_path, "user"

    # Priority 3: Bundled defaults
    defaults_path = get_defaults_dir() / filename
    return defaults_path, "default"


def load_template(name: str) -> str:
    """Load a template by name.

    Searches in order:
    1. .emdash-rules/ in current directory (project-specific)
    2. ~/.emdash-rules/ in home directory (user-wide)
    3. Built-in defaults

    Args:
        name: Template name ("spec", "tasks", or "project")

    Returns:
        The template content as a string

    Raises:
        ValueError: If template name is invalid
        FileNotFoundError: If template file doesn't exist
    """
    path, tier = get_template_path(name)

    if not path.is_file():
        raise FileNotFoundError(f"Template file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def list_templates() -> list[dict]:
    """List all templates and their active sources.

    Returns:
        List of dicts with name, path, and tier for each template
    """
    templates = []
    for name in TEMPLATE_NAMES:
        try:
            path, tier = get_template_path(name)
            templates.append({
                "name": name,
                "filename": TEMPLATE_NAMES[name],
                "path": str(path),
                "tier": tier,
                "exists": path.is_file(),
            })
        except Exception as e:
            templates.append({
                "name": name,
                "filename": TEMPLATE_NAMES[name],
                "path": None,
                "tier": "error",
                "exists": False,
                "error": str(e),
            })
    return templates


def copy_templates_to_dir(target_dir: Path, overwrite: bool = False) -> list[str]:
    """Copy default templates to a target directory.

    Args:
        target_dir: Directory to copy templates to
        overwrite: Whether to overwrite existing files

    Returns:
        List of copied template filenames
    """
    defaults_dir = get_defaults_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for name, filename in TEMPLATE_NAMES.items():
        source = defaults_dir / filename
        target = target_dir / filename

        if not source.is_file():
            continue

        if target.exists() and not overwrite:
            continue

        with open(source, "r", encoding="utf-8") as f:
            content = f.read()

        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

        copied.append(filename)

    return copied


def load_template_for_agent(name: str) -> str:
    """Load a template and wrap it for LLM agent use.

    This takes the human-readable rules markdown and wraps it with
    instructions for the LLM to follow those rules.

    Args:
        name: Template name ("spec", "tasks", or "project")

    Returns:
        LLM-ready system prompt incorporating the rules
    """
    rules = load_template(name)

    # Common tool guidance for all agents
    area_tool_guidance = """
## Key Tool: get_area_importance

Use this tool to understand where activity is concentrated in the codebase:

**Directory-level (default):**
- `get_area_importance(sort='focus')` - Find HOT SPOTS: areas with recent concentrated activity
- `get_area_importance(sort='importance')` - Find historically important areas (commits × authors)
- `get_area_importance(sort='commits')` - Areas with most total commits
- `get_area_importance(sort='authors')` - Areas with most contributors

**File-level (use files=true):**
- `get_area_importance(files=true, sort='focus')` - Hot FILES with most recent commits
- `get_area_importance(files=true, sort='importance')` - Most important individual files

The tool returns for each area/file:
- path/file_path: Directory or file path
- total_commits/commits: Commit count
- file_count: Number of files (areas only)
- unique_authors/authors: Number of contributors
- focus_pct/recent_commits: Recent activity metric

**Recommended workflow:**
1. First use sort='focus' to find hot areas
2. Then use files=true to drill into specific files in those areas
3. Use semantic_search or expand_node to explore the hot files"""

    if name == "spec":
        return f"""You are writing a feature specification. Follow these rules:

{rules}

{area_tool_guidance}

IMPORTANT:
- Your output must be a single JSON object matching the schema in the rules
- START by using get_area_importance(sort='focus') to find active areas related to the feature
- Explore the codebase using tools to find similar patterns
- Use ask_clarification if you need to ask the user questions
- Be specific and reference actual file paths from the project
- The hot spots tell you where similar work is happening - look there for patterns"""

    elif name == "tasks":
        return f"""You are creating an implementation plan. Follow these rules:

{rules}

{area_tool_guidance}

IMPORTANT:
- Your output must be markdown following the format in the rules
- START by using get_area_importance(sort='focus') to understand where changes should go
- Use get_file_history on hot spot files to find the CODE OWNER (most commits)
- Each task should be executable by an LLM in a single prompt
- Include exact file paths and line references
- Reference patterns from the active areas when describing tasks"""

    elif name == "project":
        return f"""You are writing a PROJECT.md to help new team members understand the codebase. Follow these rules:

{rules}

{area_tool_guidance}

IMPORTANT:
- Your output must be markdown following the format in the rules
- START by using get_area_importance(sort='focus') to find where the team spends time
- The "Where The Action Is" section should highlight these hot spots
- Use get_area_importance(sort='importance') to find historically critical areas
- Write like explaining to a teammate, not writing documentation
- Focus on insight and understanding, not comprehensive lists
- Hot spots reveal what's actively being built - explain WHY those areas matter"""

    elif name == "focus":
        return f"""You are a senior engineering manager analyzing team activity and focus. Follow these rules:

{rules}

CRITICAL REQUIREMENTS:
- ALL PRs must be clickable links: [PR #123](https://github.com/owner/repo/pull/123)
- ALL contributors must be clickable links: [@username](https://github.com/username)
- The GitHub repository URL will be provided in the data - use it for constructing links
- Explain WHAT is being built, not just which files are touched
- Use function/class names and docstrings to understand purpose
- Group work into thematic streams with activity percentages
- Include a table for PR analysis and key contributors
- Provide actionable insights and recommendations"""

    elif name == "pr-review":
        return f"""You are producing a PR review report. Follow these rules:

{rules}

IMPORTANT:
- Your output must be markdown
- Tell a coherent story of the change, not a file list
- Cite file paths and functions inline when relevant
- If data is truncated, note it explicitly"""

    elif name == "reviewer":
        return f"""You are a code reviewer following the team's established review patterns. Use this reviewer profile:

{rules}

CRITICAL REQUIREMENTS:
- Review code with the same focus areas and quality expectations as the top reviewers
- Match the tone and communication style described in the profile
- Generate inline comments for specific lines of code
- Provide actionable, constructive feedback
- Use the checklist to ensure comprehensive review coverage
- Your output must be structured JSON with summary, verdict, and inline comments"""

    else:
        return rules
