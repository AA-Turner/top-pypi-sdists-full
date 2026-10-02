"""Pytest-side harness for the opt-in environment suite (``agent/tests/environments``).

Each environment test runs the RELEASED SDK (``probe-research`` from PyPI, in the
venv ``run.sh`` builds) inside a real framework job, as a child process with a
hard timeout, and then checks what reached the server through the public read
API only -- never the fake's internals -- so the same test runs unchanged
against a real deployment:

* default: the agent suite's fake API, served on a loopback socket
  (``tests/served_fake_app.py``), with per-writer leases on (prod has them);
* ``PROBE_BASE_URL`` + ``PROBE_TOKEN`` (+ ``PROBE_E2E_PROJECT``) exported
  before pytest starts: that server instead. Nothing here reads a token from
  anywhere else.

The children get a clean environment: their own HOME / XDG dirs / TMPDIR
under the test's tmp dir, telemetry off, no PROBE_* / WANDB_* / agent-session
variables from the developer's shell, and the SDK's capture defaults left ON
(output capture, code snapshot, hardware, reads) -- the customer's defaults.
"""

from __future__ import annotations

import json
import math
import os
import re
import signal
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]

#: The shell's environment as pytest started, BEFORE the agent suite's autouse
#: fixtures rewrite HOME and pin test-only knobs for in-process tests.
_SHELL_ENV = dict(os.environ)

ENABLED = _SHELL_ENV.get("PROBE_ENV_TESTS") == "1"
REAL_URL = (_SHELL_ENV.get("PROBE_BASE_URL") or "").strip()
REAL_TOKEN = (_SHELL_ENV.get("PROBE_TOKEN") or "").strip()
REAL = bool(REAL_URL and REAL_TOKEN)
REAL_PROJECT = (_SHELL_ENV.get("PROBE_E2E_PROJECT") or "").strip()
#: The interpreter that runs the customer's script (the framework venv).
PYTHON = _SHELL_ENV.get("PROBE_ENV_PYTHON") or sys.executable
#: An SDK source tree (``.../agent/src``) the children import INSTEAD of the
#: venv's released package: to run the matrix against an unreleased fix.
SDK_SRC = (_SHELL_ENV.get("PROBE_ENV_SDK_SRC") or "").strip()
#: Real server only: how long to wait for the server to close a run whose
#: lease was killed (expiry 180 s, closure timer 600 s). 0 skips that wait.
CLOSE_WAIT = float(_SHELL_ENV.get("PROBE_ENV_CLOSE_WAIT_SEC") or 0)
#: Real server only: how long run_child() waits for the SDK's own detached
#: helpers -- the outbox sender and the output-capture "process died"
#: reporter -- among a killed child's marked processes to exit on their own,
#: before reap_marked() SIGKILLs whatever is still marked. Against the fake
#: server this is never consulted: uploads and crash reports land in-process
#: before the child exits, so grace 0 there changes nothing. 0 disables the
#: wait outright. See SDK_HELPER_MODULES.
SENDER_GRACE_SEC = float(_SHELL_ENV.get("PROBE_ENV_SENDER_GRACE_SEC") or 300)

requires_env = pytest.mark.skipif(
    not ENABLED, reason="opt-in suite: PROBE_ENV_TESTS=1 (agent/tests/environments/run.sh <env>)"
)

TERMINAL = {"completed", "failed", "canceled", "crashed"}

#: Variables of the developer's shell a customer's job would not have.
_STRIP_PREFIXES = (
    "PROBE_", "WANDB_", "RAY_", "CLAUDE", "CODEX", "PI_", "VIRTUAL_ENV", "CONDA",
    "PYTHON", "XDG_", "HF_", "TRANSFORMERS_", "ACCELERATE_", "JAX_", "XLA_",
    "MASTER_", "LOCAL_RANK", "RANK", "WORLD_SIZE", "SLURM_", "OMPI_", "DS_",
)


def requirement(module: str) -> None:
    """Fail (not skip) when the framework venv lacks ``module``: an opt-in run
    that silently skipped would read as a pass."""
    probe = subprocess.run(
        [PYTHON, "-c", f"import {module}"], capture_output=True, text=True, timeout=120
    )
    assert probe.returncode == 0, (
        f"{PYTHON} cannot import {module} -- build the venv with "
        f"agent/tests/environments/run.sh: {probe.stderr[-800:]}"
    )


@dataclass
class Target:
    """The server a test's children write to, and a reader for it."""

    url: str
    token: str
    project: str
    app: object | None  # the FakeApp when fake; None against a real server

    def reader(self):
        from probe.sdk import Client

        return Client(base_url=self.url, token=self.token, async_writes=False, auto_drain=False)


def make_fake_target(app) -> Target:
    """Bind a served FakeApp: leases on, uploads back through the socket, one
    project the children name."""
    app.supports_leases = True
    slug = "env-matrix"
    return Target(url="", token="ros_pat_deadbeef", project=slug, app=app)


@dataclass
class Dirs:
    root: Path
    home: Path
    work: Path
    tmp: Path
    art: Path


def make_dirs(tmp_path: Path) -> Dirs:
    d = Dirs(
        root=tmp_path,
        home=tmp_path / "home",
        work=tmp_path / "work",
        tmp=tmp_path / "t",
        art=tmp_path / "art",
    )
    for p in (d.home, d.work, d.tmp, d.art):
        p.mkdir(parents=True, exist_ok=True)
    return d


def child_env(target: Target, dirs: Dirs, **extra: str) -> dict[str, str]:
    """A customer's clean environment pointed at ``target``."""
    env = {
        k: v for k, v in _SHELL_ENV.items() if not k.startswith(_STRIP_PREFIXES)
    }
    env.update(
        HOME=str(dirs.home),
        XDG_CONFIG_HOME=str(dirs.home / ".config"),
        XDG_STATE_HOME=str(dirs.home / ".local" / "state"),
        XDG_CACHE_HOME=str(dirs.home / ".cache"),
        TMPDIR=str(dirs.tmp),
        PYTHONUNBUFFERED="1",
        # The venv's launchers (torchrun, accelerate, probe) come first.
        PATH=os.pathsep.join([str(Path(PYTHON).parent), _SHELL_ENV.get("PATH", "")]),
        # Child helpers only (envchild.py); the SDK comes from the venv
        # unless PROBE_ENV_SDK_SRC names a source tree.
        PYTHONPATH=os.pathsep.join([p for p in (SDK_SRC, str(HERE)) if p]),
        PROBE_BASE_URL=target.url,
        PROBE_TOKEN=target.token,
        PROBE_TELEMETRY="off",
        PROBE_ENV_PROJECT=target.project,
        PROBE_ENV_ART=str(dirs.art),
        # Frameworks that phone home or pick a GPU.
        WANDB_MODE="offline",
        WANDB_SILENT="true",
        HF_HUB_OFFLINE="1",
        TRANSFORMERS_OFFLINE="1",
        TOKENIZERS_PARALLELISM="false",
        CUDA_VISIBLE_DEVICES="",
        OMP_NUM_THREADS="1",
        MKL_NUM_THREADS="1",
        RAY_USAGE_STATS_ENABLED="0",
    )
    env.update({k: str(v) for k, v in extra.items()})
    return env


def child_env_offline(dirs: Dirs, **extra: str) -> dict[str, str]:
    """``child_env`` for a helper that talks to no Probe server (a reader)."""
    env = child_env(Target(url="", token="", project="", app=None), dirs, **extra)
    for key in ("PROBE_BASE_URL", "PROBE_TOKEN"):
        env.pop(key, None)
    return env


@dataclass
class Child:
    argv: list[str]
    returncode: int | None
    stdout: str
    stderr: str
    elapsed: float
    timed_out: bool
    results: list[dict] = field(default_factory=list)

    def tail(self, n: int = 4000) -> str:
        return (
            f"argv={self.argv} rc={self.returncode} timed_out={self.timed_out} "
            f"elapsed={self.elapsed:.1f}s\n--- stdout tail ---\n{self.stdout[-n:]}\n"
            f"--- stderr tail ---\n{self.stderr[-n:]}"
        )

    def result(self, tag: str | None = None) -> dict:
        rows = [r for r in self.results if tag is None or r.get("tag") == tag]
        assert rows, f"no PROBE_ENV_RESULT{'' if tag is None else ' ' + tag} line\n{self.tail()}"
        return rows[-1]


_RESULT = re.compile(r"PROBE_ENV_RESULT (\{.*\})\s*$", re.M)


def run_child(
    argv: list[str],
    *,
    env: dict[str, str],
    cwd: Path,
    timeout: float,
    on_start=None,
    helper_grace: float | None = None,
) -> Child:
    """Run ``argv`` in its own session with a HARD timeout: past it the whole
    process group is SIGKILLed, and so is any process whose command line
    names this test's tmp dir (Ray's raylet / GCS / workers).

    Against a real server (``REAL``), the SDK's own detached helpers --
    the outbox sender, the output-capture crash reporter -- may still be
    doing real work after the child exits (a big upload still in flight, a
    SIGKILLed run not yet reported). They get up to ``SENDER_GRACE_SEC`` to
    finish on their own before the marked-process sweep; everything else
    marked (Ray daemons, etc.) is reaped immediately, as always. Against the
    fake server nothing waits -- that delivery happens in-process before the
    child exits -- unless the test says otherwise with ``helper_grace``
    (seconds): a Ray Tune trial's close is queued for the outbox sender."""
    out_path = Path(cwd).parent / f"child-{uuid.uuid4().hex[:8]}.out"
    err_path = out_path.with_suffix(".err")
    started = time.monotonic()
    timed_out = False
    with open(out_path, "w") as out, open(err_path, "w") as err:
        proc = subprocess.Popen(
            argv, env=env, cwd=cwd, stdout=out, stderr=err, start_new_session=True
        )
        try:
            if on_start is not None:
                on_start(proc, out_path)
            proc.wait(timeout=max(1.0, timeout - (time.monotonic() - started)))
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            if proc.poll() is None:
                _kill_group(proc.pid)
                try:
                    proc.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    pass
    marker = str(Path(cwd).parent)
    grace = (SENDER_GRACE_SEC if REAL else 0.0) if helper_grace is None else helper_grace
    if grace > 0:
        wait_for_sdk_helpers(marker, grace)
    reap_marked(marker)
    stdout = out_path.read_text(errors="replace")
    stderr = err_path.read_text(errors="replace")
    seen: set[str] = set()
    results = []
    extra = env.get("PROBE_ENV_RESULTS_FILE")
    sources = [stdout] + ([Path(extra).read_text(errors="replace")] if extra and Path(extra).exists() else [])
    for text in sources:
        for m in _RESULT.finditer(text):
            if m.group(1) not in seen:  # the file repeats what stdout carried
                seen.add(m.group(1))
                results.append(json.loads(m.group(1)))
    return Child(
        argv=argv,
        returncode=None if timed_out else proc.returncode,
        stdout=stdout,
        stderr=stderr,
        elapsed=time.monotonic() - started,
        timed_out=timed_out,
        results=results,
    )


def _kill_group(pid: int) -> None:
    try:
        os.killpg(pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


#: The SDK's own detached helper modules (child_env's PATH puts the venv's
#: interpreter first; these are always ``python -m <module>``, so the module
#: name is a literal substring of /proc/<pid>/cmdline regardless of NUL
#: joining). Both outlive the run script on purpose:
#:   - the outbox sender, spawned by outbox_worker.maybe_spawn() at
#:     agent/src/probe/sdk/outbox_worker.py:463-464, delivers whatever is
#:     still queued (e.g. a big artifact upload) after the run process exits;
#:   - the output-capture "process died" reporter, spawned by
#:     _spawn_recovery()/_spawn_writer_gone() at
#:     agent/src/probe/sdk/logcapture.py:756 and :774 (both run
#:     agent/src/probe/sdk/outputs.py as ``--recover``/``--writer-gone``),
#:     tells the server a SIGKILLed run crashed instead of leaving it
#:     `running` forever.
SDK_HELPER_MODULES = ("probe.sdk.outbox_worker", "probe.sdk.outputs")


def _cmdline(pid: int) -> str:
    try:
        return (Path("/proc") / str(pid) / "cmdline").read_bytes().decode(errors="replace")
    except (OSError, PermissionError):
        return ""


def is_sdk_helper_cmdline(cmd: str) -> bool:
    """True when a marked process's cmdline is one of ``SDK_HELPER_MODULES``
    (the outbox sender or the output-capture crash reporter) rather than
    something else ``marked_pids`` caught, e.g. a Ray daemon."""
    return any(module in cmd for module in SDK_HELPER_MODULES)


def marked_pids(marker: str) -> list[int]:
    """PIDs whose command line or environment names ``marker`` (this test's
    tmp dir): only processes this test started can carry it."""
    pids = []
    me = os.getpid()
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit() or int(entry.name) == me:
            continue
        try:
            cmd = (entry / "cmdline").read_bytes().decode(errors="replace")
            if marker in cmd:
                pids.append(int(entry.name))
                continue
            environ = (entry / "environ").read_bytes().decode(errors="replace")
        except (OSError, PermissionError):
            continue
        if f"TMPDIR={marker}" in environ or f"HOME={marker}" in environ:
            pids.append(int(entry.name))
    return pids


def sdk_helper_pids(marker: str) -> list[int]:
    """The subset of ``marked_pids(marker)`` that are the SDK's own detached
    helpers (see ``SDK_HELPER_MODULES``)."""
    return [pid for pid in marked_pids(marker) if is_sdk_helper_cmdline(_cmdline(pid))]


def wait_for_sdk_helpers(marker: str, timeout: float) -> list[int]:
    """Real-server mode only: let the SDK's own detached helpers among this
    test's marked processes (the outbox sender, the output-capture crash
    reporter) exit on their own for up to ``timeout`` seconds. Kills nothing
    -- every other marked process (Ray daemons, etc.) is left exactly as
    ``marked_pids`` found it, for ``reap_marked`` to SIGKILL right after this
    returns, same as today. Returns whichever helper pids are still alive
    when the wait ends."""
    if timeout <= 0:
        return sdk_helper_pids(marker)
    deadline = time.monotonic() + timeout
    remaining = sdk_helper_pids(marker)
    while remaining and time.monotonic() < deadline:
        time.sleep(0.5)
        remaining = sdk_helper_pids(marker)
    return remaining


def reap_marked(marker: str, grace: float = 0.0) -> list[int]:
    """SIGKILL every process ``marked_pids`` finds; returns them."""
    if grace:
        deadline = time.monotonic() + grace
        while time.monotonic() < deadline and marked_pids(marker):
            time.sleep(0.5)
    pids = marked_pids(marker)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
    return pids


def script(env_dir: str, name: str) -> str:
    return str(HERE / env_dir / name)


# -- reads (public API only) --------------------------------------------------


def wait_status(reader, run_id: str, want: set[str] = TERMINAL, timeout: float = 60.0) -> str | None:
    deadline = time.monotonic() + timeout
    status = None
    while True:
        status = reader.get_run(run_id).get("status")
        if status in want or time.monotonic() >= deadline:
            return status
        time.sleep(1.0)


def points(reader, run_id: str) -> dict[tuple[int, str], list[float]]:
    got: dict[tuple[int, str], list[float]] = {}
    for p in reader.export_metric_points(run_id, limit=5000):
        if p.get("labels"):
            continue
        got.setdefault((p.get("step_index"), p["key"]), []).append(p.get("value"))
    return got


def reconcile(
    reader, run_id: str, expected: dict[tuple[int, str], float], timeout: float = 60.0
) -> tuple[list, list, dict]:
    """Every expected (step, key) exactly once with its value. Polls: a real
    server lands points asynchronously. Returns (missing, wrong, got)."""
    deadline = time.monotonic() + timeout
    while True:
        got = points(reader, run_id)
        missing = [k for k in expected if k not in got]
        wrong = [
            (k, expected[k], got[k])
            for k in expected
            if k in got and (len(got[k]) != 1 or not _close(got[k][0], expected[k]))
        ]
        if (not missing and not wrong) or time.monotonic() >= deadline:
            return missing, wrong, got
        time.sleep(1.0)


def _close(a, b) -> bool:
    try:
        fa, fb = float(a), float(b)
    except (TypeError, ValueError):
        return a == b
    if math.isnan(fa) or math.isnan(fb):
        return math.isnan(fa) and math.isnan(fb)
    if math.isinf(fa) or math.isinf(fb):
        return fa == fb
    return abs(fa - fb) <= 1e-9 * max(1.0, abs(fb))


def ledger_expected(ledger: list) -> dict[tuple[int, str], float]:
    """A child's ``[[step, key, value], ...]`` ledger as reconcile() input."""
    return {(int(s), k): v for s, k, v in ledger}


def writers(reader, run_id: str) -> list[dict]:
    try:
        return list(reader.list_writers(run_id))
    except Exception as exc:  # noqa: BLE001 -- a server without leases
        return [{"error": f"{type(exc).__name__}: {exc}"}]


def lease_summary(leases: list[dict]) -> list[tuple]:
    """(role, rank, released?, exit_status) per lease, sorted -- the shape the
    assertions and the report read. An unreleased lease someone reported
    gone (2.2: the output helper saw its process die) reads ``"gone"``."""
    rows = [
        (
            w.get("role"),
            w.get("rank"),
            bool(w.get("released_at")),
            w.get("exit_status")
            or ("gone" if (w.get("gone_at") or w.get("state") == "gone") else None),
        )
        for w in leases
        if "error" not in w
    ]
    return sorted(rows, key=lambda r: (str(r[0]), -1 if r[1] is None else r[1], str(r[3])))


def artifacts(reader, run_id: str) -> dict[str, dict]:
    rows = reader.list_run_artifacts(run_id)
    rows = rows.get("items", rows) if isinstance(rows, dict) else rows
    return {r.get("name"): r for r in rows}


def wait_artifacts(reader, run_id: str, names: set[str], timeout: float = 90.0) -> dict[str, dict]:
    deadline = time.monotonic() + timeout
    while True:
        got = artifacts(reader, run_id)
        live = {n for n in names if n in got and got[n].get("status") in (None, "complete", "live")}
        if live == names or time.monotonic() >= deadline:
            return got
        time.sleep(1.0)


# -- nothing written outside the expected dirs ---------------------------------


def leaked_files(run_ids: list[str], since: float) -> list[str]:
    """Files modified since ``since`` OUTSIDE the test's tmp dir that name one
    of ``run_ids``: the real home's probe dirs, /tmp, and this checkout. The
    SDK writes run ids into its outbox, intents and breadcrumbs, so a write
    that escaped the child's HOME / TMPDIR / cwd shows up here."""
    real_home = Path(_SHELL_ENV.get("HOME") or Path.home())
    roots = [
        real_home / ".config" / "probe",
        real_home / ".local" / "state" / "probe",
        real_home / ".cache" / "probe",
        Path("/tmp"),
        REPO,
    ]
    needles = [r.encode() for r in run_ids if r]
    hits: list[str] = []
    for root in roots:
        if not root.exists():
            continue
        depth = 3 if root == Path("/tmp") else 8
        for path in _walk_newer(root, since, depth):
            try:
                if path.stat().st_size > 8 * 1024 * 1024:
                    continue
                data = path.read_bytes()
            except OSError:
                continue
            if any(n in data for n in needles):
                hits.append(str(path))
    return hits


#: Directories the tests themselves own (pytest's basetemp): expected writes.
ALLOWED_ROOTS: list[Path] = []


def _walk_newer(root: Path, since: float, depth: int):
    skip = {".git", "node_modules", ".venv", ".venv-agent", "__pycache__"}
    allowed = {str(p) for p in ALLOWED_ROOTS}
    stack = [(root, 0)]
    while stack:
        d, level = stack.pop()
        try:
            entries = list(os.scandir(d))
        except OSError:
            continue
        for e in entries:
            try:
                if e.is_symlink():
                    continue
                if e.is_dir():
                    if e.path in allowed:
                        continue
                    if level < depth and e.name not in skip and not e.name.startswith("pytest-of"):
                        stack.append((Path(e.path), level + 1))
                elif e.is_file() and e.stat().st_mtime >= since:
                    yield Path(e.path)
            except OSError:
                continue
