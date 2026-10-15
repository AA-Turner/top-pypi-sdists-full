"""`probe exec --input PATH --output PATH -- CMD` (data catalog F39): a shell
step's files, which no read hook sees, are hashed with the recorder's hasher
when the step starts (inputs) and exits (outputs it created or changed), and
sent as the run's reads and writes, so hash matching draws the arrows."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from probe import cli
from probe.sdk import exclusions, inputs, probe_config as pc
from tests.conftest import make_client, run_outputs_problems


@pytest.fixture(autouse=True)
def _fresh(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    for name in ("PROBE_RUN_ID", "PROBE_RUN_EPOCH", "CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "PROBE_CAPTURE_LOG"):
        monkeypatch.delenv(name, raising=False)
    inputs._hash_results.clear()
    pc._CACHE.clear()
    pc._CHECKED.clear()
    exclusions._view_at = -1.0e9
    yield
    inputs._hash_results.clear()


class _Journal:
    def __init__(self) -> None:
        self.ops: list[tuple[str, str, dict]] = []

    def append_http(self, method, path, body, **_kw):
        self.ops.append((method, path, body))
        return True


class _Client:
    def __init__(self, features=("run_inputs", "run_outputs")) -> None:
        self.journal = _Journal()
        self.features = set(features)

    def supports_feature(self, name: str) -> bool:
        return name in self.features

    def rows(self, route: str) -> list[dict]:
        return [row for _m, path, body in self.journal.ops if path.endswith(route) for row in body[route.strip("/")]]


@pytest.fixture
def step(tmp_path):
    work = tmp_path / "work"
    (work / "data").mkdir(parents=True)
    (work / "data" / "a.jsonl").write_text("".join(f'{{"i": {i}, "pad": "{"x" * 40}"}}\n' for i in range(30)))
    (work / "data" / "b.jsonl").write_text('{"i": 99}\n' * 5)
    return work


def test_named_inputs_are_hashed_at_start_and_outputs_at_exit(step):
    client = _Client()
    named = inputs.NamedFiles(client, "run-1", inputs=["data/*.jsonl"], outputs=["out/dev.jsonl"], base=str(step))
    assert named.start() == 2
    reads = client.rows("/inputs")
    a = step / "data" / "a.jsonl"
    assert {Path(r["path"]).name for r in reads} == {"a.jsonl", "b.jsonl"}
    row_a = next(r for r in reads if r["path"].endswith("a.jsonl"))
    assert row_a["content_hash"] == hashlib.sha256(a.read_bytes()).hexdigest() and row_a["rows"] == 30
    assert "observation_id" in row_a
    assert all("coverage" not in body for _m, _p, body in client.journal.ops)  # never replaces the run's
    # The step (a shell `head`) writes its output.
    (step / "out").mkdir()
    (step / "out" / "dev.jsonl").write_text("".join(a.read_text().splitlines(keepends=True)[:10]))
    assert named.finish() == 1
    writes = client.rows("/outputs")
    assert writes[0]["rows"] == 10
    assert writes[0]["content_hash"] == hashlib.sha256((step / "out" / "dev.jsonl").read_bytes()).hexdigest()
    body = next(body for _m, path, body in client.journal.ops if path.endswith("/outputs"))
    assert run_outputs_problems(body) == []


def test_an_output_the_step_did_not_change_is_not_sent(step):
    client = _Client()
    named = inputs.NamedFiles(client, "run-2", outputs=["data/b.jsonl"], base=str(step))
    named.start()
    assert named.finish() == 0 and client.journal.ops == []


def test_off_and_read_paths_are_skipped_and_hash_paths_keep_the_floor(step):
    (step / "secret").mkdir()
    (step / "secret" / "k.txt").write_text("PRIVATE " * 20)
    (step / "notes").mkdir()
    (step / "notes" / "n.txt").write_text("looked at " * 20)
    (step / "labels").mkdir()
    (step / "labels" / "tiny.txt").write_text("yes\n")
    (step / pc.CONFIG_NAME).write_text("secret/\nnotes/ @probe read\nlabels/ @probe hash\n")
    client = _Client()
    named = inputs.NamedFiles(
        client, "run-3", inputs=["secret/k.txt", "notes", "labels/tiny.txt", "data/b.jsonl"], base=str(step)
    )
    assert named.start() == 2
    by_name = {Path(r["path"]).name: r for r in client.rows("/inputs")}
    assert set(by_name) == {"tiny.txt", "b.jsonl"}
    assert by_name["tiny.txt"]["content_hash"] is None and by_name["tiny.txt"]["size_bytes"] == 4
    assert by_name["b.jsonl"]["rows"] == 5


def test_nothing_is_sent_to_a_server_that_does_not_take_the_lists(step):
    client = _Client(features=())
    named = inputs.NamedFiles(client, "run-4", inputs=["data/a.jsonl"], outputs=["data/new.txt"], base=str(step))
    assert named.start() == 0
    (step / "data" / "new.txt").write_text("hello world\n")
    assert named.finish() == 0 and client.journal.ops == []


def test_globs_folders_and_missing_names_expand_to_files(step):
    found = inputs.expand_named(["data", "data/*.jsonl", "nothing/*.csv", "missing.txt"], str(step))
    assert [Path(p).name for p in found] == ["a.jsonl", "b.jsonl"]
    assert inputs.expand_named(["**/b.jsonl"], str(step)) == [str(step / "data" / "b.jsonl")]


# -- through the CLI, with a shell step ------------------------------------------------


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    cli.main(["project", "create", "--kind", "general", "p"])
    return app


def _deliver(app, tmp_path) -> None:
    make_client(app, tmp_spool=tmp_path / "spool").flush()


def test_exec_hashes_a_shell_steps_named_files(wired, step, tmp_path, monkeypatch):
    monkeypatch.chdir(step)
    rc = cli.main([
        "exec", "--project", "p", "--name", "build-dev", "--no-capture-outputs",
        "--input", "data/a.jsonl", "--output", "dev.jsonl",
        "--", "sh", "-c", "head -n 7 data/a.jsonl > dev.jsonl",
    ])
    assert rc == 0
    _deliver(wired, tmp_path)
    run_id = next(rid for rid, row in wired.runs.items() if row["name"] == "build-dev")
    reads = [r for batch in wired.run_inputs[run_id] for r in batch.get("inputs", [])]
    named_read = [r for r in reads if r["path"] == str(step / "data" / "a.jsonl")]
    assert named_read and named_read[0]["rows"] == 30
    assert named_read[0]["content_hash"] == hashlib.sha256((step / "data" / "a.jsonl").read_bytes()).hexdigest()
    writes = [r for batch in wired.run_outputs[run_id] for r in batch.get("outputs", [])]
    dev = [w for w in writes if w["path"] == str(step / "dev.jsonl")]
    assert dev and dev[0]["rows"] == 7
    assert dev[0]["content_hash"] == hashlib.sha256((step / "dev.jsonl").read_bytes()).hexdigest()


def test_exec_in_a_hash_folder_opens_the_run_and_keeps_no_log(wired, step, tmp_path, monkeypatch):
    (step / pc.CONFIG_NAME).write_text("@probe hash\n*\n")
    monkeypatch.chdir(step)
    seen = tmp_path / "env.json"
    rc = cli.main([
        "exec", "--project", "p", "--name", "relabel",
        "--", "sh", "-c", f"printf '%s' \"$PROBE_CAPTURE_LOG\" > {seen}",
    ])
    assert rc == 0
    assert any(row["name"] == "relabel" for row in wired.runs.values())
    assert seen.read_text() == "0"  # the child is told: no console log
    import os

    assert "PROBE_CAPTURE_LOG" not in os.environ  # restored for this process


@pytest.mark.parametrize("hashed", [True, False])
def test_a_launcher_in_a_hash_folder_keeps_no_log_and_no_file(client, app, step, monkeypatch, hashed):
    """`Run.execute` (what `probe exec` runs): in a `hash` folder the run's
    console log and its files are never captured; elsewhere both are."""
    from tests.conftest import open_run

    if hashed:
        (step / pc.CONFIG_NAME).write_text("@probe hash\n*\n")
    monkeypatch.chdir(step)
    run = open_run(client, experiment=f"hash-{hashed}", capture_outputs=False)
    result = run.execute(
        ["sh", "-c", "echo printed-a-record; head -n 2 data/a.jsonl > dev.jsonl"], cwd=str(step), capture_outputs=True
    )
    assert result.returncode == 0
    names = [a["name"] for a in app.artifacts.get(run.id, [])]
    assert ("probe/run.log" in names) is not hashed
    assert ("outputs/dev.jsonl" in names) is not hashed
    assert "a.jsonl" not in json.dumps(app.artifacts.get(run.id, [])) or not hashed


def test_exec_naming_a_hash_file_below_an_on_folder_keeps_no_log(wired, step, tmp_path, monkeypatch):
    """Review of #2791 F1: only the working directory was checked, so a shell
    step run from an `on` folder that prints a `hash` file's records shipped
    them in `probe/run.log`. Any path the command names counts, inside a
    shell string too."""
    (step / "data" / pc.CONFIG_NAME).write_text("@probe hash\n*\n")
    monkeypatch.chdir(step)
    monkeypatch.setenv("PROBE_CAPTURE_OUTPUTS", "1")  # conftest pins capture off
    rc = cli.main(["exec", "--project", "p", "--name", "peek", "--", "sh", "-c", "head -n 3 data/a.jsonl"])
    assert rc == 0
    _deliver(wired, tmp_path)
    run_id = next(rid for rid, row in wired.runs.items() if row["name"] == "peek")
    assert "probe/run.log" not in [a["name"] for a in wired.artifacts.get(run_id, [])]
    assert not [r for r in wired.requests if b'"pad"' in (r.content or b"")], "a record left the machine"


def test_exec_from_an_on_folder_naming_on_files_keeps_its_log(wired, step, tmp_path, monkeypatch):
    """The other side of F1: nothing excluded is named, so the log is kept."""
    monkeypatch.chdir(step)
    monkeypatch.setenv("PROBE_CAPTURE_OUTPUTS", "1")
    rc = cli.main(["exec", "--project", "p", "--name", "peek-on", "--", "sh", "-c", "head -n 1 data/b.jsonl"])
    assert rc == 0
    _deliver(wired, tmp_path)
    run_id = next(rid for rid, row in wired.runs.items() if row["name"] == "peek-on")
    assert "probe/run.log" in [a["name"] for a in wired.artifacts.get(run_id, [])]
