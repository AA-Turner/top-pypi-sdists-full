"""Markdown parsing and manifest rendering for injected resources."""

from __future__ import annotations

import yaml

from agentic_devtools.skill_injector_models import InjectionPlan
from agentic_devtools.skill_injector_paths import (
    _SKILLS_KIND,
    _SKILLS_MANIFEST_MARKER,
)


def _derive_fallback_description_from_markdown(content: str) -> str | None:
    """Derive a short description from Markdown *content*.

    Prefers the first heading line (``#``-prefixed); otherwise uses the first
    non-empty line. Returns ``None`` when no suitable line is found.
    """
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                return heading
        else:
            return stripped
    return None


def _parse_frontmatter(content: str) -> dict[str, object]:
    """Extract YAML front-matter from *content*.

    Returns a dictionary of parsed front-matter keys. When no valid
    front-matter block is found (missing, empty, malformed, or containing
    non-mapping YAML), the returned dict may still contain a derived
    ``_agdt_fallback_description`` entry based on the first Markdown
    heading or first non-empty line in the body. If no fallback
    description can be derived, an empty dict is returned.
    """
    if not content.startswith("---"):
        # No front-matter block; derive a fallback description from the whole
        # content so callers can still present something meaningful.
        fallback = _derive_fallback_description_from_markdown(content)
        return {"_agdt_fallback_description": fallback} if fallback else {}

    # Use splitlines() so that both LF and CRLF line endings are handled
    # identically — content.find("\n---") would miss "\r\n---" on Windows.
    lines = content.splitlines()
    close_idx = next(
        (i for i, line in enumerate(lines) if i > 0 and line == "---"),
        None,
    )
    if close_idx is None:
        # Malformed front-matter; derive a fallback description from the body
        # after the opening delimiter (if any) so we do not return the leading
        # '---' line itself as the description.
        body_without_delimiter = "\n".join(lines[1:]) if len(lines) > 1 else ""
        source_for_fallback = body_without_delimiter or content
        fallback = _derive_fallback_description_from_markdown(source_for_fallback)
        return {"_agdt_fallback_description": fallback} if fallback else {}

    raw = "\n".join(lines[1:close_idx]).strip()
    body = "\n".join(lines[close_idx + 1 :])
    fallback = _derive_fallback_description_from_markdown(body) if body else None
    if not raw:
        return {"_agdt_fallback_description": fallback} if fallback else {}
    try:
        result = yaml.safe_load(raw)
        if not isinstance(result, dict):
            result = {}
    except yaml.YAMLError:
        result = {}
    if fallback and "_agdt_fallback_description" not in result:
        result["_agdt_fallback_description"] = fallback
    return result


def _extract_description(frontmatter: dict[str, object], kind: str) -> str:
    """Return a human-readable description from *frontmatter*.

    * For ``prompts``: uses the ``agent`` key.
    * For ``agents`` and ``skills``: uses the ``description`` key.

    Falls back to a derived description from the Markdown body when available,
    otherwise to ``"—"``.
    """
    if kind == "prompts":
        desc = frontmatter.get("agent")
    else:
        desc = frontmatter.get("description")
    if not desc:
        desc = frontmatter.get("_agdt_fallback_description")
    return str(desc) if desc else "\u2014"


def _generate_readme(files: list[tuple[str, str]], kind: str) -> str:
    """Produce a managed ``agdt.README.md`` for the target directory.

    Args:
        files: list of ``(filename, description)`` tuples.  For the ``skills``
            kind the first element is the skill-relative path (e.g.
            ``my-skill/SKILL.md``), which also serves as the stale-cleanup
            record read back by :func:`_read_managed_skill_manifest`.
        kind: ``"agents"``, ``"prompts"`` or ``"skills"``.
    """
    title = {
        "agents": "Managed Agent Skills",
        "prompts": "Managed Prompt Skills",
        _SKILLS_KIND: "Managed Skills",
    }.get(kind, "Managed Skill Files")
    lines = [
        f"# {title}",
        "",
    ]
    if kind == _SKILLS_KIND:
        lines.extend([_SKILLS_MANIFEST_MARKER, ""])
        body_lines: list[str] = [
            "> **This folder is managed by [agentic-devtools](https://github.com/swai-factory/agentic-devtools).**",
            "> Do **not** edit the files listed in this manifest — they are overwritten by `agdt-setup`.",
            "> Skills you author yourself are not touched.",
            "",
            "The files below are mirrored from the `agentic-devtools` package into",
            "`.agents/skills/` so that Copilot CLI and similar tools can discover and",
            "use them by convention.  They should be checked into source control, and",
            "any local edits to the managed files listed here will be overwritten the",
            "next time `agdt-setup` is run.",
            "",
        ]
    else:
        body_lines = [
            "> **This folder is managed by [agentic-devtools](https://github.com/swai-factory/agentic-devtools).**",
            "> Do **not** edit these files manually — they are overwritten by `agdt-setup`.",
            "",
            "The files below are mirrored from the `agentic-devtools` package so that",
            "Copilot CLI and similar tools can discover and use them by convention.",
            "They should be checked into source control like any other `.github`",
            "configuration, and any local edits will be overwritten the next time",
            "`agdt-setup` is run.",
            "",
        ]
    lines.extend(body_lines)
    lines.extend(
        [
            "## File Manifest",
            "",
            "| File | Description |",
            "| ---- | ----------- |",
        ]
    )
    for filename, desc in files:
        safe_desc = desc.splitlines()[0].replace("`", "'") if desc else "\u2014"
        lines.append(f"| `{filename}` | {safe_desc} |")
    lines.extend(
        [
            "",
            "## Regeneration",
            "",
            "Run `agdt-setup` to update these files.  Stale files (removed in newer",
            "package versions) are automatically cleaned up.",
            "",
        ]
    )
    return "\n".join(lines)


def _format_plans(plans: tuple[InjectionPlan, ...]) -> str:
    """Render *plans* as a human-readable manifest diff.

    Each kind gets a count header followed by three separately labelled lists
    (adds, overwrites, deletes); an empty list renders as ``(none)`` so the
    reader can tell "nothing to do" apart from "not reported".
    """
    lines: list[str] = []
    for plan in plans:
        lines.append(
            f"  Manifest diff — {plan.kind}: "
            f"{len(plan.added)} add(s), "
            f"{len(plan.overwritten)} overwrite(s), "
            f"{len(plan.deleted)} delete(s)"
        )
        for label, marker, names in (
            ("adds", "+", plan.added),
            ("overwrites", "~", plan.overwritten),
            ("deletes", "-", plan.deleted),
        ):
            lines.append(f"    {label} ({len(names)}):")
            if names:
                lines.extend(f"      {marker} {name}" for name in names)
            else:
                lines.append("      (none)")
    return "\n".join(lines)
