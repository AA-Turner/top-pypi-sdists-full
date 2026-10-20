"""The "super lightweight" promise, measured (plan S1, Q3, X7).

The service's start path imports the standard library and its own modules,
nothing else: no typer, httpx, pydantic, mcp, tiktoken. `import probe.service`
cannot avoid the `probe` package's own `__init__` (and the two small modules it
imports), so those are pinned by name: anything new there fails here too.
And it stays small after real traffic: RSS after 100 status/hello requests.
"""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from probe.service.protocol import Method
from tests.service_harness import service_home  # noqa: F401 -- a fixture

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the service is POSIX-only (plan S8)")

#: What `import probe` itself loads (probe/__init__.py -> probe.errors ->
#: probe.sdk.errors). Not the service's to change, but pinned: a heavy import
#: added to the package's __init__ lands on the service's start path.
PACKAGE_PARENTS = frozenset({"probe", "probe.errors", "probe.sdk", "probe.sdk.errors"})
#: The interpreter's own environment hooks (a venv's site customisation).
ENVIRONMENT = ("__main__", "_virtualenv", "_distutils_hack", "__editable__")
#: Sum of `-X importtime` self times, interpreter start included. ~65 ms on the
#: devbox; the ceiling leaves room for a shared CI runner, the allowlist is the
#: strict guard.
IMPORT_BUDGET_MS = 400
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
        and name != "probe.service"
        and not name.startswith("probe.service.")
        and not name.startswith(ENVIRONMENT)
    ]
    assert not offenders, f"the service's start path imports {offenders}"
    for heavy in ("typer", "httpx", "pydantic", "mcp", "tiktoken", "click", "probe.cli", "probe.sdk.client"):
        assert heavy not in modules


def test_import_time_is_under_budget():
    _, stderr = _selftest()
    total_us = 0
    for line in stderr.splitlines():
        if not line.startswith("import time:") or "self [us]" in line:
            continue
        total_us += int(line.split(":", 1)[1].split("|")[0].strip())
    assert 0 < total_us < IMPORT_BUDGET_MS * 1000, f"start path imports took {total_us / 1000:.0f} ms"


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
