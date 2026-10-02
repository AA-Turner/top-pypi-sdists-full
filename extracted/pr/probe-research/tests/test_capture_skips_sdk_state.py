"""Capture never takes the SDK's own files as the run's code, reads or outputs.

Found by the environment suite (lane E3, #2112): a job started in `$TMPDIR`
(`docker run -w /tmp`) with no usable home queues in `$TMPDIR/probe-outbox-<uid>`
and keeps its state in `$TMPDIR/probe-home-<uid>` (#2109) -- and the code
snapshot swept that queue into the run's manifest. The same happens to any
working folder that holds the outbox or the state folder (`PROBE_OUTBOX_DIR` or
`XDG_STATE_HOME` inside the project, an explicit `spool_dir`). Read capture
excluded only the default `~/.local/state/probe`, and the output sweep only
this client's own queue and state.

Every test puts ALL of those places inside the run's working folder, each
holding a queued op an earlier job left, beside the user's own files -- some
named like Probe's -- which must still be captured.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

from probe.sdk import homedir, inputs, journal
from tests.conftest import make_client, open_run

UID = os.getuid()
#: `owndirs.REASON`, spelled out: the capture tests must run (and fail) on a
#: tree without the module.
REASON = "probe_state"
_OP = '{"kind": "http", "request": {"method": "POST", "path": "/v1/runs/earlier/metrics"}}'
#: Where the SDK keeps files, relative to the working folder (see `sdk_places`).
SDK_PLACES = (
    "outbox",  # PROBE_OUTBOX_DIR
    "queue",  # an explicit spool_dir
    "state/probe",  # XDG_STATE_HOME
    f"probe-outbox-{UID}",  # the outbox's $TMPDIR fallback
    f"probe-outbox-{UID}-k2j4",  # ... when the fixed name was taken (mkdtemp)
    f"probe-home-{UID}",  # the no-home stand-in, and capture state under HOME=/
)
#: The user's files: captured, whatever they are called.
USER_FILES = {
    "train.py": "print('train')\n",
    "data/probe-outbox.csv": "a,b\n1,2\n",
    "outbox-notes/ops/readme.txt": "my own notes about queues\n",
    f"probe-outbox-{UID}x.txt": "not the SDK's: another name\n",
}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


@pytest.fixture
def work(tmp_path, monkeypatch):
    """A working folder that is also `$TMPDIR`, and holds every SDK place."""
    work = tmp_path / "work"
    work.mkdir()
    for rel, text in USER_FILES.items():
        _write(work / rel, text)
    for place in SDK_PLACES:
        _write(work / place / "ops" / "00000000000000000001.json", _OP)
        os.chmod(work / place, 0o700)
    _write(work / "state" / "probe-telemetry" / "machine_id", "m-1")
    _write(work / f"probe-hw-run-earlier-{os.uname().nodename}.lock", "4242")
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(work / "outbox"))
    monkeypatch.setenv("XDG_STATE_HOME", str(work / "state"))
    monkeypatch.setattr(tempfile, "tempdir", str(work))
    monkeypatch.setattr(homedir, "_stand_in", None)
    monkeypatch.setattr(journal, "_private_fallback", None)
    monkeypatch.chdir(work)
    return work


def _sdk_paths(paths) -> list[str]:
    """The paths among ``paths`` that are the SDK's (by the fixture's layout)."""
    places = (*SDK_PLACES, "state/probe-telemetry")

    def sdk(path: str) -> bool:
        parts = path.split("/")
        return (
            parts[0] in places
            or "/".join(parts[:2]) in places
            or (len(parts) == 1 and parts[0].startswith("probe-hw-"))
        )

    return sorted(p for p in paths if sdk(p))


def _git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


@pytest.mark.parametrize("tree", ["plain", "git"])
def test_the_code_snapshot_skips_every_sdk_folder_in_the_working_folder(app, work, tree):
    if tree == "git":
        _git(work, "init", "-q")
        _git(work, "-c", "user.email=t@e.com", "-c", "user.name=t", "add", "train.py")
        _git(work, "-c", "user.email=t@e.com", "-c", "user.name=t", "commit", "-qm", "init")
    client = make_client(app, tmp_spool=work / "queue")
    try:
        run = open_run(client, experiment="own-state", snapshot=True)
        run.finish()
    finally:
        client.close()
    (record,) = app.execution_records.values()
    manifest = record["code"]["manifest"]
    captured = {e["path"] for e in manifest["entries"]}
    assert _sdk_paths(captured) == [], "the SDK's own files were taken as the run's code"
    assert set(USER_FILES) <= captured, "a user file was skipped"
    reported = {s["path"] for s in manifest["skipped"] if s["reason"] == REASON}
    # Once per folder (and the lock file), never file by file.
    assert reported == {
        "outbox", "queue", "state/probe", "state/probe-telemetry",
        f"probe-outbox-{UID}", f"probe-outbox-{UID}-k2j4", f"probe-home-{UID}",
        f"probe-hw-run-earlier-{os.uname().nodename}.lock",
    }


def test_read_capture_never_records_an_sdk_file(app, work, monkeypatch):
    """A data loader that opens every file under the working folder."""
    monkeypatch.setenv(inputs.READS_ENV, "1")
    monkeypatch.delenv(inputs.CHILD_DIR_ENV, raising=False)
    inputs._active.clear()
    # The explicit spool_dir is known only through the Client that queues in it.
    client = make_client(app, tmp_spool=work / "queue")
    assert inputs.start("run-own-reads")
    try:
        for path in sorted(work.rglob("*")):
            if path.is_file():
                # The SDK's own sender can deliver-and-remove or rename a
                # queued op file between this listing and the open below
                # (it shares `work` with the client's live queue) -- that
                # race is not what this test is about, so skip a file that
                # vanished out from under us instead of failing on it.
                try:
                    with open(path, "rb") as handle:
                        handle.read()
                except (FileNotFoundError, IsADirectoryError):
                    continue
        rows, _ = inputs.collect("run-own-reads", wait_s=5)
    finally:
        inputs._active.clear()
        client.close()
    read = sorted(os.path.relpath(r["path"], work) for r in rows)
    assert _sdk_paths(read) == [], "the SDK's own files were recorded as the run's reads"
    assert read == sorted(p for p in USER_FILES if not p.endswith(".py"))


def test_the_output_sweep_never_takes_an_sdk_file(app, work):
    """Files the SDK writes during the run, in every one of its places, are
    not the run's outputs; the user's new file is."""
    client = make_client(app, tmp_spool=work / "queue")
    try:
        run = open_run(client, experiment="own-outputs", capture_outputs=True)
        for place in SDK_PLACES:
            _write(work / place / "ops" / "00000000000000000002.json", _OP)
        _write(work / "state" / "probe-telemetry" / "machine_id", "m-2")
        _write(work / "results" / "metrics.json", '{"loss": 0.1}')
        run.finish()
    finally:
        client.close()
    names = {a["name"] for a in app.artifacts.get(run.id, [])}
    swept = sorted(n[len("outputs/"):] for n in names if n.startswith("outputs/"))
    assert _sdk_paths(swept) == [], "the SDK's own files were swept as outputs"
    assert "results/metrics.json" in swept


_CHILD = """
import probe
run = probe.init(project="tmpjob", name="r")
probe.log({"loss": 0.5}, step=0)
probe.finish()
print("RUN", run.id)
"""


def test_a_job_started_in_tmpdir_with_no_usable_home(app, tmp_path):
    """The environment suite's shape (managed[home=/], `-w /tmp`): HOME is `/`,
    so the outbox and capture state fall back into `$TMPDIR`, which is also
    the working folder. A queue an earlier job left there, and everything
    this job writes there, stays out of its code snapshot."""
    from tests.served_fake_app import serve

    tmp = tmp_path / "tmp"
    earlier = tmp / f"probe-outbox-{UID}" / "ops"
    earlier.mkdir(parents=True)
    os.chmod(tmp / f"probe-outbox-{UID}", 0o700)
    (earlier / "00000000000000000001.json").write_text(_OP)
    (tmp / "train.py").write_text(_CHILD)
    with serve(app) as url:
        from probe.sdk.client import Client

        setup = Client(base_url=url, token="ros_pat_deadbeef", async_writes=False,
                       auto_drain=False, spool_dir=tmp_path / "setup-spool")
        try:
            setup.create_project("tmpjob", "tmpjob", kind="general")
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
            "PROBE_HW": "0",
        })
        proc = subprocess.run([sys.executable, "train.py"], env=env, cwd=tmp,
                              capture_output=True, text=True, timeout=180)
    assert proc.returncode == 0, proc.stderr[-3000:]
    (manifest,) = [r["code"]["manifest"] for r in app.execution_records.values() if r.get("code")]
    captured = sorted(e["path"] for e in manifest["entries"])
    assert captured == ["train.py"], captured
    assert {s["path"] for s in manifest["skipped"] if s["reason"] == REASON} >= {
        f"probe-outbox-{UID}"
    }


# -- the matcher itself ----------------------------------------------------------


def test_a_folder_named_like_the_sdks_elsewhere_is_the_users(tmp_path, monkeypatch):
    from probe.sdk import owndirs

    assert owndirs.REASON == REASON
    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path / "tmp"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    own = owndirs.current()
    assert own.owns(str(tmp_path / "tmp" / f"probe-outbox-{UID}" / "ops" / "1.json"))
    assert own.owns(str(tmp_path / "state" / "probe" / "reads" / "r" / "h.1.jsonl"))
    assert not own.owns(str(tmp_path / "project" / f"probe-outbox-{UID}" / "ops" / "1.json"))
    assert not own.owns(str(tmp_path / "state" / "probe-results.csv"))
    assert not own.owns(str(tmp_path / "tmp" / "probe-outbox-notes.txt"))
    assert own.owns(str(tmp_path / "tmp" / f"probe-home-{UID}-x7q2" / ".local" / "state"))
    assert own.owns(str(tmp_path / "tmp" / "probe-hw-run-1-host.lock"))
    assert not own.owns(str(tmp_path / "tmp" / "sub" / f"probe-outbox-{UID}" / "1.json")), "only $TMPDIR's own entries"
    assert not own.owns(str(tmp_path / "tmp"))
    assert own.within(str(tmp_path / "project")) is None, "nothing of the SDK's below: no cost"


def test_a_capture_rooted_inside_an_sdk_folder_is_left_alone(tmp_path, monkeypatch):
    """A root that is itself inside one of the folders is the caller's choice
    of place: only what is below it counts."""
    from probe.sdk import owndirs

    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    within = owndirs.current().within(str(tmp_path / "outbox" / "ops"))
    assert within is None or within.top("1.json") is None


def test_many_noted_outboxes_cost_one_lookup_per_path_level(tmp_path):
    """Read capture asks on every open(): thousands of outboxes one process
    used (the test suite's) must not become a scan."""
    import time

    from probe.sdk import owndirs

    for i in range(5000):
        owndirs.note(tmp_path / f"q{i}")
    own = owndirs.current()
    started = time.perf_counter()
    for _ in range(2000):
        own.owns(str(tmp_path / "data" / "shard.tar"))
    assert time.perf_counter() - started < 0.5
    assert own.owns(str(tmp_path / "q4999" / "ops" / "1.json"))
