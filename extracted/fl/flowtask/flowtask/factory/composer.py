"""Two-phase YAML composer for the Flowtask factory agent.

Phase A — ``sketch_dag``
    The agent describes the *shape* of the workflow with abstract nodes
    (``id``, ``kind``, ``hints``, ``depends_on``). The composer ranks
    component candidates per node by delegating to the documentation toolkit,
    validates the topology (no cycles, no dangling deps), and returns a
    :class:`DagSketch`. **No YAML is rendered yet** — this is the phase where
    the agent (or the human) confirms the workflow shape before locking in
    specific components.

Phase B — ``compose_flowtask_yaml``
    The agent supplies a bound DAG (one concrete component per node, with
    its attrs). The composer topologically sorts the nodes, renders the
    Flowtask YAML, and surfaces required attributes still missing as
    :attr:`ComposedTask.open_questions` — those are what the orchestrator
    asks the human about.

The composer never executes anything. It is pure I/O over the toolkit's
read-only surface plus a topological sort and a YAML dump.
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, Awaitable, Callable, Optional, Protocol

import yaml
from pydantic import BaseModel, Field

from .validator import ValidationReport


# ---------------------------------------------------------------------------
# Public models
# ---------------------------------------------------------------------------


class DagNode(BaseModel):
    """A single abstract node in a sketched DAG.

    The agent fills these in *before* knowing which Flowtask components map
    to each step. ``kind`` and ``hints`` are what the composer feeds into
    component search.
    """

    id: str = Field(..., description="Unique identifier within the sketch (free-form).")
    kind: str = Field(..., description="Abstract role, e.g. 'download', 'transform', 'load'.")
    hints: Optional[str] = Field(
        None,
        description="Free-form natural-language detail used to refine the candidate search.",
    )
    depends_on: list[str] = Field(
        default_factory=list,
        description="IDs of nodes that must finish before this one.",
    )


class CandidateComponent(BaseModel):
    """One ranked component proposal for a sketched node."""

    name: str
    category: str
    description: str
    score: float


class SketchedNode(BaseModel):
    """A sketched DAG node enriched with ranked candidate components."""

    id: str
    kind: str
    hints: Optional[str] = None
    depends_on: list[str] = Field(default_factory=list)
    candidates: list[CandidateComponent] = Field(default_factory=list)


class DagSketch(BaseModel):
    """Result of :meth:`DagComposer.sketch_dag`."""

    nodes: list[SketchedNode]
    order: list[str] = Field(
        ..., description="Topologically sorted node IDs."
    )


class BoundNode(BaseModel):
    """A DAG node with a concrete component pick and attrs filled in."""

    id: str = Field(..., description="Matches the original :class:`DagNode.id`.")
    component: str = Field(..., description="Exact component class name.")
    attrs: dict[str, Any] = Field(default_factory=dict)
    depends_on: list[str] = Field(default_factory=list)


class ComposedTask(BaseModel):
    """Output of :meth:`DagComposer.compose_flowtask_yaml`."""

    yaml: str = Field(..., description="Rendered Flowtask YAML, ready to commit.")
    used_components: list[str]
    open_questions: list[str] = Field(
        default_factory=list,
        description="Concrete items the agent should surface to the human before shipping.",
    )
    validation: ValidationReport


class ComposerError(ValueError):
    """Raised when the DAG itself is malformed (cycles, dangling deps, dup IDs)."""


# ---------------------------------------------------------------------------
# Duck-typed dependency on the documentation toolkit
# ---------------------------------------------------------------------------


class _SearchResultProto(Protocol):
    name: str
    category: str
    description: str
    score: Optional[float]


class _AttrProto(Protocol):
    name: str
    required: bool


class _ComponentDetailProto(Protocol):
    name: str
    attributes: list[_AttrProto]


SearchFn = Callable[..., Awaitable[list[_SearchResultProto]]]
GetComponentFn = Callable[[str], Awaitable[_ComponentDetailProto]]
ValidateYamlFn = Callable[[str], Awaitable[ValidationReport]]


# ---------------------------------------------------------------------------
# Composer
# ---------------------------------------------------------------------------


class DagComposer:
    """Two-phase composer.

    Accepts the three callables it needs from the documentation toolkit so it
    stays testable without a full ai-parrot stack.
    """

    def __init__(
        self,
        *,
        search_fn: SearchFn,
        get_component_fn: GetComponentFn,
        validate_yaml_fn: ValidateYamlFn,
    ) -> None:
        self._search = search_fn
        self._get_component = get_component_fn
        self._validate_yaml = validate_yaml_fn

    # ------------------------------------------------------------------
    # Phase A: sketch_dag
    # ------------------------------------------------------------------

    async def sketch_dag(
        self,
        nodes: list[DagNode | dict[str, Any]],
        *,
        per_node_top_k: int = 5,
    ) -> DagSketch:
        """Rank candidate components for each abstract node.

        Validates topology and returns ranked candidates per node. No YAML is
        rendered.

        Args:
            nodes: List of :class:`DagNode` (or dicts that coerce into one).
            per_node_top_k: How many candidate components to return per node.

        Raises:
            ComposerError: Duplicate IDs, dangling depends_on, or a cycle.
        """
        normalised = _coerce_nodes(nodes, DagNode)
        _validate_topology(normalised)
        order = _topo_sort(normalised)

        sketched: list[SketchedNode] = []
        for node in normalised:
            query = " ".join(filter(None, [node.kind, node.hints or ""])).strip()
            raw_results = await self._search(query, None, per_node_top_k) if query else []
            candidates = [
                CandidateComponent(
                    name=r.name,
                    category=r.category,
                    description=r.description,
                    score=float(r.score or 0.0),
                )
                for r in raw_results
            ]
            sketched.append(
                SketchedNode(
                    id=node.id,
                    kind=node.kind,
                    hints=node.hints,
                    depends_on=list(node.depends_on),
                    candidates=candidates,
                )
            )
        return DagSketch(nodes=sketched, order=order)

    # ------------------------------------------------------------------
    # Phase B: compose_flowtask_yaml
    # ------------------------------------------------------------------

    async def compose_flowtask_yaml(
        self,
        nodes: list[BoundNode | dict[str, Any]],
        *,
        task_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> ComposedTask:
        """Render a Flowtask YAML from a bound DAG.

        Topologically sorts the nodes (the YAML is sequential), renders the
        YAML, validates it, and surfaces required attributes that are still
        missing as :attr:`ComposedTask.open_questions`.

        Args:
            nodes: One :class:`BoundNode` per step.
            task_name: Optional value for the top-level ``name`` key.
            description: Optional value for the top-level ``description`` key.

        Raises:
            ComposerError: Duplicate IDs, dangling deps, or a cycle.
        """
        bound = _coerce_nodes(nodes, BoundNode)
        _validate_topology(bound)
        order = _topo_sort(bound)
        by_id = {n.id: n for n in bound}
        ordered = [by_id[nid] for nid in order]

        # Surface open questions per node.
        open_questions: list[str] = []
        for node in ordered:
            try:
                detail = await self._get_component(node.component)
            except KeyError as exc:
                open_questions.append(
                    f"Node '{node.id}' references unknown component '{node.component}'. "
                    f"Search candidates first. Detail: {exc}"
                )
                continue
            for attr in detail.attributes:
                if attr.required and attr.name not in node.attrs:
                    open_questions.append(
                        f"Node '{node.id}' ({node.component}): required attribute "
                        f"'{attr.name}' is unset."
                    )

        yaml_text = _render_yaml(ordered, task_name=task_name, description=description)
        validation = await self._validate_yaml(yaml_text)

        # Boundary mismatches are full validation errors but are also worth
        # promoting to ``open_questions`` so the agent surfaces them to the
        # human alongside attribute gaps — they describe the same kind of
        # "needs human input" decision.
        for issue in validation.issues:
            if "Boundary mismatch" in issue.message:
                open_questions.append(issue.message)

        return ComposedTask(
            yaml=yaml_text,
            used_components=[n.component for n in ordered],
            open_questions=open_questions,
            validation=validation,
        )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _coerce_nodes(items, model):
    coerced = []
    for item in items:
        if isinstance(item, model):
            coerced.append(item)
        elif isinstance(item, dict):
            coerced.append(model(**item))
        else:
            raise ComposerError(
                f"Expected {model.__name__} or dict, got {type(item).__name__}."
            )
    return coerced


def _validate_topology(nodes) -> None:
    seen: set[str] = set()
    for n in nodes:
        if n.id in seen:
            raise ComposerError(f"Duplicate node id '{n.id}'.")
        seen.add(n.id)
    for n in nodes:
        for dep in n.depends_on:
            if dep not in seen:
                raise ComposerError(
                    f"Node '{n.id}' depends on unknown node '{dep}'."
                )


def _topo_sort(nodes) -> list[str]:
    """Kahn's algorithm. Raises :class:`ComposerError` on cycles.

    Stable: ties are broken by the order in which nodes were declared, so
    composed YAML stays predictable across runs.
    """
    declared_order = {n.id: idx for idx, n in enumerate(nodes)}
    deps: dict[str, set[str]] = {n.id: set(n.depends_on) for n in nodes}
    dependents: dict[str, set[str]] = defaultdict(set)
    for n in nodes:
        for d in n.depends_on:
            dependents[d].add(n.id)

    ready = deque(sorted([n.id for n in nodes if not deps[n.id]], key=declared_order.get))
    order: list[str] = []

    while ready:
        current = ready.popleft()
        order.append(current)
        # Use a sorted snapshot to keep the popping stable.
        for child in sorted(dependents[current], key=declared_order.get):
            deps[child].discard(current)
            if not deps[child]:
                ready.append(child)

    if len(order) != len(nodes):
        unresolved = sorted(deps.keys() - set(order))
        raise ComposerError(
            f"Cycle detected in DAG involving nodes: {', '.join(unresolved)}"
        )
    return order


def _render_yaml(
    nodes: list[BoundNode],
    *,
    task_name: Optional[str],
    description: Optional[str],
) -> str:
    """Render the canonical Flowtask YAML shape used by the runtime."""
    data: dict[str, Any] = {}
    if task_name:
        data["name"] = task_name
    if description:
        data["description"] = description
    data["steps"] = [{n.component: dict(n.attrs)} for n in nodes]
    return yaml.safe_dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )
