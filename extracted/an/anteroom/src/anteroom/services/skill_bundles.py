"""Shared helpers for skill frontmatter and bundled resources."""

from __future__ import annotations

import stat
from pathlib import Path
from typing import Any

import yaml

_RESOURCE_EXTENSIONS = frozenset({".md", ".txt", ".yaml", ".yml", ".json", ".xml", ".csv", ".py", ".js", ".ts", ".sh"})


def _is_symlink(path: Path) -> bool:
    """Check if *path* is a symlink using lstat (never follows the link)."""
    try:
        return stat.S_ISLNK(path.lstat().st_mode)
    except OSError:
        return False


def _extract_yaml_frontmatter(text: str, path: Path) -> tuple[str, dict[str, Any]]:
    """Extract YAML front matter from Markdown text."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return text, {}

    first_newline = text.index("\n")
    close_idx = text.find("\n---\n", first_newline)
    close_len = 4
    if close_idx == -1:
        close_idx = text.find("\n---\r\n", first_newline)
        close_len = 5
    if close_idx == -1:
        stripped = text.rstrip()
        if stripped.endswith("\n---") or stripped.endswith("\r\n---"):
            close_idx = stripped.rfind("\n---")
            close_len = len(stripped) - close_idx
        else:
            msg = f"Unclosed front matter in {path}: opening '---' found but no closing '---'"
            raise ValueError(msg)

    yaml_block = text[first_newline + 1 : close_idx]
    body = text[close_idx + close_len + 1 :] if close_idx + close_len < len(text) else ""

    try:
        data = yaml.safe_load(yaml_block)
    except yaml.YAMLError as e:
        msg = f"Invalid YAML in front matter of {path}: {e}"
        raise ValueError(msg) from e

    if data is None:
        return body, {}

    if not isinstance(data, dict):
        msg = f"Front matter in {path} must be a YAML mapping, got {type(data).__name__}"
        raise ValueError(msg)

    return body, data


def _parse_resource_list_from_frontmatter(content: str, skill_path: Path) -> list[str]:
    """Extract ``resources:`` list from SKILL.md frontmatter."""
    if not content.startswith("---\n") and not content.startswith("---\r\n"):
        return []
    try:
        _body, meta = _extract_yaml_frontmatter(content, skill_path)
    except ValueError:
        return []
    raw = meta.get("resources")
    if not raw or not isinstance(raw, list):
        return []
    return [str(r) for r in raw if isinstance(r, str) and r]


def _resolve_bundle_resources(
    skill_dir: Path,
    resource_list: list[str],
    boundary_dir: Path,
) -> list[tuple[str, str]]:
    """Resolve and read declared resource files for a bundled skill."""
    resolved_boundary = boundary_dir.resolve()
    results: list[tuple[str, str]] = []
    for rel_path in resource_list:
        raw_candidate = skill_dir / rel_path
        candidate = raw_candidate.resolve()
        if _is_symlink(raw_candidate):
            msg = f"Symlink not allowed for resource: {rel_path}"
            raise ValueError(msg)
        if not candidate.is_relative_to(resolved_boundary):
            msg = f"Path traversal blocked for resource: {rel_path}"
            raise ValueError(msg)
        if not candidate.is_file():
            msg = f"Declared resource not found: {rel_path}"
            raise ValueError(msg)
        if candidate.suffix not in _RESOURCE_EXTENSIONS:
            msg = f"Unsupported resource extension: {rel_path} (allowed: {', '.join(sorted(_RESOURCE_EXTENSIONS))})"
            raise ValueError(msg)
        raw = candidate.read_bytes()
        if b"\x00" in raw[:512]:
            msg = f"Binary file not allowed as resource: {rel_path}"
            raise ValueError(msg)
        results.append((rel_path, raw.decode("utf-8")))
    return results


def _inline_resources(skill_content: str, resources: list[tuple[str, str]]) -> str:
    """Append resource files as a structured section after skill content."""
    if not resources:
        return skill_content
    parts = [skill_content.rstrip(), "\n\n<bundled_resources>"]
    for rel_path, content in resources:
        parts.append(f'\n<resource path="{rel_path}">')
        parts.append(content)
        parts.append("</resource>")
    parts.append("\n</bundled_resources>\n")
    return "\n".join(parts)
