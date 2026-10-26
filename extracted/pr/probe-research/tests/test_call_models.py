"""A Codex or Kimi Code call's usage line names no model; an earlier line of the
same file does. The journal keeps each session's call models with its cursor
(`session_journal.CALL_MODELS_STATE`), so a model is never lost to a restart,
never taken from another session's file, and never pushed out by newer calls.
A Kimi compaction's tokens ship too (its `usage.record`: no step.end has them).
"""

from __future__ import annotations

import importlib
import json
import shutil
from contextlib import closing
from pathlib import Path

import pytest

from probe.tap_core import codex_sanitize, kimi_sanitize
from probe.tap_core import session_journal as sj
from probe.tap_core.sanitize import CallModels, call_models
from tests.test_backfill_transcripts_upload import FakeWire

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "kimi_code" / "sessions" / "wd_proj_846899122802"
TUI = FIXTURES / "session_0d2f2223-e34e-4cd1-87e3-b8d8d39aa229"  # three turns, then /compact
A = "aaaaaaaa-1111-4111-8111-111111111111"
B = "bbbbbbbb-2222-4222-8222-222222222222"


@pytest.fixture(autouse=True)
def journal_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("PROBE_TRANSCRIPT_STATE_DIR", str(tmp_path / "state"))
    return tmp_path


def _line(record: dict) -> bytes:
    return (json.dumps(record) + "\n").encode()


def _request(turn: int, step: int, model: str) -> dict:
    return {"type": "llm.request", "agentId": "main", "kind": "loop", "model": model, "modelAlias": "k",
            "turnStep": f"{turn}.{step}", "time": 1791169900000 + step}


def _part(turn: int, step: int) -> dict:
    return {"type": "context.append_loop_event", "agentId": "main", "time": 1791169900100 + step,
            "event": {"type": "content.part", "turnId": str(turn), "step": step,
                      "part": {"type": "text", "text": "ok"}}}


def _end(turn: int, step: int, output: int = 10) -> dict:
    return {"type": "context.append_loop_event", "agentId": "main", "time": 1791169900200 + step,
            "event": {"type": "step.end", "turnId": str(turn), "step": step,
                      "usage": {"inputOther": 100, "output": output, "inputCacheRead": 0, "inputCacheCreation": 0}}}


def _usage(body: bytes) -> dict[str, tuple[str | None, dict]]:
    """`inference_id -> (model, usage)` of every usage event a batch carries."""
    out = {}
    for item in json.loads(body)["events"]:
        raw = item["raw"]
        if "usage" in raw:
            out[raw["inference_id"]] = (raw["message"].get("model"), raw["usage"])
    return out


def _wire_file(root: Path, session_id: str, records: list[dict]) -> Path:
    path = root / "sessions" / "wd" / f"session_{session_id}" / "agents" / "main" / "wire.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(_line(r) for r in records))
    return path


def _append(path: Path, records: list[dict]) -> None:
    with path.open("ab") as handle:
        handle.write(b"".join(_line(r) for r in records))


class Sessions:
    """One journal process staging and delivering sessions of one harness."""

    def __init__(self, source: str) -> None:
        self.wire = FakeWire(source=source)
        self.source = source
        self.journal = sj.Journal(self.wire.base_url, "synthetic", source)

    def batch(self, session_id: str, path: Path) -> bytes:
        self.journal.ensure(session_id, path, self.wire.receipts(session_id), historical=False, cwd="/w")
        body = self.journal.stage(session_id, cwd="/w")
        assert body is not None
        assert self.journal.deliver(session_id, self.wire)
        return body

    def close(self) -> None:
        self.journal.close()


# --------------------------------------------------------------- Kimi Code


def test_a_session_counts_every_call_its_compaction_included(journal_dir):
    """The fixture session: four steps of 100/10 and a /compact of 100/10."""
    records = [json.loads(line) for line in (TUI / "agents/main/wire.jsonl").read_text().splitlines()]
    calls = [r for r in records if r["type"] == "usage.record"]
    with call_models(CallModels()):
        events = [kimi_sanitize.sanitize_event(r) for r in records]
    usage = [e["usage"] for e in events if isinstance(e, dict) and "usage" in e]
    assert sum(u["input_tokens"] for u in usage) == sum(c["usage"]["inputOther"] for c in calls) == 500
    assert sum(u["output_tokens"] for u in usage) == sum(c["usage"]["output"] for c in calls) == 50
    path = journal_dir / "sessions" / "wd" / TUI.name / "agents" / "main" / "wire.jsonl"
    path.parent.mkdir(parents=True)
    shutil.copy(TUI / "agents/main/wire.jsonl", path)
    sessions = Sessions("kimi_code")
    with closing(sessions.journal):
        shipped = _usage(sessions.batch(TUI.name.removeprefix("session_"), path))
    assert sum(u["input_tokens"] for _, u in shipped.values()) == 500
    assert {model for model, _ in shipped.values()} == {"mock-model"}


def test_two_sessions_never_share_a_steps_model(journal_dir):
    """Both files have a step 0.1; each keeps its own model, read in turn."""
    a = _wire_file(journal_dir, A, [_request(0, 1, "kimi-a")])
    b = _wire_file(journal_dir, B, [_request(0, 1, "kimi-b")])
    sessions = Sessions("kimi_code")
    with closing(sessions.journal):
        sessions.batch(A, a)
        sessions.batch(B, b)
        _append(a, [_part(0, 1), _end(0, 1)])
        _append(b, [_part(0, 1), _end(0, 1)])
        assert _usage(sessions.batch(A, a))["0:1"][0] == "kimi-a"
        assert _usage(sessions.batch(B, b))["0:1"][0] == "kimi-b"


def test_a_restart_between_a_request_and_its_usage_keeps_the_model(journal_dir):
    path = _wire_file(journal_dir, A, [_request(0, 1, "kimi-a"), _part(0, 1)])
    first = Sessions("kimi_code")
    first.batch(A, path)
    first.close()
    importlib.reload(kimi_sanitize)  # a new process: nothing in memory
    _append(path, [_end(0, 1)])
    second = Sessions("kimi_code")
    with closing(second.journal):
        assert _usage(second.batch(A, path))["0:1"][0] == "kimi-a"


def test_models_not_saved_at_the_cursor_are_read_back_from_the_file(journal_dir):
    """A session an older tap left (no saved models): read back from the file."""
    path = _wire_file(journal_dir, A, [_request(0, 1, "kimi-a"), _part(0, 1)])
    sessions = Sessions("kimi_code")
    with closing(sessions.journal):
        sessions.batch(A, path)
        state = sessions.journal.get(A)
        assert state[sj.CALL_MODELS_STATE]["models"] == {"0:1": "kimi-a"}
        state.pop(sj.CALL_MODELS_STATE)
        with sessions.journal.transaction():
            sessions.journal._save(state)
        _append(path, [_end(0, 1)])
        assert _usage(sessions.batch(A, path))["0:1"][0] == "kimi-a"
        assert sessions.journal.get(A)[sj.CALL_MODELS_STATE]["models"] == {}, "dropped once used"


def test_many_newer_calls_never_push_out_a_waiting_model(journal_dir):
    path = _wire_file(journal_dir, A, [_request(0, 1, "kimi-a")])
    other = _wire_file(journal_dir, B, [r for s in range(1, 700) for r in (_request(0, s, "kimi-b"), _end(0, s))])
    sessions = Sessions("kimi_code")
    with closing(sessions.journal):
        sessions.batch(A, path)
        while sessions.journal.get(B) is None or sessions.journal.get(B)["source_byte_end"] < other.stat().st_size:
            sessions.batch(B, other)
        _append(path, [_end(0, 1)])
        assert _usage(sessions.batch(A, path))["0:1"][0] == "kimi-a"


# --------------------------------------------------------------------- Codex


def _rollout(path: Path, records: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    _append(path, records)
    return path


def _turn_context(turn: str, model: str) -> dict:
    return {"timestamp": "2026-10-25T21:40:51Z", "type": "turn_context", "payload": {"turn_id": turn, "model": model}}


def _codex_usage(turn: str, output: int) -> dict:
    return {"timestamp": "2026-10-25T21:41:00Z", "type": "token_usage_record",
            "payload": {"turn_id": turn, "turn_token_usage": {"input_tokens": 100, "cached_input_tokens": 40,
                                                              "output_tokens": output}}}


def _codex_message() -> dict:
    return {"timestamp": "2026-10-25T21:40:55Z", "type": "response_item",
            "payload": {"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": "hi"}]}}


def test_a_codex_turns_model_survives_a_restart_and_ends_with_the_turn(journal_dir):
    path = _rollout(journal_dir / "codex" / f"rollout-x-{A}.jsonl", [_turn_context("t1", "gpt-6.1"), _codex_message()])
    first = Sessions("codex")
    first.batch(A, path)
    first.close()
    importlib.reload(codex_sanitize)
    _append(path, [_codex_usage("t1", 7)])
    second = Sessions("codex")
    with closing(second.journal):
        assert _usage(second.batch(A, path))["turn:t1"][0] == "gpt-6.1"
        _append(path, [{"type": "event_msg", "payload": {"type": "task_complete", "turn_id": "t1"}},
                       _codex_message()])
        second.batch(A, path)
        assert second.journal.get(A)[sj.CALL_MODELS_STATE]["models"] == {}, "the turn ended"


def test_a_codex_model_is_read_back_when_none_is_saved(journal_dir):
    path = _rollout(journal_dir / "codex" / f"rollout-x-{B}.jsonl", [_turn_context("t2", "gpt-6.1"), _codex_message()])
    sessions = Sessions("codex")
    with closing(sessions.journal):
        sessions.batch(B, path)
        state = sessions.journal.get(B)
        state.pop(sj.CALL_MODELS_STATE)
        with sessions.journal.transaction():
            sessions.journal._save(state)
        _append(path, [_codex_usage("t2", 9)])
        assert _usage(sessions.batch(B, path))["turn:t2"][0] == "gpt-6.1"
