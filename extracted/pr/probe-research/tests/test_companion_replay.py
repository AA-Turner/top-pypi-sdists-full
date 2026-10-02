"""The companion replay bench, driven with a canned model: no network, no key.

Pins the mechanics a bench number depends on: the virtual clock releases the
transcript at its recorded pace, the worker takes the lease at the handover, a
write lands in the in-memory Probe (and is visible to a later read), the answer
key scores it, and the compare verdict is strict.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
TAP_ROOT = AGENT / "plugins" / "probe-research-tap"
EVALS = AGENT / "evals" / "companion"

PROJECT = "11111111-1111-4111-8111-111111111111"
SVM = "22222222-2222-4222-8222-222222222222"
PCA_EXP = "33333333-3333-4333-8333-333333333333"
CHOSEN = "44444444-4444-4444-8444-444444444444"
PCA_RUN = "55555555-5555-4555-8555-555555555555"
FILE_ID = "66666666-6666-4666-8666-666666666666"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"companion_{name}", EVALS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


replay = _load("replay")
score = _load("score")


def _line(kind: str, at: dt.datetime, content, **extra) -> str:
    message = {"role": kind, "content": content}
    if kind == "assistant":
        message["stop_reason"] = extra.pop("stop_reason", "tool_use")
    return json.dumps({"type": kind, "timestamp": at.isoformat().replace("+00:00", "Z"),
                       "cwd": "/tmp", "message": message, **extra})


def _fixture(tmp_path: Path) -> Path:
    t0 = dt.datetime(2026, 9, 23, 8, 0, tzinfo=dt.timezone.utc)
    s = dt.timedelta(seconds=1)
    rows = [
        _line("user", t0, "<command-name>/probe-research:probe</command-name>\n<command-args>daemon</command-args>"),
        _line("assistant", t0 + 30 * s, [{"type": "tool_use", "id": "c1", "name": "Bash",
                                          "input": {"command": f"probe exec --project {PROJECT} -- python run.py"}}]),
        _line("user", t0 + 40 * s, [{"type": "tool_result", "tool_use_id": "c1",
                                     "content": f"val_loss 0.42\nprobe run: https://x/runs/{CHOSEN}"}]),
        _line("assistant", t0 + 60 * s,
              [{"type": "text", "text": f"The SVM (C=10, gamma=0.001) beats logistic regression: 0.9889 vs 0.9603. project:{PROJECT}"}],
              stop_reason="end_turn"),
    ]
    raw = ("\n".join(rows) + "\n").encode()
    fx = tmp_path / "fx"
    fx.mkdir()
    (fx / "transcript.jsonl").write_bytes(raw)
    first = len(rows[0]) + 1
    (fx / "meta.json").write_text(json.dumps({
        "session_id": "aaaaaaaa-0000-4000-8000-000000000001", "source": "claude_code",
        "handover_offset": first, "handover_time": t0.timestamp() + 2,
        "stop_offsets": [len(raw)], "cwd": str(tmp_path), "project": PROJECT,
    }))
    run = {"id": CHOSEN, "name": "best", "tags": [], "notes": None, "project_id": SVM}
    proj = {"id": PROJECT, "name": "digits", "description": None, "notes": None, "notes_version": 0}
    (fx / "reads.json").write_text(json.dumps({
        f"/v1/runs/{CHOSEN}": run,
        f"/v1/runs/{CHOSEN}/sub-notes": {"sub_notes": [], "limit_count": 20},
        f"/v1/runs/{CHOSEN}/artifacts": [{"id": FILE_ID, "name": "results/table.md", "kind": "file",
                                          "content_hash": "0" * 64, "notes": None}],
        f"/v1/runs/{CHOSEN}/edges": [],
        f"/v1/projects/{PROJECT}": proj,
        f"/v1/projects/{PROJECT}/sub-notes": {"sub_notes": [], "limit_count": 20},
        f"/v1/projects/{PROJECT}/artifacts": [],
        f"/v1/projects/{PROJECT}/papers": [],
    }))
    return fx


class CannedGateway:
    """Answers the first cycle that sees the decision with a project note."""

    def __init__(self) -> None:
        self.calls = 0

    def complete(self, messages, *, max_tokens=None, timeout=120):
        self.calls += 1
        seen = "\n".join(m["content"] for m in messages)
        proposals = []
        found = re.search(r"\[assistant @(\d+)\]\nThe SVM", seen)
        if found:
            at = int(found.group(1))
            proposals.append({
                "kind": "note", "target": {"type": "project", "id": PROJECT},
                "title": "SVM beats logistic regression",
                "body": "Chosen: RBF SVM, C=10, gamma=0.001: CV 0.9889 against 0.9603 for logistic regression.",
                "evidence": {"from": at, "to": at},
            })
        return {"content": json.dumps({"proposals": proposals}), "model": "canned",
                "usage": {"input_tokens": 100, "output_tokens": 10}, "finish_reason": "stop"}


def test_the_replay_releases_the_transcript_at_its_pace_and_records_writes(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    fx = _fixture(tmp_path)
    gateway = CannedGateway()
    result = replay.replay(fx, TAP_ROOT, gateway=gateway, tail_seconds=120, log=lambda *_: None)
    assert gateway.calls >= 1, result["errors"]
    assert result["cycles"], "the worker never ran a cycle"
    # Everything before the handover was the agent's: no transcript cycle starts
    # before it (a conclusions cycle spans the whole session by design; its
    # evidence is still held to the daemon's ranges).
    handover = json.loads((fx / "meta.json").read_text())["handover_offset"]
    reading = [c for c in result["cycles"] if not (c["outcome"] or "").startswith("conclusions")]
    assert reading and all(c["byte_start"] >= handover for c in reading)
    assert result["tokens"]["input"] == 100 * len([c for c in result["cycles"] if c["input_tokens"]])
    # The note the canned model proposed was decided, published into the overlay,
    # and scores as the headline on the right entity.
    assert [p["status"] for p in result["proposals"]] == ["published"], result["proposals"]
    assert any(n["target"][1] == PROJECT and "0.9889" in n["body"] for n in result["notes"])
    key = dict(EXPECTED, chosen_runs=[CHOSEN])
    assert score.score(result, key, json.loads((fx / "reads.json").read_text()))["checks"]["E1 headline"]


def test_the_overlay_serves_its_own_writes_back():
    import types

    errors = types.SimpleNamespace(Rejected=type("Rejected", (Exception,), {
        "__init__": lambda self, status, detail=None: Exception.__init__(self, status)}),
        Retryable=RuntimeError)
    api = replay.RecordingApi({
        f"/v1/projects/{PROJECT}": {"id": PROJECT, "description": None, "tags": []},
        f"/v1/projects/{PROJECT}/sub-notes": {"sub_notes": []},
        f"/v1/runs/{CHOSEN}/artifacts": [{"id": FILE_ID, "name": "t.md", "kind": "file", "notes": None}],
        f"/v1/runs/{PCA_RUN}/edges": [],
    }, errors=errors, gateway=None)
    api.request("POST", f"/v1/projects/{PROJECT}/sub-notes", {"title": "t", "body": "b"})
    assert api.get(f"/v1/projects/{PROJECT}/sub-notes")["sub_notes"][0]["title"] == "t"
    api.request("PATCH", f"/v1/projects/{PROJECT}", {"description": "digits study"})
    assert api.get(f"/v1/projects/{PROJECT}")["description"] == "digits study"
    api.request("PATCH", f"/v1/artifacts/{FILE_ID}", {"notes": "the results table"})
    assert api.get(f"/v1/runs/{CHOSEN}/artifacts")[0]["notes"] == "the results table"
    api.request("POST", "/v1/edges", {"source_type": "run", "source_id": PCA_RUN, "relation": "derived_from",
                                      "target_type": "run", "target_id": CHOSEN})
    assert api.get(f"/v1/runs/{PCA_RUN}/edges")[0]["target_id"] == CHOSEN
    with pytest.raises(Exception):
        api.get("/v1/runs/77777777-7777-4777-8777-777777777777")
    assert api.missing_reads == ["/v1/runs/77777777-7777-4777-8777-777777777777"]


def _result(notes=(), patches=None, edges=(), file_notes=None, writes=(), label="x", fixture="fx"):
    return {"label": label, "fixture": fixture, "notes": list(notes), "entity_patches": patches or {},
            "edges": list(edges), "file_notes": file_notes or {}, "writes": list(writes), "proposals": [],
            "tokens": {"input": 0, "output": 0}, "cycles": [], "errors": []}


EXPECTED = {"project": PROJECT, "svm_experiment": SVM, "pca_experiment": PCA_EXP,
            "chosen_runs": [CHOSEN], "pca_run": PCA_RUN, "superseded_run": None}
READS = {f"/v1/runs/{CHOSEN}/artifacts": [{"id": FILE_ID, "kind": "file"}, {"id": "c", "kind": "code"}]}


def test_the_answer_key_needs_the_same_facts_on_the_right_entity():
    good = {"target": ["project", PROJECT], "title": "Decision",
            "body": "RBF SVM (C=10, gamma=0.001) wins: CV 0.9889 vs 0.9603 for logistic regression. "
                    "Caveat: one split only. PCA to 32 components was dropped (0.9882)."}
    key = dict(EXPECTED, file_notes_parity={"fraction": 1.0, "tolerance": 0.1})
    s = score.score(_result(notes=[good], patches={f"/v1/projects/{PROJECT}": {"description": "d"}},
                            edges=[{"source_id": PCA_RUN, "target_id": CHOSEN, "relation": "derived_from"}],
                            file_notes={FILE_ID: "the table"}), key, READS)
    assert s["checks"] == {"E1 headline": True, "E2 pca": True, "E3 caveat": True, "E4 project": True,
                           "E7 files": True}
    assert s["metrics"] == {"E5 lineage": True, "E6 describe": True}, "reported, never counted"
    # The same text on an unrelated run proves nothing.
    elsewhere = dict(good, target=["run", "99999999-9999-4999-8999-999999999999"])
    s = score.score(_result(notes=[elsewhere]), EXPECTED, READS)
    assert not s["checks"]["E1 headline"] and not s["checks"]["E4 project"]
    # The headline needs both numbers and the chosen config, not just "SVM wins".
    vague = dict(good, body="The SVM wins.")
    assert not score.score(_result(notes=[vague]), EXPECTED, READS)["checks"]["E1 headline"]
    # The chosen config may be named by its run name instead of written out...
    named = dict(good, body="`svm-C10-gamma-0.001` won: CV 0.9889 vs 0.9603 for logistic regression.")
    assert score.score(_result(notes=[named]), EXPECTED, READS)["checks"]["E1 headline"]
    # ...but not by a different setting that merely contains the digits.
    other = dict(good, body="`svm-C100-gamma-0.001` won: CV 0.9889 vs 0.9603 for logistic regression.")
    assert not score.score(_result(notes=[other]), EXPECTED, READS)["checks"]["E1 headline"]


def test_compare_is_strict():
    def row(label, checks, files=0.0, fixture="fx"):
        return {"label": label, "fixture": fixture, "checks": checks, "passed": sum(checks.values()),
                "applicable": len(checks), "file_note_fraction": files, "notes": 0, "writes": 0,
                "held": {}, "tokens": {"input": 0, "output": 0}, "cycles": 0, "errors": 0}

    both = {"E1 headline": True, "E2 pca": True}
    one = {"E1 headline": True, "E2 pca": False}
    other = {"E1 headline": False, "E2 pca": True}
    better, lines = score.compare(score.summarize([row("base", one), row("new", both)]), "base", "new")
    assert better and lines[-1] == "VERDICT: BETTER"
    # Same total, but a check the base always passed is lost: not better.
    better, _ = score.compare(score.summarize([row("base", one), row("new", other)]), "base", "new")
    assert not better
    # A tie on checks is broken by more files noted, and only by that.
    assert score.compare(score.summarize([row("base", one), row("new", one, files=0.5)]), "base", "new")[0]
    assert not score.compare(score.summarize([row("base", one), row("new", one)]), "base", "new")[0]
    # Better on one fixture and missing on another: not better.
    better, lines = score.compare(score.summarize([row("base", one), row("new", both), row("base", one, fixture="gx")]),
                                  "base", "new")
    assert not better and "COMPARE gx: missing a label" in lines


def test_a_replay_puts_back_the_process_state_it_changes(tmp_path, monkeypatch):
    import os

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "mine"))
    before = {n for n in sys.modules if n == "tap" or n.startswith("tap.")}
    replay.replay(_fixture(tmp_path), TAP_ROOT, gateway=CannedGateway(), tail_seconds=60, log=lambda *_: None)
    assert os.environ["XDG_STATE_HOME"] == str(tmp_path / "mine")
    assert {n for n in sys.modules if n == "tap" or n.startswith("tap.")} == before


def test_a_fixture_can_carry_its_own_numbers_and_skip_a_check_that_does_not_apply():
    key = dict(EXPECTED, numbers={"svm": "0.9889", "logreg": "0.9701", "pca": "0.9882"}, describe=False)
    good = {"target": ["project", PROJECT], "title": "Decision",
            "body": "RBF SVM (C=10, gamma=0.001) wins: CV 0.9889 vs 0.9701 for logistic regression. "
                    "Caveat: one split only. PCA to 32 components: 0.9882."}
    s = score.score(_result(notes=[good]), key, READS)
    assert s["checks"]["E1 headline"] and s["checks"]["E2 pca"] and "E6 describe" not in s["checks"]
    # The default numbers no longer count for this fixture.
    old = dict(good, body=good["body"].replace("0.9701", "0.9603"))
    assert not score.score(_result(notes=[old]), key, READS)["checks"]["E1 headline"]


def test_a_frozen_fixture_drops_the_tags_the_live_daemon_wrote(tmp_path, monkeypatch):
    fixtures = _load("fixtures")
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
    ledger = tmp_path / "probe" / "companion"
    ledger.mkdir(parents=True)
    import sqlite3

    conn = sqlite3.connect(ledger / "s1.sqlite")
    conn.execute("CREATE TABLE proposals (kind TEXT, target_type TEXT, target_id TEXT, payload TEXT, status TEXT)")
    conn.executemany("INSERT INTO proposals VALUES (?, ?, ?, ?, ?)", [
        ("tag", "run", CHOSEN, json.dumps({"add": ["abandoned"]}), "published"),
        ("tag", "run", PCA_RUN, json.dumps({"add": ["abandoned"]}), "held"),  # never written
    ])
    conn.commit()
    conn.close()
    drop = fixtures.daemon_tags("s1")
    assert drop == {CHOSEN: {"abandoned"}} and fixtures.daemon_tags("no-such-session") == {}
    row = fixtures._scrub_entity({"tags": ["prod-candidate", "abandoned"], "notes": "x"}, parent=False,
                                 drop_tags=drop[CHOSEN])
    assert row["tags"] == ["prod-candidate"] and row["notes"] is None  # the agent's own tag stays


def test_lineage_to_a_run_whose_output_the_pca_run_read_counts():
    other = "77777777-7777-4777-8777-777777777777"
    edge = {"source_id": PCA_RUN, "target_id": other, "relation": "derived_from"}
    assert not score.score(_result(edges=[edge]), EXPECTED, READS)["metrics"]["E5 lineage"]
    key = dict(EXPECTED, pca_parents=[other])
    assert score.score(_result(edges=[edge]), key, READS)["metrics"]["E5 lineage"]
