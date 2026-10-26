"""Released CLIs and the current Probe service, both ways (plan D22).

    previous       the newest probe-research on PyPI that is not newer than
                   this checkout: what researchers run now
    oldest         `client-version.json` `cli.min`: the oldest CLI still supported
    first_service  the oldest supported one that has the service: `cli.min`, or
                   FIRST_SERVICE_RELEASE when `cli.min` predates it (skipped
                   when that is `oldest` itself)

Each is installed from PyPI into a throwaway venv, then:

  * every API v1 name its protocol knows is still in the current protocol and
    in the contract snapshot (`fixtures/service_api_v1_contract.json`, which
    must name everything a released piece may send or read)
  * its own client code speaks to the CURRENT service: `service.hello`,
    `status.get`, `session.register`, `session.list`, `session.record` (when it
    knows it), `session.end`; and its `probe status --json` reads that service
  * the current client and CLI speak to ITS service, started from its venv as
    `ensure()` starts any service (`runtime.json` names its interpreter): the
    same calls, every method it predates answers "unknown method" on a
    connection that stays usable, and `probe status --json` reads it
  * the current tap's own client (`python -m tap record`, `tap finish`) has
    ITS service record a session, when it records sessions at all: a tap
    updates when it merges, and talks to the service a researcher already runs

A release that predates the service (no `probe.service`) can do none of that:
it has to install, run, and leave a running current service as it found it.

CI only: marked `release_smoke` and skipped unless PROBE_RELEASE_SMOKE=1 (the
agent-ci `release-smoke` job), because it downloads from PyPI. The one check
that needs no download (the names called here are contract names) runs everywhere.

    PROBE_RELEASE_SMOKE=1 pytest -m release_smoke tests/test_service_release_smoke.py

PROBE_RELEASE_SMOKE_VERSIONS="previous=0.288.0,oldest=0.226.2,first_service=0.274.0"
tests other ones.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path

import pytest

from probe import __version__ as CURRENT_VERSION
from probe.cli import service_calls
from probe.service import client, protocol
from probe.service.protocol import Client, ErrorCode, Method
from tests.service_harness import kill_agent, service_home, spawn_agent, wait_for  # noqa: F401
from tests.test_service_api_contract import CURRENT, SNAPSHOT
from tests.test_service_recorders import _tap

pytestmark = pytest.mark.skipif(os.name != "posix", reason="the service is POSIX-only until R3")


def _from_pypi(test):
    """A test that installs released CLIs: agent-ci's release-smoke job only."""
    test = pytest.mark.release_smoke(test)
    return pytest.mark.skipif(
        os.environ.get("PROBE_RELEASE_SMOKE") != "1",
        reason="downloads released CLIs from PyPI: agent-ci's release-smoke job (PROBE_RELEASE_SMOKE=1)",
    )(test)


AGENT = Path(__file__).resolve().parents[1]
TAP_ROOT = AGENT / "plugins" / "probe-research-tap"
DIST = "probe-research"
#: The first release with `probe.service` (#3133, 2026-10-19).
FIRST_SERVICE_RELEASE = "0.274.0"
PYPI = f"https://pypi.org/pypi/{DIST}/json"
#: The calls each side makes, by their API v1 names (from the snapshot, below).
CALLS = ("service.hello", "service.status", "status.get", "session.register", "session.list", "session.record",
         "session.finish", "session.end")
#: What the old side prints: every API v1 name its protocol has (the contract
#: test's own groups), and whether it has a service client at all.
_NAMES = r'''
import json, sys
try:
    from probe.service import protocol as p
except ModuleNotFoundError as exc:
    if exc.name not in ("probe.service", "probe.service.protocol"):
        raise  # a release whose service is there and does not import: a failure, never "predates"
    print(json.dumps(None)); sys.exit(0)

def consts(name):
    cls = getattr(p, name, None)
    return sorted({v for k, v in vars(cls).items() if k.isupper() and isinstance(v, (str, int))}) if cls else []

def group(name):
    return sorted(getattr(p, name, ()) or ())

print(json.dumps({
    "methods": group("METHODS"), "topics": group("TOPICS"), "clients": group("CLIENTS"), "modes": group("MODES"),
    "actions": group("ACTIONS"), "check_triggers": group("CHECK_TRIGGERS"), "report_triggers": group("REPORT_TRIGGERS"),
    "error_codes": consts("ErrorCode"), "refused_reasons": consts("RefusedReason"), "defer_reasons": consts("DeferReason"),
    "check_outcomes": consts("CheckOutcome"), "states": consts("State"), "stop_reasons": consts("StopReason"),
    "end_reasons": consts("EndReason"), "context_env": group("CONTEXT_ENV"), "api": getattr(p, "API_VERSION", None),
}))
'''
#: The old side's client, against whichever service runs: one connection, each
#: call's answer or error. Its own `probe.service.client`, as its tap and CLI use it.
_SPEAK = r'''
import json, sys
from probe import __version__
from probe.service import client, protocol
plan = json.loads(sys.argv[1])
out = {}

def call(conn, key, method, params):
    try:
        out[key] = {"result": conn.call(method, params)}
    except client.ServiceError as exc:
        out[key] = {"error": exc.code, "data": exc.data}

with client.Connection.open(30.0) as conn:
    out["hello"] = {"result": conn.hello("cli", __version__)}
    for key, method, params in plan:
        if method in protocol.METHODS:  # an old piece sends only what it knows
            call(conn, key, method, params)
print(json.dumps(out))
'''


def _numbers(version: str) -> tuple:
    try:
        return tuple(int(part) for part in version.split("."))
    except ValueError:
        return ()


def _previous() -> str:
    """The newest release on PyPI not newer than this checkout (pre-releases
    and yanked files left out)."""
    with urllib.request.urlopen(PYPI, timeout=60) as response:  # noqa: S310 -- a fixed https URL
        releases = json.load(response)["releases"]
    ours = _numbers(CURRENT_VERSION)
    found = [
        v for v, files in releases.items()
        if _numbers(v) and _numbers(v) <= ours and any(not f.get("yanked") for f in files)
    ]
    assert found, f"no release of {DIST} on PyPI at or below {CURRENT_VERSION}"
    return max(found, key=_numbers)


def _oldest() -> str:
    return json.loads((AGENT / "client-version.json").read_text())["cli"]["min"]


def _version_for(which: str) -> str:
    chosen = dict(
        part.split("=", 1) for part in os.environ.get("PROBE_RELEASE_SMOKE_VERSIONS", "").split(",") if "=" in part
    )
    if which in chosen:
        return chosen[which]
    if which == "previous":
        return _previous()
    oldest = chosen.get("oldest") or _oldest()
    if which == "oldest":
        return oldest
    return max(oldest, FIRST_SERVICE_RELEASE, key=_numbers)


@dataclass
class Release:
    which: str
    version: str
    python: Path
    probe: Path
    names: dict | None  # its protocol's names; None: it predates the service

    def run(self, code: str, *args: str, env: dict | None = None, timeout: float = 120) -> object:
        """Run `code` on its interpreter, isolated (`-I`): only its own `probe` imports."""
        done = subprocess.run([str(self.python), "-I", "-c", code, *args], capture_output=True, text=True,
                              env=env, timeout=timeout, check=False)
        assert done.returncode == 0, f"{self.which} {self.version}: exit {done.returncode}\n{done.stderr[-3000:]}"
        return json.loads(done.stdout.strip().splitlines()[-1])


def _install(version: str, folder: Path) -> tuple[Path, Path]:
    venv = folder / "venv"
    uv = shutil.which("uv")
    if uv:
        subprocess.run([uv, "venv", "-q", "--python", sys.executable, str(venv)], check=True, timeout=300)
        install = [uv, "pip", "install", "-q", "--python", str(venv / "bin" / "python")]
    else:
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True, timeout=300)
        install = [str(venv / "bin" / "python"), "-m", "pip", "install", "-q", "--disable-pip-version-check"]
    subprocess.run([*install, f"{DIST}=={version}"], check=True, timeout=600)
    return venv / "bin" / "python", venv / "bin" / "probe"


@pytest.fixture(scope="module", params=["previous", "oldest", "first_service"])
def release(request, tmp_path_factory) -> Release:
    version = _version_for(request.param)
    if request.param == "first_service" and version == _version_for("oldest"):
        pytest.skip(f"the oldest supported release ({version}) has the service: `oldest` covers it")
    python, probe = _install(version, tmp_path_factory.mktemp(f"release-{version}"))
    names = Release(request.param, version, python, probe, None).run(_NAMES)
    if request.param != "oldest":
        assert names is not None, f"{request.param} {version} has no Probe service"
    return Release(request.param, version, python, probe, names)


@pytest.fixture
def agent():
    proc, owner = spawn_agent()
    yield owner
    kill_agent(proc)


def _env(home: Path) -> dict:
    return {**os.environ, "HOME": str(home), "PROBE_TELEMETRY": "off"}


def _plan(owner: dict, home: Path, tap_root: Path, tap_version: str) -> tuple[str, list]:
    """The calls in order, `(key, method, params)`: a session registered, listed,
    recorded (a stand-in tap: the API, not the recorder, is under test here),
    finished and ended."""
    sid, recorded = f"rs-{uuid.uuid4().hex[:12]}", f"rr-{uuid.uuid4().hex[:12]}"
    work = home / "work"
    work.mkdir(exist_ok=True)
    plan = [
        ("status", Method.STATUS, {}),
        ("status_get", Method.STATUS_GET, {}),
        ("register", Method.SESSION_REGISTER,
         {"sid": sid, "harness": "claude_code", "mode": "inline", "owner": owner, "generation": 1}),
        ("list", Method.SESSION_LIST, {}),
        ("record", Method.SESSION_RECORD, {
            "sid": recorded, "harness": "claude_code", "mode": "inline", "owner": owner, "generation": 1,
            "cwd": str(work), "transcript": str(work / f"{recorded}.jsonl"), "transcript_dir": None,
            "tap_root": str(tap_root), "tap_version": tap_version, "env": {"HOME": str(home)},
        }),
        ("finish", Method.SESSION_FINISH, {"sid": recorded, "wait": 10}),
        ("end", Method.SESSION_END, {"sid": sid, "generation": 1}),
    ]
    return sid, plan


def _speak_current(plan: list) -> dict:
    """The current client's half of `_SPEAK`."""
    out = {}
    with client.Connection.open(30.0) as conn:
        out["hello"] = {"result": conn.hello(Client.CLI, CURRENT_VERSION)}
        for key, method, params in plan:
            try:
                out[key] = {"result": conn.call(method, params)}
            except client.ServiceError as exc:
                out[key] = {"error": exc.code, "data": exc.data}
    return out


def _check_answers(out: dict, *, service_version: str, sid: str, knows_record: bool) -> None:
    hello = out["hello"]["result"]
    assert hello["api"] == protocol.API_VERSION == SNAPSHOT["api"]
    assert hello["service_version"] == service_version
    assert out["status"]["result"]["service_version"] == service_version
    # A status snapshot, or the service saying it could not take one: either way, understood.
    status_get = out["status_get"]
    assert "result" in status_get or (
        status_get["error"] == ErrorCode.REFUSED and (status_get["data"] or {}).get("reason") == "status_unavailable"
    ), status_get
    assert out["register"]["result"]["alive"] is True
    listed = {s["sid"]: s for s in out["list"]["result"]["sessions"]}
    assert listed[sid]["harness"] == "claude_code" and listed[sid]["mode"] == "inline"
    if knows_record:
        assert out["record"]["result"]["recording"] is True and out["record"]["result"]["started"] is True
        assert out["finish"]["result"] == {"recording": True, "finished": True}
    assert "error" not in out["end"], out["end"]


def _interpreter_of(pid: int) -> str:
    """The command a service runs as (`<python> -I -m probe.service`): which venv's
    code it is, when the version strings alone cannot tell (previous == this checkout)."""
    return subprocess.run(["ps", "-ww", "-o", "command=", "-p", str(pid)], capture_output=True, text=True,
                          timeout=30, check=False).stdout.strip()


def _probe_status(probe: Path, env: dict) -> dict | None:
    """`probe status --json`, or None from a CLI that has no `probe status` yet."""
    done = subprocess.run([str(probe), "status", "--json"], capture_output=True, text=True, env=env, timeout=120,
                          check=False)
    if done.returncode == 2 and "No such command" in done.stderr:
        return None
    assert done.returncode == 0, done.stderr[-3000:]
    return json.loads(done.stdout)


# -- the tests ------------------------------------------------------------------------------


def test_the_calls_made_here_are_api_v1_contract_names():
    assert set(CALLS) <= set(SNAPSHOT["methods"])
    assert set(CALLS) <= set(protocol.METHODS)


@_from_pypi
def test_the_release_installs_and_runs(release):
    done = subprocess.run([str(release.probe), "--version"], capture_output=True, text=True, timeout=120, check=False,
                          env=_env(Path(os.environ["HOME"])))
    assert done.returncode == 0, done.stderr
    assert release.version in done.stdout


@_from_pypi
def test_every_name_the_release_knows_is_still_served_and_in_the_contract(release):
    if release.names is None:
        pytest.skip(f"{release.which} {release.version} predates the Probe service")
    assert release.names["api"] == protocol.API_VERSION
    for group, names in release.names.items():
        if group == "api":
            continue
        gone = set(names) - CURRENT[group]
        assert not gone, f"{release.version}'s {group} {sorted(gone)} are gone from the current protocol"
        unlisted = set(names) - set(SNAPSHOT[group])
        assert not unlisted, (f"{release.version} shipped {group} {sorted(unlisted)}: add them to "
                              "tests/fixtures/service_api_v1_contract.json")


@_from_pypi
def test_its_client_speaks_to_the_current_service(release, service_home, agent, tmp_path):
    if release.names is None:
        # It cannot: it must only leave the current service as it found it.
        status = service_home.start()
        done = subprocess.run([str(release.probe), "--help"], capture_output=True, text=True, timeout=120,
                              env=_env(service_home.home), check=False)
        assert done.returncode == 0, done.stderr
        assert service_home.status()["pid"] == status["pid"]
        return
    status = service_home.start()
    assert status["service_version"] == CURRENT_VERSION
    assert _interpreter_of(status["pid"]).startswith(f"{sys.executable} -I -m probe.service")
    sid, plan = _plan(agent, service_home.home, _tap(tmp_path / "tap", "0.10.0"), "0.10.0")
    out = release.run(_SPEAK, json.dumps(plan), env=_env(service_home.home))
    _check_answers(out, service_version=CURRENT_VERSION, sid=sid,
                   knows_record=Method.SESSION_RECORD in release.names["methods"])
    # Its own CLI reads the current service (a release whose `probe status` names it).
    view = (_probe_status(release.probe, _env(service_home.home)) or {}).get("service")
    if view is not None:
        assert view["reach"] == "answered" and view["version"] == CURRENT_VERSION, view
    assert service_home.status()["pid"] == status["pid"], "the current service is still the one that answered"


@_from_pypi
def test_the_current_client_and_cli_speak_to_its_service(release, service_home, agent, tmp_path):
    if release.names is None:
        pytest.skip(f"{release.which} {release.version} predates the Probe service: it never runs one")
    # Its service, started the way every client starts one: `runtime.json` names its interpreter.
    client.write_runtime(str(release.python), release.version)
    status = service_home.start(timeout=30)
    assert status["service_version"] == release.version, status
    assert _interpreter_of(status["pid"]).startswith(f"{release.python} -I -m probe.service"), "its venv's service"
    sid, plan = _plan(agent, service_home.home, _tap(tmp_path / "tap", "0.10.0"), "0.10.0")
    knows_record = Method.SESSION_RECORD in release.names["methods"]
    out = _speak_current(plan)
    if not knows_record:
        assert out["record"]["error"] == ErrorCode.UNKNOWN_METHOD
        assert out["finish"]["error"] == ErrorCode.UNKNOWN_METHOD
    _check_answers(out, service_version=release.version, sid=sid, knows_record=knows_record)

    # What it predates is "unknown method", and the connection goes on.
    newer = sorted(set(protocol.METHODS) - set(release.names["methods"]))
    with client.Connection.open(10.0) as conn:
        conn.hello(Client.CLI, CURRENT_VERSION)
        for method in newer:
            with pytest.raises(client.ServiceError) as refused:
                conn.call(method, {})
            assert refused.value.code == ErrorCode.UNKNOWN_METHOD, (method, refused.value)
        assert conn.call(Method.STATUS)["service_version"] == release.version

    # The current CLI's own reads: `probe status` / `probe doctor`'s view, and `probe status --json`.
    view = service_calls.view(timeout=10)
    assert view["reach"] == "answered" and view["version"] == release.version, view
    assert sid not in {s["sid"] for s in view["sessions"]}, "ended above"
    current_probe = Path(sys.executable).with_name("probe")
    cli_view = _probe_status(current_probe, _env(service_home.home))["service"]
    assert cli_view["reach"] == "answered" and cli_view["version"] == release.version, cli_view
    assert service_home.status()["pid"] == status["pid"]


@_from_pypi
def test_the_current_tap_has_its_service_record_a_session(release, service_home, agent):
    """The tap ships when it merges and meets the service a researcher already
    runs: its own client (`tap record` at SessionStart, `tap finish` at
    SessionEnd) against a service started from the release's venv, recording
    with this checkout's tap."""
    if release.names is None or Method.SESSION_RECORD not in release.names["methods"]:
        pytest.skip(f"{release.which} {release.version} does not record sessions: `tap watch` does")
    client.write_runtime(str(release.python), release.version)
    status = service_home.start(timeout=30)
    assert status["service_version"] == release.version
    sid = f"rt-{uuid.uuid4().hex[:12]}"
    work = service_home.home / "tap-work"
    work.mkdir()
    transcript = work / f"{sid}.jsonl"
    transcript.write_text("")
    env = {**_env(service_home.home), "PYTHONPATH": str(TAP_ROOT), "PROBE_TAP_HOSTED": "1",
           # No ingest token and a dead endpoint: the recorder it starts reaches nothing.
           "PROBE_BASE_URL": "http://127.0.0.1:9",
           # The agent process, as pi names its own (no `tap owner` record here).
           "PROBE_SERVICE_OWNER_PID": str(agent["pid"])}
    marker = Path(f"/tmp/probe-research-tap-watcher-{sid}.hosted")

    def tap(*args: str, timeout: float = 30) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "-m", "tap", *args], env=env, cwd=str(work), capture_output=True,
                              text=True, timeout=timeout, check=False)

    try:
        done = tap("record", "--session-id", sid, "--cwd", str(work), "--transcript", str(transcript),
                   "--plugin-root", str(TAP_ROOT))
        assert done.returncode == 0, f"its service did not record the session ({done.stderr[-2000:]})"
        assert marker.read_text().strip() == str(status["pid"]), "the marker names its service"
        assert tap("recording", "--session-id", sid).returncode == 0
        assert sid in {s["sid"] for s in service_home.call(Method.SESSION_LIST)["sessions"]}
        done = tap("finish", "--session-id", sid, "--wait", "20", timeout=40)
        assert done.returncode == 0, f"tap finish: exit {done.returncode} (1: not recorded, 2: not finished)"
        assert wait_for(lambda: tap("recording", "--session-id", sid).returncode == 1, 10)
    finally:
        marker.unlink(missing_ok=True)
