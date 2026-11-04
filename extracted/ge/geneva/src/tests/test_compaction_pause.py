# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Pausing the Enterprise agent's compaction while jobs run (GEN-994)."""

from __future__ import annotations

import io
import json
import logging
import threading
import time
from datetime import timedelta
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import boto3
import lance
import pyarrow as pa
import pytest
from botocore.stub import Stubber

import geneva
import geneva.runners.ray.pipeline as ray_pipeline
from geneva.jobs import compaction_pause as cp
from geneva.jobs.compaction_pause import (
    PAUSE_MARKER,
    PAUSE_NOTE,
    RENEWALS_KEY,
    TABLE_OVERRIDES_CONFIG_KEY,
    CompactionPause,
    CompactionPauseConfig,
    CompactionPauseLapsedError,
    HoldRenewal,
    PauseOutcome,
    jobs_holding_pause,
    pause_compaction,
    pause_for_job,
    resume_after_job,
    resume_compaction,
    resume_if_idle,
)
from geneva.jobs.heartbeat import (
    DRIVER_EXITED,
    DRIVER_RUNNING,
    DriverHeartbeat,
    DriverHeartbeatWriter,
)
from geneva.jobs.job_registry_reader import (
    FOOTER_KEY,
    U64_MAX,
    LocalRecordReader,
    RegistryTableRef,
    S3RecordReader,
    distribution_hash,
    in_flight_compactions,
)
from geneva.runners.ray import sparse_pipeline
from geneva.runners.ray.pipeline import run_ray_add_column_remote
from geneva.runners.sparse_update import SparseUpdateResult
from geneva.utils import dt_now_utc

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

ENABLED = CompactionPauseConfig(enabled=True)
_START_KEEPER = cp._HoldKeeper.start


@pytest.fixture(autouse=True)
def _keepers_run_by_hand(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tests call a keeper's checks themselves instead of waiting on its thread."""
    monkeypatch.setattr(cp._HoldKeeper, "start", lambda self: None)


@pytest.fixture
def table_uri(tmp_path: Path) -> str:
    uri = str(tmp_path / "t.lance")
    lance.write_dataset(pa.table({"a": [1, 2, 3]}), uri)
    return uri


def _opener(uri: str) -> Callable[[], Any]:
    return lambda: lance.dataset(uri)


def _overrides(uri: str) -> dict[str, Any] | None:
    raw = lance.dataset(uri).config().get(TABLE_OVERRIDES_CONFIG_KEY)
    return None if raw is None else json.loads(raw)


def _set_overrides(uri: str, overrides: dict[str, Any]) -> None:
    lance.dataset(uri).update_config(
        {TABLE_OVERRIDES_CONFIG_KEY: json.dumps(overrides)}
    )


# --- Turning compaction off and on ---------------------------------------------


def test_pause_turns_compaction_off_and_tags_it(table_uri: str) -> None:
    assert pause_compaction(_opener(table_uri)) is PauseOutcome.PAUSED

    compaction = _overrides(table_uri)["job_types"]["compaction"]  # type: ignore[index]
    assert compaction["enabled"] is False
    marker = compaction[PAUSE_MARKER]
    assert set(marker) == {"paused_at", "previous_enabled", "note"}
    assert marker["previous_enabled"] is None  # compaction was unset
    assert marker["note"] == PAUSE_NOTE  # tells a reader how to keep it off


def test_pause_and_resume_keep_every_other_setting(table_uri: str) -> None:
    operator_settings = {
        "auto_refresh_interval_seconds": 60.0,
        "job_types": {
            "compaction": {"target_rows_per_fragment": 200000},
            "reindex_vector": {"enabled": True, "table": {"num_workers": 3}},
            "cleanup": {"enabled": False},
            "future_family": {"x": 1},
        },
        "future_setting": [1, 2],
    }
    _set_overrides(table_uri, operator_settings)

    pause_compaction(_opener(table_uri))
    paused = _overrides(table_uri)
    assert paused is not None
    assert paused["job_types"]["compaction"]["target_rows_per_fragment"] == 200000
    assert paused["job_types"]["reindex_vector"] == {
        "enabled": True,
        "table": {"num_workers": 3},
    }
    assert paused["future_setting"] == [1, 2]

    assert resume_compaction(_opener(table_uri))
    assert _overrides(table_uri) == operator_settings


def test_compaction_an_operator_turned_off_is_left_alone(table_uri: str) -> None:
    _set_overrides(table_uri, {"job_types": {"compaction": {"enabled": False}}})
    version = lance.dataset(table_uri).version

    assert pause_compaction(_opener(table_uri)) is PauseOutcome.DISABLED_BY_POLICY
    assert not resume_compaction(_opener(table_uri))

    assert lance.dataset(table_uri).version == version
    assert _overrides(table_uri) == {"job_types": {"compaction": {"enabled": False}}}


def test_a_second_pause_finds_it_already_paused(table_uri: str) -> None:
    pause_compaction(_opener(table_uri))
    version = lance.dataset(table_uri).version

    assert pause_compaction(_opener(table_uri)) is PauseOutcome.ALREADY_PAUSED
    assert lance.dataset(table_uri).version == version


def test_resume_removes_the_key_when_nothing_else_is_set(table_uri: str) -> None:
    pause_compaction(_opener(table_uri))

    assert resume_compaction(_opener(table_uri))

    assert TABLE_OVERRIDES_CONFIG_KEY not in lance.dataset(table_uri).config()


def test_resume_restores_an_explicitly_enabled_compaction(table_uri: str) -> None:
    _set_overrides(table_uri, {"job_types": {"compaction": {"enabled": True}}})

    pause_compaction(_opener(table_uri))
    marker = _overrides(table_uri)["job_types"]["compaction"][PAUSE_MARKER]  # type: ignore[index]
    assert marker["previous_enabled"] is True
    resume_compaction(_opener(table_uri))

    assert _overrides(table_uri) == {"job_types": {"compaction": {"enabled": True}}}


def test_resume_keeps_what_an_operator_set_while_paused(table_uri: str) -> None:
    pause_compaction(_opener(table_uri))
    overrides = _overrides(table_uri)
    assert overrides is not None
    overrides["job_types"]["compaction"]["enabled"] = True
    _set_overrides(table_uri, overrides)

    resume_compaction(_opener(table_uri))

    assert _overrides(table_uri) == {"job_types": {"compaction": {"enabled": True}}}


def test_resume_without_a_geneva_pause_writes_nothing(table_uri: str) -> None:
    version = lance.dataset(table_uri).version
    assert not resume_compaction(_opener(table_uri))
    assert lance.dataset(table_uri).version == version


def test_an_update_retries_over_a_concurrent_change(table_uri: str) -> None:
    opened: list[int] = []

    def open_dataset() -> Any:
        ds = lance.dataset(table_uri)
        opened.append(ds.version)
        if len(opened) == 1:
            # Someone else changes the overrides after this handle was opened.
            _set_overrides(table_uri, {"job_types": {"cleanup": {"enabled": False}}})
        return ds

    assert pause_compaction(open_dataset) is PauseOutcome.PAUSED

    assert len(opened) == 2
    overrides = _overrides(table_uri)
    assert overrides is not None
    assert overrides["job_types"]["cleanup"] == {"enabled": False}
    assert overrides["job_types"]["compaction"]["enabled"] is False


def test_unreadable_overrides_are_left_alone(
    table_uri: str, history: Any, caplog: pytest.LogCaptureFixture
) -> None:
    lance.dataset(table_uri).update_config({TABLE_OVERRIDES_CONFIG_KEY: "not json"})

    events: list[str] = []
    with caplog.at_level(logging.WARNING, logger=cp.__name__):
        pause = pause_for_job(
            table_name="t",
            job_id="j",
            open_dataset=_opener(table_uri),
            history=history,
            config=ENABLED,
            on_event=events.append,
        )

    assert pause is not None
    assert pause.outcome is PauseOutcome.FAILED
    assert pause.keeper is None
    assert "Failed to pause automatic compaction of table t" in caplog.text
    (event,) = events
    assert event.startswith("Compaction not paused: JSONDecodeError")
    assert lance.dataset(table_uri).config()[TABLE_OVERRIDES_CONFIG_KEY] == "not json"

    resume_after_job(pause)  # still tried, in case another job's pause is left

    assert lance.dataset(table_uri).config()[TABLE_OVERRIDES_CONFIG_KEY] == "not json"
    assert events[1].startswith("Compaction left paused: JSONDecodeError")


def test_pausing_is_off_by_default(table_uri: str) -> None:
    pause = pause_for_job(
        table_name="t",
        job_id="j",
        open_dataset=_opener(table_uri),
        history=None,
        config=CompactionPauseConfig(),
    )

    assert pause is None
    assert TABLE_OVERRIDES_CONFIG_KEY not in lance.dataset(table_uri).config()


def test_config_reads_env(monkeypatch: pytest.MonkeyPatch) -> None:
    from geneva.config import _CONFIG_LOADER

    monkeypatch.setenv("GENEVA_COMPACTION_PAUSE__ENABLED", "true")
    monkeypatch.setenv("GENEVA_COMPACTION_PAUSE__STALE_LEASES", "30")
    monkeypatch.setenv("GENEVA_COMPACTION_PAUSE__JOB_REGISTRY_ROOT_URI", "s3://b/sys")
    monkeypatch.setenv("GENEVA_COMPACTION_PAUSE__JOB_REGISTRY_DATABASE", "db")
    config = CompactionPauseConfig.from_loader(_CONFIG_LOADER)

    assert config.enabled
    assert config.stale_leases == 30.0
    assert CompactionPauseConfig().stale_leases == 15.0
    assert (config.job_registry_root_uri, config.job_registry_database) == (
        "s3://b/sys",
        "db",
    )


# --- Which jobs hold the pause, and resuming -----------------------------------


@pytest.fixture
def history(tmp_path: Path) -> Any:
    return geneva.connect(str(tmp_path / "db"))._history


def _beat(
    history: Any, job_id: str, *, silent_s: float = 0.0, state: str = DRIVER_RUNNING
) -> None:
    """Leave the heartbeat a driver with the default 120 s lease would."""
    written = dt_now_utc() - timedelta(seconds=silent_s)
    history._heartbeats.write(
        DriverHeartbeat(
            job_id=job_id,
            state=state,
            started_at=written - timedelta(hours=1),
            written_at=written,
            interval_s=30.0,
            lease_s=120.0,
            seq=1,
        )
    )


def _running(history: Any, table: str = "t", *, beat: bool = True) -> str:
    """A RUNNING job; ``beat`` gives it a live driver heartbeat."""
    job_id = history.launch(table, "b").job_id
    history.set_running(job_id)
    if beat:
        _beat(history, job_id)
    return job_id


def _go_quiet(history: Any, job_id: str) -> None:
    """Age a row as a driver that writes nothing for an hour would leave it."""
    history.get_table().update(
        where=f"job_id = '{job_id}'",
        values={"updated_at": dt_now_utc() - timedelta(hours=1)},
    )


class _Heartbeat:
    """A driver's heartbeat writer, last landed ``since`` seconds ago (None: never)."""

    interval_s = 30.0
    lease_s = 120.0

    def __init__(self, since: float | None = 0.0) -> None:
        self.since = since

    def wait_written(self, timeout: float) -> bool:
        return self.since is not None

    def seconds_since_written(self) -> float | None:
        return self.since

    def add_listener(self, listener: Callable[[float], None]) -> None:
        pass


def _pause(
    uri: str,
    history: Any,
    job_id: str,
    heartbeat: _Heartbeat | None = None,
    on_event: Callable[[str], None] | None = None,
) -> CompactionPause:
    """Pause as the job's driver does, by default one whose heartbeat lands."""
    pause = pause_for_job(
        table_name="t",
        job_id=job_id,
        open_dataset=_opener(uri),
        history=history,
        heartbeat=heartbeat or _Heartbeat(),  # type: ignore[arg-type]
        config=ENABLED,
        on_event=on_event,
    )
    assert pause is not None
    return pause


def _paused(uri: str) -> bool:
    overrides = _overrides(uri) or {}
    return PAUSE_MARKER in overrides.get("job_types", {}).get("compaction", {})


def _renewals(uri: str) -> dict[str, Any]:
    marker = (_overrides(uri) or {})["job_types"]["compaction"][PAUSE_MARKER]
    return marker.get(RENEWALS_KEY, {})


def test_unfinished_jobs_with_a_live_driver_hold_the_pause(history: Any) -> None:
    me = _running(history)
    running = _running(history)
    quiet = _running(history)
    _go_quiet(history, quiet)  # the row ages; the heartbeat doesn't
    pending = history.launch("t", "b").job_id
    legacy = _running(history, beat=False)  # a driver from before heartbeats
    done = _running(history)
    history.set_completed(done)
    _running(history, table="other")

    holding = jobs_holding_pause(history, "t", exclude_job_id=me)

    assert sorted(holding) == sorted([running, quiet])
    assert pending not in holding
    assert legacy not in holding


def test_the_last_job_on_the_table_resumes_compaction(
    table_uri: str, history: Any
) -> None:
    first, second = _running(history), _running(history)
    first_pause = _pause(table_uri, history, first)
    second_pause = _pause(table_uri, history, second)
    assert second_pause.outcome is PauseOutcome.ALREADY_PAUSED

    history.set_completed(first)
    resume_after_job(first_pause)
    assert _paused(table_uri)

    history.set_completed(second)
    resume_after_job(second_pause)
    assert _overrides(table_uri) is None


def test_a_job_whose_pause_failed_still_resumes_compaction_when_it_ends(
    table_uri: str, history: Any
) -> None:
    first, second = _running(history), _running(history)
    first_pause = _pause(table_uri, history, first)
    down = True

    def open_dataset() -> Any:
        if down:
            raise RuntimeError("storage unavailable")
        return lance.dataset(table_uri)

    events: list[str] = []
    second_pause = pause_for_job(
        table_name="t",
        job_id=second,
        open_dataset=open_dataset,
        history=history,
        heartbeat=_Heartbeat(),  # type: ignore[arg-type]
        config=ENABLED,
        on_event=events.append,
    )
    assert second_pause is not None
    assert second_pause.outcome is PauseOutcome.FAILED
    assert second_pause.keeper is None
    assert events == ["Compaction not paused: RuntimeError: storage unavailable"]

    history.set_completed(first)
    resume_after_job(first_pause)
    assert _paused(table_uri), "resumed under the job whose pause failed"

    down = False
    history.set_completed(second)
    resume_after_job(second_pause)
    assert _overrides(table_uri) is None


def test_a_job_that_found_compaction_off_resumes_a_later_jobs_pause(
    table_uri: str, history: Any
) -> None:
    _set_overrides(table_uri, {"job_types": {"compaction": {"enabled": False}}})
    first = _running(history)
    first_pause = _pause(table_uri, history, first)
    assert first_pause.outcome is PauseOutcome.DISABLED_BY_POLICY
    # An operator resets the overrides while the first job runs, and a second
    # job then pauses compaction for itself.
    lance.dataset(table_uri).update_config({TABLE_OVERRIDES_CONFIG_KEY: None})
    second = _running(history)
    second_pause = _pause(table_uri, history, second)
    assert second_pause.outcome is PauseOutcome.PAUSED

    history.set_completed(second)
    resume_after_job(second_pause)
    assert _paused(table_uri), "resumed under the first job"

    history.set_completed(first)
    resume_after_job(first_pause)
    assert _overrides(table_uri) is None


def test_a_job_starting_during_resume_gets_compaction_paused_again(
    table_uri: str, history: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    pause = _pause(table_uri, history, _running(history))
    answers = iter([[], ["late-job"]])
    monkeypatch.setattr(cp, "jobs_holding_pause", lambda *a, **k: next(answers))

    resume_after_job(pause)

    assert _overrides(table_uri)["job_types"]["compaction"]["enabled"] is False  # type: ignore[index]


def test_a_driver_that_exited_or_went_silent_too_long_stops_holding(
    history: Any,
) -> None:
    alive = _running(history)
    exited = _running(history)
    _beat(history, exited, state=DRIVER_EXITED)
    briefly_silent = _running(history)
    _beat(history, briefly_silent, silent_s=20 * 60)  # 10 leases
    long_silent = _running(history)
    _beat(history, long_silent, silent_s=31 * 60)  # past 15 leases

    holding = jobs_holding_pause(history, "t")

    assert sorted(holding) == sorted([alive, briefly_silent])


def test_releasing_silent_drivers_can_be_turned_off(history: Any) -> None:
    silent = _running(history)
    _beat(history, silent, silent_s=10 * 3600)
    exited = _running(history)
    _beat(history, exited, state=DRIVER_EXITED)

    assert jobs_holding_pause(history, "t", stale_leases=0) == [silent]


def test_a_killed_driver_stops_holding_the_pause(table_uri: str, history: Any) -> None:
    killed, last = _running(history), _running(history)
    _pause(table_uri, history, killed)
    last_pause = _pause(table_uri, history, last)
    _beat(history, killed, silent_s=3600)

    history.set_completed(last)
    resume_after_job(last_pause)

    assert _overrides(table_uri) is None


def test_rows_without_a_heartbeat_do_not_hold_the_pause(
    table_uri: str, history: Any
) -> None:
    _running(history, beat=False)  # orphaned by a driver from before heartbeats
    history.launch("t", "b")  # pending: its driver pauses for itself once started
    last = _running(history)
    last_pause = _pause(table_uri, history, last)

    history.set_completed(last)
    resume_after_job(last_pause)

    assert _overrides(table_uri) is None


def test_a_live_driver_silent_past_the_window_holds_through_its_renewal(
    table_uri: str, history: Any
) -> None:
    quiet, last = _running(history), _running(history)
    quiet_pause = _pause(table_uri, history, quiet, heartbeat=_Heartbeat(since=None))
    last_pause = _pause(table_uri, history, last)
    # The quiet driver can't write its heartbeat but can still write its table.
    _beat(history, quiet, silent_s=31 * 60)
    assert quiet_pause.keeper is not None
    quiet_pause.keeper.renew()

    history.set_completed(last)
    resume_after_job(last_pause)
    assert _paused(table_uri), "resumed compaction under a live driver"

    # Once its renewals lapse too, the driver is taken for dead.
    overrides = _overrides(table_uri)
    assert overrides is not None
    lapsed = (dt_now_utc() - timedelta(minutes=31)).isoformat()
    overrides["job_types"]["compaction"][PAUSE_MARKER][RENEWALS_KEY][quiet]["at"] = (
        lapsed
    )
    _set_overrides(table_uri, overrides)
    assert resume_if_idle(
        table_name="t", open_dataset=_opener(table_uri), history=history
    )
    assert _overrides(table_uri) is None


def test_a_renewal_landing_during_resume_keeps_the_pause(
    table_uri: str, history: Any
) -> None:
    quiet = _running(history, beat=False)
    last = _running(history)
    last_pause = _pause(table_uri, history, last)
    opened: list[int] = []

    def open_dataset() -> Any:
        ds = lance.dataset(table_uri)
        opened.append(ds.version)
        if len(opened) == 1:
            # The quiet driver renews after the resume read the overrides.
            pause_compaction(_opener(table_uri), renewal=HoldRenewal(quiet, 1800.0))
        return ds

    last_pause.open_dataset = open_dataset
    history.set_completed(last)
    resume_after_job(last_pause)

    assert len(opened) == 2, "the resume did not re-read the overrides"
    assert _paused(table_uri)
    assert list(_renewals(table_uri)) == [quiet]


def test_a_finished_jobs_renewal_no_longer_holds(table_uri: str, history: Any) -> None:
    renewed, last = _running(history), _running(history)
    renewed_pause = _pause(
        table_uri, history, renewed, heartbeat=_Heartbeat(since=None)
    )
    last_pause = _pause(table_uri, history, last)

    history.set_completed(renewed)
    resume_after_job(renewed_pause)  # the last job still holds
    assert list(_renewals(table_uri)) == [renewed]

    history.set_completed(last)
    resume_after_job(last_pause)
    assert _overrides(table_uri) is None


def test_a_renewal_is_not_written_once_the_job_has_ended(table_uri: str) -> None:
    keeper = _keeper(table_uri, _Heartbeat(since=None))
    keeper.stop()
    version = lance.dataset(table_uri).version

    keeper.renew()

    assert lance.dataset(table_uri).version == version


def test_a_driver_renews_when_pausing_until_its_heartbeat_lands(
    table_uri: str, history: Any
) -> None:
    landed = _pause(table_uri, history, _running(history))
    assert (
        RENEWALS_KEY
        not in _overrides(table_uri)["job_types"]["compaction"][PAUSE_MARKER]
    )  # type: ignore[index]

    not_landed = _running(history, beat=False)
    _pause(table_uri, history, not_landed, heartbeat=_Heartbeat(since=None))
    assert list(_renewals(table_uri)) == [not_landed]
    assert _renewals(table_uri)[not_landed]["valid_s"] == 15 * 120.0
    assert landed.outcome is PauseOutcome.PAUSED


def _keeper(
    uri: str,
    heartbeat: _Heartbeat | None,
    *,
    stale_leases: float = 15.0,
    events: list[str] | None = None,
) -> Any:
    return cp._HoldKeeper(
        job_id="j",
        table_name="t",
        open_dataset=_opener(uri),
        heartbeat=heartbeat,  # type: ignore[arg-type]
        stale_leases=stale_leases,
        renewed=False,
        on_event=None if events is None else events.append,
    )


def test_a_driver_renews_only_while_its_heartbeat_is_not_landing(
    table_uri: str,
) -> None:
    heartbeat = _Heartbeat(since=10.0)
    keeper = _keeper(table_uri, heartbeat)
    assert not keeper.renew_due()

    heartbeat.since = 601.0  # a third of the 30 min window
    assert keeper.renew_due()
    keeper.renew()
    assert not keeper.renew_due(), "renewed again before a third of the window"
    assert list(_renewals(table_uri)) == ["j"]

    assert _keeper(table_uri, None).renew_due(), "no heartbeats at all"
    assert not _keeper(table_uri, _Heartbeat(since=3600.0), stale_leases=0).renew_due()
    assert _keeper(table_uri, _Heartbeat(since=None), stale_leases=0).renew_due()


def test_a_job_pauses_again_if_its_pause_was_wiped(table_uri: str) -> None:
    events: list[str] = []
    keeper = _keeper(table_uri, _Heartbeat(since=None), events=events)

    keeper.renew()  # the overrides are empty, as after a reset

    assert _paused(table_uri)
    assert list(_renewals(table_uri)) == ["j"]
    assert events == [
        "Compaction pause was removed while this job runs, e.g. by an overrides "
        "reset; paused it again"
    ]


def _compaction(uri: str) -> dict[str, Any]:
    return (_overrides(uri) or {}).get("job_types", {}).get("compaction", {})


def test_an_overrides_reset_while_a_job_runs_is_undone(
    table_uri: str, history: Any
) -> None:
    events: list[str] = []
    pause = _pause(table_uri, history, _running(history), on_event=events.append)
    lance.dataset(table_uri).update_config({TABLE_OVERRIDES_CONFIG_KEY: None})
    assert pause.keeper is not None

    pause.keeper.check_pause(renew=False)  # its 5-minute check

    assert _compaction(table_uri)["enabled"] is False
    assert _compaction(table_uri)[PAUSE_MARKER]["previous_enabled"] is None
    assert events == [
        "Compaction pause was removed while this job runs, e.g. by an overrides "
        "reset; paused it again"
    ]
    history.set_completed(pause.job_id)
    resume_after_job(pause)
    assert _overrides(table_uri) is None


def test_compaction_turned_on_by_hand_while_a_job_runs_is_left_on(
    table_uri: str, history: Any
) -> None:
    events: list[str] = []
    pause = _pause(table_uri, history, _running(history), on_event=events.append)
    assert pause.keeper is not None
    _set_overrides(table_uri, {"job_types": {"compaction": {"enabled": True}}})
    version = lance.dataset(table_uri).version

    pause.keeper.check_pause(renew=False)
    pause.keeper.renew()  # even while its heartbeat isn't landing

    assert lance.dataset(table_uri).version == version
    assert events == [
        "Compaction was turned on by hand while this job runs; leaving it on"
    ]
    resume_after_job(pause)
    assert _compaction(table_uri) == {"enabled": True}


def test_a_renewal_beside_an_operators_enabled_true_is_not_repeated(
    table_uri: str,
) -> None:
    events: list[str] = []
    keeper = _keeper(table_uri, _Heartbeat(since=None), events=events)
    pause_compaction(_opener(table_uri), renewal=keeper.renewal)
    overrides = _overrides(table_uri)
    assert overrides is not None
    # `overrides get`, `enabled` edited in place, `overrides set`: the tag stays.
    overrides["job_types"]["compaction"]["enabled"] = True
    _set_overrides(table_uri, overrides)
    # A third of the window on, with nothing having shown the hold since.
    keeper._last_renewed = None
    keeper._last_shown = time.monotonic() - 1000.0
    version = lance.dataset(table_uri).version

    keeper.renew()

    assert lance.dataset(table_uri).version == version + 1
    assert _compaction(table_uri)["enabled"] is True
    assert list(_renewals(table_uri)) == ["j"]
    assert not keeper.renew_due(), "would commit a renewal on every poll"
    assert keeper.silent_s() < 60
    assert events == [
        "Compaction was turned on by hand while this job runs; leaving it on"
    ]


def test_an_operator_can_keep_compaction_off_through_previous_enabled(
    table_uri: str, history: Any
) -> None:
    job = _running(history)
    pause = _pause(table_uri, history, job)
    overrides = _overrides(table_uri)
    assert overrides is not None
    # What the note in the tag says to do, e.g. via `overrides get` / `set`.
    overrides["job_types"]["compaction"][PAUSE_MARKER]["previous_enabled"] = False
    _set_overrides(table_uri, overrides)

    history.set_completed(job)
    resume_after_job(pause)

    assert _overrides(table_uri) == {"job_types": {"compaction": {"enabled": False}}}
    # Now untagged, it's the operator's: no later job undoes it.
    later = _pause(table_uri, history, _running(history))
    assert later.outcome is PauseOutcome.DISABLED_BY_POLICY
    resume_after_job(later)
    assert _overrides(table_uri) == {"job_types": {"compaction": {"enabled": False}}}


def test_compaction_turned_off_by_hand_while_paused_stays_off(
    table_uri: str, history: Any
) -> None:
    events: list[str] = []
    job = _running(history)
    pause = _pause(table_uri, history, job, on_event=events.append)
    assert pause.keeper is not None
    # `overrides set` replaces the whole object, so the tag goes with it.
    _set_overrides(table_uri, {"job_types": {"compaction": {"enabled": False}}})
    version = lance.dataset(table_uri).version

    pause.keeper.check_pause(renew=False)
    pause.keeper.renew()
    history.set_completed(job)
    resume_after_job(pause)

    assert lance.dataset(table_uri).version == version
    assert _overrides(table_uri) == {"job_types": {"compaction": {"enabled": False}}}
    assert events == []


def test_an_operators_compaction_off_counts_as_the_jobs_hold(table_uri: str) -> None:
    keeper = _keeper(table_uri, _Heartbeat(since=1000.0))
    _set_overrides(table_uri, {"job_types": {"compaction": {"enabled": False}}})

    keeper.renew()

    # No resume can undo an operator's setting, so the job may keep committing.
    assert keeper.silent_s() < 60
    keeper.check_held()


def test_a_keeper_thread_checks_its_pause_until_stopped(table_uri: str) -> None:
    keeper = cp._HoldKeeper(
        job_id="j",
        table_name="t",
        open_dataset=_opener(table_uri),
        heartbeat=_Heartbeat(since=0.0),  # type: ignore[arg-type]
        stale_leases=15,
        renewed=False,
        on_event=None,
        poll_s=0.01,
    )
    keeper._check_every_s = 0.0  # check on every poll
    _START_KEEPER(keeper)
    try:
        _wait_until(lambda: _paused(table_uri))  # the empty overrides got paused
    finally:
        keeper.stop()
    assert not keeper._thread.is_alive()


def test_a_job_checks_its_pause_every_five_minutes(table_uri: str) -> None:
    keeper = _keeper(table_uri, _Heartbeat(since=0.0))
    assert not keeper.check_due()

    keeper._last_checked -= 300.0

    assert keeper.check_due()
    keeper.check_pause(renew=False)
    assert not keeper.check_due()


def test_a_driver_stops_committing_once_its_hold_may_have_lapsed(
    table_uri: str,
) -> None:
    # Two thirds of the 30 min window is 1200 s.
    _keeper(table_uri, _Heartbeat(since=1190.0)).check_held()
    events: list[str] = []
    keeper = _keeper(table_uri, _Heartbeat(since=1200.0), events=events)
    with pytest.raises(CompactionPauseLapsedError, match="for 20 min"):
        keeper.check_held()

    keeper.heartbeat_landed(time.monotonic())  # a compaction may have started
    with pytest.raises(CompactionPauseLapsedError):
        keeper.check_held()
    assert events == [
        "Compaction pause may have lapsed: no heartbeat or renewal for 20 min; "
        "stopping before the next commit"
    ]


def test_a_renewal_keeps_a_silent_driver_committing(table_uri: str) -> None:
    keeper = _keeper(table_uri, _Heartbeat(since=1000.0))
    keeper.renew()

    assert keeper.silent_s() < 60
    keeper.check_held()


def test_recovery_preserves_an_unobserved_lapse(table_uri: str) -> None:
    # The gate's reproducer: a driver resumes after missing its keeper polls for
    # 31 minutes, and one real keeper iteration runs once the table is reachable.
    heartbeat = SimpleNamespace(lease_s=120.0, seconds_since_written=lambda: 31 * 60.0)
    keeper = cp._HoldKeeper(
        job_id="j",
        table_name="t",
        open_dataset=_opener(table_uri),
        heartbeat=heartbeat,  # type: ignore[arg-type]
        stale_leases=15,
        renewed=False,
        on_event=None,
    )
    polls = iter([False, True])
    keeper._stop = SimpleNamespace(  # type: ignore[assignment]
        wait=lambda seconds: next(polls), is_set=lambda: False
    )
    keeper._run()

    with pytest.raises(CompactionPauseLapsedError):
        keeper.check_held()


def test_a_renewal_that_closes_a_long_gap_still_stops_commits(table_uri: str) -> None:
    keeper = _keeper(table_uri, None)
    keeper.shown(time.monotonic() - 1300.0)  # last shown 21+ min ago

    keeper.renew()

    assert keeper.silent_s() < 60
    with pytest.raises(CompactionPauseLapsedError, match="for 2[12] min"):
        keeper.check_held()


class _SwitchableStore:
    """A heartbeat store that fails while ``down`` is set."""

    def __init__(self) -> None:
        self.down = threading.Event()

    def write(self, heartbeat: DriverHeartbeat) -> None:
        if self.down.is_set():
            raise OSError("storage unavailable")


def _wait_until(predicate: Callable[[], bool], timeout: float = 10.0) -> None:
    deadline = time.monotonic() + timeout
    while not predicate():
        assert time.monotonic() < deadline, "timed out"
        time.sleep(0.01)


@pytest.mark.parametrize("outage_s", [0.0, 2.5])
def test_a_heartbeat_recovering_after_a_long_outage_still_stops_commits(
    outage_s: float,
) -> None:
    # Lease 0.2 s: a 3 s window, so commits stop after 2 s without a hold shown.
    store = _SwitchableStore()
    writer = DriverHeartbeatWriter(
        store,  # type: ignore[arg-type]
        "j",
        interval_s=0.05,
        lease_s=0.2,
    )
    writer.start()
    try:
        assert writer.wait_written(5.0)

        def unreachable() -> Any:
            raise OSError("storage unavailable")

        # No keeper polls: only the heartbeat landing again can tell it.
        keeper = cp._HoldKeeper(
            job_id="j",
            table_name="t",
            open_dataset=unreachable,
            heartbeat=writer,
            stale_leases=15,
            renewed=False,
            on_event=None,
        )
        writer.add_listener(keeper.heartbeat_landed)
        store.down.set()
        time.sleep(outage_s)
        store.down.clear()
        recovered = time.monotonic()
        _wait_until(lambda: (writer.seconds_since_written() or 99) < 1.0)
        assert time.monotonic() - recovered < 1.0

        if outage_s:
            with pytest.raises(CompactionPauseLapsedError):
                keeper.check_held()
        else:
            keeper.check_held()
    finally:
        writer.stop()


def test_a_landed_heartbeat_holds_for_good_when_silent_drivers_keep_holding(
    table_uri: str,
) -> None:
    _keeper(table_uri, _Heartbeat(since=10 * 3600.0), stale_leases=0).check_held()


def test_only_the_lapsed_jobs_commits_are_stopped(
    table_uri: str, history: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    lapsed = _running(history)
    pause = pause_for_job(
        table_name="t",
        job_id=lapsed,
        open_dataset=_opener(table_uri),
        history=history,
        heartbeat=_Heartbeat(),  # type: ignore[arg-type]
        config=ENABLED,
    )
    assert pause is not None
    monkeypatch.setattr(cp._HoldKeeper, "silent_s", lambda self: 3600.0)

    cp.check_compaction_hold("another-job")
    cp.check_compaction_hold(None)
    with pytest.raises(CompactionPauseLapsedError):
        cp.check_compaction_hold(lapsed)

    resume_after_job(pause)
    cp.check_compaction_hold(lapsed)  # the job has ended


def test_a_sparse_commit_is_stopped_before_it_lands(table_uri: str) -> None:
    from geneva.runners.sparse_update import SparseCommitManager

    def lapsed() -> None:
        raise CompactionPauseLapsedError("lapsed")

    ds = lance.dataset(table_uri)
    manager = SparseCommitManager(ds, 0, before_commit=lapsed)

    with pytest.raises(CompactionPauseLapsedError):
        manager._commit(
            lance.LanceOperation.Update(removed_fragment_ids=[], new_fragments=[])
        )
    assert lance.dataset(table_uri).version == ds.version


def test_renewing_drops_renewals_that_have_lapsed(table_uri: str) -> None:
    pause_compaction(_opener(table_uri), renewal=HoldRenewal("old", 60.0))
    overrides = _overrides(table_uri)
    assert overrides is not None
    marker = overrides["job_types"]["compaction"][PAUSE_MARKER]
    marker[RENEWALS_KEY]["old"]["at"] = (dt_now_utc() - timedelta(hours=1)).isoformat()
    _set_overrides(table_uri, overrides)

    pause_compaction(_opener(table_uri), renewal=HoldRenewal("new", 60.0))

    assert list(_renewals(table_uri)) == ["new"]


def test_an_unreadable_heartbeat_leaves_compaction_paused(
    table_uri: str, history: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    other = _running(history)
    _pause(table_uri, history, other)
    events: list[str] = []
    me = _running(history)
    pause = _pause(table_uri, history, me, on_event=events.append)

    def unreadable(job_id: str) -> None:
        raise OSError("storage unavailable")

    monkeypatch.setattr(history, "get_heartbeat", unreadable)
    with pytest.raises(OSError, match="storage unavailable"):
        jobs_holding_pause(history, "t", exclude_job_id=me)

    resume_after_job(pause)

    assert _paused(table_uri)
    assert events == ["Compaction left paused: OSError: storage unavailable"]


def test_compaction_an_operator_turned_off_is_never_resumed(
    table_uri: str, history: Any
) -> None:
    _set_overrides(table_uri, {"job_types": {"compaction": {"enabled": False}}})
    pause = _pause(table_uri, history, _running(history))
    assert pause.outcome is PauseOutcome.DISABLED_BY_POLICY
    assert pause.keeper is None

    resume_after_job(pause)

    assert _overrides(table_uri) == {"job_types": {"compaction": {"enabled": False}}}


def test_a_failed_resume_is_recorded_and_does_not_raise(
    table_uri: str, history: Any, caplog: pytest.LogCaptureFixture
) -> None:
    events: list[str] = []
    pause = _pause(table_uri, history, _running(history), on_event=events.append)

    def broken() -> Any:
        raise OSError("storage unavailable")

    pause.open_dataset = broken
    with caplog.at_level(logging.WARNING, logger=cp.__name__):
        resume_after_job(pause)

    assert "stays paused until another Geneva job on the table ends" in caplog.text
    assert events == ["Compaction left paused: OSError: storage unavailable"]


def test_a_lost_driver_resumes_compaction_from_the_submitter(
    table_uri: str, history: Any
) -> None:
    lost = _running(history)
    _pause(table_uri, history, lost)
    history.set_failed(lost, "WorkerCrashedError: the driver died")

    cp.resume_after_driver_loss(
        table_name="t", open_dataset=_opener(table_uri), history=history, config=ENABLED
    )

    assert _overrides(table_uri) is None


def test_a_driver_that_replaced_a_lost_one_keeps_the_pause(
    table_uri: str, history: Any
) -> None:
    # The same job id runs again; the new driver's heartbeat is live.
    job = _running(history)
    _pause(table_uri, history, job)

    cp.resume_after_driver_loss(
        table_name="t", open_dataset=_opener(table_uri), history=history, config=ENABLED
    )

    assert _paused(table_uri)


class _History:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.failed: list[str] = []

    def set_failed(self, job_id: str, error: str, object_ref: bytes) -> None:
        if self.fail:
            raise OSError("jobs table unavailable")
        self.failed.append(job_id)


@pytest.mark.parametrize("recorded", [True, False])
def test_the_submitter_resumes_compaction_once_it_records_a_lost_driver(
    monkeypatch: pytest.MonkeyPatch, recorded: bool
) -> None:
    import ray.exceptions

    from geneva.runners.ray import jobstate

    resumed = threading.Event()
    calls: list[dict[str, Any]] = []

    def resume(**kwargs: Any) -> None:
        calls.append(kwargs)
        resumed.set()

    monkeypatch.setattr(jobstate, "resume_after_driver_loss", resume)
    history = _History(fail=not recorded)
    state = jobstate.RayJobState(
        history,  # type: ignore[arg-type]
        "j",
        SimpleNamespace(table_name="t"),  # type: ignore[arg-type]
    )
    state.object_ref = b"ref"

    state.finish_failure(ray.exceptions.WorkerCrashedError())

    if recorded:
        assert resumed.wait(5.0)
        (call,) = calls
        assert (call["table_name"], call["history"]) == ("t", history)
    else:
        assert not resumed.wait(0.2), "resumed without recording the job failed"


# --- Waiting for compactions already running (read-only registry) -------------------


TABLE = RegistryTableRef.for_table("mydb", ["items"])


def test_distribution_hash_matches_sophon() -> None:
    # Test vector from Sophon's job_registry.rs.
    assert distribution_hash("tb_db:public$table") == "a7ac6964"


@pytest.mark.parametrize(
    ("database", "table_id", "dist_key"),
    [
        ("db", ["t"], "db:public$t"),
        ("db", ["public", "t"], "db:public$t"),
        ("db", ["a", "b", "t"], "db:a$b$t"),
        ("db/a", ["t"], "db:a$t"),
    ],
)
def test_table_ref_mirrors_sophon(
    database: str, table_id: list[str], dist_key: str
) -> None:
    ref = RegistryTableRef.for_table(database, table_id)
    assert ref.dist_key == dist_key
    assert ref.prefix == (
        f"_jobs/v1/l/{distribution_hash('tb_' + dist_key)}_tb/{dist_key}"
    )


def _write_record(root: Path, key: str, footer: dict[str, Any]) -> None:
    """A registry record: a Lance 2.0 file with the footer in schema metadata."""
    from lance.file import LanceFileWriter

    path = root.joinpath(*key.split("/"))
    path.parent.mkdir(parents=True, exist_ok=True)
    schema = pa.schema([pa.field("job_id", pa.string())])
    writer = LanceFileWriter(str(path), schema, version="2.0")
    writer.write_batch(
        pa.RecordBatch.from_pylist([{"job_id": footer["job_id"]}], schema=schema)
    )
    writer.add_schema_metadata(FOOTER_KEY, json.dumps(footer))
    writer.close()


_created = iter(range(1_790_000_000_000, 1_800_000_000_000))


def _compaction_record(
    root: Path,
    table: RegistryTableRef = TABLE,
    *,
    state: str = "in_progress",
    file_state: str = "active",
    key: str = "agent_1",
    job_type: str = "compact",
) -> tuple[str, str]:
    """A compaction record as Sophon's agent writes it; returns (job id, key)."""
    created = next(_created)
    job_id = f"j1-cp-{created}-{key}"
    record_key = (
        f"{table.prefix}/{U64_MAX - created:016x}-{key}-{job_type}/{file_state}.lance"
    )
    _write_record(
        root,
        record_key,
        {"version": 4, "job_id": job_id, "job_type": job_type, "latest_state": state},
    )
    return job_id, record_key


def _finish_compaction(root: Path, key: str) -> None:
    active = root.joinpath(*key.split("/"))
    _write_record(
        root,
        key.replace("active.lance", "succeeded.lance"),
        {"job_id": active.parent.name, "latest_state": "succeeded"},
    )
    active.unlink()


def _wait_config(root: Path, **overrides: float) -> CompactionPauseConfig:
    values: dict[str, Any] = {
        "enabled": True,
        "job_registry_root_uri": str(root),
        "job_registry_database": "mydb",
        "compaction_settle_s": 0.0,
        "compaction_poll_interval_s": 0.0,
    }
    values.update(overrides)
    return CompactionPauseConfig(**values)


def test_in_flight_compactions_are_unfinished_compactions_of_the_table(
    tmp_path: Path,
) -> None:
    running, _ = _compaction_record(tmp_path, key="agent_1")
    queued, _ = _compaction_record(tmp_path, key="agent_2", state="queued")
    _compaction_record(tmp_path, key="agent_3", state="succeeded")  # finishing
    _compaction_record(tmp_path, key="agent_4", file_state="succeeded")
    _compaction_record(tmp_path, key="agent_5", job_type="reindex_btree")
    other = RegistryTableRef.for_table("mydb", ["other"])
    _compaction_record(tmp_path, other, key="agent_6")

    found = in_flight_compactions(LocalRecordReader(str(tmp_path)), TABLE)

    assert sorted(found) == sorted([running, queued])


def test_unreadable_compaction_record_does_not_block(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    key = f"{TABLE.prefix}/{U64_MAX - 1:016x}-agent_1-compact/active.lance"
    path = tmp_path.joinpath(*key.split("/"))
    path.parent.mkdir(parents=True)
    path.write_bytes(b"?")

    with caplog.at_level(logging.WARNING):
        assert in_flight_compactions(LocalRecordReader(str(tmp_path)), TABLE) == []
    assert "Could not read job registry record" in caplog.text


def test_no_wait_without_running_compactions(tmp_path: Path) -> None:
    slept: list[float] = []
    config = _wait_config(tmp_path, compaction_settle_s=10.0)

    found = cp.wait_for_compactions(
        table_id=["items"], config=config, sleep=slept.append
    )

    assert found == []
    assert slept == [10.0]  # only the settle pause


def test_waits_until_the_compaction_finishes(tmp_path: Path) -> None:
    job_id, key = _compaction_record(tmp_path)
    waits: list[list[str]] = []
    polls: list[float] = []

    def sleep(seconds: float) -> None:
        polls.append(seconds)
        if len(polls) == 3:
            _finish_compaction(tmp_path, key)

    config = _wait_config(tmp_path, compaction_poll_interval_s=30.0)
    found = cp.wait_for_compactions(
        table_id=["items"], config=config, on_wait=waits.append, sleep=sleep
    )

    assert found == [job_id]
    assert waits == [[job_id]]
    assert polls == [0.0, 30.0, 30.0]


def test_gives_up_waiting_after_the_timeout(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    job_id, _ = _compaction_record(tmp_path)
    now = [0.0]

    def sleep(seconds: float) -> None:
        now[0] += 600.0

    config = _wait_config(tmp_path, compaction_wait_timeout_s=1800.0)
    events: list[str] = []
    with caplog.at_level(logging.WARNING, logger=cp.__name__):
        found = cp.wait_for_compactions(
            table_id=["items"],
            config=config,
            on_event=events.append,
            sleep=sleep,
            clock=lambda: now[0],
        )

    assert found == [job_id]
    assert "still running after 1800s; proceeding" in caplog.text
    assert events == [
        f"Stopped waiting for compaction {job_id} after 1800s; planning anyway"
    ]


def test_a_failed_check_for_compactions_is_recorded(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken(*args: Any) -> list[str]:
        raise RuntimeError("registry unreadable")

    monkeypatch.setattr(cp, "in_flight_compactions", broken)
    events: list[str] = []

    found = cp.wait_for_compactions(
        table_id=["items"],
        config=_wait_config(tmp_path),
        on_event=events.append,
        sleep=lambda s: None,
    )

    assert found == []
    assert events == [
        "Could not check for running compactions: RuntimeError: registry unreadable"
    ]


def test_waiting_needs_the_registry_and_can_be_turned_off(tmp_path: Path) -> None:
    _compaction_record(tmp_path)

    def unexpected(seconds: float) -> None:
        raise AssertionError("must not sleep")

    for config in [
        _wait_config(tmp_path, compaction_wait_timeout_s=0.0),
        CompactionPauseConfig(enabled=True),
        CompactionPauseConfig(
            job_registry_root_uri=str(tmp_path), job_registry_database="mydb"
        ),
    ]:
        assert (
            cp.wait_for_compactions(table_id=["items"], config=config, sleep=unexpected)
            == []
        )


def test_s3_reader_lists_keys_relative_to_the_root() -> None:
    client = boto3.client(
        "s3",
        region_name="us-west-2",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    reader = S3RecordReader("bucket", "lancedb-system", region=None, client=client)
    stub = Stubber(client)
    stub.add_response(
        "list_objects_v2",
        {"Contents": [{"Key": "lancedb-system/_jobs/v1/l/x/active.lance"}]},
        {"Bucket": "bucket", "Prefix": "lancedb-system/_jobs/v1/l/x/"},
    )
    stub.add_response(
        "get_object",
        {"Body": io.BytesIO(b"data"), "ETag": '"e"'},
        {"Bucket": "bucket", "Key": "lancedb-system/_jobs/v1/l/x/active.lance"},
    )
    stub.add_client_error("get_object", "NoSuchKey", http_status_code=404)
    with stub:
        assert reader.list("_jobs/v1/l/x") == ["_jobs/v1/l/x/active.lance"]
        assert reader.get("_jobs/v1/l/x/active.lance") == b"data"
        with pytest.raises(FileNotFoundError):
            reader.get("_jobs/v1/l/x/active.lance")


# --- Driver wiring -------------------------------------------------------------


@geneva.udf(data_type=pa.int64())
def _plus_one(a: int) -> int:
    return a + 1


def _sparse_result() -> SparseUpdateResult:
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


def _use_config(monkeypatch: pytest.MonkeyPatch, config: CompactionPauseConfig) -> None:
    monkeypatch.setattr(CompactionPauseConfig, "get", classmethod(lambda cls: config))


@pytest.fixture
def driver_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    db = geneva.connect(str(tmp_path / "db"))
    tbl = db.create_table("t", pa.table({"a": pa.array([1, 2], type=pa.int64())}))
    tbl.add_columns({"b": _plus_one})
    job_id = db._history.launch("t", "b").job_id
    registry = tmp_path / "registry"
    _use_config(monkeypatch, _wait_config(registry))
    return {
        "db_uri": str(tmp_path / "db"),
        "table": tbl,
        "job_id": job_id,
        "registry": registry,
    }


def _latest_overrides(env: dict[str, Any]) -> dict[str, Any] | None:
    tbl = env["table"]
    tbl.checkout_latest()
    raw = tbl.to_lance().config().get(TABLE_OVERRIDES_CONFIG_KEY)
    return None if raw is None else json.loads(raw)


def _run_driver(env: dict[str, Any]) -> object:
    return run_ray_add_column_remote._function(
        env["table"].get_reference(),
        "b",
        job_id=env["job_id"],
        update_mode="sparse_rows",
        where="a > 1",
    )


def test_backfill_driver_pauses_compaction_while_it_runs(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    seen: list[dict[str, Any] | None] = []

    def work(*args: object, **kwargs: object) -> SparseUpdateResult:
        seen.append(_latest_overrides(driver_env))
        return _sparse_result()

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", work)

    _run_driver(driver_env)

    (during,) = seen
    assert during is not None
    assert during["job_types"]["compaction"]["enabled"] is False
    assert _latest_overrides(driver_env) is None


def test_failed_backfill_driver_resumes_compaction(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", fail)

    with pytest.raises(RuntimeError, match="boom"):
        _run_driver(driver_env)

    assert _latest_overrides(driver_env) is None


def test_backfill_driver_records_that_compaction_was_not_paused(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    tbl = driver_env["table"]
    tbl.to_lance().update_config({TABLE_OVERRIDES_CONFIG_KEY: "not json"})
    monkeypatch.setattr(
        sparse_pipeline, "run_ray_sparse_update", lambda *a, **k: _sparse_result()
    )

    _run_driver(driver_env)

    job = geneva.connect(driver_env["db_uri"])._history.get(driver_env["job_id"])[0]
    assert any(e.startswith("Compaction not paused: ") for e in job.events)


def test_backfill_driver_without_config_writes_nothing(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    _use_config(monkeypatch, CompactionPauseConfig())
    version = driver_env["table"].version
    monkeypatch.setattr(
        sparse_pipeline, "run_ray_sparse_update", lambda *a, **k: _sparse_result()
    )

    _run_driver(driver_env)

    assert _latest_overrides(driver_env) is None
    assert driver_env["table"].version == version


def test_a_finishing_job_keeps_a_quiet_live_drivers_pause(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    tbl = driver_env["table"]
    hist = tbl._conn._history
    first = driver_env["job_id"]
    second = hist.launch("t", "b").job_id
    _use_config(monkeypatch, CompactionPauseConfig(enabled=True))
    seen: list[dict[str, Any] | None] = []

    def work(*args: Any, **kwargs: Any) -> None:
        if kwargs["job_id"] != first:
            return
        # The first driver goes quiet, e.g. planning, while another job runs.
        _go_quiet(hist, first)
        run_ray_add_column_remote._function(tbl.get_reference(), "b", job_id=second)
        assert hist.get(first)[0].status == "RUNNING"
        assert hist.get(second)[0].status == "DONE"
        seen.append(_latest_overrides(driver_env))

    monkeypatch.setattr(ray_pipeline, "run_ray_add_column", work)
    run_ray_add_column_remote._function(tbl.get_reference(), "b", job_id=first)

    (during,) = seen
    assert during is not None, "the second job resumed compaction under the first"
    assert during["job_types"]["compaction"]["enabled"] is False
    assert _latest_overrides(driver_env) is None


@pytest.mark.ray
def test_a_backfill_whose_pause_lapsed_commits_nothing(
    driver_env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    local_ray_context: None,
) -> None:
    monkeypatch.setattr(cp._HoldKeeper, "silent_s", lambda self: 3600.0)
    tbl = driver_env["table"]

    # The driver re-raises it as a picklable RuntimeError naming the type.
    with pytest.raises(RuntimeError, match="CompactionPauseLapsedError"):
        run_ray_add_column_remote._function(
            tbl.get_reference(), "b", job_id=driver_env["job_id"]
        )

    tbl.checkout_latest()
    assert tbl.to_arrow()["b"].null_count == tbl.count_rows()
    job = geneva.connect(driver_env["db_uri"])._history.get(driver_env["job_id"])[0]
    assert job.status == "FAILED"
    assert any(e.startswith("Compaction pause may have lapsed: ") for e in job.events)


def test_backfill_driver_waits_for_a_running_compaction_then_plans_on_it(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    registry = driver_env["registry"]
    compaction_id, key = _compaction_record(
        registry, RegistryTableRef.for_table("mydb", ["t"])
    )
    _use_config(monkeypatch, _wait_config(registry, compaction_poll_interval_s=0.05))
    compacted: list[int] = []

    def compaction_commits() -> None:
        # The compaction lands a new table version, then finishes.
        tbl = driver_env["table"]
        tbl.add(pa.table({"a": pa.array([3], type=pa.int64())}))
        tbl.checkout_latest()
        compacted.append(tbl.version)
        _finish_compaction(registry, key)

    timer = threading.Timer(0.3, compaction_commits)
    seen: list[int] = []

    def work(*args: object, **kwargs: Any) -> SparseUpdateResult:
        seen.append(kwargs["read_version"])
        return _sparse_result()

    monkeypatch.setattr(sparse_pipeline, "run_ray_sparse_update", work)
    timer.start()
    try:
        _run_driver(driver_env)
    finally:
        timer.cancel()

    assert seen == compacted
    job = geneva.connect(driver_env["db_uri"])._history.get(driver_env["job_id"])[0]
    assert f"Waiting for compaction {compaction_id}" in job.events


def _compact_during_wait(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> tuple[list[int], list[int], set[int]]:
    """Run the public backfill with a real compaction landing while its driver
    waits; returns the versions handed to planning, the version the compaction
    produced, and the pre-compaction fragment ids."""
    tbl = driver_env["table"]
    tbl.add(pa.table({"a": pa.array([3, 4], type=pa.int64())}))
    old_ids = {f.fragment_id for f in tbl.to_lance().get_fragments()}
    registry = driver_env["registry"]
    _, key = _compaction_record(registry, RegistryTableRef.for_table("mydb", ["t"]))
    polls: list[float] = []
    compacted: list[int] = []

    def sleep(seconds: float) -> None:
        polls.append(seconds)
        if len(polls) == 2:  # the first poll has seen the running compaction
            tbl.to_lance().optimize.compact_files(target_rows_per_fragment=100)
            tbl.checkout_latest()
            compacted.append(tbl.version)
            _finish_compaction(registry, key)

    def wait(**kwargs: Any) -> list[str]:
        return cp.wait_for_compactions(**kwargs, sleep=sleep)

    planned: list[int] = []

    def plan(*args: Any, **kwargs: Any) -> None:
        planned.append(kwargs["read_version"])

    def dispatch(ref: Any, column: str, **kwargs: Any) -> object:
        run_ray_add_column_remote._function(
            ref,
            column,
            job_id=kwargs["job_id"],
            read_version=kwargs.get("read_version"),
            read_version_pinned=kwargs.get("read_version_pinned", True),
        )
        return SimpleNamespace()

    monkeypatch.setattr(ray_pipeline, "wait_for_compactions", wait)
    monkeypatch.setattr(ray_pipeline, "run_ray_add_column", plan)
    monkeypatch.setattr(ray_pipeline, "dispatch_run_ray_add_column", dispatch)
    return planned, compacted, old_ids


def test_public_backfill_plans_against_the_compaction_it_waited_for(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    planned, compacted, old_ids = _compact_during_wait(driver_env, monkeypatch)
    tbl = driver_env["table"]
    launched_at = tbl.version

    tbl.backfill_async(
        "b", job_id=driver_env["job_id"], _admission_check=False, _return_future=True
    )

    assert planned == compacted
    assert planned[0] > launched_at
    planned_at = tbl.to_lance().checkout_version(planned[0])
    planned_ids = {f.fragment_id for f in planned_at.get_fragments()}
    assert not old_ids & planned_ids


def test_public_backfill_keeps_an_explicitly_requested_version(
    driver_env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    planned, _, _ = _compact_during_wait(driver_env, monkeypatch)
    tbl = driver_env["table"]
    requested = tbl.version

    with caplog.at_level(logging.WARNING, logger=ray_pipeline.__name__):
        tbl.backfill_async(
            "b",
            job_id=driver_env["job_id"],
            read_version=requested,
            _admission_check=False,
            _return_future=True,
        )

    assert planned == [requested]
    assert "reads a pinned table version" in caplog.text


def test_public_backfill_plans_past_a_compaction_the_wait_never_saw(
    driver_env: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A compaction the agent admitted just before the pause and finished
    before the driver polled the registry is never waited for, but the launch
    snapshot's fragments are gone all the same."""
    tbl = driver_env["table"]
    tbl.add(pa.table({"a": pa.array([3, 4], type=pa.int64())}))
    old_ids = {f.fragment_id for f in tbl.to_lance().get_fragments()}
    launched_at = tbl.version
    compacted: list[int] = []
    planned: list[int] = []

    def dispatch(ref: Any, column: str, **kwargs: Any) -> object:
        # Lands between the launch snapshot and the driver's pause.
        tbl.to_lance().optimize.compact_files(target_rows_per_fragment=100)
        tbl.checkout_latest()
        compacted.append(tbl.version)
        run_ray_add_column_remote._function(
            ref,
            column,
            job_id=kwargs["job_id"],
            read_version=kwargs.get("read_version"),
            read_version_pinned=kwargs.get("read_version_pinned", True),
        )
        return SimpleNamespace()

    def plan(*args: Any, **kwargs: Any) -> None:
        planned.append(kwargs["read_version"])

    monkeypatch.setattr(ray_pipeline, "run_ray_add_column", plan)
    monkeypatch.setattr(ray_pipeline, "dispatch_run_ray_add_column", dispatch)

    tbl.backfill_async(
        "b", job_id=driver_env["job_id"], _admission_check=False, _return_future=True
    )

    # The pause's own config commit lands after the compaction, so the job
    # plans at or past the compacted version, never at the launch snapshot.
    (planned_version,) = planned
    assert planned_version > launched_at
    assert planned_version >= compacted[0]
    planned_at = tbl.to_lance().checkout_version(planned_version)
    planned_ids = {f.fragment_id for f in planned_at.get_fragments()}
    assert not old_ids & planned_ids


@pytest.mark.parametrize(("read_version", "pinned"), [(None, False), (1, True)])
def test_sync_backfill_tells_async_whether_the_version_was_requested(
    driver_env: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
    read_version: int | None,
    pinned: bool,
) -> None:
    seen: list[Any] = []

    class _StopError(Exception):
        pass

    def capture(self: Any, *args: Any, **kwargs: Any) -> None:
        seen.append(kwargs.get("_read_version_pinned"))
        raise _StopError

    monkeypatch.setattr(type(driver_env["table"]), "backfill_async", capture)
    kwargs = {} if read_version is None else {"read_version": read_version}
    with pytest.raises(_StopError):
        driver_env["table"].backfill("b", **kwargs)

    assert seen == [pinned]
