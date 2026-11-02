"""The tap's copy of the service client must be the canonical one, byte for byte.

`plugins/probe-research-tap/tap/service/{service_api,calls,start,cli,wire,...}.py`
are COPIES of `src/probe/foundation/service_api/`: the tap runs under the system python with only
the plugin root on sys.path, and pi reaches the client through the tap (`python
-m tap service ...`), so neither can import `probe`. One client, one identity
function (procid: the tap's owner record and the service's check read the same
{pid, start}). `make sync-service-client` reconciles them; this fails when
someone edits one side only (plan A1/R7).
"""

from __future__ import annotations

import ast
import filecmp
import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_CANONICAL = _ROOT / "src" / "probe" / "foundation" / "service_api"
_TAP_ROOT = _ROOT / "plugins" / "probe-research-tap"
_COPY = _TAP_ROOT / "tap" / "service"

_SYNCED = (
    "service_api.py", "calls.py", "start.py", "cli.py", "wire.py", "vocabularies.py", "env.py", "params.py",
    "paths.py", "procid.py", "winpipe.py",
)
#: The tap's own files in tap/service/: its package docstring, and the two module names every tap
#: release before the split imported (`tap.service.client`, `tap.service.protocol`), kept as facades.
_TAP_OWNED = ("__init__.py", "client.py", "protocol.py")

def _vendored_pairs() -> set[tuple[str, str]]:
    """What `make sync-service-client` copies: plugins/VENDORED.json's [source, copy] pairs."""
    manifest = json.loads((_ROOT / "plugins" / "VENDORED.json").read_text(encoding="utf-8"))
    return {tuple(pair) for step in manifest["groups"]["sync-service-client"] for pair in step["files"]}


def test_the_vendor_manifest_syncs_exactly_these_files():
    assert _vendored_pairs() == {
        ((_CANONICAL / name).relative_to(_ROOT).as_posix(), (_COPY / name).relative_to(_ROOT).as_posix())
        for name in _SYNCED
    }


@pytest.mark.parametrize("name", _SYNCED)
def test_tap_copy_is_byte_identical(name):
    canonical, copy = _CANONICAL / name, _COPY / name
    assert copy.is_file(), f"tap copy of {name} is missing; run `make sync-service-client`"
    assert filecmp.cmp(canonical, copy, shallow=False), (
        f"plugins/probe-research-tap/tap/service/{name} drifted from src/probe/foundation/service_api/{name}: "
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
    assert not offenders, f"src/probe/foundation/service_api/{name} imports {offenders}"


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
        f"plugins/{plugin}/hooks/_service_paths.py drifted from src/probe/foundation/service_api/paths.py: "
        "run `make sync-session-marker` then `make sync-daemon-plugin`"
    )


def test_the_tap_service_folder_holds_the_copies_and_its_own_facades_only():
    """A copy no manifest names would drift unseen; a stale copy of a split file (the old client.py
    or protocol.py bytes) would shadow nothing but mislead the next reader."""
    held = {path.name for path in _COPY.glob("*.py")}
    assert held == set(_SYNCED) | set(_TAP_OWNED)


@pytest.mark.parametrize("old", ["client", "protocol"])
def test_the_tap_facades_serve_every_name_the_old_module_had(old):
    """`tap.service.client` / `.protocol` from a tap before the split (agent:16) and from this one name
    the same things: a tap process holding the old modules can import the new files under them."""
    import importlib

    probe_side = importlib.import_module(f"probe.service.{old}")
    script = (
        "import json, sys; sys.path.insert(0, sys.argv[1]); import importlib; "
        f"m = importlib.import_module('tap.service.{old}'); "
        "assert 'probe' not in sys.modules; print(json.dumps(sorted(n for n in dir(m) if not n.startswith('__'))))"
    )
    done = subprocess.run(
        [sys.executable, "-I", "-c", script, str(_TAP_ROOT)], capture_output=True, text=True, timeout=30
    )
    assert done.returncode == 0, done.stderr
    served = set(json.loads(done.stdout))
    served_there = vars(probe_side)["_homes"]  # every name the old module bound (a live door, foundation/front_door)
    wanted = {
        name for name in served_there
        if not isinstance(getattr(probe_side, name), type(sys)) and name not in sys.stdlib_module_names
        and name not in {"Any", "Callable", "Path", "dataclass", "annotations"}
    } | ({"paths", "procid"} if old == "client" else set())
    assert wanted <= served, sorted(wanted - served)
