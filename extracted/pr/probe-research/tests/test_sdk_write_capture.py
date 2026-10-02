"""What a run WRITES (lineage plan 3, F2), and the hashes that let a read match it.

A read can only be matched to bytes the server knows. The SDK's audit hook now
notes every file the run opens for WRITING; at the close each one that still
exists and changed is hashed (final bytes) and sent to
``POST /v1/runs/{id}/outputs`` -- only to a server that declares
``run_outputs``. One I/O budget pays for reads first, then writes, then output
capture's references (F3), and no fingerprint is read past it. Output capture's
redacted uploads carry the ORIGINAL's hash from the same read (F1).
"""

from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import re
import subprocess
import sys
import time
import types
from pathlib import Path

import pytest

import probe
from probe.sdk import ephemeral, fluent, inputs, outputs
from tests.conftest import RUN_OUTPUT_KEYS, make_client, open_run, run_outputs_problems

TOKEN = "ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
OTHER_TOKEN = "ghp_Z9y8X7w6V5u4T3s2R1q0P9o8N7m6L5k4J3i2"


@pytest.fixture(autouse=True)
def _recorder(monkeypatch, tmp_path):
    """Read (and so write) capture ON, its state under tmp, nothing left recording."""
    monkeypatch.setenv(inputs.READS_ENV, "1")
    for name in (inputs.CHILD_DIR_ENV, inputs.WRITES_ENV, inputs.OUTPUTS_ENV, "PROBE_RUN_ID", "PROBE_RUN_EPOCH"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    inputs._active.clear()
    inputs._hash_results.clear()
    inputs._reference_budgets.clear()
    fluent._current.set(None)
    fluent._process_default = None
    yield
    inputs._active.clear()
    fluent._current.set(None)
    fluent._process_default = None


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file(tmp_path: Path, rel: str, data: bytes) -> Path:
    path = tmp_path / "work" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _outputs(got) -> dict[str, dict]:
    return {row["path"]: row for row in got.outputs}


class _Journal:
    def __init__(self) -> None:
        self.ops: list[tuple] = []

    def append_http(self, method, path, body, *, run_ref=None, blocking=True, **_):
        self.ops.append((method, path, body, run_ref, blocking))
        return "op"


class _Client:
    def __init__(self, *features: str) -> None:
        self.features = set(features)
        self.journal = _Journal()

    def supports_feature(self, name: str) -> bool:
        return name in self.features


# -- what counts as a write ------------------------------------------------------


def test_a_write_is_recorded_once_with_its_final_bytes(tmp_path) -> None:
    out = tmp_path / "work" / "metrics.json"
    out.parent.mkdir(parents=True)
    assert inputs.start("run-w")
    for i in range(5):  # opened for writing five times, rewritten each time
        with open(out, "w") as handle:
            handle.write(json.dumps({"step": i}))
    with open(out, "a") as handle:
        handle.write("\n")
    got = inputs.collect_all("run-w", wait_s=5)
    rows = _outputs(got)
    assert list(rows) == [str(out)]
    row = rows[str(out)]
    final = out.read_bytes()
    assert row["content_hash"] == _sha(final) and row["size_bytes"] == len(final)
    assert tuple(row) == RUN_OUTPUT_KEYS  # the contract's keys, in its order
    assert re.fullmatch(r"[0-9a-f]{32}", row["observation_id"])
    from datetime import datetime

    first, last = (datetime.fromisoformat(row[k]) for k in ("first_written_at", "last_modified_at"))
    # The mtime is stamped from the kernel's coarse clock: it may read a few
    # ms BEFORE the (fine-clock) moment the open was noted.
    assert (last - first).total_seconds() > -1
    spool = next(inputs.run_dir("run-w").glob("*.jsonl")).read_text().splitlines()
    assert json.loads(spool[0]) == {"run": "run-w", "owner": os.getpid(), "follows": False}, "the spool names its run"
    assert len(spool) == 2, "one note per path per process, however often it is opened"
    # A write is not a read.
    assert str(out) not in {r["path"] for r in got.inputs}
    assert got.outputs_coverage["count"] == 1 and got.outputs_coverage["gone"] == 0


def test_a_file_deleted_before_the_close_is_not_an_output(tmp_path) -> None:
    """The write-exists-at-finish rule: a temp file is not what the run left."""
    kept = tmp_path / "work" / "kept.bin"
    scratch = tmp_path / "work" / "scratch.tmp"
    kept.parent.mkdir(parents=True)
    assert inputs.start("run-tmp")
    kept.write_bytes(b"k" * 300)
    scratch.write_bytes(b"s" * 300)
    scratch.unlink()
    got = inputs.collect_all("run-tmp", wait_s=5)
    assert list(_outputs(got)) == [str(kept)]
    assert got.outputs_coverage["gone"] == 1 and got.outputs_coverage["unchecked"] == 0


def test_an_open_that_changed_nothing_is_not_an_output(tmp_path, monkeypatch) -> None:
    """An append that wrote nothing, or a read-only `r+`, leaves the file as
    it was before the open (P2 6: compared by identity, so a file created a
    moment before the run -- well inside any clock slack -- is still judged
    right), and is never hashed (P2 5: it cannot cost a real output its
    budget)."""
    appended = _file(tmp_path, "config.yaml", b"lr: 0.1\n")  # created just now
    mapped = _file(tmp_path, "dataset.npy", b"d" * 4096)
    written = tmp_path / "work" / "out.txt"
    assert inputs.start("run-noop")
    open(appended, "a").close()
    with open(mapped, "r+b") as handle:
        handle.read()
    written.write_text("result")
    hashed: list[str] = []
    real = inputs.hash_file
    monkeypatch.setattr(inputs, "hash_file", lambda path, *a, **k: hashed.append(path) or real(path, *a, **k))
    got = inputs.collect_all("run-noop", wait_s=5)
    assert list(_outputs(got)) == [str(written)]
    assert got.outputs_coverage["unchanged"] == 2
    assert hashed == [str(written)]


def test_a_failed_write_open_is_not_an_output(tmp_path, monkeypatch) -> None:
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        pytest.skip("root opens a read-only file for writing")
    locked = _file(tmp_path, "readonly.bin", b"r" * 100)
    locked.chmod(0o444)
    assert inputs.start("run-refused")
    with pytest.raises(PermissionError):
        open(locked, "w")
    got = inputs.collect_all("run-refused", wait_s=5)
    assert got.outputs == [] and got.outputs_coverage["unchanged"] == 1


def test_a_renamed_write_is_recorded_under_its_new_name(tmp_path) -> None:
    """Write to `x.tmp`, then `os.replace` onto `x`: the checkpoint pattern."""
    final = tmp_path / "work" / "ckpt.pt"
    staging = tmp_path / "work" / "ckpt.pt.tmp"
    final.parent.mkdir(parents=True)
    assert inputs.start("run-rename")
    staging.write_bytes(b"weights" * 50)
    os.replace(staging, final)
    got = inputs.collect_all("run-rename", wait_s=5)
    assert list(_outputs(got)) == [str(final)]
    assert _outputs(got)[str(final)]["content_hash"] == _sha(b"weights" * 50)
    assert got.outputs_coverage["gone"] == 1  # the staging name


def test_a_rename_of_a_file_the_run_did_not_write_is_nothing(tmp_path) -> None:
    before = _file(tmp_path, "theirs.bin", b"t" * 100)
    assert inputs.start("run-mv")
    os.rename(before, tmp_path / "work" / "moved.bin")
    assert inputs.collect_all("run-mv", wait_s=5).outputs == []


def test_what_is_never_an_output(tmp_path, monkeypatch) -> None:
    """The recorder's own folders, caches (a write there is a download),
    credential-shaped paths and `.probeignore`d files."""
    from probe.sdk import ignore

    cache = tmp_path / "xdg-cache"
    monkeypatch.setenv("XDG_CACHE_HOME", str(cache))
    rules = ignore.load(str(tmp_path / "work"), extra=["*.skipme"])
    assert inputs.start("run-never", ignore=rules)
    never = [
        tmp_path / "state" / "probe" / "logs" / "x.log",  # Probe's state
        tmp_path / "outbox" / "ops" / "op.json",  # the outbox
        tmp_path / "work" / ".cache" / "huggingface" / "hub" / "model.bin",
        cache / "torch" / "hub" / "weights.pt",
        tmp_path / "work" / ".ssh" / "id_ed25519",
        tmp_path / "work" / "__pycache__" / "m.bin",
        tmp_path / "work" / "app" / ".env",
        tmp_path / "work" / "train.py",
        tmp_path / "work" / "dump.skipme",
    ]
    kept = tmp_path / "work" / "result.bin"
    for path in [*never, kept]:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(b"x" * 100)
    got = inputs.collect_all("run-never", wait_s=5)
    assert list(_outputs(got)) == [str(kept)]


def test_the_interpreters_own_files_are_never_outputs() -> None:
    site = next(p for p in sys.path if p.endswith("site-packages"))
    assert inputs.excluded(f"{site}/pkg/data.bin")
    assert inputs.excluded(f"{sys.prefix}/lib/foo.txt") or sys.prefix in ("/", "/usr", "/usr/local")
    assert inputs.write_excluded(f"{Path.home()}/.cache/huggingface/hub/model.safetensors")
    # A READ of a model cache is still an input (the module docstring).
    assert not inputs.excluded(f"{Path.home()}/.cache/huggingface/hub/model.safetensors")


def test_a_forked_worker_notes_its_writes_in_its_own_spool(tmp_path) -> None:
    out = tmp_path / "work" / "shard-0.bin"
    out.parent.mkdir(parents=True)
    assert inputs.start("run-fw")

    def worker(path: str) -> None:
        with open(path, "wb") as handle:
            handle.write(b"f" * 500)

    ctx = multiprocessing.get_context("fork")
    proc = ctx.Process(target=worker, args=(str(out),))
    proc.start()
    proc.join(10)
    assert proc.exitcode == 0
    got = inputs.collect_all("run-fw", wait_s=5)
    assert _outputs(got)[str(out)]["content_hash"] == _sha(b"f" * 500)


def test_the_write_cap_bounds_what_is_held(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(inputs, "MAX_PATHS", 3)
    assert inputs.start("run-wcap")
    for i in range(5):
        _file(tmp_path, f"o{i}.bin", bytes([65 + i]) * 100)
    state = inputs._active["run-wcap"]
    assert len(state.written) == 3 and state.writes_truncated
    got = inputs.collect_all("run-wcap", wait_s=5)
    assert len(got.outputs) == 3 and got.outputs_coverage["truncated"] is True


# -- the switches ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("env", "capture_outputs", "recorded"),
    [
        ({}, None, True),
        ({}, False, False),
        ({"PROBE_CAPTURE_OUTPUTS": "0"}, None, False),
        ({"PROBE_CAPTURE_OUTPUTS": "0"}, True, True),
        ({"PROBE_CAPTURE_WRITES": "0"}, None, False),
        ({"PROBE_CAPTURE_WRITES": "0"}, True, False),
    ],
)
def test_writes_follow_the_capture_switches(tmp_path, monkeypatch, env, capture_outputs, recorded) -> None:
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    out = tmp_path / "work" / "out.bin"
    out.parent.mkdir(parents=True)
    assert inputs.start("run-switch", capture_outputs=capture_outputs)
    out.write_bytes(b"o" * 100)
    assert bool(inputs.collect_all("run-switch", wait_s=5).outputs) is recorded


def test_no_reads_means_no_writes(tmp_path) -> None:
    """Writes ride the read recorder: `capture_reads=False` turns both off."""
    assert inputs.start("run-off", capture_reads=False) is False
    (tmp_path / "out.bin").write_bytes(b"o" * 100)
    assert not list(inputs.state_dir().glob("run-off/*.jsonl"))


def test_the_env_names_are_output_captures_own() -> None:
    assert inputs.OUTPUTS_ENV == outputs.CAPTURE_ENV


def test_init_capture_outputs_false_sends_no_write_list(app, tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("e1")
    run = probe.init(experiment="e1", name="no-writes", capture_outputs=False)
    (tmp_path / "result.bin").write_bytes(b"r" * 100)
    probe.finish()
    assert run.id in app.__dict__.get("run_inputs", {})
    assert run.id not in app.__dict__.get("run_outputs", {})


# -- probe exec's Python child -------------------------------------------------------


def test_an_exec_child_notes_its_writes(tmp_path) -> None:
    out = tmp_path / "child_out.bin"
    tmp = tmp_path / "child_tmp.bin"
    staged = tmp_path / "child_ckpt.tmp"
    final = tmp_path / "child_ckpt.bin"
    env = {**os.environ}
    assert inputs.prepare_child("run-cw", env)
    code = (
        "import os\n"
        f"open({str(out)!r}, 'wb').write(b'c' * 400)\n"
        f"open({str(tmp)!r}, 'wb').write(b't'); os.unlink({str(tmp)!r})\n"
        f"open({str(staged)!r}, 'wb').write(b'k' * 300); os.replace({str(staged)!r}, {str(final)!r})\n"
    )
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    got = inputs.collect_all("run-cw", wait_s=5)
    rows = _outputs(got)
    assert sorted(rows) == sorted([str(out), str(final)])
    assert rows[str(out)]["content_hash"] == _sha(b"c" * 400)
    assert rows[str(final)]["content_hash"] == _sha(b"k" * 300)
    assert got.outputs_coverage["gone"] == 2


def test_probe_exec_sends_what_its_python_child_wrote(client, app, tmp_path) -> None:
    """The launcher side: the child's hook notes, the launcher hashes the final
    bytes after the child exits and posts the contract's body."""
    out = tmp_path / "exec_out.bin"
    run = open_run(client, experiment="exp-writes")
    run.execute(
        [sys.executable, "-c", f"open({str(out)!r}, 'wb').write(b'e' * 500)"],
        cwd=str(tmp_path),
        capture_outputs=False,
    )
    assert run.id not in app.__dict__.get("run_outputs", {}), "capture_outputs=False: no write list"
    run = open_run(client, experiment="exp-writes-2")
    out2 = tmp_path / "exec_out_2.bin"
    run.execute([sys.executable, "-c", f"open({str(out2)!r}, 'wb').write(b'f' * 500)"], cwd=str(tmp_path))
    client.flush(run_ref=run.id)
    (batch,) = app.run_outputs[run.id]
    assert run_outputs_problems(batch) == []
    assert [(r["path"], r["content_hash"]) for r in batch["outputs"]] == [(str(out2), _sha(b"f" * 500))]


@pytest.mark.parametrize(
    ("argument", "sent"),
    [("capture_outputs=False", ["inputs"]), ("capture_reads=False, capture_outputs=False", [])],
)
def test_an_exec_childs_opt_out_drops_what_it_noted_before(tmp_path, argument, sent) -> None:
    """P1 (review of 6e78909f0): `probe.init(capture_outputs=False)` in a
    `probe exec` child stopped NEW notes, but those already spooled -- and
    owner.json, which says writes are on -- went out with the launcher's
    close. The opt-out is written into the child's spool and wins."""
    data = _file(tmp_path, "early_in.bin", b"i" * 300)
    out = tmp_path / "early_out.bin"
    env = {**os.environ}
    assert inputs.prepare_child("run-co", env)
    code = (
        f"open({str(data)!r}, 'rb').read(); open({str(out)!r}, 'wb').write(b'o' * 300)\n"
        f"from probe.sdk import inputs\nassert inputs.start('run-co', {argument}) is False\n"
    )
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    client = _Client(inputs.FEATURE, inputs.OUTPUTS_FEATURE)
    inputs.finalize(client, "run-co", wait_s=5)
    assert [op[1].rsplit("/", 1)[1] for op in client.journal.ops] == sent


@pytest.mark.parametrize("name", [inputs.WRITES_ENV, inputs.OUTPUTS_ENV])
def test_an_exec_childs_environment_can_turn_writes_off(tmp_path, name) -> None:
    out = tmp_path / "quiet_out.bin"
    data = _file(tmp_path, "quiet_in.bin", b"i" * 300)
    env = {**os.environ, name: "0"}
    assert inputs.prepare_child("run-cq", env)
    code = f"open({str(data)!r}, 'rb').read(); open({str(out)!r}, 'wb').write(b'q' * 100)"
    subprocess.run([sys.executable, "-c", code], env=env, check=True)
    got = inputs.collect_all("run-cq", wait_s=5)
    assert got.outputs == [] and [r["path"] for r in got.inputs] == [str(data)]


def test_init_in_an_exec_child_can_turn_its_writes_off(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv(inputs.CHILD_DIR_ENV, str(tmp_path / "spool"))
    state = {"off": False, "writes_off": False}
    monkeypatch.setattr(sys, "_probe_reads_state", state, raising=False)
    assert inputs.start("run-y", capture_outputs=False) is False
    assert state == {"off": False, "writes_off": True}


# -- delivery -------------------------------------------------------------------


@pytest.mark.parametrize(
    ("features", "routes"),
    [
        ((inputs.FEATURE, inputs.OUTPUTS_FEATURE), ["inputs", "outputs"]),
        ((inputs.FEATURE,), ["inputs"]),
        ((inputs.OUTPUTS_FEATURE,), ["outputs"]),
        ((), []),
    ],
)
def test_each_list_goes_only_to_a_server_that_takes_it(tmp_path, features, routes) -> None:
    data = _file(tmp_path, "in.bin", b"i" * 300)
    assert inputs.start("run-f")
    data.read_bytes()
    (tmp_path / "work" / "out.bin").write_bytes(b"o" * 300)
    client = _Client(*features)
    inputs.finalize(client, "run-f", wait_s=5)
    assert [op[1].rsplit("/", 1)[1] for op in client.journal.ops] == routes
    assert all(op[4] is False for op in client.journal.ops)  # never holds the close
    assert not inputs.run_dir("run-f").exists()


def test_finish_posts_the_contract_exactly(app, tmp_path, monkeypatch) -> None:
    """Through `probe.init()` / `finish()` and the fake server, which checks
    the body against the shared contract (`run_outputs_problems`)."""
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("e1")
    run = probe.init(experiment="e1", name="writer")
    out = tmp_path / "model.bin"
    out.write_bytes(b"m" * 1000)
    probe.finish()
    (batch,) = app.run_outputs[run.id]
    assert run_outputs_problems(batch) == []
    (row,) = [r for r in batch["outputs"] if r["path"] == str(out)]
    assert tuple(row) == RUN_OUTPUT_KEYS
    assert row["content_hash"] == _sha(b"m" * 1000) and row["size_bytes"] == 1000
    assert row["fingerprint"] is None and row["host"]
    assert batch["coverage"]["recorder"] == inputs.RECORDER
    assert batch["coverage"]["unseen"] == list(inputs.UNSEEN_WRITERS)
    assert app.runs[run.id]["status"] == "completed"


def test_an_old_server_gets_no_write_list(app, tmp_path, monkeypatch) -> None:
    app.supports_run_outputs = False
    monkeypatch.setattr(fluent, "Client", lambda *a, **k: make_client(app, tmp_spool=tmp_path / "spool"))
    app.seed_experiment("e1")
    run = probe.init(experiment="e1", name="old")
    (tmp_path / "model.bin").write_bytes(b"m" * 100)
    probe.finish()
    assert run.id in app.run_inputs
    assert not [r for r in app.requests if r.url.path.endswith("/outputs")]


def test_a_dead_runs_writes_are_recovered(tmp_path) -> None:
    """A write the dead recorder last SAW as it is now (its ``.wf.json``
    sidecar holds this identity) is still its bytes: recovered with its hash."""
    out = _file(tmp_path, "left.bin", b"l" * 300)
    directory = _dead_run_with_a_write("run-dead", out, seen=inputs._ident(os.stat(out)))
    client = _Client(inputs.FEATURE, inputs.OUTPUTS_FEATURE)
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 1
    by_route = {op[1].rsplit("/", 1)[1]: op[2] for op in client.journal.ops}
    body = by_route["outputs"]
    assert body["coverage"]["recovered"] is True
    assert body["coverage"]["unverified_after_exit"] == 0
    assert body["outputs"][0]["content_hash"] == _sha(b"l" * 300)
    assert body["outputs"][0]["observation_id"] == "a" * 32
    assert run_outputs_problems(body) == []
    assert not directory.exists()


def test_the_recorder_notes_what_its_writes_are_while_it_lives(tmp_path) -> None:
    """The evidence a recovery needs: `check_writes` (the hasher's thread,
    every WRITE_CHECK_S) keeps a file's LAST identity in the process's
    ``.wf.json`` sidecar when it changed since the last look, and does
    nothing when it did not."""
    out = tmp_path / "work" / "ckpt.pt"
    out.parent.mkdir(parents=True)
    assert inputs.start("run-hb")
    out.write_bytes(b"v1")
    state = inputs._active["run-hb"]
    assert state.check_writes() == 1
    assert state.check_writes() == 0, "unchanged: nothing new"
    out.write_bytes(b"v2, longer")
    inputs._check_writes()  # what the hasher runs
    spool = next(inputs.run_dir("run-hb").glob("*.jsonl"))
    seen = json.loads(inputs._sidecar(spool).read_text())
    assert seen == {str(out): list(inputs._ident(os.stat(out)))}
    assert '"wf"' not in spool.read_text(), "identities never grow the spool"
    inputs.abandon("run-hb")


def test_a_rewritten_file_keeps_one_identity_however_often_it_changes(tmp_path) -> None:
    """P3 (review of d0e4d128b): a ``"wf"`` line per changed file per sweep
    grew without bound (500k lines: 66 MB, 3.2 s of parsing on the close
    thread, outside its wait). The sidecar holds the LAST identity per path,
    so its size follows the number of files, not of sweeps."""
    outs = [tmp_path / "work" / f"ckpt{i}.pt" for i in range(3)]
    outs[0].parent.mkdir(parents=True)
    assert inputs.start("run-many-sweeps")
    state = inputs._active["run-many-sweeps"]
    for sweep in range(200):
        for out in outs:
            out.write_bytes(b"x" * (sweep + 1))
        state.check_writes()
    spool = next(inputs.run_dir("run-many-sweeps").glob("*.jsonl"))
    seen = json.loads(inputs._sidecar(spool).read_text())
    assert sorted(seen) == sorted(map(str, outs))
    assert all(seen[str(out)][2] == 200 for out in outs), "the last identity, not the first"
    notes = [line for line in spool.read_text().splitlines() if not line.startswith('{"run"')]
    assert len(notes) == 3, "one note per written path, nothing per sweep"
    noted = inputs._SpooledWrites()
    inputs._read_spools([spool], writes=noted)
    assert noted.seen == {str(out): {inputs._ident(os.stat(out))} for out in outs}
    inputs.abandon("run-many-sweeps")


def test_a_recovered_write_rewritten_since_the_last_look_is_not_hashed(tmp_path) -> None:
    """The heartbeat saw v1; the file holds v2 now (someone else's): unhashed."""
    out = _file(tmp_path, "ckpt.pt", b"v1")
    _dead_run_with_a_write("run-rewritten", out, seen=inputs._ident(os.stat(out)))
    time.sleep(0.02)
    out.write_bytes(b"v2 from another run")
    client = _Client(inputs.FEATURE, inputs.OUTPUTS_FEATURE)
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 1
    body = {op[1].rsplit("/", 1)[1]: op[2] for op in client.journal.ops}["outputs"]
    (row,) = body["outputs"]
    assert row["content_hash"] == "" and row["size_bytes"] is None
    assert row["last_modified_at"] == row["first_written_at"], "only the run's own note dates it"
    assert run_outputs_problems(body) == []


def _dead_pid() -> int:
    return int(subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                              capture_output=True, text=True, check=True).stdout)


def _dead_run_with_a_write(run_id: str, out: Path, *, seen: tuple | None = None) -> Path:
    """A crashed run's spool: one write note, and -- ``seen`` -- the identity
    its recorder last saw the file have (its ``.wf.json`` sidecar)."""
    directory = inputs.run_dir(run_id)
    directory.mkdir(parents=True)
    dead = _dead_pid()
    (directory / "owner.json").write_text(json.dumps({"run_id": run_id, "pid": dead, "writes": True}))
    note = {"w": str(out), "t": "2026-09-26T00:00:00+00:00", "n": time.time_ns(), "o": "a" * 32, "b": None}
    spool = directory / f"{inputs._host()}.{dead}.jsonl"
    spool.write_text(json.dumps(note) + "\n")
    if seen is not None:
        inputs._sidecar(spool).write_text(json.dumps({str(out): list(seen)}))
    return directory


def test_recovery_never_sends_bytes_written_after_the_writer_died(tmp_path) -> None:
    """P1 (review of 6e78909f0): run A crashes after writing ckpt.pt; its
    retry B overwrites it; a later run's recovery used to send A's row with
    B's hash, size and mtime -- a wrong link. Nothing shows the file is still
    what A left, so the row goes unhashed and is counted."""
    out = _file(tmp_path, "ckpt.pt", b"A-weights")
    _dead_run_with_a_write("run-A", out)
    time.sleep(0.05)
    out.write_bytes(b"B-weights, the retry's")
    client = _Client(inputs.FEATURE, inputs.OUTPUTS_FEATURE)
    assert inputs.recover_orphans(client, now=time.time() + 3600) == 1
    body = {op[1].rsplit("/", 1)[1]: op[2] for op in client.journal.ops}["outputs"]
    (row,) = body["outputs"]
    assert row["content_hash"] != _sha(b"B-weights, the retry's")
    assert row["content_hash"] == "" and row["fingerprint"] is None
    assert body["coverage"]["unverified_after_exit"] == 1


def test_a_run_whose_writes_were_off_sends_no_write_list(tmp_path) -> None:
    """An empty list would say "wrote nothing" for a run that opted out: a
    collector that did not record the spools (a launcher, a recovery) sends
    one only when the recorder said writes were on."""
    data = _file(tmp_path, "in.bin", b"i" * 300)
    assert inputs.start("run-nowrites", capture_outputs=False)
    data.read_bytes()
    assert json.loads((inputs.run_dir("run-nowrites") / "owner.json").read_text())["writes"] is False
    client = _Client(inputs.FEATURE, inputs.OUTPUTS_FEATURE)
    inputs.finalize(client, "run-nowrites", wait_s=5)
    assert [op[1].rsplit("/", 1)[1] for op in client.journal.ops] == ["inputs"]


def test_writes_are_looked_at_even_when_another_close_is_hashing(tmp_path) -> None:
    """P2 4: writes were stat'ed only inside the hashing worker, so a busy
    one (a recovery hashing at init) or a long queue wait left every write
    `unchecked` -- and the spools were deleted. They are looked at first, on
    their own thread; a busy worker is waited for, never skipped."""
    import threading

    busy = threading.Event()
    blocker = threading.Thread(target=busy.wait, daemon=True)
    blocker.start()
    inputs._finish_worker = blocker
    try:
        out = tmp_path / "work" / "model.bin"
        out.parent.mkdir(parents=True)
        assert inputs.start("run-starved")
        out.write_bytes(b"m" * 1000)
        got = inputs.collect_all("run-starved", wait_s=1)
        (row,) = got.outputs
        assert row["path"] == str(out) and row["size_bytes"] == 1000
        assert got.outputs_coverage["unchecked"] == 0
        assert row["content_hash"] == "", "the worker stayed busy past the deadline"
        # A worker that finishes in time is waited for, then this close hashes.
        blocker2 = threading.Thread(target=time.sleep, args=(0.3,), daemon=True)
        blocker2.start()
        inputs._finish_worker = blocker2
        assert inputs.start("run-waits")
        out.write_bytes(b"n" * 1000)
        (row,) = inputs.collect_all("run-waits", wait_s=5).outputs
        assert row["content_hash"] == _sha(b"n" * 1000)
    finally:
        busy.set()


def test_a_link_into_a_cache_is_a_download_too(tmp_path, monkeypatch) -> None:
    """P2 11: the cache rule looked at the path as written only."""
    cache = tmp_path / "xdg-cache"
    (cache / "hub").mkdir(parents=True)
    monkeypatch.setenv("XDG_CACHE_HOME", str(cache))
    (tmp_path / "work").mkdir()
    (tmp_path / "work" / "models").symlink_to(cache / "hub")
    assert inputs.start("run-link")
    (tmp_path / "work" / "models" / "weights.bin").write_bytes(b"w" * 100)
    (tmp_path / "work" / "real.bin").write_bytes(b"r" * 100)
    got = inputs.collect_all("run-link", wait_s=5)
    assert list(_outputs(got)) == [str(tmp_path / "work" / "real.bin")]


def test_a_path_object_that_raises_never_escapes_the_hook() -> None:
    class Bad:
        def __fspath__(self):
            raise ValueError("user code")

    assert inputs._hooked_path(Bad()) is None
    inputs._on_audit("os.rename", (Bad(), Bad(), None, None))  # no raise


def test_a_fork_while_a_budget_is_being_charged_does_not_deadlock_the_child(monkeypatch) -> None:
    """P3 14: the budget lock is reset in a forked child like the others."""
    for name in ("_lock", "_budget_lock", "_hash_queue", "_hasher", "_hasher_pid"):
        monkeypatch.setattr(inputs, name, getattr(inputs, name))
    held = inputs._budget_lock
    held.acquire()  # another thread was charging a budget at the fork
    try:
        inputs._after_fork_in_child()
        assert inputs._budget_lock is not held
        assert inputs._take([10], 5)
    finally:
        held.release()


def test_ten_thousand_writes_journal_quickly(tmp_path, monkeypatch) -> None:
    """A write row's hash, times and observation id are shape-checked and
    lifted past the journal's scrubber (`stamp_scrub`), as a read row's are:
    only the path is scanned."""
    from probe.sdk import redaction
    from probe.sdk.journal import Journal

    monkeypatch.setenv("PROBE_OUTBOX_MIN_FREE_BYTES", "0")
    assert redaction.enable_scrub_cache()
    rows = [
        {
            "path": f"/data/out/part-{i // 100:03d}/shard-{i}.bin",
            "host": "node-1",
            "content_hash": hashlib.sha256(str(i).encode()).hexdigest(),
            "fingerprint": None,
            "size_bytes": 1000 + i,
            "first_written_at": f"2026-09-26T00:{i // 60 % 60:02d}:{i % 60:02d}.{i:06d}+00:00",
            "last_modified_at": f"2026-09-26T01:{i // 60 % 60:02d}:{i % 60:02d}.{i:06d}+00:00",
            "observation_id": hashlib.md5(str(i).encode()).hexdigest(),
        }
        for i in range(10_000)
    ]
    uncached = [0]
    real = redaction._scrub_string
    monkeypatch.setattr(redaction, "_scrub_string", lambda v, **k: (uncached.__setitem__(0, uncached[0] + 1), real(v, **k))[1])

    class _RealJournalClient:
        journal = Journal(tmp_path / "outbox", context={"base_url": "http://x"})

        def supports_feature(self, name: str) -> bool:
            return True

    started = time.process_time()
    assert inputs.send_outputs(_RealJournalClient(), "run-10k", rows, {"recorder": "x"})
    elapsed = time.process_time() - started
    assert uncached[0] < len(rows) + 200, f"{uncached[0]} uncached scrubs"
    stored = [op for _, op in _RealJournalClient.journal.pending()]
    assert [r for op in stored for r in op["body"]["outputs"]] == rows  # nothing rewritten
    assert elapsed < 1.5, f"{elapsed:.2f}s of CPU"


def test_a_token_in_a_write_path_is_redacted(tmp_path) -> None:
    out = tmp_path / "work" / TOKEN / "out.bin"
    out.parent.mkdir(parents=True)
    assert inputs.start("run-tokpath")
    out.write_bytes(b"x" * 100)
    got = inputs.collect_all("run-tokpath", wait_s=5)
    assert TOKEN not in json.dumps(got.outputs)
    assert got.outputs[0]["content_hash"] == _sha(b"x" * 100)


# -- one I/O budget, reads first (F2c) ---------------------------------------------


def test_reads_are_hashed_before_writes_from_one_budget(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(inputs, "RUN_HASH_BUDGET_BYTES", 1000)
    monkeypatch.setattr(inputs, "EDGE_BYTES", 150)
    data = _file(tmp_path, "in.bin", b"i" * 800)
    out = tmp_path / "work" / "out.bin"
    assert inputs.start("run-order")
    data.read_bytes()
    out.write_bytes(b"o" * 800)
    got = inputs.collect_all("run-order", wait_s=5)
    assert got.inputs[0]["content_hash"] == _sha(b"i" * 800)
    row = _outputs(got)[str(out)]
    # 200 bytes left: not the write's 800, nor the 300 its fingerprint reads.
    assert row["content_hash"] == "" and row["fingerprint"] is None and row["size_bytes"] == 800
    assert got.outputs_coverage["unhashed"] == 1
    assert got.outputs_coverage["hash_cut"] == {"budget": 1}


def test_past_the_budget_fingerprints_are_charged_and_stop(tmp_path, monkeypatch) -> None:
    """Finding 13: a run that wrote many big files cannot turn its close into
    an unbounded read of their edges."""
    monkeypatch.setattr(inputs, "RUN_HASH_BUDGET_BYTES", 250)
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 100)
    monkeypatch.setattr(inputs, "EDGE_BYTES", 50)
    assert inputs.start("run-edges")
    for i in range(6):
        _file(tmp_path, f"big{i}.bin", bytes([65 + i]) * 1000)
    opened: list[str] = []
    real_open = open

    def counting_open(file, *a, **k):
        if str(file).endswith(".bin") and "big" in str(file) and "b" in (a[0] if a else k.get("mode", "r")):
            opened.append(str(file))
        return real_open(file, *a, **k)

    monkeypatch.setattr("builtins.open", counting_open)
    got = inputs.collect_all("run-edges", wait_s=5)
    monkeypatch.setattr("builtins.open", real_open)
    fingerprinted = [r for r in got.outputs if r["fingerprint"]]
    assert len(fingerprinted) == 2, "250 bytes pay for two 100-byte fingerprints"
    assert len(opened) == 2, "and nothing else is read"
    assert got.outputs_coverage["hash_cut"] == {"budget": 4}


def test_hashing_stops_at_the_deadline(tmp_path, monkeypatch) -> None:
    data = _file(tmp_path, "slow.bin", b"s" * 10_000)
    ident = inputs._ident(os.stat(data))
    budget = [1 << 40]
    # Past the deadline: nothing is read, nothing charged -- a fingerprint too.
    assert inputs.hash_file(str(data), ident, cache=None, budget=budget, deadline=time.monotonic() - 1) is None
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 100)
    assert inputs.hash_file(str(data), ident, cache=None, budget=budget, deadline=time.monotonic() - 1) is None
    assert budget == [1 << 40]
    # A full hash the deadline overtakes stops mid-file and pays for what it read.
    monkeypatch.setattr(inputs, "FULL_HASH_MAX_BYTES", 1 << 30)
    monkeypatch.setattr(inputs, "_CHUNK", 1000)
    ticks = iter(range(1000))
    monkeypatch.setattr(inputs, "time", types.SimpleNamespace(monotonic=lambda: next(ticks)))
    assert inputs.hash_file(str(data), ident, cache=None, budget=budget, deadline=3) is None
    assert (1 << 40) - budget[0] < 10_000


def test_the_close_leaves_its_budget_to_references(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(inputs, "RUN_HASH_BUDGET_BYTES", 1000)
    data = _file(tmp_path, "in.bin", b"i" * 600)
    assert inputs.start("run-left")
    data.read_bytes()
    inputs.collect_all("run-left", wait_s=5)
    budget = inputs.reference_budget("run-left")
    assert budget == [400]
    # P2 7: every capture window of the run (`Run.execute` closes two) draws
    # from the SAME object, never a fresh 10 GiB.
    assert inputs.reference_budget("run-left") is budget
    assert inputs.reference_budget("run-unrecorded") is inputs.reference_budget("run-unrecorded")


# -- capture references carry a hash (F3) -----------------------------------------


@pytest.fixture
def work(monkeypatch, tmp_path):
    folder = tmp_path / "capture"
    folder.mkdir()
    monkeypatch.chdir(folder)
    monkeypatch.setenv("PROBE_CAPTURE_LOG", "0")
    monkeypatch.setenv(ephemeral.ENV, "0")
    monkeypatch.setattr(outputs, "_shared_warned", set())
    return folder


def _captured(app, run) -> dict[str, dict]:
    return {a["name"]: a for a in app.artifacts.get(run.id, [])}


def _stored(app, row) -> bytes:
    return app.blobs.get(row["id"]) or app.blobs_by_hash.get(row["content_hash"])


def test_a_capture_reference_carries_the_files_hash(client, app, work, monkeypatch) -> None:
    monkeypatch.setenv(inputs.READS_ENV, "0")
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 1024)
    run = open_run(client, experiment="ref-hash", capture_outputs=True)
    (work / "ckpt.pt").write_bytes(b"\x01" * 5000)
    run.finish()
    row = _captured(app, run)["outputs/ckpt.pt"]
    assert row["is_reference"] and not app.puts
    assert row["content_hash"] == _sha(b"\x01" * 5000)


def test_a_reference_is_paid_from_what_the_reads_left(client, app, work, monkeypatch) -> None:
    """One budget: reads during the run, then the close's writes, then the
    references. A budget the run's reads spent leaves the reference unhashed."""
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 1024)
    monkeypatch.setattr(inputs, "RUN_HASH_BUDGET_BYTES", 6000)
    monkeypatch.setenv(inputs.WRITES_ENV, "0")
    dataset = work.parent / "dataset.bin"
    dataset.write_bytes(b"d" * 5000)
    run = open_run(client, experiment="ref-budget", capture_outputs=True, capture_reads=True)
    dataset.read_bytes()
    (work / "ckpt.pt").write_bytes(b"\x02" * 5000)
    run.finish()
    row = _captured(app, run)["outputs/ckpt.pt"]
    assert row["is_reference"] and row.get("content_hash") is None


def test_references_are_hashed_after_every_upload(client, app, work, monkeypatch) -> None:
    """Hashing a reference reads up to 1 GiB: the close's time goes to the
    uploads first, so a big file sorted early cannot starve small ones."""
    monkeypatch.setenv(inputs.READS_ENV, "0")
    monkeypatch.setattr(outputs, "INSPECT_LIMIT_BYTES", 1024)
    events: list[str] = []
    real_hash, real_queue = inputs.reference_hash, outputs.OutputCapture._queue_generated
    monkeypatch.setattr(inputs, "reference_hash", lambda p, **k: events.append("hash") or real_hash(p, **k))
    monkeypatch.setattr(
        outputs.OutputCapture, "_queue_generated",
        lambda self, name, data, **k: events.append("upload") or real_queue(self, name, data, **k),
    )
    run = open_run(client, experiment="ref-order", capture_outputs=True)
    (work / "big.bin").write_bytes(b"\x03" * 5000)  # top level: sorted before sub/
    (work / "sub").mkdir()
    (work / "sub" / "a.txt").write_text("a")
    (work / "sub" / "b.txt").write_text("b")
    run.finish()
    assert events == ["upload", "upload", "hash"]
    assert _captured(app, run)["outputs/big.bin"]["content_hash"] == _sha(b"\x03" * 5000)


def test_a_stalled_mount_cannot_hold_the_close_through_a_reference(tmp_path, monkeypatch) -> None:
    """P2 8: the reference's stat ran on the close's own thread, before the
    deadline was even checked."""
    data = _file(tmp_path, "stalled.bin", b"s" * 100)
    real = os.stat

    def stalled(path, *a, **k):
        if str(path) == str(data):
            time.sleep(3)
        return real(path, *a, **k)

    monkeypatch.setattr(os, "stat", stalled)
    began = time.monotonic()
    assert inputs.reference_hash(str(data), budget=[1 << 40], deadline=time.monotonic() + 0.3) is None
    assert time.monotonic() - began < 1.5


def test_the_hasher_looks_at_written_files_on_its_own(tmp_path, monkeypatch) -> None:
    """The heartbeat is the hasher's: no close, no call from the test."""
    import queue as _queue
    import threading

    monkeypatch.setattr(inputs, "WRITE_CHECK_S", 0.05)
    monkeypatch.setattr(inputs, "_hash_queue", _queue.Queue())
    out = tmp_path / "work" / "ckpt.pt"
    out.parent.mkdir(parents=True)
    assert inputs.start("run-beat")
    out.write_bytes(b"x" * 10)
    loop = threading.Thread(target=inputs._hash_loop, daemon=True)
    loop.start()
    sidecar = inputs._sidecar(next(inputs.run_dir("run-beat").glob("*.jsonl")))
    deadline = time.monotonic() + 5
    while not sidecar.exists() and time.monotonic() < deadline:
        time.sleep(0.02)
    for _ in range(2):  # the process's own hasher may share the queue
        inputs._hash_queue.put(None)
    loop.join(5)
    assert json.loads(sidecar.read_text()) == {str(out): list(inputs._ident(os.stat(out)))}
    inputs.abandon("run-beat")


def test_a_reference_past_the_deadline_is_left_unhashed(tmp_path) -> None:
    data = _file(tmp_path, "late.bin", b"l" * 100)
    assert inputs.reference_hash(str(data), budget=[1 << 40], deadline=time.monotonic() - 1) is None
    assert inputs.reference_hash(str(data), budget=[10], deadline=time.monotonic() + 30) is None
    assert inputs.reference_hash(str(data), budget=[1 << 40], deadline=time.monotonic() + 30) == _sha(b"l" * 100)
    # Changed since capture listed it: its hash would not describe the row.
    assert inputs.reference_hash(str(data), budget=[1 << 40], deadline=time.monotonic() + 30, size=99) is None


# -- redacted uploads carry the original's hash (F1) -------------------------------


def test_two_originals_that_redact_alike_are_one_version(client, app, work, monkeypatch) -> None:
    """Rewritten with another token of the same kind, the file redacts to the
    SAME bytes: one stored version, keeping the FIRST original's hash, and the
    later original's hash rides the run's write list instead."""
    first = f"token {TOKEN} used\n".encode()
    second = f"token {OTHER_TOKEN} used\n".encode()
    run = open_run(client, experiment="f1-two", capture_outputs=True, capture_reads=True)
    notes = work / "notes.txt"
    with open(notes, "wb") as handle:  # a write the recorder notes
        handle.write(first)
    with pytest.warns(UserWarning, match="replaced credentials"):
        run._finalize_capture()
    client.flush(run_ref=run.id)
    (row,) = [a for a in app.artifacts[run.id] if a["name"] == "outputs/notes.txt"]
    with open(notes, "wb") as handle:
        handle.write(second)
    run._capture._sweep_done = run._capture._log_done = False  # a second close sweeps again
    run.finish()
    rows = [a for a in app.artifacts[run.id] if a["name"] == "outputs/notes.txt"]
    assert len(rows) == 1 and rows[0]["meta"]["source_sha256"] == _sha(first)
    written = [r for b in app.run_outputs[run.id] for r in b["outputs"] if r["path"] == str(notes)]
    assert [r["content_hash"] for r in written] == [_sha(second)]


# -- review of d0e4d128b: the hook's cost, a late sweep, a stuck worker --------


def test_past_the_write_cap_nothing_is_judged(tmp_path, monkeypatch) -> None:
    """P2: the write hook resolved every new path (one lstat per component)
    and ran every exclusion BEFORE `record_write` looked at the cap, so a run
    past 10,000 writes paid the full price per open to note nothing."""
    monkeypatch.setattr(inputs, "MAX_PATHS", 2)
    judged: list[str] = []
    real = inputs._write_skip
    monkeypatch.setattr(inputs, "_write_skip", lambda target, path: judged.append(path) or real(target, path))
    (tmp_path / "work").mkdir()
    assert inputs.start("run-past-cap")
    for i in range(6):
        (tmp_path / "work" / f"o{i}.bin").write_bytes(b"o")
    state = inputs._active["run-past-cap"]
    assert len(state.written) == 2 and state.writes_truncated
    assert len(judged) == 2, "past the cap a write-open is not judged at all"
    inputs.abandon("run-past-cap")


def test_a_write_resolves_its_folder_once(tmp_path, monkeypatch) -> None:
    """P2: `os.path.realpath` per new path (one lstat per component) is
    replaced by the folder's cached resolution plus one lstat of the file,
    so a link into a cache is still seen (see the next test) at a fraction of
    the cost."""
    folder = tmp_path / "work" / "a" / "b" / "c"
    folder.mkdir(parents=True)
    inputs._real_dirs.clear()
    assert inputs.start("run-realpath")
    calls: list[str] = []
    real = os.path.realpath
    monkeypatch.setattr(os.path, "realpath", lambda p, *a, **k: calls.append(p) or real(p, *a, **k))
    for i in range(50):
        (folder / f"f{i}.bin").write_bytes(b"f")
    assert len(inputs._active["run-realpath"].written) == 50
    # The folder once; never a path in it (Probe's own folders -- `owndirs` --
    # may be resolved on the side, once).
    assert [c for c in calls if c.startswith(str(folder))] == [str(folder)], calls[:8]
    inputs.abandon("run-realpath")


def test_a_linked_file_into_a_cache_is_still_a_download(tmp_path, monkeypatch) -> None:
    """The folder cache must not hide a FILE that is itself a link into a cache."""
    cache = tmp_path / "xdg-cache"
    cache.mkdir()
    monkeypatch.setenv("XDG_CACHE_HOME", str(cache))
    (tmp_path / "work").mkdir()
    (tmp_path / "work" / "weights.bin").symlink_to(cache / "weights.bin")
    assert inputs.start("run-file-link")
    (tmp_path / "work" / "weights.bin").write_bytes(b"w" * 100)
    (tmp_path / "work" / "mine.bin").write_bytes(b"m" * 100)
    got = inputs.collect_all("run-file-link", wait_s=5)
    assert list(_outputs(got)) == [str(tmp_path / "work" / "mine.bin")]


def test_a_sweep_after_the_close_recreates_nothing(tmp_path) -> None:
    """P3: a `check_writes` sweep under way when the run closed reopened the
    spool (`spool()` after `close()`), re-creating the folder the close had
    removed -- and a later recovery posted an empty "recovered" list for a
    run that had closed and sent everything."""
    out = tmp_path / "work" / "ckpt.pt"
    out.parent.mkdir(parents=True)
    assert inputs.start("run-late-sweep")
    out.write_bytes(b"v1")
    state = inputs._active["run-late-sweep"]
    client = _Client(inputs.FEATURE, inputs.OUTPUTS_FEATURE)
    inputs.finalize(client, "run-late-sweep", wait_s=5)
    assert not inputs.run_dir("run-late-sweep").exists()
    out.write_bytes(b"v2, after the close")
    assert state.check_writes() == 0  # the sweep that was already under way
    state.record_write(str(tmp_path / "work" / "later.bin"))
    state.record(str(out))
    assert not inputs.run_dir("run-late-sweep").exists()
    later = _Client(inputs.FEATURE, inputs.OUTPUTS_FEATURE)
    assert inputs.recover_orphans(later, now=time.time() + 3600) == 0
    assert later.journal.ops == []


def test_a_close_does_not_wait_on_a_worker_stuck_past_its_deadline(tmp_path) -> None:
    """P3: a hashing worker hung on a stalled mount stays alive forever, and
    every later close waited its whole wait on it and hashed nothing. A
    worker alive HUNG_AFTER_S past its own deadline is no longer waited for."""
    import threading

    stuck = threading.Event()
    hung = threading.Thread(target=stuck.wait, daemon=True)
    hung.start()
    hung.probe_deadline = time.monotonic() - inputs.HUNG_AFTER_S - 1  # type: ignore[attr-defined]
    inputs._finish_worker = hung
    try:
        data = _file(tmp_path, "in.bin", b"i" * 300)
        assert inputs.start("run-after-a-hang")
        data.read_bytes()
        began = time.monotonic()
        got = inputs.collect_all("run-after-a-hang", wait_s=10)
        assert time.monotonic() - began < 5
        (row,) = got.inputs
        assert row["content_hash"] == _sha(b"i" * 300)
    finally:
        stuck.set()


def test_reopening_the_spool_past_the_write_cap_does_not_deadlock(tmp_path, monkeypatch) -> None:
    """Opening the spool is Probe's own write: judged by the hook past the
    cap, it re-entered `record_write`, which asked for the spool's lock the
    opener already held."""
    import threading

    monkeypatch.setattr(inputs, "MAX_PATHS", 1)
    (tmp_path / "work").mkdir()
    assert inputs.start("run-reopen")
    (tmp_path / "work" / "a.bin").write_bytes(b"a")  # noted: the cap is reached
    state = inputs._active["run-reopen"]
    state._fh = None  # the next line reopens the spool
    done = threading.Event()
    threading.Thread(target=lambda: (state.mark_truncated(), done.set()), daemon=True).start()
    assert done.wait(5), "the spool's lock was taken twice by one thread"
    inputs.abandon("run-reopen")
