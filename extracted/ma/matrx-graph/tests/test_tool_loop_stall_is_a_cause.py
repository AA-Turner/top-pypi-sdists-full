"""A stalled tool loop is a CAUSE, and a fan-out note never costs the structure.

THE LIVE FAILURE this file replays: workflow run
``6fa6ad90-0b7e-4996-ba6e-543a78563394`` ("Newsroom Desk", definition
9c12787a-d62e-4141-80fb-f92a088ced16) errored 2026-09-12 22:16:51Z in node
``n_check`` ("Check it against the live Rulebook"). Its agent called the
``rulebook`` tool 11 times with ``rulebook_id="org-newsroom"`` — a slug where a
UUID belongs — all 11 failed, matrx-ai's loop guard disabled tools and paused
the turn for a person to review. There is no person inside a workflow step.

Two things were then wrong at THIS boundary:

1. ``paused_loop_guard`` matched no rung, so the cause persisted as
   ``engine_error`` and the person was told "Check it against the live Rulebook
   stopped partway through."
2. The step was a 2-invocation fan-out, so the honest partial note was appended
   by re-wrapping the ``NodeFailureError`` in a bare ``ExecutionError`` — which
   dropped ``node_error``, the node's OWN stable code. Every fan-out failure was
   therefore classified from its prose instead of its code.
"""

from __future__ import annotations

from matrx_graph.errors import NodeFailureError
from matrx_graph.executor.scheduler import append_failure_notes
from matrx_graph.failure import Cause, failure_from_exception, failure_from_text
from matrx_graph.types.result import NodeError

_LIVE_TECHNICAL = (
    "NodeFailureError: Node 'n_check' failed: ai_turn_failed: AI turn ended with "
    "status 'paused_loop_guard' (paused_loop_guard): no error detail recorded"
)

_FIXED_MESSAGE = (
    "AI turn ended with status 'paused_loop_guard' (tool_loop_stalled): the "
    "'rulebook' tool failed 11 of its 11 call(s), so tools were disabled and the "
    "turn stopped. Last error from 'rulebook': “Invalid arguments: 1 validation "
    "error for RulebookArgs”. This ran as an unattended step, so there is nobody "
    "to review the pause — it is a failure, not a wait. Fix that tool, or the "
    "value this step passes it, then retry the step."
)


def _node_failure(message: str) -> NodeFailureError:
    return NodeFailureError("n_check", NodeError(code="ai_turn_failed", message=message))


# ---------------------------------------------------------------------------
# The cause
# ---------------------------------------------------------------------------


def test_the_live_text_no_longer_lands_on_engine_error() -> None:
    failure = failure_from_text(
        _LIVE_TECHNICAL,
        step_id="n_check",
        step_label="Check it against the live Rulebook",
    )
    assert failure.cause == Cause.TOOL_LOOP_STALLED
    assert "stopped partway through" not in failure.message


def test_max_iterations_is_the_same_cause() -> None:
    assert (
        failure_from_text("ai_turn_failed: … status 'max_iterations_exceeded' …").cause
        == Cause.TOOL_LOOP_STALLED
    )


def test_the_error_type_alone_settles_it() -> None:
    """matrx-ai's machine word decides before any prose is read."""
    failure = failure_from_text(
        "something with no recognizable words in it",
        error_type="tool_loop_stalled",
    )
    assert failure.cause == Cause.TOOL_LOOP_STALLED


def test_the_stalled_tools_own_error_never_reclassifies_the_run() -> None:
    """The bounded tool error is arbitrary English — it must not outrank us.

    ``rulebook`` answers a missing book with "That Rulebook doesn't exist (or was
    deleted)"; the ``not found|does not exist`` rung would tell a person
    something had been deleted.
    """
    failure = failure_from_exception(
        _node_failure(
            "AI turn ended with status 'paused_loop_guard' (tool_loop_stalled): the "
            "'rulebook' tool failed 11 of its 11 call(s). Last error from 'rulebook': "
            "“That Rulebook does not exist (or was deleted).”"
        ),
        step_id="n_check",
    )
    assert failure.cause == Cause.TOOL_LOOP_STALLED


def test_the_sentence_says_what_stalled_and_what_to_change() -> None:
    generated = failure_from_text(
        _LIVE_TECHNICAL, step_label="Check it against the live Rulebook"
    ).message
    assert "kept retrying a tool that kept failing" in generated
    assert "needs fixing" in generated


# ---------------------------------------------------------------------------
# The fan-out wrap
# ---------------------------------------------------------------------------

_LIVE_NOTE = (
    "[1 of 2 invocations in this step completed and are preserved; "
    "retry re-runs only the failed one(s)]"
)


def test_nothing_to_add_leaves_the_exception_untouched() -> None:
    inner = _node_failure(_FIXED_MESSAGE)
    assert append_failure_notes(inner, []) is inner


def test_the_partial_note_survives_and_so_does_the_code() -> None:
    inner = _node_failure(_FIXED_MESSAGE)
    failure = failure_from_exception(
        append_failure_notes(inner, [_LIVE_NOTE]),
        step_id="n_check",
        step_label="Check it against the live Rulebook",
    )
    # The cause came from the node's own code + message, not the prose ladder.
    assert failure.cause == Cause.TOOL_LOOP_STALLED
    assert failure.error_type == "ai_turn_failed"
    # The fan-out truth is still recorded, verbatim.
    assert failure.technical is not None
    assert "1 of 2 invocations in this step completed and are preserved" in failure.technical
    # And the tool is named where a person reads it.
    assert "rulebook" in failure.message
