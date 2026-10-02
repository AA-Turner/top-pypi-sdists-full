"""Multi-node DDP without Slurm: two containers, one rank each, joined by torchrun's
c10d rendezvous, and one of them killed mid-run.

The documented launch for Docker/Kubernetes (skills/instrument-code): a launcher
opens the run (``probe exec --detached-launcher``: AWAITING ATTACH) and hands
PROBE_RUN_ID + PROBE_RUN_EPOCH to every node; each rank's ``probe.init()`` joins.
Each node queues on its own local disk, as a pod without a persistent volume does.

``docker kill`` of the node that does not host the rendezvous is the "GPU node
died" case: SIGKILL for every process on it, output helper included, so nothing
on that node reports anything. The survivor's gloo collective fails at once
(connection closed by peer), so it too ends -- through its excepthook.

Checked: the survivor's lease closes with its own verdict; the dead rank's lease
is never released and expires (the fake is given the server's lease clock,
compressed to 20 s, see `FakeBackend.age_leases`); the run reaches a terminal
status; every point the survivor logged lands. `writer_lost` is a server-side
finding with no public read (app/findings, `shadow=True`): it is reported as not
observable here, never assumed.
"""

from __future__ import annotations

import os
import time

from tests.environments._cluster.backend import FakeBackend
from tests.environments._cluster.cluster import RESULTS, files_outside, node_env, start_relay
from tests.environments._cluster.fixtures import requires_env_tests, unique
from tests.environments._cluster.lab import HOME, json_lines

pytestmark = [requires_env_tests]

#: Real server: lease expiry is max(3 x beat interval, 180 s) and a run whose
#: owner released waits up to 600 s for the rest (app/runs/writers.py).
REAL_CLOSE_WAIT = float(os.environ.get("PROBE_ENV_CLOSE_WAIT_SEC", "900"))
FAKE_LEASE_EXPIRY = 20.0


def _events(node, tag):
    text = node.sh(f"cat {RESULTS}/{tag}/events-rank*.jsonl 2>/dev/null", check=False)
    return sorted(json_lines(text), key=lambda ev: ev["t"])


def test_killing_one_node_mid_run(backend, lab):
    lab.network("egress")
    start_relay(lab, backend)
    env = node_env(backend)
    vols = backend.container_volumes()
    nodes = [lab.run(n, role="node", networks=["egress"], env=env, volumes=vols, cpus=2,
                     memory="3g") for n in ("n0", "n1")]
    n0, n1 = nodes
    for node in nodes:
        node.exec("touch /tmp/.envtest-start", user=None)
    if isinstance(backend, FakeBackend):
        clock = backend.age_leases(FAKE_LEASE_EXPIRY)

    tag = unique("ddp")
    launch = n0.exec(
        f"mkdir -p {RESULTS}/{tag} && cd {RESULTS}/{tag} && probe exec --detached-launcher "
        f"--project {backend.project} --name envtest-{tag} -- "
        f"bash -c 'echo \"$PROBE_RUN_ID $PROBE_RUN_EPOCH\" > {HOME}/ids'",
        env=backend.container_env(), timeout=180, check=False,
    )
    assert launch.returncode == 0, (launch.stdout + launch.stderr)[-2000:]
    run_id, epoch = n0.read(f"{HOME}/ids").split()

    job_env = {**backend.container_env(), "PROBE_RUN_ID": run_id, "PROBE_RUN_EPOCH": epoch}
    for node in nodes:
        node.exec(
            f"mkdir -p {RESULTS}/{tag} && cd {RESULTS}/{tag} && "
            "torchrun --nnodes=2 --nproc-per-node=1 --rdzv-backend=c10d "
            "--rdzv-endpoint=n0:29400 --rdzv-id=envtest --max-restarts=0 "
            f"/harness/workload.py --out {RESULTS}/{tag} --steps 100000 --sleep 0.1 "
            f"--hold-at-step 30 > {RESULTS}/{tag}/torchrun.out 2>&1; "
            f"echo $? > {RESULTS}/{tag}/torchrun.rc",
            env=job_env, detach=True,
        )
    for node in nodes:
        lab.wait_for(f"{node.name} past step 30",
                     lambda node=node: any(ev["event"] == "holding" for ev in _events(node, tag)),
                     timeout=300, interval=2)
    time.sleep(3)
    ranks = {node.name: next(ev["rank"] for ev in _events(node, tag) if ev["event"] == "start")
             for node in nodes}
    survivor_logged_before = len(json_lines(n0.read(f"{RESULTS}/{tag}/logged-rank{ranks['n0']}.jsonl")))
    killed_logged = json_lines(n1.read(f"{RESULTS}/{tag}/logged-rank{ranks['n1']}.jsonl"))

    t_kill = time.time()
    n1.kill("KILL")
    rc = lab.wait_for("the survivor's torchrun to exit",
                      lambda: n0.read(f"{RESULTS}/{tag}/torchrun.rc"), timeout=300, interval=2)
    survivor_exit_s = round(time.time() - t_kill, 1)
    events = _events(n0, tag)
    print(f"[ddp] ranks={ranks} killed n1 (rank {ranks['n1']}); survivor torchrun rc={rc.strip()} "
          f"after {survivor_exit_s}s; survivor events tail={[e['event'] for e in events[-4:]]}")

    # The survivor's lease: its own process closed it with its own verdict.
    def survivor_lease():
        for w in backend.writers(run_id):
            if w.get("host") == "n0" and (w.get("released_at") or w.get("state") == "released"):
                return w
        return None

    lease = lab.wait_for("the survivor's lease released", survivor_lease, timeout=120, interval=3)
    print(f"[ddp] survivor lease: {lease}")
    assert lease.get("exit_status") in {"failed", "canceled", "crashed"}, lease

    # The dead rank's lease: never released, never reported gone by anyone (its
    # whole container died), so it can only expire.
    dead = [w for w in backend.writers(run_id) if w.get("host") == "n1"]
    assert dead, backend.writers(run_id)
    assert not any(w.get("released_at") for w in dead), dead

    wait = FAKE_LEASE_EXPIRY + 60 if isinstance(backend, FakeBackend) else REAL_CLOSE_WAIT
    status = backend.wait_status(run_id, {"completed", "failed", "crashed", "canceled"},
                                 timeout=wait)
    closed_after = round(time.time() - t_kill, 1)
    row = backend.run(run_id)
    print(f"[ddp] run status={status} {closed_after}s after the kill, "
          f"liveness_protocol={row.get('liveness_protocol')!r}")
    assert status in {"failed", "crashed"}, (status, backend.writers(run_id))

    # However the run closed, the dead rank's lease must end up expired: it is
    # the only record that rank 1 went away without a word.
    if isinstance(backend, FakeBackend):
        lab.wait_for("the dead rank's lease to expire",
                     lambda: any(rid == run_id for rid, _s, _t in clock.expired),
                     timeout=FAKE_LEASE_EXPIRY + 30, interval=2)
        dead_state = "expired"
    else:
        dead_state = lab.wait_for(
            "the dead rank's lease to expire",
            lambda: next((w.get("state") for w in backend.writers(run_id)
                          if w.get("host") == "n1" and w.get("state") in {"expired", "gone"}), None),
            timeout=REAL_CLOSE_WAIT, interval=10)
    print(f"[ddp] dead rank lease: {dead_state} {round(time.time() - t_kill, 1)}s after the kill")
    print("[ddp] writer_lost: NOT OBSERVABLE here -- a server-side finding (app/findings, "
          "shadow) with no public read; check run_findings for run " + run_id)

    # Every point the survivor logged lands; the dead rank's queue died with its
    # disk, so its points land only if they were delivered before the kill.
    survivor = json_lines(n0.read(f"{RESULTS}/{tag}/logged-rank{ranks['n0']}.jsonl"))
    rec = backend.reconcile(run_id, survivor, wait=120)
    assert rec.ok, rec.summary()
    have = {(p.step, p.key) for p in backend.points(run_id)}
    lost = [r for r in killed_logged if (r["step"], r["key"]) not in have]
    print(f"[ddp] survivor points {len(survivor)} (all landed; {survivor_logged_before} before "
          f"the kill); killed rank: {len(killed_logged)} logged before the kill, {len(lost)} lost "
          f"with its container, last lost steps {sorted({r['step'] for r in lost})[-5:]}")
    stray = files_outside(n0, "/tmp/.envtest-start", allowed=("/tmp/",))
    assert not stray, stray[:20]
