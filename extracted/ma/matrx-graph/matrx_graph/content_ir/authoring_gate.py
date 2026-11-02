"""COMPILE-TIME KIND RESOLUTION — a bad binding fails at SAVE, not in production.

The problem (KINDS_EVERYWHERE_PLAN §10d-B4): ``compile_graph`` is SYNC and the
kind catalog is ASYNC, so nothing checks that a declared ``input_kind`` /
``output_kind`` / ``kind_filter`` / trigger kind actually EXISTS until the run
executes — where, under the live ``workflow_io`` enforcement (ON since
2026-08-26), admission refuses the run (``KindDegradedReason``; only
``catalog_unreachable`` stays a loud skip). A typo in the Studio would
therefore ship: the workflow saves clean, publishes clean, and only fails once
someone runs it.

The fix is NOT to make compile async or to put a DB hop in the hot path. It is
to resolve at the AUTHORING boundary — save and publish — where one catalog
round-trip is free and the author is still looking at the canvas. The runtime
posture is untouched by this gate: at run time an unregistered or schema-less
kind is fatal at admission under ``workflow_io`` enforcement (the matrix is
``matrx_graph.kinds.degraded_escalation``).

WHAT IS CHECKED, AND WHAT IS NOT

Only bindings a HUMAN authored are checked: ``node.data.input_kind`` /
``output_kind``, an edge's ``kind_filter``, and a kind-triggered node's kind.
A NodeSpec's own declared kinds are CODE — an unregistered one is a platform
defect that must not block a user's publish (it screams from the registry-drift
gate instead, ``scripts/publish_kind_catalog.py``).

SEVERITY — the author's typo blocks; the platform's problem does not:

    kind_not_registered   BLOCKING   the slug names nothing; a typo or a kind
                                     that was never published
    kind_inactive         BLOCKING   the row exists but is deactivated, so
                                     nothing downstream will offer or render it
    schema_unavailable    advisory   the registration is broken — the AUTHOR
    schema_invalid        advisory   cannot fix it, so it must not block them
    catalog_unreachable   advisory   infra outage; an outage must never look
                                     like a bad workflow (same rule the engine
                                     applies under enforcement)

``kind_inactive`` blocks here even though the ENGINE deliberately ignores
``is_active`` at run time. The two are not in conflict: the engine's rule is
about validating a payload that already exists, while this gate is about
letting an author BIND to something the platform will not surface. Measured on
the live registry (2026-08-23) every slug bound by every live definition is
registered and active, so this blocks nothing that exists today.
"""

from __future__ import annotations

from enum import StrEnum

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from matrx_graph.content_ir.edge_routing import parse_edge_routing
from matrx_graph.content_ir.triggers import parse_node_trigger
from matrx_graph.kinds import KindDegradedReason, declared_output_kind
from matrx_graph.shape_probe import kind_path_problem
from matrx_graph.types.definition import Definition

if TYPE_CHECKING:
    from matrx_graph.executor.registry import NodeRegistry

__all__ = [
    "KindBinding",
    "KindBindingProblem",
    "authored_kind_bindings",
    "MappingReason",
    "kind_mapping_problems",
    "mapping_source_kinds",
    "resolve_authored_kinds",
]

#: Reasons the AUTHOR is responsible for and can fix by editing the binding.
BLOCKING_REASONS = frozenset(
    {KindDegradedReason.KIND_NOT_REGISTERED, KindDegradedReason.KIND_INACTIVE}
)


class MappingReason(StrEnum):
    """Why a connection's mapping is refused against the kind its source step declares."""

    #: The mapping reads a path the source step's declared ``output_kind`` provably does not
    #: carry (a closed level of the kind's schema lacks the segment). At run time it would
    #: arrive ABSENT — before 2026-10-28 the next step silently got ``{}``.
    PATH_NOT_ON_KIND = "path_not_on_kind"


class KindBinding(BaseModel):
    """One authored kind reference, with enough address to badge it in the UI."""

    model_config = ConfigDict(frozen=True)

    kind: str
    field: str
    """``input_kind`` | ``output_kind`` | ``kind_filter`` | ``trigger_kind`` | ``mapping``."""
    node_id: str | None = None
    edge_id: str | None = None
    label: str = ""


class KindBindingProblem(BaseModel):
    """A binding that will not resolve, and why — one per node, in words."""

    model_config = ConfigDict(frozen=True)

    binding: KindBinding
    reason: KindDegradedReason | MappingReason
    blocking: bool
    message: str


def _clean(value: object) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def authored_kind_bindings(definition: Definition) -> list[KindBinding]:
    """Every kind slug a HUMAN wrote into this definition.

    Deliberately excludes NodeSpec-declared kinds (see the module docstring):
    those are code, and a user's publish must never be blocked by them.
    """
    bindings: list[KindBinding] = []
    for node in definition.nodes:
        label = node.label or node.id
        for field in ("input_kind", "output_kind"):
            slug = _clean(node.data.get(field))
            if slug:
                bindings.append(KindBinding(kind=slug, field=field, node_id=node.id, label=label))
        trigger = parse_node_trigger(node.data)
        if trigger is not None:
            bindings.append(
                KindBinding(kind=trigger.kind, field="trigger_kind", node_id=node.id, label=label)
            )
    for edge in definition.edges:
        try:
            routing = parse_edge_routing(edge.data)
        except ValueError:
            # A malformed routing declaration is already its own validation
            # error; the kind gate must not double-report or crash on it.
            continue
        if routing.kind_filter:
            bindings.append(
                KindBinding(
                    kind=routing.kind_filter,
                    field="kind_filter",
                    edge_id=edge.id,
                    node_id=edge.target,
                    label=edge.id,
                )
            )
    return bindings


def _message(binding: KindBinding, reason: KindDegradedReason) -> str:
    where = f"'{binding.label}'" if binding.label else f"node {binding.node_id}"
    if reason is KindDegradedReason.KIND_NOT_REGISTERED:
        return (
            f"{where}: {binding.field} '{binding.kind}' is not a registered kind. "
            "Check the spelling, or register the shape before binding to it."
        )
    if reason is KindDegradedReason.KIND_INACTIVE:
        return (
            f"{where}: kind '{binding.kind}' is registered but INACTIVE, so nothing "
            "downstream will offer or render it. Activate the kind, or bind to an "
            "active one."
        )
    if reason is KindDegradedReason.SCHEMA_UNAVAILABLE:
        return (
            f"{where}: kind '{binding.kind}' has no schema in the registry — values "
            "will pass through unchecked at run time. This is a platform defect, "
            "not a problem with this workflow."
        )
    if reason is KindDegradedReason.SCHEMA_INVALID:
        return (
            f"{where}: kind '{binding.kind}' has a malformed schema, so validation "
            "will be skipped at run time. This is a platform defect, not a problem "
            "with this workflow."
        )
    return (
        f"{where}: the kind catalog could not be reached, so '{binding.kind}' was "
        "not verified. Nothing is wrong with the workflow."
    )


async def resolve_authored_kinds(
    definition: Definition, *, registry: NodeRegistry | None = None
) -> list[KindBindingProblem]:
    """Pre-resolve every authored kind binding against the LIVE catalog.

    One resolution per DISTINCT slug (``resolve_kind`` caches, and the
    availability adapter has usually warmed the same rows already), so a large
    canvas costs a handful of round-trips at save — never one per node.
    """
    from matrx_graph.kinds import resolve_kind

    bindings = authored_kind_bindings(definition)
    verdicts: dict[str, KindDegradedReason | None] = {}
    for slug in sorted({b.kind for b in bindings}):
        entry, reason = await resolve_kind(slug)
        if reason is None and entry is not None and not entry.is_active:
            reason = KindDegradedReason.KIND_INACTIVE
        verdicts[slug] = reason

    problems: list[KindBindingProblem] = []
    # Mappings are judged against each source step's DECLARED kind — the authored one, else
    # the step type's own (the same resolver compile hands the run), so save and run agree.
    source_kinds = mapping_source_kinds(definition, registry=registry)
    schemas: dict[str, dict] = {}
    for slug in sorted(set(source_kinds.values()) - {s for s, r in verdicts.items() if r is not None}):
        entry, _ = await resolve_kind(slug)
        if entry is not None and isinstance(entry.json_schema, dict) and not entry.schema_errors:
            schemas[slug] = entry.json_schema
    problems.extend(kind_mapping_problems(definition, schemas, source_kinds=source_kinds))
    for binding in bindings:
        reason = verdicts.get(binding.kind)
        if reason is None:
            continue
        problems.append(
            KindBindingProblem(
                binding=binding,
                reason=reason,
                blocking=reason in BLOCKING_REASONS,
                message=_message(binding, reason),
            )
        )
    return problems


#: Mapping sources that are engine tokens (``$FULL_PAYLOAD`` …), never paths into the output.
_TOKEN_PREFIX = "$"
#: Edge kinds that do not carry the step's output.
_NOT_OUTPUT_EDGES = frozenset({"error", "stream"})


def mapping_source_kinds(
    definition: Definition, *, registry: NodeRegistry | None = None
) -> dict[str, str]:
    """Each node's declared output kind (authored ``data.output_kind``, else its step type's
    own kind), via :func:`matrx_graph.kinds.declared_output_kind` — the resolver compile uses.
    A node whose type is not registered contributes only its authored kind."""
    if registry is None:
        from matrx_graph.executor.registry import default_registry

        registry = default_registry()
    kinds: dict[str, str] = {}
    for node in definition.nodes:
        try:
            spec_kind = registry.get(node.spec_type).spec.output_kind
        except Exception:  # noqa: BLE001 — an unknown type is its own validation error
            spec_kind = None
        slug = declared_output_kind(node.data, spec_kind)
        if slug:
            kinds[node.id] = slug
    return kinds


def kind_mapping_problems(
    definition: Definition,
    schemas: dict[str, dict],
    *,
    source_kinds: dict[str, str] | None = None,
) -> list[KindBindingProblem]:
    """Every connection mapping that reads a path its source step's DECLARED KIND rules out.

    ``schemas`` maps an output-kind slug to its resolved schema (unresolvable kinds are
    absent: unprovable, said nothing). A step whose result is reshaped (``data.shape``) or
    gathered (``data.for_each``) hands on something else, so its connections are not judged
    against its kind; keys the step adds beside its kind (``run_envelope``) are not the
    kind's. Live 2026-10-28: a Gather fed ``structured_output`` off a Run Typed Agent (whose
    output IS the kind) saved clean and received ``{}`` every run."""
    by_id = {node.id: node for node in definition.nodes}
    problems: list[KindBindingProblem] = []
    for edge in definition.edges:
        source = by_id.get(edge.source)
        if source is None or not edge.mappings or edge.kind.value in _NOT_OUTPUT_EDGES:
            continue
        slug = (
            source_kinds.get(source.id)
            if source_kinds is not None
            else declared_output_kind(source.data, None)
        )
        schema = schemas.get(slug or "")
        if not schema or source.data.get("shape") or isinstance(source.data.get("for_each"), dict):
            continue
        config = source.data.get("config") if isinstance(source.data.get("config"), dict) else {}
        beside = {str(f) for f in (config.get("run_envelope") or [])}
        label = source.label or source.id
        for target_key, source_key in edge.mappings.items():
            if not isinstance(source_key, str) or not source_key or source_key.startswith(_TOKEN_PREFIX):
                continue
            problem = kind_path_problem(schema, source_key, beside=beside, origin=f"kind '{slug}'")
            if problem is None:
                continue
            binding = KindBinding(
                kind=slug or "", field="mapping", node_id=source.id, edge_id=edge.id, label=label
            )
            problems.append(
                KindBindingProblem(
                    binding=binding,
                    reason=MappingReason.PATH_NOT_ON_KIND,
                    blocking=True,
                    message=(
                        f"Connection '{edge.id}' ({edge.source} -> {edge.target}) maps "
                        f"'{target_key}' <- '{source_key}', but '{label}' answers in kind "
                        f"'{slug}': {problem}. The step would receive nothing; map a field the "
                        "kind carries."
                    ),
                )
            )
    return problems
