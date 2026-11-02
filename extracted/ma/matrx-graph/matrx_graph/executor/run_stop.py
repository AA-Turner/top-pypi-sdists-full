"""Why a COMPLETED run stopped early — the one run-level reason a step can declare.

A run that ends because a condition step said "no" and the engine PRUNED the conditional
edge after it completes cleanly — and, without this, cannot be told apart from a run that
did everything (lane 11 fix round, 2026-10-02). The status stays ``completed`` (the
``workflow.run`` CHECK has no other value for it, and it IS a clean finish); the reason
rides beside it.

THE CONTRACT. A node output may carry ``run_stop: {reason, says}`` meaning "if nothing I
feed runs, this is why the run stopped here". At completion the scheduler keeps the FIRST
such declaration (in execution order) whose node has no successor that produced an output
in this run, and returns it as ``RunResult.stopped`` = ``{reason, says, step}``; the run
store writes it to ``workflow.run.metadata.stopped`` in the same statement as the
completion. A declaration whose successors DID run (the author wired the next step
unconditionally) is dropped — the run did not stop there, so it never says so — and so is
one beside a parallel branch that also ran.

A CAUGHT FAILURE STOPS A RUN TOO (2026-10-27). A step that FAILED — a Safety Check
(``data.assert``) that did not hold, a planned step not built yet — whose failure an ERROR
connection caught, while none of the steps its normal connections lead to (or anything after
them) ran, is where the run stopped: ``{reason: <the failure's code>, says: <its message>,
step}``. Before, the run read plain ``completed`` and only a review flag on the step said it
had ended at a failed check (Law 4). A declared ``run_stop`` wins over a caught failure; a
failure whose recovery path rejoined the normal path (a step after it ran) is not a stop.

DISPLAY, NEVER AUTHORITY: ``metadata.stopped`` and ``status`` live on ``workflow.run``, which
the run's owner can UPDATE through PostgREST. Runs shows them; nothing decides on them.
"""

from __future__ import annotations

from typing import Any

#: The output field a node declares its stop reason in.
RUN_STOP_FIELD = "run_stop"
#: Where the run store records it.
RUN_STOP_METADATA_KEY = "stopped"


def _ancestors(edges: list[Any], node_id: str) -> set[str]:
    seen: set[str] = set()
    frontier = [node_id]
    while frontier:
        current = frontier.pop()
        for edge in edges:
            if edge.target_node_id == current and edge.source_node_id not in seen:
                seen.add(edge.source_node_id)
                frontier.append(edge.source_node_id)
    return seen


def _descendants(edges: list[Any], node_ids: set[str]) -> set[str]:
    seen = set(node_ids)
    frontier = list(node_ids)
    while frontier:
        current = frontier.pop()
        for edge in edges:
            if edge.source_node_id == current and edge.target_node_id not in seen:
                seen.add(edge.target_node_id)
                frontier.append(edge.target_node_id)
    return seen


def _caught_failure_stop(
    edges: list[Any], produced: set[str], caught: dict[str, dict[str, str]]
) -> dict[str, Any] | None:
    from matrx_graph.types.primitives import EdgeKind

    for node_id, failure in caught.items():
        normal_next = {
            e.target_node_id
            for e in edges
            if e.source_node_id == node_id and getattr(e, "kind", None) is not EdgeKind.ERROR
        }
        if normal_next and _descendants(edges, normal_next) & produced:
            continue
        return {"reason": str(failure.get("code") or "step_failed"), "says": failure.get("message"),
                "step": node_id}
    return None


def declared_run_stop(
    graph: Any, last_outputs: dict[str, Any], *, caught: dict[str, dict[str, str]] | None = None
) -> dict[str, Any] | None:
    """The run-level stop record for a completed run, or None.

    Only when the declaring step's pruned successors were the ONLY remaining path: every
    step that produced an output is that step or one of its ancestors. When a parallel
    branch also ran, the run did more than stop there — the reason stays on the step's own
    output (``run_stop``) and the run records none (lane 11 round 3).
    """
    produced = set(last_outputs)
    edges = list(getattr(graph, "edges", {}).values())
    for node_id, dump in last_outputs.items():
        if not isinstance(dump, dict):
            continue
        stop = dump.get(RUN_STOP_FIELD)
        if not isinstance(stop, dict) or not stop.get("reason"):
            continue
        if produced - ({node_id} | _ancestors(edges, node_id)):
            continue
        return {"reason": str(stop["reason"]), "says": stop.get("says"), "step": node_id}
    return _caught_failure_stop(edges, produced, caught or {})


def _label(label: Any, node_id: str) -> str:
    return f"'{(label(node_id) if label else None) or node_id}'"


def _why_never_ran(
    graph: Any,
    node_id: str,
    ran: set[str],
    failed: dict[str, dict[str, str]],
    gate_dropped: dict[str, str],
) -> tuple[str, str] | None:
    """Why ``node_id`` never ran, when the reason is a FAULT: ``("failed", step)`` — a step
    upstream failed — or ``("error_gate", step)`` — the error-handler gate dropped a step that
    had its data. Walks back through steps that never ran; a step that ran stops the walk
    (whatever left its connection unused was a branch not taken). None = an ordinary finish."""
    if node_id in gate_dropped:
        return ("error_gate", node_id)
    edges = list(getattr(graph, "edges", {}).values())
    seen = {node_id}
    frontier = [node_id]
    while frontier:
        current = frontier.pop(0)
        for edge in edges:
            if edge.target_node_id != current or edge.source_node_id in seen:
                continue
            source = edge.source_node_id
            seen.add(source)
            if source in failed:
                return ("failed", source)
            if source in gate_dropped:
                return ("error_gate", source)
            if source not in ran:
                frontier.append(source)
    return None


def undelivered_deliverables(
    graph: Any,
    ran: set[str],
    *,
    failed: dict[str, dict[str, str]],
    gate_dropped: dict[str, str],
    label: Any = None,
) -> list[dict[str, str]]:
    """The run's declared deliverables lost to a FAULT, when none of them was delivered.

    Declared = THE deliverable rule (``types.deliverables.deliverable_node_ids``, one
    definition). When any declared deliverable produced an output the run delivered → ``[]``.
    When none did, each one is judged by WHY it never ran:

    * a step upstream FAILED (caught by an error connection, or ``optional``) → a finding;
    * the error-handler gate dropped a step that had its data → a finding;
    * a branch not taken / an end step reached → ordinary, no finding (an Agent build that
      ends at "stopped" or "needs a model" never reaches its result steps, by design);
    * the deliverable ITSELF is ``optional`` and failed → fail-soft, no finding.

    Each finding is ``{step, cause, by, says}``: the deliverable, ``failed``/``error_gate``, the
    step that caused it, and the sentence that says so (2026-10-27, runs f2735de2 + f49a418d).
    """
    from matrx_graph.types.deliverables import deliverable_node_ids

    declared = deliverable_node_ids(graph)
    if not declared or any(nid in ran and nid not in failed for nid in declared):
        return []
    findings: list[dict[str, str]] = []
    for nid in declared:
        node = graph.nodes[nid]
        if nid in failed:
            if getattr(node, "optional", False):
                continue  # fail-soft: the author allowed this step to fail
            says = f"{_label(label, nid)} failed: {failed[nid].get('message') or 'no message'}."
            findings.append({"step": nid, "cause": "failed", "by": nid, "says": says})
            continue
        why = _why_never_ran(graph, nid, ran, failed, gate_dropped)
        if why is None:
            continue
        cause, by = why
        if cause == "failed":
            says = (
                f"{_label(label, nid)} never ran because {_label(label, by)} failed: "
                f"{failed[by].get('message') or 'no message'}."
            )
        else:
            silent = gate_dropped[by]
            says = (
                f"{_label(label, nid)} never ran because {_label(label, by)} had its data but "
                f"also waits on an error connection from {_label(label, silent)}, which did not "
                "fail, so it was skipped."
            )
        findings.append({"step": nid, "cause": cause, "by": by, "says": says})
    return findings


__all__ = ["RUN_STOP_FIELD", "RUN_STOP_METADATA_KEY", "declared_run_stop", "undelivered_deliverables"]
