"""A lock collision the database broke reads "the database was busy", never "couldn't save the result".

Live 2026-10-28 14:35 UTC: 22 agent-run Vault READS were canceled by Postgres's lock timeout (55P03).
The step that ran the agent told the person it "finished its work but couldn't save the result" —
wrong twice: nothing had been saved, and nothing was lost. The statement rolled back in full, so the
honest sentence is that the database was busy and running again is safe.
"""

from __future__ import annotations

from matrx_graph.failure import Cause, failure_from_exception, failure_from_text
from matrx_graph.nodes.subgraph.call import SubgraphChildFailed

LockContentionError = type(
    "LockContentionError", (Exception,), {"__module__": "matrx_orm.exceptions"}
)
LIVE = (
    "Postgres canceled this statement to break a lock collision (55P03) inside a caller-managed "
    "transaction, so nothing was re-run: canceling statement due to lock timeout"
)


def test_the_exception_reads_busy() -> None:
    f = failure_from_exception(LockContentionError(LIVE), step_id="s", step_label="Synthesis")
    assert f.cause == Cause.DATABASE_BUSY
    assert "busy" in f.message
    assert "couldn't save" not in f.message


def test_the_flattened_text_reads_busy() -> None:
    f = failure_from_text(f"LockContentionError: {LIVE}", step_id="s", error_type="ExecutionError")
    assert f.cause == Cause.DATABASE_BUSY


def test_a_query_timeout_while_saving_is_still_a_save_failure() -> None:
    timeout = type("QueryTimeoutError", (Exception,), {"__module__": "matrx_orm.exceptions"})
    assert failure_from_exception(timeout("Query timed out")).cause == Cause.PERSISTENCE_FAILED


def test_a_child_that_hit_a_busy_database_hands_it_up_and_may_run_again() -> None:
    child = SubgraphChildFailed(
        "busy", child_run_id="r1", failure={"cause": Cause.DATABASE_BUSY, "message": "busy"}
    )
    assert child.code == Cause.DATABASE_BUSY
    assert child.details().get("caller_refusal") is not True
