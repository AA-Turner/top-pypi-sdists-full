"""Deterministic ordering resolution for epic-tree nodes."""

from __future__ import annotations

from collections.abc import Sequence

from .models import EpicNode, EpicTree, FeatureNode, IssueNode, SubtaskNode


def resolve_sibling_order(nodes: Sequence[IssueNode]) -> list[IssueNode]:
    """Sort sibling nodes by explicit order then document order.

    Accepts any :class:`~collections.abc.Sequence` (list, tuple, etc.) and
    returns a **new** list containing the same object references in resolved
    order (no cloning).

    Sorting rules:

    1. Nodes with an explicit ``order`` value form the head of the result,
       sorted ascending by that value.
    2. Nodes without an explicit ``order`` are appended after the explicit
       group, preserving their original document order (position in the input
       sequence).
    3. When two or more nodes share the same explicit ``order`` value, their
       relative order is determined by document order (stable tiebreak).

    Args:
        nodes: Sibling nodes in document order. May be a list, tuple, or any
            other :class:`~collections.abc.Sequence` of :class:`IssueNode`.

    Returns:
        New list of nodes in resolved order. The returned objects are the same
        references as the input (identity is preserved).
    """
    explicit: list[tuple[int, int, IssueNode]] = []
    implicit: list[tuple[int, IssueNode]] = []

    for idx, node in enumerate(nodes):
        if node.order is not None:
            explicit.append((node.order, idx, node))
        else:
            implicit.append((idx, node))

    # Sort explicit by (order_value, document_index)
    explicit.sort(key=lambda x: (x[0], x[1]))

    result: list[IssueNode] = [item[2] for item in explicit]
    result.extend(item[1] for item in implicit)
    return result


def creation_sequence(tree: EpicTree) -> list[IssueNode]:
    """Produce a flat list of all nodes in depth-first pre-order traversal.

    Performs a depth-first pre-order traversal of the epic tree. At each
    level, siblings are visited in resolved order (see
    :func:`resolve_sibling_order`). The epic root is always the first element
    in the returned list.

    Args:
        tree: A fully loaded :class:`EpicTree` instance.

    Returns:
        Flat list of all :class:`IssueNode` instances in creation sequence
        order. For an epic with no features, returns a single-element list
        containing only the epic node.
    """
    result: list[IssueNode] = []
    _visit_epic(tree.epic, result)
    return result


def _visit_epic(epic: EpicNode, result: list[IssueNode]) -> None:
    """Visit the epic node and its features in resolved order."""
    result.append(epic)
    ordered_features = resolve_sibling_order(list(epic.features))
    for feature in ordered_features:
        if not isinstance(feature, FeatureNode):
            msg = f"Expected FeatureNode, got {type(feature).__name__}"
            raise TypeError(msg)
        _visit_feature(feature, result)


def _visit_feature(feature: FeatureNode, result: list[IssueNode]) -> None:
    """Visit a feature node and its subtasks in resolved order."""
    result.append(feature)
    ordered_subtasks = resolve_sibling_order(list(feature.subtasks))
    for subtask in ordered_subtasks:
        if not isinstance(subtask, SubtaskNode):
            msg = f"Expected SubtaskNode, got {type(subtask).__name__}"
            raise TypeError(msg)
        result.append(subtask)


def get_sibling_position(node: IssueNode, resolved_siblings: Sequence[IssueNode]) -> tuple[int, int]:
    """Return the 1-based position and total count for a node in a resolved sibling list.

    Uses Python object identity (``is``) to locate the node, not equality.
    This means a different object with the same field values will **not** match.

    Args:
        node: The node to find.
        resolved_siblings: The resolved sibling list (typically the output of
            :func:`resolve_sibling_order`).

    Returns:
        A tuple ``(position, total)`` where *position* is 1-based and *total*
        is the length of *resolved_siblings*.

    Raises:
        ValueError: If *node* is not present in *resolved_siblings* (by
            identity).
    """
    total = len(resolved_siblings)
    for idx, sibling in enumerate(resolved_siblings):
        if sibling is node:
            return (idx + 1, total)
    msg = (
        f"Node ref {node.ref!r} is not present in the sibling list among {total} siblings "
        "(identity-based lookup: a different object with the same field values will not match)"
    )
    raise ValueError(msg)
