"""A follow-up turn on the same worker appends to the tools array it last sent.

Live (system_error prompt_cache_tool_list_changed / tool_inserted_before_existing_tools,
matrx-android on groq, 2026-11-05): turn 1 sent ONE tool; 2 s later turn 2 offered
``context`` first plus two more. The loop end had FORGOTTEN this worker's ledger and the
durable record had not reached the conversation row (a first turn's save is skipped until
the row's INSERT lands), so turn 2 started a fresh ledger in upstream order and ``context``
landed ahead of the tool turn 1 sent: the cached prefix rewritten, the wire guard screamed.

Run end now keeps the ledger (``end_loop``); the LRU bound releases memory and a newer
durable record still wins on hydrate. Fails on the forget-at-loop-end code ("['context',
'x', 'y']" and a guard violation); passes after.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from uuid import uuid4

from matrx_ai.orchestrator import executor
from matrx_ai.providers import cache_guard
from matrx_ai.tools import declaration_ledger


def _decl(name: str) -> dict[str, Any]:
    return {"type": "function", "function": {"name": name, "parameters": {}}}


def _send(conv: str, *names: str) -> list[dict[str, Any]]:
    return declaration_ledger.stabilize_declarations(
        "groq",
        [_decl(n) for n in names],
        name_of=lambda d: d["function"]["name"],
        conversation_id=conv,
        identities={},
    ).declarations


def _names(decls: list[dict[str, Any]]) -> list[str]:
    return [d["function"]["name"] for d in decls]


def test_a_second_loop_on_this_worker_appends_without_a_durable_record(monkeypatch) -> None:
    conv = str(uuid4())
    monkeypatch.setattr(cache_guard, "CACHE_GUARD_ENABLED", True)
    screams: list[str] = []
    monkeypatch.setattr(cache_guard, "_scream_tool_list_change", lambda **kw: screams.append(kw["kind"]))
    monkeypatch.setattr(executor, "_tool_ledger_conversation_id", lambda req: req.conversation_id)

    turn1 = _send(conv, "x")
    assert cache_guard.observe_tool_declarations(provider="groq", conversation_id=conv, payload={"tools": turn1}) is None

    # Turn 1's loop ends; no record reached the row, so turn 2 has nothing to hydrate.
    executor._end_tool_ledger_loop(SimpleNamespace(conversation_id=conv))
    declaration_ledger.hydrate_from_record(conv, None)

    turn2 = _send(conv, "context", "x", "y")
    assert _names(turn2) == ["context", "x", "y"]  # the one name order (P0.2)
    assert cache_guard.observe_tool_declarations(provider="groq", conversation_id=conv, payload={"tools": turn2}) is None
    assert screams == []


def test_loop_end_drops_the_loops_undrained_events() -> None:
    conv = str(uuid4())
    declaration_ledger._queue_events(conv, [{"kind": "tool_definition_updated", "tool": "x"}])
    declaration_ledger.end_loop(conv)
    assert declaration_ledger.drain_events(conv) == []
