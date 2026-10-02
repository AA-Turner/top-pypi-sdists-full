"""Shared NFS home: two Slurm nodes queue into ONE home directory at the same time.

A real kernel NFS server (nfsd, NFSv4.2, `sync` export) in a container; each compute
node mounts it itself, so each is a separate NFS client with its own client id,
caches and lock state -- two machines as far as the protocol is concerned. The SDK
queues every write in its outbox under $HOME before delivering it, so on a cluster
the outbox, its flock sidecars (`.append.lock`, `.drain.lock`, `.worker.lock`) and
its atomic renames all live on NFS.

Two layouts:
* default: each rank queues in its own `rank-<SLURM_PROCID>/` under the one home;
* shared: PROBE_OUTBOX_DIR names ONE directory for every rank on every node -- the
  setting the reliability plan's rollout note gave a customer ("a writable
  PROBE_OUTBOX_DIR on a large disk"). Both nodes then append to one queue and both
  nodes' background senders drain it.

Mid-run the nodes lose their route to the API for 15 s (docker network disconnect),
so both queues fill while both senders keep trying, then race to deliver the
backlog. What must hold: every point lands exactly once, nothing dead-letters, the
queues end empty, and the run closes `completed`.
"""

from __future__ import annotations

import json
import time

import pytest

from tests.environments._cluster.cluster import RESULTS, job_script, start_slurm
from tests.environments._cluster.fixtures import requires_env_tests, unique
from tests.environments._cluster.lab import HOME

pytestmark = [requires_env_tests]

_LOCK_HOLDER = r"""
import fcntl, os, sys, time
fh = open(os.path.expanduser("~/lockcheck"), "a+")
fcntl.flock(fh, fcntl.LOCK_EX)
open(os.path.expanduser("~/lockcheck.held"), "w").write("1")
time.sleep(float(sys.argv[1]))
"""

_LOCK_PROBE = r"""
import fcntl, os
fh = open(os.path.expanduser("~/lockcheck"), "a+")
try:
    fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    print("ACQUIRED")
except BlockingIOError:
    print("BLOCKED")
"""

_LOCK_WAITER = r"""
import fcntl, os, time
fh = open(os.path.expanduser("~/lockcheck"), "a+")
t = time.time()
fcntl.flock(fh, fcntl.LOCK_EX)
print(round(time.time() - t, 3))
"""

_RENAMER = r"""
import json, os
target = os.path.expanduser("~/renamecheck.json")
for i in range(400):
    tmp = target + f".tmp{os.getpid()}"
    with open(tmp, "w") as fh:
        json.dump({"i": i, "pad": "x" * 4000}, fh)
        fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, target)
print("RENAMED")
"""

_READER = r"""
import json, os, time
target = os.path.expanduser("~/renamecheck.json")
bad = seen = 0
deadline = time.time() + 30
while time.time() < deadline:
    try:
        with open(target) as fh:
            data = json.load(fh)
        seen += 1
        if data["i"] >= 399:
            break
    except FileNotFoundError:
        continue
    except (ValueError, KeyError):
        bad += 1
print(json.dumps({"seen": seen, "bad": bad}))
"""


def test_nfs_locks_and_renames_hold_across_nodes(backend, lab):
    """The two NFS properties the outbox is built on, checked directly between the
    two nodes before any SDK test trusts them: an flock held on one node excludes
    the other, and a reader on one node never sees a half-written file that the
    other node renames into place."""
    cluster = start_slurm(lab, backend)
    c1, c2 = cluster.nodes
    c1.exec(["python", "-c", _LOCK_HOLDER, "6"], detach=True)
    lab.wait_for("c1 holds the lock",
                 lambda: c2.read(f"{HOME}/lockcheck.held") is not None, timeout=30)
    assert c2.sh(["python", "-c", _LOCK_PROBE]).strip() == "BLOCKED", (
        "an flock held on c1 did not exclude c2: NFS locking is not cluster-wide here"
    )
    lab.wait_for("c1 released the lock",
                 lambda: c2.sh(["python", "-c", _LOCK_PROBE]).strip() == "ACQUIRED", timeout=30)

    # How long a BLOCKING flock waits for a lock the other node holds for 2 s.
    # Evidence for the shared-dir layout below: the Linux NFS client polls a
    # contended lock with backoff (up to 30 s) instead of being woken.
    waits = []
    for _ in range(3):
        c2.exec(["rm", "-f", f"{HOME}/lockcheck.held"])
        c1.exec(["python", "-c", _LOCK_HOLDER, "2"], detach=True)
        lab.wait_for("c1 holds the lock",
                     lambda: c2.read(f"{HOME}/lockcheck.held") is not None, timeout=30,
                     interval=0.05)
        waits.append(float(c2.sh(["python", "-c", _LOCK_WAITER], timeout=120).strip()))
        time.sleep(1)
    print(f"[nfs] a cross-node flock held for 2 s kept the other node waiting {waits} s")

    c1.exec(["python", "-c", _RENAMER], detach=True)
    seen = json.loads(c2.sh(["python", "-c", _READER], timeout=60).strip().splitlines()[-1])
    assert seen["bad"] == 0 and seen["seen"] > 0, seen


def _outbox_leftovers(cluster, root: str) -> dict:
    """Ops still queued, dead letters and quarantined files anywhere under ``root``."""
    out = cluster.ctl.sh(
        f"cd {root} 2>/dev/null && "
        "echo ops=$(find . -path '*/ops/*.json' | wc -l) "
        "failed=$(find . -path '*/failed/*' -type f | wc -l) "
        "corrupt=$(find . \\( -name '*corrupt*' -o -name '*quarantine*' \\) | wc -l) "
        "multipart=$(find . -path '*/multipart/ops/*.json' | wc -l)",
        check=False,
    ).split()
    return {k: int(v) for k, v in (item.split("=") for item in out)}


def _slow_logs(cluster, tag: str) -> str:
    events = cluster.events(tag)
    slow = [ev for ev in events if ev["event"] == "slow_log"]
    steps = {ev["rank"]: ev["step"] for ev in slow}
    longest = max((ev["seconds"] for ev in slow), default=0)
    return (f"{len(slow)} log() call(s) took over 1 s (longest {longest} s; last slow step "
            f"per rank {steps}). log() must never hold up the training loop.")


@pytest.mark.parametrize("layout", ["per-rank", "shared-dir"])
def test_two_nodes_queue_in_one_nfs_home_through_an_outage(backend, lab, layout):
    cluster = start_slurm(lab, backend)
    tag = unique(f"nfs-{layout}")
    extra = {}
    root = f"{HOME}/.local/state/probe/outbox"
    if layout == "shared-dir":
        root = f"{HOME}/probe-outbox"
        extra["PROBE_OUTBOX_DIR"] = root
    steps = 200
    job_id, _ = cluster.submit(
        job_script(tag, steps=steps, sleep=0.1, hold_at_step=40, extra_env=extra),
        tag=tag, run_name=f"envtest-nfs-{tag}",
    )
    try:
        cluster.wait_event(tag, lambda ev: ev["event"] == "holding" and ev["rank"] == 0,
                           timeout=240)
    except TimeoutError:
        pytest.fail(f"no progress in 240 s: {_slow_logs(cluster, tag)}")
    for node in cluster.nodes:
        node.disconnect("egress")
    cut_at = time.time()
    time.sleep(15)
    for node in cluster.nodes:
        node.connect("egress")
    print(f"[nfs {layout}] egress cut for {time.time() - cut_at:.1f}s")
    job = cluster.wait_job(job_id, {"COMPLETED", "FAILED", "CANCELLED"}, timeout=600)
    events = cluster.events(tag)
    assert job["JobState"] == "COMPLETED", (job, events[-6:])
    run_ids = {ev["run_id"] for ev in events if ev["event"] == "init"}
    assert len(run_ids) == 1, run_ids
    (run_id,) = run_ids

    logged = cluster.logged(tag, 0) + cluster.logged(tag, 1)
    rec = backend.reconcile(run_id, logged, wait=240)
    assert rec.ok, rec.summary()
    raw = backend.raw_deliveries(run_id)
    if raw is not None:
        # The fake keeps every POSTed point, so a point sent twice -- one node's
        # sender replaying an op the other node already delivered -- shows here.
        twice = {k: n for k, n in raw.items() if n > 1}
        assert not twice, f"{len(twice)} point(s) delivered more than once: {list(twice.items())[:5]}"

    assert backend.wait_status(run_id, {"completed", "failed", "crashed", "canceled"},
                               timeout=180) == "completed", backend.run(run_id)
    trained = [ev for ev in events if ev["event"] == "trained"]
    print(f"[nfs {layout}] log() latency per rank: "
          + "; ".join(f"rank{ev['rank']} p50={ev['log_p50']}s p99={ev['log_p99']}s "
                      f"max={ev['log_max']}s" for ev in trained))
    assert not [ev for ev in events if ev["event"] == "slow_log"], _slow_logs(cluster, tag)
    left = lab.wait_for("both queues empty",
                        lambda: (lambda d: d if d.get("ops", 1) == 0 else None)(
                            _outbox_leftovers(cluster, root)), timeout=120, interval=3)
    assert left == {"ops": 0, "failed": 0, "corrupt": 0, "multipart": 0}, left
