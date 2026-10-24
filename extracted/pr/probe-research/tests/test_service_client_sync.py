"""The tap's copy of the service client must be the canonical one, byte for byte.

`plugins/probe-research-tap/tap/service/{client,paths,procid,protocol}.py` are
COPIES of `src/probe/service/`: the tap runs under the system python with only
the plugin root on sys.path, and pi reaches the client through the tap (`python
-m tap service ...`), so neither can import `probe`. One client, one identity
function (procid: the tap's owner record and the service's check read the same
{pid, start}). `make sync-service-client` reconciles them; this fails when
someone edits one side only (plan A1/R7).
"""

from __future__ import annotations

import ast
import filecmp
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_CANONICAL = _ROOT / "src" / "probe" / "service"
_TAP_ROOT = _ROOT / "plugins" / "probe-research-tap"
_COPY = _TAP_ROOT / "tap" / "service"

_SYNCED = ("client.py", "paths.py", "procid.py", "protocol.py", "winpipe.py")


def _makefile_list() -> list[str]:
    for line in (_ROOT / "Makefile").read_text(encoding="utf-8").splitlines():
        if line.startswith("SERVICE_CLIENT_FILES :="):
            return line.split(":=", 1)[1].split()
    raise AssertionError("Makefile has no SERVICE_CLIENT_FILES")


def test_the_makefile_syncs_exactly_these_files():
    assert sorted(_makefile_list()) == sorted(_SYNCED)


@pytest.mark.parametrize("name", _SYNCED)
def test_tap_copy_is_byte_identical(name):
    canonical, copy = _CANONICAL / name, _COPY / name
    assert copy.is_file(), f"tap copy of {name} is missing; run `make sync-service-client`"
    assert filecmp.cmp(canonical, copy, shallow=False), (
        f"plugins/probe-research-tap/tap/service/{name} drifted from src/probe/service/{name}: "
        "edit the canonical file and run `make sync-service-client`"
    )


@pytest.mark.parametrize("name", _SYNCED)
def test_synced_files_import_only_the_stdlib_and_each_other(name):
    """Identical bytes must resolve as both `probe.service.*` and `tap.service.*`."""
    tree = ast.parse((_CANONICAL / name).read_text(encoding="utf-8"))
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            offenders += [a.name for a in node.names if a.name.split(".")[0] not in sys.stdlib_module_names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                module = (node.module or "").split(".")[0]
                names = [module] if module else [a.name for a in node.names]
                offenders += [n for n in names if f"{n}.py" not in _SYNCED]
            elif (node.module or "").split(".")[0] not in sys.stdlib_module_names:
                offenders.append(node.module or "")
    assert not offenders, f"src/probe/service/{name} imports {offenders}"


def test_the_tap_copy_runs_without_probe():
    """The way pi runs it: the plugin root on sys.path, no probe anywhere."""
    script = (
        "import sys; sys.path.insert(0, sys.argv[1]); "
        "from tap.service import client, procid; from tap import owner; "
        "assert 'probe' not in sys.modules, 'the tap copy pulled in probe'; "
        "assert owner._proc is procid.proc, 'tap/owner.py has its own identity function again'; "
        "import os; assert client.owner_of(os.getpid())['pid'] == os.getpid(); "
        "print(client.Ensured.RUNNING)"
    )
    done = subprocess.run(
        [sys.executable, "-I", "-c", script, str(_TAP_ROOT)], capture_output=True, text=True, timeout=30
    )
    assert done.returncode == 0, done.stderr
    assert done.stdout.strip() == "running"


@pytest.mark.parametrize("plugin", ["probe-research", "probe-research-daemon"])
def test_the_hooks_copy_of_the_service_paths_is_the_canonical_one(plugin):
    """The dispatcher and the hook host name the service's folders through
    `hooks/_service_paths.py` (they cannot import `probe`): the same machine
    key, the same sockets (R2 review: it had drifted)."""
    copy = _ROOT / "plugins" / plugin / "hooks" / "_service_paths.py"
    assert copy.is_file()
    assert filecmp.cmp(_CANONICAL / "paths.py", copy, shallow=False), (
        f"plugins/{plugin}/hooks/_service_paths.py drifted from src/probe/service/paths.py: "
        "run `make sync-session-marker` then `make sync-daemon-plugin`"
    )
