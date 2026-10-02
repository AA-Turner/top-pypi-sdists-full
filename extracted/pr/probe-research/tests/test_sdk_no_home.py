"""A process with NO home directory must still record its run.

An arbitrary-uid container (OpenShift, `docker run --user 12345`, many
managed-job runners) can start with HOME unset and no passwd entry. There
`Path.home()` raises `RuntimeError: Could not determine home directory`, and
`probe.init()` died of it in `config.config_path()` before opening a run --
found by the environment suite (managed/home[unset], 0.196.1). The outbox had
been taught this in plan 1.5; the config, state and identity paths had not.

`probe.sdk.homedir` is now the one door to `~`: the real home, else a private
`$TMPDIR/probe-home-<uid>`.
"""

from __future__ import annotations

import ast
import json
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from probe.sdk import homedir
from tests.served_fake_app import serve

SDK = Path(__file__).resolve().parent.parent / "src" / "probe" / "sdk"

# The child's own start-up: no passwd entry for this uid, exactly what a
# container running an arbitrary uid has (posixpath.expanduser asks pwd when
# HOME is unset).
_NO_PASSWD_ENTRY = """
import pwd

def _no_entry(uid):
    raise KeyError(f"getpwuid(): uid not found: {uid}")

pwd.getpwuid = _no_entry
"""

_CHILD = """
import os, probe
run = probe.init(project="nohome", name="r")
for step in range(20):
    probe.log({"loss": 1.0 / (step + 1), "opt": {"lr": step * 0.001}}, step=step)
probe.update_config({"lr": 0.1})
probe.finish()
print("RUN", run.id)
"""


@pytest.fixture
def no_home(tmp_path):
    """This process has no home: HOME unset, no passwd entry, a private TMPDIR.

    Its own MonkeyPatch, undone at ITS teardown: the suite's config-isolation
    fixture checks `Path.home()` on the way out and must find a home again."""
    import pwd

    def _no_entry(uid):
        raise KeyError(uid)

    tmp = tmp_path / "tmp"
    tmp.mkdir()
    with pytest.MonkeyPatch.context() as mp:
        for var in ("HOME", "XDG_CONFIG_HOME", "XDG_STATE_HOME", "XDG_CACHE_HOME", "PROBE_CONFIG_PATH"):
            mp.delenv(var, raising=False)
        mp.setattr(pwd, "getpwuid", _no_entry)
        mp.setattr(tempfile, "tempdir", str(tmp))
        mp.setattr(homedir, "_stand_in", None)
        yield tmp


def test_no_home_is_a_private_stand_in_under_tmpdir(no_home):
    with pytest.raises(RuntimeError):
        Path.home()  # the premise: exactly what the container sees
    assert homedir.real_home() is None
    home = homedir.home()
    assert home == no_home / f"probe-home-{os.getuid()}"
    assert stat.S_IMODE(os.stat(home).st_mode) == 0o700
    assert homedir.home() == home  # chosen once


def test_a_stand_in_someone_else_could_write_is_not_used(no_home):
    shared = no_home / f"probe-home-{os.getuid()}"
    shared.mkdir(mode=0o777)
    os.chmod(shared, 0o777)
    home = homedir.home()
    assert home != shared and home.parent == no_home
    assert stat.S_IMODE(os.stat(home).st_mode) == 0o700


def test_a_real_home_is_used_as_is(monkeypatch, tmp_path):
    monkeypatch.setenv("HOME", str(tmp_path))
    assert homedir.home() == tmp_path


def test_config_and_state_paths_resolve_without_a_home(no_home):
    from probe.sdk import config, device_identity, inputs, journal, session_marker, spool

    stand_in = homedir.home()
    for path in (
        config.config_path(),
        journal._accounts_path(),
        spool.default_dir(),
        inputs.state_dir(),
        session_marker.state_dir(),
        device_identity.device_file(),
    ):
        assert stand_in in Path(path).parents, path


def test_init_log_finish_with_no_home_directory(app, tmp_path):
    """The customer loop in a child with no HOME and no passwd entry: it
    records every point and closes `completed`, and nothing lands in a
    directory literally named `~` in the working folder."""
    site = tmp_path / "site"
    site.mkdir()
    (site / "sitecustomize.py").write_text(_NO_PASSWD_ENTRY)
    work = tmp_path / "work"
    work.mkdir()
    tmp = tmp_path / "tmp"
    tmp.mkdir()
    with serve(app) as url:
        from probe.sdk.client import Client

        setup = Client(base_url=url, token="ros_pat_deadbeef", async_writes=False, auto_drain=False,
                       spool_dir=tmp_path / "setup-spool")
        try:
            setup.create_project("nohome", "nohome", kind="general")
        finally:
            setup.close()
        # A customer's environment, not the suite's: no PROBE_* a sibling test
        # left in os.environ (PROBE_RUN_ID would make init() attach instead).
        env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "TZ") if k in os.environ}
        env.update({
            "PYTHONPATH": os.pathsep.join([str(site), *filter(None, [os.environ.get("PYTHONPATH")])]),
            "TMPDIR": str(tmp),
            "PROBE_BASE_URL": url,
            "PROBE_TOKEN": "ros_pat_deadbeef",
            "PROBE_TELEMETRY": "off",
            "PROBE_AUTO_SNAPSHOT": "0",
        })
        proc = subprocess.run(
            [sys.executable, "-c", _CHILD], env=env, cwd=work, capture_output=True, text=True, timeout=180
        )
        assert proc.returncode == 0, proc.stderr[-3000:]
        (run_id,) = [line.split()[1] for line in proc.stdout.splitlines() if line.startswith("RUN ")]
        points = {
            (p["key"], p["step_index"])
            for p in app.metric_points_posted.get(run_id, [])
            if p["kind"] != "hardware"  # on, as for a customer; the close sends its window
        }
        assert points == {(k, s) for s in range(20) for k in ("loss", "opt/lr")}
        assert app.runs[run_id]["status"] == "completed"
        assert app.runs[run_id]["config"]["lr"] == 0.1
    assert not (work / "~").exists(), "state written into a directory named ~ in the project"
    assert (tmp / f"probe-home-{os.getuid()}").is_dir()


def test_every_sdk_home_lookup_goes_through_homedir():
    """`Path.home()` raises with no home. Outside `homedir` itself it may only
    appear where the failure is caught right there (`journal.default_root`) or
    in `session_marker`'s vendored-copy branch, which has no `probe` to ask."""
    allowed = {("homedir.py", "real_home"), ("journal.py", "default_root"), ("session_marker.py", "_home")}
    found = []
    for path in sorted(SDK.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for node in ast.walk(fn):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "home"
                    and isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "Path"
                    and (path.name, fn.name) not in allowed
                ):
                    found.append(f"{path.name}:{node.lineno} in {fn.name}()")
    assert found == [], found


# -- a home that exists but cannot be written (environment suite, lane E3) ------

_CAN_WRITE_ROOT = os.access("/", os.W_OK)

_CAPTURE_CHILD = """
import probe
run = probe.init(project="slash", name="r")
print("hello from the job", flush=True)
with open("data.csv") as handle:
    handle.read()
probe.log({"loss": 0.5}, step=0)
probe.finish()
print("RUN", run.id)
"""


@pytest.mark.skipif(_CAN_WRITE_ROOT, reason="root can write a read-only folder")
def test_capture_state_moves_to_the_stand_in_when_home_cannot_be_written(tmp_path, monkeypatch):
    """HOME exists but is read-only: capture state takes the private
    `$TMPDIR/probe-home-<uid>`, as a process with no home does. A writable
    home keeps it (the control)."""
    from probe.sdk import inputs, outputs

    tmp = tmp_path / "tmp"
    tmp.mkdir()
    locked = tmp_path / "locked-home"
    locked.mkdir()
    locked.chmod(0o500)
    monkeypatch.delenv("XDG_STATE_HOME", raising=False)
    monkeypatch.setattr(tempfile, "tempdir", str(tmp))
    monkeypatch.setattr(homedir, "_stand_in", None)
    monkeypatch.setattr(homedir, "_state_writable", {}, raising=False)
    try:
        monkeypatch.setenv("HOME", str(locked))
        stand_in = tmp / f"probe-home-{os.getuid()}"
        assert homedir.home() == locked, "a home that exists is still the home"
        assert inputs.state_dir() == stand_in / ".local" / "state" / "probe" / "reads"
        assert outputs.state_dir() == stand_in / ".local" / "state" / "probe"
        assert stat.S_IMODE(os.stat(stand_in).st_mode) == 0o700
        assert list(locked.iterdir()) == [], "nothing left in the read-only home"

        writable = tmp_path / "home"
        writable.mkdir()
        monkeypatch.setenv("HOME", str(writable))
        assert inputs.state_dir() == writable / ".local" / "state" / "probe" / "reads"
        assert outputs.state_dir() == writable / ".local" / "state" / "probe"
    finally:
        locked.chmod(0o700)


@pytest.mark.skipif(_CAN_WRITE_ROOT, reason="`/` is writable here, so HOME=/ is not the case")
def test_home_slash_still_captures_the_run_log_and_reads(app, tmp_path):
    """`docker run --user 12345` gives an unknown uid HOME=/, which it cannot
    write. The outbox fell back to `$TMPDIR` (plan 1.5) but output and read
    capture did not start ('Permission denied: /.local'): the run had no
    `probe/run.log` and no read list. Now both use the outbox's kind of
    fallback, `$TMPDIR/probe-home-<uid>`."""
    work = tmp_path / "work"
    work.mkdir()
    (work / "data.csv").write_text("a,b\n1,2\n")
    tmp = tmp_path / "tmp"
    tmp.mkdir()
    with serve(app) as url:
        from probe.sdk.client import Client

        app.upload_base = url  # the child PUTs the log's bytes here, not to r2.test
        setup = Client(base_url=url, token="ros_pat_deadbeef", async_writes=False, auto_drain=False,
                       spool_dir=tmp_path / "setup-spool")
        try:
            setup.create_project("slash", "slash", kind="general")
        finally:
            setup.close()
        env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "TZ") if k in os.environ}
        env.update({
            "HOME": "/",
            "TMPDIR": str(tmp),
            "PYTHONPATH": os.pathsep.join(filter(None, [os.environ.get("PYTHONPATH")])),
            "PROBE_BASE_URL": url,
            "PROBE_TOKEN": "ros_pat_deadbeef",
            "PROBE_TELEMETRY": "off",
            "PROBE_AUTO_SNAPSHOT": "0",
            "PROBE_HW": "0",
        })
        proc = subprocess.run(
            [sys.executable, "-c", _CAPTURE_CHILD], env=env, cwd=work, capture_output=True, text=True,
            timeout=180,
        )
    assert proc.returncode == 0, proc.stderr[-3000:]
    assert "could not start" not in proc.stderr, proc.stderr[-3000:]
    (run_id,) = [line.split()[1] for line in proc.stdout.splitlines() if line.startswith("RUN ")]
    logs = [a for a in app.artifacts.get(run_id, []) if a["name"] == "probe/run.log"]
    assert logs, f"no probe/run.log; stderr: {proc.stderr[-2000:]}"
    stored = app.blobs.get(logs[0]["id"]) or app.blobs_by_hash.get(logs[0]["content_hash"])
    assert b"hello from the job" in stored
    reads = [
        row["path"]
        for request in app.requests
        if request.method == "POST" and request.url.path == f"/v1/runs/{run_id}/inputs"
        for row in json.loads(request.content)["inputs"]
    ]
    assert reads == [str(work / "data.csv")]
    assert (tmp / f"probe-home-{os.getuid()}" / ".local" / "state" / "probe").is_dir()
    assert app.runs[run_id]["status"] == "completed"


_RECORDER_CHILD = """
import json, os, subprocess, sys
from probe.sdk import inputs
data, out, worker_read = sys.argv[1:4]
assert inputs.start("run-homeless") and inputs.bind_workers("run-homeless")
state = inputs._active["run-homeless"]
open(data, "rb").read()
with open(out, "wb") as handle:
    handle.write(b"o" * 100)
state.check_writes()  # the heartbeat's look: the .wf.json sidecar
subprocess.run([sys.executable, "-c", f"open({worker_read!r}, 'rb').read()"], check=True)
sidecars = [str(p) for p in inputs.run_dir("run-homeless").glob("*.wf.json")]
binding = os.environ[inputs.BIND_ENV]
got = inputs.collect_all("run-homeless", wait_s=5)
print("RESULT " + json.dumps({
    "binding": binding, "sidecars": sidecars,
    "reads": sorted(r["path"] for r in got.inputs), "writes": [r["path"] for r in got.outputs],
}))
"""


@pytest.mark.parametrize("home", ["unset", "/"])
def test_the_recorder_binding_and_sidecars_work_with_no_usable_home(tmp_path, home):
    """HOME unset with no passwd entry, or HOME=/ (not writable): the read
    and write recorder, the spawned-worker binding file and the `.wf.json`
    sidecar all live under the private `$TMPDIR/probe-home-<uid>`."""
    tmp = tmp_path / "tmp"
    tmp.mkdir()
    work = tmp_path / "work"
    work.mkdir()
    data, out, worker_read = work / "data.bin", work / "out.bin", work / "worker.bin"
    data.write_bytes(b"d" * 100)
    worker_read.write_bytes(b"k" * 100)
    env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "TZ") if k in os.environ}
    env.update({"TMPDIR": str(tmp), "PROBE_CAPTURE_READS": "1", "PROBE_TELEMETRY": "off",
                "PYTHONPATH": os.pathsep.join(sys.path)})
    code = _RECORDER_CHILD
    if home == "unset":
        code = _NO_PASSWD_ENTRY + code
    else:
        env["HOME"] = "/"
    proc = subprocess.run([sys.executable, "-c", code, str(data), str(out), str(worker_read)], env=env,
                          cwd=work, capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stderr[-3000:]
    (line,) = [x for x in proc.stdout.splitlines() if x.startswith("RESULT ")]
    got = json.loads(line[len("RESULT "):])
    state = tmp / f"probe-home-{os.getuid()}" / ".local" / "state" / "probe"
    assert got["binding"].startswith(str(state / "bind") + os.sep), got
    assert got["sidecars"] and all(s.startswith(str(state / "reads")) for s in got["sidecars"]), got
    assert got["reads"] == sorted([str(data), str(worker_read)]), got
    assert got["writes"] == [str(out)], got
