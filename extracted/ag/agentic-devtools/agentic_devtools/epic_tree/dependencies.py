"""Blocking-reference resolution with cycle detection and topological sort."""

from __future__ import annotations

import heapq
from collections.abc import Sequence

from .errors import UnresolvedRefError
from .models import EpicTree, IssueNode
from .ordering import creation_sequence


def build_dependency_graph(tree: EpicTree) -> dict[str, set[str]]:
    """Build a directed dependency graph from blockedBy/blocks declarations.

    Edges point from blocker to blocked (A blocks B → edge A→B).
    ``blockedBy`` and ``blocks`` are treated as complementary: if A.blocks
    contains B, that's equivalent to B.blockedBy containing A.

    Args:
        tree: A validated EpicTree instance.

    Returns:
        Dict mapping each ref to the set of refs it blocks (outgoing edges).

    Raises:
        UnresolvedRefError: If a referenced ref does not exist in the tree.
            Subclass of KeyError for backward compatibility.
    """
    all_nodes = creation_sequence(tree)
    ref_set = {node.ref for node in all_nodes}

    # adjacency: blocker → set of blocked refs
    graph: dict[str, set[str]] = {node.ref: set() for node in all_nodes}

    for node in all_nodes:
        # node.blocks: this node blocks those refs
        for blocked_ref in node.blocks:
            if blocked_ref not in ref_set:
                raise UnresolvedRefError(
                    f"Unresolved ref '{blocked_ref}' in blocks of '{node.ref}'",
                    unresolved_ref=blocked_ref,
                    declaring_ref=node.ref,
                    direction="blocks",
                )
            graph[node.ref].add(blocked_ref)

        # node.blockedBy: this node is blocked by those refs
        for blocker_ref in node.blockedBy:
            if blocker_ref not in ref_set:
                raise UnresolvedRefError(
                    f"Unresolved ref '{blocker_ref}' in blockedBy of '{node.ref}'",
                    unresolved_ref=blocker_ref,
                    declaring_ref=node.ref,
                    direction="blockedBy",
                )
            graph[blocker_ref].add(node.ref)

    return graph


def _canonicalize_cycle(chain: list[str]) -> list[str]:
    """Canonicalize a closed cycle chain.

    Applies rotation so the lexicographically smallest ref is first (and last).
    The traversal direction is preserved so every consecutive hop in the
    returned chain corresponds to a real edge in the directed graph.
    """
    if len(chain) <= 2:
        # Self-loop ['A', 'A'] — already canonical
        return chain

    # Open chain (drop closing element)
    open_chain = chain[:-1]

    # Rotate so the smallest ref is first, preserving edge direction
    min_idx = open_chain.index(min(open_chain))
    rotated = open_chain[min_idx:] + open_chain[:min_idx]
    return rotated + [rotated[0]]


def _find_one_cycle_in_scc(sub_graph: dict[str, list[str]], start: str) -> list[str]:
    """Find one representative cycle in an SCC via iterative DFS, linear in SCC size.

    Follows neighbors in lexicographic order for determinism.  Guaranteed to
    find a cycle because every node in a non-trivial SCC can reach the start
    node.

    Args:
        sub_graph: Adjacency dict restricted to SCC nodes (neighbor lists sorted).
        start: Starting node (typically the lex-smallest node in the SCC).

    Returns:
        A closed cycle chain ``[start, ..., start]`` of length ≥ 3.
    """
    path: list[str] = [start]
    path_set: set[str] = {start}
    adj_idx: dict[str, int] = {start: 0}
    dfs_stack: list[str] = [start]

    while dfs_stack:
        current = dfs_stack[-1]
        neighbors = sub_graph[current]
        idx = adj_idx[current]

        advanced = False
        while idx < len(neighbors):
            neighbor = neighbors[idx]
            idx += 1
            adj_idx[current] = idx

            if neighbor == start and len(path) > 1:
                return path + [start]

            if neighbor not in path_set:
                dfs_stack.append(neighbor)
                path.append(neighbor)
                path_set.add(neighbor)
                adj_idx[neighbor] = 0
                advanced = True
                break

        if not advanced:
            dfs_stack.pop()
            path.pop()
            path_set.discard(current)

    return []  # pragma: no cover — only reachable with invalid/non-trivial SCC input


def detect_cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    """Detect cycles in the dependency graph using Tarjan's SCC algorithm.

    For each cyclic SCC, extracts one canonical representative cycle (closed
    chain where start == end) using a linear-time DFS.

    Args:
        graph: Adjacency dict (ref → set of refs it blocks).

    Returns:
        List of closed cycle chains (one per cyclic SCC), lexicographically
        sorted. Empty if acyclic.
    """
    # --- Tarjan's SCC ---
    index_map: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    counter: list[int] = [0]
    sccs: list[list[str]] = []

    def strongconnect(v: str) -> None:
        index_map[v] = counter[0]
        lowlink[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        for w in sorted(graph.get(v, set())):
            if w not in index_map:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index_map[w])

        if lowlink[v] == index_map[v]:
            scc: list[str] = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.append(w)
                if w == v:
                    break
            # A non-trivial SCC (size > 1) is always a cycle.
            # A singleton SCC is a cycle only if the node has a self-loop.
            if len(scc) > 1 or (len(scc) == 1 and scc[0] in graph.get(scc[0], set())):
                sccs.append(scc)

    for v in sorted(graph.keys()):
        if v not in index_map:
            strongconnect(v)

    # --- Find representative cycle for each SCC ---
    result: list[list[str]] = []
    for scc in sccs:
        scc_set = set(scc)

        # Self-loop case
        if len(scc) == 1:
            node = scc[0]
            result.append([node, node])
            continue

        # Build subgraph for this SCC
        sub_graph: dict[str, list[str]] = {}
        for node in sorted(scc_set):
            sub_graph[node] = sorted(n for n in graph.get(node, set()) if n in scc_set)

        # Extract one representative cycle (linear in SCC size)
        start = sorted(scc_set)[0]
        candidate = _find_one_cycle_in_scc(sub_graph, start)
        result.append(_canonicalize_cycle(candidate))

    # Sort outer list lexicographically
    result.sort()
    return result


def build_hierarchy_edges(tree: EpicTree) -> dict[str, set[str]]:
    """Build parent-before-child hierarchy edges for *tree*.

    Returns a graph mapping each ref to the set of its direct children's refs
    (epic → features, feature → subtasks).  Edge direction matches
    :func:`build_dependency_graph`: an edge ``u → v`` means *u* must be created
    before *v*.

    Args:
        tree: A validated EpicTree instance.

    Returns:
        Dict mapping each ref to the set of refs of its direct children.
    """
    all_nodes = creation_sequence(tree)
    edges: dict[str, set[str]] = {node.ref: set() for node in all_nodes}

    epic = tree.epic
    for feature in epic.features:
        edges[epic.ref].add(feature.ref)
        for subtask in feature.subtasks:
            edges[feature.ref].add(subtask.ref)

    return edges


def build_combined_graph(tree: EpicTree) -> dict[str, set[str]]:
    """Build the combined hierarchy-and-blocking precedence graph (FR-003).

    Augments the blocking graph from :func:`build_dependency_graph`
    (blocker-before-blocked) with parent-before-child hierarchy edges from
    :func:`build_hierarchy_edges`.  The union of both edge sets defines the
    precedence constraints the creation pipeline must respect.

    Args:
        tree: A validated EpicTree instance.

    Returns:
        Dict mapping each ref to the union of its blocking and hierarchy
        outgoing edges.

    Raises:
        UnresolvedRefError: If a blocking reference does not exist in the tree.
    """
    graph = build_dependency_graph(tree)
    hierarchy = build_hierarchy_edges(tree)
    for ref, children in hierarchy.items():
        graph.setdefault(ref, set()).update(children)
    return graph


def topological_sort_graph(
    graph: dict[str, set[str]],
    creation_sequence: Sequence[IssueNode],
) -> list[IssueNode]:
    """Topologically sort *graph* using creation-sequence positions as tiebreak.

    Reuses :func:`detect_cycles` to fail closed on any cycle (reporting *every*
    detected cycle) and applies Kahn's algorithm with the node's zero-based
    position in *creation_sequence* as the sole deterministic tie-breaker among
    eligible nodes.  The global ``order`` field is intentionally **not**
    reapplied here — sibling ordering is already baked into the creation
    sequence.

    Args:
        graph: Adjacency dict (ref → set of refs that must follow it).
        creation_sequence: Nodes in deterministic depth-first pre-order; supplies
            the positional tie-breaker and the returned node instances.

    Returns:
        A list of the supplied nodes in dependency-safe, deterministic order.

    Raises:
        ValueError: If *graph* contains one or more cycles.  The message lists
            every detected cycle.
    """
    positions = {item.ref: idx for idx, item in enumerate(creation_sequence)}
    ref_to_node = {item.ref: item for item in creation_sequence}

    cycles = detect_cycles(graph)
    if cycles:
        rendered = "; ".join(" \u2192 ".join(cycle) for cycle in cycles)
        raise ValueError(f"Combined dependency graph contains cycle(s): {rendered}")

    # Fallback tiebreak position for refs absent from creation_sequence.
    default_position = len(positions)

    def _position(ref: str) -> tuple[int, str]:
        return (positions.get(ref, default_position), ref)

    # Seed every sequence node as degree-0 so nodes absent from *graph* are not
    # silently dropped; graph edges then adjust the degrees as normal.
    in_degree: dict[str, int] = {item.ref: 0 for item in creation_sequence}
    for ref, successors in graph.items():
        in_degree.setdefault(ref, 0)
        for succ in successors:
            in_degree[succ] = in_degree.get(succ, 0) + 1

    heap: list[tuple[tuple[int, str], str]] = []
    for ref, deg in in_degree.items():
        if deg == 0:
            heapq.heappush(heap, (_position(ref), ref))

    result: list[IssueNode] = []
    while heap:
        _, current = heapq.heappop(heap)
        if current not in ref_to_node:
            raise ValueError(f"Graph ref {current!r} is absent from creation_sequence.")
        result.append(ref_to_node[current])
        for neighbor in sorted(graph.get(current, set())):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, (_position(neighbor), neighbor))

    if len(result) != len(in_degree):
        # Should be unreachable because detect_cycles already fired, but keep a
        # defensive guard so a partial sort is never returned silently.
        raise ValueError(  # pragma: no cover
            "Combined dependency graph is unorderable (cycle detected during sort)."
        )

    return result


def topological_sort(tree: EpicTree) -> list[IssueNode]:
    """Produce a global topological ordering of all tree nodes.

    Uses Kahn's algorithm with a composite tiebreaker:
    ``(order if order is not None else float('inf'), positional_index)``
    so nodes with explicit ``order`` precede unordered nodes.

    Args:
        tree: A validated EpicTree instance.

    Returns:
        Flat list of all nodes in dependency-respecting order.

    Raises:
        ValueError: If the dependency graph contains a cycle.
    """
    all_nodes = creation_sequence(tree)
    ref_to_node: dict[str, IssueNode] = {node.ref: node for node in all_nodes}
    # Tiebreaker: (order ?? inf, positional_index)
    ref_to_priority: dict[str, tuple[float, int]] = {
        node.ref: (node.order if node.order is not None else float("inf"), idx) for idx, node in enumerate(all_nodes)
    }

    graph = build_dependency_graph(tree)

    # Compute in-degrees
    in_degree: dict[str, int] = {ref: 0 for ref in graph}
    for ref, blocked_set in graph.items():
        for blocked in blocked_set:
            in_degree[blocked] = in_degree.get(blocked, 0) + 1

    # Kahn's with global priority queue (min-heap keyed by tiebreaker tuple)
    heap: list[tuple[tuple[float, int], str]] = []
    for ref, deg in in_degree.items():
        if deg == 0:
            heapq.heappush(heap, (ref_to_priority[ref], ref))

    result: list[IssueNode] = []
    while heap:
        _, current = heapq.heappop(heap)
        result.append(ref_to_node[current])

        for neighbor in sorted(graph.get(current, set())):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, (ref_to_priority[neighbor], neighbor))

    if len(result) != len(all_nodes):
        cycles = detect_cycles(graph)
        if cycles:
            cycle_chain = " \u2192 ".join(cycles[0])
        else:
            cycle_chain = "unknown cycle"
        raise ValueError(f"Dependency graph contains cycle(s): {cycle_chain}")

    return result
