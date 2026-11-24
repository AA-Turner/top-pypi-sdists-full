"""A stopped run times every phase of its wind-down (P1-CHAT, live 2026-11-16).

Live: request 24a11352 saw the Stop at 20:37:52.10 and sent its "request cancelled" frame at 52.39, then the
stream stayed silent until the completion frame at 55.99 — 3.6 s in which the take-back waited, with nothing
recorded to say where. Every phase from the Stop to the completion frame now lands on
``metadata.stop_wind_down`` (the completion frame carries it into the stream journal; the host adds ``settle_s``).
Break this guard: the stop branch stops passing its clock to ``_finalize_and_persist``, or the clock loses a phase.
"""

from __future__ import annotations

import time
from types import SimpleNamespace

from matrx_utils.source_guard import stable_source

from matrx_ai.orchestrator import executor


def test_the_clock_records_each_phase_since_the_last_and_rides_the_completed_metadata():
    wind = executor.StopWindDown()
    time.sleep(0.02)
    wind.mark("announce_s")
    wind.mark("persist_s")
    completed = SimpleNamespace(metadata={"status": "cancelled"})
    wind.attach(completed)
    phases = completed.metadata["stop_wind_down"]
    assert list(phases) == ["announce_s", "persist_s"]
    assert phases["announce_s"] >= 0.02 > phases["persist_s"]


def test_the_stop_branch_hands_its_clock_to_the_final_save_and_attaches_it():
    run_src = stable_source(executor._execute_until_complete_inner)
    stop = run_src.find("except ProviderCallStopped as _stopped:")
    assert stop != -1
    branch = run_src[stop : stop + 6000]
    for needle in ('_wind.mark("announce_s")', '_wind.mark("stop_cursor_s")', "wind_down=_wind", "_wind.attach("):
        assert needle in branch, f"the stopped branch lost {needle}"


def test_the_final_save_marks_its_heavy_phases_in_order():
    src = stable_source(executor._finalize_and_persist)
    order = [src.find(f'_wind_mark("{p}")') for p in ("build_s", "tool_sweep_s", "persist_s", "final_commit_s")]
    assert -1 not in order, "a phase of the final save is not timed"
    assert order == sorted(order)
