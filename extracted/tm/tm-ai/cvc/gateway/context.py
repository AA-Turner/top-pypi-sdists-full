"""
System-prompt builder — makes the agent workspace-aware.

The agent MUST know:
- which project it's in (workspace path)
- what skills/commands the user has enabled
- any persistent user memory (Honcho / cross-session profile)

Returns a string the AIAgent can use as `ephemeral_system_prompt`.
The base agent identity is provided by the vendored runtime; we only
ADD the workspace context, never replace it.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger("cvc.gateway.context")


def _read_agents_md(workspace: Path) -> Optional[str]:
    """Read AGENTS.md / CLAUDE.md / .cursorrules if present — these are
    the canonical project-context files the user has set up."""
    candidates = ["AGENTS.md", "CLAUDE.md", ".cursorrules", "CURSOR.md"]
    for name in candidates:
        path = workspace / name
        if path.exists() and path.is_file():
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
                return f"\n\n## Project context from {name}\n\n{content}"
            except Exception as e:
                logger.debug("Failed to read %s: %s", path, e)
    return None


def _summarise_workspace(workspace: Path) -> str:
    """Build a short structural summary of the workspace so the agent
    doesn't have to re-list it every turn."""
    try:
        entries = list(workspace.iterdir())[:50]
        # Group by kind
        files = [e.name for e in entries if e.is_file() and not e.name.startswith(".")]
        dirs = [e.name for e in entries if e.is_dir() and not e.name.startswith(".")]
        return (
            f"Files: {', '.join(files[:30])}\n"
            f"Directories: {', '.join(dirs[:30])}"
        )
    except Exception as e:
        return f"(could not list workspace: {e})"


def build_system_prompt(
    *,
    workspace_path: Optional[str] = None,
    extra: Optional[str] = None,
) -> str:
    """Build the workspace-aware portion of the system prompt.

    This is APPENDED to the vendored runtime's base identity. The base
    identity handles "you are CVC" / tool listing / cache rules. We
    only add the project context the user expects.
    """
    if not workspace_path:
        return extra or ""

    workspace = Path(workspace_path).expanduser().resolve()
    if not workspace.exists():
        logger.warning("Workspace path does not exist: %s", workspace)
        return extra or ""

    sections: list[str] = []

    sections.append(
        f"\n\n## Your working directory\n\n"
        f"You are currently in the project at `{workspace}`.\n"
        f"Treat this as your root. Use `read_file`, `search_files`, "
        f"`terminal` and other tools relative to this path.\n"
        f"Do NOT search the parent directories or other projects unless "
        f"the user explicitly asks."
    )

    sections.append(f"\n\n## Project layout\n\n{_summarise_workspace(workspace)}")

    # AGENTS.md / CLAUDE.md / .cursorrules
    agents_ctx = _read_agents_md(workspace)
    if agents_ctx:
        sections.append(agents_ctx)

    # Skills directories
    skills_dirs = [
        workspace / ".cursorrules.d",
        workspace / ".claude",
        workspace / ".cvc",
    ]
    for d in skills_dirs:
        if d.exists() and d.is_dir():
            sections.append(
                f"\n\n## Custom skills directory: `{d}`\n"
                f"Skills defined here extend the default toolset."
            )
            break

    if extra:
        # v3.5.0 — TIME PORTAL: if the extra block is a portal-mode
        # framing (starts with the ⏳ clock emoji), PREPEND it so the
        # model sees it FIRST, before workspace context. Otherwise it
        # would land at the bottom of the prompt where the model is
        # least likely to honour it (stable identity at the top wins
        # over tail instructions on most models).
        if extra.lstrip().startswith("## \u23f3 TIME PORTAL ACTIVE"):
            sections.insert(0, extra)
        else:
            sections.append(f"\n\n## Per-turn note\n\n{extra}")

    return "".join(sections)
