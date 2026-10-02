"""Docker plumbing for the cluster environment tests: one ``Lab`` per test.

Every container, network and volume a Lab makes carries the label
``probe.envtest=<lab id>`` and is removed on close -- and only those: a shared box
runs other people's containers, so nothing here prunes or matches by name.
Every docker call has a hard timeout.
"""

from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE_DIR = HERE / "image"
IMAGE_REPO = "probe-envtest-cluster"
LABEL = "probe.envtest"
#: The researcher every workload runs as: the same uid on every node.
USER = "researcher"
HOME = "/home/researcher"


class DockerError(RuntimeError):
    pass


def docker(*args: str, timeout: float = 120, check: bool = True, env: dict | None = None,
           input: str | None = None) -> subprocess.CompletedProcess:
    try:
        proc = subprocess.run(
            ["docker", *args], capture_output=True, text=True, timeout=timeout, env=env, input=input
        )
    except subprocess.TimeoutExpired as exc:
        raise DockerError(f"docker {shlex.join(args)[:300]} timed out after {timeout}s") from exc
    if check and proc.returncode != 0:
        raise DockerError(
            f"docker {shlex.join(args)[:300]} -> {proc.returncode}\n{proc.stderr[-2000:]}"
        )
    return proc


def docker_available() -> str | None:
    """None when docker works, else why not."""
    try:
        docker("info", "--format", "{{.ServerVersion}}", timeout=20)
    except (DockerError, FileNotFoundError) as exc:
        return f"docker unavailable: {exc}"
    return None


def released_sdk_version() -> str:
    """``PROBE_ENV_SDK_VERSION``, else the newest probe-research on PyPI: these tests
    are about the RELEASED SDK, and an image built last week must not silently keep
    testing last week's release."""
    pinned = os.environ.get("PROBE_ENV_SDK_VERSION", "").strip()
    if pinned:
        return pinned
    import urllib.request

    with urllib.request.urlopen("https://pypi.org/pypi/probe-research/json", timeout=30) as resp:
        return json.load(resp)["info"]["version"]


def _image_dir_digest() -> str:
    digest = hashlib.sha256()
    for path in sorted(IMAGE_DIR.iterdir()):
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()[:10]


def image_tag(sdk: str) -> str:
    """The tag for the current image sources and SDK version: an edit to the image
    files or a new release builds a new image instead of reusing a stale one."""
    return f"{IMAGE_REPO}:{sdk}-{_image_dir_digest()}"


def ensure_image(timeout: float = 1800) -> str:
    sdk_src = os.environ.get("PROBE_ENV_SDK_SRC", "").strip()
    if sdk_src:
        # The mounted source tree (see Lab.run's PYTHONPATH=/sdk-src wiring below)
        # shadows whatever version gets installed here, so pinning to an exact
        # release only exposes the build to PyPI's simple index refusing to serve
        # that old version during one of its maintenance windows. Build unpinned
        # instead -- pip resolves the newest version it can.
        tag = f"{IMAGE_REPO}:src-{_image_dir_digest()}"
        if docker("image", "inspect", tag, check=False, timeout=30).returncode == 0:
            return tag
        docker("build", "-t", tag, "--build-arg", "PROBE_SDK_UNPINNED=1", str(IMAGE_DIR),
               timeout=timeout)
        return tag
    sdk = released_sdk_version()
    tag = image_tag(sdk)
    if docker("image", "inspect", tag, check=False, timeout=30).returncode == 0:
        return tag
    docker("build", "-t", tag, "--build-arg", f"PROBE_SDK_VERSION={sdk}", str(IMAGE_DIR),
           timeout=timeout)
    return tag


def sdk_version(tag: str) -> str:
    return docker("run", "--rm", "--entrypoint", "cat", tag, "/etc/probe-sdk-version",
                  timeout=60).stdout.strip()


def nfsd_available() -> str | None:
    """None when the host kernel can run an NFS server in a container, else why not.

    Kernel nfsd is per network namespace but the MODULE is the host's. Loading it
    is the one host change these tests make (`sudo -n modprobe nfsd`); it starts
    no server in the host's own namespace."""
    if Path("/proc/fs/nfsd").exists() or "nfsd" in Path("/proc/modules").read_text():
        return None
    proc = subprocess.run(["sudo", "-n", "modprobe", "nfsd"], capture_output=True, text=True,
                          timeout=30)
    if proc.returncode == 0:
        return None
    return f"host kernel module nfsd is not loaded and `sudo -n modprobe nfsd` failed: {proc.stderr.strip()}"


@dataclass
class Container:
    lab: "Lab"
    name: str  # the short name, which is also its hostname and network alias
    cid: str

    @property
    def full_name(self) -> str:
        return f"{self.lab.prefix}-{self.name}"

    def exec(self, cmd: str | list[str], *, user: str | None = USER, env: dict | None = None,
             timeout: float = 120, check: bool = True, detach: bool = False,
             workdir: str | None = None) -> subprocess.CompletedProcess:
        """Run ``cmd`` in the container. ``env`` values travel through the docker CLI's
        own environment (``-e NAME`` without a value), never its argv, so a real
        token passed here does not appear in the host's process list."""
        args = ["exec"]
        if detach:
            args.append("-d")
        if user:
            args += ["-u", user]
            args += ["-e", f"HOME={HOME}", "-e", f"USER={user}", "-e", f"LOGNAME={user}"]
        if workdir:
            args += ["-w", workdir]
        cli_env = dict(os.environ)
        for key, value in (env or {}).items():
            args += ["-e", key]
            cli_env[key] = str(value)
        argv = ["bash", "-lc", cmd] if isinstance(cmd, str) else list(cmd)
        return docker(*args, self.cid, *argv, timeout=timeout, check=check, env=cli_env)

    def sh(self, cmd: str, **kw) -> str:
        return self.exec(cmd, **kw).stdout

    def read(self, path: str, *, user: str | None = USER, timeout: float = 60) -> str | None:
        proc = self.exec(["cat", path], user=user, timeout=timeout, check=False)
        return proc.stdout if proc.returncode == 0 else None

    def kill(self, signal: str = "KILL") -> None:
        docker("kill", "--signal", signal, self.cid, timeout=60, check=False)

    def logs(self, tail: int = 200) -> str:
        proc = docker("logs", "--tail", str(tail), self.cid, timeout=60, check=False)
        return (proc.stdout + proc.stderr)[-20000:]

    def running(self) -> bool:
        proc = docker("inspect", "-f", "{{.State.Running}}", self.cid, timeout=30, check=False)
        return proc.stdout.strip() == "true"

    def connect(self, network: str) -> None:
        docker("network", "connect", "--alias", self.name, self.lab.net(network), self.cid,
               timeout=60)

    def disconnect(self, network: str) -> None:
        docker("network", "disconnect", "--force", self.lab.net(network), self.cid, timeout=60)


@dataclass
class Lab:
    image: str
    lab_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    containers: dict[str, Container] = field(default_factory=dict)
    networks: dict[str, str] = field(default_factory=dict)
    volumes: list[str] = field(default_factory=list)

    @property
    def prefix(self) -> str:
        return f"envc-{self.lab_id}"

    def net(self, name: str) -> str:
        return self.networks[name]

    def network(self, name: str, *, internal: bool = False) -> str:
        full = f"{self.prefix}-{name}"
        args = ["network", "create", "--label", f"{LABEL}={self.lab_id}"]
        if internal:
            args.append("--internal")
        docker(*args, full, timeout=60)
        self.networks[name] = full
        return full

    def volume(self, name: str) -> str:
        full = f"{self.prefix}-{name}"
        docker("volume", "create", "--label", f"{LABEL}={self.lab_id}", full, timeout=60)
        self.volumes.append(full)
        return full

    def run(self, name: str, *, role: str, networks: list, env: dict | None = None,
            volumes: list[str] = (), privileged: bool = False, mount_caps: bool = False,
            cpus: float = 2.0, memory: str = "3g", aliases: list[str] = (),
            extra: list[str] = ()) -> Container:
        args = [
            "run", "-d", "--name", f"{self.prefix}-{name}", "--hostname", name,
            "--label", f"{LABEL}={self.lab_id}", "--cpus", str(cpus), "--memory", memory,
            "-e", f"ROLE={role}", "-v", f"{HERE}:/harness:ro",
        ]
        for net in networks:
            # A network is a name, or (name, [aliases on that network only]).
            net, own = (net, []) if isinstance(net, str) else net
            spec = f"name={self.net(net)},alias={name}"
            for alias in [*aliases, *own]:
                spec += f",alias={alias}"
            args += ["--network", spec]
        for key, value in (env or {}).items():
            args += ["-e", f"{key}={value}"]
        sdk_src = os.environ.get("PROBE_ENV_SDK_SRC", "").strip()
        if sdk_src:
            # An unreleased fix: every Python process in the container -- the
            # workload, `probe` commands, the detached sender they spawn -- imports
            # this tree's SDK ahead of the released one baked into the image.
            args += ["-v", f"{Path(sdk_src).resolve()}:/sdk-src:ro", "-e", "PYTHONPATH=/sdk-src"]
        for vol in volumes:
            args += ["-v", vol]
        if privileged:
            args.append("--privileged")
        elif mount_caps:
            # Enough to mount NFS, no more: SYS_ADMIN for mount(2), and AppArmor's
            # docker-default profile denies mount outright.
            args += ["--cap-add", "SYS_ADMIN", "--security-opt", "apparmor=unconfined"]
        args += list(extra)
        cid = docker(*args, self.image, timeout=120).stdout.strip()
        container = Container(self, name, cid)
        self.containers[name] = container
        return container

    def __getitem__(self, name: str) -> Container:
        return self.containers[name]

    def wait_for(self, what: str, predicate, *, timeout: float, interval: float = 1.0):
        deadline = time.monotonic() + timeout
        last = None
        while time.monotonic() < deadline:
            try:
                last = predicate()
            except DockerError as exc:
                last = exc
                last_ok = False
            else:
                last_ok = bool(last)
            if last_ok:
                return last
            time.sleep(interval)
        raise TimeoutError(f"timed out after {timeout}s waiting for {what} (last: {last!r})")

    def diagnostics(self) -> str:
        parts = []
        for c in self.containers.values():
            parts.append(f"===== {c.name} (running={c.running()})\n{c.logs(80)}")
        return "\n".join(parts)

    def close(self) -> None:
        close_lab(self.lab_id)


def close_lab(lab_id: str) -> None:
    """Remove one lab's containers, networks and volumes -- only what carries its
    label, never anything matched by name -- in an order NFS can survive.

    NFS clients FIRST, the server LAST. A client whose server is gone cannot finish
    returning its NFSv4 delegations while its processes exit: they sit in
    uninterruptible sleep (`_nfs4_proc_delegreturn`) and the container cannot be
    removed until the kernel gives up, minutes later. So each client's researcher
    processes are killed and /home unmounted while the server still answers."""
    ids = docker("ps", "-aq", "--filter", f"label={LABEL}={lab_id}", timeout=60,
                 check=False).stdout.split()
    roles = {}
    for cid in ids:
        env = docker("inspect", "-f", "{{range .Config.Env}}{{println .}}{{end}}", cid,
                     timeout=30, check=False).stdout.splitlines()
        roles[cid] = {line.split("=", 1)[0]: line.split("=", 1)[1] for line in env if "=" in line}
    clients = [c for c in ids if roles[c].get("NFS_SERVER")]
    servers = [c for c in ids if roles[c].get("ROLE") == "nfs"]
    others = [c for c in ids if c not in clients and c not in servers]
    for cid in clients:
        docker("exec", cid, "sh", "-c",
               "pkill -KILL -u researcher; sleep 1; umount -f /home 2>/dev/null || umount -l /home",
               timeout=60, check=False)
    for group in (clients, others):
        if group:
            docker("rm", "-f", "-v", *group, timeout=180, check=False)
    # The server: stop kernel nfsd while rpcbind in the same container still
    # answers. Killed outright, nfsd's shutdown unregisters from an rpcbind that
    # is already dying and hangs in `svc_unregister` until the RPC times out.
    for cid in servers:
        docker("exec", cid, "sh", "-c", "exportfs -ua; rpc.nfsd 0", timeout=60, check=False)
    if servers:
        docker("rm", "-f", "-v", *servers, timeout=180, check=False)
    for kind in ("network", "volume"):
        names = docker(kind, "ls", "-q", "--filter", f"label={LABEL}={lab_id}", timeout=60,
                       check=False).stdout.split()
        for name in names:
            docker(kind, "rm", name, timeout=60, check=False)


def json_lines(text: str | None) -> list[dict]:
    out = []
    for line in (text or "").splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass  # a torn last line from a killed writer
    return out
