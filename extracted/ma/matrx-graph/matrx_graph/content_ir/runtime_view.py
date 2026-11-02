"""The runtime wrapper kinds ON THE WIRE — the packet the UI receives.

THE PACKET (Arman, 2026-08-20 — plan of record
``common-docs/systems/architecture/content-ir/FEATURE.md`` §10b item 8):

    "if you were to send that packet to the front end, the front end would know
    which workflow it came from, which node it came from, and then inside of
    it, it would see that it's a Brave search results, and inside of that, ten
    websites."

That packet is a ``node_outcome`` instance: run/workflow/node identity, timing,
the kind verdict, and the data kind NESTED under ``output``. This module is the
one place it is assembled, so persistence and transport cannot drift into two
dialects of the same envelope.

THE EDGE CONTRACT IS NOT TOUCHED (ratified, plan §4.1): workflow EDGES carry
the data kind only. The wrapper exists at persistence and at transport to the
UI — here — and a node that genuinely wants runtime context declares the
wrapper kind as its ``input_kind``, explicitly. Nothing in this module puts a
wrapper on an edge.

THE ELISION RULE
----------------
Where the frame carrying the wrapper ALREADY carries the payload —
``NodeCompletedEvent.output``, a run read response's ``output`` — the wrapper's
``output`` is dropped and ``output_ref`` names that sibling field. This is the
same rule the verified ``__ir`` envelope follows with ``value_ref``
(``content_ir.envelope.elide_envelope_value``), for the same reason: the dict
would otherwise be serialized twice per streamed event and twice per persisted
``wf_node_events`` row. A consumer rehydrates at its single ingest gate.

COMPLETE-ONLY, LIKE ``__ir``
-----------------------------
A wrapper describes SETTLED work: a node that finished, a run that terminated.
Progressive rendering of a still-arriving kind is a different contract on a
different channel (``__ir_partial``; ``common-docs/systems/architecture/content-ir/
STREAMING_PARTIAL_KINDS.md``), and the two never mix — a wrapper is never
emitted for a streaming block, and a partial never lands on a wrapper. One law
each, no overlap.

NEVER LOAD-BEARING
------------------
Building a view is pure and cheap, but a defect in it must never fail a run:
callers wrap the call in a loud fail-open exactly as the ``__ir`` stamping does
(scream at error level, ship the frame without the wrapper).
"""

from __future__ import annotations

from typing import Any

from matrx_graph.content_ir.wrappers import NodeOutcomeWrapper, RunResultWrapper
from matrx_graph.types.result import NodeError

__all__ = [
    "OUTPUT_REF_OUTPUT",
    "output_ref_for_key",
    "node_outcome_view",
    "run_result_view",
]

#: The conventional ``output_ref`` value: the payload rides the frame's own
#: ``output`` field (``NodeCompletedEvent.output``, ``RunRecord.output``).
OUTPUT_REF_OUTPUT = "output"


def output_ref_for_key(field: str, key: str) -> str | None:
    """``"<field>.<key>"`` — a ref INTO a frame field that is a map.

    A run's frame carries ``output`` as ``{terminal node id: payload}``, so one
    terminal wrapper's payload is addressed by path, not by field name. Dots
    are the ONLY separator a consumer has to split on, so a key that contains
    one is unaddressable: this returns ``None`` and the caller inlines that
    payload instead of emitting an ambiguous ref. Losing the elision costs
    bytes; guessing at a split would hand the consumer the wrong value.
    """
    if not field or not key or "." in key:
        return None
    return f"{field}.{key}"


def node_outcome_view(
    *,
    run_id: str,
    node_id: str,
    workflow_id: str | None = None,
    step: int | None = None,
    attempt: int = 1,
    status: str = "completed",
    output: Any = None,
    output_kind: str | None = None,
    output_kind_ok: bool | None = None,
    output_kind_errors: list[str] | None = None,
    duration_ms: int | None = None,
    started_at: str | None = None,
    ended_at: str | None = None,
    output_ref: str | None = None,
    error: NodeError | None = None,
) -> dict[str, Any]:
    """One settled node invocation as a ``node_outcome`` kind instance.

    Pass ``output_ref`` (normally :data:`OUTPUT_REF_OUTPUT`) when the frame
    already carries the payload — ``output`` is then dropped from the wrapper
    and the marker names where it lives.

    Pass ``error`` for a FAILED invocation (plan §10d-B3): the packet keeps its
    shape and nests a ``node_error`` kind instance, so a failure is as
    renderable and as routable as any success.
    """
    return NodeOutcomeWrapper(
        run_id=run_id,
        node_id=node_id,
        workflow_id=workflow_id,
        step=step,
        attempt=attempt,
        status=status,
        output_kind=output_kind,
        output_kind_ok=output_kind_ok,
        output_kind_errors=output_kind_errors or None,
        duration_ms=duration_ms,
        started_at=started_at,
        ended_at=ended_at,
        output=None if output_ref else output,
        output_ref=output_ref,
        error=error,
    ).model_dump()


def run_result_view(
    *,
    run_id: str,
    workflow_id: str,
    status: str = "completed",
    output: Any = None,
    output_kind: str | None = None,
    outputs: list[dict[str, Any]] | None = None,
    duration_ms: int | None = None,
    started_at: str | None = None,
    ended_at: str | None = None,
    output_ref: str | None = None,
) -> dict[str, Any]:
    """A whole run as a ``run_result`` kind instance.

    ``outputs`` are already-built ``node_outcome`` views (one per terminal
    node), each nesting its own data kind — the typed half of the run's result.
    ``output`` is the raw terminal payload the engine recorded; on a frame that
    already carries it, pass ``output_ref`` instead so it is not repeated.
    """
    return RunResultWrapper(
        run_id=run_id,
        workflow_id=workflow_id,
        status=status,
        output_kind=output_kind,
        duration_ms=duration_ms,
        started_at=started_at,
        ended_at=ended_at,
        output=None if output_ref else output,
        output_ref=output_ref,
        outputs=[NodeOutcomeWrapper(**view) for view in (outputs or [])],
    ).model_dump()
