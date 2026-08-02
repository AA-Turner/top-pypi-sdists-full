"""Push whitelisted Claude Code skills to the Anthropic Workspace Skills API.

Idempotent: a skill matching ``display_title`` gets a new version,
otherwise it is created. Required env: ``ANTHROPIC_API_KEY``.

Usage:
    pysae-ai-tools skills push <name>            # push a single skill
    pysae-ai-tools skills push --all             # push the whole whitelist
    pysae-ai-tools skills push <name> --dry-run  # list files without uploading
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from anthropic import Anthropic

from .whitelist import PUBLISHED_SKILLS

app = typer.Typer(no_args_is_help=True, add_completion=False, help=__doc__)

SKILLS_ROOT = Path(__file__).resolve().parent.parent / "claude_plugin" / "skills"
SHARED_REFERENCES = SKILLS_ROOT / "references"

_MIME: dict[str, str] = {
    ".md": "text/markdown",
    ".txt": "text/plain",
    ".py": "text/x-python",
    ".js": "application/javascript",
    ".mjs": "application/javascript",
    ".json": "application/json",
    ".html": "text/html",
    ".css": "text/css",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".pdf": "application/pdf",
}


@dataclass
class SkillFile:
    relpath: str
    content: bytes
    mime: str


def _mime_for(path: Path) -> str:
    return _MIME.get(path.suffix.lower(), "application/octet-stream")


def _is_excluded(rel_parts: tuple[str, ...]) -> bool:
    return any(p.startswith(".") or p == "__pycache__" for p in rel_parts)


def _collect_files(name: str) -> list[SkillFile]:
    skill_dir = SKILLS_ROOT / name
    if not (skill_dir / "SKILL.md").is_file():
        raise typer.BadParameter(f"{name}: SKILL.md missing under {skill_dir}")

    # Skill-local files first so they win on path collisions with shared refs.
    files_by_rel: dict[str, SkillFile] = {}
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(skill_dir).parts
        if _is_excluded(rel_parts):
            continue
        rel = f"{name}/" + "/".join(rel_parts)
        files_by_rel[rel] = SkillFile(rel, path.read_bytes(), _mime_for(path))

    # Bundle shared references so skills referencing references/<file>.md
    # (e.g. post-mortem -> pysae-projects.md) ship self-contained on claude.ai
    # without needing the monorepo cloned. Skill-local refs override.
    if SHARED_REFERENCES.is_dir():
        for path in sorted(SHARED_REFERENCES.rglob("*")):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(SHARED_REFERENCES).parts
            if _is_excluded(rel_parts):
                continue
            rel = f"{name}/references/" + "/".join(rel_parts)
            files_by_rel.setdefault(rel, SkillFile(rel, path.read_bytes(), _mime_for(path)))

    return [files_by_rel[k] for k in sorted(files_by_rel)]


def _find_skill_id(client: Anthropic, display_title: str) -> str | None:
    for skill in client.beta.skills.list():
        if skill.source == "custom" and skill.display_title == display_title:
            return str(skill.id)
    return None


def _push(client: Anthropic, name: str, files: list[SkillFile]) -> None:
    payload = [(f.relpath, f.content, f.mime) for f in files]
    existing_id = _find_skill_id(client, name)
    if existing_id is not None:
        version = client.beta.skills.versions.create(skill_id=existing_id, files=payload)
        typer.echo(f"OK  {name}: new version (skill {existing_id}, version {version.id})")
        return
    skill = client.beta.skills.create(display_title=name, files=payload)
    typer.echo(f"OK  {name}: created skill {skill.id} (version {skill.latest_version})")


@app.command(name="push", help="Push one or all whitelisted skills to the Anthropic Workspace.")
def push(
    name: Annotated[str | None, typer.Argument(help="Skill name (subdirectory of claude_plugin/skills).")] = None,
    all_: Annotated[bool, typer.Option("--all", help="Push every skill in the whitelist.")] = False,
    dry_run: Annotated[
        bool, typer.Option("--dry-run", help="List files that would be uploaded without calling the API.")
    ] = False,
) -> None:
    if all_ and name is not None:
        raise typer.BadParameter("Pass either --all or a skill name, not both.")
    if all_:
        targets: list[str] = list(PUBLISHED_SKILLS)
    elif name is not None:
        if name not in PUBLISHED_SKILLS:
            raise typer.BadParameter(f"{name} is not in the whitelist (see pysae_ai_tools/skills/whitelist.py).")
        targets = [name]
    else:
        raise typer.BadParameter("Pass either --all or a skill name.")

    if not dry_run and not os.environ.get("ANTHROPIC_API_KEY"):
        raise typer.BadParameter("ANTHROPIC_API_KEY env var is required (skip with --dry-run).")

    client: Anthropic | None = None if dry_run else Anthropic()

    for n in targets:
        files = _collect_files(n)
        size = sum(len(f.content) for f in files)
        typer.echo(f"-- {n}: {len(files)} files, {size:,} bytes")
        for f in files:
            typer.echo(f"    {f.relpath} ({len(f.content):,} bytes)")
        if dry_run:
            continue
        assert client is not None
        _push(client, n, files)
