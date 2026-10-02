"""Review of lineage plan 3, batch B2 (cf383d2a9): each P1 reproduced here first.

1. A second run opened with capture off left the first run's worker binding in
   the environment: its spawned workers recorded into the first run.
2. A worker kept following a binding file its crashed owner left behind --
   forever, and into a new process that reused the owner's pid.
3. The C-reader wrappers were one object per alias, so a wrapped function
   pickled by reference (multiprocessing, ProcessPoolExecutor) failed.
"""

from __future__ import annotations

import json
import os
import pickle
import subprocess
import sys
import textwrap
import threading
import time
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
    for name in (inputs.OWNER_PID_ENV, inputs.BIND_ENV, inputs.CHILD_DIR_ENV):
        os.environ.pop(name, None)  # never left for the next test
    fluent._current.set(None)
    fluent._process_default = None


def _data(tmp_path: Path, name: str) -> Path:
    path = tmp_path / "work" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(name.encode() * 20)
    return path


def _spooled(run_id: str) -> list[str]:
    """Every read path spooled for ``run_id``, by anyone."""
    out = []
    for spool in inputs.run_dir(run_id).glob("*.jsonl"):
        for line in spool.read_text().splitlines():
            if line.startswith('{"p"'):
                out.append(json.loads(line)["p"])
    return sorted(out)


# -- P1 1: an opted-out run beside a bound one ------------------------------------


def test_a_run_opened_with_capture_off_unbinds_the_other_runs_workers(app, tmp_path, monkeypatch) -> None:
    """Run A records and binds its workers; another thread opens run B with
    capture_reads=False. B never recorded, so A's binding stayed, and B's
    spawned workers recorded B's files into A. With two runs open nothing is
    bound; once B closes, A is bound again."""
    b_data, a_data = _data(tmp_path, "b_only.bin"), _data(tmp_path, "a_again.bin")
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("e1")
    run_a = probe.init(experiment="e1", name="a")
    assert inputs._bound is not None and inputs._bound["run"] == run_a.id
    seen: dict = {}

    def other_thread() -> None:
        run_b = probe.init(experiment="e1", name="b", capture_reads=False)
        seen["bound_while_b"] = inputs._bound
        subprocess.run([sys.executable, "-c", f"open({str(b_data)!r}, 'rb').read()"], env=dict(os.environ),
                       check=True)
        run_b.finish()

    worker = threading.Thread(target=other_thread)
    worker.start()
    worker.join(60)
    assert seen["bound_while_b"] is None, "two runs open: nothing bound"
    assert str(b_data) not in _spooled(run_a.id), "B's worker's read is not A's"
    assert inputs._bound is not None and inputs._bound["run"] == run_a.id, "A alone again: bound"
    subprocess.run([sys.executable, "-c", f"open({str(a_data)!r}, 'rb').read()"], env=dict(os.environ),
                   check=True)
    assert str(a_data) in _spooled(run_a.id)
    probe.finish()


# -- P1 2: a crashed owner ----------------------------------------------------------


_OWNER = """
import os, subprocess, sys, time
from probe.sdk import inputs
assert inputs.start("run-crashed") and inputs.bind_workers("run-crashed")
{spawn}
open({ready!r}, "w").write(str(pid))
os._exit(0)  # a crash: nothing unbinds
"""

_WORKER = """
import os, sys, time
trigger, data, done = sys.argv[1:4]
while not os.path.exists(trigger):
    time.sleep(0.02)
open(data, "rb").read()
open(done, "w").write("x")
"""


def _crash_owner(tmp_path: Path, spawn: str) -> tuple[Path, Path, Path]:
    (tmp_path / "worker.py").write_text(_WORKER)
    trigger, data, done = tmp_path / "go", _data(tmp_path, "after_crash.bin"), tmp_path / "done"
    ready = tmp_path / "ready"
    code = textwrap.dedent(_OWNER).format(
        spawn=spawn.format(worker=str(tmp_path / "worker.py"), args=[str(trigger), str(data), str(done)]),
        ready=str(ready),
    )
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(sys.path)}
    for name in (inputs.CHILD_DIR_ENV, inputs.OWNER_PID_ENV, inputs.BIND_ENV):
        env.pop(name, None)
    subprocess.run([sys.executable, "-c", code], env=env, check=True, timeout=60)
    assert ready.exists()
    # A worker learns its owner died at its next liveness look: within
    # OWNER_CHECK_S of its last one.
    time.sleep(inputs.OWNER_CHECK_S + 3 * inputs.BIND_CHECK_S)
    trigger.write_text("go")
    deadline = time.monotonic() + 30
    while not done.exists() and time.monotonic() < deadline:
        time.sleep(0.02)
    assert done.exists()
    time.sleep(0.2)
    return data, trigger, done


_SPAWN = (
    "proc = subprocess.Popen([sys.executable, {worker!r}, *{args!r}])\n"
    "pid = proc.pid\n"
    "open({worker!r} + '.first', 'wb')  # something the worker's owner saw"
)
_FORK = (
    "pid = os.fork()\n"
    "if pid == 0:\n"
    "    sys.argv[1:4] = {args!r}\n"
    "    exec(open({worker!r}).read())\n"
    "    os._exit(0)"
)


@pytest.mark.parametrize("spawn", [_SPAWN, _FORK], ids=["spawned", "forked"])
def test_a_worker_stops_recording_once_its_owner_died(tmp_path, spawn) -> None:
    data, _, _ = _crash_owner(tmp_path, spawn)
    assert str(data) not in _spooled("run-crashed"), "a read after the owner crashed is not the run's"


def test_a_new_owner_with_the_dead_owners_pid_is_not_followed(tmp_path, monkeypatch) -> None:
    """The owner crashed; a new process got its pid and binds another run.
    A worker of the dead owner must not follow the stranger into its run."""
    assert inputs.start("run-old") and inputs.bind_workers("run-old")
    worker_env = dict(os.environ)  # what the dead owner's worker holds
    inputs._active.clear()
    saved = inputs._bound["saved"]
    inputs._bound = None  # "crashed": nothing unbound, the file stays
    for name, value in saved.items():  # the stranger starts with a clean environment
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value
    # The stranger: same pid (this process), a new run and binding.
    getattr(inputs, "_reset_owner_identity", lambda: None)()
    assert inputs.start("run-stranger") and inputs.bind_workers("run-stranger")
    data = _data(tmp_path, "worker_read.bin")
    subprocess.run([sys.executable, "-c", f"open({str(data)!r}, 'rb').read()"], env=worker_env, check=True)
    assert str(data) not in _spooled("run-stranger") and str(data) not in _spooled("run-old")
    inputs.abandon("run-stranger")


# -- P1 3: one wrapper per original ------------------------------------------------


def test_a_wrapped_torch_save_pickles_and_is_one_object() -> None:
    torch = pytest.importorskip("torch", reason="torch is not installed (optional)")
    serialization = sys.modules["torch.serialization"]

    assert inputs.start("run-pickle-torch")
    try:
        assert hasattr(torch.save, "__probe_wrapped_by__")
        assert torch.save is serialization.save
        assert pickle.loads(pickle.dumps(torch.save)) is torch.save
    finally:
        inputs.abandon("run-pickle-torch")


def test_wrapped_pyarrow_functions_pickle_and_are_one_object() -> None:
    pa = pytest.importorskip("pyarrow", reason="pyarrow is not installed")
    pq = pytest.importorskip("pyarrow.parquet", reason="pyarrow is not installed")
    import pyarrow.lib
    import pyarrow.parquet.core as core

    assert inputs.start("run-pickle-pa")
    try:
        for alias, home in ((pq.read_metadata, core.read_metadata), (pq.read_schema, core.read_schema),
                            (pa.memory_map, pyarrow.lib.memory_map)):
            assert hasattr(alias, "__probe_wrapped_by__")
            assert alias is home
            assert pickle.loads(pickle.dumps(alias)) is alias
    finally:
        inputs.abandon("run-pickle-pa")


def test_a_process_pool_maps_a_wrapped_reader(tmp_path) -> None:
    """The reviewer's repro: `Pool.map(pq.read_metadata, paths)` after init."""
    pytest.importorskip("pyarrow.parquet", reason="pyarrow is not installed")
    code = textwrap.dedent(
        f"""
        import multiprocessing as mp, os
        import pyarrow as pa, pyarrow.parquet as pq
        from probe.sdk import inputs
        paths = []
        for i in range(3):
            p = os.path.join({str(tmp_path)!r}, f"t{{i}}.parquet")
            pq.write_table(pa.table({{"x": [i]}}), p)
            paths.append(p)
        assert inputs.start("run-pool")
        with mp.get_context("fork").Pool(2) as pool:
            print([m.num_rows for m in pool.map(pq.read_metadata, paths)])
        """
    )
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(sys.path), "XDG_STATE_HOME": str(tmp_path / "state")}
    out = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr[-2000:]
    assert out.stdout.strip().splitlines()[-1] == "[1, 1, 1]"


# -- P2 4: PYTHONPATH as given ------------------------------------------------------


@pytest.mark.parametrize("given", [":/nonexistent", "/a::/b", None])
def test_binding_keeps_pythonpath_as_given_and_finish_restores_it(tmp_path, monkeypatch, given) -> None:
    """An EMPTY entry is the working folder: binding dropped it, so a worker
    importing from the working folder broke, and finish did not put it back."""
    if given is None:
        monkeypatch.delenv("PYTHONPATH", raising=False)
    else:
        monkeypatch.setenv("PYTHONPATH", given)
    assert inputs.start("run-pp") and inputs.bind_workers("run-pp")
    site, *rest = os.environ["PYTHONPATH"].split(os.pathsep)
    assert Path(site, "sitecustomize.py").exists()
    assert rest == (given.split(os.pathsep) if given else [])
    inputs.collect_all("run-pp", wait_s=1)
    assert os.environ.get("PYTHONPATH") == given


def test_a_worker_imports_from_the_working_folder_while_bound(tmp_path, monkeypatch) -> None:
    """The reviewer's repro: PYTHONPATH=":/x", a module in the working folder."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    (cwd / "localmod.py").write_text("VALUE = 'from cwd'\n")
    script = tmp_path / "elsewhere" / "runner.py"  # a script: sys.path[0] is ITS folder
    script.parent.mkdir()
    script.write_text("import localmod\nprint(localmod.VALUE)\n")
    monkeypatch.setenv("PYTHONPATH", ":/nonexistent")
    assert inputs.start("run-cwd") and inputs.bind_workers("run-cwd")
    out = subprocess.run([sys.executable, str(script)], cwd=cwd, capture_output=True, text=True)
    assert out.stdout.strip() == "from cwd", out.stderr[-500:]
    inputs.abandon("run-cwd")


def test_a_pythonpath_changed_while_bound_loses_only_the_hook_folder(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("PYTHONPATH", ":/x")
    assert inputs.start("run-pp2") and inputs.bind_workers("run-pp2")
    os.environ["PYTHONPATH"] += os.pathsep + "/added"
    inputs.collect_all("run-pp2", wait_s=1)
    assert os.environ["PYTHONPATH"] == ":/x:/added"


def test_an_exec_child_keeps_empty_pythonpath_entries() -> None:
    env = {**os.environ, "PYTHONPATH": ":/x"}
    assert inputs.prepare_child("run-exec-pp", env)
    assert env["PYTHONPATH"].split(os.pathsep)[1:] == ["", "/x"]


# -- P2 6: a forked child that follows nothing ---------------------------------------


def test_the_close_leaves_a_live_forked_childs_spool_when_nothing_was_bound(tmp_path) -> None:
    """A fork of a run that never bound its workers inherits the run and
    keeps recording it: the parent's close took (and deleted) that LIVE
    child's spool with no close marker to cut it, so what the child read
    later was lost. It is now left for the child to end."""
    first, later = _data(tmp_path, "child_first.bin"), _data(tmp_path, "child_later.bin")
    go, ready = tmp_path / "go", tmp_path / "ready"
    assert inputs.start("run-unbound-fork")  # no bind_workers
    pid = os.fork()
    if pid == 0:
        try:
            open(first, "rb").read()
            ready.write_text("x")
            deadline = time.monotonic() + 30
            while not go.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            open(later, "rb").read()
        finally:
            os._exit(0)
    try:
        deadline = time.monotonic() + 30
        while not ready.exists() and time.monotonic() < deadline:
            time.sleep(0.02)
        got = inputs.collect_all("run-unbound-fork", wait_s=5)
        inputs.discard("run-unbound-fork")
        assert got.inputs_coverage["pending_spools"] == 1, "the live child's spool is its own"
    finally:
        go.write_text("x")
        os.waitpid(pid, 0)
    assert _spooled("run-unbound-fork") == sorted([str(first), str(later)]), "nothing lost"


# -- P2 7: torch.save's wrapper, without torch -------------------------------------


_STUB = {
    "torch/__init__.py": "from .serialization import save\n",
    "torch/serialization.py": (
        "import os, subprocess\n"
        "def save(obj, f):\n"
        "    # As the real one: the file is written where no audit event is raised.\n"
        "    subprocess.run(['sh', '-c', 'printf stub > \"$1\"', 'sh', os.fspath(f)], check=True)\n"
    ),
}


def test_torch_save_is_a_write_through_a_stub_torch(tmp_path) -> None:
    """CI has no torch: a stub `torch` whose `save` writes from outside
    Python proves the wrapper, its identity at both names, and pickling."""
    stub = tmp_path / "stub"
    for rel, text in _STUB.items():
        (stub / rel).parent.mkdir(parents=True, exist_ok=True)
        (stub / rel).write_text(text)
    ckpt, pooled = tmp_path / "work" / "ckpt.pt", tmp_path / "work" / "pooled.pt"
    ckpt.parent.mkdir(parents=True)
    code = textwrap.dedent(
        f"""
        import hashlib, json, multiprocessing as mp, pickle
        from concurrent.futures import ProcessPoolExecutor
        from probe.sdk import inputs
        assert inputs.start("run-stub")
        import torch, torch.serialization
        assert torch.save is torch.serialization.save
        assert pickle.loads(pickle.dumps(torch.save)) is torch.save
        torch.save({{}}, {str(ckpt)!r})
        with ProcessPoolExecutor(1, mp_context=mp.get_context("fork")) as ex:
            ex.submit(torch.save, {{}}, {str(pooled)!r}).result()
        got = inputs.collect_all("run-stub", wait_s=5)
        print(json.dumps({{r["path"]: r["content_hash"] for r in got.outputs}}))
        """
    )
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(stub), *sys.path]),
           "XDG_STATE_HOME": str(tmp_path / "state"), inputs.READS_ENV: "1"}
    out = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr[-2000:]
    import hashlib

    written = json.loads(out.stdout.strip().splitlines()[-1])
    assert written[str(ckpt)] == hashlib.sha256(b"stub").hexdigest()
    assert pooled.read_bytes() == b"stub"


# -- P2 8: a folder link retargeted ---------------------------------------------------


def test_a_retargeted_folder_link_is_resolved_again(tmp_path, monkeypatch) -> None:
    """The folder resolution cache outlived a link's retarget: a folder link
    first to outputs, then into a cache, kept recording downloads."""
    outputs, cache = tmp_path / "outputs", tmp_path / "xdg-cache" / "hub"
    outputs.mkdir()
    cache.mkdir(parents=True)
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "xdg-cache"))
    link = tmp_path / "work" / "models"
    link.parent.mkdir()
    link.symlink_to(outputs)
    inputs._real_dirs.clear()
    assert inputs.start("run-relink")
    (link / "first.bin").write_bytes(b"1" * 10)
    tmp = tmp_path / "work" / "models.tmp"
    tmp.symlink_to(cache)
    os.replace(tmp, link)  # retargeted
    (link / "second.bin").write_bytes(b"2" * 10)
    noted = sorted(inputs._active["run-relink"].written)
    inputs.abandon("run-relink")
    assert noted == [str(link / "first.bin")], "the write through the retargeted link is a download"


def test_the_child_hook_resolves_a_retargeted_folder_link_again(tmp_path) -> None:
    outputs, cache = tmp_path / "outputs", tmp_path / "xdg-cache" / "hub"
    outputs.mkdir()
    cache.mkdir(parents=True)
    link = tmp_path / "work" / "models"
    link.parent.mkdir()
    link.symlink_to(outputs)
    env = {**os.environ, "XDG_CACHE_HOME": str(tmp_path / "xdg-cache")}
    assert inputs.prepare_child("run-child-relink", env)
    code = (
        "import os\n"
        f"open({str(link / 'first.bin')!r}, 'wb').write(b'1')\n"
        f"os.symlink({str(cache)!r}, {str(link) + '.tmp'!r}); os.replace({str(link) + '.tmp'!r}, {str(link)!r})\n"
        f"open({str(link / 'second.bin')!r}, 'wb').write(b'2')\n"
    )
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    noted = [json.loads(line)["w"] for spool in inputs.run_dir("run-child-relink").glob("*.jsonl")
             for line in spool.read_text().splitlines() if line.startswith('{"w"')]
    assert noted == [str(link / "first.bin")], "the write through the retargeted link is a download"


# -- P3 9: safetensors.safe_open stays a class -----------------------------------------


def test_safe_open_is_still_a_class_after_the_patch(tmp_path) -> None:
    np = pytest.importorskip("numpy")
    safetensors = pytest.importorskip("safetensors", reason="safetensors is not installed")
    st_numpy = pytest.importorskip("safetensors.numpy")
    from safetensors import _safetensors_rust as rust

    path = tmp_path / "w.safetensors"
    st_numpy.save_file({"w": np.arange(2, dtype="float32")}, str(path))
    assert inputs.start("run-class")
    try:
        real = safetensors.safe_open.__wrapped__  # the Rust type
        # `_safetensors_rust.safe_open` names `builtins` as its module: it is
        # the stand-in too when safetensors was imported before the recorder.
        assert rust.safe_open in (real, safetensors.safe_open)
        assert isinstance(real, type) and isinstance(safetensors.safe_open, type)
        with safetensors.safe_open(str(path), framework="np") as handle:
            assert type(handle) is real
            assert isinstance(handle, safetensors.safe_open) and isinstance(handle, rust.safe_open)
        assert pickle.loads(pickle.dumps(safetensors.safe_open)) is safetensors.safe_open
        assert safetensors.safe_open is sys.modules["safetensors.numpy"].safe_open
    finally:
        inputs.abandon("run-class")


# -- P3 10: a worker that joins the run itself ----------------------------------------


def test_a_bound_worker_that_joins_the_run_keeps_its_spool(tmp_path) -> None:
    """A spawned worker read a file through its bound hook, then opened the
    SAME run itself (a rank): its spool kept the owner's header, so the
    owner's close took and cut a live rank's spool. Each open now writes a
    header, and the last one says whose it is."""
    before, after = _data(tmp_path, "before_init.bin"), _data(tmp_path, "after_init.bin")
    ready, go = tmp_path / "ready", tmp_path / "go"
    assert inputs.start("run-rank") and inputs.bind_workers("run-rank")
    code = textwrap.dedent(
        f"""
        import os, time
        open({str(before)!r}, "rb").read()
        from probe.sdk import inputs
        assert inputs.start("run-rank")
        open({str(after)!r}, "rb").read()
        open({str(ready)!r}, "w").write("x")
        while not os.path.exists({str(go)!r}):
            time.sleep(0.02)
        """
    )
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([os.environ["PYTHONPATH"], *sys.path])}
    proc = subprocess.Popen([sys.executable, "-c", code], env=env)
    try:
        deadline = time.monotonic() + 60
        while not ready.exists() and time.monotonic() < deadline:
            time.sleep(0.02)
        assert ready.exists()
        got = inputs.collect_all("run-rank", wait_s=5)
        inputs.discard("run-rank")
        assert got.inputs == [], "the rank's reads are the rank's to send"
        assert got.inputs_coverage["pending_spools"] == 1
    finally:
        go.write_text("x")
        proc.wait(30)
    assert sorted(_spooled("run-rank")) == sorted([str(before), str(after)])


# -- P3 11: no listing while nothing records --------------------------------------------


def test_a_dataset_read_lists_nothing_while_nothing_records(tmp_path) -> None:
    pa = pytest.importorskip("pyarrow", reason="pyarrow is not installed")
    pq = pytest.importorskip("pyarrow.parquet", reason="pyarrow is not installed")
    root = tmp_path / "ds"
    root.mkdir()
    pq.write_table(pa.table({"x": [1]}), root / "p.parquet")
    assert inputs.start("run-idle")  # installs the wrappers
    inputs.abandon("run-idle")
    listed: list[int] = []

    class Counting:
        def __init__(self, real) -> None:
            self._real = real

        def get_fragments(self, *a, **k):
            listed.append(1)
            return self._real.get_fragments(*a, **k)

        def __getattr__(self, name):
            return getattr(self._real, name)

    dataset = pq.ParquetDataset(root)
    dataset._dataset = Counting(dataset._dataset)
    dataset.read()
    assert listed == [], "nothing records: no listing"
    assert inputs.start("run-busy")
    dataset.read()
    assert listed == [1]
    inputs.abandon("run-busy")


def test_finish_restores_pythonpath_exactly_even_what_binding_left_out(tmp_path, monkeypatch) -> None:
    """Binding leaves out every Probe hook folder already on PYTHONPATH (one
    hook per process); if nobody changed PYTHONPATH since, finish puts back
    exactly what was there, that folder included."""
    outer = str(tmp_path / "state" / "probe" / "reads" / "outer-run" / "site")
    given = os.pathsep.join([outer, "", "/x"])
    monkeypatch.setenv("PYTHONPATH", given)
    assert inputs.start("run-exact") and inputs.bind_workers("run-exact")
    assert outer not in os.environ["PYTHONPATH"].split(os.pathsep)
    inputs.collect_all("run-exact", wait_s=1)
    assert os.environ["PYTHONPATH"] == given


# -- last round (review of 1dbc494c2) ----------------------------------------------


def _posix_flock():
    """What an NFS client does with flock (flock(2), NOTES): a whole-file
    POSIX lock -- never in conflict with the same process's own, and
    dropped by closing ANY handle this process has on the file."""
    import fcntl
    import types

    return types.SimpleNamespace(LOCK_EX=fcntl.LOCK_EX, LOCK_SH=fcntl.LOCK_SH, LOCK_NB=fcntl.LOCK_NB,
                                 LOCK_UN=fcntl.LOCK_UN, flock=lambda fd, op: fcntl.lockf(fd, op))


def _held_elsewhere(lock: str) -> bool:
    """Whether ANOTHER process is refused a shared POSIX lock on ``lock``."""
    code = (
        "import fcntl, os, sys\n"
        f"fd = os.open({lock!r}, os.O_RDONLY)\n"
        "try:\n    fcntl.lockf(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)\nexcept OSError:\n    sys.exit(3)\n"
    )
    return subprocess.run([sys.executable, "-c", code]).returncode == 3


def test_an_nfs_owner_never_probes_its_own_lock(tmp_path, monkeypatch) -> None:
    """P2: on NFS the owner's own recovery sweep opened its `.lock`, took a
    shared lock (no conflict with its own), closed it -- dropping its own
    lock -- judged itself dead and deleted its binding: spawned workers'
    reads were never recorded on an NFS home."""
    monkeypatch.setattr(inputs, "_fcntl", _posix_flock())
    inputs._reset_owner_identity()
    try:
        assert inputs.start("run-nfs") and inputs.bind_workers("run-nfs")
        binding, lock = inputs._bound["file"], inputs._bound["lock"]
        assert _held_elsewhere(lock)
        dead = Path(lock).with_name(f"{inputs._host()}.{_dead_pid()}.feedfacefeedface.lock")
        dead.write_text("")
        dead.with_suffix(".json").write_text("{}")
        inputs._clear_dead_bindings()  # what this process's own recovery runs
        assert Path(binding).exists() and Path(lock).exists()
        assert _held_elsewhere(lock), "the owner still holds its lock"
        assert not dead.exists() and not dead.with_suffix(".json").exists(), "a dead owner's go"
    finally:
        inputs.abandon("run-nfs")
        inputs._reset_owner_identity()


def _dead_pid() -> int:
    return int(subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                              capture_output=True, text=True, check=True).stdout)


def test_a_forked_follower_asks_whether_its_owner_lives_about_once_a_second(tmp_path, monkeypatch) -> None:
    """P3: every 0.25 s binding look also locked the owner's file; on NFS
    with 128 workers a node that is ~500 lock calls/s. The binding is still
    looked at every 0.25 s; the owner's liveness about once a second."""
    assert inputs.start("run-cadence") and inputs.bind_workers("run-cadence")
    follow = {"file": inputs._bound["file"], "lock": inputs._bound["lock"], "run": "run-cadence",
              "owner": os.getpid(), "next": 0.0, "sig": None, "dead": False, "alive_next": 0.0}
    looks: list[int] = []
    alive: list[int] = []
    real_stat = os.stat

    def counted_stat(p, *a, **k):
        if os.fspath(p) == follow["file"]:
            looks.append(1)
        return real_stat(p, *a, **k)

    with monkeypatch.context() as patched:
        patched.setattr(inputs, "_owner_alive", lambda *a: alive.append(1) or True)
        patched.setattr(inputs, "_follow", follow)
        patched.setattr(os, "stat", counted_stat)
        stop = time.monotonic() + 1.4
        while time.monotonic() < stop:
            inputs._follow_binding()
            time.sleep(0.01)
    assert len(looks) >= 5, looks
    assert 1 <= len(alive) <= 2, alive
    inputs.abandon("run-cadence")


def test_a_spawned_worker_asks_whether_its_owner_lives_about_once_a_second(tmp_path) -> None:
    data = _data(tmp_path, "busy.bin")
    assert inputs.start("run-cadence-child") and inputs.bind_workers("run-cadence-child")
    code = textwrap.dedent(
        f"""
        import fcntl, time
        calls = []
        real = fcntl.flock
        fcntl.flock = lambda fd, op: (calls.append(op), real(fd, op))[1]
        stop = time.monotonic() + 1.4
        while time.monotonic() < stop:
            open({str(data)!r}, "rb").read()
            time.sleep(0.01)
        print(sum(1 for op in calls if op & fcntl.LOCK_SH))
        """
    )
    out = subprocess.run([sys.executable, "-c", code], env=dict(os.environ), capture_output=True, text=True,
                         check=True)
    assert 1 <= int(out.stdout.strip()) <= 2, out.stdout
    inputs.abandon("run-cadence-child")


def test_an_offline_list_without_coverage_is_not_taken_for_a_late_hash() -> None:
    """P3: "no coverage" marked a late re-send, so a caller's own
    `record_run_inputs(..., coverage=None)` queued offline was dropped at
    sync. A late re-send is tagged in the queue instead."""
    from probe.sdk import offline

    class _NoObservations:
        @staticmethod
        def supports_feature(name: str) -> bool:
            return name == "run_inputs"

    class _Journal:
        dir = "/nowhere"

    row = {"path": "/d/x", "stable": True, "first_seen_at": "2026-09-28T00:00:00+00:00", "observation_id": "a" * 32}
    mine = {"kind": "http", "method": "POST", "path": "/v1/runs/local:k/inputs", "body": {"inputs": [dict(row)]}}
    late = {**mine, "body": {"inputs": [dict(row)]}, "tag": inputs.LATE_TAG}
    assert offline.lineage_gate(_Journal(), _NoObservations(), mine) is False
    assert "observation_id" not in mine["body"]["inputs"][0], "sent, without the id"
    assert offline.lineage_gate(_Journal(), _NoObservations(), late) is True, "dropped"
    offline._take_gated("/nowhere")


def test_a_run_handle_nobody_closed_stops_counting_once_it_is_collected(tmp_path, monkeypatch) -> None:
    """P3: a handle never finished (dropped, or from an init that failed
    after it was made) kept every worker binding off for good."""
    import gc
    import queue as _queue

    from probe.sdk import _open_runs

    class Handle:
        id = "run-dropped"

    monkeypatch.setattr(inputs, "TAIL_S", 0.05)
    monkeypatch.setattr(inputs, "_hash_queue", _queue.Queue())
    assert inputs.start("run-kept") and inputs.bind_workers("run-kept")
    handle = Handle()
    _open_runs.opened(handle)
    assert inputs._bound is None, "two runs open"
    loop = threading.Thread(target=inputs._hash_loop, daemon=True)
    loop.start()
    del handle
    gc.collect()
    deadline = time.monotonic() + 5
    while inputs._bound is None and time.monotonic() < deadline:
        time.sleep(0.02)
    for _ in range(2):
        inputs._hash_queue.put(None)
    loop.join(5)
    assert inputs._bound is not None and inputs._bound["run"] == "run-kept"
    inputs.abandon("run-kept")


@pytest.mark.skipif(not os.path.isdir("/proc/self/fd"), reason="needs /proc/self/fd to list a child's fds")
def test_a_fork_while_the_owner_lock_opens_never_leaks_its_fd(tmp_path, monkeypatch) -> None:
    """P3: a fork from another thread between opening the owner's lock and
    publishing it left the child holding the fd without knowing -- and a
    child holding it keeps the lock taken after the owner died."""
    assert inputs.start("run-fork-race")  # installs the fork handlers
    inputs._reset_owner_identity()
    opened, real_open = threading.Event(), os.open

    def slow_open(path, *a, **k):
        fd = real_open(path, *a, **k)
        if str(path).endswith(".lock"):
            opened.set()
            time.sleep(0.5)  # the window between the open and `_owner`
        return fd

    with monkeypatch.context() as patched:
        patched.setattr(os, "open", slow_open)
        maker = threading.Thread(target=inputs._owner_identity)
        maker.start()
        assert opened.wait(5)
        pid = os.fork()
        if pid == 0:
            leaked = any(os.readlink(f"/proc/self/fd/{fd}").endswith(".lock")
                         for fd in os.listdir("/proc/self/fd") if os.path.exists(f"/proc/self/fd/{fd}"))
            os._exit(4 if leaked else 0)
        _, status = os.waitpid(pid, 0)
        maker.join(5)
    try:
        assert os.waitstatus_to_exitcode(status) == 0, "the child holds the owner's lock fd"
    finally:
        inputs.abandon("run-fork-race")
        inputs._reset_owner_identity()


def test_the_hasher_marks_done_on_the_queue_it_took_the_item_from(tmp_path, monkeypatch) -> None:
    """The full suite's one red (test_probe_exec_sends_what_its_python_child
    _read, unhashed): the hasher looked the queue up again for `task_done`.
    With the queue swapped in between (a test's monkeypatch, a fork), it
    marked the wrong one -- ValueError, the hasher died -- and left the item it
    took counted unfinished: every later close in the process then waited its
    whole wait on that count and hashed nothing."""
    import queue as _queue

    assert inputs.start("run-queue")  # the process's hasher, waiting on the queue
    real = inputs._hash_queue
    hasher = inputs._hasher
    deadline = time.monotonic() + 5
    while real.unfinished_tasks and time.monotonic() < deadline:
        time.sleep(0.01)
    with monkeypatch.context() as patched:
        patched.setattr(inputs, "_hash_queue", _queue.Queue())
        real.put(("no-such-run", "/nowhere", (0, 0, 0, 0, 0)))  # the item it is waiting for
        deadline = time.monotonic() + 5
        while real.unfinished_tasks and time.monotonic() < deadline:
            time.sleep(0.01)
    assert real.unfinished_tasks == 0, "the item stays counted unfinished"
    assert hasher.is_alive(), "the hasher died"
    inputs.abandon("run-queue")
