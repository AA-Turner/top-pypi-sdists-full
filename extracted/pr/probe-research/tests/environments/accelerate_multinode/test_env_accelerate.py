"""Hugging Face Accelerate: a 2-"node" job and notebook_launcher, on CPU.

What it simulates:

* two machines: two separate ``accelerate launch --num_machines 2
  --machine_rank {0,1}`` invocations, each with its OWN home, outbox, temp
  and working dirs (nothing shared but the loopback network), meeting at a
  static rendezvous on 127.0.0.1 -- one rank per "node";
* a notebook: the script calls ``accelerate.notebook_launcher(train,
  num_processes=2)``, which forks two workers (torch elastic, fork).

Both train a Hugging Face ``Trainer`` with ``ProbeCallback``, so they check
the #2091 hand-off: world zero opens the run and publishes (run id, epoch)
in the process group's store; rank 1 takes a lease-only ``rank`` lease on it.
Pass: rank 0's logs reconcile, one run with an ``owner`` lease (rank 0) and a
``rank`` lease (rank 1), both released ``completed``, the run ``completed``,
exit 0 everywhere, no hang -- with and without an explicit ``probe.finish()``
(a forked worker's exit runs no atexit).

Real: accelerate's launcher and notebook_launcher, torch elastic over gloo,
transformers' Trainer, the released SDK. Simulated: the two "nodes" are two
process trees on one box (loopback, not a NIC; same clock), and the server.
"""

from __future__ import annotations

import os
import socket
from concurrent.futures import ThreadPoolExecutor

import pytest

from tests.environments import envkit

pytestmark = envkit.requires_env

TIMEOUT = 420


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _check(target, results: list[dict], label: str, elapsed: float, started: float) -> None:
    by_rank = {r["rank"]: r for r in results if "rank" in r}
    assert set(by_rank) == {0, 1}, results
    r0, r1 = by_rank[0], by_rank[1]
    run_id = r0["run_id"]
    assert run_id and r1["run_id"] == run_id, f"rank 1 did not join rank 0's run: {r0['run_id']} vs {r1['run_id']}"
    reader = target.reader()
    status = envkit.wait_status(reader, run_id)
    missing, wrong, _ = envkit.reconcile(reader, run_id, envkit.ledger_expected(r0["ledger"]))
    leases = envkit.lease_summary(envkit.writers(reader, run_id))
    print(
        f"[{label}] sdk {r0['sdk_version']}: status={status} points={len(r0['ledger'])} "
        f"missing={len(missing)} wrong={len(wrong)} leases={leases} {elapsed:.1f}s"
    )
    assert not missing and not wrong, (missing[:4], wrong[:4])
    assert status == "completed", (label, status)
    assert leases == [("owner", 0, True, "completed"), ("rank", 1, True, "completed")], leases
    names = set(r0["artifacts"])
    arts = envkit.wait_artifacts(reader, run_id, names)
    assert names <= set(arts), (names, sorted(arts))
    assert envkit.leaked_files([run_id], started) == []


@pytest.mark.parametrize("finish", [True, False], ids=["finish", "exit-closes"])
def test_two_machines_hand_off_the_run_to_rank1(target, tmp_path, started, finish):
    envkit.requirement("accelerate")
    envkit.requirement("transformers")
    port = _free_port()
    accelerate = os.path.join(os.path.dirname(envkit.PYTHON), "accelerate")
    nodes = [envkit.make_dirs(tmp_path / f"node{i}") for i in (0, 1)]

    def node(i: int) -> envkit.Child:
        argv = [
            accelerate, "launch", "--multi_gpu", "--num_machines", "2", "--num_processes", "2",
            "--machine_rank", str(i), "--main_process_ip", "127.0.0.1",
            "--main_process_port", str(port), "--rdzv_backend", "static",
            envkit.script("accelerate_multinode", "hf_job.py"), "launch",
            *(["--finish"] if finish else []),
        ]
        return envkit.run_child(
            argv, env=envkit.child_env(target, nodes[i]), cwd=nodes[i].work, timeout=TIMEOUT
        )

    with ThreadPoolExecutor(2) as pool:
        children = list(pool.map(node, (0, 1)))
    for i, child in enumerate(children):
        assert not child.timed_out and child.returncode == 0, f"node {i}:\n{child.tail()}"
    results = [r for c in children for r in c.results]
    _check(target, results, f"2 nodes/{'finish' if finish else 'exit'}", max(c.elapsed for c in children), started)


@pytest.mark.parametrize("finish", [True, False], ids=["finish", "exit-closes"])
def test_notebook_launcher_forks_two_workers(target, dirs, started, finish):
    envkit.requirement("accelerate")
    envkit.requirement("transformers")
    child = envkit.run_child(
        [envkit.PYTHON, envkit.script("accelerate_multinode", "hf_job.py"), "notebook",
         *(["--finish"] if finish else [])],
        env=envkit.child_env(target, dirs, HF_JOB_PORT=str(_free_port())),
        cwd=dirs.work,
        timeout=TIMEOUT,
    )
    assert not child.timed_out and child.returncode == 0, child.tail()
    child.result("kernel")
    _check(target, child.results, f"notebook/{'finish' if finish else 'exit'}", child.elapsed, started)
