"""Human-readable manifest paths; never resolve or fetch the referenced files."""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any


@dataclass
class _Directory:
    directories: dict[str, _Directory] = field(default_factory=dict)
    files: list[str] = field(default_factory=list)


def _visible(value: str) -> str:
    """Escape controls and Unicode format characters; keep ordinary names readable."""
    return "".join(
        json.dumps(char)[1:-1] if unicodedata.category(char) in ("Cc", "Cf", "Zl", "Zp") else char
        for char in value
    )


def _path(entry: Any) -> tuple[str, list[str]] | None:
    if not isinstance(entry, dict):
        return None
    path = entry.get("file_path") or entry.get("object_path")
    if not isinstance(path, str) or not path:
        return None
    uri = re.match(r"^([a-zA-Z][a-zA-Z0-9+.-]*://[^/]+/)(.*)$", path, re.DOTALL)
    if uri:
        root, path = uri.groups()
    elif "://" in path:
        return None
    elif path.startswith("/"):
        root, path = "/", path[1:]
    else:
        root = ""
    parts = path.split("/")
    # Unusual paths remain verbatim instead of being silently normalized.
    if any(part in ("", ".", "..") for part in parts):
        return None
    return root, parts


def _tree(directory: _Directory) -> list[str]:
    lines: list[str] = []
    pending: list[tuple[_Directory | str, str]] = [(directory, "")]
    # Iterative traversal also supports paths deeper than Python's recursion limit.
    while pending:
        node, prefix = pending.pop()
        if isinstance(node, str):
            lines.append(node)
            continue
        children = [(name + "/", child) for name, child in sorted(node.directories.items())]
        children.extend((name, None) for name in sorted(node.files))
        for index in range(len(children) - 1, -1, -1):
            name, child = children[index]
            last = index == len(children) - 1
            if child is not None:
                pending.append((child, prefix + ("    " if last else "│   ")))
            pending.append((prefix + ("└── " if last else "├── ") + _visible(name), ""))
    return lines


def manifest_lines(manifest: list[Any]) -> list[str]:
    """Group by storage root and show a lossless hierarchy of file paths.

    Entries without usable paths retain their original values in a separate block.
    Full metadata remains available through the command's JSON/YAML output.
    """
    groups: dict[str, list[list[str]]] = {}
    other: list[Any] = []
    for entry in manifest:
        path = _path(entry)
        if path is None:
            other.append(entry)
        else:
            root, parts = path
            groups.setdefault(root, []).append(parts)

    count = sum(len(paths) for paths in groups.values())
    lines = [f"manifest: {count} {'file' if count == 1 else 'files'}"]
    for root, paths in sorted(groups.items()):
        common: list[str] = []
        for parts in zip(*(path[:-1] for path in paths)):
            if len(set(parts)) != 1:
                break
            common.append(parts[0])
        shared_root = root + "/".join(common) + ("/" if common else "")
        lines.append(f"root: {_visible(shared_root or './')}")
        directory = _Directory()
        for parts in paths:
            node = directory
            for part in parts[len(common) : -1]:
                node = node.directories.setdefault(part, _Directory())
            node.files.append(parts[-1])
        lines.extend(_tree(directory))
    if other:
        lines.append(f"other entries: {len(other)}")
        for entry in other:
            lines.append("  " + _visible(json.dumps(entry, ensure_ascii=False, default=str)))
    return lines
