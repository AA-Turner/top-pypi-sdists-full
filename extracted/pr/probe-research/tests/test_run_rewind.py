"""run(on_conflict=Rewind(step=N)) — resume from a checkpoint, rewriting the tail.

The parameterized policy (0185): the incumbent reopens IN PLACE and its record
from ``step`` onward is discarded in the same server transaction, so the
relaunch's writes land instead of losing to first-write-wins slots. `completed`
unlocks under the explicit flag (the deliberate stop-then-rewind flow); the
preflight + receipt echo make a pre-0185 server a loud no-op instead of a
silent reopen-without-delete; and every telemetry write now carries the
writer's ``(session_id, write_epoch)`` so a superseded process fences.
"""

from __future__ import annotations

import pytest

from probe import Rewind, errors


def _stopped_job(client, app, status="completed", steps=(50, 100, 150)):
    client.create_project("rewind-lab", "Rewind Lab", kind="general")
    run = client.run(project="rewind-lab", name="job", external_id="job", heartbeat=False)
    for s in steps:
        run.log({"loss": 1.0 / s}, step=s)
    app.runs[run.id]["status"] = status
    app.runs[run.id]["ended_at"] = "2026-01-01T01:00:00Z"
    return run


def _relaunch(client, step):
    return client.run(
        project="rewind-lab",
        name="job",
        external_id="job",
        heartbeat=False,
        on_conflict=Rewind(step=step),
    )


# -- the policy object itself ------------------------------------------------


def test_rewind_validates_its_step():
    with pytest.raises(errors.ValidationError):
        Rewind(step=-1)
    with pytest.raises(errors.ValidationError):
        Rewind(step="100")  # type: ignore[arg-type]
    with pytest.raises(errors.ValidationError):
        Rewind(step=True)  # bool is an int in name only


def test_the_policy_error_names_rewind(client):
    client.create_project("rewind-lab", "Rewind Lab", kind="general")
    with pytest.raises(errors.ValidationError) as excinfo:
        client.run(project="rewind-lab", name="x", on_conflict="rewind")
    assert "Rewind(step=" in str(excinfo.value)


# -- the rewind flow ---------------------------------------------------------


def test_rewind_resumes_a_completed_incumbent_and_discards_the_tail(client, app):
    first = _stopped_job(client, app)

    resumed = _relaunch(client, 100)

    assert resumed.id == first.id, "same identity — a rewind is not a retry row"
    row = app.runs[first.id]
    assert row["status"] == "running"
    assert row["write_epoch"] == 2
    steps = [p["step_index"] for p in app.metric_points_posted[first.id]]
    assert steps == [50], "everything from the rewind step onward is gone"
    (recovery,) = row["recoveries"]
    assert recovery["prior_status"] == "completed"


def test_the_rewound_range_is_writable_again(client, app):
    _stopped_job(client, app)
    resumed = _relaunch(client, 100)

    # The guard armed at the POST-DELETE maximum (50), so the checkpoint step
    # itself — and everything after it — is writable, W&B-style.
    resumed.log({"loss": 0.42}, step=100)

    steps = [p["step_index"] for p in app.metric_points_posted[resumed.id]]
    assert steps == [50, 100]
    # Below the surviving curve: still guarded -- dropped with a warning
    # (plan 2.4, D6), and refused outright under strict.
    with pytest.warns(UserWarning, match="DROPPED"):
        assert resumed.log({"loss": 0.9}, step=50) is None
    with pytest.raises(errors.ValidationError):
        resumed.log({"loss": 0.9}, step=50, strict=True)
    assert [p["step_index"] for p in app.metric_points_posted[resumed.id]] == [50, 100]


def test_rewind_works_on_a_dead_incumbent_too(client, app):
    _stopped_job(client, app, status="crashed")
    resumed = _relaunch(client, 100)
    assert app.runs[resumed.id]["status"] == "running"


def test_rewind_refuses_a_live_incumbent(client, app):
    _stopped_job(client, app, status="running")
    with pytest.raises(errors.ConflictError) as excinfo:
        _relaunch(client, 100)
    assert "alive" in str(excinfo.value)


def test_plain_resume_still_refuses_completed_and_names_rewind(client, app):
    _stopped_job(client, app)
    with pytest.raises(errors.ConflictError) as excinfo:
        client.run(project="rewind-lab", name="job", external_id="job", heartbeat=False)
    assert "Rewind(step=" in str(excinfo.value)


# -- version skew ------------------------------------------------------------


def test_a_pre_rewind_server_is_a_loud_noop(client, app):
    """The preflight fires BEFORE the reopen: nothing about the run changes."""
    first = _stopped_job(client, app)
    app.supports_rewind = False

    with pytest.raises(errors.NotFoundError) as excinfo:
        _relaunch(client, 100)

    assert "predates run rewind" in str(excinfo.value)
    row = app.runs[first.id]
    assert row["status"] == "completed", "no state changed"
    assert "recoveries" not in row, "the reopen was never sent"


def test_a_missing_rewind_echo_is_a_hard_error(client, app):
    """Belt to the preflight's suspenders: a server that declares the feature
    but drops the echo is never trusted to have deleted anything."""
    _stopped_job(client, app, status="crashed")
    app.supports_rewind_echo = False

    with pytest.raises(errors.ConflictError) as excinfo:
        _relaunch(client, 100)
    assert "no rewind echo" in str(excinfo.value)


# -- writer fencing (the epoch rides every write) -----------------------------


def test_writes_carry_the_writer_fingerprint(client, app):
    client.create_project("rewind-lab", "Rewind Lab", kind="general")
    run = client.run(project="rewind-lab", name="fresh", heartbeat=False)
    run.log({"loss": 1.0}, step=1)

    raw = app.metric_batches_posted[-1]
    assert raw["write_epoch"] == 1, "a fresh handle writes under epoch 1"
    assert raw["session_id"] == run.session_id


def test_a_rewound_handle_writes_under_the_new_epoch(client, app):
    _stopped_job(client, app)
    resumed = _relaunch(client, 100)
    resumed.log({"loss": 0.1}, step=120)

    raw = app.metric_batches_posted[-1]
    assert raw["write_epoch"] == 2, "the receipt's epoch, not the create default"
    assert raw["session_id"] == resumed.session_id


# -- fork: the keep-both path -------------------------------------------------


def test_fork_run_keeps_the_source_untouched(client, app):
    source = _stopped_job(client, app)

    fork = client.fork_run(source.id, step=100, heartbeat=False)

    assert fork.id != source.id
    src_row = app.runs[source.id]
    assert src_row["status"] == "completed", "a fork writes nothing to its source"
    assert "superseded" not in (src_row.get("tags") or [])
    fork_row = app.runs[fork.id]
    assert fork_row["parent_run_id"] == source.id
    assert fork_row["parent_relation"] == "fork"
    assert fork_row["foreign_keys"]["fork_of"] == source.id
    assert fork_row["foreign_keys"]["fork_step"] == 100
    steps = [p["step_index"] for p in app.metric_points_posted[source.id]]
    assert steps == [50, 100, 150], "the source curve survives whole"
