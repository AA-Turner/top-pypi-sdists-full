"""Basic connectivity utilities for mesh nodes."""

from __future__ import annotations

from collections import deque
from typing import Iterable, Set

class Node:
    """Simple graph node."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.connections: Set[Node] = set()

    def connect(self, other: "Node") -> None:
        self.connections.add(other)
        other.connections.add(self)

def verify_connectivity(nodes: Iterable[Node]) -> bool:
    """Return True if all nodes are reachable from the first node."""
    node_list = list(nodes)
    if not node_list:
        return True
    visited: Set[Node] = set()
    q: deque[Node] = deque([node_list[0]])
    while q:
        n = q.popleft()
        if n in visited:
            continue
        visited.add(n)
        q.extend(n.connections - visited)
    return len(visited) == len(node_list)
