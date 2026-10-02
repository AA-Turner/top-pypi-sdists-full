"""``AgentRunResult.bounded_work`` — THE ONE VERDICT for multi-pass runs.

Live 2026-08-26: a scheduled backfill ran five passes, classified 839 keywords,
hit a transient provider blip on the sixth, and reported ``success=False`` because
the verdict was derived from the LAST pass. The repeat guard read that status,
concluded the schedule had never worked, and disabled it. These cases pin the
rule that replaced that: work landed means the run is not failed, and the stop
is named in the summary and the metadata, never only in a log.
"""

from __future__ import annotations

from matrx_scheduler import RUN_STOPPED_EARLY_KEY, RUN_UNITS_DONE_KEY, AgentRunResult

BLIP = "MandateError: Google response cut off in transit"


def test_committed_work_then_a_blip_is_a_partial_success_that_names_its_stop() -> None:
    r = AgentRunResult.bounded_work(
        units_done=839, failures=[BLIP], summary="passes=6 classified=839", metadata={"x": 1}
    )
    assert r.success is True
    assert r.units_done == 839
    assert r.stopped_early and "839" in r.stopped_early and BLIP in r.stopped_early
    assert "STOPPED_EARLY" in (r.result_summary or "") and BLIP in r.result_summary
    assert r.error_message == BLIP  # the diagnosis is not thrown away
    assert r.metadata == {"x": 1}


def test_no_work_and_a_failure_is_a_failed_run() -> None:
    r = AgentRunResult.bounded_work(units_done=0, failures=[BLIP], summary="passes=1 classified=0")
    assert r.success is False
    assert r.stopped_early is None
    assert r.error_message == BLIP


def test_clean_run_has_no_stop_reason() -> None:
    r = AgentRunResult.bounded_work(units_done=200, failures=[], summary="ok")
    assert r.success is True and r.stopped_early is None and r.error_message is None


def test_many_failures_are_bounded_in_the_message() -> None:
    r = AgentRunResult.bounded_work(units_done=1, failures=[f"e{i}" for i in range(7)], summary="s")
    assert r.error_message == "e0; e1; e2 (+4 more)"


def test_reserved_keys_are_exported_for_the_ledger_contract() -> None:
    assert RUN_UNITS_DONE_KEY == "units_done" and RUN_STOPPED_EARLY_KEY == "stopped_early"
