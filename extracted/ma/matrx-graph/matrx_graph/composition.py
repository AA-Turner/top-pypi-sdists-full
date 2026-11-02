"""The PARENT→CHILD input contract for composed graphs (``subgraph.call``).

🚨 THE FAILURE THIS EXISTS TO KILL (live, 2026-08-19, podcast challenger).
A child organ (W6, "Audio Render") gained a REQUIRED entry field (``cast_json``)
and was published to the live registry. Its parent (W0) — which must supply that
field — was published ~2 minutes later, because a parent references its children
by live id and therefore *cannot* be written first. A race that started inside
that window died at the seam::

    Node 'call_w6' failed: child_run_errored: subgraph.call: child run … ended
    errored: NodeInputValidationError: 'cast_json' is a required property

Nothing could see it coming. Validation is per-definition: the child validates,
the parent validates, and the mismatch lives strictly BETWEEN them. The gating
rule's guard (D-48) is single-definition by construction and structurally cannot
reach across a ``subgraph.call``.

What this module adds is the missing cross-definition check: for every
``subgraph.call`` in a parent, every REQUIRED field of the child's entry node
must be supplied by the parent. It is a pure function over built definitions, so
it runs in a unit test at authoring time — long before anything is published —
and again in the seeder over the whole set BEFORE the first write, so a child
contract can never reach the registry ahead of the parent that feeds it.

**Undeterminable is a REFUSAL, not a pass.** When the parent's supply for a call
cannot be read statically, that call is reported as ``undeterminable`` and the
caller decides — never silently treated as satisfied. A guard that quietly skips
what it cannot parse is how the seam broke in the first place.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field

from matrx_graph.types.definition import Definition, NodeDef

#: The node type whose ``config.definition_id`` names a child definition.
SUBGRAPH_CALL = "subgraph.call"

#: The entry-node type whose ``config.fields`` declare a definition's contract.
USER_INPUT = "io.user_input"

#: The node type a parent conventionally uses to build a call's ``inputs`` dict.
DATA_TRANSFORM = "data.transform"


def required_entry_fields(definition: Definition) -> set[str]:
    """The field keys a run of ``definition`` MUST be given.

    A field marked ``required`` but carrying a ``default`` is still required —
    the schema is the contract, and the executor refuses on a missing value
    regardless of what a default would have produced. (An author who means "use
    the default when absent" writes ``required: False``; a field that is both
    required and defaulted is a contradiction worth seeing, not smoothing over.)
    """
    keys: set[str] = set()
    for node in definition.nodes:
        if node.spec_type != USER_INPUT:
            continue
        for fld in (node.data.get("config") or {}).get("fields") or []:
            if isinstance(fld, dict) and fld.get("required") and fld.get("key"):
                keys.add(str(fld["key"]))
    return keys


def _supplied_keys_from_expression(expression: str) -> set[str] | None:
    """The literal keys a transform expression puts under ``inputs``.

    Returns ``None`` when the expression is not a literal mapping we can read —
    the caller must treat that as undeterminable, never as satisfied.
    """
    try:
        tree = ast.parse(expression.strip(), mode="eval")
    except SyntaxError:
        return None
    outer = tree.body
    if not isinstance(outer, ast.Dict):
        return None
    for key, value in zip(outer.keys, outer.values, strict=False):
        if not (isinstance(key, ast.Constant) and key.value == "inputs"):
            continue
        if not isinstance(value, ast.Dict):
            return None
        keys: set[str] = set()
        for inner_key in value.keys:
            if not (isinstance(inner_key, ast.Constant) and isinstance(inner_key.value, str)):
                return None  # a computed key — unreadable, so undeterminable
            keys.add(inner_key.value)
        return keys
    return None


def _supplied_keys_for_call(parent: Definition, call: NodeDef) -> set[str] | None:
    """What the parent hands this ``subgraph.call`` as the child's run inputs.

    Two authored shapes are readable: the call's own literal
    ``config``/``input`` ``inputs`` dict, and — the convention every organ
    parent uses — a ``data.transform`` feeding the call's ``inputs`` port with a
    literal ``{'inputs': {...}}`` expression.
    """
    for holder in (call.data.get("input") or {}, call.data.get("config") or {}):
        literal = holder.get("inputs")
        if isinstance(literal, dict) and literal:
            return set(map(str, literal.keys()))

    feeders = [
        e
        for e in parent.edges
        if e.target == call.id and "inputs" in ((e.data or {}).get("mappings") or {})
    ]
    if len(feeders) != 1:
        # Zero feeders means nothing supplies the child at all; more than one
        # means the payload is assembled by the engine's merge and no single
        # expression tells the truth about it.
        return None
    source = next((n for n in parent.nodes if n.id == feeders[0].source), None)
    if source is None or source.spec_type != DATA_TRANSFORM:
        return None
    expression = (source.data.get("config") or {}).get("expression")
    if not isinstance(expression, str):
        return None
    return _supplied_keys_from_expression(expression)


@dataclass(frozen=True)
class CallContract:
    """One ``subgraph.call`` measured against the child it calls."""

    call_node_id: str
    child_definition_id: str
    child_label: str
    required: frozenset[str]
    supplied: frozenset[str] | None

    @property
    def undeterminable(self) -> bool:
        return self.supplied is None

    @property
    def missing(self) -> frozenset[str]:
        if self.supplied is None:
            return frozenset()
        return frozenset(self.required - self.supplied)

    def problem(self) -> str | None:
        if self.undeterminable:
            return (
                f"{self.call_node_id} → {self.child_label}: the parent's supply "
                "cannot be read statically, so this seam is UNVERIFIED. Feed the "
                "call from exactly one data.transform whose expression is a "
                "literal {'inputs': {...}} mapping, or give the call a literal "
                "inputs dict."
            )
        if self.missing:
            return (
                f"{self.call_node_id} → {self.child_label}: the child REQUIRES "
                f"{sorted(self.missing)} and the parent supplies "
                f"{sorted(self.supplied or ())}. A run reaching this call dies "
                "with NodeInputValidationError. Add the field(s) to the parent's "
                "pack step, or make them optional on the child."
            )
        return None


@dataclass
class CompositionReport:
    contracts: list[CallContract] = field(default_factory=list)
    #: Calls whose child definition was not among the ones handed in.
    unresolved_children: list[str] = field(default_factory=list)

    @property
    def problems(self) -> list[str]:
        found = [p for c in self.contracts if (p := c.problem()) is not None]
        found += [
            f"{call_id}: child definition not supplied to the check — the seam is UNVERIFIED"
            for call_id in self.unresolved_children
        ]
        return found

    def raise_for_problems(self, *, parent_label: str) -> None:
        problems = self.problems
        if problems:
            joined = "\n  - ".join(problems)
            raise ValueError(
                f"{parent_label}: the parent→child input contract is broken:\n  - {joined}"
            )


def check_composition_contract(
    parent: Definition, children: dict[str, Definition]
) -> CompositionReport:
    """Measure every ``subgraph.call`` in ``parent`` against its child.

    ``children`` maps the ``definition_id`` each call names to that child's
    built :class:`Definition`.
    """
    report = CompositionReport()
    for node in parent.nodes:
        if node.spec_type != SUBGRAPH_CALL:
            continue
        child_id = str((node.data.get("config") or {}).get("definition_id") or "")
        child = children.get(child_id)
        if child is None:
            report.unresolved_children.append(node.id)
            continue
        supplied = _supplied_keys_for_call(parent, node)
        report.contracts.append(
            CallContract(
                call_node_id=node.id,
                child_definition_id=child_id,
                child_label=str(child.metadata.get("challenger_stage") or child_id),
                required=frozenset(required_entry_fields(child)),
                supplied=None if supplied is None else frozenset(supplied),
            )
        )
    return report


__all__ = [
    "CallContract",
    "CompositionReport",
    "check_composition_contract",
    "required_entry_fields",
]
