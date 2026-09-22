"""The ONE place a decision turn reaches the stream.

WHY THIS FILE EXISTS. A decision model is a model in the agent system exactly
like an image, video or TTS model — and every one of those delivers its typed
result to the live surface as a ``data`` event (``MediaBlockData``), which is
what lets a runner and an agent-battle column show the result as it lands.
Decisions returned their ``decision_answers`` part on the ``UnifiedResponse``
and emitted NOTHING, so the part existed only on the persisted
``chat.message`` row: the live battle column read its content parts, found
none, and said "this run finished without writing an answer" while the run had
in fact succeeded (2026-09-21, feedback efc7c841). Reloading the conversation
rendered the same answers correctly — the defect was the missing event, never
the decision.

BOTH ROUTES, ONE EMISSION. The native holder (TypeSafe System One) and a text
model's verbalized answer produce the identical part and must produce the
identical event; a second emission site is how the two wires drift.

Best-effort by contract: a decision that ran and was paid for is never failed
by a stream that is not there (a background/system run has no emitter at all).
The part still rides the response and still persists.
"""

from __future__ import annotations

import logging

from matrx_ai.decisions.kinds import DecisionAnswers

logger = logging.getLogger(__name__)

__all__ = ["decision_answers_event", "emit_decision_answers"]


def decision_answers_event(answers: DecisionAnswers):
    """The typed wire event for one ``decision_answers`` part.

    Built by validating the kind's OWN ``to_part()`` dump against the wire
    twin, so the live event and the persisted part cannot say different things
    and a field added to the kind and not to the wire fails loudly here.
    """
    from matrx_connect.context.data_types import DecisionAnswersData

    part = answers.to_part()
    part["type"] = "decision_answers"
    return DecisionAnswersData.model_validate(part)


async def emit_decision_answers(answers: DecisionAnswers) -> None:
    """Send the decision's answers on the current stream, if there is one."""
    from matrx_ai.context import app_context as app_context_mod

    # ``try_get_app_context`` and not ``get_app_context``: a decision can run
    # with no stream at all (a worker, a schedule, a script), and that is not
    # an error — the part still rides the response and still persists.
    ctx = app_context_mod.try_get_app_context()
    emitter = getattr(ctx, "emitter", None) if ctx is not None else None
    if emitter is None:
        return
    try:
        await emitter.send_data(decision_answers_event(answers))
    except Exception:  # noqa: BLE001 — a paid, completed decision never fails on its stream
        logger.warning(
            "[decisions] could not stream the decision_answers part (model=%s, method=%s); "
            "the part still rides the response and persists.",
            answers.model,
            answers.method,
            exc_info=True,
        )
