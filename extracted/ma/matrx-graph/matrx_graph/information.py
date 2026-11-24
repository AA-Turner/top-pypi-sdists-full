"""Information nodes: the engine seam.

An information node (``info.note``, ``info.frame``, ``info.media``, ``info.kind``, ``info.record``
and the reference cards) is stored in a graph's ``nodes`` and NEVER runs: its spec declares
``executes = False``. A ``relation`` edge attaches one to anything and carries nothing. This module is
the ONE place that takes them out of the executable graph (one-graph CONTRACTS §2.3):

* ``split_information(definition) -> (executable, info_nodes, relation_edges)`` — called beside
  ``expand_step_settings`` in ``validate_definition`` and ``compile``. Information nodes and relation
  edges never reach a ``CompiledGraph``; the scheduler asserts it.
* ``information_problems(definition)`` — what is wrong with the information content itself
  (unknown type, a plain edge on a note, an entry node or result that is a note, a bad ``parentId``).
* ``hash_projection(definition)`` / ``definition_hash`` — the hash is computed over the executable
  projection, so a definition with no information content hashes byte-identically to what
  ``_hash_definition`` always produced, and editing a note never changes it.
* ``executable_node_types(definition)`` — what a worker must be able to run (worker capability).
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, NamedTuple

from matrx_graph.types.definition import Definition, EdgeDef, NodeDef
from matrx_graph.types.primitives import EdgeKind

INFO_PREFIX = "info."
#: ``node.type`` (the renderer category) of every information node.
INFO_NODE_TYPE = "info"
FRAME_SPEC_TYPE = "info.frame"
#: Presentation metadata the one-graph migration lifts into nodes; excluded from the hash while
#: it still carries content (an EMPTY key was always part of the hash and stays so).
LEGACY_PRESENTATION_KEYS = ("annotations", "groups")
#: ``metadata`` key the one-graph migration writes on a row it rewrote: ``[{"old": <hash>, "new": <hash>}]``,
#: the whole-document hash the row had before (what runs and triggers recorded) beside the hash it has now.
#: A hash consumer accepts every ``old`` (``legacy_hashes``). Never part of any hash.
HASH_ALIASES_KEY = "definition_hash_aliases"
HASH_RECORD_KEYS = (HASH_ALIASES_KEY,)


class InformationSplit(NamedTuple):
    executable: Definition
    info_nodes: list[NodeDef]
    relation_edges: list[EdgeDef]


class InformationProblem(NamedTuple):
    path: str
    message: str
    node_id: str | None = None
    edge_id: str | None = None


def _registry(registry: Any | None) -> Any:
    if registry is not None:
        return registry
    from matrx_graph.executor.registry import default_registry

    reg = default_registry()
    reg.ensure_bootstrapped()
    return reg


def is_information_type(spec_type: str, registry: Any | None = None) -> bool:
    """THE rule: a type never runs when its registered spec declares ``executes = False``. A type the
    registry does not know falls back to the ``info.`` prefix (reported by ``information_problems``,
    and never run)."""
    reg = _registry(registry)
    if reg.has(spec_type):
        return not reg.get(spec_type).spec.executes
    return spec_type.startswith(INFO_PREFIX)


def is_information_raw(node_type: Any, spec_type: Any, registry: Any | None = None) -> bool:
    """The rule for a node's raw fields (``node.type``, ``data.spec_type``): renderer type ``info``,
    or a spec type that never runs. Both the Definition path and the stored-document path use this."""
    if node_type == INFO_NODE_TYPE:
        return True
    spec = spec_type if isinstance(spec_type, str) and spec_type else node_type
    return isinstance(spec, str) and is_information_type(spec, registry)


def is_information_node(node: Any, registry: Any | None = None) -> bool:
    """Accepts every node shape the engine reads: a ``NodeDef`` (``type`` + ``data.spec_type``) or a
    duck-typed node carrying only ``spec_type``."""
    data = getattr(node, "data", None)
    spec = getattr(node, "spec_type", None) or (data.get("spec_type") if isinstance(data, dict) else None)
    return is_information_raw(getattr(node, "type", None), spec, registry)


def information_node_ids(definition: Definition, registry: Any | None = None) -> set[str]:
    reg = _registry(registry)
    return {n.id for n in definition.nodes if is_information_node(n, reg)}


def _has_legacy_content(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0


def split_information(definition: Definition, registry: Any | None = None) -> InformationSplit:
    """Take every information node and relation edge out of ``definition``.

    ``executable`` is a copy with only runnable nodes and the edges between them. It also drops what
    the hash projection drops (legacy ``metadata.annotations`` / ``groups`` that still carry content)
    and prunes ``entry_nodes`` that name an information node (``information_problems`` reports it).
    A definition with no information content comes back equal to the input.
    """
    reg = _registry(registry)
    info_ids = {n.id for n in definition.nodes if is_information_node(n, reg)}
    legacy = [k for k in (*LEGACY_PRESENTATION_KEYS, *HASH_RECORD_KEYS) if _has_legacy_content(definition.metadata.get(k))]
    relation_edges = [
        e for e in definition.edges if e.data.get("kind") == EdgeKind.RELATION.value or e.source in info_ids or e.target in info_ids
    ]
    if not info_ids and not relation_edges and not legacy:
        return InformationSplit(definition, [], [])
    relation_ids = {e.id for e in relation_edges}
    updates: dict[str, Any] = {
        "nodes": [n for n in definition.nodes if n.id not in info_ids],
        "edges": [e for e in definition.edges if e.id not in relation_ids],
        "entry_nodes": [n for n in definition.entry_nodes if n not in info_ids],
    }
    if legacy:
        updates["metadata"] = {k: v for k, v in definition.metadata.items() if k not in legacy}
    executable = definition.model_copy(update=updates)
    return InformationSplit(
        executable,
        [n for n in definition.nodes if n.id in info_ids],
        relation_edges,
    )


def information_problems(definition: Definition, registry: Any | None = None) -> list[InformationProblem]:
    """Everything wrong with the information content of ``definition`` (errors; the caller decides)."""
    reg = _registry(registry)
    problems: list[InformationProblem] = []
    by_id = {n.id: n for n in definition.nodes}
    info_ids = {n.id for n in definition.nodes if is_information_node(n, reg)}
    for node in definition.nodes:
        if node.id not in info_ids:
            continue
        spec_type = node.spec_type
        if not reg.has(spec_type):
            problems.append(InformationProblem(
                f"nodes[{node.id}].data.spec_type",
                f"Unknown information type '{spec_type}'. Information nodes use a registered info.* type.",
                node_id=node.id,
            ))
            continue
        if node.data.get("is_primary"):
            problems.append(InformationProblem(
                f"nodes[{node.id}].data.is_primary",
                f"'{node.id}' is an information node and never runs, so it cannot be the workflow's result.",
                node_id=node.id,
            ))
    for nid in definition.entry_nodes:
        if nid in info_ids:
            problems.append(InformationProblem(
                "entry_nodes",
                f"entry_nodes names '{nid}', an information node. Information nodes never run, so they cannot start a run.",
                node_id=nid,
            ))
    for edge in definition.edges:
        touches = edge.source in info_ids or edge.target in info_ids
        is_relation = edge.data.get("kind") == EdgeKind.RELATION.value
        if touches and not is_relation:
            problems.append(InformationProblem(
                f"edges[{edge.id}].data.kind",
                f"Connection '{edge.id}' touches an information node but is not a relation. "
                "Information nodes attach with relation connections; they carry no data.",
                edge_id=edge.id,
            ))
        if is_relation:
            for end, label in ((edge.source, "source"), (edge.target, "target")):
                if end not in by_id:
                    problems.append(InformationProblem(
                        f"edges[{edge.id}].{label}",
                        f"Relation '{edge.id}' has no {label} node '{end}'.",
                        edge_id=edge.id,
                    ))
    for node in definition.nodes:
        parent = node.parentId
        if parent is None:
            continue
        holder = by_id.get(parent)
        if holder is None or holder.spec_type != FRAME_SPEC_TYPE:
            problems.append(InformationProblem(
                f"nodes[{node.id}].parentId",
                f"'{node.id}' sits in '{parent}', which is not a frame in this graph.",
                node_id=node.id,
            ))
            continue
        seen = {node.id}
        walker: NodeDef | None = holder
        while walker is not None and walker.parentId is not None:
            if walker.id in seen:
                problems.append(InformationProblem(
                    f"nodes[{node.id}].parentId", f"Frames '{node.id}' and '{walker.id}' contain each other.", node_id=node.id,
                ))
                break
            seen.add(walker.id)
            walker = by_id.get(walker.parentId)
    return problems


def executable_node_types(definition: Definition, registry: Any | None = None) -> list[NodeDef]:
    """The nodes of ``definition`` a worker must be able to run."""
    reg = _registry(registry)
    return [n for n in definition.nodes if not is_information_node(n, reg)]


#: Node fields this campaign added with a default; never part of the hash.
_HASH_EXCLUDED_NODE_FIELDS = ("parentId", "executes")


def hash_projection(definition: Definition, registry: Any | None = None) -> dict[str, Any]:
    """The JSON the definition hash is computed over: the executable part only. For a definition
    with no information content it is exactly ``definition.model_dump(mode="json")`` as it always was."""
    executable = split_information(definition, registry).executable
    payload = executable.model_dump(mode="json")
    for node in payload.get("nodes", []):
        for key in _HASH_EXCLUDED_NODE_FIELDS:
            node.pop(key, None)
    return payload


def definition_hash(definition: Definition, registry: Any | None = None) -> str:
    canonical = json.dumps(hash_projection(definition, registry), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]


def hash_projection_of_raw(raw: dict[str, Any], registry: Any | None = None) -> str:
    """The hash of a stored definition document (dict), tolerant of drafts that no longer validate
    only in the ways ``Definition`` tolerates. Used by the live-row proofs and the migration."""
    return definition_hash(Definition.model_validate(raw), registry)


class InformationReachedTheGraph(AssertionError):
    """An information node or relation edge was found in a CompiledGraph. Never expected."""


def assert_graph_is_executable(graph: Any) -> None:
    """The scheduler's guard: a CompiledGraph holds no information node and no relation edge."""
    reg = _registry(None)
    for node_id, node in graph.nodes.items():
        # The registry is the one rule (a spec that declares ``executes = False``); no name-prefix guess.
        if reg.has(node.spec_type) and not reg.get(node.spec_type).spec.executes:
            raise InformationReachedTheGraph(f"information node '{node_id}' ({node.spec_type}) reached the scheduler")
    for edge_id, edge in graph.edges.items():
        if edge.kind is EdgeKind.RELATION:
            raise InformationReachedTheGraph(f"relation edge '{edge_id}' reached the scheduler")


def legacy_definition_hash(definition: Definition) -> str:
    """The hash a definition had BEFORE information nodes existed: the whole expanded document,
    legacy ``metadata.annotations`` / ``groups`` and any information content included.

    A record trigger or a run stamped before this change recorded this value. Consumers of a
    recorded hash accept either it or ``definition_hash`` until the one-graph migration has
    re-stamped the rows that carry notes or frames (CONTRACTS §2.3, §2.5); for a definition with
    no information content the two are equal.
    """
    from matrx_graph.step_settings import expand_step_settings

    payload = expand_step_settings(definition).model_dump(mode="json")
    for node in payload.get("nodes", []):
        node.pop("parentId", None)
    for key in HASH_RECORD_KEYS:
        payload.get("metadata", {}).pop(key, None)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]


def hash_aliases(definition: Definition) -> set[str]:
    """The ``old`` hashes the one-graph migration recorded on this definition (CONTRACTS §2.3)."""
    raw = definition.metadata.get(HASH_ALIASES_KEY)
    if not isinstance(raw, list):
        return set()
    return {p["old"] for p in raw if isinstance(p, dict) and isinstance(p.get("old"), str) and p["old"]}


def legacy_hashes(definition: Definition) -> set[str]:
    """Every hash an older run or trigger may have recorded for this definition besides
    ``definition_hash``: the whole-document hash, and the hashes it had before the migration moved
    its notes and frames into nodes. THE set a hash consumer checks a recorded hash against."""
    return {legacy_definition_hash(definition), *hash_aliases(definition)}


def executable_of(definition: Any) -> Any:
    """``definition`` without its information nodes and relation edges — for the readers of a raw
    Definition that count steps, connections or terminals (a note is not a step). A dict (a stored
    document) comes back as a dict; anything else (a CompiledGraph, None) is returned as it is."""
    if isinstance(definition, Definition):
        return split_information(definition).executable
    if isinstance(definition, dict) and isinstance(definition.get("nodes"), list):
        info_ids = {
            n.get("id") for n in definition["nodes"]
            if isinstance(n, dict) and is_information_raw(n.get("type"), (n.get("data") or {}).get("spec_type"))
        }
        edges = [
            e for e in definition.get("edges") or []
            if isinstance(e, dict)
            and (e.get("data") or {}).get("kind") != EdgeKind.RELATION.value
            and e.get("source") not in info_ids and e.get("target") not in info_ids
        ]
        if not info_ids and len(edges) == len(definition.get("edges") or []):
            return definition
        return {**definition, "nodes": [n for n in definition["nodes"] if n.get("id") not in info_ids], "edges": edges}
    return definition


# ── The stored spelling of an information node, as an author may write it ────────────────────────
#: Where a note sits above the steps it explains, and how far apart they are kept.
NOTE_GAP_ABOVE_STEPS = 260
#: A note farther than this from the steps' bounding box is brought back beside them.
NOTE_MAX_DISTANCE = 700


def canonical_information_node(raw: Any, registry: Any | None = None) -> Any:
    """An information node as the store keeps it: ``type: "info"``, ``data.spec_type`` the spec, and
    the spec's fields FLAT in ``data`` (``text``, ``color`` ...). An author (the Conductor) writes the
    step-shaped spelling — ``type: "info.note"`` with the fields under ``data.config`` — and every
    reader (the Studio face, the minimap, the engine split) reads the stored one, so the two are
    reconciled once, here, at the write door. Anything that is not an information node, or is not a
    dict, comes back unchanged. Idempotent."""
    if not isinstance(raw, dict):
        return raw
    node_type = raw.get("type")
    data = raw.get("data") if isinstance(raw.get("data"), dict) else {}
    spec = data.get("spec_type") if isinstance(data.get("spec_type"), str) and data.get("spec_type") else None
    if spec is None and isinstance(node_type, str) and node_type != INFO_NODE_TYPE:
        spec = node_type
    if not is_information_raw(node_type, spec, registry):
        return raw
    if spec is None or not spec.startswith(INFO_PREFIX):
        return raw
    flat = {k: v for k, v in data.items() if k != "config"}
    config = data.get("config")
    if isinstance(config, dict):
        for key, value in config.items():
            flat.setdefault(key, value)
    flat["spec_type"] = spec
    return {**raw, "type": INFO_NODE_TYPE, "data": flat}


def place_information_nodes(
    nodes: list[dict[str, Any]], registry: Any | None = None, movable: set[str] | None = None
) -> list[str]:
    """Bring an agent's note that sits nowhere near the steps it explains back above them (left edge
    of the steps' box). A node with a position within ``NOTE_MAX_DISTANCE`` of the steps keeps it; a
    frame is never moved (it holds steps by ``parentId``). ``movable`` (the ids a write adds) limits it:
    a note the person already placed is never moved. Mutates ``nodes``; returns the moved ids."""
    steps: list[tuple[float, float]] = []
    infos: list[dict[str, Any]] = []
    for n in nodes:
        if not isinstance(n, dict):
            continue
        data = n.get("data") if isinstance(n.get("data"), dict) else {}
        if is_information_raw(n.get("type"), data.get("spec_type"), registry):
            infos.append(n)
            continue
        pos = n.get("position")
        if isinstance(pos, dict) and isinstance(pos.get("x"), (int, float)) and isinstance(pos.get("y"), (int, float)):
            steps.append((float(pos["x"]), float(pos["y"])))
    if not steps:
        return []
    min_x = min(x for x, _ in steps)
    max_x = max(x for x, _ in steps)
    min_y = min(y for _, y in steps)
    max_y = max(y for _, y in steps)
    moved: list[str] = []
    for n in infos:
        data = n.get("data") if isinstance(n.get("data"), dict) else {}
        if data.get("spec_type") != "info.note":
            continue
        if movable is not None and str(n.get("id")) not in movable:
            continue
        pos = n.get("position")
        has = isinstance(pos, dict) and isinstance(pos.get("x"), (int, float)) and isinstance(pos.get("y"), (int, float))
        if has:
            x, y = float(pos["x"]), float(pos["y"])
            gap_x = max(min_x - x, 0.0, x - max_x)
            gap_y = max(min_y - y, 0.0, y - max_y)
            if max(gap_x, gap_y) <= NOTE_MAX_DISTANCE and not (x == 0 and y == 0 and (min_x, min_y) != (0, 0)):
                continue
        n["position"] = {"x": min_x, "y": min_y - NOTE_GAP_ABOVE_STEPS}
        moved.append(str(n.get("id")))
    return moved
