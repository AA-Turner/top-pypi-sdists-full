"""Marker-delimited ``specs/README.md`` index generation for the nest command.

Generates a deterministic index of the nested spec hierarchy and writes it into
``specs/README.md`` between HTML comment markers, preserving any surrounding
hand-written content verbatim.
"""

from __future__ import annotations

import re
from pathlib import Path

#: Opening marker delimiting the generated index section.
INDEX_START_MARKER = "<!-- agdt-nest-index:start -->"
#: Closing marker delimiting the generated index section.
INDEX_END_MARKER = "<!-- agdt-nest-index:end -->"

_NUMERIC_DIR_PATTERN = re.compile(r"^\d+$")
_SECTION_RE = re.compile(
    re.escape(INDEX_START_MARKER) + r".*?" + re.escape(INDEX_END_MARKER),
    re.DOTALL,
)


def generate_index_section(specs_root: str | Path, max_depth: int = 3) -> str:
    """Generate the marker-delimited index section for the nested spec tree.

    Walks the numeric (already-nested) directories under ``specs_root`` in
    deterministic numeric order and renders one indented bullet per directory,
    using its ``specs/``-relative path.

    Args:
        specs_root: Path to the specs/ directory.
        max_depth: Maximum traversal depth relative to ``specs_root``.

    Returns:
        The full index section including the start and end markers.

    Raises:
        ValueError: If ``max_depth`` is not a positive integer.
    """
    if max_depth <= 0:
        raise ValueError(f"max_depth must be a positive integer, got: {max_depth}")

    specs_path = Path(specs_root)
    lines: list[str] = [INDEX_START_MARKER, "", "## Spec Hierarchy Index", ""]

    entries = _collect_entries(specs_path, max_depth)
    if entries:
        for depth, rel_path in entries:
            indent = "  " * depth
            lines.append(f"{indent}- [`{rel_path}`]({rel_path}/)")
    else:
        lines.append("_No nested specs yet._")

    lines.extend(["", INDEX_END_MARKER])
    return "\n".join(lines)


def update_readme(specs_root: str | Path, max_depth: int = 3) -> Path:
    """Create or update the marker-delimited index in ``specs/README.md``.

    Behavior:

    * Existing marker section → replaced in place, surrounding content is
      preserved verbatim.
    * README exists without markers → the section is appended.
    * README missing → the file is created containing only the section.

    Args:
        specs_root: Path to the specs/ directory.
        max_depth: Maximum traversal depth relative to ``specs_root``.

    Returns:
        Path to the written ``README.md``.
    """
    specs_path = Path(specs_root)
    readme_path = specs_path / "README.md"
    section = generate_index_section(specs_path, max_depth=max_depth)

    if not readme_path.exists():
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        readme_path.write_text(section + "\n", encoding="utf-8")
        return readme_path

    content = readme_path.read_text(encoding="utf-8")
    if _SECTION_RE.search(content):
        updated = _SECTION_RE.sub(lambda _match: section, content, count=1)
    else:
        separator = "" if content.endswith("\n") else "\n"
        updated = f"{content}{separator}\n{section}\n"

    readme_path.write_text(updated, encoding="utf-8")
    return readme_path


def _collect_entries(specs_path: Path, max_depth: int) -> list[tuple[int, str]]:
    """Collect (depth, specs-relative path) entries for numeric directories."""
    entries: list[tuple[int, str]] = []

    if not specs_path.is_dir():
        return entries

    def _walk(directory: Path, depth: int) -> None:
        if depth >= max_depth:
            return
        children = [child for child in directory.iterdir() if child.is_dir() and _NUMERIC_DIR_PATTERN.match(child.name)]
        for child in sorted(children, key=lambda path: int(path.name)):
            entries.append((depth, child.relative_to(specs_path).as_posix()))
            _walk(child, depth + 1)

    _walk(specs_path, 0)
    return entries
