"""Plan 2.8 for the two documented multi-node launches: every rank holds a lease.

`probe exec -- sbatch job.sh` and `probe exec --detached-launcher -- ...` open
the run AWAITING ATTACH: the submitter exits the moment the scheduler accepts
the job, and each rank's `probe.init()` joins the run through `PROBE_RUN_ID`.
Found by the Slurm environment test (lane E1, #2113): such a run never asked
for the lease rules (`Client._lease_for_create` returned early for a
hand-off), so it stayed `legacy`. The ranks' writer-gone reports after a
`scancel` changed nothing, the run stayed `running` until the 900 s reaper,
and `writer_lost` (which reads only `leases` runs,
app/findings/snapshot.py) could never see a lost node.

Now the hand-off's create asks for `leases` with no writer of its own (the
submitter holds no lease: it is gone before the work starts), every rank
registers its lease when it attaches, and the run closes by the lease rules.
"""

from __future__ import annotations

import json
import os
import signal
import stat
import subprocess
import sys
import time

import pytest

from probe import cli
from probe.sdk import fluent, outputs
from tests.conftest import make_client


@pytest.fixture
def app(app):
    app.supports_leases = True
    return app


@pytest.fixture
def cli_client(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "login-spool")

    monkeypatch.setattr(cli, "Client", factory)
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"])
    return app


@pytest.fixture
def sbatch(tmp_path, monkeypatch):
    """A stand-in `sbatch` on PATH: it accepts the job and returns, as the
    real one does."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    script = bindir / "sbatch"
    script.write_text("#!/bin/sh\necho 'Submitted batch job 42'\n")
    script.chmod(script.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    monkeypatch.setenv("PATH", f"{bindir}{os.pathsep}{os.environ.get('PATH', '')}")
    return str(script)


#: The two documented hand-off launches.
LAUNCHES = {
    "sbatch": ["--", "sbatch", "job.sh"],
    "detached-launcher": ["--detached-launcher", "--", sys.executable, "-c", "pass"],
}


def _launch(app, how: str, name: str) -> dict:
    """`probe exec` on the login node; returns the run row it opened."""
    rc = cli.main(["exec", "--project", "p", "--experiment", "e", "--name", name, *LAUNCHES[how]])
    assert rc == 0
    return next(r for r in app.runs.values() if r["name"] == name)


def _join(app, tmp_path, monkeypatch, run: dict, rank: int, world_size: int = 2):
    """One rank of the job: its own process (own client, own outbox) whose
    `probe.init()` joins through PROBE_RUN_ID + PROBE_RUN_EPOCH, exactly as
    fluent.init does (`_attach_from_env`, then a non-zero rank sends no
    terminal status of its own)."""
    env = {
        "PROBE_RUN_ID": run["id"],
        "PROBE_RUN_EPOCH": str(run["write_epoch"]),
        "RANK": str(rank),
        "WORLD_SIZE": str(world_size),
        "LOCAL_RANK": "0",
    }
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    client = make_client(app, tmp_spool=tmp_path / f"rank{rank}-spool")
    handle = fluent._attach_from_env(client, {})
    if fluent._nonzero_global_rank() is not None:
        handle._sends_terminal_status = False
    for key in env:
        monkeypatch.delenv(key)
    handle.stop_heartbeat()  # the loop's beats are not what these tests are about
    return handle


def _now() -> str:
    """An `ended_at` inside attach's adopt window: the fake stamps a fixed
    date months away from wall-clock time."""
    from datetime import datetime

    from probe._compat import UTC

    return datetime.now(UTC).isoformat()


def _status_patches(app, run_id: str) -> list:
    return [
        json.loads(r.content).get("status")
        for r in app.requests
        if r.method == "PATCH"
        and r.url.path == f"/v1/runs/{run_id}"
        and r.content
        and json.loads(r.content).get("status") not in (None, "running")
    ]


def _releases(app, run_id: str) -> list:
    return [
        json.loads(r.content)["exit_status"]
        for r in app.requests
        if r.method == "POST"
        and r.url.path.startswith(f"/v1/runs/{run_id}/writers/")
        and r.url.path.endswith("/release")
    ]


@pytest.mark.parametrize("how", sorted(LAUNCHES))
def test_a_hand_off_asks_for_leases_and_the_launcher_holds_none(cli_client, sbatch, how):
    """The create asks for the lease rules with NO writer: the submitter is
    gone before the job starts, so a lease of its own would either end the run
    `completed` at submit time (its release) or expire into a false
    `writer_lost` (never released)."""
    app = cli_client
    run = _launch(app, how, f"queued-{how}")

    create = [
        json.loads(r.content)
        for r in app.requests
        if r.method == "POST" and r.url.path.endswith("/runs") and b"queued" in r.content
    ]
    (body,) = create
    assert body.get("awaiting_attach") is True
    assert body.get("liveness_protocol") == "leases"
    assert "writer" not in body, "the submitter holds no lease"
    assert run["status"] == "created" and run["liveness_protocol"] == "leases"
    assert not app.leases.get(run["id"]), "no lease before a rank attaches"
    assert not [r for r in app.requests if "/writers/" in r.url.path]


@pytest.mark.parametrize("how", sorted(LAUNCHES))
def test_two_attached_ranks_hold_leases_and_a_clean_finish_closes_completed(
    cli_client, sbatch, tmp_path, monkeypatch, how
):
    app = cli_client
    run = _launch(app, how, f"clean-{how}")
    rank0 = _join(app, tmp_path, monkeypatch, run, 0)
    rank1 = _join(app, tmp_path, monkeypatch, run, 1)

    leases = app.leases[run["id"]]
    assert {w["session_id"] for w in leases.values()} == {rank0.session_id, rank1.session_id}
    assert sorted((w["role"], w["rank"]) for w in leases.values()) == [("owner", 0), ("rank", 1)]
    assert all(w["world_size"] == 2 for w in leases.values())
    assert rank0._lease_protocol == rank1._lease_protocol == "leases", "the attach beat said so"
    assert app.runs[run["id"]]["status"] == "running"

    rank1.finish()
    assert app.runs[run["id"]]["status"] == "running", "rank 0 is still live"
    rank0.finish()

    assert app.runs[run["id"]]["status"] == "completed"
    assert _status_patches(app, run["id"]) == [], "the leases decided it, not a status write"
    assert sorted(_releases(app, run["id"])) == ["completed", "completed"]


@pytest.mark.parametrize(
    "ending",
    [
        # What each rank's own SIGTERM close sends since #2119 (scancel and a
        # preemption alike): `failed`, marked preempted.
        "failed",
        # A Ctrl-C the job turns into KeyboardInterrupt on every rank.
        "canceled",
    ],
)
def test_both_ranks_release_and_the_leases_close_the_run_on_the_last(
    cli_client, sbatch, tmp_path, monkeypatch, ending
):
    """Each rank records how it ended and releases its lease with it: the run
    closes on the LAST release, by the lease rules, with no status write and
    no wait for the reaper. Rank 0 (the owner) finishing first does not close
    it while rank 1 is still live."""
    app = cli_client
    run = _launch(app, "sbatch", f"ended-{ending}")
    rank0 = _join(app, tmp_path, monkeypatch, run, 0)
    rank1 = _join(app, tmp_path, monkeypatch, run, 1)

    rank0.finish(ending)
    assert app.runs[run["id"]]["status"] == "running", "rank 1's lease is still live"
    rank1.finish(ending)

    assert app.runs[run["id"]]["status"] == ending
    assert _status_patches(app, run["id"]) == []
    assert sorted(_releases(app, run["id"])) == [ending, ending]


_RANK_SCRIPT = """
import json, os, sys, time
import probe

run = probe.init()
for step in range(20):
    probe.log({f"rank{sys.argv[1]}/loss": 1.0 / (step + 1)}, step=step)
print("CHILD " + json.dumps({"event": "ready", "run_id": run.id}), flush=True)
if sys.argv[2] == "finish":
    # Every rank is in before any finishes, as a DDP job's first collective
    # guarantees.
    while not os.path.exists(sys.argv[3]):
        time.sleep(0.02)
    probe.finish()
    sys.exit(0)
while True:
    time.sleep(0.05)
"""


def _stop_workers_of(outbox: str) -> None:
    """Stop the detached outbox workers this test's children left (found by
    their outbox), as test_sigterm_flush.py does."""
    for pid in os.listdir("/proc"):
        if not pid.isdigit():
            continue
        try:
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                argv = f.read().split(b"\0")
        except OSError:
            continue
        if b"probe.sdk.outbox_worker" in argv and any(outbox.encode() in a for a in argv):
            try:
                os.kill(int(pid), signal.SIGKILL)
            except OSError:
                pass


def _wait_ready(proc, timeout: float = 60.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        line = proc.stdout.readline()
        if not line:
            break
        if line.startswith("CHILD "):
            return
    proc.kill()
    raise AssertionError(f"the rank never got ready: {proc.communicate()[1][-3000:]}")


def _job(url: str, run: dict, outbox: str, mode: str) -> list:
    """One attempt of the 2-rank job: real processes whose `probe.init()` joins
    through the environment `sbatch --export=ALL` carries into every attempt
    (the same PROBE_RUN_ID and PROBE_RUN_EPOCH, requeue included)."""
    from tests.served_fake_app import child_env

    procs = []
    for rank in (0, 1):
        env = child_env(
            url,
            PROBE_RUN_ID=run["id"],
            PROBE_RUN_EPOCH=str(run["write_epoch"]),
            RANK=str(rank),
            WORLD_SIZE="2",
            LOCAL_RANK="0",
            PROBE_HW="0",
            PROBE_EPHEMERAL="0",
            PROBE_SIGTERM_FLUSH_SECONDS="10",
            PROBE_OUTBOX_DIR=outbox,
        )
        procs.append(
            subprocess.Popen(
                [sys.executable, "-c", _RANK_SCRIPT, str(rank), mode, outbox + ".go"],
                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
        )
    for proc in procs:
        _wait_ready(proc)
    return procs


def _scancel(procs) -> list:
    """What `scancel` does to the job's processes: SIGTERM to every rank."""
    for proc in procs:
        proc.send_signal(signal.SIGTERM)
    return [proc.communicate(timeout=30) for proc in procs]


def _preempted(row: dict) -> bool:
    marks = (row.get("summary_metrics") or row.get("summary") or {}).get("probe_finish") or {}
    return marks.get("reason") == "preempted" and marks.get("signal") == "SIGTERM"


@pytest.fixture
def served(cli_client, tmp_path):
    from tests.served_fake_app import serve

    outbox = str(tmp_path / "outbox")
    procs: list = []
    with serve(cli_client) as url:
        yield url, outbox, procs
        for proc in procs:
            if proc.poll() is None:
                proc.kill()
    _stop_workers_of(outbox)


def test_scancel_sigterms_both_rank_processes_and_the_leases_close_the_run_failed(
    cli_client, sbatch, served
):
    """The scancel path end to end, with REAL rank processes: `probe exec --
    sbatch` opens the hand-off, two processes join through PROBE_RUN_ID as
    ranks 0 and 1 of a 2-rank job, and both get SIGTERM, as `scancel` sends
    it. Since #2119 each one delivers its queue, releases its lease `failed`
    (preempted) and dies of SIGTERM; the leases then close the run `failed`,
    with no status write and no reaper. Slurm cannot tell a user's `scancel`
    from a preemption through SIGTERM alone, so `failed` is the verdict."""
    app = cli_client
    url, outbox, procs = served
    run = _launch(app, "sbatch", "scancel-procs")
    procs += _job(url, run, outbox, "loop")
    ends = _scancel(procs)

    assert [proc.returncode for proc in procs] == [-signal.SIGTERM] * 2, [e[1][-2000:] for e in ends]
    row = app.runs[run["id"]]
    assert row["liveness_protocol"] == "leases"
    assert row["status"] == "failed", (row["status"], [e[1][-2000:] for e in ends])
    leases = list(app.leases[run["id"]].values())
    assert sorted((w["role"], w["exit_status"]) for w in leases) == [
        ("owner", "failed"), ("rank", "failed")
    ], leases
    assert _status_patches(app, run["id"]) == [], "the leases decided it, not a status write"
    assert _preempted(row), row.get("summary_metrics")


def test_a_requeue_after_the_sigterm_close_continues_the_preempted_run(
    cli_client, sbatch, served
):
    """`scontrol requeue` ends attempt 1 with SIGTERM, which since #2119 closes
    the run `failed`, marked preempted; Slurm then starts the job again with
    the SAME environment. Attach refused every `failed`, so the requeued
    attempt's `probe.init()` raised. A `failed` the SIGTERM close wrote is a
    scheduler's stop, not a verdict anyone chose: attach reopens it (fresh
    epoch) and the second attempt finishes the run `completed`."""
    app = cli_client
    url, outbox, procs = served
    run = _launch(app, "sbatch", "requeue-procs")
    first = _job(url, run, outbox, "loop")
    procs += first
    _scancel(first)
    assert app.runs[run["id"]]["status"] == "failed" and _preempted(app.runs[run["id"]])
    app.runs[run["id"]]["ended_at"] = _now()  # the fake's clock is fixed

    second = _job(url, run, outbox, "finish")
    procs += second
    open(outbox + ".go", "w").close()
    ends = [proc.communicate(timeout=60) for proc in second]

    assert [proc.returncode for proc in second] == [0, 0], [e[1][-2000:] for e in ends]
    row = app.runs[run["id"]]
    assert row["status"] == "completed" and int(row["write_epoch"]) == 2, row["status"]
    current = [w for w in app.leases[run["id"]].values() if int(w["write_epoch"]) == 2]
    assert sorted((w["role"], w["exit_status"]) for w in current) == [
        ("owner", "completed"), ("rank", "completed")
    ], current


@pytest.fixture
def reporter(app, monkeypatch, tmp_path):
    """The output helper's client, pointed at the fake (test_writer_gone.py)."""
    client = make_client(app, tmp_spool=tmp_path / "helper-spool")
    monkeypatch.setattr(outputs, "_recovery_client", lambda record: (client, client.journal))
    return client


def _report_gone(tmp_path, handle) -> dict:
    """What the rank's output helper sends once its rank is gone (plan 2.2)."""
    capture = outputs.OutputCapture(
        handle._client, handle.id, str(tmp_path), tee=False, launcher=False,
        writer=handle._writer_record(),
    )
    entry = tmp_path / f"rec-{handle.session_id}.json"
    entry.write_text(json.dumps(capture._record(shared_with=[])))
    return outputs.writer_gone(str(entry))


def test_ranks_killed_with_no_close_are_reported_gone_and_the_run_closes_crashed(
    cli_client, sbatch, tmp_path, monkeypatch, reporter
):
    """Ranks that end with no close of their own -- SIGKILL (Slurm's, KillWait
    after the SIGTERM), an OOM kill, or SIGTERM with
    `PROBE_SIGTERM_FLUSH_SECONDS=0` -- release nothing; each rank's output
    helper reports its writer gone. Both leases GONE, no lease live, every
    rank slot registered: `crashed` at the second report, not after the 900 s
    reaper."""
    app = cli_client
    run = _launch(app, "sbatch", "scancel-killed")
    rank0 = _join(app, tmp_path, monkeypatch, run, 0)
    rank1 = _join(app, tmp_path, monkeypatch, run, 1)

    first = _report_gone(tmp_path, rank1)
    assert first["sent"] is True and first["applied"] is False
    assert app.runs[run["id"]]["status"] == "running", "rank 0 is still live"
    second = _report_gone(tmp_path, rank0)

    assert second["sent"] is True and second["applied"] is True
    assert app.runs[run["id"]]["status"] == "crashed"
    assert all(w["gone_at"] for w in app.leases[run["id"]].values())


def test_one_rank_killed_is_a_lost_writer_and_the_worst_verdict(
    cli_client, sbatch, tmp_path, monkeypatch, reporter
):
    """A node lost mid-run: rank 1's helper reports it gone while rank 0 keeps
    writing. The run is on leases with rank 1's current-epoch lease GONE and
    rank 0's live and nobody's work-ending release yet -- the shape
    `writer_lost` pages on (app/findings/detectors.py::detect_writer_lost,
    which reads only `leases` runs). The run stays open while rank 0 works,
    and rank 0's clean finish cannot hide the lost rank: `crashed`."""
    app = cli_client
    run = _launch(app, "sbatch", "node-lost")
    rank0 = _join(app, tmp_path, monkeypatch, run, 0)
    rank1 = _join(app, tmp_path, monkeypatch, run, 1)

    outcome = _report_gone(tmp_path, rank1)

    row = app.runs[run["id"]]
    leases = app.leases[run["id"]]
    assert outcome["applied"] is False and row["status"] == "running"
    assert row["liveness_protocol"] == "leases", "writer_lost reads only leases runs"
    lost, live = leases[rank1.session_id], leases[rank0.session_id]
    assert lost["gone_at"] and lost["rank"] == 1
    assert int(lost["write_epoch"]) == int(row["write_epoch"]), "a current-epoch lease"
    assert not live["gone_at"] and not live["released_at"], "another writer is still live"

    rank0.log({"loss": 0.5}, step=1)
    rank0.finish()

    assert app.runs[run["id"]]["status"] == "crashed"
    assert _status_patches(app, run["id"]) == []


def test_an_opener_that_beats_the_hand_off_itself_stays_legacy(client, app):
    """`awaiting_attach` with the opener's own run-level heartbeat: that beat
    would flip a `leases` run on its first tick, so the create does not ask."""
    from tests.conftest import open_run

    run = open_run(client, experiment="e", name="beats", awaiting_attach=True)
    run.stop_heartbeat()
    create = [r for r in app.requests if r.method == "POST" and r.url.path.endswith("/runs")][-1]
    assert "liveness_protocol" not in json.loads(create.content)
    assert app.runs[run.id]["liveness_protocol"] is None


def test_a_server_without_leases_gets_the_hand_off_it_always_got(cli_client, sbatch):
    app = cli_client
    app.supports_leases = False
    run = _launch(app, "sbatch", "old-server")
    create = [
        json.loads(r.content)
        for r in app.requests
        if r.method == "POST" and r.url.path.endswith("/runs") and b"old-server" in r.content
    ]
    assert "liveness_protocol" not in create[0]
    assert run["liveness_protocol"] is None and run["status"] == "created"


def test_a_requeue_after_the_kill_continues_the_same_run(
    cli_client, sbatch, tmp_path, monkeypatch, reporter
):
    """A requeue after attempt 1 was killed with no close (both helpers report
    their rank gone, so the leases close the run `crashed` in seconds); Slurm
    starts the job again with the SAME environment -- PROBE_RUN_ID and
    PROBE_RUN_EPOCH=1. On a legacy run nothing closed it, so the requeue found
    it `running`; on leases it finds `crashed`, a verdict nobody chose, and
    must reopen it in place (plan: "requeue right after kill -> resumes"; the
    crash notice waits `crash_notice_requeue_grace_seconds` for exactly this)
    instead of refusing `probe.init()`. The SIGTERM-close requeue is
    `test_a_requeue_after_the_sigterm_close_continues_the_preempted_run`."""
    app = cli_client
    run = _launch(app, "sbatch", "requeued")
    first = [_join(app, tmp_path / "a", monkeypatch, run, r) for r in (0, 1)]
    for handle in reversed(first):
        _report_gone(tmp_path, handle)
    assert app.runs[run["id"]]["status"] == "crashed"
    app.runs[run["id"]]["ended_at"] = _now()  # the fake's clock is fixed

    second = [_join(app, tmp_path / "b", monkeypatch, run, r) for r in (0, 1)]

    row = app.runs[run["id"]]
    assert row["status"] == "running" and int(row["write_epoch"]) == 2
    assert {h.id for h in second} == {run["id"]}, "the requeue writes the same run"
    assert {h.write_epoch for h in second} == {2}
    current = [w for w in app.leases[run["id"]].values() if int(w["write_epoch"]) == 2]
    assert sorted((w["role"], w["rank"]) for w in current) == [("owner", 0), ("rank", 1)]

    for handle in reversed(second):
        handle.finish()
    assert app.runs[run["id"]]["status"] == "completed", "attempt 1's GONE leases are the old epoch's"


@pytest.fixture
def rank_lease_exits(monkeypatch):
    """`_rank_lease.hold` registers an atexit release: keep it inside the test."""
    from probe.integrations import _rank_lease

    registered: list = []
    monkeypatch.setattr(_rank_lease, "_at_exit", registered.append)
    yield _rank_lease
    for lease in list(_rank_lease._LEASES.values()):
        lease.release()
    _rank_lease._LEASES.clear()


def test_a_trainer_integrations_rank_lease_joins_a_hand_off_on_leases(
    cli_client, sbatch, tmp_path, monkeypatch, rank_lease_exits
):
    """Lightning's `ProbeLogger` / the HF callback (#2091): rank 0 joins through
    PROBE_RUN_ID and broadcasts (run id, epoch); every other rank holds a
    lease-only `rank` lease (`_rank_lease.hold`). On a hand-off that is now a
    lease on a `leases` run, so the leases close it."""
    app = cli_client
    run = _launch(app, "sbatch", "lightning")
    rank0 = _join(app, tmp_path, monkeypatch, run, 0)
    lease = rank_lease_exits.hold(
        run["id"], rank0.write_epoch, rank=1, client=make_client(app, tmp_spool=tmp_path / "r1")
    )

    held = app.leases[run["id"]][lease.session_id]
    assert (held["role"], held["rank"]) == ("rank", 1)
    assert lease.run._lease_protocol == "leases"

    lease.release()
    assert app.runs[run["id"]]["status"] == "running", "rank 0 is still live"
    rank0.finish()
    assert app.runs[run["id"]]["status"] == "completed"
    assert _status_patches(app, run["id"]) == []
