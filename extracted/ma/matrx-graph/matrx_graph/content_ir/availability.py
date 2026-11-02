"""The Kind Availability Index — what is reachable, from where, in one workflow.

Three of Arman's requirements (plan of record
``common-docs/systems/architecture/content-ir/FEATURE.md`` §7.7) turned
out to be ONE primitive, so it is built once and all three consume it:

* **The pull picker** — standing inside the node he is building, Arman browses
  everything available anywhere in the workflow: *"I get to kinda go
  shopping… you get to see all the kinds, including all the internal ones."*
* **Path exposure** — publishing a key DEEPER than a kind as a named accessor,
  which is the whole of "push" (being seen is automatic and needs no publish).
* **Kind-triggered nodes** — a node connected to nothing that fires when a kind
  appears *"wherever they're generated from… and doesn't matter how deeply
  nested they are."*

THE IDEA
--------
A node declares ONE output kind. The registry knows what that kind CONTAINS —
nested kinds, however deep — even though the workflow definition never mentions
them. So the set of values a workflow can actually offer is far larger than the
set of values it names, and it is computable without running anything.

That computation is what retires a whole category of nodes: pointing at a
nested kind brings its access path with it, so *"a lot of these extractions
don't even need a node anymore, because it's just automatic."*

AVAILABILITY IS WORKFLOW-WIDE, NEVER ADJACENCY-BOUND
----------------------------------------------------
*"Just because something goes from step two to three doesn't mean that step
nine can't also consume it."* This module deliberately does NOT filter by graph
reachability. What it does compute is ORDER (a node cannot consume a value
produced after it runs, when step order is known) and USE (who already consumes
each entry), because "show me what nobody is using yet" is the picker's default
and most valuable view.

PURE BY DESIGN
--------------
No DB, no engine, no I/O: callers pass the node declarations and a schema
resolver. That keeps it testable in isolation and usable from three very
different callers — the compiler, the API that feeds the designer's picker, and
the runtime subscription matcher.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.envelope import KIND_KEY

__all__ = [
    "NodeKindDeclaration",
    "AvailableKind",
    "KindAvailabilityIndex",
    "build_availability_index",
    "SchemaResolver",
    "EdgeResolver",
    "MAX_NESTING_DEPTH",
]

#: Resolve a kind slug to its registered JSON Schema (``None`` when unknown).
#: In production this is backed by ``matrx_graph.kinds``; tests pass a dict's
#: ``get``. Keeping it a callable is what keeps this module pure.
SchemaResolver = Callable[[str], dict[str, Any] | None]

#: Resolve a kind slug to its DECLARED composition edges — ``(field_name,
#: child_slug)`` pairs from ``content_ir.kind_edge``. This is the index's
#: FIRST nesting source and it is not redundant with the schema walk:
#: measured on the live registry (2026-08-20), 51 parent kinds declare
#: composition here while their ``emitted_json_schema`` pins ``__kind`` on
#: NOTHING — every kind registered before ``KindModel`` existed
#: (``flashcard_set -> cards -> flashcard``, ``quiz_set -> questions ->
#: quiz_question``, ``study_notes -> sections -> study_notes_section``). With
#: only the schema walk their interiors are invisible to the picker, which is
#: the precise capability §7.7a promises. Optional: passing ``None`` keeps the
#: schema-only behavior for a caller with no registry.
EdgeResolver = Callable[[str], "Sequence[tuple[str, str]]"]

#: Nested-kind walking stops here. Kind graphs are small and mostly shallow;
#: this is a cycle/pathology guard, not a modeling limit. Cycles are also
#: tracked explicitly (a kind may legitimately contain itself — a comment with
#: replies — and the picker must not hang or explode on it).
MAX_NESTING_DEPTH = 6


class NodeKindDeclaration(BaseModel):
    """One node's declared I/O, as the index needs it.

    Deliberately not ``CompiledNode``: the index is computed for the DESIGNER
    (on an unsaved, possibly invalid definition) as often as for a compiled
    graph, so it takes the minimum and stays usable in both worlds.
    """

    model_config = ConfigDict(frozen=True)

    node_id: str
    label: str = ""
    output_kind: str | None = None
    #: Kinds this node consumes. Drives the used/unused split — the picker's
    #: default view is "outputs nobody has picked up yet".
    consumes: tuple[str, ...] = ()
    #: Execution order when known (compile assigns it). ``None`` = unknown,
    #: which the index treats as "no ordering claim", never as "first".
    step: int | None = None


class AvailableKind(BaseModel):
    """One value a node could consume, and how to reach it."""

    model_config = ConfigDict(frozen=True)

    kind: str
    #: The node that produces the root value this entry lives inside.
    source_node_id: str
    source_node_label: str = ""
    #: Access path from the producing node's output to this value. Empty for
    #: the node's own output kind; otherwise the dotted route through the
    #: registered schemas (``results[].author``). This is what makes selection
    #: carry its own path and retire extraction nodes.
    path: str = ""
    #: Nesting depth: 0 = the node's own output, 1+ = inside it.
    depth: int = 0
    #: True when the value is a LIST of this kind — the picker shows it as a
    #: collection, and the `each` vs `all` edge mode becomes meaningful.
    is_collection: bool = False
    #: Whether any node in the workflow already consumes this kind.
    used: bool = False
    #: Set when the walk stopped early here (cycle or depth cap) — surfaced so
    #: the UI can say "more inside" instead of pretending this is a leaf.
    truncated: bool = False

    @property
    def is_nested(self) -> bool:
        """A nested internal part rather than a whole node result.

        The picker filters on this — Arman: *"filter only for full results or
        known internal parts."*
        """
        return self.depth > 0

    def reference(self) -> str:
        """The stable accessor for this value: ``<node_id>`` or ``<node_id>.<path>``.

        This is exactly what "push" publishes when a node exposes a key deeper
        than a kind — the exposure is a saved accessor, never copied data.
        """
        return self.node_reference(self.source_node_id, self.path)

    @staticmethod
    def node_reference(node_id: str, path: str) -> str:
        return f"{node_id}.{path}" if path else node_id


class KindAvailabilityIndex(BaseModel):
    """Everything reachable in one workflow, with the picker's views on it."""

    model_config = ConfigDict(frozen=True)

    entries: tuple[AvailableKind, ...] = ()
    #: Slugs that could not be resolved (declared but unregistered). A LOUD
    #: fact, never a silent omission: an unresolvable kind means the picker is
    #: showing an incomplete world, and the caller must be able to say so.
    unresolved_kinds: tuple[str, ...] = ()

    def for_node(self, node_id: str, *, respect_order: bool = True) -> tuple[AvailableKind, ...]:
        """What ``node_id`` could consume.

        Excludes the node's own output (a node does not consume itself) and,
        when step order is known and ``respect_order`` is set, anything
        produced after it runs. Nothing else is filtered: availability is
        workflow-wide by ruling, not adjacency-bound.
        """
        target_step = next((e.step for e in self._declarations if e.node_id == node_id), None)
        out = []
        for entry in self.entries:
            if entry.source_node_id == node_id:
                continue
            if respect_order and target_step is not None:
                source_step = next(
                    (d.step for d in self._declarations if d.node_id == entry.source_node_id),
                    None,
                )
                if source_step is not None and source_step >= target_step:
                    continue
            out.append(entry)
        return tuple(out)

    def unused(self) -> tuple[AvailableKind, ...]:
        """Values nobody consumes yet — the picker's DEFAULT view.

        Arman: *"show me all the values that are being outputted, but no one's
        using them. Because most likely, that's something I'm gonna wanna
        use."*
        """
        return tuple(e for e in self.entries if not e.used)

    def used_entries(self) -> tuple[AvailableKind, ...]:
        return tuple(e for e in self.entries if e.used)

    def of_kind(self, slug: str) -> tuple[AvailableKind, ...]:
        """Every place ``slug`` appears, at any depth, from any node.

        This is what a kind-triggered node subscribes against and what a
        kind-filtered edge resolves — routing by what the payload IS.
        """
        return tuple(e for e in self.entries if e.kind == slug)

    def from_node(self, node_id: str) -> tuple[AvailableKind, ...]:
        """Everything one node offers — its output and every part inside it."""
        return tuple(e for e in self.entries if e.source_node_id == node_id)

    # Declarations are carried privately so ``for_node`` can reason about order
    # without callers threading them back in.
    _declarations: tuple[NodeKindDeclaration, ...] = ()

    def with_declarations(
        self, declarations: Sequence[NodeKindDeclaration]
    ) -> KindAvailabilityIndex:
        object.__setattr__(self, "_declarations", tuple(declarations))
        return self


def build_availability_index(
    declarations: Iterable[NodeKindDeclaration],
    resolve_schema: SchemaResolver,
    *,
    resolve_edges: EdgeResolver | None = None,
    max_depth: int = MAX_NESTING_DEPTH,
) -> KindAvailabilityIndex:
    """Compute every kind reachable in a workflow, nested kinds included.

    ``resolve_schema`` maps a kind slug to its registered JSON Schema. Nested
    kinds are discovered by walking that schema: any position whose schema
    pins ``__kind`` to a constant IS a kind instance, which is exactly what
    ``KindModel`` emits (``{"const": "website"}``) — so the index reads the
    same declaration the data itself carries. No separate nesting registry is
    consulted and none can drift from the schemas.
    """
    declarations = tuple(declarations)
    consumed: set[str] = {slug for d in declarations for slug in d.consumes}
    entries: list[AvailableKind] = []
    unresolved: list[str] = []

    for declaration in declarations:
        root = declaration.output_kind
        if not root:
            continue
        schema = resolve_schema(root)
        if schema is None:
            if root not in unresolved:
                unresolved.append(root)
            # Still offer the node's own output: the workflow DECLARES it, and
            # hiding it would make the picker lie about what exists. Only its
            # interior is unknown.
            entries.append(
                AvailableKind(
                    kind=root,
                    source_node_id=declaration.node_id,
                    source_node_label=declaration.label,
                    used=root in consumed,
                    truncated=True,
                )
            )
            continue

        entries.append(
            AvailableKind(
                kind=root,
                source_node_id=declaration.node_id,
                source_node_label=declaration.label,
                used=root in consumed,
            )
        )
        entries.extend(
            _walk(
                # A self-referencing model's schema is a bare ``$ref`` into
                # ``$defs`` at the ROOT, so the entry point must be
                # dereferenced while the DOCUMENT stays the ref-resolution
                # root. Walking the undereferenced document finds no
                # properties and silently returns nothing.
                schema=_deref(schema, schema) or schema,
                root_schema=schema,
                resolve_schema=resolve_schema,
                declaration=declaration,
                consumed=consumed,
                path="",
                depth=1,
                max_depth=max_depth,
                seen=(root,),
                unresolved=unresolved,
                resolve_edges=resolve_edges,
                current_slug=root,
            )
        )

    return KindAvailabilityIndex(
        entries=tuple(entries), unresolved_kinds=tuple(unresolved)
    ).with_declarations(declarations)


def _kind_const(schema: dict[str, Any]) -> str | None:
    """The kind slug a schema position pins, if it is a kind instance.

    ``KindModel`` emits the discriminator as ``{"const": "<slug>"}`` (with a
    matching default), so a position that declares ``__kind`` with a constant
    IS an instance of that kind. ``enum``-of-one is accepted too — some
    hand-written registry schemas spell it that way.
    """
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return None
    marker = properties.get(KIND_KEY)
    if not isinstance(marker, dict):
        return None
    const = marker.get("const")
    if isinstance(const, str) and const:
        return const
    values = marker.get("enum")
    if isinstance(values, list) and len(values) == 1 and isinstance(values[0], str):
        return values[0]
    return None


def _deref(schema: Any, root: dict[str, Any], hops: int = 0) -> dict[str, Any] | None:
    """Follow ``$ref`` within one document (pydantic's ``$defs`` style)."""
    while isinstance(schema, dict) and "$ref" in schema:
        if hops > 16:
            return None
        hops += 1
        ref = str(schema["$ref"])
        if ref in ("#", "#/"):
            return root
        target = (root.get("$defs") or {}).get(ref.rsplit("/", 1)[-1])
        if not isinstance(target, dict):
            return None
        schema = target
    return schema if isinstance(schema, dict) else None


def _branches(schema: dict[str, Any], root: dict[str, Any]) -> list[dict[str, Any]]:
    """The position itself plus every union member, each dereferenced.

    A field typed ``Website | None`` (very common — every optional nested kind)
    is an ``anyOf``, so without this the picker would miss exactly the values
    an author most often wants.
    """
    out = [schema]
    for keyword in ("anyOf", "oneOf", "allOf"):
        members = schema.get(keyword)
        if isinstance(members, list):
            for member in members:
                resolved = _deref(member, root)
                if resolved is not None:
                    out.append(resolved)
    return out


def _walk(
    *,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    resolve_schema: SchemaResolver,
    declaration: NodeKindDeclaration,
    consumed: set[str],
    path: str,
    depth: int,
    max_depth: int,
    seen: tuple[str, ...],
    unresolved: list[str],
    resolve_edges: EdgeResolver | None = None,
    current_slug: str = "",
) -> list[AvailableKind]:
    """Find every nested kind inside ``schema``, depth-first.

    TWO independent sources, deliberately, because neither is complete alone:
    the schema's own ``__kind`` constants (what ``KindModel`` emits) and the
    registry's DECLARED ``kind_edge`` rows (the only interior most older kinds
    have). Entries are deduped by ``(path, kind)``, so a kind declared in both
    — the correct, converged state — appears once.
    """
    if depth > max_depth:
        return []
    found: list[AvailableKind] = []
    claimed: set[tuple[str, str]] = set()

    properties: dict[str, Any] = {}
    for branch in _branches(schema, root_schema):
        branch_properties = branch.get("properties")
        if isinstance(branch_properties, dict):
            for key, value in branch_properties.items():
                properties.setdefault(key, value)

    for key, raw in properties.items():
        if key == KIND_KEY:
            continue
        for candidate in _branches(_deref(raw, root_schema) or {}, root_schema):
            if not candidate:
                continue
            is_collection = False
            target = candidate
            if candidate.get("type") == "array" or "items" in candidate:
                items = _deref(candidate.get("items"), root_schema)
                if items is None:
                    continue
                target, is_collection = items, True
                # A union INSIDE the array (list[Website | Video]) still has to
                # be opened, or heterogeneous collections vanish from the index.
                for member in _branches(items, root_schema):
                    slug = _kind_const(member)
                    if slug:
                        target = member
                        break

            slug = _kind_const(target)
            if not slug:
                continue

            entry_path = f"{path}.{key}" if path else key
            if is_collection:
                entry_path = f"{entry_path}[]"
            claimed.add((entry_path, slug))
            cyclic = slug in seen
            found.append(
                AvailableKind(
                    kind=slug,
                    source_node_id=declaration.node_id,
                    source_node_label=declaration.label,
                    path=entry_path,
                    depth=depth,
                    is_collection=is_collection,
                    used=slug in consumed,
                    truncated=cyclic or depth >= max_depth,
                )
            )
            if cyclic:
                # A kind may legitimately contain itself (a comment with
                # replies). Record the entry, mark it, and stop — the picker
                # says "more inside" rather than hanging.
                break

            # Prefer the REGISTERED schema for the nested kind (it is the
            # canonical definition and may carry more than the inlined copy);
            # fall back to the inlined subschema when it is unregistered, so a
            # not-yet-published nested kind still appears.
            registered = resolve_schema(slug)
            if registered is None:
                nested_document, nested_entry = root_schema, target
                if slug not in unresolved:
                    unresolved.append(slug)
            else:
                # Same root-``$ref`` dereference as the entry point above: the
                # document carries ``$defs``, the entry is what we walk.
                nested_document = registered
                nested_entry = _deref(registered, registered) or registered
            found.extend(
                _walk(
                    schema=nested_entry,
                    root_schema=nested_document,
                    resolve_schema=resolve_schema,
                    declaration=declaration,
                    consumed=consumed,
                    path=entry_path,
                    depth=depth + 1,
                    max_depth=max_depth,
                    seen=seen + (slug,),
                    unresolved=unresolved,
                    resolve_edges=resolve_edges,
                    current_slug=slug,
                )
            )
            break

    found.extend(
        _walk_declared_edges(
            schema=schema,
            root_schema=root_schema,
            resolve_schema=resolve_schema,
            resolve_edges=resolve_edges,
            current_slug=current_slug,
            declaration=declaration,
            consumed=consumed,
            path=path,
            depth=depth,
            max_depth=max_depth,
            seen=seen,
            unresolved=unresolved,
            claimed=claimed,
        )
    )
    return found


def _walk_declared_edges(
    *,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    resolve_schema: SchemaResolver,
    resolve_edges: EdgeResolver | None,
    current_slug: str,
    declaration: NodeKindDeclaration,
    consumed: set[str],
    path: str,
    depth: int,
    max_depth: int,
    seen: tuple[str, ...],
    unresolved: list[str],
    claimed: set[tuple[str, str]],
) -> list[AvailableKind]:
    """Nested kinds the REGISTRY declares that the schema does not carry.

    ``content_ir.kind_edge`` is an explicit statement — *this kind's ``cards``
    field holds ``flashcard`` instances* — made when the kind was registered.
    Reading it is not inference: the alternative (matching a ``$defs`` name
    against the slug table) WOULD be a guess, and this module never guesses
    what a path points at.

    One field may declare several children (``flashcard_set.cards`` declares
    ``flashcard``, ``enhanced_flashcard`` AND ``tiered_flashcard``). All three
    are emitted at the same path, because the list genuinely may hold any of
    them and hiding two would make the picker lie about what can arrive.
    """
    if resolve_edges is None or not current_slug or depth > max_depth:
        return []
    try:
        edges = list(resolve_edges(current_slug))
    except Exception:  # noqa: BLE001 — a registry miss must never break the picker
        return []
    if not edges:
        return []

    properties: dict[str, Any] = {}
    for branch in _branches(schema, root_schema):
        branch_properties = branch.get("properties")
        if isinstance(branch_properties, dict):
            for key, value in branch_properties.items():
                properties.setdefault(key, value)

    found: list[AvailableKind] = []
    for field_name, child_slug in edges:
        if not field_name or not child_slug:
            continue
        # Collection-ness comes from the SCHEMA (the shape is the schema's
        # job); the edge only says which kind lives there. A field the schema
        # does not declare is still offered — the edge is a declaration in its
        # own right — as a scalar, which is the conservative reading.
        field_schema = _deref(properties.get(field_name), root_schema) or {}
        is_collection = field_schema.get("type") == "array" or "items" in field_schema
        entry_path = f"{path}.{field_name}" if path else field_name
        if is_collection:
            entry_path = f"{entry_path}[]"
        if (entry_path, child_slug) in claimed:
            continue  # the schema walk already found it — converged, not double
        claimed.add((entry_path, child_slug))
        cyclic = child_slug in seen
        found.append(
            AvailableKind(
                kind=child_slug,
                source_node_id=declaration.node_id,
                source_node_label=declaration.label,
                path=entry_path,
                depth=depth,
                is_collection=is_collection,
                used=child_slug in consumed,
                truncated=cyclic or depth >= max_depth,
            )
        )
        if cyclic:
            continue
        child_schema = resolve_schema(child_slug)
        if child_schema is None:
            if child_slug not in unresolved:
                unresolved.append(child_slug)
            continue
        found.extend(
            _walk(
                schema=_deref(child_schema, child_schema) or child_schema,
                root_schema=child_schema,
                resolve_schema=resolve_schema,
                declaration=declaration,
                consumed=consumed,
                path=entry_path,
                depth=depth + 1,
                max_depth=max_depth,
                seen=seen + (child_slug,),
                unresolved=unresolved,
                resolve_edges=resolve_edges,
                current_slug=child_slug,
            )
        )
    return found
