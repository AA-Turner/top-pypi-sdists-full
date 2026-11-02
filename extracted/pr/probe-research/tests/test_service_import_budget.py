"""The "super lightweight" promise, measured (plan S1, Q3, X7).

The service's start path imports the standard library and its own modules,
nothing else: no typer, httpx, pydantic, mcp, tiktoken. `import probe.service`
cannot avoid the `probe` package's own `__init__` (and the two small modules it
imports), so those are pinned by name: anything new there fails here too.
And it stays small after real traffic: RSS after 100 status/hello requests.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import time

import pytest

from probe.foundation.service_api.wire import Method
from tests.service_harness import service_home  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

#: What `import probe` itself loads (probe/__init__.py -> probe.errors ->
#: probe.sdk.errors). Not the service's to change, but pinned: a heavy import
#: added to the package's __init__ lands on the service's start path.
PACKAGE_PARENTS = frozenset({"probe", "probe.errors", "probe.sdk", "probe.sdk.errors"})
#: The update child's contract the service shares with the CLI (agent:12: one definition where the
#: service restated it): stdlib only, pinned by name like the parents above.
UPDATE_CONTRACT = frozenset({"probe.shared", "probe.shared.updates", "probe.shared.updates.step"})
#: The service's client side and the two stdlib-only helpers its split pieces use (agent:16):
#: `foundation/service_api` is the client the tap vendors, `front_door` serves old module paths,
#: `compose` folds a split class's parts back into it.
SERVICE_FOUNDATION = ("probe.foundation.service_api", "probe.foundation.front_door", "probe.foundation.compose")
#: The interpreter's own environment hooks (a venv's site customisation).
ENVIRONMENT = ("__main__", "_virtualenv", "_distutils_hack", "__editable__")
#: CPU time (user + system) of the start path: interpreter start, imports and the
#: self-test. ~130 ms on the devbox; the ceiling leaves room for a slower runner, the
#: allowlist is the strict guard. CPU, not a stopwatch: a starved runner stretched the
#: wall-clock import times to 1013 ms best of 5 (1111 ms on one core beside 8 busy
#: loops, where the CPU time stays ~160 ms).
IMPORT_BUDGET_MS = 400
#: A hang guard only: an import that blocks (a DNS lookup, a lock) costs no CPU.
WALL_CEILING_S = 5.0
RSS_BUDGET_MB = 40


def _selftest() -> tuple[list[str], str]:
    # The flags `client.ensure` spawns the service with.
    done = subprocess.run(
        [sys.executable, "-I", "-X", "importtime", "-m", "probe.service", "--selftest"],
        capture_output=True,
        text=True,
        timeout=60,
        cwd="/",
    )
    assert done.returncode == 0, done.stderr[-2000:]
    return json.loads(done.stdout), done.stderr


def test_the_start_path_imports_only_the_stdlib_and_the_service():
    modules, _ = _selftest()
    stdlib = sys.stdlib_module_names
    offenders = [
        name
        for name in modules
        if name.split(".")[0] not in stdlib
        and name not in PACKAGE_PARENTS
        and name not in UPDATE_CONTRACT
        and name != "probe.service"
        and not name.startswith("probe.service.")
        and name != "probe.foundation"
        and not name.startswith(SERVICE_FOUNDATION)
        and not name.startswith(ENVIRONMENT)
    ]
    assert not offenders, f"the service's start path imports {offenders}"
    for heavy in ("typer", "httpx", "pydantic", "mcp", "tiktoken", "click", "probe.cli", "probe.sdk.client"):
        assert heavy not in modules


def _start_path_cpu() -> tuple[int, float, str]:
    """The start path's CPU time in microseconds (`os.wait4`: this child's alone), its wall
    time in seconds, and its `-X importtime` report, for the failure message."""
    started = time.monotonic()
    with tempfile.TemporaryFile() as stderr:
        child = subprocess.Popen(
            [sys.executable, "-I", "-X", "importtime", "-m", "probe.service", "--selftest"],
            stdout=subprocess.DEVNULL,
            stderr=stderr,
            cwd="/",
        )
        watchdog = threading.Timer(60, child.kill)
        watchdog.start()
        try:
            _, status, usage = os.wait4(child.pid, 0)
        finally:
            watchdog.cancel()
        wall_s = time.monotonic() - started
        child.returncode = os.waitstatus_to_exitcode(status)
        stderr.seek(0)
        report = stderr.read().decode(errors="replace")
    assert child.returncode == 0, report[-2000:]
    return int((usage.ru_utime + usage.ru_stime) * 1_000_000), wall_s, report


def _slowest_imports(report: str, count: int = 8) -> list[str]:
    timed = []
    for line in report.splitlines():
        if line.startswith("import time:") and "self [us]" not in line:
            self_us, _cumulative, name = line.split(":", 1)[1].split("|")
            timed.append((int(self_us), name.strip()))
    return [f"{name} {us / 1000:.0f} ms" for us, name in sorted(timed, reverse=True)[:count]]


def test_import_time_is_under_budget():
    # The fastest of a few is the cost of the start path; a real regression is
    # slow in every one of them.
    runs = [_start_path_cpu() for _ in range(5)]
    best_us, _wall_s, report = min(runs)
    assert min(wall_s for _us, wall_s, _report in runs) < WALL_CEILING_S, "the start path hangs"
    assert 0 < best_us < IMPORT_BUDGET_MS * 1000, (
        f"the start path took {best_us / 1000:.0f} ms of CPU (best of 5); slowest imports: "
        f"{_slowest_imports(report)}"
    )


def _rss_kb(pid: int) -> int:
    try:
        for line in open(f"/proc/{pid}/status", encoding="utf-8"):
            if line.startswith("VmRSS:"):
                return int(line.split()[1])
    except OSError:
        pass
    out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, check=True)
    return int(out.stdout.strip())


def test_rss_after_a_hundred_requests_is_under_budget(service_home):
    status = service_home.start()
    with service_home.connect() as conn:
        conn.sock.settimeout(60)  # status.get waits for a `probe.core.run status` child (~1 s, more on a busy runner)
        for i in range(100):
            if i % 3 == 0:
                conn.call(Method.STATUS_GET, {})  # one child run, then the 30 s cache
            elif i % 3 == 1:
                conn.call(Method.STATUS)
            else:
                conn.hello("cli", "test")
    rss_mb = _rss_kb(status["pid"]) / 1024
    assert rss_mb < RSS_BUDGET_MB, f"service RSS {rss_mb:.1f} MB after 100 requests"
