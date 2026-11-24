"""A tools array another worker already sent is the conversation's array, not a change.

Live (system_error prompt_cache_tool_list_changed / tool_definition_changed_mid_conversation,
conversation d0a43827, 2026-11-06 03:57Z, ``changed: ["ask_person"]``): the ``ask_person`` tool row was
edited at 03:55:50 (v9 -> v10, its ``kind``/``payload`` descriptions) while the conversation was live.
The next turn ran on ANOTHER worker: its ledger adopted the new definition as a deliberate, recorded break
(excused there) and saved the record. The following turn came back to the first worker: it hydrated that
newer record, so its ledger saw nothing new and recorded no break, but its wire guard still remembered the
OLD block from its own earlier turn and screamed a change the provider had already been sent.

Hydrating a newer record now resets the wire guard's memory of that conversation (the array the provider
last saw is the record's, not this worker's). Fails before (the guard screams
``tool_definition_changed_mid_conversation``); passes after.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from matrx_ai.providers import cache_guard
from matrx_ai.tools import declaration_ledger


def _decl(name: str, description: str = "") -> dict[str, Any]:
    return {"name": name, "description": description, "input_schema": {"type": "object"}}


def _send(conv: str, *decls: dict[str, Any]) -> list[dict[str, Any]]:
    return declaration_ledger.stabilize_declarations(
        "anthropic", list(decls), name_of=lambda d: d["name"], conversation_id=conv, identities={}
    ).declarations


def test_a_definition_another_worker_adopted_is_not_screamed_here(monkeypatch) -> None:
    conv = str(uuid4())
    monkeypatch.setattr(cache_guard, "CACHE_GUARD_ENABLED", True)
    screams: list[str] = []
    monkeypatch.setattr(cache_guard, "_scream_tool_list_change", lambda **kw: screams.append(kw["kind"]))

    # Worker A, turn 1: the old ask_person.
    a1 = _send(conv, _decl("context"), _decl("ask_person", "v9"))
    assert cache_guard.observe_tool_declarations(provider="anthropic", conversation_id=conv, payload={"tools": a1}) is None
    record_a = declaration_ledger.export_record(conv)

    # Worker B, turn 2 (its own memory: only the row's record): the edited tool row -> a recorded break.
    declaration_ledger.forget_conversation(conv)
    declaration_ledger.hydrate_from_record(conv, record_a)
    b2 = _send(conv, _decl("context"), _decl("ask_person", "v10"))
    assert any(e["kind"] == "tool_definition_updated" for e in declaration_ledger.drain_events(conv))
    record_b = declaration_ledger.export_record(conv)
    assert [d["description"] for d in b2] == ["v10", ""]  # ask_person, context: the one name order

    # Back on worker A, turn 3: its ledger is turn 1's; the row carries B's newer record.
    declaration_ledger.forget_conversation(conv)
    declaration_ledger.hydrate_from_record(conv, record_a)
    assert declaration_ledger.hydrate_from_record(conv, record_b) is True
    a3 = _send(conv, _decl("context"), _decl("ask_person", "v10"))
    assert declaration_ledger.drain_events(conv) == []  # nothing new to the conversation
    assert cache_guard.observe_tool_declarations(provider="anthropic", conversation_id=conv, payload={"tools": a3}) is None
    assert screams == []


def test_a_real_change_after_hydrating_still_screams(monkeypatch) -> None:
    conv = str(uuid4())
    monkeypatch.setattr(cache_guard, "CACHE_GUARD_ENABLED", True)
    screams: list[str] = []
    monkeypatch.setattr(cache_guard, "_scream_tool_list_change", lambda **kw: screams.append(kw["kind"]))
    first = [_decl("context"), _decl("ask_person", "v9")]
    assert cache_guard.observe_tool_declarations(provider="anthropic", conversation_id=conv, payload={"tools": first}) is None
    second = [_decl("ask_person", "v9"), _decl("context")]  # reordered, nothing recorded
    assert cache_guard.observe_tool_declarations(provider="anthropic", conversation_id=conv, payload={"tools": second})
    assert screams == ["tool_reordered_mid_conversation"]
