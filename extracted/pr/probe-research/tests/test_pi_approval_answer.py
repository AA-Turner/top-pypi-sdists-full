"""An answer pi's dialog writes is one the Probe daemon acts on.

The pi extension (`plugins/probe-research-pi/src/core/approvals.ts`) answers the
daemon's held questions itself, in pi's own dialog, by writing the Board's
answer file. `fixtures/pi_approval_answer.json` holds a held request (made by
`Board.hold`) and the two files that writer produces for it; the pi package's
vitest asserts its writer produces them byte for byte. This side proves the
Board and the worker take them: `Board.answer` writes the same dict for the
same pick, `take_answer` hands it back, and the worker settles a yes by running
the held action and a no by refusing it.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from probe.daemon import approvals as appr

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "pi_approval_answer.json").read_text(encoding="utf-8"))
REQUEST = FIXTURE["request"]
SID = REQUEST["session_id"]


def _board(root: Path, at: float) -> appr.Board:
    board = appr.Board(root, clock=lambda: at)
    (root / "requests" / f"{REQUEST['id']}.json").write_text(json.dumps(REQUEST, indent=1), encoding="utf-8")
    return board


@pytest.mark.parametrize("pick", ["yes", "no"])
def test_the_board_writes_the_same_answer_for_the_same_pick(tmp_path, pick):
    expected = FIXTURE[pick]
    board = _board(tmp_path, expected["at"])
    assert board.answer(REQUEST["id"], expected["choice"], channel=expected["channel"]) is True
    written = json.loads((tmp_path / "answers" / f"{REQUEST['id']}.json").read_text(encoding="utf-8"))
    assert written == expected


@pytest.mark.parametrize("pick", ["yes", "no"])
def test_take_answer_accepts_what_pi_writes(tmp_path, pick):
    expected = FIXTURE[pick]
    board = _board(tmp_path, expected["at"])
    (tmp_path / "answers" / f"{REQUEST['id']}.json").write_text(json.dumps(expected, indent=1), encoding="utf-8")
    taken = board.take_answer(REQUEST["id"])
    assert taken == expected
    assert taken["answer"] == (appr.YES if pick == "yes" else appr.NO)
    assert (taken["choice"] == REQUEST["question"]["yes_label"]) == (pick == "yes")
    # Stamped inside the request's life, or the worker would ignore it.
    assert REQUEST["asked_at"] <= expected["at"] <= REQUEST["expires_at"]


# ---------------------------------------------------------------------------
# The worker's settle path, on the same request and the same answer files.
# It needs the daemon's AI libraries (the `daemon` extra); the Board tests
# above do not, so the skip is per test, not per module.
# ---------------------------------------------------------------------------


class _Replay:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        return 0, json.dumps({"ok": True})


def _worker(tmp_path: Path, monkeypatch, pick: str):
    pytest.importorskip("pydantic_ai")
    from probe.daemon import lease
    from probe.daemon import worker as worker_mod

    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "no-config.json"))
    monkeypatch.delenv("PROBE_DAEMON_KEY", raising=False)
    monkeypatch.setenv("PROBE_DAEMON_MCP", "0")
    lease.sessions_dir().mkdir(parents=True, exist_ok=True)
    (lease.sessions_dir() / f"{SID}.state").write_text("daemon")
    work = tmp_path / "home" / "work"
    work.mkdir(parents=True)
    transcript = tmp_path / f"{SID}.jsonl"
    transcript.write_text("")
    at = FIXTURE[pick]["at"]
    w = worker_mod.Worker(worker_mod.Session(SID, transcript, work, "pi", home=tmp_path / "home"),
                          clock=lambda: at, replay=_Replay())
    root = appr.approvals_dir()
    (root / "requests" / f"{REQUEST['id']}.json").write_text(json.dumps(REQUEST, indent=1), encoding="utf-8")
    (root / "answers" / f"{REQUEST['id']}.json").write_text(json.dumps(FIXTURE[pick], indent=1), encoding="utf-8")
    return w


def test_the_worker_runs_the_held_action_on_pis_yes(tmp_path, monkeypatch):
    w = _worker(tmp_path, monkeypatch, "yes")
    from probe.daemon import tools

    async def same_facts(deps, parsed):
        return REQUEST["facts"]

    monkeypatch.setattr(tools, "deletion_facts", same_facts)
    asyncio.run(w.settle_answers())
    settled = w.board.get(REQUEST["id"])
    assert settled.state == appr.APPROVED
    assert settled.channel == "pi-dialog"
    assert w.replay.calls == [REQUEST["held"]["argv"]]


def test_the_worker_refuses_the_held_action_on_pis_no(tmp_path, monkeypatch):
    w = _worker(tmp_path, monkeypatch, "no")
    asyncio.run(w.settle_answers())
    settled = w.board.get(REQUEST["id"])
    assert settled.state == appr.DENIED
    assert settled.channel == "pi-dialog"
    assert settled.outcome == f"no ({REQUEST['question']['no_label']!r})"
    assert w.replay.calls == []
