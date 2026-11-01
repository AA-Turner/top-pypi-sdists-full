"""Plan A1: every process entry path resolves and runs, and every one the code names is pinned here.

The lists below are kept FOREVER: frozen update hand-offs, older installs, released taps and
plugins exec these names across versions. Never delete an entry; a moved module keeps a
runnable stub at the old path (as `probe.cli.outbox_worker` does).
"""

from __future__ import annotations

import ast
import contextlib
import fcntl
import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from importlib.metadata import distribution
from pathlib import Path

import pytest
from tests.safety_net.entry_paths.code_scan import Scan

#: `python -m <module>` entries. Each value says who execs it.
PINNED_MODULES = {
    "probe.cli": "the daemon's CLI fallback, the service's CLI child, the update hand-off",
    "probe.cli.main": "the CLI module itself; the plugins' guard reads `python -m probe.cli.main` as the CLI",
    "probe.cli.version_refresh": "the CLI's detached version check and update (`--apply`, `--apply-if-newer`)",
    "probe.cli.pi_pins": "pi's session start, detached",
    "probe.cli.import_jobs": "the service's import worker (`-I -u -m`)",
    "probe.cli.outbox_worker": "outbox drainers spawned by releases before the move to probe.sdk",
    "probe.core.run": "the service's action child and the frozen update hand-off (`-I -m ... update`)",
    "probe.service": "the service itself: the client, the tap, an install's start check",
    "probe.service.client": "the hooks, the tap, the CLI, the keeper hand-off (`-I -m ... ensure|check-now`)",
    "probe.service.keeper": "the OS keeper unit (systemd, launchd, Task Scheduler) via lifeboat.sh",
    "probe.service.guard": "the updater's post-switch watchdog",
    "probe.box": "the box watcher, from a training run or the service",
    "probe.sdk.outbox_worker": "the outbox drainer, from the SDK, the CLI and the service",
    "probe.sdk.outputs": "a run's output recovery (`--recover`, `--writer-gone`), from the log helper",
    "probe.daemon.cli_spec": "the daemon host writing its command spec (`-I -m ... --write-to`)",
}
#: Imported by ANOTHER process, often another release (`python -I -c "..."`): kept forever too.
PINNED_IMPORTS = {
    ("probe", ()): "every release imports it (`handoff.EVERY_RELEASE_MODULES`)",
    ("probe.core.run", ()): "a new env's update path, imported before it is exec'd (`handoff.UPDATE_MODULES`)",
    ("probe.core.adopt", ()): "a new env's update path, imported before it is exec'd (`handoff.UPDATE_MODULES`)",
    ("probe.cli.main", ()): "an install's 'does the CLI import' check (`installs.py`)",
    ("probe._entry", ("main",)): "the service's daemon worker (`workers.ENTRY`); the `probe` console script",
    ("probe.daemon.host", ("main",)): "the service's daemon host (`daemonhost.HOST_ENTRY`)",
    ("probe.service", ("client",)): "the old service's successor wait, run with the CLI's interpreter",
    # Same release as the code naming them (its own interpreter and files): pinned so a rename is seen.
    ("probe.cli", ("main",)): "the backfill launchers (same release)",
    ("probe.cli.backfill_record_tool", ("main",)): "the backfill record session's `probe` (same release)",
    ("probe.cli.import_jobs", ("main",)): "an import job's gated child (same release)",
}
#: Module strings the code spells that are not runnable entries, and why. Each must still resolve.
NOT_RUNNABLE = {
    "probe": "`_entry._rerun` builds `python -m probe` when main() is handed argv (tests only); there is no "
             "probe/__main__.py, so that form fails today: a known gap, reported, not pinned as runnable",
    "probe.sdk._readers": "a frame's module name the input recorder skips (`inputs._READERS_MODULE`)",
    "probe.sdk.capture.lineage.c_readers": "the same, since the readers moved (`lineage._READERS_MODULE`, agent:11)",
}
#: Console scripts: old installs' wrappers import these targets by name.
PINNED_SCRIPTS = {
    "probe": "probe._entry:main",
    "probe-research-mcp": "probe._entry:mcp_main",
    "probe-research-mcp-http": "probe._entry:mcp_http_main",
}
DIST = "probe-research"
MCP_INITIALIZE = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "safety-net", "version": "0"}}})


@dataclass
class Run:
    """How one entry is run safely, and what proves it reached its own handling.

    `{tmp}` in argv, env and paths is the test's tmp_path.
    """

    argv: list[str] = field(default_factory=list)
    isolated: bool = True  # `-I`, as its real callers run it
    code: int = 0
    stdin: str = ""
    marker: str = ""  # a regex the output (stdout + stderr) must match
    env: dict = field(default_factory=dict)
    lease: str = ""  # a lock the test holds: the entry finds another owner and stands down
    leaves: str = ""  # a file only its own code makes
    never_leaves: str = ""  # a file it would make had it NOT stood down


_OUTBOX = dict(argv=["{tmp}/outbox-q"], isolated=False, lease="outbox-q/.worker.lock",
               leaves="outbox-q/ops", never_leaves="outbox-q/status.json")
RUNS = {
    "probe.cli": Run(["--version"], marker=r"^probe \d+\.\d+"),
    "probe.cli.main": Run(["--version"], isolated=False, marker=r"^probe \d+\.\d+"),
    # The refresh, against no server: it records the failed fetch in its cache.
    "probe.cli.version_refresh": Run(["--no-daemon"], isolated=False, leaves="version-cache.json",
                                     env={"PROBE_VERSION_CACHE": "{tmp}/version-cache.json"}),
    # Nothing of pi's in this HOME: no pin, said as JSON.
    "probe.cli.pi_pins": Run([], isolated=False, marker=r'"pin": null'),
    "probe.cli.import_jobs": Run(["--help"], marker=r"job_id"),
    # Another worker holds the outbox lease: promote-only, never a drain pass, exit 0.
    "probe.cli.outbox_worker": Run(**_OUTBOX),
    "probe.sdk.outbox_worker": Run(**_OUTBOX),
    "probe.core.run": Run(["version"], stdin="{}", marker=r'"cli_version"'),
    # `--selftest` is service/'s check; here its own argument handling refuses an unknown flag.
    "probe.service": Run(["--safety-net"], code=2, marker=r"usage: python -m probe\.service"),
    "probe.service.client": Run(["socket"], marker=r'"socket"'),
    # No session recorded in this HOME: nothing to keep, exit 0 and say nothing (its no-op).
    "probe.service.keeper": Run([]),
    "probe.service.guard": Run(["--help"], marker=r"--old-python"),
    # Another watcher holds the box lease: exit 0 at once (else it would watch forever).
    "probe.box": Run([], isolated=False, env={"PROBE_BOX_DIR": "{tmp}/box/runs"}, lease="box/watcher.lock"),
    # A record that is not there: the reporter claims `<entry>.gone` first.
    "probe.sdk.outputs": Run(["--writer-gone", "{tmp}/entry.json"], isolated=False, leaves="entry.json.gone"),
    "probe.daemon.cli_spec": Run([], marker=r'"root"'),
}


@pytest.fixture(scope="module")
def scan() -> Scan:
    return Scan()


def _run(argv: list[str], env: dict, *, stdin: str = "", timeout: float = 120) -> subprocess.CompletedProcess:
    try:
        return subprocess.run([sys.executable, *argv], env=env, cwd=env["HOME"], input=stdin, capture_output=True,
                              text=True, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        pytest.fail(f"`python {' '.join(argv)}` did not exit in {timeout:.0f} s:\n{exc.stderr}", pytrace=False)


@contextlib.contextmanager
def _held(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def test_every_pinned_entry_has_a_way_to_run():
    assert set(RUNS) == set(PINNED_MODULES)


@pytest.mark.parametrize("module", sorted(PINNED_MODULES))
def test_pinned_module_resolves(module):
    spec = importlib.util.find_spec(module)
    assert spec is not None, f"`python -m {module}` no longer resolves; keep a runnable stub at the old path"
    if spec.submodule_search_locations is not None:
        assert importlib.util.find_spec(f"{module}.__main__") is not None, f"package {module} lost its __main__"
        return
    # Statically too: an entry whose run is silent (the keeper, the box) would not show a lost main block.
    tree = ast.parse(Path(spec.origin).read_text(encoding="utf-8"))
    assert any(isinstance(node, ast.If) and "__main__" in ast.unparse(node.test) for node in tree.body), \
        f"{module} has no `if __name__ == \"__main__\":` block: `python -m {module}` would run nothing"


@pytest.mark.parametrize("module", sorted(PINNED_MODULES))
def test_pinned_module_runs(module, child_env, tmp_path):
    run = RUNS[module]
    env = {**child_env, **{k: v.replace("{tmp}", str(tmp_path)) for k, v in run.env.items()}}
    argv = ["-I"] * run.isolated + ["-m", module] + [a.replace("{tmp}", str(tmp_path)) for a in run.argv]
    with _held(tmp_path / run.lease) if run.lease else contextlib.nullcontext():
        done = _run(argv, env, stdin=run.stdin)
    said = done.stdout + done.stderr
    assert done.returncode == run.code, f"`python {' '.join(argv)}` exited {done.returncode}:\n{said[-3000:]}"
    assert "Traceback" not in done.stderr, done.stderr[-3000:]
    if run.marker:
        assert re.search(run.marker, said, re.MULTILINE), f"`python {' '.join(argv)}` said:\n{said[-3000:]}"
    if run.leaves:
        assert (tmp_path / run.leaves).exists(), f"{module} never reached its own code ({run.leaves})"
    if run.never_leaves:
        assert not (tmp_path / run.never_leaves).exists(), f"{module} ignored the held lease ({run.never_leaves})"


@pytest.mark.parametrize("pinned", sorted(PINNED_IMPORTS), ids=lambda p: ":".join((p[0], *p[1])))
def test_pinned_import_imports_under_isolation(pinned, child_env):
    module, names = pinned
    program = f"from {module} import {', '.join(names)}" if names else f"import {module}"
    done = _run(["-I", "-c", program], child_env)
    assert done.returncode == 0, f"`python -I -c {program!r}` failed:\n{done.stderr[-3000:]}"


@pytest.mark.parametrize("module", sorted(NOT_RUNNABLE))
def test_named_non_entries_still_resolve(module):
    assert importlib.util.find_spec(module) is not None, f"the code names {module}, which is gone"


def test_console_scripts_are_pinned():
    scripts = {ep.name: ep.value for ep in distribution(DIST).entry_points if ep.group == "console_scripts"}
    assert scripts == PINNED_SCRIPTS
    for ep in distribution(DIST).entry_points:
        if ep.group == "console_scripts":
            assert callable(ep.load()), ep


def _script(name: str, *args: str) -> list[str]:
    """`python -I -c` running console script `name` exactly as its installed wrapper would."""
    program = ("import sys; from importlib.metadata import distribution; "
               f"ep = next(e for e in distribution({DIST!r}).entry_points "
               f"if e.group == 'console_scripts' and e.name == {name!r}); "
               f"sys.argv = [{name!r}, *sys.argv[1:]]; sys.exit(ep.load()())")
    return ["-I", "-c", program, *args]


def test_probe_script_runs(child_env):
    done = _run(_script("probe", "--version"), child_env)
    assert done.returncode == 0 and re.match(r"probe \d+\.\d+", done.stdout), done.stdout + done.stderr


def test_mcp_stdio_script_answers_initialize(child_env):
    done = _run(_script("probe-research-mcp"), child_env, stdin=MCP_INITIALIZE + "\n")
    assert done.returncode == 0, done.stderr[-3000:]
    answer = json.loads(done.stdout.splitlines()[0])
    assert answer["id"] == 1 and answer["result"]["serverInfo"]["name"], answer


def test_mcp_http_script_reaches_its_own_settings(child_env):
    """No safe no-op (it serves forever): a PORT it cannot parse stops it before it binds."""
    done = _run(_script("probe-research-mcp-http"), {**child_env, "PORT": "safety-net-port"})
    assert done.returncode == 1 and "'safety-net-port'" in done.stderr, done.stderr[-3000:]


def test_every_dash_m_module_the_code_runs_is_pinned(scan):
    unpinned = {m: sorted(w) for m, w in scan.dash_m.items() if m not in PINNED_MODULES and m not in NOT_RUNNABLE}
    assert not unpinned, f"`-m` entries not in PINNED_MODULES (pin each, forever): {unpinned}"


def test_every_module_constant_is_pinned(scan):
    known = set(PINNED_MODULES) | {m for m, _ in PINNED_IMPORTS} | set(NOT_RUNNABLE)
    unpinned = {m: sorted(w) for m, w in scan.constants.items() if m not in known}
    assert not unpinned, f"*_MODULE(S) values not pinned here: {unpinned}"


def test_every_import_program_the_code_runs_is_pinned(scan):
    unpinned = {f"{m}:{','.join(n)}": sorted(w) for (m, n), w in scan.imports.items() if (m, n) not in PINNED_IMPORTS}
    assert not unpinned, f"`-c` imports not in PINNED_IMPORTS: {unpinned}"


def test_the_scan_sees_the_known_entries(scan):
    """Guards the scan itself: it must find the hand-off's and the service's own entry strings."""
    assert {"probe.core.run", "probe.service", "probe.service.client", "probe.service.keeper"} <= set(scan.dash_m)
    assert {"probe.core.run", "probe.core.adopt", "probe"} <= set(scan.constants)
    assert ("probe.daemon.host", ("main",)) in scan.imports
