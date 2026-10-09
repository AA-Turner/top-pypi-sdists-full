"""`.probe.config` in the SDK: `probe.init()` opens no run where it is excluded,
`log_artifact` records nothing about an excluded file, and code, output and read
capture skip excluded paths -- with or without a `.probeignore`."""

from __future__ import annotations

import os

import pytest

import probe
from probe.sdk import disabled, exclusions, inputs, outputs, probe_config as pc, snapshot
from probe.sdk.run import Run


@pytest.fixture
def tree(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("PROBE_OUTBOX_DIR", str(tmp_path / "outbox"))
    for name in ("CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "PI_SESSION_ID", "PROBE_MODE", "PROBE_RUN_ID"):
        monkeypatch.delenv(name, raising=False)
    pc._CACHE.clear()
    pc._CHECKED.clear()
    exclusions._view_at = -1.0e9
    repo = tmp_path / "repo"
    (repo / "data").mkdir(parents=True)
    (repo / "src").mkdir()
    (repo / "data" / "rows.jsonl").write_text("x")
    (repo / "src" / "train.py").write_text("x")
    (repo / pc.CONFIG_NAME).write_text("/data/\n")
    return repo


def test_init_in_an_excluded_folder_opens_no_run(tree, monkeypatch, capsys):
    monkeypatch.chdir(tree / "data")
    run = probe.init(project="p", name="r")
    try:
        assert isinstance(run, disabled.DisabledRun)
        err = capsys.readouterr().err
        assert "is excluded by" in err and "no run was opened" in err
    finally:
        run.finish()


def test_init_from_an_excluded_script(tree, monkeypatch, capsys):
    script = tree / "data" / "go.py"
    script.write_text("x")
    monkeypatch.chdir(tree)
    monkeypatch.setattr("sys.argv", [str(script)])
    run = probe.init(project="p", name="r")
    try:
        assert isinstance(run, disabled.DisabledRun)
    finally:
        run.finish()


def test_run_excluded_is_none_elsewhere(tree, monkeypatch):
    monkeypatch.chdir(tree / "src")
    monkeypatch.setattr("sys.argv", [str(tree / "src" / "train.py")])
    assert exclusions.run_excluded() is None


def test_log_artifact_skips_an_excluded_file(tree, capsys):
    # Returns before touching the run at all.
    assert Run.log_artifact(object(), "rows", path=str(tree / "data" / "rows.jsonl")) is None
    assert "so it was not uploaded" in capsys.readouterr().err


def test_output_walk_skips_excluded(tree):
    found, _cut = outputs._walk(str(tree), set(), 1000)
    assert "src/train.py" in found
    assert not any(p.startswith("data/") for p in found)


def test_read_capture_skips_excluded(tree):
    # Judged where reads are hashed and recorded; the open() wrapper does no I/O.
    assert inputs._config_excluded(str(tree / "data" / "rows.jsonl"))
    assert not inputs._config_excluded(str(tree / "src" / "train.py"))
    assert not inputs._ignored(None, str(tree / "data" / "rows.jsonl"))


def test_code_capture_drops_excluded_without_naming_them(tree):
    ignored = snapshot._Ignored(None, str(tree))
    assert ignored.path("data/rows.jsonl")
    assert not ignored.path("src/train.py")
    assert ignored.directory("data")
    assert ignored.report([]) == []  # not even the name of an excluded path is recorded


def test_snapshot_include_cannot_pull_in_excluded(tree):
    from probe.sdk.snapshot import capture_manifest

    m = capture_manifest(str(tree), include=["data/*", "src/*"])
    paths = {e["path"] for e in m["entries"]} | {s["path"] for s in m.get("skipped", [])}
    assert "src/train.py" in paths
    assert not any(p.startswith("data") for p in paths)


def test_log_artifact_checks_folders_and_file_uris(tree, capsys):
    (tree / pc.CONFIG_NAME).write_text("/data/\n")
    pc._CACHE.clear()
    assert Run.log_artifact(object(), "ds", path=str(tree / "data"), reference=True) is None
    assert Run.log_artifact(object(), "ds", uri=f"file://{tree}/data/rows.jsonl") is None
    assert capsys.readouterr().err.count("was not uploaded") == 2


def test_retired_defaults_only_count_inside_an_agent_session(tree, monkeypatch, tmp_path):
    import json as _json

    legacy = tmp_path / "old"
    (legacy / ".probe").mkdir(parents=True)
    (legacy / ".probe" / "config.json").write_text(_json.dumps({"defaults": {"session_state": "off"}}))
    exclusions._view_at = -1.0e9
    assert not exclusions.excluded(legacy / "train.py").excluded  # a training node: runs record
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "11111111-2222-3333-4444-55555555555a")
    exclusions._view_at = -1.0e9
    assert exclusions.excluded(legacy / "train.py").excluded


def test_excluded_reads_are_never_counted_or_queued(tree, monkeypatch, tmp_path):
    """A loader reading an excluded dataset must not fill the run's read list
    (MAX_PATHS) or spend its hashing budget."""
    from probe.sdk import fluent

    monkeypatch.setenv(inputs.READS_ENV, "1")
    for name in (inputs.CHILD_DIR_ENV, inputs.WRITES_ENV, inputs.OUTPUTS_ENV):
        monkeypatch.delenv(name, raising=False)
    inputs._active.clear()
    fluent._current.set(None)
    for i in range(5):
        (tree / "data" / f"part-{i}.jsonl").write_text("x")
    try:
        assert inputs.start("run-excl")
        for i in range(5):
            with open(tree / "data" / f"part-{i}.jsonl") as handle:
                handle.read()
        (tree / "src" / "rows.csv").write_text("a,b")
        with open(tree / "src" / "rows.csv") as handle:
            handle.read()
        target = inputs._active["run-excl"]
        assert target.count == 1
        assert {os.path.basename(p) for p in target.config_excluded} == {f"part-{i}.jsonl" for i in range(5)}
    finally:
        inputs.abandon("run-excl")
        inputs._active.clear()


def test_a_manifest_never_names_an_excluded_path(tree):
    from probe.sdk.snapshot import capture_manifest

    (tree / pc.CONFIG_NAME).write_text("/client-acme/\n")
    (tree / "client-acme" / "node_modules").mkdir(parents=True)
    (tree / "client-acme" / "node_modules" / "x.js").write_text("x")
    pc._CACHE.clear()
    m = capture_manifest(str(tree))
    named = {e["path"] for e in m["entries"]} | {s["path"] for s in m.get("skipped", [])}
    assert not any(p.startswith("client-acme") for p in named)
