"""Accessor paths — turning a picker selection into actual values at runtime.

THE POINT (plan of record
``common-docs/systems/architecture/content-ir/FEATURE.md`` §7.7a):

    "Pointing at a nested kind brings the whole path with it… a lot of these
    extractions don't even need a node anymore, because it's just automatic."

``availability.AvailableKind.reference()`` hands the designer a stable string
(``search.results[].author``). This module is the other half: given that string
and a run's data, produce the value(s). Without it the picker would be a
catalog that selects nothing, and every selection would still need an
extraction node — which is exactly what §7.7a retires.

THE GRAMMAR (one grammar, produced by ``AvailableKind`` and consumed here)
-------------------------------------------------------------------------
    reference := <node_id> [ "." <segment> ]*
    segment   := <key> | <key> "[]"

A ``[]`` segment means "step into this list". It is the ONLY multiplicity
operator, and it is why resolution ALWAYS returns a list of values:

* ``search``                      -> [ the whole output ]
* ``search.query``                -> [ "pizza" ]
* ``search.results[]``            -> [ website, website, website ]
* ``search.results[].author``     -> [ author, author ]   (websites with no
                                       author contribute NOTHING — a hole is
                                       an absence, never a ``None`` in the
                                       middle of a typed list)

Multiple ``[]`` segments compose by flattening in document order, which is what
makes ``a[].b[].c`` behave the way an author reading it expects.

WRAPPERS ARE UNWRAPPED AT THE ROOT, ONCE
----------------------------------------
Edges carry the data kind (the ratified edge contract), but PERSISTED run data
carries the runtime wrapper. So a reference resolved against a stored
``node_outcome`` must see through it — otherwise every path in the index would
have to be spelled ``output.results[].author`` against storage and
``results[].author`` against the wire, and the picker would be lying to one of
them. Unwrapping happens exactly once, at the root, and it is the wrapper
contract that decides where to look (``output`` / ``content``) — never a guess.

FAILURE POSTURE
---------------
Resolution never raises on missing data: a key that is not there yields no
value and is RECORDED in ``notes``. A caller that needs a hard failure asserts
on ``values``/``notes`` itself, with its own message. A type mismatch (``[]``
against a non-list) is a genuine authoring/contract defect, so it is recorded
LOUDLY as a note and the value is still offered — a silent empty result would
send an author hunting through the wrong node.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.envelope import KIND_KEY
from matrx_graph.content_ir.model import kind_of

__all__ = [
    "ParsedReference",
    "PathResolution",
    "parse_reference",
    "resolve_path",
    "resolve_reference",
    "unwrap_runtime_wrapper",
    "WRAPPER_PAYLOAD_FIELDS",
]

#: Where each runtime wrapper kind keeps its payload. This is the wrapper
#: contract from ``content_ir.wrappers`` expressed as data, so unwrapping is a
#: lookup rather than an isinstance ladder that would miss serialized payloads.
#: A wrapper whose payload field holds a LIST (``agent_result.content``) is
#: unwrapped to that list — the list IS the payload, in document order.
WRAPPER_PAYLOAD_FIELDS: dict[str, str] = {
    "node_outcome": "output",
    "run_result": "output",
    "tool_result": "output",
    "agent_result": "content",
}


class ParsedReference(BaseModel):
    """A reference split into the node it starts at and the path inside it."""

    model_config = ConfigDict(frozen=True)

    node_id: str
    path: str = ""
    segments: tuple[str, ...] = ()

    @property
    def is_whole_output(self) -> bool:
        return not self.segments


class PathResolution(BaseModel):
    """The values a reference resolved to, plus everything that went wrong.

    ``values`` is always a list — see the grammar above. ``notes`` is the loud
    half: missing keys and type mismatches are recorded rather than raised, so
    a caller can report "3 of 5 results had no author" instead of a bare empty
    list that looks identical to a broken reference.
    """

    model_config = ConfigDict(frozen=True)

    reference: str = ""
    values: list[Any] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    #: True when the root itself could not be found (unknown node id). Distinct
    #: from "found the node, it had no such key" — a different fix each time.
    root_missing: bool = False

    @property
    def found(self) -> bool:
        return bool(self.values)

    def single(self) -> Any | None:
        """The one value, when exactly one resolved — the 99% consumption case."""
        return self.values[0] if len(self.values) == 1 else None


def parse_reference(reference: str, known_node_ids: Sequence[str] | None = None) -> ParsedReference:
    """Split ``node.path.to[].value`` into its node id and path segments.

    Node ids are author-controlled and MAY contain dots, so when the caller can
    name the graph's nodes we match the LONGEST known id first and only then
    split the remainder. Without that hint we fall back to splitting at the
    first dot — correct for every id the studio mints, and the reason the hint
    exists at all.
    """
    reference = (reference or "").strip()
    if not reference:
        return ParsedReference(node_id="", path="")

    if known_node_ids:
        for node_id in sorted(known_node_ids, key=len, reverse=True):
            if reference == node_id:
                return ParsedReference(node_id=node_id, path="")
            if reference.startswith(f"{node_id}."):
                path = reference[len(node_id) + 1 :]
                return ParsedReference(
                    node_id=node_id, path=path, segments=tuple(_split_path(path))
                )

    node_id, _, path = reference.partition(".")
    return ParsedReference(node_id=node_id, path=path, segments=tuple(_split_path(path)))


def _split_path(path: str) -> list[str]:
    return [segment for segment in path.split(".") if segment]


def unwrap_runtime_wrapper(value: Any) -> Any:
    """Return the payload inside a runtime wrapper, or ``value`` unchanged.

    Applied at the ROOT of a resolution only (see the module docstring). A
    wrapper nested INSIDE data is left alone deliberately: at that point it is
    data the author addressed on purpose, and silently skipping a level would
    make a path mean two different things depending on where it appeared.
    """
    slug = kind_of(value)
    if slug not in WRAPPER_PAYLOAD_FIELDS:
        return value
    field = WRAPPER_PAYLOAD_FIELDS[slug]
    if isinstance(value, Mapping):
        return value.get(field)
    return getattr(value, field, None)


def _child(container: Any, key: str) -> tuple[Any, bool]:
    """One key lookup against a mapping or a model. Returns (value, present)."""
    if isinstance(container, Mapping):
        if key in container:
            return container[key], True
        return None, False
    if isinstance(container, BaseModel):
        if key in type(container).model_fields:
            return getattr(container, key), True
        # Wire name (``__kind``) and any populate-by-alias field: the payload
        # half of the boundary spells fields by alias, so a path authored
        # against serialized data must still resolve against the model.
        for name, field in type(container).model_fields.items():
            if field.alias == key or field.serialization_alias == key:
                return getattr(container, name), True
        return None, False
    if hasattr(container, key):
        return getattr(container, key), True
    return None, False


def resolve_path(root: Any, path: str, *, unwrap_root: bool = True) -> PathResolution:
    """Resolve ``path`` against ``root``, returning every value it reaches."""
    notes: list[str] = []
    current: list[Any] = [unwrap_runtime_wrapper(root) if unwrap_root else root]
    if current == [None] and unwrap_root and kind_of(root) in WRAPPER_PAYLOAD_FIELDS:
        notes.append(f"the {kind_of(root)} wrapper carried no payload — the step produced nothing")
        return PathResolution(reference=path, values=[], notes=notes)

    walked: list[str] = []
    for segment in _split_path(path):
        walked.append(segment)
        key, is_collection = (segment[:-2], True) if segment.endswith("[]") else (segment, False)
        here = ".".join(walked)
        next_values: list[Any] = []
        # A key that is not declared at all and a key that is declared but
        # null are BOTH holes to a consumer, and both are counted — an
        # explicitly-null optional (the common case: 1 of 3 results has no
        # rating) must not resolve silently to a shorter list than the author
        # expected.
        missing = 0
        for container in current:
            if container is None:
                missing += 1
                continue
            value, present = _child(container, key)
            if not present or value is None:
                missing += 1
                continue
            if is_collection:
                if isinstance(value, list | tuple):
                    next_values.extend(value)
                else:
                    notes.append(
                        f"'{here}' is declared as a collection but carried a "
                        f"{type(value).__name__} — using it as a single value. "
                        "The producing kind and the reference disagree; one of "
                        "them is wrong."
                    )
                    next_values.append(value)
            else:
                next_values.append(value)
        if missing:
            notes.append(f"'{here}' was absent on {missing} value(s)")
        current = next_values
        if not current:
            break

    return PathResolution(reference=path, values=current, notes=notes)


def resolve_reference(
    reference: str,
    node_outputs: Mapping[str, Any],
    *,
    known_node_ids: Sequence[str] | None = None,
) -> PathResolution:
    """Resolve a full ``<node>.<path>`` reference against a run's node outputs.

    ``node_outputs`` maps node id -> whatever that node produced (a raw payload
    or a runtime wrapper — both work). This is the call the picker's selection
    turns into at run time, and the reason a selection needs no extraction node.
    """
    parsed = parse_reference(reference, known_node_ids or list(node_outputs.keys()))
    if parsed.node_id not in node_outputs:
        return PathResolution(
            reference=reference,
            values=[],
            notes=[
                f"no step named '{parsed.node_id}' produced anything in this run "
                "(it may not have run yet, or the reference names a step that "
                "was renamed or deleted)"
            ],
            root_missing=True,
        )
    resolution = resolve_path(node_outputs[parsed.node_id], parsed.path)
    return resolution.model_copy(update={"reference": reference})


def has_kind_marker(value: Any) -> bool:
    """Whether a serialized payload carries the wire discriminator."""
    return isinstance(value, Mapping) and isinstance(value.get(KIND_KEY), str)
