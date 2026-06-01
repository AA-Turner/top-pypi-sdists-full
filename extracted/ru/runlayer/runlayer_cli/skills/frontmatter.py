from __future__ import annotations

import re

_SKILL_FRONTMATTER_RE = re.compile(r"^(---\n)(.*?\n)(---\n?)", re.DOTALL)


def rewrite_skill_frontmatter_name(
    content: str,
    skill_name: str,
    *,
    fallback_description: str | None,
    insert_missing_name: bool = True,
) -> str:
    match = _SKILL_FRONTMATTER_RE.match(content)
    if match is None:
        if fallback_description is None:
            return content
        return f"---\nname: {skill_name}\ndescription: {fallback_description}\n---\n\n{content}"

    prefix, frontmatter, suffix = match.groups()
    lines = frontmatter.splitlines()
    updated = False
    next_lines: list[str] = []
    for line in lines:
        if not updated and line.startswith("name:"):
            next_lines.append(f"name: {skill_name}")
            updated = True
            continue
        next_lines.append(line)

    if not updated and insert_missing_name:
        next_lines.insert(0, f"name: {skill_name}")

    if not updated and not insert_missing_name:
        return content

    updated_frontmatter = "\n".join(next_lines)
    return f"{prefix}{updated_frontmatter}\n{suffix}{content[match.end() :]}"
