"""RunState names a run's close as Run already tracks it, and RunHandle is what Run, OfflineRun and
DisabledRun all answer (agent:10)."""

from __future__ import annotations

import pytest
from conftest import open_run

from probe.sdk.delivery.offline.offline import OfflineRun
from probe.sdk.run.disabled import DisabledRun
from probe.sdk.run.handle import RunHandle
from probe.sdk.run.run import Run
from probe.sdk.run.state import TRANSITIONS, RunState, get_run_state


def _moves(states: list[RunState]) -> list[RunState]:
    return [s for i, s in enumerate(states) if i == 0 or s != states[i - 1]]


def test_every_kind_of_run_is_a_run_handle() -> None:
    assert all(issubclass(kind, RunHandle) for kind in (Run, OfflineRun, DisabledRun))


def test_a_finish_walks_open_finishing_closing_closed(client, app, monkeypatch) -> None:
    run = open_run(client, experiment="states")
    seen = [get_run_state(run)]
    for name in ("_close", "set_status"):
        real = getattr(run, name)

        def watched(*args, _real=real, **kwargs):
            seen.append(get_run_state(run))
            return _real(*args, **kwargs)

        monkeypatch.setattr(run, name, watched)
    run.finish()
    seen.append(get_run_state(run))
    moves = _moves(seen)
    assert moves == [RunState.OPEN, RunState.FINISHING, RunState.CLOSING, RunState.CLOSED]
    assert all(after in TRANSITIONS[before] for before, after in zip(moves, moves[1:]))


def test_a_close_that_failed_reads_open_so_finish_can_retry(client, app, monkeypatch) -> None:
    run = open_run(client, experiment="refused")

    def refuse(*args, **kwargs):
        raise RuntimeError("the server is down")

    monkeypatch.setattr(run, "set_status", refuse)
    with pytest.raises(RuntimeError):
        run.finish(strict=True)
    assert vars(run)["_terminal_in_flight"] is not None  # the write was attempted ...
    assert get_run_state(run) is RunState.OPEN  # ... and failed: nothing closed or queued


def test_a_bare_terminal_status_closes_without_finishing(client, app) -> None:
    run = open_run(client, experiment="bare")
    run.set_status("completed", sync=True)
    assert get_run_state(run) is RunState.CLOSED


def test_nothing_leaves_closed_and_a_disabled_run_stays_open() -> None:
    assert TRANSITIONS[RunState.CLOSED] == frozenset()
    run = DisabledRun()
    run.finish()
    assert get_run_state(run) is RunState.OPEN
