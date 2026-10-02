"""Slurm: a controller and two compute nodes in containers, NFS home, torch gloo DDP.

The documented launch (skills/instrument-code: "Slurm"): ``probe exec -- sbatch job.sh``
on the login side opens the run AWAITING ATTACH and exports PROBE_RUN_ID +
PROBE_RUN_EPOCH; ``sbatch`` (default ``--export=ALL``) carries them into the job and
``srun`` into both ranks, whose ``probe.init()`` joins the run -- rank 0 as its owner,
rank 1 as a rank.

Opt-in: PROBE_ENV_TESTS=1. Real server: PROBE_BASE_URL + PROBE_TOKEN + PROBE_E2E_PROJECT.
"""

from __future__ import annotations

import os
import re
import time

import pytest

from tests.environments._cluster.backend import FakeBackend
from tests.environments._cluster.cluster import files_outside, job_script, start_slurm
from tests.environments._cluster.fixtures import requires_env_tests, unique
from tests.environments._cluster.lab import sdk_version

pytestmark = [requires_env_tests]

#: One artifact over the 64 MiB single-upload ceiling: the multipart path (M1).
BIG_MB = 70
#: How long a scancel'd run may stay `running` (plan 2.2's target is < 1 min).
SCANCEL_CLOSE_SEC = float(os.environ.get("PROBE_ENV_SCANCEL_CLOSE_SEC", "120"))

_HAND_OFF_LEGACY = (
    "bug (lane E1, fixed by lane K, first released after 0.198.1): a run `probe exec -- "
    "sbatch` opens AWAITING ATTACH never asked for the lease rules "
    "(client._lease_for_create), so both ranks' writer-gone reports changed nothing and "
    "only the 900 s reaper could close it"
)
#: The first release whose hand-off runs follow the lease rules. An SDK source tree
#: under test (PROBE_ENV_SDK_SRC) is a checkout of main, which has it.
#: cli v0.199.0 shipped WITHOUT this fix (#2123 branched before it and landed after),
#: so the gate is the release after 0.199.0, not 0.198.2.
_HAND_OFF_LEASES_IN = (0, 199, 1)


def _released_before(version: str, fixed_in: tuple[int, ...]) -> bool:
    if os.environ.get("PROBE_ENV_SDK_SRC", "").strip():
        return False
    parts = tuple(int(n) for n in re.findall(r"\d+", version)[: len(fixed_in)])
    return parts < fixed_in


@pytest.fixture
def scancel_closes(request, image) -> None:
    """A strict xfail only on a release without the fix, so the mark neither hides
    a regression nor fails a fixed SDK."""
    if _released_before(sdk_version(image), _HAND_OFF_LEASES_IN):
        request.applymarker(pytest.mark.xfail(strict=True, reason=_HAND_OFF_LEGACY))


def _logged(cluster, tag: str, ranks=(0, 1)) -> list[dict]:
    rows = []
    for rank in ranks:
        rows += cluster.logged(tag, rank)
    return rows


def _run_ids(cluster, tag: str) -> set[str]:
    return {ev["run_id"] for ev in cluster.events(tag) if ev["event"] == "init"}


def test_two_node_ddp_job_lands_every_rank(backend, lab):
    """The happy path: both ranks' data, both leases, config, a small and a 70 MiB
    artifact, `completed`, exit 0, nothing written outside the researcher's home."""
    cluster = start_slurm(lab, backend)
    for node in cluster.nodes:
        node.exec("touch /tmp/.envtest-start", user=None)
    tag = unique("happy")
    job_id, launch = cluster.submit(job_script(tag, steps=40, big_mb=BIG_MB), tag=tag,
                                    run_name=f"envtest-slurm-{tag}")
    job = cluster.wait_job(job_id, {"COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"}, timeout=600)
    events = cluster.events(tag)
    assert job["JobState"] == "COMPLETED" and job.get("ExitCode") == "0:0", (job, events[-6:])

    (run_id,) = _run_ids(cluster, tag)
    assert {ev["host"] for ev in events if ev["event"] == "finished"} == {"c1", "c2"}, events

    rec = backend.reconcile(run_id, _logged(cluster, tag))
    assert rec.ok, rec.summary()
    assert rec.expected == 40 * 2 * 2 + 40 * 3  # rankN/{loss,step_time} x 2 ranks + loss, opt/*

    status = backend.wait_status(run_id, {"completed", "failed", "crashed", "canceled"}, timeout=120)
    assert status == "completed", backend.run(run_id)

    writers = backend.writers(run_id)
    by_host = {w.get("host"): w for w in writers}
    assert set(by_host) == {"c1", "c2"}, writers
    assert sorted(w.get("role") for w in writers) == ["owner", "rank"], writers
    assert all(w.get("exit_status") == "completed" for w in writers), writers

    config = backend.run(run_id).get("config") or {}
    assert config.get("phase") == "trained", config

    expected_arts = {a["name"]: a for ev in events if ev["event"] == "artifacts"
                     for a in ev["artifacts"]}
    # A > 64 MiB artifact goes up in parts from the queue AFTER finish() returns,
    # so its row can appear later than the run's close.
    try:
        arts = lab.wait_for(
            "every logged artifact listed",
            lambda: (lambda a: a if set(expected_arts) <= set(a) else None)(
                {x.get("name"): x for x in backend.artifacts(run_id)}),
            timeout=600 if backend.kind == "real" else 120, interval=3,
        )
    except TimeoutError:
        listed = {x.get("name") for x in backend.artifacts(run_id)}
        stranded = cluster.ctl.sh(
            "find ~/.local/state/probe/outbox -path '*/multipart/ops/*.json' "
            "-exec grep -h -E '\"(name|attempts)\"' {} + | tr -d ' ,' | paste -sd' '",
            check=False).strip()
        pytest.fail(
            f"not listed: {sorted(set(expected_arts) - listed)}. Still queued in the NFS "
            f"outbox with no sender left to deliver it: [{stranded}]. The detached sender "
            "exited while the upload was queued (its exit check ignored the multipart queue)"
        )
    for name, meta in expected_arts.items():
        assert name in arts, (name, sorted(arts), backend.request_summary())
        size = arts[name].get("size_bytes") or arts[name].get("size")
        assert size in (None, meta["size"]), (name, size, meta)

    # Outside the (NFS) home, only the node's TMPDIR may be written: every SDK
    # process creates the private fallback outbox root `$TMPDIR/probe-outbox-<uid>`
    # (empty while the home outbox works; journal.private_fallback_root).
    for node in cluster.nodes:
        stray = files_outside(node, "/tmp/.envtest-start", allowed=("/tmp/",))
        in_tmp = files_outside(node, "/tmp/.envtest-start", allowed=())
        print(f"[happy] {node.name} wrote under /tmp: {in_tmp[:10]}")
        assert not stray, (node.name, stray[:20])


def test_scancel_mid_run_closes_the_run_and_keeps_what_was_logged(backend, lab, scancel_closes):
    """``scancel`` sends SIGTERM to both ranks (SIGKILL KillWait=10 s later). Since
    #2119 each rank's SIGTERM handler delivers its queue, closes its run `failed`
    marked preempted -- on a hand-off that is a RELEASE of its lease: the owner's on
    rank 0, a rank's on rank 1 -- and dies of SIGTERM. SIGTERM does not say whether a
    person or the scheduler stopped the job, so it is never `canceled`. The leases
    then close the run `failed`, in seconds, not after the reaper's 15 minutes.

    Checked, in this order: every point whose ``log()`` returned before the kill
    reaches the server (the queue is on the NFS home, so it outlives the job); the run
    leaves `running` within ``PROBE_ENV_SCANCEL_CLOSE_SEC`` (default 120 s), on the
    lease rules, `failed`, both leases released `failed`, `probe_finish` preempted.
    A hand-off follows the lease rules only from the release after 0.198.1: a strict
    xfail on an older one (there the run stays `running`)."""
    cluster = start_slurm(lab, backend)
    tag = unique("scancel")
    job_id, _ = cluster.submit(job_script(tag, steps=100_000, sleep=0.1, hold_at_step=30),
                               tag=tag, run_name=f"envtest-scancel-{tag}")
    cluster.wait_event(tag, lambda ev: ev["event"] == "holding", timeout=300)
    time.sleep(3)
    t_cancel = time.time()
    cluster.ctl.exec(f"scancel {job_id}", timeout=60)
    job = cluster.wait_job(job_id, {"CANCELLED", "FAILED", "COMPLETED"}, timeout=120)
    assert job["JobState"] == "CANCELLED", job
    (run_id,) = _run_ids(cluster, tag)

    rec = backend.reconcile(run_id, _logged(cluster, tag), wait=180)
    assert rec.ok, rec.summary()

    status = backend.wait_status(run_id, {"completed", "failed", "crashed", "canceled"},
                                 timeout=SCANCEL_CLOSE_SEC)
    closed_after = round(time.time() - t_cancel, 1)
    row = backend.run(run_id)
    writers = backend.writers(run_id)
    print(f"[scancel] run {run_id} status={status} after {closed_after}s; "
          f"liveness_protocol={row.get('liveness_protocol')!r}; writers={writers}")
    assert status in {"crashed", "failed", "canceled"}, (
        f"run still {status!r} {closed_after}s after scancel. liveness_protocol="
        f"{row.get('liveness_protocol')!r} (a hand-off run must follow the lease rules, or "
        "both ranks' writer-gone reports change nothing and only the 900 s reaper closes it)"
    )
    if isinstance(backend, FakeBackend):
        assert row.get("liveness_protocol") == "leases", row
    else:
        # The real server's run read doesn't expose `liveness_protocol` (it
        # comes back None -- only the release-writer response carries it, and
        # this test never calls it directly). Prove "followed the lease
        # rules" instead from the writers list: at least one lease
        # (session_id + role + rank) present, and the run closed within
        # SCANCEL_CLOSE_SEC (checked above via `status`/`closed_after`).
        assert closed_after <= SCANCEL_CLOSE_SEC, (closed_after, SCANCEL_CLOSE_SEC)
        leased = [w for w in writers
                  if w.get("session_id") and w.get("role") is not None and w.get("rank") is not None]
        assert leased, f"no writer carried a lease (session_id/role/rank): {writers}"
    ended = sorted((w.get("role"), w.get("exit_status")) for w in writers)
    assert ended == [("owner", "failed"), ("rank", "failed")], writers
    assert status == "failed", status
    finish = (row.get("summary_metrics") or row.get("summary") or {}).get("probe_finish") or {}
    assert finish.get("reason") == "preempted" and finish.get("signal") == "SIGTERM", finish


def test_requeue_continues_the_same_run(backend, lab):
    """``scontrol requeue`` kills the running job (SIGTERM, then SIGKILL) and runs it
    again with the SAME environment, so PROBE_RUN_ID/EPOCH are the first attempt's.
    The job resumes from its checkpoint; both attempts must write ONE run, every
    step must land, and the run must end `completed`."""
    cluster = start_slurm(lab, backend)
    tag = unique("requeue")
    steps = 120
    job_id, _ = cluster.submit(
        job_script(tag, steps=steps, sleep=0.1, requeue=True, hold_at_step=40),
        tag=tag, run_name=f"envtest-requeue-{tag}",
    )
    cluster.wait_event(tag, lambda ev: ev["event"] == "holding", timeout=300)
    cluster.ctl.exec(f"scontrol requeue {job_id}", user=None, timeout=60)
    cluster.wait_event(tag, lambda ev: ev["event"] == "init" and ev["attempt"] == "1",
                       timeout=400)
    job = cluster.wait_job(job_id, {"COMPLETED", "FAILED", "CANCELLED"}, timeout=600)
    events = cluster.events(tag)
    inits = [ev for ev in events if ev["event"] == "init"]
    print(f"[requeue] job={job.get('JobState')} restarts={job.get('Restarts')} inits={inits}")
    assert job["JobState"] == "COMPLETED", (job, events[-8:])
    run_ids = {ev["run_id"] for ev in inits}
    assert len(run_ids) == 1, f"the requeued attempt wrote a different run: {inits}"
    (run_id,) = run_ids

    # A step the first attempt logged but did not checkpoint is logged again by the
    # second, with a different value (the model restarts): either value is right.
    logged = _logged(cluster, tag)
    last = {}
    for row in logged:
        last[(row["step"], row["key"])] = row
    rec = backend.reconcile(run_id, list(last.values()), wait=180)
    relogged = {(r["step"], r["key"]) for r in logged} and [
        k for k in last if sum(1 for r in logged if (r["step"], r["key"]) == k) > 1
    ]
    wrong = [w for w in rec.wrong_value if (w[0], w[1]) not in set(relogged)]
    assert not rec.missing and not wrong, rec.summary()
    assert backend.wait_status(run_id, {"completed", "failed", "crashed", "canceled"},
                               timeout=180) == "completed", backend.run(run_id)
