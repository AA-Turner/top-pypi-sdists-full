"""Helpers for writing and materializing Aegis-owned skill packages."""

from __future__ import annotations

from pathlib import Path
import re
import shutil

from .provenance import InstalledSkillProvenance
from .runtime import load_skill_package_definition


_VALID_SEGMENT_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def write_skill_package(
    root: Path,
    *,
    skill_id: str,
    display_name: str,
    summary: str,
    instruction_text: str,
    category: str | None = None,
    overwrite: bool = False,
    source_kind: str = "aegis-experience",
) -> Path:
    resolved_skill_id = _validated_segment(skill_id, field_name="skill_id")
    resolved_category = _validated_segment(category, field_name="category") if category else None
    resolved_display_name = display_name.strip()
    resolved_summary = " ".join(summary.split())
    resolved_instructions = instruction_text.strip()
    if not resolved_display_name:
        raise ValueError("display_name is required")
    if not resolved_summary:
        raise ValueError("summary is required")
    if not resolved_instructions:
        raise ValueError("instruction_text is required")
    skill_dir = root.expanduser()
    if resolved_category:
        skill_dir = skill_dir / resolved_category
    skill_dir = skill_dir / resolved_skill_id
    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_file = skill_dir / "SKILL.md"
    if skill_file.exists() and not overwrite:
        raise FileExistsError(skill_file)
    skill_file.write_text(
        _render_skill_markdown(
            skill_id=resolved_skill_id,
            display_name=resolved_display_name,
            summary=resolved_summary,
            instruction_text=resolved_instructions,
            source_kind=source_kind,
        ),
        encoding="utf-8",
    )
    return skill_dir


def materialize_skill_package(
    root: Path,
    source_path: Path,
    *,
    source_bucket: str,
    install_provenance: InstalledSkillProvenance | None = None,
    overwrite: bool = True,
) -> Path:
    resolved_bucket = _validated_segment(source_bucket, field_name="source_bucket")
    definition = load_skill_package_definition(source_path)
    resolved_skill_id = _validated_segment(definition.skill_id, field_name="skill_id")
    source_entry = Path(definition.entry_path).expanduser().resolve()
    source_dir = source_entry.parent
    target_dir = root.expanduser() / resolved_bucket / resolved_skill_id
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if target_dir.exists():
        if not overwrite:
            return target_dir
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir)
    if install_provenance is not None:
        _write_install_provenance(target_dir / "SKILL.md", install_provenance)
    return target_dir


def _validated_segment(value: str | None, *, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} is required")
    resolved = value.strip().lower()
    if not resolved:
        raise ValueError(f"{field_name} is required")
    if not _VALID_SEGMENT_RE.match(resolved):
        raise ValueError(
            f"{field_name} must use lowercase letters, digits, dots, underscores, or hyphens: {value!r}"
        )
    return resolved


def _render_skill_markdown(
    *,
    skill_id: str,
    display_name: str,
    summary: str,
    instruction_text: str,
    source_kind: str,
) -> str:
    lines = [
        "---",
        f"name: {display_name}",
        f"skill_id: {skill_id}",
        f"description: {summary}",
        "version: 1.0.0",
        f"source_kind: {source_kind}",
        "---",
        "",
        f"# {display_name}",
        "",
        instruction_text.rstrip(),
        "",
    ]
    return "\n".join(lines)


def _write_install_provenance(skill_file: Path, install_provenance: InstalledSkillProvenance) -> None:
    text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter_block(text)
    for key, value in install_provenance.to_metadata().items():
        normalized = str(value).strip()
        if normalized:
            frontmatter[key] = normalized
    skill_file.write_text(_render_frontmatter_block(frontmatter, body), encoding="utf-8")


def _split_frontmatter_block(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return ({}, text)
    closing = text.find("\n---\n", 4)
    if closing == -1:
        return ({}, text)
    payload: dict[str, str] = {}
    for raw_line in text[4:closing].splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        payload[key.strip()] = value.strip()
    return payload, text[closing + len("\n---\n") :]


def _render_frontmatter_block(frontmatter: dict[str, str], body: str) -> str:
    lines = ["---"]
    lines.extend(f"{key}: {value}" for key, value in frontmatter.items())
    lines.extend(["---", ""])
    stripped_body = body.lstrip("\n").rstrip()
    if stripped_body:
        lines.append(stripped_body)
        lines.append("")
    return "\n".join(lines)
