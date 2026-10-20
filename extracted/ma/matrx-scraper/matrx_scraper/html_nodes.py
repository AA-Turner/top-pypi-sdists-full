"""Removing or replacing selectolax nodes without touching freed memory.

selectolax hands back C pointers. ``decompose()`` and ``replace_with()`` free the node AND everything inside it,
so a Python ``Node`` collected earlier for one of those insides now points at freed memory, and the next call on it
is a segmentation fault that takes the whole process down (no Python exception, nothing to catch). Two ordinary
ways to hold such a node:

- **The same node twice.** A selector group returns one entry per matching selector, so an element matching two
  of them comes back twice (``a[href^="tel:"], a[href^="TEL:"]`` matches every phone link twice, because attribute
  prefixes compare case-insensitively). Replacing it the second time crashed the workflow worker and the API
  server twelve times on 2026-10-16 (Smart Add on a brewery site with one ``tel:`` link).
- **A node inside one already removed** (``<nav>`` inside ``<header>``, ``<script>`` inside ``<svg>``).

:func:`each_live_node` is the ONE way to walk a collected node list while changing the tree: every node once, in
the order given, and never one that is (or sits inside) a node an earlier step removed. Ancestry is read up front,
while every node is still alive.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any


def each_live_node(nodes: Iterable[Any], step: Callable[[Any], bool]) -> int:
    """Run ``step(node)`` on each distinct node still in the tree; ``step`` returns True when it removed or replaced
    that node. Returns how many it removed."""
    plan: list[tuple[Any, int, tuple[int, ...]]] = []
    seen: set[int] = set()
    for node in nodes:
        mem = node.mem_id
        if mem in seen:
            continue
        seen.add(mem)
        chain: list[int] = []
        parent = node.parent
        while parent is not None:
            chain.append(parent.mem_id)
            parent = parent.parent
        plan.append((node, mem, tuple(chain)))
    removed: set[int] = set()
    count = 0
    for node, mem, ancestors in plan:
        if any(a in removed for a in ancestors):
            continue
        if step(node):
            removed.add(mem)
            count += 1
    return count


def _decompose(node: Any) -> bool:
    node.decompose()
    return True


def decompose_all(nodes: Iterable[Any]) -> int:
    """Remove every node in ``nodes`` (with its insides) — each once, never one already removed."""
    return each_live_node(nodes, _decompose)


__all__ = ["decompose_all", "each_live_node"]
