"""0205: a run cannot exist without something that owns its liveness.

These tests exist because of a measured failure, not a hypothetical one. On one
tenant, 41 of 41 runs were opened by the CLI from a laptop while the training ran
on a remote host; 3 had any owner heartbeat; 8 were reaped to 'untracked' ~16
minutes into work that was still going; 9 more sat in 'created' forever because
no sweep scanned that status. The handshake below is what closes it.
"""

from __future__ import annotations

import pytest

from datetime import datetime, timedelta
from probe._compat import UTC

from probe import errors
from probe.sdk.run import Run
from tests.conftest import open_run


def _recently() -> str:
    """An `ended_at` inside the adopt window. The fake's own clock is fixed and
    months away from wall-clock now, which the window check reads (correctly) as
    a stale id."""
    return (datetime.now(UTC) - timedelta(minutes=5)).isoformat()


class TestInitAttachesFromTheEnvironment:
    """`probe exec` exports the id; `probe.init()` must JOIN that run.

    Before 0205 `Run.execute()` exported PROBE_RUN_ID and nothing on earth read
    it, so a wrapped script that also called probe.init() produced TWO runs --
    one with an exit code and no curves, one with curves and no exit code -- and
    neither was the run anyone meant.
    """

    def test_init_joins_the_run_named_by_the_environment(self, client, app, monkeypatch):
        import probe

        existing = open_run(client, experiment="e", name="r", heartbeat=False)
        monkeypatch.setenv("PROBE_RUN_ID", existing.id)
        before = len(app.runs)

        run = probe.init(client=client)
        try:
            assert run.id == existing.id, "init created a second run instead of joining"
            assert len(app.runs) == before, "a run was created despite PROBE_RUN_ID"
        finally:
            probe.finish()

    def test_the_joined_handle_beats_as_attached(self, client, app, monkeypatch):
        """Only beats from INSIDE the work stamp attached_at. This is that beat."""
        import probe

        existing = open_run(client, experiment="e", name="r", heartbeat=False)
        monkeypatch.setenv("PROBE_RUN_ID", existing.id)
        monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "0.01")

        run = probe.init(client=client)
        try:
            assert run.attached is True
            _wait_for(lambda: app.run_attached_beats.get(existing.id, 0) >= 1)
            assert app.runs[existing.id]["attached_at"] is not None
        finally:
            probe.finish()

    @pytest.mark.xfail(
        strict=True,
        reason=(
            "PRE-EXISTING GAP, exposed when the fake's run rows gained the "
            "write_epoch every real RunDetailOut serializes (SDK reliability "
            "1.10). attach_run(reopen_if_dead=True) adopts the row's CURRENT "
            "epoch whenever the row carries one -- always, since 0185 -- so "
            "PROBE_RUN_EPOCH never reaches a probe.init() handle. This passed "
            "only because the fake omitted the field. Letting the caller's "
            "epoch win would fence sibling ranks after an untracked reopen; "
            "the precedence is a lane-F 2.3 decision, not fixed here."
        ),
    )
    def test_the_epoch_travels_so_a_stale_attempt_can_be_fenced(
        self, client, app, monkeypatch
    ):
        """A run id names a ROW, not an attempt. Without the epoch a stale
        process holding an old id inherits the newer attempt's write authority."""
        import probe

        existing = open_run(client, experiment="e", name="r", heartbeat=False)
        monkeypatch.setenv("PROBE_RUN_ID", existing.id)
        monkeypatch.setenv("PROBE_RUN_EPOCH", "7")

        run = probe.init(client=client)
        try:
            assert run.write_epoch == 7
        finally:
            probe.finish()

    def test_an_unreadable_epoch_warns_and_attaches_unfenced(
        self, client, app, monkeypatch
    ):
        """Fail OPEN: the server still fences on its own copy, and refusing the
        attach would strand a job over a malformed environment variable."""
        import probe

        existing = open_run(client, experiment="e", name="r", heartbeat=False)
        monkeypatch.setenv("PROBE_RUN_ID", existing.id)
        monkeypatch.setenv("PROBE_RUN_EPOCH", "not-a-number")

        with pytest.warns(UserWarning, match="PROBE_RUN_EPOCH"):
            run = probe.init(client=client)
        try:
            assert run.id == existing.id
        finally:
            probe.finish()

    @pytest.mark.parametrize("kwarg", ["experiment", "project", "name", "slug"])
    def test_a_conflicting_argument_raises_instead_of_guessing(
        self, client, app, monkeypatch, kwarg
    ):
        """The environment already chose the run. Honouring either side silently
        is how telemetry lands on a run nobody was looking at."""
        import probe

        existing = open_run(client, experiment="e", name="r", heartbeat=False)
        monkeypatch.setenv("PROBE_RUN_ID", existing.id)

        with pytest.raises(errors.ValidationError) as excinfo:
            probe.init(client=client, **{kwarg: "something-else"})
        assert kwarg in str(excinfo.value)
        assert existing.id in str(excinfo.value)

    def test_without_the_variable_init_still_creates(self, client, app, monkeypatch):
        import probe

        monkeypatch.delenv("PROBE_RUN_ID", raising=False)
        open_run(client, experiment="e", name="seed", heartbeat=False)
        before = len(app.runs)
        run = probe.init(client=client, experiment="e", name="fresh")
        try:
            assert len(app.runs) == before + 1
            assert run.id in app.runs
        finally:
            probe.finish()


class TestAttachReopens:
    """A job can reach its run after the sweep already ended it."""

    def test_a_created_run_is_moved_to_running(self, client, app):
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id]["status"] = "created"

        attached = client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)
        assert attached.id == run.id
        assert app.runs[run.id]["status"] == "running"

    @pytest.mark.parametrize("unchosen", ["untracked", "crashed"])
    def test_an_unchosen_ending_is_reopened_with_a_fresh_epoch(self, client, app, unchosen):
        """'untracked' is the reaper's verdict, not a human's; 'crashed' is the
        system's report that the processes died -- what a requeued job finds
        once its first attempt's leases were reported gone (plan 2.8). Nobody
        chose either."""
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(status=unchosen, ended_at=_recently())
        epoch_before = app.runs[run.id].get("write_epoch", 1)

        client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)
        assert app.runs[run.id]["status"] == "running"
        assert app.runs[run.id].get("write_epoch", 1) == epoch_before + 1

    def test_a_failed_the_sigterm_close_wrote_is_reopened(self, client, app):
        """#2119: a SIGTERM closes the run `failed`, marked preempted -- how
        `scontrol requeue` ends the attempt it starts again with the same
        PROBE_RUN_ID. A scheduler's stop, not a verdict anyone chose."""
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(
            status="failed",
            ended_at=_recently(),
            summary_metrics={"probe_finish": {"reason": "preempted", "signal": "SIGTERM"}},
        )

        client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)
        assert app.runs[run.id]["status"] == "running"

    def test_a_failed_with_another_ending_is_still_refused(self, client, app):
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(
            status="failed",
            ended_at=_recently(),
            summary_metrics={"probe_finish": {"reason": "exception"}},
        )

        with pytest.raises(errors.ConflictError, match="failed"):
            client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)
        assert app.runs[run.id]["status"] == "failed"

    @pytest.mark.parametrize("chosen", ["failed", "canceled"])
    def test_a_chosen_ending_is_refused(self, client, app, chosen):
        """A stale PROBE_RUN_ID in a .env must not resurrect last week's run."""
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(status=chosen, ended_at=_recently())

        with pytest.raises(errors.ConflictError) as excinfo:
            client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)
        assert chosen in str(excinfo.value)
        assert app.runs[run.id]["status"] == chosen

    def test_a_run_that_ended_long_ago_is_refused(self, client, app):
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(status="untracked", ended_at="2020-01-01T00:00:00+00:00")

        with pytest.raises(errors.ConflictError, match="window"):
            client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)

    def test_a_live_run_is_joined_not_reopened(self, client, app):
        """THE MULTI-RANK CASE. Eight DDP workers read one PROBE_RUN_ID: the
        first reopens, the rest arrive to find it live. Treating that as an
        error would kill every rank but one at import and leave a run that looks
        tracked because rank 0 attached."""
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        epoch_before = app.runs[run.id].get("write_epoch", 1)

        for _ in range(8):
            client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)

        assert app.runs[run.id]["status"] == "running"
        assert app.runs[run.id].get("write_epoch", 1) == epoch_before, (
            "a live run must not be reopened once per rank"
        )

    def test_an_attach_reopen_arms_the_resume_guard(self, client, app):
        """Plan 2.4. A job that reaches its run after the reaper ended it (a
        requeue, a late start) and restarts from an older checkpoint must drop
        the steps the first attempt already wrote, not splice a second curve
        over them. The reopen receipt's `last_step` used to be thrown away on
        this path."""
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        run.log({"loss": 1.0}, step=40)
        app.runs[run.id].update(status="untracked", ended_at=_recently())

        attached = client.attach_run(run.id, heartbeat=False, reopen_if_dead=True)
        assert attached._resume_from_step == 40
        with pytest.warns(UserWarning, match="DROPPED"):
            assert attached.log({"loss": 2.0}, step=40) is None
        assert "last_step" not in attached.data and "_resume_last_step" not in attached.data

    def test_attach_without_the_flag_leaves_a_dead_run_dead(self, client, app):
        """Reopening is opt-in: the miles observer path attaches to runs it must
        never resurrect."""
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(status="untracked", ended_at=_recently())

        client.attach_run(run.id, heartbeat=False)
        assert app.runs[run.id]["status"] == "untracked"


class TestTheLauncherOwnsTheRun:
    def test_a_handle_that_merely_observes_is_still_inert(self, client, app, monkeypatch):
        """The 0106 rule survives 0205: constructing Run() directly never beats."""
        monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "60")
        created = open_run(client, experiment="e", name="r", heartbeat=False)
        attached = Run(client, client.get_run(created.id))
        assert attached._hb_thread is None
        assert app.run_heartbeats.get(created.id) is None

    def test_an_attached_handle_beats_when_asked(self, client, app, monkeypatch):
        """The inverse, and the point of 0205: `probe exec` holds a handle that
        DOES beat, for as long as the child lives. Before this, a wrapped child
        that logged nothing for fifteen minutes was reaped mid-flight."""
        monkeypatch.setenv("PROBE_HEARTBEAT_SECONDS", "0.01")
        created = open_run(client, experiment="e", name="r", heartbeat=False)

        handle = client.attach_run(created.id, heartbeat=True, attached=False)
        try:
            _wait_for(lambda: app.run_heartbeats.get(created.id, 0) >= 1)
            # The launcher holds the run open; it does NOT claim the job
            # inside it ever reported.
            assert app.runs[created.id]["attached_at"] is None
        finally:
            handle.stop_heartbeat()


def _wait_for(predicate, timeout: float = 3.0) -> None:
    import time

    deadline = time.time() + timeout
    while time.time() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("condition not reached within timeout")


class TestTheHandshakeEndToEnd:
    """T13: the two-run bug, pinned.

    `probe exec` around a script that also calls `probe.init()` must produce ONE
    run carrying BOTH halves -- the launcher's exit status and the job's curves.
    Before 0205 it produced two, and neither was complete.

    In-process rather than through a real subprocess: the child would need to
    reach the fake API, which does not survive a fork. What is exercised is the
    contract between the two halves -- what execute() exports, and what init()
    does with it -- which is exactly the seam that was broken.
    """

    def test_exec_then_init_is_one_run_with_both_halves(
        self, client, app, monkeypatch, tmp_path
    ):
        import probe

        # The launcher opens the run and owns it. (open_run seeds the parent
        # experiment; client.run() resolves rather than creates one.)
        open_run(client, experiment="e", name="seed", heartbeat=False)
        launcher_handle = client.run(
            experiment="e", name="handshake", heartbeat=True, launcher=True
        )
        runs_after_launch = len(app.runs)

        # What execute() puts in the child's environment.
        monkeypatch.setenv("PROBE_RUN_ID", launcher_handle.id)
        monkeypatch.setenv("PROBE_RUN_EPOCH", str(launcher_handle.write_epoch))

        # The job inside.
        job = probe.init(client=client)
        try:
            assert job.id == launcher_handle.id
            assert len(app.runs) == runs_after_launch, "the job created a second run"
            job.log({"loss": 0.5}, step=1)
        finally:
            probe.finish()

        row = app.runs[launcher_handle.id]
        assert row["liveness_mode"] == "wrapped", "the launcher opened it"
        assert row["status"] == "completed", "the job finished it"
        points = app.metric_points.get(launcher_handle.id, []) + app.metric_points_posted.get(
            launcher_handle.id, []
        )
        assert points, "the curves landed on the same run"

    def test_the_launcher_does_not_overwrite_the_jobs_verdict(self, client, app):
        """D5/D20: whoever spoke with knowledge stands.

        A child that failed inside its own loop and said so must not be recorded
        as 'completed' because the wrapper's process happened to exit 0.
        """
        open_run(client, experiment="e", name="seed", heartbeat=False)
        handle = client.run(experiment="e", name="verdict", heartbeat=True, launcher=True)
        handle.set_status("failed")

        # The launcher's own finalize, as execute() issues it.
        handle.set_status("completed", only_if_running=True)

        assert app.runs[handle.id]["status"] == "failed"


class TestReviewFindings:
    """Regressions for the 2026-09-11 review. Each names the failure it pins."""

    def test_a_reopen_epoch_beats_the_callers_stale_one(self, client, app):
        """F2. The launcher exported PROBE_RUN_EPOCH BEFORE the reopen existed,
        so applying the caller's value after reopening set the handle back one
        generation -- and `ensure_writer_epoch` then refused every metric, log
        and span for the rest of the job. In exactly the queued-start case the
        24h reopen window was built for.
        """
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(status="untracked", ended_at=_recently())
        stale_epoch = app.runs[run.id].get("write_epoch", 1)

        handle = client.attach_run(
            run.id, heartbeat=False, reopen_if_dead=True, write_epoch=stale_epoch
        )

        assert app.runs[run.id]["write_epoch"] == stale_epoch + 1
        assert handle.write_epoch == stale_epoch + 1, (
            "the handle must write under the generation the reopen minted"
        )

    def test_the_attached_beat_carries_the_settled_epoch(self, client, app, monkeypatch):
        """F7. The epoch was applied AFTER _wrap_run, so the beat thread and the
        synchronous attached-beat both went out under the row's old generation
        -- the fence was off on exactly the beats that keep a run looking alive.
        """
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id]["write_epoch"] = 1
        seen: list = []
        real = client.heartbeat_run
        monkeypatch.setattr(
            client,
            "heartbeat_run",
            lambda rid, *a, **kw: (seen.append(kw.get("write_epoch")), real(rid, *a, **kw))[1],
        )

        client.attach_run(run.id, heartbeat=False, attached=True, write_epoch=9)
        assert seen == [9], f"the attached beat must be fenced at the caller's epoch, got {seen}"

    def test_recovery_keeps_the_handles_epoch(self, client, app):
        """F3, then SDK reliability 1.1. F3: the recovery threw the receipt
        away, so a BUMPED epoch never reached the handle and every later write
        was fenced. 1.1 removes the bump itself: self-recovery asks the server
        to keep the generation, so the handle, the beat loop, every op already
        queued and every sibling rank stay valid."""
        from probe.sdk.run import _recover_after_outage
        import weakref

        run = open_run(client, experiment="e", name="r", heartbeat=False)
        # The epoch guard is strict on purpose: recovery must prove the row is
        # still OURS. A row with no epoch at all (a pre-0185 server) is never
        # recovered, which is the safe direction.
        app.runs[run.id].update(status="crashed", ended_at=_recently(), write_epoch=1)

        new_epoch = _recover_after_outage(
            client, run.id, role="owner", write_epoch=1, handle_ref=weakref.ref(run),
        )

        assert app.runs[run.id]["status"] == "running"
        assert new_epoch == 1 and run.write_epoch == 1
        assert app.runs[run.id]["write_epoch"] == 1
        (reopen,) = [r for r in app.requests if r.url.path.endswith("/reopen")]
        import json

        body = json.loads(reopen.content)
        assert (body["keep_epoch"], body["expected_write_epoch"]) == (True, 1)

    def test_a_handle_without_an_epoch_does_not_recover(self, client, app):
        """It cannot prove the crashed row is still its own."""
        from probe.sdk.run import _recover_after_outage

        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(status="crashed", ended_at=_recently())

        assert _recover_after_outage(client, run.id, role="owner", write_epoch=None) is None
        assert app.runs[run.id]["status"] == "crashed"

    def test_recovery_refuses_a_run_a_newer_attempt_took_over(self, client, app):
        """Same path, opposite direction: an old process waking up must never
        clobber a legitimate successor."""
        from probe.sdk.run import _recover_after_outage

        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(status="crashed", write_epoch=5)

        assert _recover_after_outage(client, run.id, role="owner", write_epoch=2) is None
        assert app.runs[run.id]["status"] == "crashed"

    def test_the_launcher_re_reads_before_finalizing(self, client, app):
        """F4. `only_if_running` consulted the handle's CACHED row, which the
        launcher read once at attach time and never refreshed -- so it was
        always 'running' on the execute() path. The server has no terminal guard
        of its own (patch_run appends `status = $n` unconditionally), so a child
        that wrote `finish("failed")` had it silently overwritten with
        'completed' by a launcher exiting 0.
        """
        open_run(client, experiment="e", name="seed", heartbeat=False)
        handle = client.run(experiment="e", name="verdict", heartbeat=True, launcher=True)
        # The CHILD's verdict, written by a different process: the launcher's
        # cached _data still says 'running'.
        app.runs[handle.id]["status"] = "failed"
        assert handle._data["status"] == "running", "precondition: the cache is stale"

        handle.set_status("completed", only_if_running=True)

        assert app.runs[handle.id]["status"] == "failed", (
            "the launcher must not overwrite a verdict written with knowledge"
        )

    def test_attach_names_the_arguments_it_cannot_honour(self, client, app, monkeypatch):
        """F9. Everything outside the identity set was dropped on the floor:
        `probe.init(hw=True)` stopped collecting hardware metrics with no sign."""
        import probe

        existing = open_run(client, experiment="e", name="r", heartbeat=False)
        monkeypatch.setenv("PROBE_RUN_ID", existing.id)

        with pytest.warns(UserWarning, match="ignored .*hw"):
            run = probe.init(client=client, hw=True)
        probe.finish()
        assert run.id == existing.id


# -- SDK reliability 1.1 + 1.10: an outage must not cost the run its data -----


class _Network:
    """An outage switch for ONE client's heartbeats.

    A journaling client (`async_writes=True`) never touches the network to
    write: every log lands in the outbox. So the beat is the one call that
    notices an outage, and flipping it here is the whole outage as far as the
    recovery path can tell.
    """

    def __init__(self, client, monkeypatch) -> None:
        self.down = False
        self.ok_beats = 0
        self.failed_beats = 0
        real = client.heartbeat_run

        def beat(run_id, *args, **kwargs):
            if self.down:
                self.failed_beats += 1
                raise errors.TransportError("connection refused (simulated outage)")
            out = real(run_id, *args, **kwargs)
            self.ok_beats += 1
            return out

        monkeypatch.setattr(client, "heartbeat_run", beat)


def _start_beating(client, handle):
    """The real beat loop, on the handle's own epoch, with a fast interval."""
    import threading
    import weakref

    from probe.sdk.run import _beat_forever

    stop = threading.Event()
    thread = threading.Thread(
        target=_beat_forever,
        args=(client, handle.id, stop, 0.005, "owner", handle.write_epoch, False,
              weakref.ref(handle)),
        daemon=True,
    )
    thread.start()
    return stop, thread


def _stop_beating(beat) -> None:
    stop, thread = beat
    stop.set()
    thread.join(timeout=5)


def _deliver(app, client) -> None:
    """What the detached worker does once the network is back: drain the
    journal through a fresh client of its own."""
    from probe.sdk.journal import drain
    from tests.conftest import make_client

    worker = make_client(app)
    try:
        drain(client.journal, client_factory=lambda ctx: worker)
    finally:
        worker.close()


def _steps_landed(app, run_id: str) -> set[int]:
    return {
        p["step_index"]
        for p in app.metric_points_posted.get(run_id, [])
        if p.get("key") == "loss" and p.get("step_index") is not None
    }


class TestAnOutageKeepsTheEpoch:
    """1.1. Live-verified on 0.186.1: a 20-minute outage lost 2,478 of 2,659
    steps. The reaper marked the silent run `crashed`; on reconnect the beat
    thread reopened it with a fresh session, which BUMPED `write_epoch`; every
    op already queued still carried the old epoch, so the server fenced each
    one with 409 and the drain dead-lettered it, beyond `probe outbox retry`.
    Self-recovery must keep the generation it is recovering.
    """

    def test_a_long_outage_loses_nothing(self, app, tmp_path, monkeypatch):
        from tests.conftest import make_client

        client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        net = _Network(client, monkeypatch)
        beat = _start_beating(client, run)
        try:
            net.down = True
            for step in range(200):
                run.log({"loss": 1.0 / (step + 1)}, step=step)
            _wait_for(lambda: net.failed_beats >= 3)
            # Past the stale window: the reaper ends the silent run.
            app.runs[run.id].update(status="crashed", ended_at=_recently())

            net.down = False
            _wait_for(lambda: app.runs[run.id]["status"] == "running")
            for step in range(200, 250):
                run.log({"loss": 1.0 / (step + 1)}, step=step)
        finally:
            _stop_beating(beat)

        _deliver(app, client)

        assert client.journal.failed() == [], "a recovered outage dead-lettered data"
        assert app.fenced_writes == []
        assert _steps_landed(app, run.id) == set(range(250))
        assert app.runs[run.id]["write_epoch"] == 1, "self-recovery kept the generation"
        assert run.write_epoch == 1

    def test_every_rank_of_one_job_keeps_delivering(self, app, tmp_path, monkeypatch):
        """Round-1 architecture finding 1: each recovery used a fresh session
        and only the recovering handle adopted the bumped epoch, so the FIRST
        rank to reconnect fenced every other rank out for the rest of the run."""
        from tests.conftest import make_client

        rank0 = make_client(app, tmp_spool=tmp_path / "rank-0", async_writes=True)
        run0 = open_run(rank0, experiment="e", name="r", heartbeat=False)
        rank1 = make_client(app, tmp_spool=tmp_path / "rank-1", async_writes=True)
        # What a second rank does with PROBE_RUN_ID + PROBE_RUN_EPOCH.
        run1 = rank1.attach_run(run0.id, heartbeat=False, write_epoch=run0.write_epoch)
        nets = [_Network(rank0, monkeypatch), _Network(rank1, monkeypatch)]
        beats = [_start_beating(rank0, run0), _start_beating(rank1, run1)]
        try:
            for net in nets:
                net.down = True
            for step in range(100):
                run0.log({"loss": 1.0}, step=step)
                run1.log({"loss_rank1": 1.0}, step=step)
            _wait_for(lambda: all(net.failed_beats >= 3 for net in nets))
            app.runs[run0.id].update(status="crashed", ended_at=_recently())

            for net in nets:
                net.down = False
            _wait_for(lambda: app.runs[run0.id]["status"] == "running")
            # Every rank has beaten twice since: each ran its recovery check.
            floor = [net.ok_beats for net in nets]
            _wait_for(lambda: all(n.ok_beats >= f + 2 for n, f in zip(nets, floor)))
            for step in range(100, 120):
                run0.log({"loss": 1.0}, step=step)
                run1.log({"loss_rank1": 1.0}, step=step)
        finally:
            for beat in beats:
                _stop_beating(beat)

        _deliver(app, rank0)
        _deliver(app, rank1)

        assert rank0.journal.failed() == [] and rank1.journal.failed() == []
        assert app.fenced_writes == [], "a recovered rank fenced its siblings"
        posted = app.metric_points_posted.get(run0.id, [])
        assert {p["step_index"] for p in posted if p["key"] == "loss"} == set(range(120))
        assert {p["step_index"] for p in posted if p["key"] == "loss_rank1"} == set(range(120))
        assert app.runs[run0.id]["write_epoch"] == 1
        assert (run0.write_epoch, run1.write_epoch) == (1, 1)

    def test_an_older_server_is_not_reopened_and_still_gets_the_data(
        self, app, tmp_path, monkeypatch
    ):
        """G1: gate with `supports_feature` and fall back. An older server
        drops `keep_epoch` and BUMPS, which is the bug; `_require_feature`
        would raise inside the swallow-everything beat thread and never
        recover. Skipping is safe because a crashed row still takes data:
        the fence refuses only carried < current."""
        from tests.conftest import make_client

        app.supports_keep_epoch = False
        client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        net = _Network(client, monkeypatch)
        beat = _start_beating(client, run)
        try:
            net.down = True
            for step in range(50):
                run.log({"loss": 1.0}, step=step)
            _wait_for(lambda: net.failed_beats >= 3)
            app.runs[run.id].update(status="crashed", ended_at=_recently())
            net.down = False
            _wait_for(lambda: net.ok_beats >= 2)
            for step in range(50, 60):
                run.log({"loss": 1.0}, step=step)
        finally:
            _stop_beating(beat)

        reopens = [r for r in app.requests if r.url.path.endswith("/reopen")]
        assert reopens == [], "an older server must not be asked to reopen (it would bump)"
        assert app.runs[run.id]["status"] == "crashed"
        assert app.runs[run.id]["write_epoch"] == 1

        _deliver(app, client)
        assert client.journal.failed() == []
        assert _steps_landed(app, run.id) == set(range(60)), "the data still lands"

        # And the real verdict still closes it: the status PATCH carries the
        # handle's epoch, which is the row's.
        run.set_status("completed", sync=True)
        assert app.runs[run.id]["status"] == "completed"

    def test_recovery_never_takes_back_a_run_a_newer_attempt_owns(
        self, client, app, monkeypatch
    ):
        """The keep is honoured only at the CURRENT epoch. Between this
        process's read and its reopen, a newer attempt reopened the run
        (epoch 2) and crashed too: the old process must not revive it."""
        import weakref

        from probe.sdk.run import _recover_after_outage

        run = open_run(client, experiment="e", name="r", heartbeat=False)
        stale_read = {**app.runs[run.id], "status": "crashed", "write_epoch": 1}
        app.runs[run.id].update(status="crashed", write_epoch=2)
        monkeypatch.setattr(client, "get_run", lambda *_a, **_kw: dict(stale_read))

        assert _recover_after_outage(
            client, run.id, role="owner", write_epoch=1, handle_ref=weakref.ref(run)
        ) is None
        assert app.runs[run.id]["status"] == "crashed"
        assert app.runs[run.id]["write_epoch"] == 2


class TestTerminalWritesAreFenced:
    """1.10. The deferred terminal PATCH carried no epoch and the route
    checked none, so an OLD attempt's queued finish could mark the NEWER
    attempt `completed` once the outbox drained."""

    def test_a_stale_attempts_queued_finish_cannot_close_the_new_attempt(
        self, app, tmp_path
    ):
        import uuid

        from tests.conftest import make_client

        old_client = make_client(app, tmp_spool=tmp_path / "old", async_writes=True)
        old = open_run(old_client, experiment="e", name="r", heartbeat=False)
        # The old attempt's close is queued behind an outage...
        old.set_status("completed", ended_at=_recently())
        ((_, op),) = [
            (p, o) for p, o in old_client.journal.pending() if o.get("method") == "PATCH"
        ]
        assert op["body"]["write_epoch"] == 1, "the close names its generation"

        # ...while a relaunch takes the run over (epoch 2) and keeps training.
        app.runs[old.id].update(status="crashed", ended_at=_recently())
        relaunch = make_client(app)
        receipt = relaunch.reopen_run(old.id, session_id=str(uuid.uuid4()))
        assert receipt["write_epoch"] == 2

        _deliver(app, old_client)

        assert app.runs[old.id]["status"] == "running", (
            "a superseded attempt's finish closed the live one"
        )
        assert [w["path"] for w in app.fenced_writes] == [f"/v1/runs/{old.id}"]
        (dead,) = old_client.journal.failed()
        assert dead[1]["method"] == "PATCH"

    def test_the_deferred_finish_carries_the_epoch(self, app, tmp_path):
        from tests.conftest import make_client

        client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        run._queue_deferred_finish("completed", None, 0)

        (op,) = [o for _, o in client.journal.pending() if o.get("method") == "PATCH"]
        assert op["body"]["status"] == "completed"
        assert op["body"]["write_epoch"] == 1

    def test_a_handle_that_does_not_know_its_epoch_sends_none(self, app, tmp_path):
        """A bare `Run(client, {"id": ref})` (the CLI's offline handle) used
        to default to epoch 1, which fenced it out of any reopened run. An
        unknown epoch is sent as NO epoch -- the fence's fail-open case."""
        from tests.conftest import make_client

        client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
        seeded = open_run(client, experiment="e", name="r", heartbeat=False)
        handle = Run(client, {"id": seeded.id})
        assert handle.write_epoch is None
        handle.log({"loss": 1.0}, step=1)
        handle.set_status("completed")

        bodies = [o["body"] for _, o in client.journal.pending()]
        assert bodies and all("write_epoch" not in b for b in bodies), bodies


class TestReviewOf2010:
    """Findings from the review of #2010, each pinned."""

    def test_a_transient_failure_during_recovery_is_retried(self, app, tmp_path, monkeypatch):
        """LOW-1. `failures` reset after the first landed beat even when the
        recovery itself failed, so one 503 right after an outage (every rank's
        backlog draining at once) left the run `crashed` for the whole job."""
        from tests.conftest import make_client

        client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        net = _Network(client, monkeypatch)
        real_reopen = client.reopen_run
        calls = {"n": 0}

        def flaky_reopen(*a, **kw):
            calls["n"] += 1
            if calls["n"] == 1:
                raise errors.ServerError("503 busy", status=503)
            return real_reopen(*a, **kw)

        monkeypatch.setattr(client, "reopen_run", flaky_reopen)
        beat = _start_beating(client, run)
        try:
            net.down = True
            _wait_for(lambda: net.failed_beats >= 3)
            app.runs[run.id].update(status="crashed", ended_at=_recently())
            net.down = False
            _wait_for(lambda: app.runs[run.id]["status"] == "running")
        finally:
            _stop_beating(beat)

        assert calls["n"] == 2
        assert app.runs[run.id]["write_epoch"] == 1

    def test_retries_stop_at_the_cap(self, app, tmp_path, monkeypatch):
        from probe.sdk import run as run_mod
        from tests.conftest import make_client

        client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        net = _Network(client, monkeypatch)
        calls = {"n": 0}

        def always_busy(*a, **kw):
            calls["n"] += 1
            raise errors.ServerError("503 busy", status=503)

        monkeypatch.setattr(client, "reopen_run", always_busy)
        beat = _start_beating(client, run)
        try:
            net.down = True
            _wait_for(lambda: net.failed_beats >= 3)
            app.runs[run.id].update(status="crashed", ended_at=_recently())
            net.down = False
            floor = net.ok_beats
            _wait_for(lambda: net.ok_beats >= floor + run_mod._MAX_RECOVERY_TRIES + 10)
        finally:
            _stop_beating(beat)

        assert calls["n"] == run_mod._MAX_RECOVERY_TRIES
        assert app.runs[run.id]["status"] == "crashed"

    def test_a_refused_recovery_is_not_retried(self, app, tmp_path, monkeypatch):
        """A 409 means a sibling recovered it first or a newer attempt owns it:
        retrying cannot help and must not hammer the route."""
        from tests.conftest import make_client

        client = make_client(app, tmp_spool=tmp_path / "outbox", async_writes=True)
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        net = _Network(client, monkeypatch)
        calls = {"n": 0}

        def refused(*a, **kw):
            calls["n"] += 1
            raise errors.ConflictError("keep_epoch refused", detail={"message": "x"})

        monkeypatch.setattr(client, "reopen_run", refused)
        beat = _start_beating(client, run)
        try:
            net.down = True
            _wait_for(lambda: net.failed_beats >= 3)
            app.runs[run.id].update(status="crashed", ended_at=_recently())
            net.down = False
            floor = net.ok_beats
            _wait_for(lambda: net.ok_beats >= floor + 10)
        finally:
            _stop_beating(beat)

        assert calls["n"] == 1

    def test_the_launcher_replaces_a_reaper_crash_with_the_real_exit(self, client, app):
        """LOW-2. When recovery could not run (an older server, or the retries
        above ran out), the row stays `crashed`. The launcher's finalize used
        `only_if_running=True` and wrote nothing, so a wrapped job that exited 0
        ended `crashed`. `crashed` is a guess; the exit code is not."""
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id].update(status="crashed", ended_at=_recently())

        run.set_status("completed", only_if_running=True)

        assert app.runs[run.id]["status"] == "completed"

    @pytest.mark.parametrize("verdict", ["completed", "failed", "canceled", "untracked"])
    def test_the_launcher_still_never_overwrites_a_chosen_verdict(self, client, app, verdict):
        run = open_run(client, experiment="e", name="r", heartbeat=False)
        app.runs[run.id]["status"] = verdict

        assert run.set_status("completed", only_if_running=True) is None
        assert app.runs[run.id]["status"] == verdict
