"""The pin (plan writer-owns-summary §3.5, D6): the last summary the writer
loaded with `probe summary checkout` comes back once, at the start of the next
run's new message, when lean history or a compaction dropped the tool result
that showed it; never while the conversation still shows it, and never as a
per-request tail.

Same seams as test_daemon_conversation.py: Pydantic AI's FunctionModel, `probe`
commands answered by a replay, a real chat log.
"""

from __future__ import annotations

import asyncio
import json

import pytest

pytest.importorskip("pydantic_ai")
pytest.importorskip("pydantic_ai_harness")

from pydantic_ai.models.function import FunctionModel  # noqa: E402

from probe.daemon import model as model_mod  # noqa: E402
from probe.daemon import tools  # noqa: E402
from probe.daemon import worker as worker_mod  # noqa: E402
from tests.test_daemon_conversation import (  # noqa: E402,F401 -- `_isolated` is an autouse fixture
    Replay,
    Script,
    _append_turn,
    _compacting,
    _isolated,
    _live,
    _text,
    _worker,
)

TEXT = "Does a cosine decay beat a constant LR?\n\n**Where it stands (Oct 15):** B2decay 48.8 (sft-b2decay-3).\n"
HEADER = "# Summary of willow you loaded (v3)"


class CheckoutReplay(Replay):
    """`probe summary checkout` prints the checkout's JSON, as the CLI does."""

    def __init__(self, tmp_path) -> None:
        super().__init__()
        self.draft = tmp_path / "state" / "probe" / "summaries" / "project" / "pid" / "sid.md"

    async def run(self, argv, op_id):
        self.calls.append(list(argv))
        if argv[:2] == ["summary", "checkout"]:
            self.draft.parent.mkdir(parents=True, exist_ok=True)
            self.draft.write_text(TEXT)
            return 0, json.dumps(
                {
                    "target": "project",
                    "label": "willow",
                    "path": str(self.draft),
                    "version": 3,
                    "markdown": TEXT,
                    "you": "Richard",
                    "today": "2026-10-15",
                    "edited_by": None,
                    "edited_at": None,
                    "mode": "recorder",
                }
            )
        return 0, json.dumps({"ok": True})


@pytest.fixture
def lean(monkeypatch):
    monkeypatch.setattr(model_mod, "_PUSHED", {})
    monkeypatch.setenv(model_mod.ENV_WRITER_HISTORY, "lean")


def _first_run(tmp_path, monkeypatch, steps=None):
    script = Script(
        steps or [("shell", "probe summary checkout --project willow"), ("done", "loaded it")]
    )
    w = _worker(
        tmp_path,
        model=FunctionModel(script),
        replay=CheckoutReplay(tmp_path),
        mode="conversation",
        monkeypatch=monkeypatch,
    )
    w.read_new()
    assert asyncio.run(w.run_bite("turn end")) is True
    assert w.store.fact(tools.SUMMARY_PIN)["label"] == "willow"
    return w


def _next_message(w, prompt: str) -> str:
    _append_turn(w.session.transcript, prompt)
    script = Script([("done", "nothing new")])
    w._model = FunctionModel(script)
    w.read_new()
    assert asyncio.run(w.run_bite("prompt")) is True
    # The new message is the request's last part (Pydantic AI may hold two user
    # prompts in one request; each goes on the wire as its own message).
    parts = [
        p.content
        for m in script.seen[0][0]
        for p in m.parts
        if isinstance(getattr(p, "content", None), str)
    ]
    return parts[-1]


def test_the_header_is_the_plans():
    assert worker_mod.SUMMARY_PIN_HEADER.format(label="willow", version=3) == HEADER


def test_after_a_lean_run_drops_the_checkout_the_next_message_starts_with_the_pin_once(
    tmp_path, monkeypatch, lean
):
    w = _first_run(tmp_path, monkeypatch)
    assert '"version": 3' not in _live(w)["messages"], "lean history kept no tool result"
    nxt = _next_message(w, "NEXT: run three seeds of B2decay")
    assert nxt.startswith(f"{HEADER}\n\n{TEXT}"), nxt[:300]
    assert "NEXT: run three seeds" in nxt
    again = _next_message(w, "THIRD: compare them")
    assert HEADER not in again, "once: the pin is in the history now"


def test_while_the_checkout_is_still_in_the_history_there_is_no_pin(tmp_path, monkeypatch):
    w = _first_run(tmp_path, monkeypatch)  # full history: tool results stay
    assert str(CheckoutReplay(tmp_path).draft) in _live(w)["messages"]
    assert HEADER not in _next_message(w, "NEXT: run three seeds")


def test_after_a_compaction_cleared_the_checkout_the_pin_comes_back_once(tmp_path, monkeypatch):
    from probe.daemon.events import Event, Kind

    _compacting(monkeypatch)
    w = _first_run(
        tmp_path,
        monkeypatch,
        [
            ("shell", "probe summary checkout --project willow"),
            ("shell", "ls"),
            ("shell", "ls -a"),
            ("done", "loaded it"),
        ],
    )
    assert _live(w)["compactions"] >= 1
    w.store.add(
        [
            Event(
                kind=Kind.AGENT_TEXT, stream="main", offset=900_000, text="NEW after the compaction"
            )
        ]
    )
    _, history, built = w._next_in_conversation("turn end", None)
    assert history and built.prompt.startswith(f"{HEADER}\n\n{TEXT}"), built.prompt[:200]
    assert "NEW after the compaction" in built.prompt


def test_a_landed_push_pins_what_was_pushed(tmp_path, monkeypatch, lean):
    w = _first_run(tmp_path, monkeypatch)
    pin = w.store.fact(tools.SUMMARY_PIN)
    w.store.set_fact(
        tools.SUMMARY_PIN, {**pin, "version": 4, "text": TEXT + "\n## Oct 15 · Richard\n- seeds\n"}
    )
    nxt = _next_message(w, "NEXT")
    assert nxt.startswith("# Summary of willow you loaded (v4)") and "- seeds" in nxt


def test_a_fresh_start_carries_the_pin_in_its_first_message(tmp_path, monkeypatch, lean):
    w = _first_run(tmp_path, monkeypatch)
    w.store.end_conversation(_live(w)["id"], "test: start fresh")
    _append_turn(w.session.transcript, "after the fresh start")
    w.read_new()
    _, history, built = w._next_in_conversation("prompt", None)
    assert history is None and built.prompt.startswith(HEADER)


def test_no_checkout_no_pin(tmp_path, monkeypatch, lean):
    w = _first_run(tmp_path, monkeypatch)
    w.store.set_fact(tools.SUMMARY_PIN, None)
    assert "# Summary of" not in _next_message(w, "NEXT")


def test_the_pin_is_scrubbed_like_the_checkout_it_replaces(tmp_path, monkeypatch, lean):
    """The checkout's tool result went through `scrub`; once lean history or a
    compaction drops it, the pin must not bring a person's quoted key back."""
    w = _first_run(tmp_path, monkeypatch)
    pin = w.store.fact(tools.SUMMARY_PIN)
    w.store.set_fact(tools.SUMMARY_PIN, {**pin, "text": TEXT + "\n> key AKIAIOSFODNN7EXAMPLE\n"})
    nxt = _next_message(w, "NEXT")
    assert nxt.startswith(HEADER) and "AKIAIOSFODNN7EXAMPLE" not in nxt and "<redacted:" in nxt
