"""Hierarchy metadata I/O for hierarchy.yml files.

Provides ``write_hierarchy_yml`` and ``read_hierarchy_yml`` for serializing
and deserializing ``HierarchyMetadata`` to/from YAML files in spec directories.
Non-hierarchical (standalone) issues do not receive a hierarchy.yml file.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from agentic_devtools.hierarchy.models import ChildInfo, HierarchyLevel, HierarchyMetadata


def write_hierarchy_yml(path: Path, metadata: HierarchyMetadata) -> bool:
    """Write hierarchy metadata to a hierarchy.yml file.

    Skips writing for STANDALONE issues (no parent, no children) per FR-003.

    Args:
        path: Path to write the hierarchy.yml file.
        metadata: The hierarchy metadata to serialize.

    Returns:
        True if the file was written, False if skipped (standalone).
    """
    if metadata.level == HierarchyLevel.STANDALONE:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)

    data = metadata.to_dict()
    content = yaml.dump(data, default_flow_style=False, sort_keys=False, allow_unicode=True)
    path.write_text(content, encoding="utf-8")
    return True


def read_hierarchy_yml(path: Path) -> HierarchyMetadata:
    """Read and validate a hierarchy.yml file.

    Args:
        path: Path to the hierarchy.yml file.

    Returns:
        Parsed HierarchyMetadata instance.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file content is invalid.
    """
    if not path.exists():
        msg = f"Hierarchy file not found: {path}"
        raise FileNotFoundError(msg)

    content = path.read_text(encoding="utf-8")
    if not content.strip():
        msg = f"Hierarchy file is empty: {path}"
        raise ValueError(msg)

    try:
        data: Any = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        msg = f"Malformed YAML in {path}: {exc}"
        raise ValueError(msg) from exc
    if not isinstance(data, dict):
        msg = f"Expected YAML mapping in {path}, got {type(data).__name__}"
        raise ValueError(msg)

    # Parse level
    raw_level = data.get("level")
    if not isinstance(raw_level, str):
        msg = f"Missing or invalid 'level' field in {path}"
        raise ValueError(msg)
    try:
        level = HierarchyLevel(raw_level)
    except ValueError:
        msg = f"Invalid hierarchy level '{raw_level}' in {path}. Valid: {[lv.value for lv in HierarchyLevel]}"
        raise ValueError(msg) from None

    # Parse parent
    parent = data.get("parent")
    if parent is not None:
        if isinstance(parent, (bool, float)):
            msg = f"Invalid 'parent' value in {path}: {parent!r}"
            raise ValueError(msg)
        if not isinstance(parent, int):
            try:
                parent = int(parent)
            except (ValueError, TypeError):
                msg = f"Invalid 'parent' value in {path}: {parent!r}"
                raise ValueError(msg) from None
        if parent <= 0:
            msg = f"Invalid 'parent' value in {path}: {parent!r} (must be a positive integer)"
            raise ValueError(msg)

    # Parse children
    raw_children = data.get("children", [])
    if not isinstance(raw_children, list):
        msg = f"'children' must be a list in {path}"
        raise ValueError(msg)

    children: list[ChildInfo] = []
    for entry in raw_children:
        if not isinstance(entry, dict):
            msg = f"Each child entry must be a mapping in {path}"
            raise ValueError(msg)
        number = entry.get("number")
        title = entry.get("title", "")
        if isinstance(number, (bool, float)):
            msg = f"Invalid child number in {path}: {number!r}"
            raise ValueError(msg)
        if not isinstance(number, int):
            if number is None:
                msg = f"Invalid child number in {path}: {number!r}"
                raise ValueError(msg)
            try:
                number = int(number)
            except (ValueError, TypeError):
                msg = f"Invalid child number in {path}: {number!r}"
                raise ValueError(msg) from None
        if number <= 0:
            msg = f"Invalid child number in {path}: {number!r} (must be a positive integer)"
            raise ValueError(msg)
        # Parse optional order field: absent in hierarchy.yml files written before
        # order support was added — treat missing order as None for backward compatibility.
        raw_order = entry.get("order")
        order: int | None = None
        if raw_order is not None:
            if isinstance(raw_order, bool):
                msg = f"Invalid child order in {path}: {raw_order!r}"
                raise ValueError(msg)
            if isinstance(raw_order, float):
                msg = f"Invalid child order in {path}: {raw_order!r} (must be an integer, not a float)"
                raise ValueError(msg)
            if not isinstance(raw_order, int):
                try:
                    raw_order = int(raw_order)
                except (ValueError, TypeError):
                    msg = f"Invalid child order in {path}: {raw_order!r}"
                    raise ValueError(msg) from None
            order = raw_order
        children.append(ChildInfo(number=number, title=str(title), order=order))

    # Parse informational_children
    raw_info = data.get("informational_children", [])
    if not isinstance(raw_info, list):
        msg = f"'informational_children' must be a list in {path}"
        raise ValueError(msg)

    informational_children: list[ChildInfo] = []
    for entry in raw_info:
        if not isinstance(entry, dict):
            msg = f"Each informational_children entry must be a mapping in {path}"
            raise ValueError(msg)
        number = entry.get("number")
        title = entry.get("title", "")
        if isinstance(number, (bool, float)):
            msg = f"Invalid informational child number in {path}: {number!r}"
            raise ValueError(msg)
        if not isinstance(number, int):
            if number is None:
                msg = f"Invalid informational child number in {path}: {number!r}"
                raise ValueError(msg)
            try:
                number = int(number)
            except (ValueError, TypeError):
                msg = f"Invalid informational child number in {path}: {number!r}"
                raise ValueError(msg) from None
        if number <= 0:
            msg = f"Invalid informational child number in {path}: {number!r} (must be a positive integer)"
            raise ValueError(msg)
        informational_children.append(ChildInfo(number=number, title=str(title)))

    return HierarchyMetadata(
        level=level,
        parent=parent,
        children=children,
        informational_children=informational_children,
    )
