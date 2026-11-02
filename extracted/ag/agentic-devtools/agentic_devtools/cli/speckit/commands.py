"""
Speckit command implementations.

Each command reads the corresponding ``.github/agents/speckit.<name>.agent.md``
template, strips its YAML frontmatter, replaces ``$ARGUMENTS`` with the
arguments the user supplied on the CLI, or appends them when the template does
not contain that placeholder. It prints the rendered prompt and saves it in
the workflow state directory; it does not start a ``gh copilot`` session.
"""

import re
import sys
from pathlib import Path

from ...state import _get_git_repo_root, get_state_dir

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
_SKILL_LINK_RE = re.compile(r"\[(?P<label>[^\]]+)\]\((?P<path>(?:\.\.?/)*\.agents/skills/[^)]+/SKILL\.md)\)")


def _inline_skill_links(content: str, agent_file: Path, repo_root: Path) -> str:
    """Replace local skill links with their text and append the linked skill content."""
    skill_root = (repo_root / ".agents" / "skills").resolve()
    embedded_skills: list[str] = []

    def replace_link(match: re.Match[str]) -> str:
        skill_file = (agent_file.parent / match.group("path")).resolve()
        if not skill_file.is_relative_to(skill_root):
            raise ValueError(f"Linked skill must resolve within .agents/skills: {skill_file}")
        skill_content = skill_file.read_text(encoding="utf-8")
        skill_content = _FRONTMATTER_RE.sub("", skill_content, count=1)
        embedded_skills.append(skill_content)
        return match.group("label")

    content = _SKILL_LINK_RE.sub(replace_link, content)
    if embedded_skills:
        content = f"{content.rstrip()}\n\n" + "\n\n".join(skill_content.rstrip() for skill_content in embedded_skills)
    return content


def _load_prompt(name: str, arguments: str) -> str:
    """
    Load a speckit agent template and include the CLI arguments.

    Reads from ``.github/agents/speckit.<name>.agent.md`` (the full agent
    content) rather than the thin ``.github/prompts/`` router files.

    Args:
        name: Speckit command name, e.g. ``"specify"``.
        arguments: User-supplied arguments string (may be empty).

    Returns:
        Rendered prompt text with linked local skills inlined.

    Raises:
        SystemExit: If the repo root or agent file cannot be found.
    """
    repo_root = _get_git_repo_root()
    if repo_root is None:
        print("ERROR: Not inside a git repository.", file=sys.stderr)
        sys.exit(1)

    agent_file = repo_root / ".github" / "agents" / f"speckit.{name}.agent.md"
    if not agent_file.exists():
        print(f"ERROR: Agent file not found: {agent_file}", file=sys.stderr)
        sys.exit(1)

    content = agent_file.read_text(encoding="utf-8")
    # Strip YAML frontmatter (between leading --- and closing ---)
    content = _FRONTMATTER_RE.sub("", content, count=1)
    content = _inline_skill_links(content, agent_file, repo_root)
    if "$ARGUMENTS" in content:
        content = content.replace("$ARGUMENTS", arguments)
    elif arguments:
        content = f"{content.rstrip()}\n\n## User-provided arguments\n\n{arguments}\n"
    return content


def _run(name: str, arguments: str) -> None:
    """
    Load prompt for *name*, print it to stdout, and save it to the state dir.

    Printing to stdout lets the Copilot CLI agent (running in the terminal)
    see the prompt and act on it immediately, without spawning a nested
    ``gh copilot`` process.

    Args:
        name: Speckit command name.
        arguments: User-supplied arguments string.
    """
    prompt = _load_prompt(name, arguments)

    # Save to state dir so the prompt can be referenced later
    temp_dir = get_state_dir()
    temp_dir.mkdir(parents=True, exist_ok=True)
    saved_path = temp_dir / f"temp-speckit-{name}-prompt.md"
    saved_path.write_text(prompt, encoding="utf-8")
    save_notice = f"\n[Prompt saved to: {saved_path}]"

    separator = "=" * 80
    print(f"\n{separator}")
    print(f"SPECKIT: {name.upper()}")
    print(separator)
    print(prompt)
    print(separator)
    print(save_notice)


def _parse_args(argv: list | None = None) -> str:
    """Return remaining CLI args joined as a single string."""
    args = argv if argv is not None else sys.argv[1:]
    return " ".join(args)


# ---------------------------------------------------------------------------
# Command entry points
# ---------------------------------------------------------------------------


def speckit_specify(argv: list | None = None) -> None:
    """agdt-speckit-specify — create or update a feature specification."""
    _run("specify", _parse_args(argv))


def speckit_plan(argv: list | None = None) -> None:
    """agdt-speckit-plan — generate an implementation plan."""
    _run("plan", _parse_args(argv))


def speckit_tasks(argv: list | None = None) -> None:
    """agdt-speckit-tasks — generate actionable tasks from design artifacts."""
    _run("tasks", _parse_args(argv))


def speckit_implement(argv: list | None = None) -> None:
    """agdt-speckit-implement — execute the implementation plan."""
    _run("implement", _parse_args(argv))


def speckit_clarify(argv: list | None = None) -> None:
    """agdt-speckit-clarify — identify underspecified areas in the spec."""
    _run("clarify", _parse_args(argv))


def speckit_checklist(argv: list | None = None) -> None:
    """agdt-speckit-checklist — generate a custom checklist for the feature."""
    _run("checklist", _parse_args(argv))


def speckit_analyze(argv: list | None = None) -> None:
    """agdt-speckit-analyze — cross-artifact consistency and quality analysis."""
    _run("analyze", _parse_args(argv))


def speckit_constitution(argv: list | None = None) -> None:
    """agdt-speckit-constitution — create or update the project constitution."""
    _run("constitution", _parse_args(argv))


def speckit_taskstoissues(argv: list | None = None) -> None:
    """agdt-speckit-taskstoissues — convert tasks to GitHub issues."""
    _run("taskstoissues", _parse_args(argv))
