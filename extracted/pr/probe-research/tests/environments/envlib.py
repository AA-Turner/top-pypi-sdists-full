"""Shared harness for the opt-in environment suite (``PROBE_ENV_TESTS=1``).

Every test here drives the RELEASED SDK (``probe-research`` from PyPI, in its own
interpreter: ``PROBE_ENV_PYTHON``, built by ``run.sh``) through the customer
loop -- init -> log (steps, nested dicts) -> update_config -> log_artifact ->
finish -- in a real child process, container or kernel, plus the failure mode of
its environment. The harness itself never imports the SDK under test.

TWO BACKENDS, ONE READ PATH. By default each test serves the agent suite's
``FakeApp`` over a real loopback socket (``tests/served_fake_app.py``), flagged
to declare what production declares (multipart, live logs, writer leases).
With ``PROBE_BASE_URL`` + ``PROBE_TOKEN`` + ``PROBE_E2E_PROJECT`` in the
environment the same tests run against that server instead. Either way the
results are READ BACK over HTTP (``GET /v1/runs/{id}``, ``.../metrics/export``,
``.../artifacts``, ``.../spans``), so the read code a production run relies on
is the code the fake runs exercise. Fault knobs (a busy server, a real-time
clock for liveness) exist only on the fake; against a real server they are
no-ops and a test reports what it could not arrange.
"""

from __future__ import annotations

import contextlib
import dataclasses
import functools
import json
import math
import os
import re
import shutil
import subprocess
import time
import uuid
from collections.abc import Iterator
from pathlib import Path

import httpx
import pytest

HERE = Path(__file__).resolve().parent
AGENT = HERE.parent.parent
#: The customer loop every environment runs (stdlib + the released SDK only).
CUSTOMER_LOOP = HERE / "customer_loop.py"

ENABLED = os.environ.get("PROBE_ENV_TESTS") == "1"
# Read ONCE, at import: the agent suite's autouse fixtures rewrite HOME and
# friends per test, and a real server's coordinates must survive that.
_REAL = {
    "url": os.environ.get("PROBE_BASE_URL") or "",
    "token": os.environ.get("PROBE_TOKEN") or "",
    "project": os.environ.get("PROBE_E2E_PROJECT") or "",
}
REAL_SERVER = bool(_REAL["url"] and _REAL["token"])

#: A file to append the evidence lines to (optional); they also go to stdout.
RESULTS_FILE = os.environ.get("PROBE_ENV_RESULTS") or ""
#: An SDK source tree (``.../agent/src``) the children import INSTEAD of the
#: released package (run.sh's PROBE_ENV_SDK_SRC): to check an unreleased fix.
#: Host children get it on PYTHONPATH; containers mount it at /sdk-src.
SDK_SRC = (os.environ.get("PROBE_ENV_SDK_SRC") or "").strip()

requires_env = pytest.mark.skipif(
    not ENABLED, reason="environment suite is opt-in: PROBE_ENV_TESTS=1 (see run.sh)"
)


# -- fixtures (each environment's conftest.py imports these) --------------------------


@pytest.fixture
def be():
    """A fresh backend per test: a prod-shaped served fake, or the real server
    named by PROBE_BASE_URL/PROBE_TOKEN/PROBE_E2E_PROJECT."""
    with backend() as backend_:
        yield backend_


@pytest.fixture(scope="session")
def sdk_py() -> str:
    return sdk_python()


@pytest.fixture(scope="session")
def sdk_version(sdk_py) -> str:
    """The released version under test (the base image's, when an SDK source
    tree overlays it: the evidence lines carry `sdk_src` then)."""
    return sdk_identity(sdk_py)["version"]


# -- the released SDK ----------------------------------------------------------------


def sdk_python() -> str:
    """The interpreter holding the released ``probe-research`` (run.sh builds it)."""
    py = os.environ.get("PROBE_ENV_PYTHON") or ""
    if not py or not Path(py).exists():
        # Fail, not skip: an opt-in run that skipped would read as a pass.
        pytest.fail("PROBE_ENV_PYTHON (an interpreter with the released SDK) is not set; use run.sh")
    return py


@functools.lru_cache(maxsize=None)
def sdk_identity(python: str) -> dict:
    """``{"version": ..., "file": ...}`` of the SDK that interpreter imports.

    Refuses an editable/in-repo install: this suite measures what customers run."""
    out = subprocess.run(
        [
            python,
            "-c",
            "import importlib.metadata as m, probe, json;"
            "print(json.dumps({'version': m.version('probe-research'), 'file': probe.__file__}))",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        env=_base_env(),  # no PYTHONPATH: the INSTALLED package's version
    )
    if out.returncode != 0:
        raise AssertionError(f"{python} cannot import the SDK: {out.stderr[-800:]}")
    ident = json.loads(out.stdout.strip().splitlines()[-1])
    if str(AGENT / "src") in ident["file"] and os.environ.get("PROBE_ENV_ALLOW_CHECKOUT_SDK") != "1":
        raise AssertionError(
            f"{python} imports the in-repo SDK ({ident['file']}), not a release "
            "(PROBE_ENV_ALLOW_CHECKOUT_SDK=1 permits it on purpose)"
        )
    ident["checkout"] = str(AGENT / "src") in ident["file"]
    return ident


def record(test: str, **fields) -> dict:
    """One machine-readable evidence line per test: printed, and appended to
    ``PROBE_ENV_RESULTS`` when set. Never carries a token."""
    line = {"test": test, "server": "real" if REAL_SERVER else "fake", **fields}
    if SDK_SRC:
        line["sdk_src"] = SDK_SRC
    text = json.dumps(line, sort_keys=True, default=str)
    print("ENV-RESULT " + text, flush=True)
    if RESULTS_FILE:
        with open(RESULTS_FILE, "a", encoding="utf-8") as fh:
            fh.write(text + "\n")
    return line


# -- the customer loop's values ------------------------------------------------------
# Mirrored in customer_loop.py (which may not import this file: it runs inside
# containers and kernels that have only the released SDK). Keep them in step;
# test_env_loop_values_match guards it.

KEYS = ("loss", "opt/lr", "opt/betas/b1")


def point_value(step: int, key: str) -> float:
    if key == "loss":
        return 1.0 / (step + 1)
    if key == "opt/lr":
        return step * 0.001
    if key == "opt/betas/b1":
        return 0.9 + (step % 7) * 0.001
    raise KeyError(key)


def expected_points(steps) -> dict[tuple[int, str], float]:
    return {(s, k): point_value(s, k) for s in steps for k in KEYS}


CONFIG = {"lr": 0.1, "model": {"layers": 4, "act": "gelu"}}


@dataclasses.dataclass
class Reconciliation:
    expected: int
    delivered: int
    missing: list
    mismatched: list
    duplicates: int
    unexpected: list

    @property
    def ok(self) -> bool:
        return not self.missing and not self.mismatched and not self.unexpected

    def summary(self) -> dict:
        return {
            "expected": self.expected,
            "delivered": self.delivered,
            "missing": len(self.missing),
            "missing_sample": sorted(self.missing)[:5],
            "mismatched": self.mismatched[:5],
            "duplicates": self.duplicates,
            "unexpected": self.unexpected[:5],
        }


def reconcile(expected: dict[tuple[int, str], float], points: list[dict]) -> Reconciliation:
    """Every logged (step, key, value) against the server's `model` points.

    A duplicate carrying the SAME value (a replay) is counted, not failed; two
    different values for one (step, key) are a mismatch whatever the order."""
    seen: dict[tuple[int, str], list[float]] = {}
    for p in points:
        if (p.get("kind") or "model") != "model" or p.get("step_index") is None:
            continue
        seen.setdefault((int(p["step_index"]), p["key"]), []).append(float(p["value"]))
    missing = [k for k in expected if k not in seen]
    mismatched = []
    duplicates = 0
    for key, values in seen.items():
        duplicates += len(values) - 1
        if key in expected and any(not math.isclose(v, expected[key], rel_tol=0, abs_tol=1e-12) for v in values):
            mismatched.append({"step": key[0], "key": key[1], "want": expected[key], "got": values[:3]})
    unexpected = sorted(k for k in seen if k not in expected and k[1] in KEYS)
    return Reconciliation(
        expected=len(expected),
        delivered=len([k for k in expected if k in seen]),
        missing=missing,
        mismatched=mismatched,
        duplicates=duplicates,
        unexpected=unexpected,
    )


# -- backends ------------------------------------------------------------------------


class Backend:
    """The server a test's children write to, and the one door it reads through."""

    url: str
    token: str
    project: str
    fake = None  # the FakeApp, on the fake backend only

    @property
    def is_fake(self) -> bool:
        return self.fake is not None

    # -- child wiring
    def env(self) -> dict[str, str]:
        return {"PROBE_BASE_URL": self.url, "PROBE_TOKEN": self.token}

    # -- reads (HTTP, both backends)
    def _get(self, path: str, **params):
        with httpx.Client(base_url=self.url, timeout=30.0) as http:
            resp = http.get(
                path,
                params={k: v for k, v in params.items() if v is not None} or None,
                headers={"Authorization": f"Bearer {self.token}"},
            )
        resp.raise_for_status()
        return resp.json()

    def run(self, run_id: str) -> dict:
        return self._get(f"/v1/runs/{run_id}")

    def points(self, run_id: str) -> list[dict]:
        out: list[dict] = []
        after = None
        for _ in range(10_000):
            page = self._get(f"/v1/runs/{run_id}/metrics/export", after_id=after, limit=5000)
            out.extend(page.get("points") or [])
            nxt = page.get("next_after_id")
            if nxt is None or (after is not None and nxt <= after):
                break
            after = nxt
        return out

    def artifacts(self, run_id: str) -> list[dict]:
        rows = self._get(f"/v1/runs/{run_id}/artifacts")
        return rows.get("items", rows) if isinstance(rows, dict) else rows

    def spans(self, run_id: str) -> list[dict]:
        rows = self._get(f"/v1/runs/{run_id}/spans")
        return rows.get("items", rows) if isinstance(rows, dict) else rows

    def wait_status(self, run_id: str, want: set[str], timeout: float) -> str | None:
        deadline = time.monotonic() + timeout
        status = None
        while True:
            status = self.run(run_id).get("status")
            if status in want or time.monotonic() >= deadline:
                return status
            time.sleep(1.0)

    def wait_points(self, run_id: str, expected: dict, timeout: float) -> Reconciliation:
        """Poll until every expected point is readable (or the timeout): a
        delivery the SDK handed to a detached worker lands after the child exits."""
        deadline = time.monotonic() + timeout
        while True:
            rec = reconcile(expected, self.points(run_id))
            if rec.ok or time.monotonic() >= deadline:
                return rec
            time.sleep(1.0)

    # -- fault knobs (fake only; real: no-op, returns False)
    def set_metrics_busy(self, on: bool) -> bool:
        return False


class RealBackend(Backend):
    def __init__(self) -> None:
        if not _REAL["project"]:
            raise AssertionError("PROBE_E2E_PROJECT is required with PROBE_BASE_URL/PROBE_TOKEN")
        self.url = _REAL["url"].rstrip("/")
        self.token = _REAL["token"]
        self.project = _REAL["project"]


_FAKE_STORE = b"http://r2.test"


class _ServedFake:
    """``FakeApp`` behind the loopback bridge, plus what a real server has and
    the in-process fake does not:

    * A WALL CLOCK for liveness. The fake's silence counters and lease expiry
      only move when a test moves them by hand; a child process cannot. Before
      every request this advances each run's silence by the real time elapsed
      and expires a lease unheard for ``max(3 x interval, 180 s)`` -- the
      server's rule (app/runs/writers.py).
    * The raw-point EXPORT of what was posted. ``FakeApp`` serves reads from a
      seeded store; this answers ``/metrics/export`` from the points the SDK
      actually POSTED (duplicates kept), in the server's page shape.
    * An object store the child can reach (see `handler`).
    """

    def __init__(self, app) -> None:
        self.app = app
        self.base = ""
        self._last = time.monotonic()
        self._beats: dict[tuple[str, str], tuple[int, float]] = {}

    def _tick(self) -> None:
        now = time.monotonic()
        dt, self._last = now - self._last, now
        for clock in (self.app.run_silence, self.app.run_beat_silence):
            for rid in list(clock):
                clock[rid] += dt
        for rid, leases in self.app.leases.items():
            for session, lease in leases.items():
                beats = int(lease.get("beats") or 0)
                seen = self._beats.get((rid, session))
                if seen is None or seen[0] != beats:
                    self._beats[(rid, session)] = (beats, now)
                    lease.pop("expired", None)
                    continue
                expiry = max(3 * float(lease.get("interval_seconds") or 60.0), 180.0)
                if now - seen[1] >= expiry:
                    lease["expired"] = True

    def _export(self, rid: str, params) -> httpx.Response:
        rows = [dict(p, id=i + 1) for i, p in enumerate(self.app.metric_points_posted.get(rid, []))]
        after = params.get("after_id")
        if after is not None:
            rows = [r for r in rows if r["id"] > int(after)]
        limit = int(params.get("limit") or 1000)
        page = rows[:limit]
        nxt = page[-1]["id"] if len(rows) > limit else None
        return httpx.Response(200, json={"points": page, "next_after_id": nxt})

    def handler(self, request: httpx.Request) -> httpx.Response:
        self._tick()
        m = re.fullmatch(r"/v1/runs/([^/]+)/metrics/export", request.url.path)
        if m and request.method == "GET":
            return self._export(m.group(1), request.url.params)
        resp = self.app.handler(request)
        # FakeApp hard-codes its object store as http://r2.test for multipart
        # part URLs and downloads (an in-process MockTransport routes any
        # host); a child process must reach THIS server for them.
        if self.base and _FAKE_STORE in resp.content:
            headers = {k: v for k, v in resp.headers.items() if k.lower() != "content-length"}
            return httpx.Response(
                resp.status_code,
                headers=headers,
                content=resp.content.replace(_FAKE_STORE, self.base.encode()),
            )
        return resp


class FakeBackend(Backend):
    def __init__(self, url: str, app) -> None:
        self.url = url
        self.token = "ros_pat_deadbeef"
        self.project = "env-suite"
        self.fake = app

    def set_metrics_busy(self, on: bool) -> bool:
        """Every metric POST answers production's contention 503 (Retry-After 2)
        while on: the run's writes queue in its outbox, in order."""
        self.fake.metrics_busy_retry_after = "2"
        self.fake.metrics_busy_next = 10**9 if on else 0
        return True


def _prod_shaped_fake():
    from tests.conftest import FakeApp

    app = FakeApp()
    # What production's /v1/server/features declares today (charts/research-os
    # values: multipart verifier on in managed prod; leases on by default).
    app.supports_artifact_multipart = True
    app.supports_run_log_stream = True
    app.supports_leases = True
    return app


@contextlib.contextmanager
def backend() -> Iterator[Backend]:
    if REAL_SERVER:
        yield RealBackend()
        return
    from tests.served_fake_app import serve

    app = _prod_shaped_fake()
    served = _ServedFake(app)
    with serve(served) as url:
        served.base = url
        app.upload_base = url  # presigned PUTs and part URLs reach the same fake
        be = FakeBackend(url, app)
        _create_project(be)
        yield be


def _create_project(be: Backend) -> None:
    with httpx.Client(base_url=be.url, timeout=30.0) as http:
        resp = http.post(
            "/v1/projects",
            json={"slug": be.project, "name": be.project, "kind": "general"},
            headers={"Authorization": f"Bearer {be.token}"},
        )
    assert resp.status_code in (200, 201, 409), resp.text


# -- children ------------------------------------------------------------------------


def _base_env() -> dict[str, str]:
    """A customer's environment, not this suite's: none of the agent suite's
    PROBE_* pins (hw off, reads off, flush attempts 1 ...) leak into a child."""
    keep = ("PATH", "LANG", "LC_ALL", "SYSTEMROOT", "COMSPEC", "PATHEXT", "WINDIR", "TZ")
    return {k: os.environ[k] for k in keep if k in os.environ}


def child_env(be: Backend, root: Path, **extra: str | None) -> dict[str, str]:
    """HOME, TMPDIR and XDG dirs under ``root``; the backend's URL/token;
    telemetry off. ``extra`` values of None REMOVE a variable."""
    home = root / "home"
    tmp = root / "tmp"
    home.mkdir(parents=True, exist_ok=True)
    tmp.mkdir(parents=True, exist_ok=True)
    env = {
        **_base_env(),
        "HOME": str(home),
        "USERPROFILE": str(home),  # Windows' Path.home() reads this, not HOME
        "TMPDIR": str(tmp),
        "TEMP": str(tmp),  # Windows' tempfile reads TEMP/TMP, not TMPDIR
        "TMP": str(tmp),
        "PYTHONUNBUFFERED": "1",
        "PROBE_TELEMETRY": "off",
        "PROBE_ENV_PROJECT": be.project,
        **be.env(),
    }
    for key, value in extra.items():
        if value is None:
            env.pop(key, None)
        else:
            env[key] = value
    if SDK_SRC:
        env["PYTHONPATH"] = os.pathsep.join(p for p in (env.get("PYTHONPATH"), SDK_SRC) if p)
    return env


def container_env(be: Backend, **extra: str) -> dict[str, str]:
    """What a managed job's container is given: the server and a token, and
    nothing of this host (its HOME, TMPDIR and PATH are the image's own)."""
    env = {
        "PYTHONUNBUFFERED": "1",
        "PROBE_TELEMETRY": "off",
        "PROBE_ENV_PROJECT": be.project,
        **be.env(),
        **extra,
    }
    if SDK_SRC:
        env["PYTHONPATH"] = "/sdk-src"
    return env


def sdk_src_mount() -> list[str]:
    """`docker run` args mounting PROBE_ENV_SDK_SRC at /sdk-src, if set."""
    return ["-v", f"{SDK_SRC}:/sdk-src:ro"] if SDK_SRC else []


@dataclasses.dataclass
class LoopEvents:
    """What customer_loop.py reported on stdout (``PROBE-ENV {json}`` lines)."""

    events: list[dict]

    @classmethod
    def parse(cls, text: str) -> "LoopEvents":
        out = []
        for line in text.splitlines():
            if line.startswith("PROBE-ENV "):
                try:
                    out.append(json.loads(line[len("PROBE-ENV "):]))
                except ValueError:
                    pass
        return cls(out)

    def first(self, event: str) -> dict | None:
        return next((e for e in self.events if e.get("event") == event), None)

    @property
    def run_id(self) -> str | None:
        e = self.first("run")
        return e and e.get("id")


def scan_new_files(root: Path, since: float) -> list[str]:
    """Files under ``root`` modified at or after ``since`` (best effort)."""
    found = []
    if not root.exists():
        return found
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            path = Path(dirpath) / name
            try:
                if path.stat().st_mtime >= since:
                    found.append(str(path))
            except OSError:
                continue
    return found


def real_home_writes(since: float, needles: list[str]) -> list[str]:
    """Probe state this test's child wrote into the REAL home of the account
    running the suite -- a child that escaped its redirected HOME/XDG dirs
    would land there.

    BEST EFFORT on a shared machine: other sessions write the same real dirs
    concurrently, so a new file counts only when its name or first 64 KB
    names something of THIS test (a run id, the test's temp root). Containers
    get the exact answer from `docker diff` instead."""
    try:
        import pwd

        real = Path(pwd.getpwuid(os.getuid()).pw_dir)
    except (ImportError, KeyError):
        real = Path(os.path.expanduser("~"))
    hits = []
    wanted = [n for n in needles if n]
    for sub in (".local/state/probe", ".config/probe", ".cache/probe"):
        for path in scan_new_files(real / sub, since):
            try:
                with open(path, "rb") as fh:
                    head = fh.read(65536).decode("utf-8", "replace")
            except OSError:
                head = ""
            if any(n in path or n in head for n in wanted):
                hits.append(path)
    return hits


# -- docker --------------------------------------------------------------------------


def docker_available() -> bool:
    if not shutil.which("docker"):
        return False
    try:
        return subprocess.run(["docker", "info"], capture_output=True, timeout=20).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


IMAGE_REPO = "probe-env-sdk"


def ensure_image(version: str) -> str:
    """``probe-env-sdk:<version>``: python:3.12-slim + the released SDK. Built
    on first use and kept for the next run; ``docker rmi`` it when done."""
    tag = f"{IMAGE_REPO}:{version}"
    have = subprocess.run(["docker", "image", "inspect", tag], capture_output=True, timeout=30)
    if have.returncode == 0:
        return tag
    built = subprocess.run(
        [
            "docker", "build", "--network", "host", "-q", "-t", tag,
            "--build-arg", f"SDK_VERSION={version}",
            str(HERE / "managed"),
        ],
        capture_output=True,
        text=True,
        timeout=900,
    )
    if built.returncode != 0:
        raise AssertionError(f"docker build failed: {built.stderr[-2000:]}")
    return tag


class Container:
    """One named container this test owns; always removed (with its disk)."""

    _n = 0

    def __init__(self, image: str, argv: list[str], *, env: dict[str, str], docker_args: list[str]):
        Container._n += 1
        self.name = f"probe-env-{os.getpid()}-{Container._n}-{uuid.uuid4().hex[:6]}"
        self.image = image
        self.argv = argv
        self.env = env
        self.docker_args = docker_args
        self.removed = False

    def start(self) -> None:
        # Values go through the docker CLI's OWN environment (`-e NAME`), so a
        # token never appears on an argv that `ps` can read.
        env_flags = [a for k in sorted(self.env) for a in ("-e", k)]
        cmd = [
            "docker", "run", "-d", "--name", self.name,
            "--network", "host", "--cpus", "2", "--memory", "1g",
            *self.docker_args, *env_flags, self.image, *self.argv,
        ]
        out = subprocess.run(
            cmd, env={**_base_env(), **self.env}, capture_output=True, text=True, timeout=120
        )
        if out.returncode != 0:
            raise AssertionError(f"docker run failed: {out.stderr[-2000:]}")

    def logs(self) -> str:
        out = subprocess.run(["docker", "logs", self.name], capture_output=True, text=True, timeout=60)
        return out.stdout + out.stderr

    def wait_for(self, marker: str, timeout: float) -> str:
        deadline = time.monotonic() + timeout
        while True:
            text = self.logs()
            if marker in text:
                return text
            if not self.running():
                raise AssertionError(f"container exited before {marker!r}:\n{text[-3000:]}")
            if time.monotonic() >= deadline:
                raise AssertionError(f"no {marker!r} within {timeout}s:\n{text[-3000:]}")
            time.sleep(0.25)

    def state(self) -> dict:
        out = subprocess.run(
            ["docker", "inspect", "--format", "{{json .State}}", self.name],
            capture_output=True, text=True, timeout=60,
        )
        return json.loads(out.stdout) if out.returncode == 0 else {}

    def running(self) -> bool:
        return bool(self.state().get("Running"))

    def wait_exit(self, timeout: float) -> int:
        out = subprocess.run(
            ["timeout", str(int(timeout)), "docker", "wait", self.name],
            capture_output=True, text=True, timeout=timeout + 30,
        )
        if out.returncode != 0:
            raise AssertionError(f"container still running after {timeout}s:\n{self.logs()[-3000:]}")
        return int(out.stdout.strip())

    def stop(self, grace: int) -> tuple[int, float]:
        """``docker stop -t grace``: SIGTERM, then SIGKILL after ``grace`` s --
        what Kubernetes, SageMaker, Vertex and a spot reclaim do. Returns
        (exit code, seconds the stop took)."""
        t = time.monotonic()
        subprocess.run(["docker", "stop", "-t", str(grace), self.name], capture_output=True, timeout=grace + 60)
        return int(self.state().get("ExitCode", -1)), time.monotonic() - t

    def diff(self) -> list[str]:
        """Every path the container changed in its own layer (tmpfs excluded)."""
        out = subprocess.run(["docker", "diff", self.name], capture_output=True, text=True, timeout=60)
        return [line for line in out.stdout.splitlines() if line.strip()]

    def remove(self) -> None:
        """The container AND its disk: nothing it queued survives."""
        if not self.removed:
            subprocess.run(["docker", "rm", "-f", "-v", self.name], capture_output=True, timeout=120)
            self.removed = True


#: Paths Docker itself adds to a container's layer: the bind-mount points this
#: suite uses and the `--init` binary. Never the SDK's doing.
DOCKER_INJECTED = ("/envtests", "/ckpt", "/sdk-src", "/usr/sbin/docker-init")


def writes_outside(diff: list[str], allowed: tuple[str, ...]) -> list[str]:
    """`docker diff` lines that ADD or DELETE a path outside the allowed
    prefixes. `C` (changed) lines only say a directory has a changed child,
    and that child has its own A/D line, so they are not counted."""
    allowed = (*allowed, *DOCKER_INJECTED)
    bad = []
    for line in diff:
        kind, _, path = line.partition(" ")
        if kind == "C" or "/__pycache__" in path:
            continue  # a parent of a real change; the interpreter's own bytecode cache
        if any(path == a or path.startswith(a.rstrip("/") + "/") for a in allowed):
            continue
        bad.append(line)
    return bad


def run_child(
    argv: list[str], *, env: dict[str, str], cwd: Path, timeout: float
) -> subprocess.CompletedProcess:
    """A host child with a HARD timeout: a hang is a failure, never a stuck suite."""
    try:
        return subprocess.run(argv, env=env, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        raise AssertionError(
            f"child hung past {timeout}s: {argv[:3]}\nstdout: {(exc.stdout or '')[-2000:]}\n"
            f"stderr: {(exc.stderr or '')[-2000:]}"
        ) from None


def sdk_warnings(text: str) -> list[str]:
    """The SDK's own warnings in a child's output, once each, shortened: what a
    customer sees on stderr (e.g. "output capture could not start")."""
    seen: list[str] = []
    for line in text.splitlines():
        _, sep, msg = line.partition("UserWarning: ")
        if sep:
            short = re.sub(r"[0-9a-f]{8}-[0-9a-f-]{27}", "<id>", msg.strip())[:160]
            if short not in seen:
                seen.append(short)
    return seen


def tail(text: str | bytes | None, n: int = 2500) -> str:
    if text is None:
        return ""
    if isinstance(text, bytes):
        text = text.decode("utf-8", "replace")
    return text[-n:]
