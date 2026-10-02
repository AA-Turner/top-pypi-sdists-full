"""Spawned workers record into the run (lineage plan 3, F5).

A fork inherits the audit hook; a worker started by spawn or forkserver is a
fresh interpreter that has none. `probe.init()` now binds this process's
Python workers to its run (`inputs.bind_workers`): the environment gives new
workers the child hook `probe exec` uses, and a binding file tells the ones
already running which run they belong to. These tests pin the lifecycle:
spawn and forkserver workers land in the right run; a persistent worker stops
recording a closed run and follows its owner to the next one, and what it
spooled after the close is cut; two runs at once bind nothing; the
environment is restored at finish; and an opt-out -- the run's, the worker's
environment's, or a worker opening its own run -- propagates.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

import probe
from probe.sdk import fluent, inputs
from tests.conftest import make_client


@pytest.fixture(autouse=True)
def _recorder(monkeypatch, tmp_path):
    monkeypatch.setenv(inputs.READS_ENV, "1")
    for name in (inputs.CHILD_DIR_ENV, inputs.OWNER_PID_ENV, inputs.BIND_ENV, inputs.WRITES_ENV,
                 inputs.OUTPUTS_ENV, "PROBE_RUN_ID", "PROBE_RUN_EPOCH"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    inputs._active.clear()
    inputs._hash_results.clear()
    fluent._current.set(None)
    fluent._process_default = None
    yield
    inputs._active.clear()
    if inputs._bound is not None:
        inputs._unbind()
    fluent._current.set(None)
    fluent._process_default = None


def _data(tmp_path: Path, name: str, size: int = 200) -> Path:
    path = tmp_path / "work" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(name.encode() * max(size // len(name), 1))
    return path


def _python(tmp_path: Path, code: str, **env: str) -> subprocess.CompletedProcess:
    """Run ``code`` in a FRESH interpreter as the owner: its own os.environ,
    multiprocessing state and forkserver. The workers' targets live in a
    module beside it (``workers``), importable by a spawned child."""
    (tmp_path / "workers.py").write_text(
        textwrap.dedent(
            """
            import time

            def read(path):
                with open(path, "rb") as handle:
                    return len(handle.read())

            def write(path, data):
                with open(path, "wb") as handle:
                    handle.write(data)
            """
        )
    )
    full = {
        **os.environ,
        "XDG_STATE_HOME": str(tmp_path / "state"),
        "PROBE_OUTBOX_DIR": str(tmp_path / "outbox"),
        inputs.READS_ENV: "1",
        "PYTHONPATH": os.pathsep.join([str(tmp_path), os.environ.get("PYTHONPATH", "")]).rstrip(os.pathsep),
        **env,
    }
    for name in (inputs.CHILD_DIR_ENV, inputs.OWNER_PID_ENV, inputs.BIND_ENV):
        full.pop(name, None)
    out = subprocess.run(
        [sys.executable, "-c", textwrap.dedent(code)], env=full, capture_output=True, text=True, timeout=120
    )
    assert out.returncode == 0, out.stderr[-4000:]
    return out


def _paths(got) -> list[str]:
    return sorted(row["path"] for row in got.inputs)


# -- the binding --------------------------------------------------------------------


@pytest.mark.parametrize("method", ["spawn", "forkserver"])
def test_spawned_and_forkserver_workers_record_into_the_run(tmp_path, method) -> None:
    data = _data(tmp_path, f"{method}.bin")
    out = tmp_path / "work" / f"{method}-out.bin"
    got = _python(
        tmp_path,
        f"""
        import json, multiprocessing, workers
        from probe.sdk import inputs
        assert inputs.start("run-{method}")
        assert inputs.bind_workers("run-{method}")
        ctx = multiprocessing.get_context("{method}")
        for target, args in ((workers.read, ({str(data)!r},)), (workers.write, ({str(out)!r}, b"o" * 99))):
            proc = ctx.Process(target=target, args=args)
            proc.start()
            proc.join(60)
            assert proc.exitcode == 0
        got = inputs.collect_all("run-{method}", wait_s=10)
        print(json.dumps({{"reads": [r["path"] for r in got.inputs],
                          "writes": [r["path"] for r in got.outputs]}}))
        """,
    )
    answer = json.loads(got.stdout.strip().splitlines()[-1])
    assert answer == {"reads": [str(data)], "writes": [str(out)]}


def test_an_offline_runs_spawned_worker_records_into_it(tmp_path) -> None:
    """An offline run's id is `local:<key>`. Its folder, named after the id,
    put a colon on PYTHONPATH -- which splits on it -- so no spawned worker
    ever loaded the hook. The folder name escapes it (`inputs.run_folder`);
    the spool header still names the run by its id, and the close queues the
    worker's read for `probe sync`."""
    data = _data(tmp_path, "offline.bin")
    got = _python(
        tmp_path,
        f"""
        import json, multiprocessing, os, workers
        import probe
        from probe.sdk import inputs, offline
        from probe.sdk.journal import Journal

        run = probe.init(mode="offline", project="p1", name="spawner")
        assert run.id.startswith("local:"), run.id
        site = os.environ["PYTHONPATH"].split(os.pathsep)[0]
        hook = os.path.isfile(os.path.join(site, "sitecustomize.py"))
        with multiprocessing.get_context("spawn").Pool(1) as pool:
            assert pool.apply(workers.read, ({str(data)!r},)) > 0
        probe.finish()
        (queue,) = offline.find_offline_dirs()
        reads = [row["path"] for _, op in Journal(queue).pending() if str(op.get("path")).endswith("/inputs")
                 for row in op["body"]["inputs"]]
        left = [str(p) for p in inputs.state_dir().rglob("*.jsonl")]
        print(json.dumps({{"site": site, "hook": hook, "reads": reads, "left": left}}))
        """,
        PROBE_BASE_URL="http://offline.invalid",
        PROBE_TELEMETRY="0",
    )
    answer = json.loads(got.stdout.strip().splitlines()[-1])
    assert answer["hook"] and ":" not in answer["site"], answer["site"]
    assert str(data) in answer["reads"], answer
    assert answer["left"] == []


def test_a_run_folder_name_carries_no_separator_and_maps_back() -> None:
    """Stable (the owner, its workers, a recovery and `probe sync` agree) and
    reversible (a recovery reads the run id off the folder)."""
    server = "0f8e2c1a-4b7d-4c1e-9a0b-3d2f1e0c9b8a"
    assert inputs.run_folder(server) == server and inputs.run_dir(server).name == server
    for run_id in ("local:" + "a" * 32, "a/b\\c;d%e:f", "local%3Aabc"):
        name = inputs.run_folder(run_id)
        assert not set(name) & set(":;/\\" + os.pathsep + os.sep), name
        assert inputs._folder_run(name) == run_id
        assert inputs.run_dir(run_id).parent == inputs.state_dir()
    assert inputs.run_folder("local:abc") == "local%3Aabc"


def test_init_binds_workers_and_finish_restores_the_environment(app, tmp_path, monkeypatch) -> None:
    """`probe.init()` binds; a `python` subprocess is a spawned worker too;
    `probe.finish()` unbinds and leaves the environment as it found it."""
    data = _data(tmp_path, "features.bin")
    monkeypatch.setenv("PYTHONPATH", "/somewhere/else")
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("e1")
    run = probe.init(experiment="e1", name="spawner")
    assert os.environ[inputs.CHILD_DIR_ENV] == str(inputs.run_dir(run.id))
    assert os.environ[inputs.OWNER_PID_ENV] == str(os.getpid())
    site, rest = os.environ["PYTHONPATH"].split(os.pathsep, 1)
    assert Path(site, "sitecustomize.py").exists() and rest == "/somewhere/else"
    binding = Path(os.environ[inputs.BIND_ENV])
    assert json.loads(binding.read_text())["run"] == run.id
    env = {**os.environ, "PYTHONPATH": os.environ["PYTHONPATH"] + os.pathsep + os.pathsep.join(sys.path)}
    subprocess.run([sys.executable, "-c", f"open({str(data)!r}, 'rb').read()"], env=env, check=True)
    probe.finish()
    paths = [r["path"] for b in app.__dict__.get("run_inputs", {}).get(run.id, []) for r in b["inputs"]]
    assert str(data) in paths
    assert os.environ["PYTHONPATH"] == "/somewhere/else"
    for name in (inputs.CHILD_DIR_ENV, inputs.OWNER_PID_ENV, inputs.BIND_ENV):
        assert name not in os.environ
    assert not binding.exists()


def test_a_second_run_unbinds_and_the_one_left_is_bound(tmp_path) -> None:
    """Only while exactly one run records here: with two, a worker's reads
    belong to neither for sure."""
    pythonpath = os.environ.get("PYTHONPATH")
    assert inputs.start("run-one") and inputs.bind_workers("run-one")
    assert os.environ[inputs.CHILD_DIR_ENV] == str(inputs.run_dir("run-one"))
    assert inputs.start("run-two")
    assert inputs.bind_workers("run-two") is False
    assert inputs.CHILD_DIR_ENV not in os.environ and inputs._bound is None
    inputs.collect_all("run-one", wait_s=1)  # run-two is alone again
    assert os.environ[inputs.CHILD_DIR_ENV] == str(inputs.run_dir("run-two"))
    inputs.collect_all("run-two", wait_s=1)
    assert inputs.CHILD_DIR_ENV not in os.environ and os.environ.get("PYTHONPATH") == pythonpath


def test_a_run_opened_by_a_cli_or_service_binds_nothing() -> None:
    """Only `probe.init()` asks: `start` alone never touches the environment."""
    assert inputs.start("run-service")
    assert inputs.CHILD_DIR_ENV not in os.environ and inputs._bound is None
    inputs.abandon("run-service")


@pytest.mark.parametrize("method", ["spawn", "fork"])
def test_a_persistent_worker_follows_its_owner_to_the_next_run(tmp_path, method) -> None:
    """A Pool (or persistent DataLoader) worker outlives the run it started
    in: after the close it records nothing into it -- what it spooled in the
    moments before it noticed is cut at the close -- and once a second run
    opens it records into that one."""
    a, late, between, d = (_data(tmp_path, f"{n}.bin") for n in ("a", "late", "between", "d"))
    got = _python(
        tmp_path,
        f"""
        import json, multiprocessing, time, workers
        from probe.sdk import inputs

        class Client:
            journal = None
            def supports_feature(self, name):
                return True

        assert inputs.start("run-1") and inputs.bind_workers("run-1")
        pool = multiprocessing.get_context("{method}").Pool(1)
        pool.apply(workers.read, ({str(a)!r},))
        inputs._stop("run-1")  # the close: marked, then unbound
        pool.apply(workers.read, ({str(late)!r},))  # before the worker looks again
        first = inputs.collect_all("run-1", wait_s=10)
        inputs.discard("run-1")
        time.sleep(3 * inputs.BIND_CHECK_S)
        pool.apply(workers.read, ({str(between)!r},))  # no run: nothing
        assert inputs.start("run-2") and inputs.bind_workers("run-2")
        time.sleep(3 * inputs.BIND_CHECK_S)
        pool.apply(workers.read, ({str(d)!r},))
        second = inputs.collect_all("run-2", wait_s=10)
        inputs.discard("run-2")
        pool.close(); pool.join()
        left = sorted(str(p) for p in inputs.state_dir().rglob("*.jsonl"))
        print(json.dumps({{"run-1": [r["path"] for r in first.inputs],
                          "run-2": [r["path"] for r in second.inputs], "left": left}}))
        """,
    )
    answer = json.loads(got.stdout.strip().splitlines()[-1])
    assert answer["run-1"] == [str(a)], "the read after the close is not the closed run's"
    assert answer["run-2"] == [str(d)]
    assert answer["left"] == [], "nothing left for a recovery to send to either run"


def test_the_close_takes_its_workers_live_spools_and_cuts_them_there(tmp_path) -> None:
    """A live worker's spool is its owner's to take at the close (its header
    names the owner; a rank's names itself and is left), and what it spooled
    after the close -- in the moments before it looked at the binding again
    -- is dropped: a read made after the close is not the closed run's."""
    from datetime import datetime, timedelta, timezone

    early, late = _data(tmp_path, "early.bin"), _data(tmp_path, "late.bin")
    assert inputs.start("run-cut") and inputs.bind_workers("run-cut")
    now = datetime.now(timezone.utc)

    def line(path: Path, at: datetime) -> str:
        st = os.stat(path)
        return json.dumps({"p": str(path), "d": st.st_dev, "i": st.st_ino, "s": st.st_size,
                           "m": st.st_mtime_ns, "c": st.st_ctime_ns, "t": at.isoformat()}) + "\n"

    worker = os.getppid()  # alive, and not this process
    spool = inputs.run_dir("run-cut") / f"{inputs._host()}.{worker}.jsonl"
    spool.write_text(
        json.dumps({"run": "run-cut", "owner": os.getpid(), "follows": True}) + "\n"
        + line(early, now - timedelta(seconds=30))
        + line(late, now + timedelta(seconds=30))
    )
    got = inputs.collect_all("run-cut", wait_s=5)
    assert _paths(got) == [str(early)]
    assert got.inputs_coverage["pending_spools"] == 0, "the worker's live spool was taken"


def test_a_spool_bound_to_another_run_is_skipped(tmp_path) -> None:
    data = _data(tmp_path, "stray.bin")
    assert inputs.start("run-own-spools")
    directory = inputs.run_dir("run-own-spools")
    st = os.stat(data)
    dead = int(subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                              capture_output=True, text=True, check=True).stdout)
    stray = {"p": str(data), "d": st.st_dev, "i": st.st_ino, "s": st.st_size, "m": st.st_mtime_ns,
             "c": st.st_ctime_ns, "t": "2026-09-28T00:00:00+00:00"}
    (directory / f"{inputs._host()}.{dead}.jsonl").write_text(
        json.dumps({"run": "someone-else", "owner": dead}) + "\n" + json.dumps(stray) + "\n"
    )
    assert inputs.collect_all("run-own-spools", wait_s=1).inputs == []


# -- opt-outs propagate ----------------------------------------------------------


def test_a_run_without_writes_binds_its_workers_without_writes(tmp_path) -> None:
    data = _data(tmp_path, "in.bin")
    out = tmp_path / "work" / "out.bin"
    assert inputs.start("run-no-writes", capture_outputs=False)
    assert inputs.bind_workers("run-no-writes")
    code = f"open({str(data)!r}, 'rb').read(); open({str(out)!r}, 'wb').write(b'x' * 50)"
    subprocess.run([sys.executable, "-c", code], env=_worker_env(), check=True)
    got = inputs.collect_all("run-no-writes", wait_s=5)
    assert _paths(got) == [str(data)] and got.outputs == []


def test_a_worker_whose_environment_opts_out_records_nothing(tmp_path) -> None:
    data = _data(tmp_path, "quiet.bin")
    assert inputs.start("run-quiet-worker") and inputs.bind_workers("run-quiet-worker")
    env = {**_worker_env(), inputs.READS_ENV: "0"}
    subprocess.run([sys.executable, "-c", f"open({str(data)!r}, 'rb').read()"], env=env, check=True)
    assert inputs.collect_all("run-quiet-worker", wait_s=5).inputs == []


@pytest.mark.parametrize("own_capture", [False, True])
def test_a_worker_opening_its_own_run_leaves_the_binding(tmp_path, own_capture) -> None:
    """A worker that calls `probe.init()` for a run of its own (or opts out)
    stops recording into the owner's run -- quietly: the owner did not opt
    out -- and its own workers are not bound to the owner's run either."""
    before, after, grandchild = (_data(tmp_path, f"{n}.bin") for n in ("before", "after", "grandchild"))
    assert inputs.start("run-owner") and inputs.bind_workers("run-owner")
    grand = f"open({str(grandchild)!r}, 'rb').read()"
    code = (
        "import os, subprocess, sys\n"
        "from probe.sdk import inputs\n"
        f"open({str(before)!r}, 'rb').read()\n"
        f"inputs.start('run-worker-own', capture_reads={own_capture})\n"
        f"open({str(after)!r}, 'rb').read()\n"
        f"subprocess.run([sys.executable, '-c', {grand!r}], check=True)\n"
        "print(os.environ.get('PROBE_READS_DIR'), os.environ.get('PROBE_READS_OWNER_PID'))\n"
    )
    out = subprocess.run([sys.executable, "-c", code], env=_worker_env(), check=True, capture_output=True, text=True)
    assert out.stdout.split() == ["None", "None"]
    got = inputs.collect_all("run-owner", wait_s=5)
    assert _paths(got) == [str(before)], "only what it read while it was the owner's worker"
    assert got.inputs_coverage.get("truncated") is False
    assert "inputs" not in got.opted_out, "the owner did not opt out"


def test_an_exec_child_of_a_bound_process_is_a_plain_exec_child() -> None:
    assert inputs.start("run-launcher-bound") and inputs.bind_workers("run-launcher-bound")
    env = dict(os.environ)
    assert inputs.prepare_child("run-exec-inner", env)
    assert inputs.OWNER_PID_ENV not in env and inputs.BIND_ENV not in env
    assert env[inputs.CHILD_DIR_ENV] == str(inputs.run_dir("run-exec-inner"))
    assert str(inputs.run_dir("run-launcher-bound")) not in env["PYTHONPATH"]
    inputs.abandon("run-launcher-bound")


def _worker_env() -> dict[str, str]:
    """This (bound) process's environment, as a subprocess inherits it --
    with the test's import path, so the worker can import Probe."""
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([env.get("PYTHONPATH", ""), *sys.path]).strip(os.pathsep)
    return env


def test_a_forked_worker_never_binds_workers_of_its_own() -> None:
    """A worker forked while its parent was bound follows the parent's
    binding; it must never become an owner of the parent's run itself."""
    assert inputs.start("run-fork-owner") and inputs.bind_workers("run-fork-owner")
    pid = os.fork()
    if pid == 0:  # the forked worker
        try:
            inputs._rebind()
            os._exit(0 if inputs._bound is None else 1)
        except BaseException:
            os._exit(2)
    _, status = os.waitpid(pid, 0)
    assert os.waitstatus_to_exitcode(status) == 0
    assert inputs._bound is not None and inputs._bound["pid"] == os.getpid()
    inputs.abandon("run-fork-owner")
