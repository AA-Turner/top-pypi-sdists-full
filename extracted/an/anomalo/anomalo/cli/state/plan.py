from __future__ import annotations

import heapq
import sys
from dataclasses import dataclass
from typing import Callable, Dict, Iterator, List, Set, Tuple

from graphlib import CycleError, TopologicalSorter

from .errors import ClobberingWrite
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


def _labels_key(
    table_ref: str, check_ref: str | None, is_system_check: bool
) -> ResourceKey:
    if check_ref:
        # Distinct per variant for the same reason check_key is: the labels on a
        # system check and on a user check of one ref are two pieces of state.
        kind = "system_check_labels" if is_system_check else "check_labels"
        return (kind, table_ref, check_ref)
    return ("table_labels", table_ref)


def _channels_key(
    table_ref: str, check_ref: str | None, is_system_check: bool
) -> ResourceKey:
    if check_ref:
        kind = "system_check_channels" if is_system_check else "check_channels"
        return (kind, table_ref, check_ref)
    return ("table_channels", table_ref)


def resource_key(action: Action) -> ResourceKey:
    """The piece of server state this action writes."""
    if isinstance(action, TableConfigAction):
        return table_config_key(action.table_ref)
    if isinstance(action, CheckAction):
        return check_key(action.table_ref, action.check_ref, action.is_system_check)
    if isinstance(action, LabelAction):
        return _labels_key(action.table_ref, action.check_ref, action.is_system_check)
    if isinstance(action, NotificationChannelAction):
        return _channels_key(action.table_ref, action.check_ref, action.is_system_check)
    raise TypeError(f"No resource key defined for {type(action).__name__}")


_RESOURCE_DESCRIPTIONS = {
    "check": 'check "{1}" on table "{0}"',
    "system_check": 'system check "{1}" on table "{0}"',
}


def describe_resource(key: ResourceKey) -> str:
    """A resource key phrased for an error a customer has to act on."""
    kind, *rest = key
    template = _RESOURCE_DESCRIPTIONS.get(kind)
    if template is None:  # pragma: no cover - only prerequisites are ever described
        return " ".join(key)
    return template.format(*rest)


def write_target(action: Action) -> ResourceKey:
    """The server object this action writes.

    Usually one resource is one object, but not always: table configuration and
    table-level notification channels own different fields of the same
    `tables/<id>/config` object. They stay separate `ResourceKey`s because they are
    separate pieces of declared state — this is the coarser identity the ordering
    guard below needs.
    """
    if isinstance(action, TableConfigAction) or (
        isinstance(action, NotificationChannelAction) and not action.check_ref
    ):
        return ("table_config_object", action.table_ref)
    return resource_key(action)


def is_full_replace(action: Action) -> bool:
    """Whether applying this action overwrites every field of its write target.

    `Client.configure_table` (POST) always sends every parameter, so it blanks
    whatever the caller omitted. `PATCH tables/<id>/config` touches only the fields
    it is given.
    """
    return isinstance(action, TableConfigAction)


def required_resources(action: Action) -> Tuple[ResourceKey, ...]:
    """State this action has to be applied *after*, where the plan writes it too.

    Keys naming state the plan does not touch are dropped when the graph is built,
    so it is safe to declare a dependency that is already satisfied on the server.
    These are ordering edges; see `prerequisite_resources` for the stricter question
    of what an action cannot do without.
    """
    if isinstance(action, TableConfigAction):
        return ()
    if isinstance(action, CheckAction):
        # A check belongs to a configured table, so configuration goes first — the
        # server creates a table's system checks as a side effect of it.
        return (table_config_key(action.table_ref),)
    if isinstance(action, (LabelAction, NotificationChannelAction)):
        if not action.check_ref:
            return (table_config_key(action.table_ref),)
        # Attaching to a check requires that check to exist. Bind the variant this
        # action actually targets: depending on both would make a failed system
        # check skip label work for a healthy user check with the same ref, and
        # vice versa.
        return (
            check_key(
                action.table_ref,
                action.check_ref,
                is_system_check=action.is_system_check,
            ),
            table_config_key(action.table_ref),
        )
    raise TypeError(f"No dependencies defined for {type(action).__name__}")


def prerequisite_resources(action: Action) -> Tuple[ResourceKey, ...]:
    """The subset of `required_resources` whose absence makes an action impossible.

    Most edges are ordering, not prerequisite. A check, a table's labels and a
    table's notification channels all apply to an unconfigured table — the public
    API only requires the `Table` row to exist, and
    `test_add_notification_channel_without_prior_config_action` pins that. So a
    missing table configuration is not grounds to refuse a plan; it only says which
    action has to go first.

    Attaching labels or channels to a check that does not exist genuinely cannot
    work, and that is the family of bugs that shipped as "apply it twice".
    """
    if (
        isinstance(action, (LabelAction, NotificationChannelAction))
        and action.check_ref
    ):
        return (
            check_key(
                action.table_ref,
                action.check_ref,
                is_system_check=action.is_system_check,
            ),
        )
    return ()


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

    def __init__(
        self,
        nodes: List[PlanNode],
        unsatisfiable: List[Tuple[PlanNode, ResourceKey]] | None = None,
    ) -> None:
        self.nodes = nodes
        # Actions that need state which neither the plan creates nor the server
        # already has. Applying one can only fail, so `apply` reports these before
        # writing anything.
        self.unsatisfiable = unsatisfiable or []

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


def build_plan(
    actions: List[Action],
    is_satisfied: Callable[[ResourceKey], bool] | None = None,
) -> Plan:
    """Order actions by their declared dependencies.

    Ties are broken by the order the planner emitted them, so a plan whose actions
    already satisfy their dependencies comes back unchanged.

    A required resource the plan does not create is assumed to exist on the server.
    Pass `is_satisfied` to check that assumption instead of taking it: it is called
    only for those keys, so it costs a lookup per genuinely-missing dependency
    rather than one per action. Anything it rejects lands on `Plan.unsatisfiable`.
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

    unsatisfiable: List[Tuple[PlanNode, ResourceKey]] = []
    for node in nodes.values():
        node.depends_on = {
            required
            for required in required_resources(node.action)
            if required in nodes and required != node.key
        }
        if is_satisfied is None:
            continue
        for prerequisite in prerequisite_resources(node.action):
            if prerequisite not in nodes and not is_satisfied(prerequisite):
                unsatisfiable.append((node, prerequisite))

    graph = {key: node.depends_on for key, node in nodes.items()}
    try:
        ordered = [nodes[key] for key in _stable_topological_order(graph, nodes)]
    except CycleError as e:
        # Unreachable with the current edges, which are acyclic by construction.
        # Falling back beats aborting a customer's apply over a planner bug.
        print(
            f"Warning: Could not order changes by dependency ({e}); "
            "applying them in the order they were computed",
            file=sys.stderr,
        )
        ordered = list(nodes.values())

    _reject_clobbering_writes(ordered)
    return Plan(ordered, unsatisfiable)


def _reject_clobbering_writes(ordered: List[PlanNode]) -> None:
    """Refuse an order that puts a full-replace write after a partial one.

    Both calls would report success and the earlier change would be gone, with
    nothing printed — that is the #36463 failure, where sending only notification
    channels through `POST configure_table` blanked `check_cadence_type` and marked
    the table deconfigured. Unlike the cycle fallback above this raises rather than
    warning: continuing would corrupt configuration the customer asked us to write.

    Only *aliasing* resources are checked. Two actions writing the same resource are
    a planner bug that `build_plan` deliberately tolerates rather than dropping a
    change, and the later one is meant to win.

    Unreachable today, because a table's channels declare a dependency on its
    configuration and so are ordered after it. That is the point — the next pair of
    resources to alias one object fails loudly instead of silently.
    """
    first_writer: Dict[ResourceKey, PlanNode] = {}
    for node in ordered:
        target = write_target(node.action)
        earlier = first_writer.get(target)
        aliases_earlier = earlier is not None and resource_key(
            earlier.action
        ) != resource_key(node.action)
        if aliases_earlier and is_full_replace(node.action):
            raise ClobberingWrite(str(node.action), str(earlier.action))
        first_writer.setdefault(target, node)


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
