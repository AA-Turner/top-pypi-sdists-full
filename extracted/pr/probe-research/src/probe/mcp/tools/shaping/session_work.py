"""remove the caller's own session work from rows, edges and provenance graphs."""

from __future__ import annotations
from typing import Any


#: Keys by which a view row NAMES another entity: its own id, an edge's two
#: ends, and the run a file or trial belongs to. A row naming a project,
#: experiment or run the caller's session created is that session's work (or
#: attached to it) and leaves the view.
_SESSION_WORK_REF_KEYS = ("id", "source_id", "target_id", "run_id")
#: Single-entity slots in a view payload ("where this came from", "which run
#: wrote it"). One naming the session's work is emptied rather than kept.
_SESSION_WORK_SLOTS = frozenset({"origin", "run", "written_by_run"})


def _names_session_work(node: dict, hidden: frozenset[str]) -> bool:
    for key in _SESSION_WORK_REF_KEYS:
        value = node.get(key)
        if isinstance(value, str) and value.lower() in hidden:
            return True
    label = node.get("uuid")
    if isinstance(label, str) and label.partition(":")[2].lower() in hidden:
        return True
    run = node.get("run")
    return isinstance(run, dict) and _names_session_work(run, hidden)


def _scrub_session_work(value: Any, hidden: frozenset[str]) -> Any:
    """`value` without the rows, edges and slots that name an entity in `hidden`
    (ids the caller's session created). Deterministic and structural: it walks
    every list and dict, so a view added later is covered without being named."""
    if isinstance(value, list):
        return [
            _scrub_session_work(item, hidden)
            for item in value
            if not (isinstance(item, dict) and _names_session_work(item, hidden))
        ]
    if isinstance(value, dict):
        return {
            key: (
                None
                if key in _SESSION_WORK_SLOTS
                and isinstance(item, dict)
                and _names_session_work(item, hidden)
                else _scrub_session_work(item, hidden)
            )
            for key, item in value.items()
        }
    return value


def _typed_id_names(value: Any, hidden: frozenset[str]) -> bool:
    """Whether a typed node id (`run:<uuid>`, `artifact_version:<uuid>`,
    `file:<sha256>`) names an entity in `hidden`, which holds bare ids."""
    return isinstance(value, str) and value.partition(":")[2].lower() in hidden


def _scrub_provenance_graph(payload: Any, hidden: frozenset[str]) -> Any:
    """A `GET /v1/provenance` graph without the nodes that name `hidden` work
    and every edge that names one of them.

    Its own pass because its ids are TYPED (`node_id = f"{type}:{id}"`) and
    its edges name nodes by `from` / `to`, neither of which the structural
    scrub reads: without this, the session's runs stayed in a lineage graph
    under `X-Probe-Hide-Session-Work`. A methods-view step whose run is hidden
    goes with the structural scrub (`step.run.id` is a bare id)."""
    if not isinstance(payload, dict):
        return payload
    nodes, edges = payload.get("nodes"), payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return payload
    return {
        **payload,
        "nodes": [
            node
            for node in nodes
            if not (isinstance(node, dict) and _typed_id_names(node.get("id"), hidden))
        ],
        "edges": [
            edge
            for edge in edges
            if not (
                isinstance(edge, dict)
                and (
                    _typed_id_names(edge.get("from"), hidden)
                    or _typed_id_names(edge.get("to"), hidden)
                )
            )
        ],
    }
