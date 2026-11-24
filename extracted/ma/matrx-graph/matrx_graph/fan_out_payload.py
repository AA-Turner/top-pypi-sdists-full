"""A For each item carries ITS element of a per-item list, never the whole list (FX8, 2026-11-02).

A per-item template (``control.map``'s ``payload_template`` — which is what ``data.for_each`` on a
step becomes — and ``data.map_template``'s ``template``) resolves ``$in.<key>`` against the step's
OTHER inputs. When ``<key>`` is a list with one element per item, a bare ``"$in.<key>"`` copies the
WHOLE list into every one of the N items: N items x the list = N x N elements, held in memory, sent,
checkpointed and evented once per item. Small lists never notice; large ones kill the worker.

Live, run 424e086e (Brand foundation, 2026-11-02): subgraph b6ca80bb fanned 30 checks out with
``src: "$in.batches"``; each batch held ~312 KB, so every item carried ~9.4 MB and the step ~280 MB.
The worker stalled at ``check~each`` four times and recovery gave up. The fix selects the item's own
element: ``["$in.batches.[batch_id={$item.values.0.batch_id}]"]``.

``whole_list_payload_findings`` names every bare ``$in.<key>`` (or bare ``$in``, or a ``$format``
``{in.<key>}``) in a per-item template whose ``<key>`` is PROVABLY a per-item list:

* ``selected_elsewhere`` — the same template also reads ``$in.<key>`` one element per item
  (``.{$index}`` or ``.[field={$item…}]``, both of which only a list answers): the author already knows the list has one
  element per item, and the bare reference is the unfiltered copy (the 424e086e shape);
* ``iterated_list`` — ``<key>`` arrives from the same upstream field as ``items``: the list being
  iterated, copied into each of its own items (N x N by construction);
* ``iterated_elsewhere`` — ``<key>`` arrives from the upstream field another For each in the same
  workflow iterates as its ``items``: a per-item collection (one element per batch, page, row…)
  broadcast whole to every item (the 424e086e wiring: ``ask`` iterated ``take.batches``, ``check``
  received ``take.batches`` whole).

Each finding carries the fix: the selector the template already uses, else the two lawful shapes
(``$in.<key>.{$index}`` for index-aligned lists, ``$in.<key>.[<id>={$item.<id path>}]`` to join by id).

Pure: the validator (an ERROR on every save / publish / validate door for the first two codes — a
patch that introduces one is refused; a WARNING for ``iterated_elsewhere``) and the live scanner
(aidream ``scripts/check_fan_out_payloads.py``) call this function.
"""

from __future__ import annotations

import matrx_graph.information as _information

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

#: ``node_type -> (config_key, list_input_key)``: every node holding a per-item template.
from matrx_graph.shape_probe import TEMPLATE_HOSTS

if TYPE_CHECKING:
    from matrx_graph.types.definition import Definition

CODES = ("selected_elsewhere", "iterated_list", "iterated_elsewhere")
#: Provably N x N: the validator REFUSES these. ``iterated_elsewhere`` is a warning — the other For
#: each's list is per item THERE, and a small one may be meant for every item here.
REFUSED_CODES = frozenset({"selected_elsewhere", "iterated_list"})

_IN_PREFIX = "$in."
#: ``{in.key}`` / ``{in.key:join}`` write the whole list into the text; ``:n`` / ``:count`` write a number.
_FORMAT_WHOLE = re.compile(r"\{in\.([A-Za-z0-9_]+)(?::join)?\}")
#: Operators whose strings are not values copied into the item (``$uuid5`` refuses a list part).
_NOT_COPIED = frozenset({"$uuid5", "$run"})


@dataclass(frozen=True)
class WholeListFinding:
    code: str
    #: The step that runs (or shapes) once per item — the authored step for ``data.for_each``.
    step_id: str
    #: The expanded node holding the template (``<step>~each`` for ``data.for_each``).
    node_id: str
    node_type: str
    #: The input key whose whole list every item carries.
    key: str
    #: The template location (dot path inside the template) holding the bare reference.
    where: str
    #: The per-item selector already used for ``key`` in the same template, when there is one.
    selector: str | None
    #: Where ``key`` arrives from: ``"<node>.<field>"``, when a mapped connection says.
    source: str | None
    message: str

    @property
    def refused(self) -> bool:
        return self.code in REFUSED_CODES


def _segments(path: str) -> list[str]:
    from matrx_graph.nodes._template import _segments as split

    return split(path)


def _is_per_item_segment(segment: str) -> bool:
    """A segment that PROVES the value is a list read one element per item: a position
    (``{$index}``) or a selector (``[field={$item…}]``). ``{$item.x}`` alone is not proof — it may
    be a key into a lookup table (a dict) that is legitimately needed whole elsewhere."""
    if segment == "{$index}":
        return True
    return segment.startswith("[") and "=" in segment and ("{$item" in segment or "{$index}" in segment)


def _walk(template: Any, where: str, whole: list[tuple[str, str]], selected: dict[str, str]) -> None:
    """Collect bare ``$in.<key>`` references (``whole``: (key, where)) and, per key, the first
    per-item selector prefix the template reads it through (``selected``)."""
    if isinstance(template, str):
        if template == "$in":
            whole.append(("*", where))
            return
        if not template.startswith(_IN_PREFIX):
            return
        parts = _segments(template[len(_IN_PREFIX):])
        if len(parts) == 1:
            whole.append((parts[0], where))
        elif _is_per_item_segment(parts[1]):
            selected.setdefault(parts[0], f"$in.{parts[0]}.{parts[1]}")
        return
    if isinstance(template, dict):
        if any(op in template for op in _NOT_COPIED):
            return
        fmt = template.get("$format")
        if isinstance(fmt, str):
            for match in _FORMAT_WHOLE.finditer(fmt):
                whole.append((match.group(1), f"{where}.$format" if where else "$format"))
        for key, value in template.items():
            if key == "$format":
                continue
            _walk(value, f"{where}.{key}" if where else str(key), whole, selected)
        return
    if isinstance(template, list):
        for i, value in enumerate(template):
            _walk(value, f"{where}.{i}" if where else str(i), whole, selected)


def _input_sources(definition: Definition, node_id: str) -> dict[str, str]:
    """``input key -> "<source node>.<source field>"`` for every data connection into the node."""
    from matrx_graph.step_settings import owner_of

    sources: dict[str, str] = {}
    for edge in definition.edges:
        if edge.target != node_id or edge.kind.value in ("error", "stream", "control"):
            continue
        origin = owner_of(edge.source) or edge.source
        mappings = edge.mappings
        if mappings is None:
            continue
        for key, source_path in mappings.items():
            if isinstance(source_path, str) and source_path:
                sources[str(key)] = f"{origin}.{source_path}"
    return sources


def _fix_text(key: str, selector: str | None, for_each: bool) -> str:
    where = "data.for_each.payload_template" if for_each else "the template"
    if selector:
        return (
            f"Read only this item's element, the way {where} already does elsewhere: "
            f"[\"{selector}\"] (keep the list brackets when the step expects a list), "
            f"or \"{selector}.<field>\" for one field of it."
        )
    return (
        f"Read only this item's element in {where}: \"$in.{key}.{{$index}}\" when the lists are "
        f"index-aligned, or [\"$in.{key}.[<id field>={{$item.<id path>}}]\"] to join by id "
        f"(keep the list brackets when the step expects a list)."
    )


def whole_list_payload_findings(definition: Definition, *, expanded: bool = False) -> list[WholeListFinding]:
    """Every per-item template that copies a per-item list whole into each item (module docstring)."""
    definition = _information.executable_of(definition)  # a note is not a step
    from matrx_graph.step_settings import expand_step_settings, owner_of

    if not expanded:
        definition = expand_step_settings(definition)

    hosts = [n for n in definition.nodes if n.spec_type in TEMPLATE_HOSTS]
    sources_of = {n.id: _input_sources(definition, n.id) for n in hosts}
    iterated: dict[str, str] = {}
    for node in hosts:
        list_key = TEMPLATE_HOSTS[node.spec_type][1]
        src = sources_of[node.id].get(list_key)
        if src:
            iterated.setdefault(src, owner_of(node.id) or node.id)

    findings: list[WholeListFinding] = []
    for node in hosts:
        config_key, list_key = TEMPLATE_HOSTS[node.spec_type]
        template = node.config.get(config_key) if isinstance(node.config, dict) else None
        if template is None:
            continue
        whole: list[tuple[str, str]] = []
        selected: dict[str, str] = {}
        _walk(template, "", whole, selected)
        if not whole:
            continue
        sources = sources_of[node.id]
        items_source = sources.get(list_key)
        step_id = owner_of(node.id) or node.id
        for_each = step_id != node.id
        step_name = next((n.label for n in definition.nodes if n.id == step_id and n.label), step_id)
        seen: set[tuple[str, str]] = set()
        for key, where in whole:
            keys = [k for k in sources if k != list_key] if key == "*" else [key]
            for k in keys:
                if (k, where) in seen:
                    continue
                src = sources.get(k)
                selector = selected.get(k)
                if selector:
                    code, why = "selected_elsewhere", (
                        f"the same template reads it per item as '{selector}', so it holds one element "
                        "per item"
                    )
                elif src and items_source and src == items_source:
                    code, why = "iterated_list", f"it is the list being iterated ('{src}')"
                elif src and src in iterated and iterated[src] != step_id:
                    code, why = "iterated_elsewhere", (
                        f"it is '{src}', the list the For each on '{iterated[src]}' iterates — one element "
                        "per item"
                    )
                else:
                    continue
                seen.add((k, where))
                ref = "$in" if key == "*" else f"$in.{k}"
                findings.append(WholeListFinding(
                    code=code, step_id=step_id, node_id=node.id, node_type=node.spec_type, key=k,
                    where=where, selector=selector, source=src,
                    message=(
                        f"'{step_name}': the per-item value '{where or config_key}' is '{ref}', which copies "
                        f"the WHOLE '{k}' list into every item — N items x the list, held, sent and saved "
                        f"once per item (run 424e086e died this way: 30 items x ~9 MB). {why[0].upper()}{why[1:]}. "
                        + _fix_text(k, selector, for_each)
                    ),
                ))
    return findings
