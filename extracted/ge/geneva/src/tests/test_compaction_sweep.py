# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Resuming compaction that dead drivers left paused on other tables (GEN-1005)."""

from __future__ import annotations

import json
import random
import time
from datetime import timedelta
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import lance
import pyarrow as pa
import pytest

import geneva
from geneva.jobs import compaction_sweep as sweep
from geneva.jobs import jobs
from geneva.jobs.compaction_pause import (
    _ACTIVE_PAUSES,
    PAUSE_MARKER,
    TABLE_OVERRIDES_CONFIG_KEY,
    CompactionPauseConfig,
    HoldRenewal,
    _HoldKeeper,
    pause_compaction,
    pause_for_job,
    resume_after_job,
)
from geneva.jobs.compaction_sweep import (
    SWEEP_LEASE_KEY,
    SWEEP_PROGRESS_KEY,
    CompactionSweeper,
    SweepLease,
    SweepProgress,
    claim_sweep,
    sweep_paused_tables,
)
from geneva.jobs.heartbeat import DRIVER_RUNNING, DriverHeartbeat
from geneva.runners.ray import sparse_pipeline
from geneva.runners.ray.pipeline import _sibling_table, run_ray_add_column_remote
from geneva.runners.sparse_update import SparseUpdateResult
from geneva.utils import dt_now_utc

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from geneva.db import Connection

ENABLED = CompactionPauseConfig(enabled=True)
_START_SWEEPER = CompactionSweeper.start
_RESUMED = "Resumed compaction of table {}, which no running Geneva job held any more"


@pytest.fixture(autouse=True)
def _threads_run_by_hand(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests sweep and check holds themselves instead of waiting on threads."""
    monkeypatch.setattr(CompactionSweeper, "start", lambda self: None)
    monkeypatch.setattr(_HoldKeeper, "start", lambda self: None)


@pytest.fixture
def history(tmp_path: Path) -> Any:
    return geneva.connect(str(tmp_path / "db"))._history


@pytest.fixture
def tables(tmp_path: Path) -> Path:
    path = tmp_path / "tables"
    path.mkdir()
    return path


def _uri(tables: Path, name: str) -> str:
    return str(tables / f"{name}.lance")


def _create(tables: Path, name: str) -> str:
    uri = _uri(tables, name)
    lance.write_dataset(pa.table({"a": [1, 2, 3]}), uri)
    return uri


def _table_opener(tables: Path) -> Callable[[str], Any]:
    """Opens a table by name, as a driver opens tables in its namespace. A
    table that doesn't exist raises."""
    return lambda name: lance.dataset(_uri(tables, name))


def _overrides(uri: str) -> dict[str, Any] | None:
    raw = lance.dataset(uri).config().get(TABLE_OVERRIDES_CONFIG_KEY)
    return None if raw is None else json.loads(raw)


def _set_overrides(uri: str, overrides: dict[str, Any]) -> None:
    lance.dataset(uri).update_config(
        {TABLE_OVERRIDES_CONFIG_KEY: json.dumps(overrides)}
    )


def _paused(uri: str) -> bool:
    overrides = _overrides(uri) or {}
    return PAUSE_MARKER in overrides.get("job_types", {}).get("compaction", {})


def _beat(history: Any, job_id: str, *, silent_s: float = 0.0) -> None:
    """Leave the heartbeat a driver with the default 120 s lease would."""
    written = dt_now_utc() - timedelta(seconds=silent_s)
    history._heartbeats.write(
        DriverHeartbeat(
            job_id=job_id,
            state=DRIVER_RUNNING,
            started_at=written - timedelta(hours=1),
            written_at=written,
            interval_s=30.0,
            lease_s=120.0,
            seq=1,
        )
    )


def _running(history: Any, table: str, *, silent_s: float = 0.0) -> str:
    """A RUNNING job whose driver last heartbeat ``silent_s`` ago."""
    job_id = history.launch(table, "b").job_id
    history.set_running(job_id)
    _beat(history, job_id, silent_s=silent_s)
    return job_id


def _left_paused(tables: Path, history: Any, name: str) -> str:
    """A table whose only job paused its compaction and then died with its
    submitter: the row is still RUNNING, but the driver has been silent for
    31 min, past the 30 min hold window. Returns the dead job's id."""
    uri = _create(tables, name)
    job_id = _running(history, name, silent_s=31 * 60)
    pause_compaction(lambda: lance.dataset(uri))
    assert _paused(uri)
    return job_id


def _jobs_dataset(history: Any) -> Callable[[], Any]:
    return lambda: history.get_table(True).to_lance()


def _lease(history: Any) -> SweepLease | None:
    return SweepLease.parse(_jobs_dataset(history)().config().get(SWEEP_LEASE_KEY))


def _sweeper(
    history: Any,
    tables: Path,
    *,
    job_id: str = "me",
    table_name: str = "mine",
    open_table: Callable[[str], Any] | None = None,
    interval_s: float = 1800.0,
    namespace: list[str] | None = None,
) -> tuple[CompactionSweeper, list[str]]:
    events: list[str] = []
    sweeper = CompactionSweeper(
        job_id=job_id,
        table_name=table_name,
        open_table=open_table or _table_opener(tables),
        history=history,
        interval_s=interval_s,
        on_event=events.append,
        namespace=namespace,
    )
    return sweeper, events


def _recording(tables: Path, opened: list[str]) -> Callable[[str], Any]:
    open_table = _table_opener(tables)

    def record(name: str) -> Any:
        opened.append(name)
        return open_table(name)

    return record


# --- One sweep per interval, by one driver --------------------------------------


def test_a_claim_lasts_one_interval_and_is_then_claimable(history: Any) -> None:
    jobs = _jobs_dataset(history)
    start = dt_now_utc()

    lease = claim_sweep(jobs, holder="a", interval_s=1800, now=start)

    assert lease == SweepLease("a", start, start + timedelta(seconds=1800))
    assert _lease(history) == lease
    almost = start + timedelta(seconds=1799)
    assert claim_sweep(jobs, holder="b", interval_s=1800, now=almost) is None
    expired = start + timedelta(seconds=1800)
    next_lease = claim_sweep(jobs, holder="b", interval_s=1800, now=expired)
    assert next_lease is not None
    assert _lease(history) == next_lease


def test_of_two_drivers_claiming_at_once_only_one_wins(history: Any) -> None:
    jobs = _jobs_dataset(history)
    # Both read the lease, finding none, before either claims.
    read_by_a, read_by_b = jobs(), jobs()

    assert claim_sweep(lambda: read_by_a, holder="a", interval_s=1800) is not None
    # b's claim is a compare-and-swap against a version a's claim has changed.
    assert claim_sweep(lambda: read_by_b, holder="b", interval_s=1800) is None

    lease = _lease(history)
    assert lease is not None
    assert lease.holder == "a"


def test_claims_and_job_rows_do_not_get_in_each_others_way(history: Any) -> None:
    jobs = _jobs_dataset(history)
    read_before_rows = jobs()
    job_id = _running(history, "t")
    history.add_event(job_id, "progress")

    # Rows written after the claim's version was read don't conflict with it.
    assert claim_sweep(lambda: read_before_rows, holder="a", interval_s=60) is not None
    # And rows still write after it, leaving it in place.
    history.set_completed(job_id)
    history.launch("t", "b")

    statuses = [getattr(job.status, "value", job.status) for job in history.get(job_id)]
    assert statuses == ["DONE"]
    lease = _lease(history)
    assert lease is not None
    assert lease.holder == "a"


@pytest.mark.parametrize(
    "raw",
    [
        "not a lease",
        '{"holder": "x"}',
        # Far in the future, but without a time zone, so it can't be compared.
        '{"holder": "x", "claimed_at": "2999-01-01T00:00:00", '
        '"expires_at": "2999-01-01T00:30:00"}',
    ],
)
def test_a_lease_that_cannot_be_read_is_claimed_over(history: Any, raw: str) -> None:
    jobs = _jobs_dataset(history)
    jobs().update_config({SWEEP_LEASE_KEY: raw})

    assert claim_sweep(jobs, holder="a", interval_s=60) is not None
    lease = _lease(history)
    assert lease is not None
    assert lease.holder == "a"


def test_only_the_driver_that_wins_the_claim_sweeps(history: Any, tables: Path) -> None:
    dead = _uri(tables, "dead")
    _left_paused(tables, history, "dead")
    first, _ = _sweeper(history, tables, job_id="a")
    opened: list[str] = []
    second, _ = _sweeper(
        history, tables, job_id="b", open_table=_recording(tables, opened)
    )

    assert first.sweep_once() == ["dead"]
    assert second.sweep_once() is None

    assert opened == []  # the driver that lost the claim checked no table
    assert not _paused(dead)


# --- What a sweep resumes -------------------------------------------------------


def test_the_sweep_resumes_a_table_whose_driver_died(
    history: Any, tables: Path
) -> None:
    dead = _uri(tables, "dead")
    _left_paused(tables, history, "dead")
    sweeper, events = _sweeper(history, tables)

    assert sweeper.sweep_once() == ["dead"]

    assert _overrides(dead) is None  # as it was before the pause
    assert events == [_RESUMED.format("dead")]


def test_sweep_finds_late_tables_past_namespace_query_limit(
    rest_pushdown_db: Connection, tables: Path
) -> None:
    history = rest_pushdown_db._history
    _create(tables, "filler")
    for _ in range(12):
        history.launch("filler", "b")
    live = _uri(tables, "live")
    _beat(history, _left_paused(tables, history, "live"))
    dead = _uri(tables, "dead")
    _left_paused(tables, history, "dead")
    sweeper, events = _sweeper(history, tables)

    assert sweeper.sweep_once() == ["dead"]

    assert not _paused(dead)
    assert _paused(live)
    assert events == [_RESUMED.format("dead")]


@pytest.mark.parametrize("at_query_limit", [False, True])
def test_sweep_keeps_a_live_holder_after_ten_stale_jobs(
    rest_pushdown_db: Connection,
    tables: Path,
    monkeypatch: pytest.MonkeyPatch,
    at_query_limit: bool,
) -> None:
    history = rest_pushdown_db._history
    held = _uri(tables, "held")
    _left_paused(tables, history, "held")
    for _ in range(9):
        _running(history, "held", silent_s=31 * 60)
    _running(history, "held")
    if at_query_limit:
        monkeypatch.setattr(jobs, "UNBOUNDED_QUERY_LIMIT", 10)
    sweeper, events = _sweeper(history, tables)

    assert sweeper.sweep_once() == []

    assert _paused(held)
    assert events == []


def test_the_sweep_leaves_tables_that_running_jobs_hold(
    history: Any, tables: Path
) -> None:
    landing = _uri(tables, "landing")
    _beat(history, _left_paused(tables, history, "landing"))  # heartbeat is back
    renewed = _uri(tables, "renewed")
    renewer = _left_paused(tables, history, "renewed")
    # Its heartbeat is not landing, so it renews its hold in the tag instead.
    pause_compaction(
        lambda: lance.dataset(renewed), renewal=HoldRenewal(renewer, 1800.0)
    )
    sweeper, events = _sweeper(history, tables)

    assert sweeper.sweep_once() == []

    assert _paused(landing)
    assert _paused(renewed)
    assert events == []


def test_the_sweep_resumes_a_table_whose_job_rows_are_final(
    history: Any, tables: Path
) -> None:
    # E.g. an operator cancelled the dead job's row: no unfinished row is left
    # on the table, but its pause is.
    cancelled = _uri(tables, "cancelled")
    history.set_cancelled(_left_paused(tables, history, "cancelled"))
    sweeper, _ = _sweeper(history, tables)

    assert sweeper.sweep_once() == ["cancelled"]
    assert not _paused(cancelled)


def test_the_sweep_leaves_what_an_operator_chose(history: Any, tables: Path) -> None:
    # Turned off by hand, without Geneva's tag.
    off = _create(tables, "off")
    _running(history, "off", silent_s=31 * 60)
    _set_overrides(off, {"job_types": {"compaction": {"enabled": False}}})
    # Paused by Geneva, and asked to stay off once Geneva's jobs end.
    stay_off = _uri(tables, "stay_off")
    _left_paused(tables, history, "stay_off")
    overrides = _overrides(stay_off)
    assert overrides is not None
    overrides["job_types"]["compaction"][PAUSE_MARKER]["previous_enabled"] = False
    _set_overrides(stay_off, overrides)
    sweeper, _ = _sweeper(history, tables)

    assert sweeper.sweep_once() == ["stay_off"]

    assert _overrides(off) == {"job_types": {"compaction": {"enabled": False}}}
    assert _overrides(stay_off) == {"job_types": {"compaction": {"enabled": False}}}


def test_the_sweep_skips_the_drivers_own_table(history: Any, tables: Path) -> None:
    mine = _uri(tables, "mine")
    _left_paused(tables, history, "mine")
    opened: list[str] = []
    sweeper, _ = _sweeper(history, tables, open_table=_recording(tables, opened))

    assert sweeper.sweep_once() == []

    assert "mine" not in opened
    assert _paused(mine)


def test_a_table_that_cannot_be_checked_does_not_stop_the_sweep(
    history: Any, tables: Path
) -> None:
    history.launch("dropped", "b")  # rows remain for a table that is gone
    later = _uri(tables, "later")
    _left_paused(tables, history, "later")
    sweeper, _ = _sweeper(history, tables)

    assert sweeper.sweep_once() == ["later"]
    assert not _paused(later)


def test_a_stopped_sweeper_stops_between_tables(history: Any, tables: Path) -> None:
    first, second = _uri(tables, "first"), _uri(tables, "second")
    _left_paused(tables, history, "first")
    _left_paused(tables, history, "second")
    sweeper: CompactionSweeper | None = None
    open_table = _table_opener(tables)

    def stop_after_first(name: str) -> Any:
        assert sweeper is not None
        if name == "first":
            sweeper.stop()
        return open_table(name)

    sweeper, _ = _sweeper(history, tables, open_table=stop_after_first)

    # Stopping before resume starts leaves this table paused too.
    assert sweeper.sweep_once() == []
    assert _paused(first)
    assert _paused(second)


def test_a_sweep_that_fails_never_raises(
    history: Any, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken(*args: Any, **kwargs: Any) -> None:
        raise OSError("jobs table unreachable")

    monkeypatch.setattr(history, "get_table", broken)
    sweeper, events = _sweeper(history, tables)

    assert sweeper.sweep_once() is None
    assert events == []


def test_sweep_paused_tables_resumes_only_what_it_may(
    history: Any, tables: Path
) -> None:
    _left_paused(tables, history, "dead")
    _beat(history, _left_paused(tables, history, "live"))

    resumed = sweep_paused_tables(
        jobs_dataset=_jobs_dataset(history)(),
        history=history,
        open_table=_table_opener(tables),
    )

    assert resumed == ["dead"]


def _expire_claim(history: Any) -> None:
    lease = _lease(history)
    assert lease is not None
    expired = SweepLease(
        lease.holder, lease.claimed_at, dt_now_utc() - timedelta(seconds=1)
    )
    _jobs_dataset(history)().update_config({SWEEP_LEASE_KEY: expired.to_json()})


def test_table_budget_continues_across_drivers_without_starving_later_tables(
    history: Any, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sweep, "_MAX_TABLES", 2)
    history.launch("dropped", "b")
    for name in ["a", "b", "c", "d"]:
        _left_paused(tables, history, name)

    resumed = []
    for index in range(3):
        opened: list[str] = []
        driver, _ = _sweeper(
            history, tables, job_id=str(index), open_table=_recording(tables, opened)
        )
        resumed.extend(driver.sweep_once() or [])
        assert len(set(opened)) <= 2
        saved = json.loads(_jobs_dataset(history)().config()[SWEEP_PROGRESS_KEY + "[]"])
        assert set(saved) == {"version", "last_name"}
        _expire_claim(history)

    assert resumed == ["a", "b", "c", "d"]
    progress = SweepProgress.parse(
        _jobs_dataset(history)().config()[SWEEP_PROGRESS_KEY + "[]"]
    )
    assert progress == SweepProgress()


def test_row_budget_uses_a_stable_snapshot_and_later_picks_up_new_jobs(
    rest_pushdown_db: Connection, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    history = rest_pushdown_db._history
    monkeypatch.setattr(sweep, "_MAX_HISTORY_ROWS", 3)
    _create(tables, "filler")
    for _ in range(4):
        history.launch("filler", "b")
    _left_paused(tables, history, "late")
    first, _ = _sweeper(history, tables)
    assert first.sweep_once() == []
    progress = SweepProgress.parse(
        _jobs_dataset(history)().config()[SWEEP_PROGRESS_KEY + "[]"]
    )
    assert progress.last_name == "filler"

    # The cursor stays on the snapshot even after deleting its earlier rows.
    history.get_table(True).delete("table_name = 'filler'")
    _left_paused(tables, history, "earlier")
    _expire_claim(history)
    second, _ = _sweeper(history, tables, job_id="second")
    assert second.sweep_once() == ["late"]
    assert _paused(_uri(tables, "earlier"))

    _expire_claim(history)
    third, _ = _sweeper(history, tables, job_id="third")
    assert third.sweep_once() == ["earlier"]


@pytest.mark.parametrize("stop_during_discovery", [False, True])
def test_slow_discovery_makes_progress_unless_stopped(
    history: Any,
    tables: Path,
    monkeypatch: pytest.MonkeyPatch,
    stop_during_discovery: bool,
) -> None:
    _left_paused(tables, history, "dead")
    clock = [0.0]
    stopped = [False]
    monkeypatch.setattr(sweep, "time", SimpleNamespace(monotonic=lambda: clock[0]))
    scanner = lance.LanceDataset.scanner

    def slow_scanner(self: Any, **kwargs: Any) -> Any:
        clock[0] += 2 * sweep._SWEEP_BUDGET_S
        stopped[0] = stop_during_discovery
        return scanner(self, **kwargs)

    monkeypatch.setattr(lance.LanceDataset, "scanner", slow_scanner)
    resumed = sweep_paused_tables(
        jobs_dataset=_jobs_dataset(history)(),
        history=history,
        open_table=_table_opener(tables),
        stopped=lambda: stopped[0],
    )
    assert resumed == ([] if stop_during_discovery else ["dead"])
    assert _paused(_uri(tables, "dead")) == stop_during_discovery


def test_name_cursor_skips_empty_names_and_escapes_quotes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sweep, "_MAX_TABLES", 1)
    ds = lance.write_dataset(
        pa.table({"table_name": [None, "", "z", "owner's", "a", "owner's", "mine"]}),
        str(tmp_path / "names.lance"),
    )
    progress = SweepProgress()
    opened: list[str] = []

    def open_table(name: str) -> Any:
        opened.append(name)
        return SimpleNamespace(config=dict)

    for _ in range(3):
        assert (
            sweep_paused_tables(
                jobs_dataset=ds,
                history=None,
                open_table=open_table,
                skip_table="mine",
                progress=progress,
            )
            == []
        )
        progress = SweepProgress.parse(progress.to_json())
    assert opened == ["a", "owner's", "z"]
    assert progress == SweepProgress()


def test_time_budget_leaves_an_incomplete_check_paused_and_advances(
    history: Any, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ["first", "second"]:
        _left_paused(tables, history, name)
    clock = [0.0]
    monkeypatch.setattr(sweep, "time", SimpleNamespace(monotonic=lambda: clock[0]))
    open_table = _table_opener(tables)

    def slow(name: str) -> Any:
        clock[0] += sweep._SWEEP_BUDGET_S
        return open_table(name)

    first, _ = _sweeper(history, tables, open_table=slow)
    assert first.sweep_once() == []
    assert _paused(_uri(tables, "first"))
    assert _paused(_uri(tables, "second"))
    _expire_claim(history)
    second, _ = _sweeper(history, tables, job_id="second")
    assert second.sweep_once() == ["second"]
    _expire_claim(history)
    third, _ = _sweeper(history, tables, job_id="third")
    assert third.sweep_once() == ["first"]


def test_repeated_names_are_deduplicated_across_intervals(
    history: Any, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sweep, "_MAX_TABLES", 2)
    for name in ["a", "b", "c"]:
        _create(tables, name)
    for name in ["a", "a", "b", "a", "c", "c", "a", "c"]:
        history.launch(name, "b")
    _left_paused(tables, history, "late")
    resumed = []
    for index, expected in enumerate([["a", "b"], ["c", "late"]]):
        opened: list[str] = []
        driver, _ = _sweeper(
            history, tables, job_id=str(index), open_table=_recording(tables, opened)
        )
        resumed.extend(driver.sweep_once() or [])
        assert list(dict.fromkeys(opened)) == expected
        assert all(opened.count(name) == 1 for name in expected if name != "late")
        _expire_claim(history)
    assert resumed == ["late"]


@pytest.mark.parametrize("table_count", [200, 500, 2000])
def test_interleaved_history_checks_each_table_once_per_pass(
    tmp_path: Path, tables: Path, table_count: int
) -> None:
    names = [f"t{index:04d}" for index in range(table_count)]
    rng = random.Random(0)
    rows = names + [rng.choice(names) for _ in range(50_000 - table_count)]
    rng.shuffle(rows)
    uri = str(tmp_path / "interleaved.lance")
    lance.write_dataset(pa.table({"table_name": rows}), uri)
    history = SimpleNamespace(
        get_table=lambda _: SimpleNamespace(to_lance=lambda: lance.dataset(uri))
    )
    opened: list[str] = []

    def open_table(name: str) -> Any:
        opened.append(name)
        return SimpleNamespace(config=dict)

    intervals = (table_count + sweep._MAX_TABLES - 1) // sweep._MAX_TABLES
    for index in range(intervals):
        previous = len(opened)
        driver, _ = _sweeper(history, tables, job_id=str(index), open_table=open_table)
        assert driver.sweep_once() == []
        assert len(opened) - previous <= sweep._MAX_TABLES
        _expire_claim(history)

    assert sorted(opened) == names
    saved = lance.dataset(uri).config()[SWEEP_PROGRESS_KEY + "[]"]
    assert SweepProgress.parse(saved) == SweepProgress()


@pytest.mark.parametrize("checked", [None, ["a", "b"]])
def test_legacy_row_progress_restarts_the_name_cursor(checked: Any) -> None:
    saved = {"version": 4, "offset": 23}
    if checked is not None:
        saved["checked"] = checked
    assert SweepProgress.parse(json.dumps(saved)) == SweepProgress()


@pytest.mark.parametrize("removed_by_cleanup", [False, True])
def test_expired_snapshot_restarts_without_reusing_its_name_cursor(
    history: Any, tables: Path, removed_by_cleanup: bool
) -> None:
    history.launch("filler", "b")
    snapshot = _jobs_dataset(history)()
    history.get_table(True).delete("table_name = 'filler'")
    _left_paused(tables, history, "dead")
    current = _jobs_dataset(history)()
    if removed_by_cleanup:
        current.cleanup_old_versions(older_than=timedelta(0))
        version = snapshot.version
    else:
        version = 999999
    with pytest.raises(OSError, match="(?i)not found"):
        current.checkout_version(version)
    progress = SweepProgress(version=version, last_name="zzz")
    assert sweep_paused_tables(
        jobs_dataset=current,
        history=history,
        open_table=_table_opener(tables),
        progress=progress,
    ) == ["dead"]
    assert progress == SweepProgress()


@pytest.mark.parametrize(
    "raw",
    [
        None,
        "invalid",
        "[]",
        '{"version": 1, "last_name": 3}',
        '{"version": null, "last_name": "t"}',
        '{"version": true, "last_name": ""}',
    ],
)
def test_invalid_progress_restarts(raw: str | None) -> None:
    assert SweepProgress.parse(raw) == SweepProgress()


def test_an_old_sweeper_cannot_overwrite_a_new_claims_progress(
    history: Any, tables: Path
) -> None:
    _create(tables, "t")
    history.launch("t", "b")
    key = SWEEP_PROGRESS_KEY + "[]"
    newer = SweepProgress(version=1, last_name="t")

    def replace_claim(name: str) -> Any:
        lease = _lease(history)
        assert lease is not None
        assert (
            claim_sweep(
                _jobs_dataset(history),
                holder="new",
                interval_s=1800,
                now=lease.expires_at + timedelta(seconds=1),
            )
            is not None
        )
        _jobs_dataset(history)().update_config({key: newer.to_json()})
        return _table_opener(tables)(name)

    old, _ = _sweeper(history, tables, open_table=replace_claim)
    assert old.sweep_once() == []
    assert SweepProgress.parse(_jobs_dataset(history)().config()[key]) == newer


def test_namespaces_do_not_share_discovery_progress(
    history: Any, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sweep, "_MAX_TABLES", 1)
    for name in ["first", "second"]:
        _create(tables, name)
        history.launch(name, "b")
    for namespace, expected in [(["a"], "first"), (["b"], "first"), (["a"], "second")]:
        opened: list[str] = []
        driver, _ = _sweeper(
            history, tables, namespace=namespace, open_table=_recording(tables, opened)
        )
        assert driver.sweep_once() == []
        assert opened == [expected]
        _expire_claim(history)


def test_progress_save_racing_a_new_claim_conflicts_even_with_unchanged_lease(
    history: Any,
) -> None:
    jobs = _jobs_dataset(history)
    old = claim_sweep(jobs, holder="old", interval_s=60)
    assert old is not None
    before_new_claim = jobs()
    newer = claim_sweep(
        jobs, holder="new", interval_s=60, now=old.expires_at + timedelta(seconds=1)
    )
    assert newer is not None
    with pytest.raises(OSError, match="[Ii]ncompatible transaction"):
        before_new_claim.update_config(
            {
                SWEEP_LEASE_KEY: old.to_json(),
                SWEEP_PROGRESS_KEY + "[]": SweepProgress(
                    version=1, last_name="t"
                ).to_json(),
            }
        )
    assert _lease(history) == newer


# --- Running in a driver --------------------------------------------------------


def _pause_mine(
    history: Any,
    tables: Path,
    config: CompactionPauseConfig = ENABLED,
    *,
    sweep: bool = True,
) -> Any:
    uri = _create(tables, "mine")
    job_id = _running(history, "mine")
    pause = pause_for_job(
        table_name="mine",
        job_id=job_id,
        open_dataset=lambda: lance.dataset(uri),
        history=history,
        config=config,
        open_table=_table_opener(tables) if sweep else None,
    )
    assert pause is not None
    return pause


def test_a_driver_sweeps_while_its_job_runs(
    history: Any, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    started, stopped = [], []
    monkeypatch.setattr(CompactionSweeper, "start", lambda self: started.append(self))
    monkeypatch.setattr(CompactionSweeper, "stop", lambda self: stopped.append(self))

    pause = _pause_mine(history, tables)

    assert pause.sweeper is not None
    assert started == [pause.sweeper]
    resume_after_job(pause)
    assert stopped == [pause.sweeper]


def test_a_driver_whose_table_an_operator_turned_off_still_sweeps(
    history: Any, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    stopped: list[CompactionSweeper] = []
    monkeypatch.setattr(CompactionSweeper, "stop", lambda self: stopped.append(self))
    uri = _create(tables, "mine")
    _set_overrides(uri, {"job_types": {"compaction": {"enabled": False}}})
    pause = pause_for_job(
        table_name="mine",
        job_id=_running(history, "mine"),
        open_dataset=lambda: lance.dataset(uri),
        history=history,
        config=ENABLED,
        open_table=_table_opener(tables),
    )
    assert pause is not None
    assert pause.sweeper is not None

    resume_after_job(pause)

    assert stopped == [pause.sweeper]


def test_sweeping_can_be_turned_off(history: Any, tables: Path) -> None:
    config = CompactionPauseConfig(enabled=True, sweep_interval_s=0)

    assert _pause_mine(history, tables, config).sweeper is None


def test_a_driver_that_cannot_open_other_tables_does_not_sweep(
    history: Any, tables: Path
) -> None:
    assert _pause_mine(history, tables, sweep=False).sweeper is None


def test_the_sweep_interval_defaults_to_30_minutes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert CompactionPauseConfig().sweep_interval_s == 1800.0

    monkeypatch.setenv("GENEVA_COMPACTION_PAUSE__SWEEP_INTERVAL_S", "60")
    assert CompactionPauseConfig.get().sweep_interval_s == 60.0


def test_a_sweeper_thread_sweeps_until_stopped(
    history: Any, tables: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(CompactionSweeper, "start", _START_SWEEPER)
    monkeypatch.setattr(sweep, "_CHECK_EVERY_S", 0.05)
    dead = _uri(tables, "dead")
    _left_paused(tables, history, "dead")
    sweeper, events = _sweeper(history, tables, interval_s=0.2)

    sweeper.start()
    try:
        deadline = time.monotonic() + 10
        while _paused(dead):
            assert time.monotonic() < deadline, "the sweeper never resumed the table"
            time.sleep(0.02)
    finally:
        sweeper.stop()

    assert not sweeper._thread.is_alive()
    assert _RESUMED.format("dead") in events


def test_a_sibling_table_is_the_same_namespace_with_another_name(
    tmp_path: Path,
) -> None:
    db = geneva.connect(str(tmp_path / "db"))
    ref = db.create_table("mine", pa.table({"a": [1]})).get_reference()

    other = _sibling_table(ref, "other")

    assert other.table_id == [*ref.table_id[:-1], "other"]
    assert other.version is None
    assert other.table_uri is None
    assert other.namespace_config == ref.namespace_config
    assert other.storage_options == ref.storage_options


@geneva.udf
def _plus_one(a: int) -> int:
    return a + 1


def test_a_backfill_driver_resumes_a_table_a_dead_driver_left_paused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    db = geneva.connect(str(tmp_path / "db"))
    history = db._history
    tbl = db.create_table("t", pa.table({"a": pa.array([1, 2], type=pa.int64())}))
    tbl.add_columns({"b": _plus_one})
    other = db.create_table("other", pa.table({"a": [1]}))
    other_uri = other.to_lance().uri
    _running(history, "other", silent_s=31 * 60)
    pause_compaction(lambda: lance.dataset(other_uri))
    job_id = history.launch("t", "b").job_id
    monkeypatch.setattr(CompactionPauseConfig, "get", classmethod(lambda cls: ENABLED))
    swept: list[list[str] | None] = []

    def work(*args: object, **kwargs: object) -> SparseUpdateResult:
        # Mid-job, the driver's own sweeper opens the other table through the
        # job's namespace, finds no live holder, and resumes it.
        pause = _ACTIVE_PAUSES[job_id]
        assert pause.sweeper is not None
        swept.append(pause.sweeper.sweep_once())
        return SparseUpdateResult(
            base_version=1,
            committed_version=2,
            rows_total=2,
            rows_matched=1,
            rows_written=1,
            fragments_total=1,
            fragments_touched=1,
            fragment_equiv_rows=2,
        )

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", work)

    run_ray_add_column_remote._function(
        tbl.get_reference(),
        "b",
        job_id=job_id,
        update_mode="sparse_rows",
        where="a > 1",
    )

    assert swept == [["other"]]
    assert not _paused(other_uri)
    assert _RESUMED.format("other") in history.get(job_id)[0].events
