"""Shared builders for the customization-quality unit tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from agentic_devtools.cli.checks.customization_quality import CustomizationUnit


def make_unit(
    path: str = ".agents/skills/demo/SKILL.md",
    *,
    kind: str = "skill",
    listing: str = ".agents/skills",
    frontmatter: dict[str, Any] | None = None,
    body: str = "",
    size_bytes: int | None = None,
    source: str | None = None,
) -> CustomizationUnit:
    """Build a :class:`CustomizationUnit` without touching the filesystem."""
    actual_body = body
    return CustomizationUnit(
        path=path,
        listing=listing,
        kind=kind,
        frontmatter=frontmatter or {},
        body=actual_body,
        size_bytes=len(actual_body.encode("utf-8")) if size_bytes is None else size_bytes,
        source=actual_body if source is None else source,
    )


def write_file(repo_root: Path, rel_path: str, content: str) -> Path:
    """Write *content* to ``repo_root/rel_path``, creating parent directories."""
    target = repo_root / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target
