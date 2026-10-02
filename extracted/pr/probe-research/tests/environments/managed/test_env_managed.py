"""Managed / ephemeral jobs: SageMaker, Vertex, Modal, spot instances.

Simulated with Docker (``python:3.12-slim`` + the released SDK, 2 CPUs, 1 GB):
the job's own disk is the container's overlay layer, and "destroyed" means
``docker rm -v`` -- the queue on that layer is gone for good. The stop is
``docker stop -t 30``: SIGTERM, then SIGKILL 30 s later, which is what
Kubernetes (Vertex custom jobs, SageMaker HyperPod), a GCP spot reclaim and
SageMaker's stop do. Two ways the signal lands are both real and both tested:

* ``init`` -- a PID 1 that forwards it (``--init``: tini, as K8s images with an
  init, SageMaker's training toolkit and most launchers do): Python gets
  SIGTERM, whose default action ends it at once -- no ``finally``, no atexit.
* ``pid1`` -- Python IS PID 1 (``CMD ["python", "train.py"]``): the kernel
  drops a signal PID 1 has no handler for, so the job runs on through the grace
  and dies of SIGKILL.

What is NOT simulated: the platforms' own agents (SageMaker's uploader of
/opt/ml/model, Modal's volume commit), network egress policies, and GPUs.
"""

from __future__ import annotations

import json
import os
import re
import time
import uuid

import pytest

from tests.environments import envlib
from tests.environments.envlib import Container, LoopEvents, record

pytestmark = [
    envlib.requires_env,
    pytest.mark.skipif(envlib.ENABLED and not envlib.docker_available(), reason="needs a Docker daemon"),
]

GRACE = int(os.environ.get("PROBE_ENV_GRACE_SEC", "30"))
MOUNT = ["-v", f"{envlib.HERE}:/envtests:ro", *envlib.sdk_src_mount()]
LOOP = ["python", "-u", "/envtests/customer_loop.py"]
TERMINAL = {"completed", "failed", "crashed", "canceled"}
#: A child that never hangs still may take init (90 s budget) + finish (600 s
#: budget, PROBE_FINISH_TIMEOUT_SEC) when a door is down; past that it hangs.
FINISH_BOUND = 780


@pytest.fixture(scope="module")
def image(sdk_version) -> str:
    return envlib.ensure_image(sdk_version)


def _loop(*args: str) -> list[str]:
    return [*LOOP, *args]


def _artifact_names(be, run_id: str) -> dict[str, dict]:
    rows = {}
    for row in be.artifacts(run_id):
        if row.get("name") in ("small.txt", "big.bin"):
            rows.setdefault(row["name"], row)
    return rows


def _events_of(container: Container) -> LoopEvents:
    return LoopEvents.parse(container.logs())


# -- (a) SIGTERM with writes queued, then the container and its disk destroyed --------


_NO_SIGTERM_FLUSH = (
    "finding (design call, reported by lane E3; fixed by the SIGTERM flush, "
    "PROBE_SIGTERM_FLUSH_SECONDS, first released after 0.198.1): the SDK installs no "
    "SIGTERM handler, so a SIGTERMed job neither flushes its queue within the grace nor "
    "closes its run; on a throwaway disk the queue dies with the container and the run "
    "stays `running` until the 15-min reaper (the output helper that reports writer-gone "
    "dies with PID 1)"
)
#: The first release with the SIGTERM flush (above): the one after 0.198.1. If
#: a release lands before that change merges, bump this to the one after it.
#: An SDK source tree under test (PROBE_ENV_SDK_SRC) is a checkout that has it.
_SIGTERM_FLUSH_IN = (0, 198, 2)


@pytest.fixture
def flavor(request, sdk_version) -> str:
    """How the signal lands; a strict xfail only on a release without the
    flush, so the mark neither hides a regression nor fails a fixed SDK."""
    if _released_before(sdk_version, _SIGTERM_FLUSH_IN):
        request.applymarker(pytest.mark.xfail(strict=True, reason=_NO_SIGTERM_FLUSH))
    return request.param


@pytest.mark.parametrize("flavor", ["init", "pid1"], indirect=True)
def test_env_managed_sigterm_with_queued_writes_then_destroyed(be, image, sdk_version, flavor):
    """The server is busy (503 + Retry-After, production's contention answer)
    while the job trains, so its writes queue on the job's own disk; the
    platform then stops the job and destroys the container.

    Healthy again from the moment the stop is sent: whatever the SDK does
    with the grace period -- flush, send directly -- it can reach the server.
    Pass = every point and the config arrive, and the run ends failed/crashed
    within 60 s (plan 2.2's "< 1 min"), never `completed`, never left
    `running` for the 15-minute reaper.

    Since the SIGTERM flush both flavors pass: `init`'s Python gets the
    signal from tini; `pid1`'s gets it too once a handler is installed (the
    kernel drops only a signal PID 1 has no handler for), and exits 143 since
    the kernel will not kill a PID 1 with SIGTERM's default action."""
    steps = range(0, 300)
    expected = envlib.expected_points(steps)
    busy = be.set_metrics_busy(True)
    job = Container(
        image,
        _loop("--name", f"sigterm-{flavor}", "--steps", "0:300", "--config", "--small-artifact", "--then", "wait"),
        env=envlib.container_env(be),
        docker_args=[*(["--init"] if flavor == "init" else []), *MOUNT],
    )
    try:
        job.start()
        job.wait_for('"event": "ready"', timeout=180)
        events = _events_of(job)
        run_id = events.run_id
        queued_at_stop = envlib.reconcile(expected, be.points(run_id))
        be.set_metrics_busy(False)
        exit_code, stop_took = job.stop(GRACE)
        diff = job.diff()
    finally:
        job.remove()
    destroyed_at = time.monotonic()
    rec = be.wait_points(run_id, expected, timeout=15)
    status = be.wait_status(run_id, TERMINAL, timeout=60)
    status_after = round(time.monotonic() - destroyed_at, 1)
    run = be.run(run_id)
    arts = _artifact_names(be, run_id)
    outbox = (events.first("start") or {}).get("outbox", {})
    record(
        f"managed/sigterm[{flavor}]",
        sdk=sdk_version,
        busy_server_arranged=busy,
        outbox_verdict={k: outbox.get(k) for k in ("durable", "fstype", "reason")},
        undelivered_when_stopped=queued_at_stop.expected - queued_at_stop.delivered,
        container_exit=exit_code,
        stop_seconds=round(stop_took, 1),
        points=rec.summary(),
        config_delivered=bool((run.get("config") or {}).get("model")),
        small_artifact=(arts.get("small.txt") or {}).get("status"),
        status=status,
        status_checked_after_s=status_after,
        probe_finish=((run.get("summary_metrics") or run.get("summary") or {}).get("probe_finish")),
        writes_outside_root_home=envlib.writes_outside(diff, ("/root", "/job", "/tmp")),
    )
    assert outbox.get("durable") is False, f"the SDK should see the overlay disk as throwaway: {outbox}"
    assert rec.ok, f"lost with the container: {rec.summary()}"
    assert (run.get("config") or {}).get("model") == envlib.CONFIG["model"]
    assert status in {"failed", "crashed"}, (
        f"run left {status!r} {status_after}s after its container was destroyed"
    )


# -- (b) spot preemption, then a NEW container resumes from the checkpoint ------------


def test_env_managed_spot_preemption_resumes_in_a_new_container(be, image, sdk_version, tmp_path):
    """Container 1 trains steps 0..229 checkpointing every 50 steps to a
    volume that outlives it (S3/EFS/a PVC), is preempted (SIGTERM, SIGKILL at
    +30 s) and destroyed. Container 2 -- fresh disk, same checkpoint volume,
    same `external_id` -- resumes at step 200, re-logs 200..229 and finishes.

    Pass = ONE run holds every step 0..299, container 2 continued container
    1's run (same id), it finished `completed` with exit 0, and the takeover
    wait stayed inside PROBE_TAKEOVER_WAIT_SEC (300 s)."""
    ckpt_dir = tmp_path / "ckpt"
    ckpt_dir.mkdir()
    os.chmod(ckpt_dir, 0o777)
    job_id = f"spot-{uuid.uuid4().hex[:10]}"
    common = ["--name", "spot-job", "--external-id", job_id, "--steps", "0:300",
              "--ckpt", "/ckpt/state.json", "--ckpt-every", "50"]
    mounts = [*MOUNT, "-v", f"{ckpt_dir}:/ckpt"]
    # 0.1 s a step: a real loop, so the SDK's normal delivery lag (p95 ~1.5 s
    # measured on the fake) leaves only the last ~15 steps at risk -- all
    # after the step-199 checkpoint, so the restart re-logs them.
    first = Container(
        image,
        _loop(*common, "--stop-after", "229", "--step-sleep", "0.1", "--then", "wait"),
        env=envlib.container_env(be),
        docker_args=["--init", *mounts],
    )
    try:
        first.start()
        first.wait_for('"event": "ready"', timeout=300)
        run_1 = _events_of(first).run_id
        exit_1, _ = first.stop(GRACE)
    finally:
        first.remove()
    saved = json.loads((ckpt_dir / "state.json").read_text())["step"]
    before = envlib.reconcile(envlib.expected_points(range(0, 230)), be.points(run_1))

    second = Container(
        image,
        _loop(*common, "--config", "--small-artifact", "--then", "finish"),
        env=envlib.container_env(be),
        docker_args=["--init", *mounts],
    )
    t = time.monotonic()
    try:
        second.start()
        exit_2 = second.wait_exit(timeout=600)
        logs_2 = second.logs()
    finally:
        second.remove()
    took_2 = round(time.monotonic() - t, 1)
    events_2 = LoopEvents.parse(logs_2)
    run_2 = events_2.run_id
    expected = envlib.expected_points(range(0, 300))
    rec = be.wait_points(run_2 or run_1, expected, timeout=60) if (run_2 or run_1) else None
    status = be.wait_status(run_2, TERMINAL, timeout=60) if run_2 else None
    record(
        "managed/spot-resume",
        sdk=sdk_version,
        checkpoint_step=saved,
        first_delivered_of_0_229=before.summary(),
        first_exit=exit_1,
        second_exit=exit_2,
        same_run=run_1 == run_2,
        run_1=run_1,
        run_2=run_2,
        second_seconds=took_2,
        init_seconds=(events_2.first("run") or {}).get("init_seconds"),
        resumed_at=(events_2.first("resumed_from_checkpoint") or {}).get("next_step"),
        points=rec.summary() if rec else None,
        status=status,
        second_stderr_tail=envlib.tail(logs_2, 600) if exit_2 != 0 else "",
    )
    assert saved == 199
    assert exit_2 == 0, f"the resumed job failed:\n{envlib.tail(logs_2)}"
    assert run_2 == run_1, f"the new container opened {run_2}, not the preempted {run_1}"
    assert rec is not None and rec.ok, rec.summary() if rec else "no run id"
    assert status == "completed"


# -- (c) read-only root filesystem, only /tmp writable --------------------------------


def test_env_managed_read_only_root_only_tmp_writable(be, image, sdk_version):
    """``--read-only`` with a tmpfs /tmp: HOME (/root) exists but cannot be
    written, as in hardened Vertex/Kubernetes pods. The whole loop, a 65 MiB
    artifact included (multipart, settled at close because the queue is on a
    throwaway disk). Pass = every point, config, both artifacts, `completed`,
    exit 0, and nothing written anywhere but /tmp."""
    expected = envlib.expected_points(range(0, 50))
    job = Container(
        image,
        _loop("--name", "ro-root", "--steps", "0:50", "--config", "--small-artifact",
              "--big-mib", "65", "--workdir", "/tmp", "--then", "finish"),
        env=envlib.container_env(be),
        docker_args=["--init", "--read-only", "--tmpfs", "/tmp:rw,exec,size=512m", "-w", "/tmp", *MOUNT],
    )
    try:
        job.start()
        code = job.wait_exit(timeout=FINISH_BOUND)
        logs = job.logs()
        diff = job.diff()
    finally:
        job.remove()
    events = LoopEvents.parse(logs)
    run_id = events.run_id
    rec = be.wait_points(run_id, expected, timeout=60) if run_id else None
    status = be.wait_status(run_id, TERMINAL, timeout=60) if run_id else None
    arts = _artifact_names(be, run_id) if run_id else {}
    run = be.run(run_id) if run_id else {}
    record(
        "managed/read-only-root",
        sdk=sdk_version,
        exit=code,
        outbox=(events.first("start") or {}).get("outbox"),
        points=rec.summary() if rec else None,
        config_delivered=bool((run.get("config") or {}).get("model")),
        artifacts={k: (v.get("status"), v.get("is_reference")) for k, v in arts.items()},
        status=status,
        diff=diff[:10],
        sdk_warnings=envlib.sdk_warnings(logs),
        stderr_tail=envlib.tail(logs, 800) if code != 0 else "",
    )
    assert code == 0, envlib.tail(logs)
    assert rec is not None and rec.ok, rec.summary() if rec else "no run"
    assert (run.get("config") or {}).get("model") == envlib.CONFIG["model"]
    assert status == "completed"
    assert set(arts) == {"small.txt", "big.bin"}, arts
    assert envlib.writes_outside(diff, ()) == [], f"wrote outside /tmp on a read-only root: {diff[:10]}"


# -- (d) HOME unset or not writable ----------------------------------------------------

_HOMES = {
    # A uid with no passwd entry and no HOME at all: Path.home() raises.
    "unset": ["env", "-u", "HOME"],
    # What Docker itself gives a uid it cannot find: HOME=/ (not writable).
    "slash": ["env", "HOME=/"],
    # A HOME that names nothing.
    "nonexistent": ["env", "HOME=/nonexistent/home"],
}


_NO_HOME_CRASH = (
    "bug (lane E3, fixed by #2109, first released in 0.198.0): with HOME unset and "
    "no passwd entry probe.init() raises RuntimeError('Could not determine home "
    "directory') from config.config_path() -- Path.home() is called unguarded on "
    "the init path"
)
#: The first release with #2109 (above). An SDK source tree under test
#: (PROBE_ENV_SDK_SRC) is a checkout of main, which has it.
_HOME_FIXED_IN = (0, 198, 0)


def _released_before(version: str, fixed_in: tuple[int, ...]) -> bool:
    if envlib.SDK_SRC:
        return False
    parts = tuple(int(n) for n in re.findall(r"\d+", version)[: len(fixed_in)])
    return parts < fixed_in


@pytest.fixture
def home(request, sdk_version) -> str:
    """The HOME case; `unset` is a strict xfail only on a release without the
    fix, so the mark neither hides a regression nor fails a fixed SDK."""
    if request.param == "unset" and _released_before(sdk_version, _HOME_FIXED_IN):
        request.applymarker(pytest.mark.xfail(strict=True, reason=_NO_HOME_CRASH))
    return request.param


@pytest.mark.parametrize("home", ["nonexistent", "slash", "unset"], indirect=True)
def test_env_managed_home_unset_or_unwritable(be, image, sdk_version, home):
    """An arbitrary uid (OpenShift, many managed runners) with a HOME that is
    missing, `/`, or nonexistent. Pass = the loop completes with every point,
    config and artifact, exit 0, and writes land only under /tmp."""
    expected = envlib.expected_points(range(0, 50))
    job = Container(
        image,
        [*_HOMES[home], *_loop("--name", f"home-{home}", "--steps", "0:50", "--config",
                               "--small-artifact", "--workdir", "/tmp", "--then", "finish")],
        env=envlib.container_env(be),
        docker_args=["--init", "--user", "12345:12345", "-w", "/tmp", *MOUNT],
    )
    try:
        job.start()
        code = job.wait_exit(timeout=FINISH_BOUND)
        logs = job.logs()
        diff = job.diff()
    finally:
        job.remove()
    events = LoopEvents.parse(logs)
    run_id = events.run_id
    rec = be.wait_points(run_id, expected, timeout=60) if run_id else None
    status = be.wait_status(run_id, TERMINAL, timeout=60) if run_id else None
    arts = _artifact_names(be, run_id) if run_id else {}
    run = be.run(run_id) if run_id else {}
    outside = envlib.writes_outside(diff, ("/tmp",))
    record(
        f"managed/home[{home}]",
        sdk=sdk_version,
        exit=code,
        outbox=(events.first("start") or {}).get("outbox"),
        points=rec.summary() if rec else None,
        config_delivered=bool((run.get("config") or {}).get("model")),
        artifacts={k: v.get("status") for k, v in arts.items()},
        status=status,
        writes_outside_tmp=outside[:10],
        sdk_warnings=envlib.sdk_warnings(logs),
        stderr_tail=envlib.tail(logs, 800) if code != 0 else "",
    )
    assert code == 0, envlib.tail(logs)
    assert rec is not None and rec.ok, rec.summary() if rec else "no run"
    assert (run.get("config") or {}).get("model") == envlib.CONFIG["model"]
    assert status == "completed"
    assert "small.txt" in arts
    assert outside == [], outside[:10]
