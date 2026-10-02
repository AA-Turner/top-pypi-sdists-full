"""Ray Train (TorchTrainer, 2 CPU workers) and Ray Tune (4 trials).

What it simulates: a customer's single-node Ray job where Ray itself starts
the processes that log. Train: the driver opens the run and hands (id,
epoch) to the workers through ``runtime_env`` env_vars (the documented
shape); every worker attaches with ``probe.init()``, world rank 0 logs.
Tune: one Probe run per trial, opened inside the trainable; a scheduler
stops one trial early; one trial's actor is SIGKILLed. Run as a function
trainable and as a ``tune.Trainable`` class, and -- against the fake --
with 2 s of latency on every close request, which is what a real network
does to a close Ray gives 200 ms.

Real: Ray (its raylet, GCS, worker and trial actors, its teardown), Ray
Train V2 with torch DDP over gloo, Ray Tune's controller and scheduler, the
released SDK. Simulated: one node (no multi-node Ray cluster), CPU only, and
the server (the fake unless PROBE_BASE_URL is set). A SIGKILLed actor stands
in for an OOM kill or a lost node.
"""

from __future__ import annotations

import shutil
import tempfile
import time
from pathlib import Path

import pytest

from tests.environments import envchild, envkit
from tests.served_fake_app import close_latency

pytestmark = envkit.requires_env

TIMEOUT = 480
#: The Tune trial whose actor SIGKILLs itself (`ray_tune_job.py`).
KILLED_TRIAL = 2
#: How long to wait for that trial's run to read `crashed`. The fake closes it
#: the moment the writer-gone report lands; a real server acts on that report
#: (or on the lease expiring) later -- on prod it still read `running` at 20 s.
#: `PROBE_ENV_CLOSE_WAIT_SEC`, 300 s when unset or 0.
KILLED_TRIAL_WAIT = (envkit.CLOSE_WAIT or 300.0) if envkit.REAL else 20.0


@pytest.fixture
def ray_env(target, dirs):
    """The child env plus a SHORT temp dir: Ray's unix sockets live under it
    and a pytest tmp path overflows the 107-byte socket path limit."""
    short = tempfile.mkdtemp(prefix="e2ray-", dir="/tmp")
    env = envkit.child_env(
        target, dirs,
        RAY_SHORT_TMP=short,
        PROBE_ENV_RESULTS_FILE=str(dirs.root / "results.jsonl"),
    )
    # Ray's own logs there repeat what the workers printed (run ids included).
    envkit.ALLOWED_ROOTS.append(Path(short))
    yield env
    envkit.reap_marked(short)
    envkit.ALLOWED_ROOTS.remove(Path(short))
    shutil.rmtree(short, ignore_errors=True)


def _train(ray_env, dirs, mode: str) -> envkit.Child:
    envkit.requirement("ray.train.torch")
    child = envkit.run_child(
        [envkit.PYTHON, envkit.script("ray_jobs", "ray_train_job.py"), mode],
        env=ray_env, cwd=dirs.work, timeout=TIMEOUT,
    )
    assert not child.timed_out, f"hung: {child.tail()}"
    return child


def _logged_steps(child: envkit.Child) -> list[int]:
    return sorted({r["step"] for r in child.results if r.get("tag") == "worker0-logged"})


def test_ray_train_two_workers_one_run(target, dirs, ray_env, started):
    child = _train(ray_env, dirs, "ok")
    assert child.returncode == 0, child.tail()
    driver = child.result("driver-done")
    run_id = driver["run_id"]
    starts = [child.result(f"worker{r}-start") for r in (0, 1)]
    assert {s["run_id"] for s in starts} == {run_id}, starts
    reader = target.reader()
    status = envkit.wait_status(reader, run_id)
    missing, wrong, _ = envkit.reconcile(reader, run_id, envchild.expected(range(10)))
    leases = envkit.lease_summary(envkit.writers(reader, run_id))
    print(
        f"[ray-train/ok] sdk {starts[0]['sdk_version']} ray {driver['ray_version']}: "
        f"status={status} missing={len(missing)} wrong={len(wrong)} leases={leases} "
        f"worker env={[s.get('RANK') for s in starts]} {child.elapsed:.1f}s"
    )
    assert not missing and not wrong, (missing[:4], wrong[:4])
    assert status == "completed"
    assert leases == [
        ("owner", None, True, "completed"),
        ("owner", 0, True, "completed"),
        ("rank", 1, True, "completed"),
    ], leases
    names = set(driver["artifacts"])
    arts = envkit.wait_artifacts(reader, run_id, names)
    assert names <= set(arts), (names, sorted(arts))
    assert envkit.leaked_files([run_id], started) == []


def test_ray_train_worker_sigkilled(target, dirs, ray_env, started):
    child = _train(ray_env, dirs, "kill")
    run_id = child.result("driver-start")["run_id"]
    child.result("worker1-killing")
    reader = target.reader()
    status = envkit.wait_status(reader, run_id, timeout=30)
    steps = _logged_steps(child)
    missing, wrong, _ = envkit.reconcile(reader, run_id, envchild.expected(steps))
    leases = envkit.lease_summary(envkit.writers(reader, run_id))
    print(
        f"[ray-train/kill] rc={child.returncode} status={status} rank0 logged {steps} "
        f"missing={len(missing)} leases={leases} {child.elapsed:.1f}s"
    )
    # The driver does not hang: fit() raises within seconds, uncaught -> 1.
    assert child.returncode == 1, child.tail()
    assert "TrainingFailedError" in child.stderr, child.tail()
    # Everything rank 0 logged before Ray tore it down reached the server.
    assert steps and not missing and not wrong, (steps, missing[:4], wrong[:4])
    # The driver released `failed`; the SIGKILLed worker's output helper
    # reported it gone; the worker Ray killed in its teardown released
    # nothing (no exit hook ran, and nothing reported it).
    assert leases == [
        ("owner", None, True, "failed"),
        ("owner", 0, False, None),
        ("rank", 1, False, "gone"),
    ], leases
    if target.app is not None:
        # The fake has no lease clock: rank 0's silent lease never expires.
        assert status == "running", status
    elif envkit.CLOSE_WAIT:
        # A real server closes it once rank 0's lease expires (>= 180 s),
        # worst verdict first: the GONE counts `crashed`.
        final = envkit.wait_status(reader, run_id, timeout=envkit.CLOSE_WAIT)
        print(f"[ray-train/kill] real server final status {final}")
        assert final == "crashed", final
    assert envkit.leaked_files([run_id], started) == []


#: The round trip the fake adds to each CLOSE request -- the run's closing
#: PATCH and the lease release -- in the slow-close variant: a close then
#: takes about as long as over a real network, where it takes far longer than
#: the 200 ms Ray gives a stopped trial between SIGTERM and SIGKILL.
CLOSE_LATENCY = 2.0
#: A function trial's close is queued for the detached outbox sender, which
#: may still be delivering it (2 s a request, slow) when the job exits: even
#: against the fake it gets this long before the harness reaps it.
TUNE_HELPER_GRACE = 60.0


@pytest.mark.parametrize(
    ("api", "close"),
    [("function", "fast"), ("function", "slow"), ("class", "slow")],
    ids=["function-fast-close", "function-slow-close", "class-slow-close"],
)
def test_ray_tune_one_run_per_trial(target, dirs, ray_env, started, api, close):
    envkit.requirement("ray.tune")
    if close == "slow":
        if target.app is None:
            pytest.skip("a real server's latency is its own; the slow close is the fake's")
        target.app.latency = close_latency(CLOSE_LATENCY)
    child = envkit.run_child(
        [envkit.PYTHON, envkit.script("ray_jobs", "ray_tune_job.py"), api],
        env=ray_env, cwd=dirs.work, timeout=TIMEOUT,
        helper_grace=None if envkit.REAL else TUNE_HELPER_GRACE,
    )
    assert not child.timed_out, f"hung: {child.tail()}"
    job_ended = time.monotonic()
    done = child.result("tune-done")
    reader = target.reader()
    runs = {t: child.result(f"trial{t}-start")["run_id"] for t in range(4)}
    report = {}
    for t, run_id in runs.items():
        steps = sorted({r["step"] for r in child.results if r.get("tag") == f"trial{t}-logged"})
        wait = KILLED_TRIAL_WAIT if t == KILLED_TRIAL else 20
        status = envkit.wait_status(reader, run_id, timeout=wait)
        if t == KILLED_TRIAL:
            print(
                f"[ray-tune/{api}-{close}/trial{t}] read {status!r} {time.monotonic() - job_ended:.1f}s "
                f"after the job ended (waited up to {wait:.0f}s)"
            )
        missing, wrong, _ = envkit.reconcile(reader, run_id, envchild.expected(steps, salt=t), timeout=20)
        report[t] = {
            "status": status, "logged": steps, "missing": len(missing), "wrong": len(wrong),
            "leases": envkit.lease_summary(envkit.writers(reader, run_id)),
            "tune": done["states"].get(str(t), done["states"].get(t)),
        }
    for t, row in report.items():
        print(f"[ray-tune/{api}-{close}/trial{t}] {row}")
    print(f"[ray-tune/{api}-{close}] rc={child.returncode} {child.elapsed:.1f}s")
    assert child.returncode == 0, child.tail()
    assert len(set(runs.values())) == 4, runs  # one run per trial
    for t, row in report.items():
        assert row["logged"] and not row["missing"] and not row["wrong"], (t, row)
    # Trials 0 and 1 ran every iteration: trial 0 then called probe.finish(),
    # trial 1 just returned (class: both closed in `cleanup()`).
    for t in (0, 1):
        assert report[t]["status"] == "completed", report[t]
        assert report[t]["leases"] == [("owner", None, True, "completed")], report[t]
        assert report[t]["logged"] == list(range(10)), report[t]
    # Trial 2's actor was SIGKILLed: Tune records ActorDiedError, and its
    # output helper reports the writer gone, so the run is `crashed` at once.
    assert report[2]["tune"]["error"] == "ActorDiedError", report[2]
    assert report[2]["status"] == "crashed", report[2]
    assert report[2]["leases"] == [("owner", None, False, "gone")], report[2]
    # Trial 3 was stopped by the scheduler -- `completed`, with the steps it
    # logged (a stop is not a failure to the SDK; Tune calls it TERMINATED).
    # Function: `tune.report()` ends its thread with sys.exit(0), which closes
    # the run at once, queued for the outbox worker -- Ray SIGKILLs the actor's
    # process group 200 ms after its SIGTERM, too soon for the exit hook's
    # close over a real network (prod: `running`, lease held). Class: closed in
    # `cleanup()`, which Tune waits for.
    assert report[3]["tune"]["error"] is None and report[3]["logged"] != list(range(10)), report[3]
    assert report[3]["status"] == "completed", report[3]
    assert report[3]["leases"] == [("owner", None, True, "completed")], report[3]
    assert envkit.leaked_files(list(runs.values()), started) == []
