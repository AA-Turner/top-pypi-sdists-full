"""Interrupted folder preparation reuses only successful, unchanged paid reads."""

from __future__ import annotations

from collections import Counter
from dataclasses import replace
import json
import stat

import pytest

from probe.cli import backfill as bf
from probe.cli import backfill_evidence as evidence_mod
from probe.cli import backfill_run as runner


def _tail(payload):
    return json.dumps({"type": "result", "result": json.dumps(payload)})


def _plan():
    return {
        "projects": [{"slug": "alpha", "name": "Alpha"}],
        "assignments": [{"path": "a.py", "project": "alpha"}],
        "summary": "One project",
    }


@pytest.fixture
def inputs(tmp_path, monkeypatch):
    folder = tmp_path / "source"
    folder.mkdir()
    work = tmp_path / "work"
    work.mkdir()
    ev = evidence_mod.Evidence(
        root=str(folder),
        files=[evidence_mod.FileEvidence(
            path=str(folder / "a.py"), size=10, mtime=0,
            tier=evidence_mod.Tier.EVIDENCE, sample="train()",
        )],
        clusters=[], sampled_files=1, sampled_bytes=7,
    )
    monkeypatch.setattr(bf, "git_context", lambda *_: None)
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: pytest.fail("Unexpected agent call"))
    return folder, work, ev


def _classify(inputs, *, agent=bf.Agent.CLAUDE, existing=()):
    folder, work, ev = inputs
    return runner.classify(folder, ev, agent=agent, existing=list(existing), work_dir=work)


def test_completed_classification_survives_a_new_context_and_keeps_session(inputs, monkeypatch):
    calls = []
    progress = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(k) or (True, _tail(_plan())))
    with runner.classification_context("same-observed-files"):
        first = _classify(inputs)
    with runner.classification_context(
        "same-observed-files", lambda message, **fields: progress.append((message, fields)),
    ):
        second = _classify(inputs)
    assert len(calls) == 1
    assert first == second
    assert second[2] == calls[0]["session_id"]
    assert [fields["cached"] for _, fields in progress] == [False, True]
    assert all(fields["phase"] == "scanning" and fields["stage"] == "classify"
               for _, fields in progress)
    assert [fields["completed"] for _, fields in progress] == [0, 1]
    assert all(fields["total"] == 1 for _, fields in progress)
    assert stat.S_IMODE((inputs[1] / "prep-cache").stat().st_mode) == 0o700
    assert all(stat.S_IMODE(path.stat().st_mode) == 0o600
               for path in (inputs[1] / "prep-cache").glob("*.json"))


def test_no_context_preserves_uncached_behavior(inputs, monkeypatch):
    calls = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(1) or (True, _tail(_plan())))
    for _ in range(2):
        assert _classify(inputs)[0] is not None
    assert len(calls) == 2
    assert not (inputs[1] / "prep-cache").exists()


@pytest.mark.parametrize("change", ["identity", "evidence", "agent", "existing", "git", "github"])
def test_changed_classification_inputs_are_not_reused(inputs, monkeypatch, change):
    calls = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(1) or (True, _tail(_plan())))
    with runner.classification_context("observed-a"):
        _classify(inputs)
    folder, work, ev = inputs
    if change == "evidence":
        ev = replace(ev, files=[replace(ev.files[0], sample="evaluate()")])
    elif change in {"git", "github"}:
        name = "git-history.md" if change == "git" else "github-context.txt"
        (work / name).write_text("New evidence from repository history")
    with runner.classification_context("observed-b" if change == "identity" else "observed-a"):
        _classify(
            (folder, work, ev),
            agent=bf.Agent.CODEX if change == "agent" else bf.Agent.CLAUDE,
            existing=["existing-project"] if change == "existing" else [],
        )
    assert len(calls) == 2


@pytest.mark.parametrize("failed", [(False, _tail(_plan())), (True, "not a plan")])
def test_failed_or_unparsed_classification_is_not_cached(inputs, monkeypatch, failed):
    results = iter([failed, (True, _tail(_plan()))])
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: next(results))
    with runner.classification_context("observed"):
        assert _classify(inputs)[0] is None
    assert not list((inputs[1] / "prep-cache").glob("*.json"))
    with runner.classification_context("observed"):
        assert _classify(inputs)[0] is not None


@pytest.mark.parametrize("corruption", ["truncated", "wrong_shape", "invalid_plan", "oversized"])
def test_corrupt_cache_is_recomputed(inputs, monkeypatch, corruption):
    calls = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(1) or (True, _tail(_plan())))
    with runner.classification_context("observed"):
        _classify(inputs)
    path, = (inputs[1] / "prep-cache").glob("*.json")
    if corruption == "truncated":
        path.write_text('{"value":')
    elif corruption == "wrong_shape":
        path.write_text("[]")
    elif corruption == "invalid_plan":
        data = json.loads(path.read_text())
        data["value"]["tail"] = _tail({"projects": 12, "assignments": [{}]})
        path.write_text(json.dumps(data))
    else:
        monkeypatch.setattr(runner, "_PREP_CACHE_ENTRY_BYTES", 64)
        path.write_text(" " * 65)
    with runner.classification_context("observed"):
        assert _classify(inputs)[0] is not None
    assert len(calls) == 2


@pytest.mark.parametrize("failed_phase", ["survey", "assign"])
def test_restart_reuses_completed_slices_after_second_slice_fails(inputs, monkeypatch, failed_phase):
    folder, work, ev = inputs
    rows = [json.dumps({"path": f"{name}.py", "sample": name}) for name in ("a", "b", "c")]
    monkeypatch.setattr(evidence_mod, "chunk_lines", lambda _: [[row] for row in rows])
    calls = Counter()
    failing = True
    progress = []

    def agent(folder, prompt, **kwargs):
        heading = kwargs["heading"]
        phase = "survey" if heading.startswith("Reading") else (
            "assign" if heading.startswith("Filing") else "name"
        )
        index = next((i for i in (1, 2, 3) if f"slice {i} of 3" in heading), 0)
        calls[phase, index] += 1
        if failing and phase == failed_phase and index == 2:
            return False, "connection lost"
        if phase == "survey":
            return True, _tail({"findings": [{"work": f"slice {index}"}]})
        if phase == "name":
            return True, _tail({"projects": _plan()["projects"]})
        return True, _tail({"assignments": [{"path": f"{index}.py", "project": "alpha"}]})

    monkeypatch.setattr(bf, "launch_agent", agent)
    with runner.classification_context("observed"):
        plan, detail = runner.classify_chunked(
            folder, ev, agent=bf.Agent.CLAUDE, existing=[], work_dir=work,
        )
    assert plan is None
    assert "slice 2 of 3" in detail and "connection lost" in detail
    failing = False
    with runner.classification_context(
        "observed", lambda message, **fields: progress.append((message, fields)),
    ):
        plan, _ = runner.classify_chunked(
            folder, ev, agent=bf.Agent.CLAUDE, existing=[], work_dir=work,
        )
    assert plan is not None
    assert len(plan.assignments) == 3
    assert calls[failed_phase, 2] == runner.PASS_ATTEMPTS + 1
    assert calls["survey", 1] == 1
    assert calls["assign", 1] == 1
    assert calls["assign", 3] == 1
    assert calls["name", 0] == 1
    assert all(fields["phase"] == "scanning" and fields["total"] == 7
               for _, fields in progress)
    completed = [fields["completed"] for _, fields in progress]
    assert completed == sorted(completed) and completed[-1] == 7
    assert any(fields["cached"] and fields["stage"] == failed_phase
               for _, fields in progress)


@pytest.mark.parametrize("key", ["projects", "assignments", "findings"])
def test_unusable_chunk_results_are_not_saved(inputs, monkeypatch, key):
    calls = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(1) or (True, _tail({key: []})))
    folder, work, _ = inputs
    for _ in range(2):
        with runner.classification_context("observed"):
            runner._run_pass(folder, "prompt", agent=bf.Agent.CLAUDE, heading="Reading",
                             work_dir=work, total=1, key=key)
    assert len(calls) == 2
    assert not list((work / "prep-cache").glob("*.json"))


@pytest.mark.parametrize("change", [None, "feedback", "evidence", "session", "identity", "agent"])
def test_revision_cache_tracks_correction_inputs_and_returns_session(inputs, monkeypatch, change):
    calls = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(k) or (True, _tail(_plan())))
    folder, work, ev = inputs
    with runner.classification_context("observed-a"):
        first = runner.revise(folder, ev, "Use Alpha", agent=bf.Agent.CLAUDE,
                              session_id="original-session", work_dir=work)
    if change == "evidence":
        ev = replace(ev, files=[replace(ev.files[0], sample="evaluate()")])
    with runner.classification_context("observed-b" if change == "identity" else "observed-a"):
        second = runner.revise(
            folder, ev, "Use Beta" if change == "feedback" else "Use Alpha",
            agent=bf.Agent.CODEX if change == "agent" else bf.Agent.CLAUDE,
            session_id="another-session" if change == "session" else "original-session",
            work_dir=work,
        )
    assert len(calls) == (1 if change is None else 2)
    if change is None:
        assert second == first
        assert second[2] == "original-session"


def test_nested_context_restores_outer_identity_after_exception(inputs, monkeypatch):
    calls = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(1) or (True, _tail(_plan())))
    with runner.classification_context("outer"):
        _classify(inputs)
        with pytest.raises(RuntimeError), runner.classification_context("inner"):
            _classify(inputs)
            raise RuntimeError("interrupted")
        _classify(inputs)
    assert len(calls) == 2
    _classify(inputs)
    assert len(calls) == 3


@pytest.mark.parametrize("agent", [bf.Agent.CLAUDE, bf.Agent.CODEX])
def test_cold_revision_keeps_its_new_session_when_reused(inputs, monkeypatch, agent):
    calls = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(k) or (True, _tail(_plan())))
    folder, work, ev = inputs
    results = []
    for _ in range(2):
        with runner.classification_context("observed"):
            results.append(runner.revise(folder, ev, "Use Alpha", agent=agent,
                                         session_id=None, work_dir=work))
    assert len(calls) == 1
    assert results[0] == results[1]
    assert results[1][2] == calls[0]["session_id"]
    assert (results[1][2] is not None) == (agent is bf.Agent.CLAUDE)


def test_failed_revision_retries_without_reusing_its_failed_output(inputs, monkeypatch):
    results = iter([(False, _tail(_plan())), (True, _tail(_plan()))])
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: next(results))
    folder, work, ev = inputs
    with runner.classification_context("observed"):
        assert runner.revise(folder, ev, "Use Alpha", agent=bf.Agent.CLAUDE,
                             session_id="original-session", work_dir=work)[0] is None
    assert not list((work / "prep-cache").glob("*.json"))
    with runner.classification_context("observed"):
        assert runner.revise(folder, ev, "Use Alpha", agent=bf.Agent.CLAUDE,
                             session_id="original-session", work_dir=work)[0] is not None


def test_cache_write_failure_does_not_discard_the_agent_result(inputs, monkeypatch):
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: (True, _tail(_plan())))
    (inputs[1] / "prep-cache").write_text("not a directory")
    with runner.classification_context("observed"):
        assert _classify(inputs)[0] is not None


def test_old_cache_entries_are_evicted_at_the_count_bound(inputs, monkeypatch):
    calls = []
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: calls.append(1) or (True, _tail(_plan())))
    monkeypatch.setattr(runner, "_PREP_CACHE_ENTRIES", 2)
    for identity in ("first", "second", "third"):
        with runner.classification_context(identity):
            _classify(inputs)
    assert len(list((inputs[1] / "prep-cache").glob("*.json"))) == 2
    with runner.classification_context("third"):
        _classify(inputs)
    assert len(calls) == 3
    with runner.classification_context("first"):
        _classify(inputs)
    assert len(calls) == 4


def test_cache_total_bytes_are_bounded(inputs, monkeypatch):
    monkeypatch.setattr(bf, "launch_agent", lambda *a, **k: (True, _tail(_plan())))
    with runner.classification_context("first"):
        _classify(inputs)
    path, = (inputs[1] / "prep-cache").glob("*.json")
    limit = path.stat().st_size + 64
    monkeypatch.setattr(runner, "_PREP_CACHE_BYTES", limit)
    with runner.classification_context("second"):
        _classify(inputs)
    entries = list((inputs[1] / "prep-cache").glob("*.json"))
    assert sum(path.stat().st_size for path in entries) <= limit
    assert len(entries) == 1
