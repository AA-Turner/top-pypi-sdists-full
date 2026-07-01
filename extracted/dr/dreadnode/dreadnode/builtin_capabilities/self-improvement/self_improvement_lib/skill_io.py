"""Skill-file reads and writes — the capability's side-effectful surface."""

from datetime import UTC, datetime
from pathlib import Path

import yaml

from dreadnode.agents.skills import load_skill
from dreadnode.agents.tools import tool

_CAPABILITY_ROOT = Path(__file__).resolve().parents[1]
_PROPOSED_DIR = _CAPABILITY_ROOT / "skills-proposed"


@tool
async def write_skill(
    name: str,
    description: str,
    instructions: str,
    allowed_tools: list[str] | None = None,
    triggering_error_kind: str | None = None,
    triggering_sample: str | None = None,
) -> str:
    """Create a new SKILL.md under the proposed-skills directory.

    Fails if a skill with this name already exists — use update_skill instead.
    """
    target_dir = _PROPOSED_DIR / name
    skill_md = target_dir / "SKILL.md"
    if skill_md.exists():
        raise FileExistsError(f"skill {name!r} already exists at {skill_md}; use update_skill")
    target_dir.mkdir(parents=True, exist_ok=True)

    frontmatter: dict = {
        "name": name,
        "description": description,
        "metadata": {
            "dreadnode.self_improvement": {
                "origin": "reflector",
                "proposed_at": datetime.now(UTC).isoformat(),
                "triggering_error_kind": triggering_error_kind,
                "triggering_sample": triggering_sample,
                "usage": {"invocations": 0, "successes": 0, "failures": 0},
            },
        },
    }
    if allowed_tools:
        frontmatter["allowed-tools"] = " ".join(allowed_tools)

    skill_md.write_text(f"---\n{yaml.safe_dump(frontmatter)}---\n\n{instructions.strip()}\n")
    load_skill(skill_md)
    return f"wrote {skill_md}"


@tool
async def update_skill(
    name: str,
    instructions: str,
    description: str | None = None,
) -> str:
    """Update an existing proposed skill's body (and optionally description)."""
    skill_md = _PROPOSED_DIR / name / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"no proposed skill {name!r} at {skill_md}")

    existing = load_skill(skill_md)
    metadata: dict = dict(existing.metadata or {})
    meta: dict = metadata.setdefault("dreadnode.self_improvement", {})
    meta["updated_at"] = datetime.now(UTC).isoformat()
    frontmatter: dict = {
        "name": existing.name,
        "description": description or existing.description,
        "metadata": metadata,
    }
    if existing.allowed_tools:
        frontmatter["allowed-tools"] = " ".join(existing.allowed_tools)

    skill_md.write_text(f"---\n{yaml.safe_dump(frontmatter)}---\n\n{instructions.strip()}\n")
    load_skill(skill_md)
    return f"updated {skill_md}"


@tool
async def record_skill_outcome(skill_path: str, success: bool) -> str:
    """Increment usage counters on a skill's frontmatter."""
    path = Path(skill_path)
    text = path.read_text()
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError(f"not a frontmatter skill file: {skill_path}")

    frontmatter = yaml.safe_load(parts[1]) or {}
    meta = frontmatter.setdefault("metadata", {}).setdefault("dreadnode.self_improvement", {})
    usage = meta.setdefault("usage", {"invocations": 0, "successes": 0, "failures": 0})
    usage["invocations"] += 1
    usage["successes" if success else "failures"] += 1
    usage["last_used_at"] = datetime.now(UTC).isoformat()

    path.write_text(f"---\n{yaml.safe_dump(frontmatter)}---\n{parts[2]}")
    return f"recorded {'success' if success else 'failure'} on {path.name}"
