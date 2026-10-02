"""Compute nodes with no internet.

(a) Egress only through the site's HTTP proxy. The node sits on an INTERNAL docker
    network (no route anywhere); a squid container on that network and on an
    ordinary one is the only way out. HTTPS_PROXY/HTTP_PROXY point at it -- the
    usual cluster setup. Every SDK process must go through it: the training
    process, the background sender it forks, the presigned artifact upload.

(b) No egress at all. The job runs ``probe.init(mode="offline")`` with its home on
    NFS; afterwards ``probe sync`` on a login node that shares the home and can reach
    the server delivers the run -- the ``wandb offline`` + ``wandb sync`` workflow.

Neither is a Slurm job: the property under test is the network, so the node is a
plain container running the workload as the researcher (fidelity note in README).
"""

from __future__ import annotations

import json
import time

import pytest

from tests.environments._cluster.backend import FakeBackend
from tests.environments._cluster.cluster import (
    RESULTS,
    files_outside,
    node_env,
    start_nfs,
    start_relay,
)
from tests.environments._cluster.fixtures import requires_env_tests, unique
from tests.environments._cluster.lab import HOME, json_lines

pytestmark = [requires_env_tests]


def _topology(lab, backend, *, squid: bool):
    lab.network("cluster", internal=True)
    lab.network("egress")
    start_relay(lab, backend)
    start_nfs(lab)
    vols = backend.container_volumes()
    env = node_env(backend, {"NFS_SERVER": "nfs"})
    node = lab.run("c1", role="node", networks=["cluster"], env=env, volumes=vols,
                   mount_caps=True, cpus=2, memory="3g")
    login = lab.run("login", role="node", networks=["cluster", "egress"], env=env, volumes=vols,
                    mount_caps=True, cpus=1, memory="1g")
    proxy = None
    if squid:
        proxy = lab.run("squid", role="squid", networks=["cluster", "egress"], cpus=1,
                        memory="512m")
        lab.wait_for("squid listening",
                     lambda: "3128" in proxy.sh("ss -ltn", user=None, check=False), timeout=60)
    for c in (node, login):
        lab.wait_for(f"{c.name} home mounted",
                     lambda c=c: "nfs" in c.sh("stat -f -c %T /home", user=None, check=False),
                     timeout=90)
        c.exec("touch /tmp/.envtest-start", user=None)
    return node, login, proxy


def _nothing_outside_home_and_tmp(*containers) -> None:
    for c in containers:
        stray = files_outside(c, "/tmp/.envtest-start", allowed=("/tmp/",))
        assert not stray, (c.name, stray[:20])


def _no_direct_route(node, url: str) -> str:
    """The negative control: the node itself cannot reach the API."""
    proc = node.exec(f"curl --noproxy '*' -sS -o /dev/null -m 8 {url}/healthz", check=False,
                     timeout=60)
    assert proc.returncode != 0, f"the node reached {url} directly: the test proves nothing"
    return (proc.stderr or "").strip()


def _events(node, tag):
    text = node.sh(f"cat {RESULTS}/{tag}/events-rank*.jsonl 2>/dev/null", check=False)
    return sorted(json_lines(text), key=lambda ev: ev["t"])


def _logged(node, tag):
    return json_lines(node.read(f"{RESULTS}/{tag}/logged-rank0.jsonl"))


def _outbox_op_paths(node) -> list[str]:
    out = node.sh(f"find {HOME}/.local/state/probe/outbox -path '*/ops/*.json'",
                  check=False)
    return [p for p in out.splitlines() if p.strip()]


def _drained_outbox(node, *, timeout: float, interval: float = 3.0) -> str:
    """Poll the queued-op count until it reaches 0 (or ``timeout`` elapses) and
    return the final count. On timeout the assertion this feeds should show
    which op kinds are still stuck -- never their bodies or tokens."""
    deadline = time.monotonic() + timeout
    left = node.sh(f"find {HOME}/.local/state/probe/outbox -path '*/ops/*.json' | wc -l",
                   check=False).strip()
    while left != "0" and time.monotonic() < deadline:
        time.sleep(interval)
        left = node.sh(f"find {HOME}/.local/state/probe/outbox -path '*/ops/*.json' | wc -l",
                       check=False).strip()
    if left != "0":
        stuck = []
        for path in _outbox_op_paths(node):
            raw = node.read(path)
            try:
                op = json.loads(raw) if raw else {}
            except (json.JSONDecodeError, TypeError):
                op = {}
            stuck.append({"kind": op.get("kind"), "method": op.get("method"),
                          "path": op.get("path")})
        left = f"{left} (still queued: {stuck})"
    return left


@pytest.mark.parametrize("case", ["upper", "lower"])
def test_everything_goes_through_the_site_proxy(backend, lab, case):
    node, _login, proxy = _topology(lab, backend, squid=True)
    why = _no_direct_route(node, backend.url)
    names = ("HTTPS_PROXY", "HTTP_PROXY") if case == "upper" else ("https_proxy", "http_proxy")
    env = {**backend.container_env(), **{n: "http://squid:3128" for n in names}}
    tag = unique(f"proxy-{case}")
    proc = node.exec(
        f"cd {HOME} && timeout 600 python /harness/workload.py --out {RESULTS}/{tag} "
        f"--steps 60 --project {backend.project} --name envtest-{tag}",
        env=env, timeout=660, check=False,
    )
    events = _events(node, tag)
    assert proc.returncode == 0, (proc.returncode, proc.stderr[-3000:], events[-4:])
    (run_id,) = {ev["run_id"] for ev in events if ev["event"] == "init"}

    rec = backend.reconcile(run_id, _logged(node, tag), wait=120)
    assert rec.ok, rec.summary()
    assert backend.wait_status(run_id, {"completed", "failed", "crashed", "canceled"},
                               timeout=120) == "completed", backend.run(run_id)
    names_listed = lab.wait_for(
        "summary.json listed",
        lambda: (lambda n: n if "summary.json" in n else None)(
            {a.get("name") for a in backend.artifacts(run_id)}),
        timeout=120, interval=3,
    )
    assert "summary.json" in names_listed

    log = proxy.read("/var/log/squid/access.log", user=None) or ""
    api_host = backend.url.split("://", 1)[1].split("/", 1)[0]
    assert f"CONNECT {api_host}:443" in log, log[-2000:]
    if isinstance(backend, FakeBackend):
        # The fake's presigned uploads are plain http://r2.test/... (HTTP_PROXY).
        assert "http://r2.test/put/" in log, log[-2000:]
    # The background sender, not just the training process, must have used the
    # proxy: nothing is left queued on the node. Against a real server the drain
    # is asynchronous (the sender runs on its own schedule through squid), so
    # poll for it instead of snapshotting one instant; against the fake it is
    # already synchronous, so the poll exits on its first check.
    left = _drained_outbox(node, timeout=1 if isinstance(backend, FakeBackend) else 180)
    assert left == "0", left
    _nothing_outside_home_and_tmp(node)
    print(f"[proxy {case}] direct: {why[:120]}; squid lines: {len(log.splitlines())}")


def test_offline_run_then_probe_sync_from_the_login_node(backend, lab):
    node, login, _ = _topology(lab, backend, squid=False)
    _no_direct_route(node, backend.url)
    tag = unique("offline")
    before = len(backend.requests()) if isinstance(backend, FakeBackend) else None
    # Credentials are deliberately present: an offline run must not use them.
    proc = node.exec(
        f"cd {HOME} && timeout 300 python /harness/workload.py --out {RESULTS}/{tag} "
        f"--steps 60 --mode offline --project {backend.project} --name envtest-{tag}",
        env=backend.container_env(), timeout=360, check=False,
    )
    events = _events(node, tag)
    assert proc.returncode == 0, (proc.returncode, proc.stderr[-3000:], events[-4:])
    (local_id,) = {ev["run_id"] for ev in events if ev["event"] == "init"}
    init_s = next(ev["seconds"] for ev in events if ev["event"] == "init")
    finish_s = next(ev["seconds"] for ev in events if ev["event"] == "finished")
    assert init_s < 10 and finish_s < 30, (init_s, finish_s)
    if before is not None:
        assert len(backend.requests()) == before, "the offline run reached the server"

    sync = login.exec("timeout 600 probe sync", env=backend.container_env(), timeout=660,
                      check=False)
    out = sync.stdout + sync.stderr
    assert sync.returncode == 0, out[-3000:]
    print(f"[offline] probe sync:\n{out[-1500:]}")
    # Offline, the run has only a local id (`local:<key>`); `probe sync` prints the
    # id the server gave it.
    assert local_id.startswith("local:"), local_id
    synced = [row for row in json.loads(sync.stdout[sync.stdout.index("["):])
              if row.get("key") == local_id.split(":", 1)[1]]
    assert len(synced) == 1 and synced[0]["state"] == "synced" and synced[0]["clean"], out[-2000:]
    run_id = synced[0]["run_id"]
    assert synced[0]["dropped_writes"] == 0 and synced[0]["dead_lettered"] == 0, synced[0]
    rec = backend.reconcile(run_id, _logged(node, tag), wait=120)
    assert rec.ok, rec.summary() + "\n" + out[-1500:] + "\n" + backend.request_summary()
    assert backend.wait_status(run_id, {"completed", "failed", "crashed", "canceled"},
                               timeout=120) == "completed", backend.run(run_id)
    assert "summary.json" in {a.get("name") for a in backend.artifacts(run_id)}

    again = login.exec("timeout 300 probe sync", env=backend.container_env(), timeout=360,
                       check=False)
    assert again.returncode == 0, (again.stdout + again.stderr)[-2000:]
    raw = backend.raw_deliveries(run_id)
    if raw is not None:
        twice = {k: n for k, n in raw.items() if n > 1}
        assert not twice, f"a second sync re-sent {len(twice)} point(s)"
    left = login.sh(f"find {HOME}/.local/state/probe/outbox -path '*/ops/*.json' | wc -l",
                    check=False).strip()
    assert left == "0", left
    _nothing_outside_home_and_tmp(node, login)
