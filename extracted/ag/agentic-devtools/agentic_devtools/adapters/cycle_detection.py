"""Cycle detection utility for dependency graphs.

Provides DFS-based topological sort that rejects circular dependencies
with descriptive error messages identifying the cycle path.
"""

from __future__ import annotations


class CycleDetectedError(Exception):
    """Raised when a circular dependency is detected.

    Attributes:
        cycle: List of node identifiers forming the cycle.
    """

    def __init__(self, cycle: list[str]) -> None:
        self.cycle = cycle
        cycle_str = " -> ".join(cycle)
        super().__init__(f"Circular dependency detected: {cycle_str}")


def detect_cycles(edges: list[tuple[str, str]]) -> list[str]:
    """Perform topological sort and detect cycles in a directed graph.

    Uses DFS-based topological sort.  If a cycle is detected, raises
    :class:`CycleDetectedError` with the cycle path.

    Args:
        edges: List of (source, target) directed edges where source must come
            before target in the resulting order (for example, source is a
            prerequisite of target).

    Returns:
        A topologically sorted list of node identifiers (no cycle).

    Raises:
        CycleDetectedError: If a circular dependency is found.
    """
    # Build adjacency list
    graph: dict[str, list[str]] = {}
    all_nodes: set[str] = set()
    for source, target in edges:
        all_nodes.add(source)
        all_nodes.add(target)
        graph.setdefault(source, []).append(target)
        graph.setdefault(target, [])

    # DFS-based topological sort with cycle detection
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {node: WHITE for node in all_nodes}
    order: list[str] = []
    path: list[str] = []

    def dfs(node: str) -> None:
        color[node] = GRAY
        path.append(node)
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
                # Found a cycle - extract the cycle path
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                raise CycleDetectedError(cycle)
            if color[neighbor] == WHITE:
                dfs(neighbor)
        path.pop()
        color[node] = BLACK
        order.append(node)

    for node in sorted(all_nodes):
        if color[node] == WHITE:
            dfs(node)

    order.reverse()
    return order
