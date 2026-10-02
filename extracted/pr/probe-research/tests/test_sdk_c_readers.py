"""Readers that open files from C, told to the read recorder (lineage plan 3, F4).

Python's ``open`` audit event never fires for a library that opens its files
from C or Rust. `probe.sdk._readers` wraps the Python entry points of the ones
that matter -- pyarrow.parquet, pyarrow.memory_map, h5py, safetensors -- and
``torch.save`` (a write), lazily, and hands each path to the recorder. These
tests pin that each wrapped reader records the files it OPENED (a dataset's
files when they are read, never at construction), that h5py's mode says read
or write, that ``torch.load`` is seen with no wrapper at all, that the same
wrappers run in ``probe exec``'s child, and that Probe's own calls are not the
run's. A reader leaves ``inputs.UNSEEN_READERS`` only when a test here proves
it is seen.

The libraries are not in the ``dev`` extras (torch alone is ~700 MB): each
test skips, saying so, where one is not installed.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
import types
from pathlib import Path

import pytest

from probe.sdk import _readers, fluent, inputs


def _lib(name: str):
    return pytest.importorskip(name, reason=f"{name} is not installed (not in the dev extras)")


@pytest.fixture(autouse=True)
def _recorder(monkeypatch, tmp_path):
    """Read (and write) capture ON, its state under tmp, nothing left recording."""
    monkeypatch.setenv(inputs.READS_ENV, "1")
    for name in (inputs.CHILD_DIR_ENV, inputs.WRITES_ENV, inputs.OUTPUTS_ENV, "PROBE_RUN_ID"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    inputs._active.clear()
    inputs._hash_results.clear()
    fluent._current.set(None)
    fluent._process_default = None
    yield
    inputs._active.clear()


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _reads(run_id: str) -> dict[str, dict]:
    got = inputs.collect_all(run_id, wait_s=10)
    return {row["path"]: row for row in got.inputs}


def _parquet(path: Path, rows: int = 50) -> Path:
    pa = _lib("pyarrow")
    pq = _lib("pyarrow.parquet")
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(pa.table({"x": list(range(rows))}), path)
    return path


def _partitioned(root: Path) -> dict[int, list[Path]]:
    """A hive dataset: year=2020 and year=2021, two files each."""
    out: dict[int, list[Path]] = {}
    for year in (2020, 2021):
        out[year] = [_parquet(root / f"year={year}" / f"part-{i}.parquet", rows=10 + i) for i in range(2)]
    return out


# -- pyarrow ------------------------------------------------------------------------


def test_read_table_of_a_file_records_it(tmp_path) -> None:
    pq = _lib("pyarrow.parquet")
    data = _parquet(tmp_path / "work" / "train.parquet")
    assert inputs.start("run-pq-file")
    assert pq.read_table(data).num_rows == 50
    rows = _reads("run-pq-file")
    assert rows[str(data)]["content_hash"] == _sha(data)


def test_a_dataset_is_recorded_when_read_never_when_opened(tmp_path) -> None:
    """Opening a dataset is not consuming its files: construction records
    nothing, and a read records only the files it scans (after the partition
    filter) -- through ParquetDataset, which read_table builds."""
    pq = _lib("pyarrow.parquet")
    root = tmp_path / "work" / "ds"
    parts = _partitioned(root)
    assert inputs.start("run-pq-ds")
    dataset = pq.ParquetDataset(root, filters=[("year", "=", 2020)])
    assert inputs._active["run-pq-ds"].seen == {}, "construction reads nothing"
    assert dataset.read().num_rows == 21
    pq.read_table(root, filters=[("year", "=", 2020)])  # the same files, deduped
    rows = _reads("run-pq-ds")
    assert sorted(rows) == sorted(str(p) for p in parts[2020])
    assert all(rows[str(p)]["content_hash"] == _sha(p) for p in parts[2020])


def test_pandas_read_parquet_of_a_folder_is_recorded(tmp_path) -> None:
    pd = _lib("pandas")
    _lib("pyarrow.parquet")
    root = tmp_path / "work" / "pdds"
    parts = _partitioned(root)
    assert inputs.start("run-pd")
    assert len(pd.read_parquet(root)) == 42
    assert sorted(_reads("run-pd")) == sorted(str(p) for group in parts.values() for p in group)


def test_parquet_file_and_read_metadata_record_the_file(tmp_path) -> None:
    pq = _lib("pyarrow.parquet")
    one = _parquet(tmp_path / "work" / "one.parquet")
    two = _parquet(tmp_path / "work" / "two.parquet", rows=7)
    assert inputs.start("run-pqf")
    assert pq.ParquetFile(one).metadata.num_rows == 50
    assert pq.read_metadata(two).num_rows == 7  # opened: its footer is read
    three = _parquet(tmp_path / "work" / "three.parquet", rows=3)
    assert pq.read_schema(three).names == ["x"]
    assert sorted(_reads("run-pqf")) == sorted([str(one), str(two), str(three)])


#: A dataset made from a FILE OBJECT (pandas' `read_parquet(file)` opens the
#: file and hands pyarrow the handle): reading `_dataset.filesystem` on it
#: segfaults pyarrow, so the wrapper never touches it -- the audit hook saw
#: the `open`. Each call runs in its own process: a crash fails the test
#: instead of killing pytest. name -> (code, what it read: "file" or "dir").
#:
#: The file-object `read_table` calls pass `use_threads=False`: pyarrow's
#: THREADED scan of a Python file object races the interpreter's exit and
#: aborts the process ("terminate called without an active exception"), with
#: or without Probe -- measured on pyarrow 25.0.1, a script whose last call is
#: `pq.read_table(open(f))` aborted in 60-93% of runs on 3.10, 3.11 and 3.12
#: with no Probe at all (`pd.read_parquet(f)`: 3 of 200), and 0 of 200 with
#: `use_threads=False`. The dataset is still made from the file object, so
#: the wrapper under test is the same (the old one still segfaults here).
_PARQUET_CALLS = {
    "pd.read_parquet(file)": ("assert len(pd.read_parquet(FILE, use_threads=False)) == 50", "file"),
    "pd.read_parquet(dir)": ("assert len(pd.read_parquet(DIR)) == 42", "dir"),
    "pq.read_table(file)": ("assert pq.read_table(FILE).num_rows == 50", "file"),
    "pq.read_table(open(file))": (
        "with open(FILE, 'rb') as fh:\n    assert pq.read_table(fh, use_threads=False).num_rows == 50",
        "file",
    ),
    "pq.ParquetDataset(dir).read()": ("assert pq.ParquetDataset(DIR).read().num_rows == 42", "dir"),
    "pq.ParquetFile(open(file))": (
        "with open(FILE, 'rb') as fh:\n    assert pq.ParquetFile(fh).read().num_rows == 50",
        "file",
    ),
}


def _parquet_call_code(call: str, file: Path, root: Path, run_id: str | None) -> str:
    """``call`` with pyarrow (and pandas, when it uses it) imported first (a
    script's imports run before ``probe.init()``), recording into ``run_id``
    -- or, None, into whatever run the process's hook records (a ``probe
    exec`` child)."""
    head = [
        "import faulthandler, json",
        "faulthandler.enable()",
        "import pyarrow.parquet as pq",
        *(["import pandas as pd"] if "pd." in call else []),
        f"FILE, DIR = {str(file)!r}, {str(root)!r}",
    ]
    if run_id is None:
        return "\n".join([*head, call, "print('ok')"]) + "\n"
    return "\n".join([
        *head,
        "from probe.sdk import inputs",
        f"assert inputs.start({run_id!r})",
        call,
        f"got = inputs.collect_all({run_id!r}, wait_s=10)",
        "print(json.dumps(sorted(r['path'] for r in got.inputs)))",
    ]) + "\n"


@pytest.mark.parametrize("name", list(_PARQUET_CALLS))
def test_a_parquet_read_never_crashes_and_records_what_it_opened(tmp_path, name) -> None:
    if name.startswith("pd."):
        _lib("pandas")
    _lib("pyarrow.parquet")
    file = _parquet(tmp_path / "work" / "one.parquet")
    root = tmp_path / "work" / "ds"
    parts = _partitioned(root)
    call, read = _PARQUET_CALLS[name]
    env = {**os.environ, "XDG_STATE_HOME": str(tmp_path / "state"),
           "PROBE_OUTBOX_DIR": str(tmp_path / "outbox"), inputs.READS_ENV: "1"}
    for variable in (inputs.CHILD_DIR_ENV, inputs.OWNER_PID_ENV, inputs.BIND_ENV):
        env.pop(variable, None)
    code = _parquet_call_code(call, file, root, "run-pq-call")
    out = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, f"{name} exited {out.returncode}:\n{out.stderr[-3000:]}"
    expected = [str(file)] if read == "file" else sorted(str(p) for group in parts.values() for p in group)
    assert json.loads(out.stdout.strip().splitlines()[-1]) == expected


def test_parquet_reads_in_an_exec_child_never_crash_and_are_recorded(tmp_path) -> None:
    """The child hook (`probe exec`, spawned workers) runs the same wrappers."""
    _lib("pyarrow.parquet")
    with_pandas = importlib.util.find_spec("pandas") is not None  # else the pyarrow calls alone
    calls = [call for name, (call, _) in _PARQUET_CALLS.items() if with_pandas or not name.startswith("pd.")]
    file = _parquet(tmp_path / "work" / "one.parquet")
    root = tmp_path / "work" / "ds"
    parts = _partitioned(root)
    env = {**os.environ}
    assert inputs.prepare_child("run-pq-child", env)
    code = _parquet_call_code("\n".join(calls), file, root, None)
    out = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, f"exited {out.returncode}:\n{out.stderr[-3000:]}"
    got = inputs.collect_all("run-pq-child", wait_s=10)
    assert sorted(r["path"] for r in got.inputs) == sorted(
        [str(file), *(str(p) for group in parts.values() for p in group)]
    )


def test_a_dataset_is_listed_only_when_made_from_local_paths() -> None:
    """What the wrapped `ParquetDataset.__init__` decides from its arguments
    alone: a file object, a buffer, a URI or another filesystem is not listed
    at `read()` (the native dataset is never asked)."""
    import io

    class Remote:  # a filesystem that is not this machine's disk
        pass

    class Local:
        pass

    Local.__name__ = "LocalFileSystem"
    local = [("/data/x.parquet", None), (Path("/data/ds"), None), (["/a.parquet", Path("/b.parquet")], None),
             ("/data/x.parquet", Local())]
    not_local = [(io.BytesIO(b"PAR1"), None), (b"/data/x.parquet", None), ("s3://bucket/x.parquet", None),
                 ("/data/x.parquet", Remote()), ([], None), (["/a.parquet", io.BytesIO()], None), (None, None)]
    for source, filesystem in local:
        assert _readers._local_fs(filesystem) and _readers._local_paths(source), source
    for source, filesystem in not_local:
        assert not (_readers._local_fs(filesystem) and _readers._local_paths(source)), source


def test_a_pyarrow_dataset_read_directly_is_named_unseen(tmp_path) -> None:
    """`pyarrow.dataset` types are immutable C++ wrappers: a Dataset's own
    scan cannot be seen without a proxy that would break isinstance. Nothing
    is recorded at construction (or guessed), and the coverage says so."""
    ds = _lib("pyarrow.dataset")
    root = tmp_path / "work" / "direct"
    _partitioned(root)
    assert inputs.start("run-ds-direct")
    assert ds.dataset(root, partitioning="hive").to_table().num_rows == 42
    got = inputs.collect_all("run-ds-direct", wait_s=5)
    assert got.inputs == []
    assert any("pyarrow.dataset" in reader for reader in got.inputs_coverage["unseen"])


def test_a_dataset_past_the_cap_says_it_was_cut(tmp_path, monkeypatch) -> None:
    pq = _lib("pyarrow.parquet")
    root = tmp_path / "work" / "many"
    for i in range(3):
        _parquet(root / f"p{i}.parquet", rows=5)
    monkeypatch.setattr(_readers, "MAX_DATASET_FILES", 2)
    assert inputs.start("run-ds-cap")
    pq.read_table(root)
    got = inputs.collect_all("run-ds-cap", wait_s=5)
    assert len(got.inputs) == 2 and got.inputs_coverage["truncated"] is True


def test_memory_map_reads_and_writes_by_mode(tmp_path) -> None:
    """The Hugging Face `datasets` cache is read through `pa.memory_map`."""
    pa = _lib("pyarrow")
    cache = tmp_path / "work" / "data-00000.arrow"
    cache.parent.mkdir(parents=True)
    cache.write_bytes(b"a" * 4096)
    scratch = tmp_path / "work" / "scratch.bin"
    scratch.write_bytes(b"s" * 4096)
    # Made a while ago, as a file mapped for writing usually is: a change in
    # the same clock tick as its creation would leave its identity as it was.
    os.utime(scratch, (time.time() - 60, time.time() - 60))
    assert inputs.start("run-mmap")
    with pa.memory_map(str(cache)) as source:
        assert source.read(4) == b"aaaa"
    with pa.memory_map(str(scratch), "r+") as sink:
        sink.write(b"XY")
    got = inputs.collect_all("run-mmap", wait_s=5)
    assert [r["path"] for r in got.inputs] == [str(cache)]
    assert [(r["path"], r["content_hash"]) for r in got.outputs] == [(str(scratch), _sha(scratch))]


# -- h5py ---------------------------------------------------------------------------


@pytest.mark.parametrize("mode", ["w", "w-", "x", "a", "r+"])
def test_h5py_write_modes_are_writes(tmp_path, mode) -> None:
    h5py = _lib("h5py")
    np = _lib("numpy")
    path = tmp_path / "work" / f"out-{mode}.h5"
    path.parent.mkdir(parents=True)
    if mode in ("a", "r+"):
        with h5py.File(path, "w") as handle:
            handle["seed"] = np.arange(3)
    assert inputs.start(f"run-h5-{mode}")
    with h5py.File(path, mode) as handle:
        handle["x"] = np.arange(10)
    got = inputs.collect_all(f"run-h5-{mode}", wait_s=5)
    assert got.inputs == [], "a write mode is not a read"
    assert [(r["path"], r["content_hash"]) for r in got.outputs] == [(str(path), _sha(path))]


def test_h5py_read_mode_is_a_read(tmp_path) -> None:
    h5py = _lib("h5py")
    np = _lib("numpy")
    path = tmp_path / "work" / "features.h5"
    path.parent.mkdir(parents=True)
    with h5py.File(path, "w") as handle:
        handle["x"] = np.arange(10)
    assert inputs.start("run-h5-r")
    with h5py.File(path) as handle:  # the default mode, "r"
        assert list(handle["x"][:3]) == [0, 1, 2]
    with h5py.File(str(path), mode="r") as handle:
        handle["x"][:]
    got = inputs.collect_all("run-h5-r", wait_s=5)
    assert [(r["path"], r["content_hash"]) for r in got.inputs] == [(str(path), _sha(path))]
    assert got.outputs == []


def test_h5py_writes_follow_the_switches(tmp_path) -> None:
    h5py = _lib("h5py")
    np = _lib("numpy")
    path = tmp_path / "work" / "quiet.h5"
    path.parent.mkdir(parents=True)
    assert inputs.start("run-h5-quiet", capture_outputs=False)
    with h5py.File(path, "w") as handle:
        handle["x"] = np.arange(3)
    assert inputs._active["run-h5-quiet"].written == {}
    inputs.abandon("run-h5-quiet")


# -- safetensors --------------------------------------------------------------------


def test_safetensors_reads_are_recorded(tmp_path) -> None:
    np = _lib("numpy")
    st_numpy = _lib("safetensors.numpy")
    safetensors = _lib("safetensors")
    one = tmp_path / "work" / "model-1.safetensors"
    two = tmp_path / "work" / "model-2.safetensors"
    one.parent.mkdir(parents=True)
    st_numpy.save_file({"w": np.arange(8, dtype="float32")}, str(one))
    st_numpy.save_file({"w": np.arange(9, dtype="float32")}, str(two))
    assert inputs.start("run-st")
    with safetensors.safe_open(str(one), framework="np") as handle:
        assert list(handle.keys()) == ["w"]
    assert st_numpy.load_file(two)["w"].shape == (9,)
    rows = _reads("run-st")
    assert sorted(rows) == sorted([str(one), str(two)])
    assert rows[str(one)]["content_hash"] == _sha(one)


def test_safetensors_torch_load_file_is_recorded(tmp_path) -> None:
    torch = _lib("torch")
    st_torch = _lib("safetensors.torch")
    path = tmp_path / "work" / "adapter.safetensors"
    path.parent.mkdir(parents=True)
    st_torch.save_file({"w": torch.zeros(4)}, str(path))
    assert inputs.start("run-st-torch")
    assert st_torch.load_file(path)["w"].shape == (4,)
    assert list(_reads("run-st-torch")) == [str(path)]


# -- torch ----------------------------------------------------------------------------


def test_torch_save_is_a_write(tmp_path) -> None:
    """torch.save writes from C++ (PyTorchFileWriter): unseen by the hook."""
    torch = _lib("torch")
    path = tmp_path / "work" / "ckpt.pt"
    path.parent.mkdir(parents=True)
    assert inputs.start("run-torch-save")
    torch.save({"w": torch.ones(3)}, path)
    torch.save({"w": torch.ones(4)}, str(path))  # saved again: the final bytes count
    got = inputs.collect_all("run-torch-save", wait_s=5)
    assert [(r["path"], r["content_hash"]) for r in got.outputs] == [(str(path), _sha(path))]


def test_torch_load_is_seen_with_no_wrapper(tmp_path) -> None:
    """torch.load opens its file with Python's `open` (`_open_file`), so the
    audit hook sees it: nothing wraps it."""
    torch = _lib("torch")
    path = tmp_path / "work" / "weights.pt"
    path.parent.mkdir(parents=True)
    torch.save({"w": torch.ones(3)}, path)
    assert inputs.start("run-torch-load")
    assert not hasattr(torch.load, "__probe_wrapped_by__")
    assert torch.load(path)["w"].sum().item() == 3
    assert _reads("run-torch-load")[str(path)]["content_hash"] == _sha(path)


# -- the wrappers themselves --------------------------------------------------------


def test_note_read_records_like_an_open(tmp_path) -> None:
    data = tmp_path / "work" / "custom.bin"
    data.parent.mkdir(parents=True)
    data.write_bytes(b"c" * 100)
    secret = tmp_path / ".ssh" / "id_rsa"
    secret.parent.mkdir()
    secret.write_bytes(b"k")
    assert inputs.start("run-note")
    inputs.note_read(data)
    inputs.note_read(str(secret))  # the same exclusions as an open
    inputs.note_read(b"/no/such/file")
    inputs.note_read(object())  # not a path: nothing, no raise
    rows = _reads("run-note")
    assert list(rows) == [str(data)] and rows[str(data)]["content_hash"] == _sha(data)


def test_probes_own_calls_through_a_wrapper_are_not_the_runs(tmp_path) -> None:
    pq = _lib("pyarrow.parquet")
    data = _parquet(tmp_path / "work" / "probe_own.parquet")
    assert inputs.start("run-own")
    with inputs.internal():
        pq.read_table(data)
    own = types.ModuleType("probe.sdk.pretend")  # Probe code calling the reader
    exec("def read(pq, path):\n    return pq.read_table(path)\n", own.__dict__)
    own.read(pq, data)
    assert _reads("run-own") == {}


def test_a_wrapper_does_no_io_of_its_own(tmp_path, monkeypatch) -> None:
    """With no run recording a wrapped call costs a function call; with one,
    exactly the one stat the recorder spends on any read."""
    pq = _lib("pyarrow.parquet")
    data = _parquet(tmp_path / "work" / "io.parquet")
    assert inputs.start("run-io")
    inputs.abandon("run-io")
    import threading

    caller = threading.get_ident()
    stats: list[str] = []
    real = os.stat

    def counted(p, *a, **k):
        if threading.get_ident() == caller:  # not the background hasher's
            stats.append(os.fspath(p))
        return real(p, *a, **k)

    monkeypatch.setattr(os, "stat", counted)
    pq.ParquetFile(data)
    assert stats == [], "no run: nothing looked at"
    assert inputs.start("run-io-2")
    pq.ParquetFile(data)
    state = str(tmp_path / "state")
    assert [p for p in stats if not p.startswith(state)] == [str(data)], "one stat, the recorder's own"
    inputs.abandon("run-io-2")


def test_the_wrappers_install_only_when_the_library_is_imported(tmp_path) -> None:
    """Lazy: starting the recorder imports none of them; one imported later
    is patched as it is imported."""
    _lib("h5py")
    code = (
        "import sys\n"
        "from probe.sdk import inputs\n"
        "assert inputs.start('run-lazy')\n"
        "heavy = ('pyarrow', 'h5py', 'safetensors', 'torch')\n"
        "assert not [m for m in heavy if m in sys.modules], [m for m in heavy if m in sys.modules]\n"
        "import h5py\n"
        "print(hasattr(h5py.File.__init__, '__probe_wrapped_by__'))\n"
    )
    env = {**os.environ, "XDG_STATE_HOME": str(tmp_path / "state"), inputs.READS_ENV: "1"}
    env.pop(inputs.CHILD_DIR_ENV, None)
    out = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "True"


def test_a_reader_imported_by_name_before_init_is_seen(tmp_path) -> None:
    """transformers binds `safe_open` (and `load_file as safe_load_file`) by
    name when it is imported -- usually before `probe.init()`. Install points
    every module global that IS a patched function at its wrapper, once."""
    _lib("safetensors.numpy")
    weights = tmp_path / "work" / "early.safetensors"
    weights.parent.mkdir(parents=True)
    code = (
        "import json, sys, types\n"
        "import numpy as np\n"
        "from safetensors.numpy import save_file, load_file as early_load\n"
        "from safetensors import safe_open as early_open\n"
        f"save_file({{'w': np.arange(3, dtype='float32')}}, {str(weights)!r})\n"
        "user = types.ModuleType('early_user')\n"
        "user.safe_open, user.safe_load_file = early_open, early_load\n"
        "sys.modules['early_user'] = user\n"
        "from probe.sdk import inputs\n"
        "assert inputs.start('run-early')\n"
        f"user.safe_open({str(weights)!r}, framework='np').keys()\n"
        "got = inputs.collect_all('run-early', wait_s=5)\n"
        "print(json.dumps({'reads': [r['path'] for r in got.inputs],\n"
        "                  'load_file': hasattr(user.safe_load_file, '__probe_wrapped_by__')}))\n"
    )
    env = {**os.environ, "XDG_STATE_HOME": str(tmp_path / "state"), inputs.READS_ENV: "1"}
    env.pop(inputs.CHILD_DIR_ENV, None)
    out = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert json.loads(out.stdout.strip().splitlines()[-1]) == {"reads": [str(weights)], "load_file": True}


# -- probe exec's child -------------------------------------------------------------


def test_an_exec_child_records_c_readers_and_torch_save(tmp_path) -> None:
    """The child hook runs the same wrappers (`_readers`' source, exec'd)."""
    pq = _lib("pyarrow.parquet")
    h5py = _lib("h5py")
    np = _lib("numpy")
    _lib("torch")
    st_numpy = _lib("safetensors.numpy")
    table = _parquet(tmp_path / "work" / "child.parquet")
    h5 = tmp_path / "work" / "child.h5"
    with h5py.File(h5, "w") as handle:
        handle["x"] = np.arange(4)
    weights = tmp_path / "work" / "child.safetensors"
    st_numpy.save_file({"w": np.arange(2, dtype="float32")}, str(weights))
    ckpt = tmp_path / "work" / "child_ckpt.pt"
    assert pq  # imported here for the fixture only
    env = {**os.environ}
    assert inputs.prepare_child("run-child-c", env)
    code = (
        "import pyarrow.parquet as pq, h5py, torch\n"
        "from safetensors import safe_open\n"
        f"pq.read_table({str(table)!r})\n"
        f"h5py.File({str(h5)!r}, 'r').close()\n"
        f"safe_open({str(weights)!r}, framework='np').keys()\n"
        f"torch.save({{'w': torch.ones(2)}}, {str(ckpt)!r})\n"
    )
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    got = inputs.collect_all("run-child-c", wait_s=10)
    assert sorted(r["path"] for r in got.inputs) == sorted(map(str, (table, h5, weights)))
    assert [(r["path"], r["content_hash"]) for r in got.outputs] == [(str(ckpt), _sha(ckpt))]


def test_readers_source_reaches_the_child_hook() -> None:
    assert "def install(note_read, note_write" in inputs.CHILD_SITE_CODE
    json.dumps(inputs.UNSEEN_READERS)  # plain strings, for the coverage record
