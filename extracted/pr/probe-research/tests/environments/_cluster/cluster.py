"""Topologies the cluster environment tests build, on top of `lab.Lab`.

Networks:
  ``cluster``  internal (no route out): NFS server, Slurm traffic, compute nodes.
  ``egress``   an ordinary bridge: the API relay (fake mode) and whatever may reach
               the API -- the Slurm nodes in the Slurm test, the login node, squid.
"""

from __future__ import annotations

import json
import os
import shlex
import time
from dataclasses import dataclass
from pathlib import Path

from .backend import Backend, FakeBackend
from .lab import HOME, Container, Lab, json_lines

RESULTS = f"{HOME}/results"


def start_relay(lab: Lab, backend: Backend) -> Container | None:
    """Fake mode: the relay that puts the fake on ``egress`` as ``api`` and ``r2.test``."""
    if not isinstance(backend, FakeBackend):
        return None
    relay = lab.run("relay", role="relay", networks=["egress"], aliases=["api", "r2.test"],
                    volumes=backend.relay_volumes(), cpus=1, memory="256m")
    lab.wait_for("relay listening", lambda: "relay up" in relay.logs(), timeout=30)
    return relay


def start_nfs(lab: Lab, *, export_opts: str = "") -> Container:
    export = lab.volume("export")
    env = {"NFS_EXPORT_OPTS": export_opts} if export_opts else {}
    nfs = lab.run("nfs", role="nfs", networks=["cluster"], volumes=[f"{export}:/export"],
                  privileged=True, cpus=1, memory="512m", env=env)
    lab.wait_for("nfsd up", lambda: "nfsd up" in nfs.logs(), timeout=60)
    return nfs


def node_env(backend: Backend, extra: dict | None = None) -> dict[str, str]:
    """What every node's processes see from the container's own environment: no
    credential (that is passed per command, see `Container.exec`)."""
    env = {}
    if isinstance(backend, FakeBackend):
        env["SSL_CERT_FILE"] = backend.container_env()["SSL_CERT_FILE"]
    env.update(extra or {})
    return env


@dataclass
class SlurmCluster:
    lab: Lab
    backend: Backend
    ctl: Container
    nodes: list[Container]

    def submit(self, script: str, *, tag: str, run_name: str, env: dict | None = None,
               timeout: float = 180) -> tuple[str, str]:
        """``probe exec -- sbatch`` from the login side, the documented Slurm launch:
        the run opens AWAITING ATTACH and each rank's ``probe.init()`` joins it.
        Returns (job id, probe exec output)."""
        path = f"{RESULTS}/{tag}/job.sh"
        self.ctl.exec(["bash", "-c", f"mkdir -p {RESULTS}/{tag} && cat > {path} <<'JOB'\n{script}\nJOB\n"],
                      timeout=60)
        cmd = (
            f"cd {RESULTS}/{tag} && probe exec --project {shlex.quote(self.backend.project)} "
            f"--name {shlex.quote(run_name)} -- sbatch --parsable {path}"
        )
        proc = self.ctl.exec(cmd, env={**self.backend.container_env(), **(env or {})},
                             timeout=timeout, check=False)
        text = proc.stdout + proc.stderr
        job_ids = [line.strip() for line in proc.stdout.splitlines() if line.strip().isdigit()]
        if proc.returncode != 0 or not job_ids:
            raise AssertionError(f"probe exec -- sbatch failed ({proc.returncode}):\n{text[-3000:]}")
        return job_ids[-1], text

    def job(self, job_id: str) -> dict[str, str]:
        out = self.ctl.sh(f"scontrol show job -o {job_id}", user=None, check=False, timeout=30)
        fields = {}
        for token in out.split():
            if "=" in token:
                k, _, v = token.partition("=")
                fields[k] = v
        return fields

    def wait_job(self, job_id: str, states: set[str], timeout: float) -> dict[str, str]:
        return self.lab.wait_for(
            f"job {job_id} in {states}",
            lambda: (lambda j: j if j.get("JobState") in states else None)(self.job(job_id)),
            timeout=timeout, interval=2,
        )

    def events(self, tag: str) -> list[dict]:
        text = self.ctl.sh(f"cat {RESULTS}/{tag}/events-rank*.jsonl 2>/dev/null", check=False)
        return sorted(json_lines(text), key=lambda ev: ev["t"])

    def logged(self, tag: str, rank: int) -> list[dict]:
        return json_lines(self.ctl.read(f"{RESULTS}/{tag}/logged-rank{rank}.jsonl"))

    def wait_event(self, tag: str, predicate, timeout: float) -> dict:
        def found():
            for ev in self.events(tag):
                if predicate(ev):
                    return ev
            return None

        return self.lab.wait_for(f"event in {tag}", found, timeout=timeout, interval=1)


def start_slurm(lab: Lab, backend: Backend, *, nfs_opts: str = "") -> SlurmCluster:
    lab.network("cluster", internal=True)
    lab.network("egress")
    start_relay(lab, backend)
    start_nfs(lab)
    env = node_env(backend, {"NFS_SERVER": "nfs", **({"NFS_OPTS": nfs_opts} if nfs_opts else {})})
    vols = backend.container_volumes()
    ctl = lab.run("slurmctl", role="slurmctl", networks=["cluster", "egress"], env=env,
                  volumes=vols, mount_caps=True, cpus=1, memory="1g")
    nodes = [
        # `<name>-hsn` resolves to the node's CLUSTER address only: DDP traffic
        # must stay on the cluster network when a test cuts `egress`.
        lab.run(name, role="slurmd", networks=[("cluster", [f"{name}-hsn"]), "egress"], env=env,
                volumes=vols, mount_caps=True, cpus=2, memory="3g")
        for name in ("c1", "c2")
    ]
    lab.wait_for(
        "both Slurm nodes idle",
        lambda: ctl.sh("sinfo -h -o '%t %D'", user=None, check=False, timeout=30).split()
        == ["idle", "2"],
        timeout=90, interval=2,
    )
    return SlurmCluster(lab, backend, ctl, nodes)


def job_script(tag: str, *, steps: int, sleep: float = 0.0, big_mb: int = 0, requeue: bool = False,
               extra_env: dict | None = None, hold_at_step: int = -1, resume: bool = False) -> str:
    """An sbatch script for 2 nodes x 1 task: torch gloo DDP across the nodes."""
    exports = "".join(f"export {k}={shlex.quote(str(v))}\n" for k, v in (extra_env or {}).items())
    args = f"--out {RESULTS}/{tag} --steps {steps} --sleep {sleep}"
    if big_mb:
        args += f" --big-mb {big_mb}"
    if hold_at_step >= 0:
        args += f" --hold-at-step {hold_at_step}"
    if resume or requeue:
        args += " --resume"
    return (
        "#!/bin/bash\n"
        "#SBATCH --nodes=2\n#SBATCH --ntasks-per-node=1\n"
        f"#SBATCH --output={RESULTS}/{tag}/slurm-%j-%t.out\n"
        + ("#SBATCH --requeue\n" if requeue else "#SBATCH --no-requeue\n")
        # Rank 0's node on the CLUSTER network (its -hsn alias), and each rank's
        # gloo interface the one that routes there -- never `egress`, which the
        # NFS test cuts mid-run.
        + "FIRST=$(scontrol show hostnames \"$SLURM_JOB_NODELIST\" | head -n1)\n"
        "export MASTER_ADDR=$(getent hosts \"$FIRST-hsn\" | awk '{print $1}')\n"
        "export MASTER_PORT=29500\n"
        + exports
        + "srun --kill-on-bad-exit=1 bash -c 'export GLOO_SOCKET_IFNAME=$(ip -o route get "
        "$(getent hosts nfs | awk \"{print \\$1}\") | sed -n \"s/.* dev \\([^ ]*\\).*/\\1/p\"); "
        f"exec python /harness/workload.py {args}'\n"
    )


def files_outside(container: Container, since_marker: str, allowed: tuple[str, ...]) -> list[str]:
    """Files the researcher created or changed since ``since_marker`` outside ``allowed``
    prefixes: what "nothing written outside expected dirs" checks."""
    out = container.sh(
        "find / -xdev \\( -path /proc -o -path /sys -o -path /dev -o -path /home \\) -prune "
        f"-o -user researcher -newer {since_marker} -print 2>/dev/null",
        user=None, check=False, timeout=120,
    )
    return [p for p in out.splitlines() if p and not p.startswith(allowed)]
