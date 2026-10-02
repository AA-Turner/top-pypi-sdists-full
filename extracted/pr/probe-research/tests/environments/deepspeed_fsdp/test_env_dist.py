"""DeepSpeed (ZeRO-1, CPU accelerator, gloo) and torch FSDP (CPU, gloo), 2 ranks.

What it simulates: a customer's plain distributed script (no Lightning / HF
integration) launched by ``torchrun --nproc_per_node 2``, logging from rank 0
only, with every rank calling ``probe.init()`` / ``probe.finish()`` -- in the
two ways a rank can learn the run: under ``probe exec`` (the launcher exports
PROBE_RUN_ID) or by rank 0 broadcasting the id over the process group.

Checks: every point rank 0 logged, a writer lease on EACH rank (plus the
launcher's under probe exec), every lease released ``completed``, the run
``completed``, exit 0, no hang.

Real: torch 2.x FSDP and DeepSpeed's CPU accelerator over gloo, torchrun,
``probe exec``, the released SDK. Simulated: two ranks on one box (not two
nodes), no GPU (no NCCL, no CUDA streams), and the server (the fake unless
PROBE_BASE_URL is set).
"""

from __future__ import annotations

import os

import pytest

from tests.environments import envkit

pytestmark = envkit.requires_env

TIMEOUT = 420


@pytest.mark.parametrize("handoff", ["exec", "broadcast"])
@pytest.mark.parametrize("fw", ["fsdp", "deepspeed"])
def test_two_rank_job_logs_from_rank0_and_leases_every_rank(target, dirs, started, fw, handoff):
    envkit.requirement("deepspeed" if fw == "deepspeed" else "torch.distributed.fsdp")
    bindir = os.path.dirname(envkit.PYTHON)
    job = [
        os.path.join(bindir, "torchrun"), "--standalone", "--nproc_per_node", "2",
        envkit.script("deepspeed_fsdp", "dist_job.py"), fw, handoff,
    ]
    if handoff == "exec":
        job = [
            os.path.join(bindir, "probe"), "exec", "--project", target.project,
            "--name", f"{fw}-exec", "--", *job,
        ]
    extra = {"DS_ACCELERATOR": "cpu"} if fw == "deepspeed" else {}
    child = envkit.run_child(
        job, env=envkit.child_env(target, dirs, **extra), cwd=dirs.work, timeout=TIMEOUT
    )
    assert not child.timed_out and child.returncode == 0, child.tail()
    r0, r1 = child.result("rank0"), child.result("rank1")
    assert r0["run_id"] == r1["run_id"], (r0["run_id"], r1["run_id"])
    assert r0["finish_raised"] is None and r1["finish_raised"] is None, (r0, r1)
    run_id = r0["run_id"]

    reader = target.reader()
    status = envkit.wait_status(reader, run_id)
    missing, wrong, _ = envkit.reconcile(reader, run_id, envkit.ledger_expected(r0["ledger"]))
    leases = envkit.lease_summary(envkit.writers(reader, run_id))
    summary = (
        f"[{fw}/{handoff}] sdk {r0['sdk_version']} torch {r0['torch_version']} "
        f"ds {r0['ds_version']}: status={status} points={len(r0['ledger'])} "
        f"missing={len(missing)} leases={leases} {child.elapsed:.1f}s"
    )
    print(summary)
    assert not missing and not wrong, (summary, missing[:4], wrong[:4])
    assert status == "completed", summary
    if handoff == "exec":
        want = [
            ("launcher", None, True, "completed"),
            ("rank", 0, True, "completed"),
            ("rank", 1, True, "completed"),
        ]
    else:
        want = [("owner", 0, True, "completed"), ("rank", 1, True, "completed")]
    assert leases == want, summary
    names = set(r0["artifacts"])
    arts = envkit.wait_artifacts(reader, run_id, names)
    assert names <= set(arts), (names, sorted(arts))
    assert envkit.leaked_files([run_id], started) == []
