from __future__ import annotations

import heapq
import sys
from dataclasses import dataclass
from typing import Dict, Iterator, List, Set, Tuple

from graphlib import CycleError, TopologicalSorter

from .models import (
    Action,
    CheckAction,
    LabelAction,
    NotificationChannelAction,
    TableConfigAction,
)


# A stable identity for one piece of server state. Tuples so keys are hashable,
# comparable, and readable in error messages.
ResourceKey = Tuple[str, ...]


def table_config_key(table_ref: str) -> ResourceKey:
    return ("table_config", table_ref)


def check_key(table_ref: str, check_ref: str, is_system_check: bool) -> ResourceKey:
    # System and user checks share a ref namespace but are distinct resources with
    # different apply paths, so they must not collide on one key.
    kind = "system_check" if is_system_check else "check"
    return (kind, table_ref, check_ref)


def _labels_key(table_ref: str, check_ref: str | None) -> ResourceKey:
    if check_ref:
        return ("check_labels", table_ref, check_ref)
    return ("table_labels", table_ref)


def _channels_key(table_ref: str, check_ref: str | None) -> ResourceKey:
    if check_ref:
        return ("check_channels", table_ref, check_ref)
    return ("table_channels", table_ref)


def resource_key(action: Action) -> ResourceKey:
    """The piece of server state this action writes."""
    if isinstance(action, TableConfigAction):
        return table_config_key(action.table_ref)
    if isinstance(action, CheckAction):
        return check_key(action.table_ref, action.check_ref, action.is_system_check)
    if isinstance(action, LabelAction):
        return _labels_key(action.table_ref, action.check_ref)
    if isinstance(action, NotificationChannelAction):
        return _channels_key(action.table_ref, action.check_ref)
    raise TypeError(f"No resource key defined for {type(action).__name__}")


def required_resources(action: Action) -> Tuple[ResourceKey, ...]:
    """State that must already exist before this action can be applied.

    Keys naming state the plan does not touch are dropped when the graph is built,
    so it is safe to declare a dependency that is already satisfied on the server.
    """
    if isinstance(action, TableConfigAction):
        return ()
    if isinstance(action, CheckAction):
        # A check cannot be created or updated before its table is configured.
        return (table_config_key(action.table_ref),)
    if isinstance(action, (LabelAction, NotificationChannelAction)):
        if not action.check_ref:
            return (table_config_key(action.table_ref),)
        # Attaching to a check requires the check to exist and to have an id.
        # Bind the variant this action actually targets: machine.py only stamps
        # check_id on actions for system checks, and apply-time resolution
        # (_resolve_check_id) prefers the ref-based user-check lookup otherwise.
        # Depending on both variants would make a failed system check skip
        # label work for a healthy user check with the same ref, and vice versa.
        is_system_check = action.check_id is not None
        return (
            check_key(
                action.table_ref, action.check_ref, is_system_check=is_system_check
            ),
            table_config_key(action.table_ref),
        )
    raise TypeError(f"No dependencies defined for {type(action).__name__}")


@dataclass
class PlanNode:
    key: ResourceKey
    action: Action
    depends_on: Set[ResourceKey]
    # Position in the order the planner emitted actions. Used to break ties so a
    # plan is reproducible and diffs stay stable between runs.
    emitted_at: int


class Plan:
    """Actions ordered so each one follows the state it depends on.

    Replaces the previous contract, where apply order was whatever order
    `_compute_actions` happened to append in — a code-layout convention that no
    test asserted and that four separate bug fixes had to nudge by hand.
    """

    def __init__(self, nodes: List[PlanNode]) -> None:
        self.nodes = nodes

    def __len__(self) -> int:
        return len(self.nodes)

    def __iter__(self) -> Iterator[PlanNode]:
        return iter(self.nodes)

    @property
    def actions(self) -> List[Action]:
        return [node.action for node in self.nodes]

    def dependents_of(self, key: ResourceKey) -> Set[ResourceKey]:
        """Every key that transitively depends on `key`."""
        dependents: Set[ResourceKey] = set()
        frontier = {key}
        while frontier:
            current = frontier.pop()
            for node in self.nodes:
                if current in node.depends_on and node.key not in dependents:
                    dependents.add(node.key)
                    frontier.add(node.key)
        return dependents


def build_plan(actions: List[Action]) -> Plan:
    """Order actions by their declared dependencies.

    Ties are broken by the order the planner emitted them, so a plan whose actions
    already satisfy their dependencies comes back unchanged.
    """
    nodes: Dict[ResourceKey, PlanNode] = {}
    for index, action in enumerate(actions):
        key = resource_key(action)
        if key in nodes:
            # Two actions writing one resource is a planner bug, but dropping an
            # action would silently lose a change. Keep both, distinctly keyed.
            key = key + (str(index),)
        nodes[key] = PlanNode(
            key=key, action=action, depends_on=set(), emitted_at=index
        )

    for node in nodes.values():
        node.depends_on = {
            required
            for required in required_resources(node.action)
            if required in nodes and required != node.key
        }

    graph = {key: node.depends_on for key, node in nodes.items()}
    try:
        ordered_keys = _stable_topological_order(graph, nodes)
    except CycleError as e:
        # Unreachable with the current edges, which are acyclic by construction.
        # Falling back beats aborting a customer's apply over a planner bug.
        print(
            f"Warning: Could not order changes by dependency ({e}); "
            "applying them in the order they were computed",
            file=sys.stderr,
        )
        return Plan(list(nodes.values()))

    return Plan([nodes[key] for key in ordered_keys])


def _stable_topological_order(
    graph: Dict[ResourceKey, Set[ResourceKey]], nodes: Dict[ResourceKey, PlanNode]
) -> List[ResourceKey]:
    """Always take the earliest-emitted action that is ready.

    Draining a whole `get_ready()` batch before asking for more would group the plan
    by dependency depth — every table's configuration first, then every check —
    which reorders plans that were already correct. Re-checking after each choice
    keeps a valid plan byte-identical to the order it was emitted in.
    """
    sorter = TopologicalSorter(graph)
    sorter.prepare()
    ready: List[Tuple[int, ResourceKey]] = []

    def _offer(keys: Tuple[ResourceKey, ...]) -> None:
        for key in keys:
            heapq.heappush(ready, (nodes[key].emitted_at, key))

    _offer(sorter.get_ready())
    ordered: List[ResourceKey] = []
    while ready:
        _, key = heapq.heappop(ready)
        ordered.append(key)
        sorter.done(key)
        _offer(sorter.get_ready())
    return ordered
