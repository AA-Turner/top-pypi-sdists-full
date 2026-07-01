"""
cvc.agent.skills — Skill system for CVC Agent.

Skills are reusable patterns/templates defined as markdown files
with YAML frontmatter. They can be auto-invoked based on prompt
patterns or manually triggered via the /skill command.

Two on-disk layouts are supported:

1. **CVC native (flat)** — historical CVC layout:
   ``<workspace>/.cvc/skills/<name>/skill.md`` or
   ``<workspace>/.cvc/skills/<name>.md`` (and ``~/.cvc/skills/...``).

2. **Upstream (categorised, nested)** — the layout under
   ``~/.cvc/skills/<category>/<name>/SKILL.md``. Categories may
   be nested (e.g. ``mlops/training``).

Frontmatter (YAML between ``---`` markers, parsed tolerantly so
PyYAML is not a hard runtime requirement):

    name: skill-name
    description: What this skill does
    tools: [read_file, grep]
    auto_invoke: ["regex pattern"]

The loader returns a flat ``list[Skill]``. A persona's selected-skill
list filters this set at session start via :func:`filter_by_persona`.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

logger = logging.getLogger("cvc.agent.skills")

# Upstream shared skill tree — discovered automatically so dashboard-listed
# upstream skills actually execute in the CLI agent loop.
_HERMES_SKILLS_DIR = Path.home() / ".hermes" / "skills"

# CVC ships its own copy of the full upstream skill catalogue (core + optional)
# under ``cvc/bundled_skills/`` so users get all 160+ skills out-of-the-box
# without having to install the upstream agent, OpenClaw, Claude Code, etc.
# Resolved relative to this file so it works in both editable and wheel installs.
_BUNDLED_SKILLS_DIR = Path(__file__).resolve().parent.parent / "bundled_skills"


@dataclass
class Skill:
    """A loaded CVC skill."""
    name: str
    description: str
    content: str  # The skill's instruction content
    tools: list[str] = field(default_factory=list)  # Allowed tools
    auto_invoke_patterns: list[str] = field(default_factory=list)
    path: Path | None = None
    category: str = ""  # Upstream category (e.g. "mlops/training"); empty for native

    def matches(self, prompt: str) -> bool:
        """Check if this skill should auto-invoke for the given prompt."""
        for pattern in self.auto_invoke_patterns:
            try:
                if re.search(pattern, prompt, re.IGNORECASE):
                    return True
            except re.error:
                pass
        return False


def discover_skills(workspace: str | Path, include_archived: bool = False) -> list[Skill]:
    """Discover skills from project, user, and upstream shared directories.

    Order (later wins on name collision so the user can shadow an upstream skill
    by dropping a file with the same name into ``~/.cvc/skills/``):

    1. ``~/.cvc/skills/<cat>/<name>/SKILL.md`` (shared)
    2. ``~/.cvc/skills/...`` (user override)
    3. ``<workspace>/.cvc/skills/...`` (workspace override)

    Skills with lifecycle state ``archived`` (per usage records) are filtered
    out unless ``include_archived=True``. Lifecycle is driven by the vendored
    upstream ``skill_usage`` substrate (item 3.3).
    """
    by_name: dict[str, Skill] = {}

    # 1. CVC's bundled skill catalogue (always available — ships with the wheel)
    for skill in _walk_hermes_dir(_BUNDLED_SKILLS_DIR):
        by_name[skill.name] = skill

    # 2. Upstream shared skills (override bundled if user has upstream installed)
    for skill in _walk_hermes_dir(_HERMES_SKILLS_DIR):
        by_name[skill.name] = skill

    # 3 & 4. CVC native (flat) skills
    native_dirs = [
        Path.home() / ".cvc" / "skills",
        Path(workspace) / ".cvc" / "skills",
    ]
    for d in native_dirs:
        for skill in _walk_native_dir(d):
            by_name[skill.name] = skill

    # When showing archived skills, also walk the .archive/ subtree (skills are
    # physically moved there by ``archive_skill``).
    if include_archived:
        for d in native_dirs:
            archive_root = d / ".archive"
            for skill in _walk_native_dir(archive_root):
                by_name.setdefault(skill.name, skill)

    skills = list(by_name.values())

    # Phase B (3.3): filter archived skills from the active set.
    if not include_archived:
        try:
            from cvc.skills.usage import (
                load_usage,
                STATE_ARCHIVED,
            )
            usage = load_usage()
            archived = {
                n for n, rec in usage.items()
                if isinstance(rec, dict) and rec.get("state") == STATE_ARCHIVED
            }
            if archived:
                skills = [s for s in skills if s.name not in archived]
        except Exception as exc:  # pragma: no cover — substrate may be missing
            logger.debug("skill_usage filter unavailable: %s", exc)

    return skills


def _walk_native_dir(search_dir: Path) -> Iterable[Skill]:
    """CVC's historical flat layout."""
    if not search_dir.is_dir():
        return
    for item in sorted(search_dir.iterdir()):
        # Skip dotfiles and hidden subdirs (.usage.json, .archive, etc.)
        if item.name.startswith("."):
            continue
        skill = None
        if item.is_dir():
            skill_file = item / "skill.md"
            if not skill_file.exists():
                # Tolerate uppercase SKILL.md in native dirs too
                skill_file = item / "SKILL.md"
            if skill_file.exists():
                skill = _load_skill(skill_file, item.name)
        elif item.suffix == ".md":
            skill = _load_skill(item, item.stem)
        if skill:
            yield skill


def _walk_hermes_dir(root: Path) -> Iterable[Skill]:
    """Upstream layout: ``<root>/<category...>/<name>/SKILL.md``.

    Categories may be nested (one or more levels). We just rglob for
    every SKILL.md and derive ``category`` from the relative path.
    """
    if not root.is_dir():
        return
    for skill_file in sorted(root.rglob("SKILL.md")):
        try:
            rel = skill_file.relative_to(root)
        except ValueError:
            continue
        # rel = <cat>/.../<name>/SKILL.md  →  name = parent dir, category = the rest
        parts = rel.parts
        if len(parts) < 2:
            continue
        name = parts[-2]
        category = "/".join(parts[:-2])
        skill = _load_skill(skill_file, name)
        if skill:
            skill.category = category
            yield skill


def _parse_frontmatter_tolerant(text: str) -> tuple[dict, str]:
    """Parse YAML-ish frontmatter without requiring PyYAML.

    Returns (frontmatter_dict, body). If parsing fails or no frontmatter,
    returns ({}, text).
    """
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    fm_text, body = parts[1], parts[2].lstrip("\n")

    # Try real YAML first
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(fm_text) or {}
        if isinstance(data, dict):
            return data, body
    except Exception:
        pass

    # Tolerant key:value fallback (handles description, name, simple lists)
    fm: dict = {}
    for line in fm_text.strip().splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        key = k.strip()
        val = v.strip()
        if val.startswith("[") and val.endswith("]"):
            # Cheap list parse
            inner = val[1:-1].strip()
            items = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
            fm[key] = items
        else:
            fm[key] = val.strip('"').strip("'")
    return fm, body


def _load_skill(skill_file: Path, name: str) -> Skill | None:
    """Load a skill from a markdown file with optional YAML frontmatter."""
    try:
        text = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning("Failed to read skill %s: %s", skill_file, e)
        return None

    frontmatter, content = _parse_frontmatter_tolerant(text)
    if not content:
        content = text

    tools = frontmatter.get("tools", []) or []
    auto = frontmatter.get("auto_invoke", []) or []
    if isinstance(tools, str):
        tools = [tools]
    if isinstance(auto, str):
        auto = [auto]

    return Skill(
        name=str(frontmatter.get("name", name)),
        description=str(frontmatter.get("description", content[:140])),
        content=content,
        tools=list(tools),
        auto_invoke_patterns=list(auto),
        path=skill_file,
    )


def find_matching_skills(skills: list[Skill], prompt: str) -> list[Skill]:
    """Find skills that should auto-invoke for a given prompt."""
    return [s for s in skills if s.matches(prompt)]


def filter_by_persona(skills: list[Skill], persona_skill_ids: list[str]) -> list[Skill]:
    """Restrict a discovered skill set to those a persona has selected.

    An empty / falsy ``persona_skill_ids`` means *no filtering* — caller
    keeps the full set. This matches the dashboard UX where a persona with
    zero ticked skills implicitly uses everything available.

    Built-in tool ids (``read_file``, ``patch``, ``terminal``, ``search_files``,
    ``cvc_commit`` etc.) that don't correspond to a discovered Skill are
    silently ignored — they're already exposed as tools, not skills.
    """
    if not persona_skill_ids:
        return skills
    wanted = {str(s) for s in persona_skill_ids}
    return [s for s in skills if s.name in wanted]
