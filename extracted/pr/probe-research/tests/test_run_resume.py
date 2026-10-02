"""run(on_conflict="auto"/"resume") — a dead incumbent is reopened in place.

Same run, same curve: the reopen bumps the write epoch, registers the new
writer session, and the returned handle refuses steps the first execution
already wrote. Completed and live incumbents still conflict — resuming is for
dead runs only, and a from-scratch retry belongs to "supersede".
"""

from __future__ import annotations

import warnings

import pytest

from probe import errors


def _crashed_job(client, app, status="crashed", steps=(50, 100)):
    """A run that logged some curve and then died."""
    client.create_project("resume-lab", "Resume Lab", kind="general")
    run = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    for s in steps:
        run.log({"loss": 1.0 / (s or 1)}, step=s)
    app.runs[run.id]["status"] = status
    app.runs[run.id]["ended_at"] = "2026-01-01T01:00:00Z"
    return run


def test_auto_resumes_a_crashed_incumbent_in_place(client, app):
    first = _crashed_job(client, app)

    resumed = client.run(
        project="resume-lab", name="job", external_id="job", heartbeat=False
    )  # default policy: auto

    assert resumed.id == first.id  # same identity, not a -rN sibling
    row = app.runs[first.id]
    assert row["status"] == "running"
    assert row["ended_at"] is None
    assert row["write_epoch"] == 2
    assert row["current_session_id"] == resumed.session_id
    (recovery,) = row["recoveries"]
    assert recovery["prior_status"] == "crashed"
    assert recovery["last_step"] == 100


def _said(caught, needle: str) -> list[str]:
    return [str(w.message) for w in caught if needle in str(w.message)]


def _resume_guard_span(app, run_id: str) -> dict:
    """The latest upsert of the run's keyed `resume_guard` diagnostic span."""
    rows = [s for s in app.spans.get(run_id, []) if s.get("external_key") == "resume_guard"]
    assert rows, "no resume_guard span was written"
    return rows[-1]


def test_a_step_already_written_is_dropped_with_one_warning(client, app):
    """D6 (plan 2.4). A relaunch that restarted from an OLDER checkpoint
    re-logs steps the first execution already wrote. That used to RAISE inside
    `log()`, killing the relaunch at its first step; W&B drops the call and
    warns, and so does this. `<=`, not `<`: a re-logged step 100 would mix two
    executions' values at one step."""
    _crashed_job(client, app)  # wrote 50 and 100, then died
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert resumed.log({"loss": 0.5}, step=50) is None
        assert resumed.log({"loss": 0.5}, step=100) is None  # the resume point itself
        assert resumed.step(50, attributes={"phase": "retry"}) is None  # records too
        resumed.log({"loss": 0.5}, step=101)
        resumed.log({"loss": 0.5}, step=102)

    steps = [p["step_index"] for p in app.metric_points_posted[resumed.id]]
    assert steps.count(50) == 1 and steps.count(100) == 1  # the first execution's, once
    assert steps.count(101) == 1 and steps.count(102) == 1
    assert 50 not in app.steps.get(resumed.id, {})
    (drop,) = _said(caught, "DROPPED")
    assert "step 50" in drop and "resume point (100)" in drop
    assert "Rewind(step=50)" in drop and "fork_run" in drop
    (resumed_line,) = _said(caught, "logging resumed")
    assert "step 101" in resumed_line and "dropping 3" in resumed_line
    span = _resume_guard_span(app, resumed.id)
    assert span["span_type"] == "diagnostic"
    assert span["attributes"]["dropped_calls"] == 3
    assert span["attributes"]["resume_point"] == 100
    assert span["attributes"]["resumed_at_step"] == 101


def test_a_commit_false_row_past_the_resume_point_announces_the_resume(client, app):
    """Plan (f) meets 2.4: the first write past the resume point says "logging
    resumed" and closes the resume span, even when it goes out as a
    `commit=False` row rather than as an ordinary call."""
    _crashed_job(client, app)
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert resumed.log({"loss": 0.5}, step=50) is None
        resumed.log({"loss": 0.4}, step=101, commit=False)
        resumed.log({"acc": 0.9})  # joins step 101 and writes the row

    (resumed_line,) = _said(caught, "logging resumed")
    assert "step 101" in resumed_line and "dropping 1" in resumed_line
    assert _resume_guard_span(app, resumed.id)["attributes"]["resumed_at_step"] == 101


def test_strict_still_raises_below_the_resume_point(client, app):
    _crashed_job(client, app)
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)

    with pytest.raises(errors.ValidationError) as excinfo:
        resumed.log({"loss": 0.5}, step=100, strict=True)
    assert "supersede" in str(excinfo.value)
    with pytest.raises(errors.ValidationError):
        resumed.step(50, strict=True)


def test_a_dropped_call_journals_nothing(client, app):
    """Dropped means never queued: the only op the drops leave is the keyed,
    non-blocking diagnostic span counting them."""
    _crashed_job(client, app)
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    client.async_writes = True  # queue instead of sending, so the queue is the evidence
    try:
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            for step in (10, 20, 30):
                resumed.log({"loss": 0.5}, step=step)
    finally:
        client.async_writes = False
    ops = [op for _, op in client.journal.pending() if op.get("run_ref") == resumed.id]
    assert [op["path"].rsplit("/", 1)[-1] for op in ops] == ["spans"]
    assert ops[0]["blocking"] is False


def test_resumed_auto_steps_continue_past_the_resume_point(client, app):
    _crashed_job(client, app)
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)

    resumed.log({"loss": 0.4})  # no step: auto counter must start at 101

    assert max(p["step_index"] for p in app.metric_points_posted[resumed.id]) == 101


def test_auto_on_a_completed_incumbent_still_conflicts(client, app):
    _crashed_job(client, app, status="completed")

    with pytest.raises(errors.ConflictError) as excinfo:
        client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    assert "supersede" in str(excinfo.value)


def test_auto_on_a_live_incumbent_refuses_to_hijack(client, app):
    client.create_project("resume-lab", "Resume Lab", kind="general")
    client.run(
        project="resume-lab", name="job", external_id="job", heartbeat=False
    )  # fake leaves it "running"

    with pytest.raises(errors.ConflictError) as excinfo:
        client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    assert "alive" in str(excinfo.value)


def test_explicit_resume_on_a_live_incumbent_also_refuses(client, app):
    client.create_project("resume-lab", "Resume Lab", kind="general")
    client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)

    with pytest.raises(errors.ConflictError):
        client.run(
            project="resume-lab",
            name="job",
            external_id="job",
            heartbeat=False,
            on_conflict="resume",
        )


def test_resume_against_an_old_backend_names_the_upgrade(client, app):
    _crashed_job(client, app)
    app.supports_reopen = False

    with pytest.raises(errors.NotFoundError) as excinfo:
        client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    assert "predates" in str(excinfo.value)


def test_supersede_still_available_for_from_scratch_retries(client, app):
    first = _crashed_job(client, app)

    retry = client.run(
        project="resume-lab",
        name="job",
        external_id="job",
        heartbeat=False,
        on_conflict="supersede",
    )

    assert retry.id != first.id
    assert app.runs[retry.id]["external_id"] == "job-r2"
    assert "superseded" in app.runs[first.id]["tags"]


def test_auto_resumes_an_untracked_incumbent_in_place(client, app):
    """0106: 'untracked' is dead-and-reopenable exactly like 'crashed' — the
    mirror-registered-then-reattached flow this status exists for."""
    first = _crashed_job(client, app, status="untracked")

    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)

    assert resumed.id == first.id
    row = app.runs[first.id]
    assert row["status"] == "running"
    (recovery,) = row["recoveries"]
    assert recovery["prior_status"] == "untracked"


# -- #2022 review follow-ups ---------------------------------------------------


def _guard_rows(app, run_id: str, key: str = "resume_guard") -> list[dict]:
    return [s for s in app.spans.get(run_id, []) if s.get("external_key") == key]


def test_finish_writes_the_final_drop_count(client, app):
    """The span is written on the 1st, 10th, 100th... drop. A relaunch that
    finishes inside the dropped range used to leave it `running` at 10 of 57."""
    _crashed_job(client, app)
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        for step in range(1, 58):
            resumed.log({"loss": 0.5}, step=step)
        resumed.finish("completed")
    last = _guard_rows(app, resumed.id)[-1]
    assert last["attributes"]["dropped_calls"] == 57
    assert last["status"] == "completed"


def test_finish_closes_a_guard_span_whose_count_was_already_right(client, app):
    """Exactly 10 drops: the 10th write had the right count but left the span
    `running`, and nothing closed it."""
    _crashed_job(client, app)
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        for step in range(1, 11):
            resumed.log({"loss": 0.5}, step=step)
        assert _guard_rows(app, resumed.id)[-1]["status"] == "running"
        resumed.finish("completed")
    last = _guard_rows(app, resumed.id)[-1]
    assert (last["status"], last["attributes"]["dropped_calls"]) == ("completed", 10)


def test_finish_writes_the_guard_span_only_when_there_were_drops(client, app):
    """Negative control: no drops -> no span at all. With drops, finish always
    writes the closed final counts once more (one keyed upsert), even after a
    resume already wrote them: the "only when something is missing"
    bookkeeping raced with log() on other threads (#2044 review)."""
    _crashed_job(client, app)
    clean = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    clean.log({"loss": 0.5}, step=101)
    clean.finish("completed")
    assert _guard_rows(app, clean.id) == []

    app.runs[clean.id].update(status="crashed", ended_at="2026-01-01T02:00:00Z")
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        resumed.log({"loss": 0.5}, step=5)
        resumed.log({"loss": 0.5}, step=200)  # past the resume point: closes it
    before = len(_guard_rows(app, resumed.id))
    resumed.finish("completed")
    assert len(_guard_rows(app, resumed.id)) == before + 1
    last = _guard_rows(app, resumed.id)[-1]
    assert (last["status"], last["attributes"]["dropped_calls"]) == ("completed", 1)
    assert last["attributes"]["resumed_at_step"] == 200


def test_the_guard_span_is_the_runs_not_the_open_spans_or_units(client, app):
    """Never parented under the caller's open span, never stamped with the open
    unit's coords: the server sets a span's coordinate once, so a later write
    from another unit would be refused."""
    _crashed_job(client, app)
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        with resumed.span("epoch", name="epoch-0"):
            with resumed.unit(coords={"rank": 3}):
                resumed.log({"loss": 0.5}, step=5)
    (row,) = _guard_rows(app, resumed.id)
    assert row.get("parent_span_id") is None
    assert not row.get("coords")


def test_each_rank_keeps_its_own_guard_span(client, app, monkeypatch):
    """Ranks resuming together wrote ONE span id and overwrote each other."""
    monkeypatch.setenv("RANK", "2")
    monkeypatch.setenv("WORLD_SIZE", "4")
    _crashed_job(client, app)
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        resumed.log({"loss": 0.5}, step=5)
    (row,) = _guard_rows(app, resumed.id, "resume_guard/rank-2")
    assert row["attributes"]["rank"] == 2
    assert _guard_rows(app, resumed.id) == []


def test_resume_drops_are_not_reported_as_outbox_loss(client, app):
    """#2044 review HIGH. Counting a resume drop on `client.dropped_writes`
    made finish() (#2014) stamp `probe_finish.dropped_writes` and warn that
    writes were "dropped before they reached the outbox": a run dropping steps
    exactly as designed was marked as data loss. The run counts its own."""
    _crashed_job(client, app)  # wrote 50 and 100, then died
    resumed = client.run(project="resume-lab", name="job", external_id="job", heartbeat=False)
    before = client.dropped_writes
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        for step in (10, 20, 30):
            resumed.log({"loss": 0.5}, step=step)
        resumed.step(60)
        resumed.log({"loss": 0.5}, step=101)
        resumed.finish("completed")
    assert client.dropped_writes == before
    assert resumed._resume_drops == 4
    summary = app.runs[resumed.id].get("summary") or {}
    assert "probe_finish" not in summary, summary.get("probe_finish")
    assert not [str(w.message) for w in caught if "reached the outbox" in str(w.message)]


def _attached_after_a_reopen(client, app, external_id):
    from tests.conftest import open_run
    from tests.test_run_liveness import _recently

    run = open_run(client, experiment="e", name="r", heartbeat=False)
    run.log({"loss": 1.0}, step=40)
    app.runs[run.id].update(status="untracked", ended_at=_recently(), external_id=external_id)
    return client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)


def test_an_attached_job_is_pointed_at_exits_that_work_from_an_attach(client, app):
    """probe.init() joining PROBE_RUN_ID takes no on_conflict (and ignores
    "supersede"), and `probe run start --rewind-to-step` is deprecated (#1551).
    The warning and the strict error name what works from an attach: re-key
    the relaunch by its external id without PROBE_RUN_ID, `probe exec
    --parent ... --relation retry`, and `probe run fork ... --step`."""
    attached = _attached_after_a_reopen(client, app, "job-7")
    ref = attached._data.get("slug") or attached.id
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        attached.log({"loss": 2.0}, step=40)
    (drop,) = [str(w.message) for w in caught if "DROPPED" in str(w.message)]
    assert "WITHOUT PROBE_RUN_ID, with probe.init(external_id='job-7', on_conflict=probe.Rewind(step=40))" in drop
    assert f"probe run fork {ref} --step 40" in drop
    assert "probe run start" not in drop
    with pytest.raises(errors.ValidationError) as refused:
        attached.log({"loss": 2.0}, step=40, strict=True)
    # Filed beside the run it retries: `probe exec` otherwise files a new run
    # in the active project (#2044 verify).
    assert attached.project_id
    assert (
        f"probe exec --project id:{attached.project_id} --parent {ref} --relation retry"
        in str(refused.value)
    )
    assert "supersede" not in str(refused.value)


def test_an_attached_run_with_no_external_id_is_not_told_to_rewind(client, app):
    """A rewind needs the external id; without one, saying "rewind" names a
    command that refuses."""
    attached = _attached_after_a_reopen(client, app, None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        attached.log({"loss": 2.0}, step=40)
    (drop,) = [str(w.message) for w in caught if "DROPPED" in str(w.message)]
    assert "not possible for this run (it has no external id" in drop
    assert "Rewind" not in drop
